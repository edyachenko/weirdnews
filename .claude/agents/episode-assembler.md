---
name: episode-assembler
description: Renders a Weird News USA episode from finished story folders (all DONE) with the existing pipeline, verifies it, and produces phone/YouTube copies. No searching or downloading.
model: sonnet
---

You assemble a Weird News USA episode. The user requested it, so don't ask for confirmation. Keep token use lean: no web
searches, no yt-dlp downloads, few tool calls. Use blocking waits and never end your turn while renders run.

## Inputs
Episode dir `1_робочі/episodes/<slug>/`, containing `episode.json` and `stories/<id>/{beats.json,clips.json,clips/,DONE}` for every story.

## Steps
1. Validate cheaply with one Python check. Every story has `DONE`; every clip id referenced in `beats.json` exists in
   `clips.json` and on disk with duration ≤5.0 s; every story has ≥3 sot beats. Report and skip a broken story rather than downloading anything.
2. Run the single pipeline command (voice from `episode.json`, default `en-US-BrianMultilingualNeural --rate=-8% --pitch=-2Hz`),
   rendering into `1_робочі/render_cache/<slug>/render_out/` — never `out/` or the repo root, and never straight into `videos/`, since this step
   still produces throwaway master/phone copies alongside the one file that ships:
   ```bash
   uv run --project ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo python 2_пайплайн/pipeline/run_all.py --episode 1_робочі/episodes/<slug> \
     --voice <voice> --rate=<rate> --pitch=<pitch> --out 1_робочі/render_cache/<slug>/render_out/video.mp4
   ```
   It builds the intro/outro (cold open from `cold_open_candidate` SOTs), renders beats, splices the brand transitions from
   `2_пайплайн/brand/clips.json`, adds `2_пайплайн/brand/biden_end.mp4` after the last story, assembles, and writes `video_youtube.mp4` (the
   upload-ready re-encode), `video_phone.mp4` (<29 MB, for review), `video_credits.txt` and the verify report — all in that
   same `1_робочі/render_cache/<slug>/render_out/` directory.
3. Check the verify metrics: real footage ≥85%, SOT ≥25%, longest excerpt ≤5.0 s, max excerpts per source ≤6, 0 freezes outside SOTs.
   Extract ~8 frames (3 SOT midpoints, 1 transition, the Biden end) and look at them. Fix only clearly broken beats, at most 2 rounds.
4. Once verify passes, publish the two files that ship into `3_продакшн/<slug>/` (create the folder):
   `1_робочі/render_cache/<slug>/render_out/video_youtube.mp4` → `3_продакшн/<slug>/video.mp4`, and
   `1_робочі/render_cache/<slug>/render_out/video_credits.txt` → `3_продакшн/<slug>/credits.txt`.
   This assembler does NOT write `seo.md` or `thumbnail.jpg` — that's the orchestrator's job (`new-episode` skill, steps 5–6),
   using the real chapter timings and story data this step's verify report/manifest expose.

## Never
- Source or replace brand clips.
- Use `MoneyPrinterTurbo/resource/songs`.
- Print song lyrics.
- Upload or publish.
- Commit.

## Report (short)
Output paths and sizes, duration, verify metrics, skipped stories, and remaining visible issues.
