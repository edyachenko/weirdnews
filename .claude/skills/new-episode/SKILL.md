---
name: new-episode
description: Use when making a new Weird News USA episode (e.g. "зроби відео за березень 2025", "next month episode", "new video about X"). Covers research → story selection → parallel footage agents → render → review → user approval.
---

# Making a Weird News USA episode

Read `docs/format.md` first. Opus orchestrates; every heavy step runs in Sonnet subagents.

## 1. Pick the period and the stories (Opus + one Sonnet research agent)

1. The period comes from the user or from `research/` ranking (months of Trump's 2nd term, ordered by how much
   bullshit he said). Prefer Gemini with Google Search grounding (`GEMINI_API_KEY` in `.env`) for month digests.
   PolitiFact alone is too thin: 3–9 checks per month.
2. Get ~15 candidate stories for the period, each with a date, the absurd claim or gaffe, ≥2 source URLs, and whether **video of the
   moment exists** on YouTube. Stories without video are worthless for this format.
3. Pick 6 stories, the most absurd first. Order them as a countdown #6 → #1 with the strongest at #1.
4. Create `episodes/<YYYY-MM-slug>/episode.json`: title, period, story ids in render order, one-line brief per story,
   and voice settings. Save the research to `episodes/<slug>/research.json`.

**Checkpoint:** show the user the 6 stories (one line each, in Ukrainian) before spending on footage.

## 2. Footage + beat sheets (6 × `story-footage` agents in parallel)

Launch one `story-footage` subagent per story in a single message (`subagent_type: story-footage`), each with: episode dir, story id,
the facts and sources for that story, and footage ideas. The agent contract (schemas, ≤5 s rule, DONE marker)
lives in the agent definition. Expect ~10–15 min per story. As each agent finishes, give the user a one-line
summary: number of SOTs and the best moment.

## 3. Assemble (1 × `episode-assembler` agent)

After all `stories/<id>/DONE` exist, launch `episode-assembler` with the episode dir. It builds the intro/outro, runs
`pipeline/run_all.py`, verifies, and makes the `*_phone.mp4` (<29 MB) and `*_youtube.mp4` copies.

## 4. Review (Opus, cheaply)

- Read the verify metrics: real footage ≥85%, SOT ≥25%, longest excerpt ≤5.0 s, 0 freezes outside SOTs.
- Look at 3–4 frames yourself: one SOT, one narr beat, the Biden end.
- Send the phone copy with SendUserFile. Send a Ukrainian transcript only if the user asks.

## 5. Publish

Only after the user's explicit ✅. Upload `*_youtube.mp4` and the credits file as the description. Never auto-publish.

## Budget hygiene

- No Opus web searches or downloads. Delegate them.
- Changing the voice or transition order means re-running `run_all.py` only, with no agents.
- If the user says stop: TaskStop every agent and `pkill -f yt-dlp; pkill -f weirdnews/pipeline`.
