# n6_portland_guard — notes

## Fact checks
- Trump's Truth Social post (Sept 27, 2025, 10:19 AM per the CNN graphic) matches the exact wording quoted in
  `episode.json`/`research.json`: "war ravaged Portland", "up to 200" is implied by "all necessary Troops" in the
  post itself — the "up to 200" figure and the National Guard framing come from the Time/OPB/NPR source articles,
  not from the post's own text. Narration attributes the 200 figure only implicitly ("National Guard troops in");
  it is not claimed to be an exact quote.
- "A judge blocked the deployment" (closing narr beat) simplifies "a federal judge issued a temporary restraining
  order blocking the deployment while the case proceeded" from `episode.json`. TRO, not a final ruling — kept the
  narration deliberately vague ("blocked") rather than implying a permanent injunction.

## Judgment calls
- **The CNN clips are not Trump's spoken voice.** CNN's video is a breaking-news graphic of the actual Truth Social
  post (screenshot, key lines highlighted) read aloud by a CNN narrator/anchor, not archival audio of Trump
  speaking on camera. The visual makes this clear (visible "Truth Social" branding, tweet-style layout), and
  narration in beats.json always frames it as "Trump called/posted," never "Trump said on camera." Labeled
  "via CNN" in the caption, correctly attributing the reading to CNN rather than implying it's Trump's own voice.
- **The National Guard b-roll (`n6_visual_guard_*`) is NOT Portland footage.** It's file footage CBC used while
  their anchor recapped earlier 2025 deployments to Los Angeles and Washington, D.C. ("Earlier this summer... Los
  Angeles... National Guard troops have been out on the streets [of DC] for weeks"). No actual footage of National
  Guard troops in Portland exists because the judge blocked the deployment before it happened. I used this footage
  only as generic "National Guard" visual under narration that does not claim it depicts Portland, and the `shows`
  field in clips.json explicitly flags "(not Portland)" on all three. This keeps the story at ~100% real footage
  without misrepresenting what's on screen.
- Both KATU SOT clips come from the same press-conference video/shot (Gov. Tina Kotek, outdoor podium, Portland),
  identified by the video's own title. No mayor Keith Wilson footage was found in the searched candidates, so the
  rebuttal side of the story rests on Kotek only; this is accurate to what's sourced (Time/OPB/NPR all quote Kotek
  directly) even though `episode.json`'s brief also names Mayor Wilson.
- KATU's auto-captions are YouTube's rolling/word-level style; the two KATU clip in/out points were reconstructed
  from per-word `<c>` timestamps rather than cue boundaries (which repeat text across multiple overlapping cues).
  Timings were sanity-checked against a decoded frame from each clip; both land on-message with no truncated words
  at the cut points, but exact frame-perfect start could be off by a few hundred ms.

## Runtime / mix
- 4 SOT clips (CNN x2, KATU x2), total ~16.7s of ~46s estimated story runtime (~36%) — within the 25–40% target.
- 0% stock. All 7 clips are real news footage from real outlets, uploaded 2025-09-27 (same day as the event).
- `n6_sot_fullforce` marked `cold_open_candidate: true` — "I am also authorizing full force if necessary" reads as
  the most self-serious/absurd standalone line for the episode's cold open.
