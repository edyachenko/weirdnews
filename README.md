# weirdnews: Weird News USA

Automated English news-commentary YouTube episodes built from **real footage**: short
(≤5.0 s) excerpts of news and official videos, a sarcastic TTS host, and the channel's own
brand transitions. Each episode covers one month of Trump's 2nd term, countdown style.

Repo layout is 4 top-level groups — see `CLAUDE.md`'s Layout section for the full map:
`3_продакшн/` (finished, ready to upload), `1_робочі/` (per-episode working data + render
cache), `2_пайплайн/` (render code + brand assets), `4_доки/` (rules, docs, channel identity).

## Setup

```bash
2_пайплайн/scripts/setup.sh    # brew ffmpeg/yt-dlp/uv, clones MoneyPrinterTurbo, creates .env
```

Fill in `.env` (`PEXELS_API_KEY`, `GEMINI_API_KEY`) — see `.env.example`. Never commit `.env`.

## Render an episode

```bash
uv run --project ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo python 2_пайплайн/pipeline/run_all.py \
  --episode 1_робочі/episodes/2026-09-trump-month \
  --voice en-US-BrianMultilingualNeural --rate=-8% --pitch=-2Hz \
  --out 1_робочі/render_cache/2026-09-trump-month/render_out/video.mp4
```

TTS is cached (`1_робочі/render_cache/tts_cache/`), so re-running with a different
voice/rate/pitch only re-renders the narration, never footage. Everything episode-specific
(story order, title/period, voice defaults, intro/outro text + visuals) lives in the
episode's `episode.json` — see `1_робочі/episodes/2026-09-trump-month/`.

The command above produces (next to `video.mp4`) `video_youtube.mp4` — the file that
actually ships. Once it passes verify, copy it to `3_продакшн/<slug>/video.mp4` alongside a
`thumbnail.jpg` and `seo.md` (see `4_доки/docs/seo-playbook.md`) — that folder is the only
one that matters for uploading.

## Making a new episode

Read `CLAUDE.md` and `4_доки/docs/format.md` first (the rules everything rests on), then run
the `new-episode` skill (`.claude/skills/new-episode/SKILL.md`): research → story selection →
parallel footage agents (`.claude/agents/story-footage.md`) → assembly
(`.claude/agents/episode-assembler.md`) → review → SEO + thumbnail → the user's explicit
approval before anything is published.
