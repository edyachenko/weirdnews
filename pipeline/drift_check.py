#!/usr/bin/env python
"""Measure audio-vs-video drift in the final assembled episode.

The old verification (global duration match + freeze check) passed on all four shipped
episodes even though audio was measurably lagging video by the end, worse on longer
episodes -- because both checks only ever look at totals, never at WHERE a given beat's
audio actually lands on the timeline. This script checks that directly: for a handful of
checkpoint beats spread through the episode, it cross-correlates that beat's OWN rendered
audio (still cached in work/<slug>/render/*.mp4) against a window of the final file's audio
around the beat's manifest-expected start time (cumulative sum of every prior beat's own
duration), and reports the offset in milliseconds.

Root cause this was written to catch: both concat points in the pipeline
(render_beat.py's concat_shots, assemble.py's concat_and_normalize) used to go through the
ffmpeg concat DEMUXER, which stitches by raw packet/duration continuity -- reliable only
for homogeneous-parameter inputs. Source clips have heterogeneous native frame rates
(29.97/25/30/60fps); concatenating shots cut from them let each beat's internal splice
carry a tiny (sub-frame) timing error, and concatenating ~65-70 of those beats compounded
that error into several hundred ms of drift by the end of a ~380s episode. Both concat
points now use the concat FILTER instead (decoded frames, PTS reset per input) -- this
script is how that fix is proven, not just asserted.

Usage:
  uv run --project MoneyPrinterTurbo python pipeline/drift_check.py \
      --manifest work/2026-09-trump-month/render/manifest.json \
      --final out/2026-09-trump-month.mp4 \
      [--checkpoints 10] [--margin 2.5]
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import exact_video_duration  # noqa: E402

SR = 16000
HOP_S = 0.01


def extract_pcm(path, start=None, duration=None, sr=SR):
    cmd = ["ffmpeg", "-y"]
    if start is not None:
        cmd += ["-ss", str(max(start, 0.0))]
    cmd += ["-i", path]
    if duration is not None:
        cmd += ["-t", str(duration)]
    cmd += ["-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-acodec", "pcm_s16le", "-"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return np.frombuffer(p.stdout, dtype=np.int16).astype(np.float64)


def envelope(samples, sr=SR, hop_s=HOP_S):
    """RMS energy envelope at hop_s resolution -- tracks loudness shape, small enough to
    brute-force cross-correlate, and robust to the final loudnorm pass changing absolute
    level (envelopes are z-scored before correlating)."""
    hop = max(1, int(sr * hop_s))
    n = len(samples) // hop
    if n == 0:
        return np.array([])
    trimmed = samples[: n * hop].reshape(n, hop)
    return np.sqrt(np.mean(trimmed ** 2, axis=1) + 1e-9)


def zscore(x):
    x = x - x.mean()
    s = x.std()
    return x / s if s > 1e-9 else x


def find_offset(window_env, ref_env):
    """Index (in hops) into window_env where ref_env's envelope best matches, by
    normalized cross-correlation. Returns (offset_index, match_score)."""
    if len(ref_env) == 0 or len(window_env) < len(ref_env):
        return None, None
    w = zscore(window_env)
    r = zscore(ref_env)
    corr = np.correlate(w, r, mode="valid")
    idx = int(np.argmax(corr))
    score = float(corr[idx] / len(r))
    return idx, score


def has_signal(samples, thresh=50.0):
    return len(samples) > 0 and float(np.sqrt(np.mean(samples ** 2))) > thresh


def measure_drift(manifest_path, final_video, n_checkpoints=10, margin=2.5, ref_len=2.0):
    manifest = json.load(open(manifest_path))

    entries = []
    t = 0.0
    for e in manifest:
        # same duration definition concat_and_normalize uses to clamp each input's audio
        # (frame-count/fps, not the container's format=duration) so "expected" here means
        # exactly what the fixed concat actually produces.
        dur = exact_video_duration(e["out"])
        entries.append({"out": e["out"], "kind": e["kind"], "start": t, "dur": dur})
        t += dur
    total = t

    # title cards are silent (anullsrc) -- useless as a correlation reference. Bumpers are
    # a short looped music/song clip (Y.M.C.A.-style) -- its periodic rhythm makes
    # cross-correlation prone to locking onto the wrong repeat (a false multi-hundred-ms
    # "drift" that is really just the song's own beat), so only narr/sot beats (speech,
    # non-periodic) are used as checkpoints.
    candidates = [e for e in entries if e["kind"] in ("narr", "sot") and e["dur"] >= ref_len + 0.3]
    if not candidates:
        return {"error": "no usable checkpoint beats found", "total_duration_s": total}

    if len(candidates) <= n_checkpoints:
        chosen = list(candidates)
    else:
        step = (len(candidates) - 1) / (n_checkpoints - 1)
        picked_idx = sorted({round(i * step) for i in range(n_checkpoints)})
        chosen = [candidates[i] for i in picked_idx]
    # the last checkpoint is the one that matters most -- drift accumulates, so the worst
    # case is always near the end. Make sure it's always included.
    if candidates[-1]["out"] not in {c["out"] for c in chosen}:
        chosen.append(candidates[-1])

    results = []
    for e in chosen:
        ref = extract_pcm(e["out"], start=0.0, duration=min(ref_len, e["dur"] - 0.05))
        if not has_signal(ref):
            continue
        ref_env = envelope(ref)

        expected = e["start"]
        win_start = max(expected - margin, 0.0)
        win_dur = min(ref_len, e["dur"]) + 2 * margin
        window = extract_pcm(final_video, start=win_start, duration=win_dur)
        win_env = envelope(window)

        idx, score = find_offset(win_env, ref_env)
        if idx is None:
            continue
        actual = win_start + idx * HOP_S
        drift_ms = (actual - expected) * 1000.0
        results.append({
            "beat": os.path.basename(e["out"]), "kind": e["kind"],
            "expected_s": round(expected, 3), "actual_s": round(actual, 3),
            "drift_ms": round(drift_ms, 1), "match_score": round(score, 3),
        })

    max_drift = max((abs(r["drift_ms"]) for r in results), default=None)
    return {
        "total_duration_s": round(total, 3),
        "n_checkpoints": len(results),
        "checkpoints": results,
        "max_drift_ms": max_drift,
        "pass_under_50ms": (max_drift is not None and max_drift < 50.0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--final", required=True)
    ap.add_argument("--checkpoints", type=int, default=10)
    ap.add_argument("--margin", type=float, default=2.5)
    args = ap.parse_args()
    report = measure_drift(
        os.path.expanduser(args.manifest), os.path.expanduser(args.final),
        n_checkpoints=args.checkpoints, margin=args.margin,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
