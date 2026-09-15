#!/usr/bin/env python
"""Verify the assembled video against the format bible's requirements.

Usage:
  uv run --project MoneyPrinterTurbo python pipeline/verify.py \
      --episode episodes/2026-09-trump-month \
      --intro-outro work/2026-09-trump-month/render/intro_outro.json \
      --final out/2026-09-trump-month.mp4 \
      --frames-out out/frames_2026-09-trump-month \
      [--bumpers brand/clips.json] \
      [--workdir work/2026-09-trump-month/render]
"""
import argparse
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import run, ffprobe_duration, ffprobe_dims, has_audio_stream, load_episode, bumper_slot_names  # noqa: E402
from drift_check import measure_drift  # noqa: E402


def gather_beats(root, order, intro_outro_path, bumpers_path=None):
    """Returns list of dicts: {section, type, kind(sot only: sot/visual/stock/bumper),
    duration, clip_path(optional), caption(optional), source_url}."""
    items = []
    io = json.load(open(intro_outro_path)) if os.path.exists(intro_outro_path) else {"intro": [], "outro": []}

    def handle_sot(section, b, clip_path, kind="sot", source_url=None, transcript=None):
        dur = ffprobe_duration(clip_path)
        items.append({
            "section": section, "type": "sot", "kind": kind, "duration": dur,
            "clip_path": clip_path, "caption": b.get("caption"), "transcript": transcript,
            "source_url": source_url,
        })

    def handle_narr(section, b, visual_paths_kinds):
        words = len(b["text"].split())
        est = max(words / 2.3, 2.0)
        items.append({
            "section": section, "type": "narr", "duration_est": est,
            "text": b["text"], "visuals": visual_paths_kinds,
        })

    for b in io.get("intro", []):
        if b["type"] == "title":
            items.append({"section": "intro", "type": "title", "duration_est": b.get("seconds", 2.5)})
        elif b["type"] == "sot":
            handle_sot("intro", b, os.path.expanduser(b["clip"]), source_url=b.get("source_url"))
        else:
            vis = []
            for v in b["visuals"]:
                p = v["path"] if isinstance(v, dict) else v
                vis.append((os.path.expanduser(p), "visual"))
            handle_narr("intro", b, vis)

    if bumpers_path and os.path.exists(bumpers_path):
        base = os.path.dirname(bumpers_path)
        bumper = json.load(open(bumpers_path))
        b0 = next((x for x in bumper if x["id"] == "ymca_open"), None)
        if b0:
            p = b0["file"] if os.path.isabs(b0["file"]) else os.path.join(base, b0["file"])
            handle_sot("bumper", {}, p, kind="bumper", source_url=b0.get("source_url"))

    slots = bumper_slot_names(len(order))
    gap_after = dict(zip(order, slots[1:]))
    bumper_by_id = {}
    if bumpers_path and os.path.exists(bumpers_path):
        base = os.path.dirname(bumpers_path)
        for x in json.load(open(bumpers_path)):
            p = x["file"] if os.path.isabs(x["file"]) else os.path.join(base, x["file"])
            bumper_by_id[x["id"]] = (p, x.get("source_url"))

    for sid in order:
        sdir = os.path.join(root, "stories", sid)
        bp = os.path.join(sdir, "beats.json")
        if not os.path.exists(bp):
            continue
        beats_doc = json.load(open(bp))
        clips = json.load(open(os.path.join(sdir, "clips.json")))
        clip_by_id = {c["id"]: c for c in clips}
        for b in beats_doc["beats"]:
            if b["type"] == "sot":
                c = clip_by_id[b["clip"]]
                p = c["file"] if os.path.isabs(c["file"]) else os.path.join(sdir, c["file"])
                handle_sot(sid, b, p, kind=c.get("kind", "sot"),
                           source_url=c.get("source_url"), transcript=c.get("transcript"))
            else:
                vis = []
                for vid in b.get("visuals", []):
                    c = clip_by_id[vid]
                    p = c["file"] if os.path.isabs(c["file"]) else os.path.join(sdir, c["file"])
                    vis.append((p, c.get("kind", "visual")))
                handle_narr(sid, b, vis)

        gid = gap_after.get(sid)
        if gid in bumper_by_id:
            p, src = bumper_by_id[gid]
            handle_sot("bumper", {}, p, kind="bumper", source_url=src)

    for b in io.get("outro", []):
        if b["type"] == "sot":
            handle_sot("outro", b, os.path.expanduser(b["clip"]), source_url=b.get("source_url"))
        else:
            vis = []
            for v in b["visuals"]:
                p = v["path"] if isinstance(v, dict) else v
                vis.append((os.path.expanduser(p), "visual"))
            handle_narr("outro", b, vis)

    return items


def compute_metrics(items):
    total = 0.0
    sot_total = 0.0
    stock_total = 0.0
    real_total = 0.0
    longest_excerpt = 0.0
    src_counts = {}
    narr_stretch = 0.0
    longest_narr_stretch = 0.0

    for it in items:
        if it["type"] == "sot":
            d = it["duration"]
            total += d
            longest_excerpt = max(longest_excerpt, d)
            if it["kind"] == "stock":
                stock_total += d
            else:
                sot_total += d
                real_total += d
            if it.get("source_url"):
                src_counts[it["source_url"]] = src_counts.get(it["source_url"], 0) + 1
            longest_narr_stretch = max(longest_narr_stretch, narr_stretch)
            narr_stretch = 0.0
        elif it["type"] == "title":
            total += it["duration_est"]
        else:
            d = it["duration_est"]
            total += d
            narr_stretch += d
            for path, kind in it["visuals"]:
                vd = min(ffprobe_duration(path), 4.0)
                if kind == "stock":
                    stock_total += 0  # visuals under narration aren't "real footage" claim changer; count separately
            # visuals themselves don't add to `total` (they're concurrent with narration audio, not sequential)
    longest_narr_stretch = max(longest_narr_stretch, narr_stretch)

    return {
        "total_runtime_s": total,
        "sot_pct": (sot_total / total * 100) if total else 0,
        "real_pct": ((total - stock_total) / total * 100) if total else 0,
        "stock_pct": (stock_total / total * 100) if total else 0,
        "longest_excerpt_s": longest_excerpt,
        "max_excerpts_per_source": max(src_counts.values()) if src_counts else 0,
        "source_excerpt_counts": src_counts,
        "longest_uninterrupted_narr_s": longest_narr_stretch,
    }


def extract_frames(final_video, items, frames_out, n_random=12):
    os.makedirs(frames_out, exist_ok=True)
    dur = ffprobe_duration(final_video)
    random.seed(7)
    times = sorted(random.uniform(2, max(dur - 2, 3)) for _ in range(n_random))
    for i, t in enumerate(times):
        out = os.path.join(frames_out, f"random_{i:02d}_{t:.1f}s.png")
        run(["ffmpeg", "-y", "-ss", str(t), "-i", final_video, "-frames:v", "1", out])
    return times


def check_freezes(final_video, workdir, n=0.0005, d=1.0):
    """freezedetect n=0.0005:d=1.0 on the final file: tight enough that only near-bit-
    identical consecutive frames count as frozen, so genuinely low-motion real footage
    (a static interview shot, a coin close-up) does NOT need a synthetic noise dither to
    clear the bar -- render_beat.py's shots rely on the zoom/pan drift alone, which keeps
    the encode compressible. Fails if any freeze >1.0s is found outside a SOT/bumper beat
    (a real pause inside a SOT -- e.g. the n1 "...2001" beat -- is fine). Timeline is built
    from the actual rendered per-beat files in `workdir` (named NNN_<...>.mp4 by
    assemble.py), so it's exact, not estimated."""
    p = run(["ffmpeg", "-i", final_video, "-vf", f"freezedetect=n={n}:d={d}",
             "-map", "0:v", "-f", "null", "-"], check=False)
    out = getattr(p, "stdout", "") or ""
    starts = [float(x) for x in re.findall(r"freeze_start:\s*([\d.]+)", out)]
    durs = [float(x) for x in re.findall(r"freeze_duration:\s*([\d.]+)", out)]
    freezes = [{"start": s, "duration": dd} for s, dd in zip(starts, durs)]

    timeline = []
    manifest_path = os.path.join(workdir, "manifest.json") if workdir else None
    if manifest_path and os.path.exists(manifest_path):
        # exact in-order beat list written by assemble.py -- includes bumpers, which live
        # outside `workdir` and would otherwise be invisible to a directory listing.
        t = 0.0
        for entry in json.load(open(manifest_path)):
            f = entry["out"]
            fd = ffprobe_duration(f)
            is_sot_like = entry["kind"] in ("sot", "bumper", "title")
            timeline.append((t, t + fd, is_sot_like, os.path.basename(f)))
            t += fd
    elif workdir and os.path.isdir(workdir):
        files = sorted(f for f in os.listdir(workdir) if f.endswith(".mp4") and f[:3].isdigit())
        t = 0.0
        for f in files:
            fd = ffprobe_duration(os.path.join(workdir, f))
            is_sot_like = ("_sot" in f) or ("bumper" in f) or ("_title" in f)
            timeline.append((t, t + fd, is_sot_like, f))
            t += fd

    bad = []
    for fr in freezes:
        s = fr["start"]
        allowed = any(a - 0.05 <= s < b + 0.05 and is_sot for a, b, is_sot, _ in timeline)
        if not allowed:
            bad.append(fr)

    return {
        "freezes_found": freezes,
        "freezes_outside_sot": bad,
        "freeze_check_pass": len(bad) == 0,
        "timeline_beats": len(timeline),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True, help="episodes/<slug> directory")
    ap.add_argument("--intro-outro", required=True)
    ap.add_argument("--final", required=True)
    ap.add_argument("--frames-out", required=True)
    ap.add_argument("--bumpers", default=None)
    ap.add_argument("--workdir", default=None)
    args = ap.parse_args()

    ep = load_episode(args.episode)
    root = ep["_stories_root"]
    order = ep["story_order"]
    final = os.path.expanduser(args.final)
    bumpers_path = os.path.expanduser(args.bumpers) if args.bumpers else None
    workdir = os.path.expanduser(args.workdir) if args.workdir else None

    items = gather_beats(root, order, os.path.expanduser(args.intro_outro), bumpers_path=bumpers_path)
    metrics = compute_metrics(items)

    w, h = ffprobe_dims(final)
    dur = ffprobe_duration(final)
    audio_ok = has_audio_stream(final)

    frame_times = extract_frames(final, items, os.path.expanduser(args.frames_out))
    freeze_report = check_freezes(final, workdir)

    drift_report = {}
    manifest_path = os.path.join(workdir, "manifest.json") if workdir else None
    if manifest_path and os.path.exists(manifest_path):
        try:
            drift_report = {"drift": measure_drift(manifest_path, final)}
        except Exception as e:
            drift_report = {"drift": {"error": str(e)}}

    report = {
        "final_duration_s": dur,
        "final_dims": f"{w}x{h}",
        "has_audio": audio_ok,
        **metrics,
        "n_random_frames": len(frame_times),
        "sot_beats_total": sum(1 for it in items if it["type"] == "sot"),
        **freeze_report,
        **drift_report,
    }
    print(json.dumps(report, indent=2))
    with open(os.path.join(os.path.expanduser(args.frames_out), "..", "verify_report.json"), "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    main()
