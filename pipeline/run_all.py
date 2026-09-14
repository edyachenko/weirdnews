#!/usr/bin/env python
"""One command: TTS (voice/rate/pitch as parameters, cached), render every beat + the
Y.M.C.A. bumpers, assemble, make the phone + YouTube copies and credits, and verify.
Everything episode-specific (story order, title/period, voice defaults, intro/outro
narration + visuals) comes from episodes/<slug>/episode.json. Re-running with a different
--voice/--rate/--pitch redoes only the narration audio + the beats that depend on it -- it
never re-downloads or re-cuts any footage (stories' SOT/visual clips, or the brand bumpers
built once by build_brand_bumpers.py).

Usage:
  uv run --project MoneyPrinterTurbo python pipeline/run_all.py \
      --episode episodes/2026-09-trump-month \
      --voice en-US-BrianMultilingualNeural --rate=-8% --pitch=-2Hz \
      --out out/2026-09-trump-month.mp4
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import run, load_episode, ROOT  # noqa: E402

MPT_PROJECT = os.path.join(ROOT, "MoneyPrinterTurbo")
PIPELINE_DIR = os.path.dirname(__file__)
BUMPERS_JSON = os.path.join(ROOT, "brand/clips.json")
TTS_CACHE_DIR = os.path.join(ROOT, "work", "tts_cache")  # shared across episodes/voices; keyed by hash


def uv_python(*a):
    return ["uv", "run", "--project", MPT_PROJECT, "python", *[str(x) for x in a]]


def title_lines(title):
    """Split an episode title like "Trump's Month: The Greatest Hits" into the two-line
    title-card layout (first line keeps the colon, both uppercased)."""
    if ":" in title:
        t1, t2 = title.split(":", 1)
        return f"{t1.strip().upper()}:", t2.strip().upper()
    return title.strip().upper(), ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True, help="episodes/<slug> directory")
    ap.add_argument("--voice", default=None, help="default: episode.json's voice.voice")
    ap.add_argument("--rate", default=None, help="default: episode.json's voice.rate")
    ap.add_argument("--pitch", default=None, help="default: episode.json's voice.pitch")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-parallel", type=int, default=4)
    args = ap.parse_args()

    ep = load_episode(args.episode)
    episode_dir = ep["_dir"]
    slug = ep["_slug"]
    voice_defaults = ep.get("voice", {})
    voice = args.voice or voice_defaults.get("voice")
    rate = args.rate or voice_defaults.get("rate")
    pitch = args.pitch or voice_defaults.get("pitch")
    if not voice:
        sys.exit("no --voice given and episode.json has no voice.voice default")

    out = os.path.expanduser(args.out)
    workdir = os.path.join(ROOT, "work", slug, "render")
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(TTS_CACHE_DIR, exist_ok=True)

    # 1) title card + intro/outro beats (deterministic given the story pool; cheap, no
    #    network/downloads -- safe to always regenerate)
    title_png = os.path.join(workdir, "title.png")
    t1, t2 = title_lines(ep.get("title", slug))
    run(uv_python(os.path.join(PIPELINE_DIR, "plates.py"), "title", "--out", title_png,
                  "--title", t1, "--subtitle", t2))

    intro_outro_json = os.path.join(workdir, "intro_outro.json")
    run(uv_python(
        os.path.join(PIPELINE_DIR, "build_intro_outro.py"),
        "--episode", episode_dir, "--title-png", title_png, "--out", intro_outro_json,
    ))

    # 2) validate the beat plan (durations, per-source excerpt counts, <=5.0s rule)
    beats_master = os.path.join(workdir, "beats_master.json")
    bb = run(uv_python(
        os.path.join(PIPELINE_DIR, "build_beats.py"),
        "--episode", episode_dir, "--intro-outro", intro_outro_json, "--out", beats_master,
    ), check=False)
    build_beats_report = {}
    try:
        build_beats_report = json.loads(bb.stdout[bb.stdout.index("{"):])
    except Exception:
        pass

    # 3) render every beat (with the brand bumpers spliced in) + concat + phone/YouTube
    #    copies + credits
    assemble_cmd = uv_python(
        os.path.join(PIPELINE_DIR, "assemble.py"),
        "--episode", episode_dir, "--intro-outro", intro_outro_json, "--work", workdir,
        "--out", out, "--max-parallel", args.max_parallel,
        "--bumpers", BUMPERS_JSON, "--voice", voice, "--tts-cache-dir", TTS_CACHE_DIR,
    )
    if rate:
        assemble_cmd += [f"--rate={rate}"]
    if pitch:
        assemble_cmd += [f"--pitch={pitch}"]
    asm = run(assemble_cmd)
    assemble_report = {}
    try:
        assemble_report = json.loads(asm.stdout[asm.stdout.index("{"):])
    except Exception:
        pass

    # 4) verify (metrics + freeze check + spot-check frames)
    frames_out = os.path.join(ROOT, "out", f"frames_{slug}")
    verify_cmd = uv_python(
        os.path.join(PIPELINE_DIR, "verify.py"),
        "--episode", episode_dir, "--intro-outro", intro_outro_json, "--final", out,
        "--frames-out", frames_out, "--bumpers", BUMPERS_JSON, "--workdir", workdir,
    )
    vr = run(verify_cmd)
    try:
        first_brace = vr.stdout.index("{")
        verify_report = json.loads(vr.stdout[first_brace:])
    except Exception:
        verify_report = {}

    print(json.dumps({
        "ok": True,
        "out": out,
        "slug": slug,
        "voice": voice, "rate": rate, "pitch": pitch,
        "build_beats_warnings": build_beats_report.get("warnings", []),
        "assemble": assemble_report,
        "verify": verify_report,
    }, indent=2))


if __name__ == "__main__":
    main()
