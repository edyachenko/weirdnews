#!/usr/bin/env python
"""Download a YouTube section and trim it precisely to <=5.0s, per SPEC.md.

python cut_clips.py download-section VIDEO_ID START END --out raw.mp4
python cut_clips.py trim raw.mp4 IN_OFFSET DURATION --out clip.mp4   # duration must be <=5.0
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import run, ffprobe_duration  # noqa: E402


def download_section(video_id, start, end, out_path, retry_web_safari=False):
    cmd = [
        "yt-dlp", "--download-sections", f"*{start}-{end}",
        "-f", "bv*[height<=1080]+ba/b", "--merge-output-format", "mp4",
        "--force-keyframes-at-cuts", "--sleep-requests", "1", "-o", out_path,
    ]
    if retry_web_safari:
        cmd += ["--extractor-args", "youtube:player_client=web_safari"]
    cmd.append(f"https://www.youtube.com/watch?v={video_id}")
    p = subprocess.run(cmd, capture_output=True, text=True)
    blocked = ("403" in p.stderr or "Sign in to confirm" in p.stderr or
               "403" in p.stdout or "Sign in to confirm" in p.stdout)
    if p.returncode != 0 and blocked and not retry_web_safari:
        return download_section(video_id, start, end, out_path, retry_web_safari=True)
    return p.returncode, p.stdout + p.stderr


def trim(src, in_offset, duration, out_path):
    duration = min(float(duration), 5.0)
    run(["ffmpeg", "-y", "-ss", str(in_offset), "-i", src, "-t", str(duration),
         "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
         "-c:a", "aac", "-ar", "48000", "-ac", "2", out_path])
    return ffprobe_duration(out_path)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    pd = sub.add_parser("download-section")
    pd.add_argument("video_id")
    pd.add_argument("start")
    pd.add_argument("end")
    pd.add_argument("--out", required=True)

    pt = sub.add_parser("trim")
    pt.add_argument("src")
    pt.add_argument("in_offset")
    pt.add_argument("duration")
    pt.add_argument("--out", required=True)

    args = ap.parse_args()
    if args.cmd == "download-section":
        rc, out = download_section(args.video_id, args.start, args.end, args.out)
        print(out)
        sys.exit(rc)
    else:
        dur = trim(args.src, args.in_offset, args.duration, args.out)
        print(f"trimmed to {dur:.2f}s -> {args.out}")


if __name__ == "__main__":
    main()
