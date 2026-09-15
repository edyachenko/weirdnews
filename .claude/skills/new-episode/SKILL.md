---
name: new-episode
description: Use when making a new Weird News USA episode (e.g. "зроби відео за березень 2025", "next month episode", "new video about X"). Covers research → story selection → parallel footage agents → render → review → user approval.
---

# Making a Weird News USA episode

Read `4_доки/docs/format.md` first. Opus orchestrates; every heavy step runs in Sonnet subagents.

## 1. Pick the period and the stories (Opus + one Sonnet research agent)

1. The period comes from the user or from `4_доки/research/` ranking (months of Trump's 2nd term, ordered by how much
   bullshit he said). Prefer Gemini with Google Search grounding (`GEMINI_API_KEY` in `.env`) for month digests.
   PolitiFact alone is too thin: 3–9 checks per month.
2. Get ~15 candidate stories for the period, each with a date, the absurd claim or gaffe, ≥2 source URLs, and whether **video of the
   moment exists** on YouTube. Stories without video are worthless for this format.
3. Pick 6 stories, the most absurd first. Order them as a countdown #6 → #1 with the strongest at #1.
4. Create `1_робочі/episodes/<YYYY-MM-slug>/episode.json`: title, period, story ids in render order, one-line brief per story,
   and voice settings. Save the research to `1_робочі/episodes/<slug>/research.json`.

**Checkpoint:** show the user the 6 stories (one line each, in Ukrainian) before spending on footage.

## 2. Footage + beat sheets (6 × `story-footage` agents in parallel)

Launch one `story-footage` subagent per story in a single message (`subagent_type: story-footage`), each with: episode dir, story id,
the facts and sources for that story, and footage ideas. The agent contract (schemas, ≤5 s rule, DONE marker)
lives in the agent definition. Expect ~10–15 min per story. As each agent finishes, give the user a one-line
summary: number of SOTs and the best moment.

## 3. Assemble (1 × `episode-assembler` agent)

After all `stories/<id>/DONE` exist, launch `episode-assembler` with the episode dir. It renders into
`1_робочі/render_cache/<slug>/render_out/` (never `out/`, never straight into `videos/`), verifies, then publishes the two files
that ship into a fresh `3_продакшн/<slug>/`: `video.mp4` (the upload-ready re-encode) and `credits.txt`.

## 4. Review (Opus, cheaply)

- Read the verify metrics: real footage ≥85%, SOT ≥25%, longest excerpt ≤5.0 s, 0 freezes outside SOTs.
- Look at 3–4 frames yourself: one SOT, one narr beat, the Biden end.
- Send `1_робочі/render_cache/<slug>/render_out/video_phone.mp4` with SendUserFile (that copy is <29 MB; `3_продакшн/<slug>/video.mp4` usually isn't). Send a Ukrainian transcript only if the user asks.

## 5. SEO package (Opus, cheap — no agent needed)

Follow `4_доки/docs/seo-playbook.md`. Get exact chapter timestamps from `ffprobe` on each beat file in
`1_робочі/render_cache/<slug>/render_out/` (or the manifest there), summed in render order — not estimates. Write
`3_продакшн/<slug>/seo.md` directly (not `1_робочі/episodes/<slug>/`): 3 title options, the full description (sources +
chapters + CTA + hashtags), 15–25 tags, and 3–4 thumbnail overlay-text options.

## 6. Thumbnail (Opus, cheap)

Never an AI-generated face for a real person — use a real frame, same fair-use logic as the video itself.
Sample several timestamps across 2–3 of the episode's most viral SOT clips (`1_робочі/episodes/<slug>/stories/*/clips/`),
not just #1 — the funniest reaction beats the most "on-topic" one. Composite in PIL (see the approach already used
for prior episodes): punchy contrast/saturation grade, bold hook text in `BeVietnamPro-Bold` bottom-left, a
"TOP 6" badge + the episode's month/year top-left, the "WEIRD NEWS USA" tag top-right. Crop out the source's own
chyron before adding your own text. Save straight to `3_продакшн/<slug>/thumbnail.jpg`.

## 7. Publish

Only after the user's explicit ✅. Upload `3_продакшн/<slug>/video.mp4` with `3_продакшн/<slug>/thumbnail.jpg`, paste the
`seo.md` title/description/tags. Never auto-publish.

## Budget hygiene

- No Opus web searches or downloads. Delegate them.
- Changing the voice or transition order means re-running `run_all.py` only, with no agents.
- If the user says stop: TaskStop every agent and `pkill -f yt-dlp; pkill -f weirdnews/pipeline`.

## Folder contract (don't let this drift again)

- `1_робочі/episodes/<slug>/` — production/working data only: `episode.json`, `research.json`, `stories/*/{beats.json,clips.json,clips/}`.
  Never a shipped deliverable.
- `1_робочі/render_cache/<slug>/` — render cache and throwaway copies (master, phone, debug frames, logs). Gitignored, regenerable, safe to delete
  once `3_продакшн/<slug>/` exists and has been reviewed.
- `3_продакшн/<slug>/` — **the only folder that matters for uploading**: `video.mp4`, `thumbnail.jpg`, `seo.md`, `credits.txt`.
  Nothing else lives here, and everything here is finished/upload-ready, not work-in-progress.
