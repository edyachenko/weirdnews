#!/usr/bin/env python
"""Render every beat (intro, the episode's stories, outro) and concatenate into the final video.

Usage:
  uv run --project MoneyPrinterTurbo python pipeline/assemble.py \
      --episode episodes/2026-09-trump-month \
      --intro-outro work/2026-09-trump-month/render/intro_outro.json \
      --work work/2026-09-trump-month/render \
      --out out/2026-09-trump-month.mp4 \
      --max-parallel 4
"""
import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from common import run, ffprobe_duration, load_episode, bumper_slot_names, ROOT  # noqa: E402
import plates  # noqa: E402

PIPELINE_DIR = os.path.dirname(__file__)
MPT_PROJECT = os.path.join(ROOT, "MoneyPrinterTurbo")


def uv_python(*args):
    return ["uv", "run", "--project", MPT_PROJECT, "python", *[str(a) for a in args]]


def resolve_visual_arg(path, in_s=None, dur=None):
    s = path
    if in_s is not None or dur is not None:
        s += f":{in_s if in_s is not None else ''}:{dur if dur is not None else ''}"
    return s


def render_title_card(png_path, out_path, seconds, bug_png=None):
    """Title card: a Pillow PNG (with alpha) over black for `seconds`, with a subtle slow
    zoom so it's never a dead-static hold (Change 2: no frozen frames anywhere)."""
    vf = f"[0:v]scale={1920}:{1080}[bg]"
    inputs = ["-f", "lavfi", "-i", f"color=c=black:s=1920x1080:d={seconds}:r=30", "-i", png_path]
    filt = "[0:v][1:v]overlay=0:0[v0]"
    idx = 1
    if bug_png:
        inputs += ["-i", bug_png]
        idx += 1
        filt += f";[v0][{idx}:v]overlay=0:0[v1]"
        outlbl = "v1"
    else:
        outlbl = "v0"
    # subtle continuous zoom-in (1.0x -> ~1.06x over the card's duration)
    filt += (
        f";[{outlbl}]scale=iw*1.06:ih*1.06,"
        f"zoompan=z='min(zoom+0.0012,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s=1920x1080:fps=30[vz]"
    )
    cmd = ["ffmpeg", "-y", *inputs,
           "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo",
           "-filter_complex", filt, "-map", "[vz]", "-map", f"{idx+1}:a",
           "-t", str(seconds), "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k", "-shortest", out_path]
    run(cmd)
    return out_path


def render_one_beat(job, tts_opts=None):
    """job: dict with 'kind': 'narr'|'sot'|'title'|'bumper', plus args, plus 'out' path."""
    if job["kind"] == "bumper":
        return job["out"]  # pre-rendered by build_ymca_bumpers.py, used as-is
    if os.path.exists(job["out"]) and job.get("skip_if_exists"):
        return job["out"]
    if job["kind"] == "title":
        render_title_card(job["png"], job["out"], job.get("seconds", 2.5), bug_png=job.get("bug"))
        return job["out"]
    if job["kind"] == "narr":
        cmd = uv_python(
            os.path.join(PIPELINE_DIR, "render_beat.py"), "narr",
            "--text", job["text"],
            "--visuals", *job["visuals"],
            "--out", job["out"],
            "--bug", job["bug"],
        )
        if job.get("extra_pool"):
            cmd += ["--extra-pool", *job["extra_pool"]]
        if job.get("plate"):
            cmd += ["--plate", job["plate"], "--plate-seconds", str(job.get("plate_seconds", 3.5))]
        if tts_opts:
            if tts_opts.get("voice"):
                cmd += ["--voice", tts_opts["voice"]]
            if tts_opts.get("rate"):
                cmd += [f"--rate={tts_opts['rate']}"]
            if tts_opts.get("pitch"):
                cmd += [f"--pitch={tts_opts['pitch']}"]
            if tts_opts.get("cache_dir"):
                cmd += ["--tts-cache-dir", tts_opts["cache_dir"]]
    else:
        cmd = uv_python(
            os.path.join(PIPELINE_DIR, "render_beat.py"), "sot",
            "--clip", job["clip"],
            "--caption", job["caption"],
            "--banner", job.get("banner", "none"),
            "--out", job["out"],
            "--bug", job["bug"],
        )
        if job.get("label"):
            cmd += ["--label", job["label"]]
    run(cmd)
    return job["out"]


def load_all_story_clips(root, order):
    """sid -> (sdir, clip_by_id) for every story in order, loaded once so intro/outro
    narr beats can draw a cross-story fallback pool (Change 2: never freeze a frame)."""
    out = {}
    for sid in order:
        sdir = os.path.join(root, "stories", sid)
        cp = os.path.join(sdir, "clips.json")
        if not os.path.exists(cp):
            continue
        clips = json.load(open(cp))
        out[sid] = (sdir, {c["id"]: c for c in clips})
    return out


def bumper_map(bumpers, bumpers_path=None):
    """bumpers: list of clip dicts from a brand/clips.json-style bumper list (id, file, ...).
    Returns {name: (absolute_path, meta)}. Relative `file` entries resolve against the
    bumpers file's own directory (brand/rendered/, written by build_brand_bumpers.py)."""
    if not bumpers:
        return {}
    base = os.path.dirname(bumpers_path) if bumpers_path else os.path.join(ROOT, "brand", "rendered")
    m = {}
    for b in bumpers:
        p = b["file"]
        if not os.path.isabs(p):
            p = os.path.join(base, p)
        m[b["id"]] = (p, b)
    return m


def build_jobs(root, order, intro_outro_path, workdir, bug_png, bumpers=None, bumpers_path=None):
    jobs = []
    credits = []
    all_story_clips = load_all_story_clips(root, order)
    # flat pool of every real (non-bumper) clip path across all stories, for intro/outro
    all_clip_paths = []
    for sid, (sdir, clip_by_id) in all_story_clips.items():
        for c in clip_by_id.values():
            p = c["file"]
            if not os.path.isabs(p):
                p = os.path.join(sdir, p)
            all_clip_paths.append(p)

    bmap = bumper_map(bumpers, bumpers_path=bumpers_path)

    def clip_path_from_id(sdir, clip_by_id, cid):
        c = clip_by_id[cid]
        p = c["file"]
        if not os.path.isabs(p):
            p = os.path.join(sdir, p)
        return p, c

    idx = [0]

    def next_out(prefix):
        idx[0] += 1
        return os.path.join(workdir, f"{idx[0]:03d}_{prefix}.mp4")

    def add_bumper(name):
        if name not in bmap:
            return
        path, meta = bmap[name]
        jobs.append({"kind": "bumper", "out": path})
        credits.append({
            "section": "bumper", "channel": meta.get("channel", ""),
            "title": meta.get("title", ""), "url": meta.get("source_url", ""),
        })

    io = json.load(open(intro_outro_path))

    # --- intro ---
    for b in io.get("intro", []):
        if b["type"] == "title":
            jobs.append({
                "kind": "title", "png": os.path.expanduser(b["png"]),
                "seconds": b.get("seconds", 2.5), "out": next_out("intro_title"), "bug": bug_png,
            })
        elif b["type"] == "sot":
            jobs.append({
                "kind": "sot", "clip": os.path.expanduser(b["clip"]), "caption": b["caption"],
                "label": b.get("label"), "banner": b.get("banner", "none"),
                "out": next_out("intro_sot"), "bug": bug_png,
            })
            if b.get("source_url"):
                credits.append({"section": "intro", "channel": b.get("channel", ""), "title": b.get("title", ""), "url": b["source_url"]})
        else:
            visuals = []
            used = set()
            for v in b["visuals"]:
                if isinstance(v, dict):
                    p = os.path.expanduser(v["path"])
                    visuals.append(resolve_visual_arg(p, v.get("in"), v.get("dur")))
                    used.add(p)
                    if v.get("source_url"):
                        credits.append({"section": "intro", "channel": v.get("channel", ""), "title": v.get("title", ""), "url": v["source_url"]})
                else:
                    p = os.path.expanduser(v)
                    visuals.append(p)
                    used.add(p)
            jobs.append({
                "kind": "narr", "text": b["text"], "visuals": visuals,
                "extra_pool": [p for p in all_clip_paths if p not in used],
                "plate": os.path.expanduser(b["plate"]) if b.get("plate") else None,
                "out": next_out("intro_narr"), "bug": bug_png,
            })

    # --- the episode's stories, with a Y.M.C.A. bumper before the first, between each
    # consecutive pair, and after the last ---
    slots = bumper_slot_names(len(order))
    add_bumper(slots[0])  # ymca_open
    for story_i, sid in enumerate(order):
        sdir, clip_by_id = all_story_clips[sid]
        beats_doc = json.load(open(os.path.join(sdir, "beats.json")))
        number = beats_doc["number"]
        headline = beats_doc["headline"]
        for src in beats_doc.get("sources", []):
            credits.append({"section": sid, "channel": src.get("outlet", ""), "title": beats_doc["headline"], "url": src.get("url", "")})

        plate_png = os.path.join(workdir, f"plate_{sid}.png")
        plates.lower_third(number, headline, plate_png)

        # this story's own fallback pool: its other visual clips first, then its SOT clips
        # (muted), in clips.json order -- used when a narr beat's explicit visuals run out.
        # clips.json ids follow the "<sid>_sot_*" / "<sid>_visual_*" convention; fall back
        # to the explicit "kind" field when id-sniffing is inconclusive.
        story_visual_paths, story_sot_paths = [], []
        for cid, c in clip_by_id.items():
            p = c["file"]
            if not os.path.isabs(p):
                p = os.path.join(sdir, p)
            if "_sot_" in cid or c.get("kind") == "sot":
                story_sot_paths.append(p)
            else:
                story_visual_paths.append(p)
        story_pool = story_visual_paths + story_sot_paths

        first = True
        for b in beats_doc["beats"]:
            if b["type"] == "sot":
                path, c = clip_path_from_id(sdir, clip_by_id, b["clip"])
                job = {
                    "kind": "sot", "clip": path, "caption": b["caption"],
                    "label": b.get("label"), "banner": c.get("banner", "none"),
                    "out": next_out(f"{sid}_sot"), "bug": bug_png,
                }
                if c.get("source_url"):
                    credits.append({"section": sid, "channel": c.get("channel", ""), "title": c.get("title", ""), "url": c["source_url"]})
            else:
                visuals = []
                used = set()
                for vid in b.get("visuals", []):
                    path, c = clip_path_from_id(sdir, clip_by_id, vid)
                    visuals.append(path)
                    used.add(path)
                    if c.get("source_url"):
                        credits.append({"section": sid, "channel": c.get("channel", ""), "title": c.get("title", ""), "url": c["source_url"]})
                job = {
                    "kind": "narr", "text": b["text"], "visuals": visuals,
                    "extra_pool": [p for p in story_pool if p not in used],
                    "out": next_out(f"{sid}_narr"), "bug": bug_png,
                }
                if first:
                    job["plate"] = plate_png
                    job["plate_seconds"] = 3.5
                    first = False
            jobs.append(job)

        add_bumper(slots[story_i + 1])

    # brand gag after all stories: the same Biden clip every episode
    add_bumper("biden_end")

    # --- outro ---
    for b in io.get("outro", []):
        if b["type"] == "sot":
            jobs.append({
                "kind": "sot", "clip": os.path.expanduser(b["clip"]), "caption": b["caption"],
                "label": b.get("label"), "banner": b.get("banner", "none"),
                "out": next_out("outro_sot"), "bug": bug_png,
            })
        else:
            visuals = []
            used = set()
            for v in b["visuals"]:
                if isinstance(v, dict):
                    p = os.path.expanduser(v["path"])
                    visuals.append(resolve_visual_arg(p, v.get("in"), v.get("dur")))
                    used.add(p)
                else:
                    p = os.path.expanduser(v)
                    visuals.append(p)
                    used.add(p)
            jobs.append({
                "kind": "narr", "text": b["text"], "visuals": visuals,
                "extra_pool": [p for p in all_clip_paths if p not in used],
                "out": next_out("outro_narr"), "bug": bug_png,
            })

    return jobs, credits


def concat_and_normalize(clip_paths, out_path):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in clip_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
        listfile = f.name
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
         "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-r", "30", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
         out_path])
    os.unlink(listfile)


def make_phone_copy(src, out_path, max_mb=29):
    dur = ffprobe_duration(src)
    # target size budget with margin
    target_kbps_total = (max_mb * 8192) / dur * 0.92
    v_kbps = max(int(target_kbps_total - 64), 300)
    v_kbps = min(v_kbps, 700)
    run(["ffmpeg", "-y", "-i", src, "-vf", "scale=1280:-2", "-c:v", "libx264",
         "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps*1.2)}k", "-bufsize", f"{v_kbps*2}k",
         "-preset", "medium", "-c:a", "aac", "-b:a", "64k", "-ar", "44100", out_path])
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    return size_mb


def make_youtube_copy(src, out_path):
    """Upload-quality re-encode: h264 crf 21, audio copy (no re-encode), faststart for
    progressive playback. Keeping audio as a copy avoids a second loudnorm pass drifting
    from the concat's own loudnorm."""
    run(["ffmpeg", "-y", "-i", src, "-c:v", "libx264", "-crf", "21", "-preset", "medium",
         "-c:a", "copy", "-movflags", "+faststart", out_path])
    return os.path.getsize(out_path) / (1024 * 1024)


def write_credits(credits, out_path, name="episode"):
    seen = set()
    lines = [f"Sources / credits for {name}", ""]
    for c in credits:
        key = c.get("url") or c.get("title")
        if not key or key in seen:
            continue
        seen.add(key)
        lines.append(f"[{c.get('section','')}] {c.get('channel','')} — {c.get('title','')}")
        if c.get("url"):
            lines.append(f"    {c['url']}")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True, help="episodes/<slug> directory")
    ap.add_argument("--intro-outro", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-parallel", type=int, default=4)
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--bumpers", default=None, help="path to a brand/clips.json-style bumper list")
    ap.add_argument("--voice", default=None)
    ap.add_argument("--rate", default=None)
    ap.add_argument("--pitch", default=None)
    ap.add_argument("--tts-cache-dir", default=None)
    args = ap.parse_args()

    ep = load_episode(args.episode)
    root = ep["_stories_root"]
    order = ep["story_order"]
    workdir = os.path.expanduser(args.work)
    os.makedirs(workdir, exist_ok=True)

    bug_png = os.path.join(workdir, "bug.png")
    plates.bug(bug_png)

    bumpers = None
    bumpers_path = os.path.expanduser(args.bumpers) if args.bumpers else None
    if bumpers_path and os.path.exists(bumpers_path):
        bumpers = json.load(open(bumpers_path))

    tts_opts = {"voice": args.voice, "rate": args.rate, "pitch": args.pitch,
                "cache_dir": os.path.expanduser(args.tts_cache_dir) if args.tts_cache_dir else None}

    jobs, credits = build_jobs(root, order, os.path.expanduser(args.intro_outro), workdir, bug_png,
                                bumpers=bumpers, bumpers_path=bumpers_path)
    for j in jobs:
        j["skip_if_exists"] = args.skip_existing

    print(f"{len(jobs)} beats to render, max_parallel={args.max_parallel}", file=sys.stderr)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_parallel) as ex:
        futs = {ex.submit(render_one_beat, j, tts_opts): j for j in jobs}
        for fut in concurrent.futures.as_completed(futs):
            j = futs[fut]
            try:
                fut.result()
                print(f"done: {j['out']}", file=sys.stderr)
            except Exception as e:
                print(f"FAILED: {j['out']}: {e}", file=sys.stderr)
                raise

    clip_paths = [j["out"] for j in jobs]
    os.makedirs(os.path.dirname(os.path.expanduser(args.out)), exist_ok=True)
    concat_and_normalize(clip_paths, os.path.expanduser(args.out))

    # exact in-order beat list (incl. bumpers, which live outside `workdir`) so verify.py
    # can build a precise timeline instead of guessing from a directory listing
    with open(os.path.join(workdir, "manifest.json"), "w") as f:
        json.dump([{"out": j["out"], "kind": j["kind"]} for j in jobs], f, indent=2)

    phone_out = os.path.expanduser(args.out).replace(".mp4", "_phone.mp4")
    size_mb = make_phone_copy(os.path.expanduser(args.out), phone_out)

    youtube_out = os.path.expanduser(args.out).replace(".mp4", "_youtube.mp4")
    youtube_size_mb = make_youtube_copy(os.path.expanduser(args.out), youtube_out)

    credits_out = os.path.expanduser(args.out).replace(".mp4", "_credits.txt")
    write_credits(credits, credits_out, name=ep["_slug"])

    dur = ffprobe_duration(os.path.expanduser(args.out))
    print(json.dumps({
        "ok": True, "out": args.out, "duration_s": dur,
        "phone_out": phone_out, "phone_size_mb": size_mb,
        "youtube_out": youtube_out, "youtube_size_mb": youtube_size_mb,
        "credits_out": credits_out, "n_beats": len(jobs),
    }, indent=2))


if __name__ == "__main__":
    main()
