# weirdnews: Weird News USA

Automated English news-commentary YouTube episodes built from **real footage**: short excerpts of news and
official videos, a sarcastic TTS host, and the channel's own brand transitions. The first episode ("Trump's Month",
Aug 14 – Sep 14 2026) was built on 2026-09-14. The plan is a series where each video covers one month of Trump's 2nd term.

- Format bible (read before making anything): `docs/format.md`
- What worked, what failed, and why: `docs/retrospective-2026-09-14.md`
- How to make an episode end to end: skill `.claude/skills/new-episode/SKILL.md`

## The rules everything rests on

1. **Real footage is the product.** Stock or text cards got v1 and v2 rejected. Target 100% real footage and ≥25% SOT (original audio).
2. **Every excerpt ≤5.0 s.** The user considers this rule proven by experience. Enforce it and don't argue or add legal caveats.
3. **Brand assets come from the user only**: `brand/ymca_*.mp4` (transitions, random order) and `brand/biden_end.mp4`
   (after the last story, every episode). Never replace them with clips you found yourself.
4. **Facts sourced, opinions as opinions**, no invented quotes, no medical diagnoses.
5. **Nothing is published without the user's explicit ✅.**

## Working style (the user's limits matter)

- **Opus plans, Sonnet executes.** Heavy work (footage search, downloads, renders) goes to subagents with
  `model: sonnet`: `.claude/agents/story-footage.md`, one per story, run in parallel, and `.claude/agents/episode-assembler.md`.
  Opus writes the episode spec, launches the agents, and reviews results.
- Subagent prompts must say: work autonomously, use blocking waits, don't end the turn while renders or downloads run.
- If the user says stop, stop every agent immediately (TaskStop) and kill leftover yt-dlp/ffmpeg processes.
- Talk to the user in Ukrainian. Keep it short.

## Layout

```
brand/                   user's fixed brand clips (committed)
docs/                    format bible, retrospectives
pipeline/                render code: tts, render_beat, plates, assemble, verify, run_all, build_brand_bumpers
episodes/<slug>/         one episode: episode.json, research.json, stories/<id>/{beats.json,clips.json,notes.md}
  stories/<id>/clips/    downloaded excerpts (git-ignored, reproducible from clips.json)
research/                month ranking and research scripts
MoneyPrinterTurbo/       vendored clone, used only for its uv venv (edge-tts, Pillow) and fonts (git-ignored)
out/, work*/             renders and intermediates (git-ignored)
```

## Commands

```bash
scripts/setup.sh                                   # clone MPT + uv sync, brew yt-dlp/ffmpeg
uv run --project MoneyPrinterTurbo python pipeline/build_brand_bumpers.py      # re-roll transition order
uv run --project MoneyPrinterTurbo python pipeline/run_all.py \
  --episode episodes/2026-09-trump-month \
  --voice en-US-BrianMultilingualNeural --rate=-8% --pitch=-2Hz \
  --out out/2026-09-trump-month.mp4                # TTS (cached) → beats → assemble → phone copy → credits → verify
```

`--rate=` and `--pitch=` need the `=` form, because argparse misreads a leading `-`.

## Watch out for

- **YouTube downloads:** run one yt-dlp process per agent, with `--sleep-requests 1 --sleep-interval 2`, and download **only sections**
  (`--download-sections "*START-END"`). Find timestamps from auto-subs (`--skip-download --write-auto-subs`).
  If blocked, try `--extractor-args "youtube:player_client=web_safari"`. If still blocked, write MANUAL_DOWNLOADS.md for the user.
- **Never print song lyrics** (subs of music videos included). The output filter kills the agent mid-task.
- **CNN pages return HTTP 451 to WebFetch.** Use the Playwright MCP browser to read them.
- **Pexels/urllib needs an explicit User-Agent** (Cloudflare 403). Keys live in `.env` (see `.env.example`), never print them.
- **Frozen frames** come from narr beats with too little footage. `verify.py` fails any freeze >1 s outside SOTs.
- Concatenating independently encoded shots with `-c copy` creates stalled frames. Re-encode at concat.
- The final concat file is huge (~700 MB). Upload the `*_youtube.mp4` re-encode (crf 20, faststart) instead.
- Disk is tight on the Mac (~35 GB free). Delete full-length downloads and old `work*/` dirs.
