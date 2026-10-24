"""Build the between-story transition bumpers from the channel's own brand clips.

The user supplies the transition clips (brand/ymca_*.mp4). Each bumper slot gets one of
them at random (no clip twice in a row), used whole with its own audio: normalized to the
pipeline format, loudnorm, persistent WEIRD NEWS USA bug. Writes brand/clips.json in the
same shape assemble.py's --bumpers expects.
"""
import argparse
import glob
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import run, ffprobe_duration, loudnorm_filter, PIPELINE_GROUP, W, H, FPS  # noqa: E402
import plates  # noqa: E402

BRAND = os.path.join(PIPELINE_GROUP, "brand")
OUT = os.path.join(BRAND, "rendered")
SLOTS = ["ymca_open", "ymca_gap1", "ymca_gap2", "ymca_gap3", "ymca_gap4", "ymca_gap5", "ymca_close"]


def pick(sources, rng):
    picks, prev = [], None
    for _ in SLOTS:
        choice = rng.choice([s for s in sources if s != prev] or sources)
        picks.append(choice)
        prev = choice
    return picks


def render(src, dst, bug_png):
    vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
          f"format=yuv420p[b];[b][1:v]overlay=0:0[v]")
    run(["ffmpeg", "-y", "-i", src, "-i", bug_png, "-filter_complex", vf,
         "-map", "[v]", "-map", "0:a", "-af", loudnorm_filter(),
         "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
         "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k", dst])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=None, help="fix the random order (default: new order each run)")
    args = ap.parse_args()

    sources = sorted(glob.glob(os.path.join(BRAND, "ymca_*.mp4")))
    if not sources:
        sys.exit(f"no brand clips in {BRAND}")
    os.makedirs(OUT, exist_ok=True)
    bug_png = os.path.join(OUT, "bug.png")
    plates.bug(bug_png)

    rng = random.Random(args.seed)
    clips = []
    for slot, src in zip(SLOTS, pick(sources, rng)):
        dst = os.path.join(OUT, f"{slot}.mp4")
        render(src, dst, bug_png)
        clips.append({"id": slot, "file": os.path.relpath(dst, BRAND), "kind": "bumper", "duration": ffprobe_duration(dst),
                      "source": os.path.basename(src), "channel": "", "title": "", "source_url": ""})
        print(f"{slot}: {os.path.basename(src)}")
    biden = os.path.join(BRAND, "biden_end.mp4")
    if os.path.exists(biden):
        dst = os.path.join(OUT, "biden_end.mp4")
        render(biden, dst, bug_png)
        clips.append({"id": "biden_end", "file": os.path.relpath(dst, BRAND), "kind": "bumper", "duration": ffprobe_duration(dst),
                      "source": "biden_end.mp4", "channel": "AFGuidesHD", "title": "Joe Biden ending scene",
                      "source_url": "https://youtu.be/Dn6wCLRVCNo"})
        print("biden_end: biden_end.mp4")
    json.dump(clips, open(os.path.join(BRAND, "clips.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
