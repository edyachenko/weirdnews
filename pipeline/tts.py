#!/usr/bin/env python
"""Generate narration audio + word-timed caption chunks with edge-tts.

Run with: uv run --project MoneyPrinterTurbo python pipeline/tts.py \
    --text "..." --out beat.mp3 --captions beat.captions.json [--voice en-US-AndrewNeural]

Produces:
  <out>            mp3 audio (loudnorm'd to -16 LUFS as a post step, see loudnorm() below)
  <captions>        JSON list of {"start": s, "end": s, "text": "line1\nline2"} chunks,
                    each chunk <=2 lines, <=42 chars/line, built from real word-boundary timing.
"""
import argparse
import asyncio
import json
import subprocess
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from common import wrap_caption, loudnorm_filter, run  # noqa: E402

VOICE = "en-US-AndrewNeural"


async def synth(text, voice, mp3_path, rate=None, pitch=None):
    import edge_tts

    kwargs = {}
    if rate:
        kwargs["rate"] = rate
    if pitch:
        kwargs["pitch"] = pitch
    communicate = edge_tts.Communicate(text, voice, boundary="WordBoundary", **kwargs)
    words = []
    with open(mp3_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append({
                    "text": chunk["text"],
                    "start": chunk["offset"] / 1e7,  # 100ns units -> seconds
                    "end": (chunk["offset"] + chunk["duration"]) / 1e7,
                })
    return words


def group_words_into_captions(words, max_chars=42, max_lines=2, words_per_chunk_target=6):
    """Group word-timed tokens into caption cues that fit <=2 lines of <=42 chars,
    using the real TTS word timings so captions are perfectly in sync."""
    chunks = []
    cur = []

    def flush():
        if not cur:
            return
        text = " ".join(w["text"] for w in cur)
        lines = wrap_caption(text, max_chars, max_lines)
        # if wrap_caption had to drop words to fit 2 lines, that's a sign the chunk is
        # too big; but with words_per_chunk_target<=6 this practically never happens.
        chunks.append({
            "start": cur[0]["start"],
            "end": cur[-1]["end"],
            "text": "\n".join(lines),
        })
        cur.clear()

    for w in words:
        cur.append(w)
        joined = " ".join(x["text"] for x in cur)
        too_long = len(joined) > max_chars * max_lines * 0.85
        end_of_clause = w["text"].strip().endswith((",", ".", "!", "?", ";", "—"))
        if len(cur) >= words_per_chunk_target or too_long or (end_of_clause and len(cur) >= 3):
            flush()
    flush()
    return chunks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True, help="output mp3 path")
    ap.add_argument("--captions", required=True, help="output captions json path")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--rate", default=None, help="e.g. -8%%")
    ap.add_argument("--pitch", default=None, help="e.g. -3Hz")
    ap.add_argument("--no-loudnorm", action="store_true")
    args = ap.parse_args()

    # edge-tts intermittently returns NoAudioReceived under parallel load; retry with backoff
    import time
    for attempt in range(4):
        try:
            words = asyncio.run(synth(args.text, args.voice, args.out, rate=args.rate, pitch=args.pitch))
            break
        except Exception as e:  # noqa: BLE001
            if attempt == 3:
                raise
            print(f"edge-tts attempt {attempt + 1} failed ({type(e).__name__}); retrying", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    if not words:
        raise SystemExit(f"edge-tts returned no word boundaries for text: {args.text!r}")

    if not args.no_loudnorm:
        tmp = args.out + ".norm.mp3"
        run([
            "ffmpeg", "-y", "-i", args.out, "-af", loudnorm_filter(),
            "-ar", "48000", "-ac", "2", "-b:a", "192k", tmp,
        ])
        os.replace(tmp, args.out)

    caps = group_words_into_captions(words)
    with open(args.captions, "w") as f:
        json.dump({"voice": args.voice, "text": args.text, "words": words, "captions": caps}, f, indent=2)

    dur = words[-1]["end"]
    print(json.dumps({"ok": True, "duration": dur, "n_caption_chunks": len(caps)}))


if __name__ == "__main__":
    main()
