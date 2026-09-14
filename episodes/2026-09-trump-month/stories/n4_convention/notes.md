# n4_convention notes

## Fact basis
CNN fact-checked three Trump lines from the Republican midterm convention in Dallas
(source: `trump_month/research.json`, story `convention_fact_check`):
- "no empty seats" — CNN night-2 fact-check (verified false, arena had visible empty seats)
- "almost every item" [getting cheaper] — CNN night-1 fact-check (verified misleading, prices
  were rising)
- "every single promise" [kept] — CNN night-1 fact-check (verified false)

## Footage found
All three lines located and confirmed verbatim in real speech footage via auto-caption search:

- **"No empty seats. The fake news."** — FOX 26 Houston, "FULL: Trump's speech on Day 2 of RNC
  Midterm Convention" (youtube 2vuxB-PRXMM, uploaded 20260911), at 00:14:35.5. Trump directly
  addresses the "empty seats" headline on camera — this is the strongest, funniest SOT and is
  marked `cold_open_candidate`.
- **"...prices and almost every other item are rapidly going down."** — C-SPAN, "President Trump
  FULL REMARKS at GOP Midterm Convention" (youtube ZvYeMCcOhWE, uploaded 20260910), at
  00:30:36.9. Actual wording is "almost every OTHER item," a close paraphrase of the research.json
  quote; transcript field uses the exact spoken words.
- **"every single promise I've made to you as a candidate, I've delivered on."** — same C-SPAN
  video, at 01:35:47.0. Exact match to the CNN-quoted line.

This gives 3 real Trump SOTs (~13.1s combined, ~26% of the story's ~50s runtime), satisfying the
≥3 SOT / 25-40% requirement without needing a CNN anchor clip.

## What I could not find
No CNN fact-check segment/anchor video for this specific story surfaced in a YouTube search
(CNN's coverage here appears to be a text article, not a broadcast segment) — the footage-ideas
list mentioned "CNN fact-check segment anchor lines" as an option, but I did not find one and did
not need it once 3 solid Trump SOTs were secured. Not used; no impact on requirements.

No genuine wide "arena full of empty seats" establishing shot was found in the material checked
(C-SPAN's feed and FOX 26's feed both stay tight on the podium throughout the sections searched).
Visual b-roll instead uses tight/medium shots of Trump at the podium with the crowd and flags
visible behind him, all real footage of the actual event. Given the limited variety of usable
wide shots, `n4_v_open`, `n4_v_arrival`, and `n4_v_crowd` are each used twice across narr beats
(one original use + one permitted reuse), per the "a visual clip may be reused once" rule.

## Sources / outlets used
FOX 26 Houston, C-SPAN. Both real outlets, uploads within the Aug 14 – Sep 16 2026 window.

## No swap
Story kept as-is (id n4_convention); no need to swap to a different story — usable footage was
found in the first two videos checked, both accessible without any yt-dlp blocking.

## Housekeeping
Full-length source downloads (only the needed --download-sections excerpts were ever pulled, not
full videos), subtitle .vtt files, and intermediate frame grabs were all deleted after use. Final
story folder is ~16 MB, well under the 500 MB cap.
