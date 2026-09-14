# n6_bls_rigged -- notes

## Fact checks
- Firing date Aug 1, 2025; Trump's escalated "almost 900,000 jobs" revision claim came Aug 5 and was
  rated Pants Fire by PolitiFact (source in beats.json). This story does not use the "900,000" line as
  a caption anywhere (no clean on-camera SOT of it was found in the three source videos), so it is left
  out of clip transcripts to avoid an unsourced on-screen claim; the "rigged"/no-evidence framing carries
  the point instead.
- All source videos are dated Aug 3-4, 2025, inside the episode's Aug 1-5 window for this story. No
  cross-date caption risk.

## Outlet-attribution judgment calls
- `n6_sot_exco_noway` and `n6_sot_exco_locked`: uploaded by **Forbes Breaking News**, but the footage
  itself is a rebroadcast of a **CNN State of the Union** interview -- Forbes's own on-screen graphic
  reads "VIDEO: CNN" and dates it August 3, 2025. `clips.json.channel` records the uploader (Forbes
  Breaking News, for sourcing/redownload purposes); the caption label in `beats.json` says "via CNN"
  since that is the actual outlet credited on screen and is what a viewer would see if they froze the
  frame. Outlet logos (Forbes lower third + CNN tag) are untouched, not cropped.
- `n6_sot_hassett`: CBS News's own broadcast, but the Hassett soundbite is itself an inset clip of
  **NBC's Meet the Press**, tagged "MEET THE PRESS/NBC SUNDAY" on screen with an NBC peacock logo, plus
  a CBS-added chyron naming Hassett. Labeled "via NBC" for the same reason as above; `channel` in
  clips.json stays CBS News (the video we actually downloaded from).
- The former BLS commissioner's name is never stated on screen in the excerpts used (only "COMMISSIONER
  REACTS..." / his title), so no name is put in captions or beats -- avoids risking a wrong name from
  memory. He is referred to as "Trump's own former BLS chief" in narration, which matches the episode
  brief's framing exactly.

## Cold open candidate
`n6_sot_exco_noway` ("There's no way for that to happen.") marked `cold_open_candidate: true` -- shortest,
driest, funniest rebuttal in the set; lands hardest cut cold with no setup.

## Runtime / mix
4 SOTs, ~14.75s combined, against an estimated ~52.5s total story runtime (~28% SOT) -- inside the
25-40% target. 3 dedicated muted visual/b-roll clips provided beyond the SOTs themselves so narration
beats are never starved for footage (`n6_vis_graphic`, `n6_vis_trump_broll`, `n6_vis_exco_broll`); narr
beats also list the opposite story's muted SOT-kind clips as a second fallback where useful.

## Source videos (deleted after cutting, per contract)
- CBS News, `y_pYLzj9WOU` (Aug 4, 2025) -- 3 excerpts used (2 SOT + 2 visual, one visual is muted overlap
  of the same shot as the Trump SOT) = 4 total cuts from this video, within the 6-per-video max.
- Forbes Breaking News, `yN_v-y441Pg` (Aug 3, 2025) -- 3 excerpts used (2 SOT + 1 visual), within the
  6-per-video max.
- MS NOW candidate (`h0k0Ki6ZS_c`) was inspected but not used: it's a long panel/methodology discussion
  with no clean, cleanly-attributable single-speaker soundbite in the window that wasn't already better
  covered by the CBS and Forbes cuts; skipped to keep excerpt count and source count lean.

## Full-length downloads
All intermediate full/partial downloads and frame grabs lived under a scratch tmp dir outside this repo
and were deleted after clips were cut (see cleanup step). Nothing besides `clips/*.mp4`, `clips.json`,
`beats.json`, this file, and `DONE` remains in the story folder.
