# n3_ymca_dance — notes

## Source
Used the YouTube upload named directly in episode.json's sources: FOX 9 Minneapolis-St. Paul's
"Donald Trump dances to end Michigan rally celebrating 100 days in office"
(https://www.youtube.com/watch?v=C7xJJkclKvk), uploaded 2025-04-29, 223s runtime. This is a real
broadcast-affiliate channel (Fox O&O), upload date matches the event day, and the whole clip covers
exactly the closing dance-and-exit — no reaction/compilation framing.

Did not pull the C-SPAN "User Clip" or the RT article footage separately; the FOX 9 upload contains
the same moment (speech ends → YMCA starts → dance → walk off) at higher resolution than C-SPAN's
listing usually offers, and RT's page is a text writeup, not primary footage. Both stayed in
beats.json `sources` for factual backing per the facts block in episode.json.

## Timing / verification
Scrubbed the 223s FOX 9 video by extracting frames every 1-2s to hand-locate the moment without
transcribing anything. Confirmed via frames only (never printed the sung words):
- ~0-70s: still speaking at podium.
- ~72-76s: song audibly starts (crowd noise shifts, he turns from mic).
- ~93-99s: full front-facing arm-pump dance — the strongest single shot, used as cold-open candidate.
- ~101-106s: side/back arm-pump toward crowd.
- ~109-114s: crowd-facing wide shot, signs up, visibly singing/cheering.
- ~199-203s: exit — fist raised, points back at crowd, walks through the blue curtain.

All 4 excerpts pulled from this single source video (well under the 6-clip cap), each ≤5.0s
(4.0-4.8s), h264+aac, audio kept intact including the song exactly as it played live.

## Lyrics rule compliance
No lyrics were printed, quoted, or transcribed anywhere in clips.json, beats.json, or this file.
Every SOT transcript field says "(YMCA plays ...)" or "(dancing, no spoken words)". Beat narration
refers to the song only by title ("YMCA" is the song's title, not a lyric) and describes the crowd's
behavior ("sang along") without quoting words.

## Reaction beat added 2026-09-21
Per the revised format.md "Reaction beats" rule (at least 2 distinct reaction/punch inserts per
story, not just the crowd shot), searched for a second insert:
- Checked for real news/late-night coverage from that week (Apr 29 - May 5 2025) specifically
  reacting to this dance going viral. Found nothing that cleanly qualified: a Comedy Central UK
  upload ("Trump Busts Out Iconic YMCA Dance Moves") turned out to be about the January 2025
  pre-inaugural rally dance, not the Warren, Michigan one — wrong event, so it was rejected rather
  than risk misattribution. Other hits were either 2020-era CBS/local-news pieces about a different
  dance/TikTok trend, or repost/aggregator channels (e.g. "Diario AS") with no real anchor reaction,
  just the same FOX 9 footage re-clipped — excluded per the "skip reaction channels" rule.
- Went back to the already-downloaded FOX 9 source instead (option 1, the free/preferred source).
  Re-pulled two short --download-sections excerpts (never the full 223s file) covering the walk
  down the stairs and through the crowd (~114-200s) that hadn't been scrubbed the first time, and
  found a clean, distinct reaction: a young woman in the front rows makes a heart shape with her
  hands as Trump passes by shaking hands, roughly 167.8-171.3s. Cut to 3.5s (`n3_reaction_heart_hands`),
  re-encoded h264 (1280x720) + aac to match the other clips. This is a different kind of reaction
  (one fan, sincere/affectionate) from the wide singing/cheering crowd shot already used, so it adds
  variety rather than repeating the same beat, and stays proportionate — no "everyone's losing it"
  overreach, matching the calibration guidance.
- Placed as its own `sot` beat right after the crowd-singing beat and before the exit beat, with a
  one-line label via FOX 9, same as the other SOTs.
- No lyrics involved in identifying or describing this moment; transcript field is again
  "(YMCA plays over the PA, no dialogue)".

## Judgment calls
- Marked `n3_sot_dance_front` (93.0-97.8s) as the cold_open_candidate: cleanest, most iconic
  front-on framing of the dance with no occlusion.
- Story is visual/musical per the brief, so beats alternate narr/sot with captions noting
  "(dancing)"/"(no spoken words)" instead of quoting dialogue, as instructed.
- Did not use stock — the real footage is the joke, per format.md guidance for money-shot stories.
- Deleted the full-length source download and thumbnail scratch files after trimming; final story
  folder is ~17MB, well under the 500MB budget.
