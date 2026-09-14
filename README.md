# weirdnews: Weird News USA

Automated English news-commentary YouTube episodes built from **real footage**: short
(≤5.0 s) excerpts of news and official videos, a sarcastic TTS host, and the channel's own
brand transitions. Each episode covers one month of Trump's 2nd term, countdown style.

## Setup

```bash
scripts/setup.sh        # brew ffmpeg/yt-dlp/uv, clones MoneyPrinterTurbo, creates .env
```

Fill in `.env` (`PEXELS_API_KEY`, `GEMINI_API_KEY`) — see `.env.example`. Never commit `.env`.

## Render an episode

```bash
uv run --project MoneyPrinterTurbo python pipeline/run_all.py \
  --episode episodes/2026-09-trump-month \
  --voice en-US-BrianMultilingualNeural --rate=-8% --pitch=-2Hz \
  --out out/2026-09-trump-month.mp4
```

TTS is cached (`work/tts_cache/`), so re-running with a different voice/rate/pitch only
re-renders the narration, never footage. Everything episode-specific (story order,
title/period, voice defaults, intro/outro text + visuals) lives in the episode's
`episode.json` — see `episodes/2026-09-trump-month/`.

## Making a new episode

Read `CLAUDE.md` and `docs/format.md` first (the rules everything rests on), then run the
`new-episode` skill (`.claude/skills/new-episode/SKILL.md`): research → story selection →
parallel footage agents (`.claude/agents/story-footage.md`) → assembly
(`.claude/agents/episode-assembler.md`) → review → the user's explicit approval before
anything is published.
