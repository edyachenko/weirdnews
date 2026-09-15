#!/usr/bin/env python
"""Merge intro_outro.json + all stories/<id>/beats.json into one ordered render plan.

Usage: python build_beats.py --episode 1_робочі/episodes/2026-09-trump-month --out beats_master.json

Validates: every sot/visual clip id resolves to a real file, every clip <=5.0s,
counts excerpts per source video (warns if >6), computes expected runtime.
Order: intro, then the episode's story_order (countdown), then outro.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import ffprobe_duration, load_episode  # noqa: E402


def load_story(root, sid):
    sdir = os.path.join(root, "stories", sid)
    beats_path = os.path.join(sdir, "beats.json")
    clips_path = os.path.join(sdir, "clips.json")
    if not os.path.exists(beats_path):
        return None
    beats = json.load(open(beats_path))
    clips = json.load(open(clips_path)) if os.path.exists(clips_path) else []
    clip_by_id = {c["id"]: c for c in clips}
    return sdir, beats, clip_by_id


def resolve_clip_file(sdir, clip_by_id, clip_id):
    c = clip_by_id.get(clip_id)
    if not c:
        raise ValueError(f"clip id {clip_id!r} not found in clips.json")
    path = c["file"]
    if not os.path.isabs(path):
        path = os.path.join(sdir, path)
    return path, c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True, help="1_робочі/episodes/<slug> directory")
    ap.add_argument("--out", required=True)
    ap.add_argument("--intro-outro", default=None)
    args = ap.parse_args()
    ep = load_episode(args.episode)
    root = ep["_stories_root"]
    order = ep["story_order"]

    plan = []
    src_counts = {}
    total_runtime_est = 0.0
    sot_runtime_est = 0.0
    stock_runtime_est = 0.0
    warnings = []

    io_path = args.intro_outro or os.path.join(root, "intro_outro.json")
    io = json.load(open(io_path)) if os.path.exists(io_path) else {"intro": [], "outro": []}

    def add_beats(story_id, sdir, beats, clip_by_id, number=None, headline=None, sources=None):
        nonlocal total_runtime_est, sot_runtime_est, stock_runtime_est
        for b in beats:
            entry = dict(b)
            entry["_story"] = story_id
            if b["type"] == "sot":
                path, c = resolve_clip_file(sdir, clip_by_id, b["clip"])
                dur = ffprobe_duration(path)
                if dur > 5.05:
                    warnings.append(f"{story_id}:{b['clip']} duration {dur:.2f}s > 5.0s")
                entry["_file"] = path
                entry["_duration"] = dur
                entry["_banner"] = c.get("banner", "none")
                entry["_source_url"] = c.get("source_url")
                entry["_kind"] = c.get("kind", "sot")
                src_counts[c.get("source_url", path)] = src_counts.get(c.get("source_url", path), 0) + 1
                total_runtime_est += dur
                sot_runtime_est += dur
                if c.get("kind") == "stock":
                    stock_runtime_est += dur
            else:  # narr
                words = len(b["text"].split())
                est = max(words / 2.3, 2.0)
                entry["_duration_est"] = est
                total_runtime_est += est
                vis_files = []
                for vid in b.get("visuals", []):
                    path, c = resolve_clip_file(sdir, clip_by_id, vid)
                    dur = ffprobe_duration(path)
                    if dur > 5.05:
                        warnings.append(f"{story_id}:{vid} duration {dur:.2f}s > 5.0s")
                    vis_files.append(path)
                    src_counts[c.get("source_url", path)] = src_counts.get(c.get("source_url", path), 0) + 1
                    if c.get("kind") == "stock":
                        stock_runtime_est += min(dur, 4.0)
                entry["_visual_files"] = vis_files
            if number is not None:
                entry["_number"] = number
                entry["_headline"] = headline
                entry["_sources"] = sources
            plan.append(entry)

    plan.append({"type": "raw_group", "name": "intro", "beats": io.get("intro", [])})
    for b in io.get("intro", []):
        if b["type"] == "sot":
            pass  # intro beats resolved separately by assemble.py using their own clip refs

    for i, sid in enumerate(order):
        loaded = load_story(root, sid)
        if loaded is None:
            warnings.append(f"story {sid} missing beats.json — SKIPPED")
            continue
        sdir, beats_doc, clip_by_id = loaded
        add_beats(sid, sdir, beats_doc["beats"], clip_by_id,
                  number=beats_doc.get("number"), headline=beats_doc.get("headline"),
                  sources=beats_doc.get("sources"))

    plan.append({"type": "raw_group", "name": "outro", "beats": io.get("outro", [])})

    out = {
        "plan": plan,
        "warnings": warnings,
        "source_excerpt_counts": src_counts,
        "over_6_sources": {k: v for k, v in src_counts.items() if v > 6},
        "estimated_runtime_s": total_runtime_est,
        "estimated_sot_runtime_s": sot_runtime_est,
        "estimated_sot_pct": (sot_runtime_est / total_runtime_est * 100) if total_runtime_est else 0,
        "estimated_stock_pct": (stock_runtime_est / total_runtime_est * 100) if total_runtime_est else 0,
    }
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: v for k, v in out.items() if k != "plan"}, indent=2))


if __name__ == "__main__":
    main()
