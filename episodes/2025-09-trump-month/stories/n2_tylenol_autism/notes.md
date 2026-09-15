# n2_tylenol_autism — notes

## Source
All footage is from a single video: **LiveNOW from FOX**, "FULL: Trump, RFK Jr. and Dr. Oz on autism rates and
Tylenol" (https://www.youtube.com/watch?v=IQ1nbaa14Vo), uploaded 2025-09-22 — same day as the event, so no
date-mismatch caveat. 4 excerpts pulled from this one source (within the 6-per-video cap).

## Fact checks
- "Taking Tylenol... there's no downside [to not taking it]" — PolitiFact rated this **Pants Fire**
  (https://politifact.com/factchecks/2025/sep/23/donald-trump/president-donald-trump-said-theres-no-downside-to/).
  Mainstream medical groups (ACOG etc.) warn that untreated high fever in pregnancy carries its own real risks,
  which is the actual downside to "don't take it at all."
- "You get a vat of 80 different vaccines" — PolitiFact rated this **False**
  (https://politifact.com/factchecks/2025/sep/26/donald-trump/no-small-children-dont-receive-80-different-vaccin/).
  The real CDC childhood schedule includes far fewer than 80 vaccines/doses by the relevant age.
- No causal link between acetaminophen and autism has been established in decades of research; Kenvue
  (Tylenol's manufacturer) disputed Trump's claim outright (per CNN, ABC News sourcing in episode.json).

## Judgment calls
- Used the president's own words verbatim, including the stutter/repetition ("there's there's no downside") —
  left as spoken rather than cleaned up, since it's real and the mangled delivery is part of the joke.
- `n2_sot_vaccines` transcript keeps the doubled "a a vat" filler exactly as spoken.
- Chose the LiveNOW from FOX feed over other full uploads (e.g. Global News) because its picture quality and
  audio sync were the cleanest for tight sub-5s trims; it is a bona fide FOX-owned live-news channel, not a
  reaction/compilation channel.
- `n2_visual_arrival` (muted-eligible, kept audio per spec) shows Trump walking to the podium — real footage of
  the actual event, used to open the story before any SOT lands, and reused later as filler b-roll per the
  "no frozen frames" rule.
- Marked both `n2_sot_vaccines` and `n2_sot_nodownside` as cold-open candidates — the "vat of 80 different
  vaccines" line and the flat "there's there's no downside" delivery are the two funniest/most quotable
  moments in the piece.
- All clips carry the LiveNOW from FOX lower-third chyron (banner: "bottom"); captions in the render should sit
  higher on screen to avoid overlapping it, and the outlet's own bug/logo must stay visible per the "never crop
  outlet logos" rule.
- Runtime lands around ~41s with SOT at ~28% of story time — inside the required 25–40% SOT band, slightly
  under the episode's general 45–55s per-story guideline, prioritized to keep narration tight and true to the
  ≤35-words-per-beat rule rather than padding with filler visuals.

## Cleanup
Deleted all full/oversized intermediate downloads and temp frames after trimming; only the 4 final clips remain
in `clips/`.
