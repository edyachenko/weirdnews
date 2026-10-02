# n6_presidents_compare -- notes

## Source
Single source video for all 6 clips: The White House's own YouTube upload,
"President Trump Signs an Executive Order, Aug. 3, 2026" (EtctNOj2gz4),
upload_date 20260803. This is the official primary-source feed of the Oval
Office ceremony where Trump signed the EO creating the Presidential Military
Spouse Commission. Found on the first candidate search (no extra searches
needed -- the footage lead in the brief, White House / RSBN / LiveNOW, was
right there in the first ytsearch10 result list).

All 4 SOT + 2 visual/reaction clips are cut from one 28s downloaded section
(00:09:55-00:10:23 of the source), so the "max 6 excerpts per source video"
cap is used exactly, all from one continuous take -- no re-encoding risk from
cutting across shots, no shot-matching issues.

## Caption accuracy vs. auto-captions
YouTube's auto-captions for this segment are rough (no real diarization, and
some words are clearly mis-heard -- e.g. the spouse's actual reply is
reported everywhere as "100%", but the auto-caption renders that moment as
"A little bit more... Yes... I think so"). Captions used in clips.json and
beats.json follow the published quotes from Yahoo News / The Blast / Military
Times (which match each other and match the well-documented viral clip), not
the raw auto-caption text. Auto-caption timestamps were used only to locate
the moment in the video, not as the source of the words themselves.

## Judgement calls
- n6_sot_sleepyjoe clip bundles Trump's needle line ("A little more than
  sleepy Joe?") and the spouse's reply ("100%") into one 5.0s SOT rather than
  splitting them, since they land as a single back-and-forth beat and
  splitting would have pushed either half under ~1s.
- n6_sot_goodbad compresses "Is it good or bad?" and the spouse's "No, it's
  good, actually it's very good" into one clip for the same reason.
- Reaction inserts (n6_vis_reaction1, n6_vis_reaction2) are genuine in-frame
  reactions from the same shot -- the standing group of spouses and Defense
  Secretary Hegseth visibly smiling/laughing as the exchange plays out, and
  the spouse herself laughing with her hand half-raised right after her
  "100%" answer. No reaction-channel/SNL/meme search hit was used (one
  ytsearch15 query for "Trump sleepy Joe military spouse compare reaction"
  came back with nothing specific to this moment -- mostly unrelated SNL
  cold opens and other Trump content), so per the method, step 2 (check the
  story's own footage for an in-frame reaction) was used instead, and it had
  what was needed for free.
- Did not caption-identify the spouse by name -- source articles (Yahoo,
  The Blast) do not name her either, so the story refers to her only as
  "the spouse" / "a military spouse," matching the sourcing.
- No signing-the-EO visual included: a second yt-dlp download (section
  00:13:27-00:13:52, the actual pen-to-paper moment) stalled for 25+ minutes
  at 48 bytes, almost certainly IP contention with other agents' concurrent
  yt-dlp processes (confirmed via `ps` -- another story's download was
  running at the same time). Killed it rather than retry, since the
  requirements (>=3 SOT, >=2 reaction inserts, real footage of the actual
  event) were already met from the first section alone. The desk/group wide
  shot already covers "Trump at the Resolute Desk" and "cutaway to the room"
  from the footage-ideas list; it's just missing the literal pen-signing
  insert.
- All clips carry the White House's own "TEXT POTUS TO 45470" bottom-third
  promotional banner throughout (banner: "bottom" in clips.json) -- captions
  should sit in the upper/middle area of frame, not the lower third.

## Budget
yt-dlp search calls used: 2 of the ~4 allowed (1 candidate search that found
the White House video directly, 1 reaction-beat search). No MANUAL_DOWNLOADS.md
needed -- everything required came from the first successful download.
