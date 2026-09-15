#!/usr/bin/env python
"""Scan all stories/<id>/clips.json for cold_open_candidate:true SOTs, pick up to 3
(one per story preferred, scanned in the episode's story order), and write intro_outro.json's
intro cold-open + title card + intro narration, plus the outro narration -- both narration
texts and their b-roll visuals coming from episode.json.

Usage: python build_intro_outro.py --episode 1_робочі/episodes/2026-09-trump-month \
    --title-png work/2026-09-trump-month/render/title.png --out .../intro_outro.json
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import load_episode  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True, help="1_робочі/episodes/<slug> directory")
    ap.add_argument("--title-png", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    ep = load_episode(args.episode)
    root = ep["_stories_root"]
    # cold-open candidates are scanned in cold_open_order if the episode sets one
    # (preserves a specific pick across re-renders); otherwise the render order.
    order = ep.get("cold_open_order") or ep["story_order"]

    candidates = []
    for sid in order:
        cp = os.path.join(root, "stories", sid, "clips.json")
        if not os.path.exists(cp):
            continue
        clips = json.load(open(cp))
        for c in clips:
            if c.get("kind") == "sot" and c.get("cold_open_candidate"):
                path = c["file"]
                if not os.path.isabs(path):
                    path = os.path.join(root, "stories", sid, path)
                candidates.append({
                    "story": sid, "clip": path, "caption": c.get("transcript", ""),
                    "label": f"via {c.get('channel','')}", "banner": c.get("banner", "none"),
                    "source_url": c.get("source_url"),
                })
                break  # one per story max for the cold open

    picks = candidates[:3]

    intro_beats = []
    for p in picks:
        intro_beats.append({
            "type": "sot", "clip": p["clip"], "caption": p["caption"],
            "label": p["label"], "banner": p["banner"], "source_url": p["source_url"],
        })
    intro_beats.append({"type": "title", "png": os.path.expanduser(args.title_png), "seconds": 2.3})
    intro_beats.append({
        "type": "narr",
        "text": ep["intro"]["text"],
        "visuals": [{"path": p} for p in ep["intro"]["_visuals_abs"]],
    })

    outro_beats = [{
        "type": "narr",
        "text": ep["outro"]["text"],
        "visuals": [{"path": p} for p in ep["outro"]["_visuals_abs"]],
    }]

    out = {"intro": intro_beats, "outro": outro_beats}
    with open(os.path.expanduser(args.out), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({"picked_cold_opens": [p["story"] for p in picks], "n_candidates_found": len(candidates)}, indent=2))


if __name__ == "__main__":
    main()
