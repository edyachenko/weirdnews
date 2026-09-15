#!/usr/bin/env python
"""Thin wrapper around yt-dlp for footage discovery, per SPEC.md's footage method.

search:  python find_footage.py search "Trump Dallas convention speech" --n 10
subs:    python find_footage.py subs VIDEO_ID --out-dir 1_робочі/render_cache/<slug>/subs
"""
import argparse
import os
import subprocess
import sys


def search(query, n, since=None, until=None):
    cmd = [
        "yt-dlp", f"ytsearch{n}:{query}", "--flat-playlist",
        "--print", "%(id)s|%(channel)s|%(title)s|%(duration)s|%(upload_date)s",
        "--sleep-requests", "1",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    if since or until:
        filtered = []
        for l in lines:
            parts = l.split("|")
            date = parts[4] if len(parts) > 4 else "NA"
            if date == "NA":
                filtered.append(l)  # keep, caller decides
                continue
            if since and date < since:
                continue
            if until and date > until:
                continue
            filtered.append(l)
        lines = filtered
    return lines


def fetch_subs(video_id, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cmd = [
        "yt-dlp", "--skip-download", "--write-auto-subs", "--sub-langs", "en",
        "--sub-format", "vtt", "-o", os.path.join(out_dir, "%(id)s"),
        "--sleep-requests", "1",
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("search")
    ps.add_argument("query")
    ps.add_argument("--n", type=int, default=10)
    ps.add_argument("--since", default=None, help="YYYYMMDD")
    ps.add_argument("--until", default=None, help="YYYYMMDD")

    pf = sub.add_parser("subs")
    pf.add_argument("video_id")
    pf.add_argument("--out-dir", required=True)

    args = ap.parse_args()
    if args.cmd == "search":
        for l in search(args.query, args.n, args.since, args.until):
            print(l)
    else:
        rc, out = fetch_subs(args.video_id, args.out_dir)
        print(out)
        sys.exit(rc)


if __name__ == "__main__":
    main()
