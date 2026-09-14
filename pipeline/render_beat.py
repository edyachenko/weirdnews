#!/usr/bin/env python
"""Render one beat (narr or sot) to a normalized 1920x1080/30fps/yuv420p mp4 with audio.

narr beat:
  uv run --project .../MoneyPrinterTurbo python render_beat.py narr \
    --text "..." --visuals clipA.mp4:0.2:3.4 clipB.mp4 ... \
    --out beat.mp4 [--plate lt.png --plate-seconds 3.5] --bug bug.png \
    [--extra-pool more1.mp4 more2.mp4 ...] [--voice NAME --rate -8% --pitch -3Hz] \
    [--tts-cache-dir DIR]

  Each --visuals entry is "path[:in_sec[:dur_sec]]". If in/dur omitted, the whole clip is used
  (clipped to <=4s). Shots are shown 2-4s each, muted, cut to exactly fill the narration duration.
  --extra-pool is a fallback list (other visuals from the same story, then its SOT clips) used
  to keep cycling real footage if the primary --visuals run out before the narration does.
  Frames are NEVER frozen/held to pad: the visual track always either shows more real footage
  or, only once that pool is genuinely exhausted, a slow zoom/pan drift over looped real footage.

sot beat:
  uv run --project .../MoneyPrinterTurbo python render_beat.py sot \
    --clip clip.mp4 --caption "exact words" --label "via CNN" --banner bottom \
    --out beat.mp4 --bug bug.png
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from common import (  # noqa: E402
    W, H, FPS, ROOT, run, ffprobe_duration, is_4x3_or_portrait, scale_crop_filter,
    NORMALIZE_V, loudnorm_filter,
)
import plates  # noqa: E402

PIPELINE_DIR = os.path.dirname(__file__)
MPT_PROJECT = os.path.join(ROOT, "MoneyPrinterTurbo")
DEFAULT_VOICE = "en-US-AndrewNeural"

# Per-process cache: source path -> usable duration before any trailing freeze.
_FREEZE_CACHE = {}


def uv_python(*args):
    return ["uv", "run", "--project", MPT_PROJECT, "python", *args]


def usable_duration(path, tail_window=4.0):
    """Full source duration, clamped to exclude a trailing frozen tail (freezedetect
    n=0.0005:d=1.0, same threshold verify.py checks). A freeze run that reaches the end
    of the file (no freeze_end logged) is trimmed off; a mid-clip freeze is left alone."""
    if path in _FREEZE_CACHE:
        return _FREEZE_CACHE[path]
    dur = ffprobe_duration(path)
    p = run(["ffmpeg", "-i", path, "-vf", "freezedetect=n=0.0005:d=1.0",
             "-map", "0:v", "-f", "null", "-"], check=False)
    out = getattr(p, "stdout", "") or ""
    starts = [float(x) for x in re.findall(r"freeze_start:\s*([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"freeze_end:\s*([\d.]+)", out)]
    usable = dur
    if len(starts) > len(ends) and starts:
        # last freeze never resolved -> it runs to EOF; trim it off if it's near the tail
        tail_start = starts[-1]
        if tail_start >= dur - tail_window - 1.0:
            usable = max(tail_start, 0.5)
    _FREEZE_CACHE[path] = usable
    return usable


def gen_tts(text, out_mp3, out_captions, voice=DEFAULT_VOICE, rate=None, pitch=None, cache_dir=None):
    """Generate (or reuse a cached) narration mp3 + captions for (voice, rate, pitch, text)."""
    if cache_dir:
        key = hashlib.sha256(
            json.dumps({"v": voice, "r": rate, "p": pitch, "t": text}, sort_keys=True).encode()
        ).hexdigest()[:24]
        cdir = os.path.join(cache_dir, key)
        cmp3 = os.path.join(cdir, "narr.mp3")
        ccaps = os.path.join(cdir, "narr.captions.json")
        cinfo = os.path.join(cdir, "info.json")
        if os.path.exists(cmp3) and os.path.exists(ccaps) and os.path.exists(cinfo):
            shutil.copy(cmp3, out_mp3)
            shutil.copy(ccaps, out_captions)
            return json.load(open(cinfo))

    cmd = uv_python(
        os.path.join(PIPELINE_DIR, "tts.py"),
        "--text", text, "--out", out_mp3, "--captions", out_captions, "--voice", voice,
    )
    if rate:
        cmd += [f"--rate={rate}"]
    if pitch:
        cmd += [f"--pitch={pitch}"]
    p = run(cmd)
    info = json.loads(p.stdout.strip().splitlines()[-1])

    if cache_dir:
        os.makedirs(cdir, exist_ok=True)
        shutil.copy(out_mp3, cmp3)
        shutil.copy(out_captions, ccaps)
        with open(cinfo, "w") as f:
            json.dump(info, f)
    return info


def make_shot(src, in_sec, dur, out_path):
    """Cut+cover-crop a shot, with a barely-perceptible continuous zoom drift
    (<=~1.06x over a 5s shot) so a naturally low-motion source (a static product/coin
    shot, a still interview talking head) still has real per-frame motion. No synthetic
    noise dither: verify.py's freezedetect threshold (n=0.0005) is tight enough that this
    zoom alone clears it, and skipping the dither keeps the encode compressible (dithered
    grain is incompressible and was the main driver of oversized renders)."""
    base = scale_crop_filter(is_4x3_or_portrait(src))
    vf = (
        f"{base},fps={FPS},scale=iw*1.08:ih*1.08,"
        f"zoompan=z='min(zoom+0.0002,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={W}x{H}:fps={FPS},format=yuv420p"
    )
    cmd = ["ffmpeg", "-y"]
    if in_sec is not None:
        cmd += ["-ss", str(in_sec)]
    cmd += ["-i", src, "-t", str(dur), "-vf", vf, "-an",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out_path]
    run(cmd)


def make_shot_with_zoom(src, in_sec, dur, out_path):
    """Last-resort fill: loop real footage (never a still) with a slow zoom/pan drift,
    for when the whole story's visual+SOT pool has been exhausted and narration remains.
    Never freezes a frame -- the source keeps playing (looped if needed) under the zoom."""
    base_vf = scale_crop_filter(is_4x3_or_portrait(src))
    zoom_vf = (
        f"{base_vf},scale=iw*1.3:ih*1.3,"
        f"zoompan=z='min(zoom+0.0009,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={W}x{H}:fps={FPS},format=yuv420p"
    )
    cmd = ["ffmpeg", "-y", "-stream_loop", "-1"]
    if in_sec is not None:
        cmd += ["-ss", str(in_sec)]
    cmd += ["-i", src, "-t", str(dur), "-vf", zoom_vf, "-an",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out_path]
    run(cmd)


def concat_shots(shot_paths, out_path):
    """Re-encode across the join (not -c copy): stream-copying independently-encoded
    shots through the concat demuxer can duplicate/stall a frame right at the splice
    (non-monotonic timestamps from mismatched GOPs), which freezedetect then reports as
    a frozen frame even though nothing in our own code held a static frame there."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in shot_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
        listfile = f.name
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
         "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "18",
         "-preset", "veryfast", out_path])
    os.unlink(listfile)


def build_visuals_track(visuals, total_dur, tmpdir, extra_pool=None):
    """visuals: list of (path, in_sec_or_None, dur_or_None) -- the beat's own explicit shots.
    extra_pool: fallback list of source paths (other visuals from the story first, then its
    SOT clips muted) cycled in when `visuals` runs out before total_dur is covered. Only once
    extra_pool is also exhausted does the last shot extend via a slow zoom on looped real
    footage (make_shot_with_zoom) -- the track never holds/freezes a static frame to pad.
    Returns path to a silent 1920x1080@30fps video track exactly total_dur seconds long."""
    extra_pool = extra_pool or []
    shots = []
    shot_meta = []  # (src, in_sec, dur) per shot, for the zoom fallback
    remaining = total_dur

    def add_shot(src, in_sec, dur):
        nonlocal remaining
        idx = len(shots)
        shot_path = os.path.join(tmpdir, f"shot_{idx:02d}.mp4")
        make_shot(src, in_sec, dur, shot_path)
        shots.append(shot_path)
        shot_meta.append((src, in_sec, dur))
        remaining -= dur

    # Phase A: the beat's own explicit visuals, each capped to a natural 2-4s shot
    # (or the whole remaining time if there's only one).
    n = max(1, len(visuals))
    target = total_dur if n == 1 else min(max(total_dur / n, 2.0), 4.0)
    for path, in_sec, dur in visuals:
        if remaining <= 0.05:
            break
        src_dur = ffprobe_duration(path)
        req_in = in_sec if in_sec is not None else 0.0
        avail = max(src_dur - req_in, 0.3)
        this_target = dur if dur is not None else target
        use_dur = min(this_target, avail, 5.0, remaining)
        use_dur = max(use_dur, 0.5)
        add_shot(path, req_in, use_dur)

    # Phase B: primary visuals ran dry but narration hasn't -- cycle the extra pool
    # (other real footage from the same story), 2-4s shots, varying the in-point each
    # lap through the pool so repeats don't look identical.
    guard = 0
    pool_idx = 0
    while remaining > 0.05 and extra_pool and guard < 100:
        guard += 1
        path = extra_pool[pool_idx % len(extra_pool)]
        lap = pool_idx // len(extra_pool)
        pool_idx += 1
        src_dur = usable_duration(path)
        in_sec = (lap * (src_dur * 0.4)) % max(src_dur - 1.0, 0.3)
        avail = max(src_dur - in_sec, 0.3)
        use_dur = min(max(min(remaining, 4.0), 2.0), avail, 5.0, remaining)
        use_dur = max(use_dur, 0.5)
        add_shot(path, in_sec, use_dur)

    # Phase C: story pool truly exhausted (or there was never any footage at all) but
    # narration still isn't covered -- extend the last real shot with a slow zoom over
    # looped footage instead of freezing a frame.
    if remaining > 0.05:
        if shot_meta:
            src, in_sec, dur = shot_meta[-1]
            extra = remaining
            new_dur = dur + extra
            zoom_path = os.path.join(tmpdir, f"shot_{len(shots)-1:02d}_zoom.mp4")
            make_shot_with_zoom(src, in_sec, new_dur, zoom_path)
            shots[-1] = zoom_path
        else:
            # no footage at all was supplied -- degenerate case, zoom on a black clip
            # is pointless, so just synthesize a plain color track (never a frozen photo).
            zoom_path = os.path.join(tmpdir, "shot_black.mp4")
            run(["ffmpeg", "-y", "-f", "lavfi",
                 "-i", f"color=c=black:s={W}x{H}:d={total_dur}:r={FPS}",
                 "-vf", "format=yuv420p", zoom_path])
            shots = [zoom_path]
        remaining = 0.0

    concat_path = os.path.join(tmpdir, "visuals_concat.mp4")
    concat_shots(shots, concat_path)
    actual = ffprobe_duration(concat_path)
    fixed_path = os.path.join(tmpdir, "visuals_fixed.mp4")
    if actual < total_dur - 0.05:
        # Should be rare now (Phase C covers the general case), but guard against small
        # rounding gaps the same way -- with a zoom on the tail, not a freeze clone.
        if shot_meta:
            src, in_sec, _ = shot_meta[-1]
            make_shot_with_zoom(src, in_sec, total_dur, fixed_path)
        else:
            run(["ffmpeg", "-y", "-i", concat_path,
                 "-vf", f"tpad=stop_mode=clone:stop_duration={total_dur - actual}",
                 "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", fixed_path])
    else:
        run(["ffmpeg", "-y", "-i", concat_path, "-t", str(total_dur),
             "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", fixed_path])
    return fixed_path


def overlay_chain(base_video, overlays, out_path, audio_path=None, audio_trim=None):
    """overlays: list of (png_path, start, end_or_None). end None = whole duration."""
    cmd = ["ffmpeg", "-y", "-i", base_video]
    for png, _, _ in overlays:
        cmd += ["-i", png]
    if audio_path:
        cmd += ["-i", audio_path]
    filt_parts = []
    cur = "0:v"
    for i, (png, start, end) in enumerate(overlays, start=1):
        outlbl = f"v{i}"
        if end is None:
            enable = ""
        else:
            enable = f":enable='between(t,{start},{end})'"
        filt_parts.append(f"[{cur}][{i}:v]overlay=0:0{enable}[{outlbl}]")
        cur = outlbl
    filt = ";".join(filt_parts)
    cmd += ["-filter_complex", filt, "-map", f"[{cur}]"]
    if audio_path:
        aidx = len(overlays) + 1
        cmd += ["-map", f"{aidx}:a"]
    cmd += ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p"]
    if audio_path:
        cmd += ["-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k", "-shortest"]
    else:
        cmd += ["-an"]
    cmd += [out_path]
    run(cmd)


def render_narr(args):
    tmpdir = tempfile.mkdtemp(prefix="narr_")
    mp3 = os.path.join(tmpdir, "narr.mp3")
    caps_json = os.path.join(tmpdir, "narr.captions.json")
    info = gen_tts(args.text, mp3, caps_json, voice=args.voice, rate=args.rate,
                    pitch=args.pitch, cache_dir=args.tts_cache_dir)
    dur = info["duration"] + 0.15

    visuals = []
    for v in args.visuals:
        parts = v.split(":")
        path = parts[0]
        in_sec = float(parts[1]) if len(parts) > 1 and parts[1] else None
        d = float(parts[2]) if len(parts) > 2 and parts[2] else None
        visuals.append((path, in_sec, d))

    used_paths = {p for p, _, _ in visuals}
    extra_pool = [p for p in (args.extra_pool or []) if p not in used_paths]

    visuals_track = build_visuals_track(visuals, dur, tmpdir, extra_pool=extra_pool)

    caps = json.load(open(caps_json))["captions"]
    overlays = []
    for i, c in enumerate(caps):
        lines = c["text"].split("\n")
        png = os.path.join(tmpdir, f"cap_{i:02d}.png")
        plates.caption_box(lines, png, position="bottom")
        overlays.append((png, c["start"], c["end"]))

    if args.plate:
        overlays.append((args.plate, 0, args.plate_seconds))
    if args.bug:
        overlays.append((args.bug, None, None))

    overlay_chain(visuals_track, overlays, args.out, audio_path=mp3)
    print(json.dumps({"ok": True, "duration": dur, "out": args.out}))


def render_sot(args):
    tmpdir = tempfile.mkdtemp(prefix="sot_")
    src_dur = usable_duration(args.clip)
    dur = min(src_dur, 5.0)

    vf = scale_crop_filter(is_4x3_or_portrait(args.clip)) + f",fps={FPS},format=yuv420p"
    normed = os.path.join(tmpdir, "normed.mp4")
    run(["ffmpeg", "-y", "-i", args.clip, "-t", str(dur), "-vf", vf,
         "-af", loudnorm_filter(), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
         "-c:a", "aac", "-ar", "48000", "-ac", "2", normed])

    from common import wrap_caption
    lines = wrap_caption(args.caption)
    cap_png = os.path.join(tmpdir, "cap.png")
    cap_position = "top" if args.banner == "bottom" else "bottom"
    plates.caption_box(lines, cap_png, position=cap_position)

    overlays = [(cap_png, None, None)]
    if args.label:
        label_png = os.path.join(tmpdir, "label.png")
        plates.label_topleft(args.label, label_png)
        overlays.append((label_png, None, None))
    if args.bug:
        overlays.append((args.bug, None, None))

    overlay_chain(normed, overlays, args.out, audio_path=normed)
    print(json.dumps({"ok": True, "duration": dur, "out": args.out}))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    pn = sub.add_parser("narr")
    pn.add_argument("--text", required=True)
    pn.add_argument("--visuals", nargs="+", required=True)
    pn.add_argument("--extra-pool", nargs="*", default=None)
    pn.add_argument("--out", required=True)
    pn.add_argument("--plate", default=None)
    pn.add_argument("--plate-seconds", type=float, default=3.5)
    pn.add_argument("--bug", default=None)
    pn.add_argument("--voice", default=DEFAULT_VOICE)
    pn.add_argument("--rate", default=None)
    pn.add_argument("--pitch", default=None)
    pn.add_argument("--tts-cache-dir", default=None)

    ps = sub.add_parser("sot")
    ps.add_argument("--clip", required=True)
    ps.add_argument("--caption", required=True)
    ps.add_argument("--label", default=None)
    ps.add_argument("--banner", default="none", choices=["none", "top", "bottom"])
    ps.add_argument("--out", required=True)
    ps.add_argument("--bug", default=None)

    args = ap.parse_args()
    if args.cmd == "narr":
        render_narr(args)
    else:
        render_sot(args)


if __name__ == "__main__":
    main()
