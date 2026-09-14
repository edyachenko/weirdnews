# n6_fed — notes

## Story
Trump threatens to halt trade with top trading partners unless the Fed cuts rates (Truth Social post,
Sep 4 2026, 9:41 AM). Confirmed word-for-word against CNN's article and the on-screen Truth Social
screenshot used in the CNN NewsNight segment: "LOWER THE RATE OR I'LL STOP TRADING WITH COUNTRIES WITH
WHICH WE HAVE A DEFICIT ... IT'S BETTER THAN TARIFFS! The Fed Board, with its great new leader, must get
smart — BE PATRIOTS for a change." Matches research.json's `fed_trade_threat` entry exactly.

No swap needed — the story had ample usable video.

## Sources used (all real outlets, all within the Aug 14 – Sep 16 2026 window)
1. **CNN** — "Is Trump threatening to sabotage the economy to force Fed rate cuts?" (CNN NewsNight,
   uploaded 2026-09-05). Anchor reads Trump's exact Truth Social quote over a graphic of the actual post
   (visibly timestamped Sep 04, 2026, 9:41 AM) — this is the clip carrying the literal quote SOT, since
   the quote itself was written, not spoken by Trump on camera.
2. **Forbes Breaking News** — "Trump Publicly Urges Kevin Warsh, Federal Reserve Not To Hike Interest
   Rates" (uploaded 2026-09-01). Real, on-camera Trump audio/video from an Oval Office press
   availability. Word-level auto-captions made these cuts easy to trim precisely. Two SOTs used:
   "we have the right to stop doing business with them" and "they would go from a so-called elite
   country to a poverty-stricken country" (the latter marked `cold_open_candidate`).
   - **Caveat**: the on-screen banner during this clip reads "PRESIDENT TRUMP MAKES A HEALTHCARE
     AFFORDABILITY ANNOUNCEMENT IN THE OVAL OFFICE," dated August 31, 2026 — four days before the
     Sep 4 Truth Social post. This is a reporter's off-topic question during an unrelated presser, not
     footage of the Sep 4 moment itself. The words are real, on-camera, and on-topic (Trump making the
     exact same trade-for-rate-cuts argument in his own voice, as part of the same pressure campaign
     research.json describes), but it predates the specific post by a few days. Flagging this so the
     assembler doesn't caption it as "Sep 4" — the beat captions don't claim a date, only quote the
     words.
3. **MS NOW** (formerly MSNBC) — "Trump's threat to halt trade 'will make the Great Depression look
   like a walk in the park': Analyst" (uploaded 2026-09-08). Real economic commentator on the
   "Money Power Politics with Stephanie Ruhle" program, discussing this exact story.
   - **Caveat**: auto-captions had a ~2s gap between "IT WILL MAKE THE GREAT DEPRESSION" and "LOOK LIKE
     A WALK IN THE PARK" with no detected silence in the audio track across that gap (confirmed via
     ffmpeg silencedetect) — meaning the analyst likely said a few words the captions dropped. Transcript
     is written as "It will make the Great Depression ... look like a walk in the park" with an ellipsis
     to flag the possible gap honestly rather than guess at filler words.

## Method notes
- All excerpt in/out points were derived from YouTube auto-caption timestamps. Where captions had only
  cue-level granularity (CNN, no `<c>` word tags), I cross-checked cut points against `ffmpeg
  silencedetect` on the downloaded segment to avoid cutting mid-word. Where captions had word-level
  `<c>` tags (Forbes), cuts are precise to those timestamps.
- All clips re-encoded h264/aac via ffmpeg from `--download-sections` pulls (or full download for the
  170s Forbes video, which was short enough to grab whole).
- No stock footage used — real news footage covered every beat, so the ≤10% stock allowance wasn't
  needed.
- `raw/` (full/segment downloads used only as cutting sources) deleted after trimming, per spec.

## incoming_from_assembler
The assembler had pre-fetched `fed_cnn_quote.mp4` (a ~29s pull from the same CNN NewsNight video,
9aamEcWOeyY) with a note suggesting the same "Lower the rate or I'll stop trading..." anchor-read SOT
I independently found and cut as `n6_sot_quote`. My cut is equivalent (same source, same quote) but
trimmed more precisely against `ffmpeg silencedetect`. I additionally sourced two more outlets
(Forbes Breaking News for real on-camera Trump audio, MS NOW for analyst reaction) that the assembler's
note flagged as not yet fetched, giving the story 3 sources instead of 1. Deleted the redundant
pre-fetched raw file after confirming my own clip covers the same ground; kept nothing duplicated.

## Runtime check
- 4 SOT beats, 17.2s combined (~35% of estimated ~49.4s total runtime) — within the 25–40% target.
- 9 beats total (5 narr / 4 sot), alternating, starting and ending on narr.
- 8 clips, 3 sources (CNN, Forbes Breaking News, MS NOW), max 3 excerpts from any one source (limit is 6).
- Folder size ~31MB after cleanup, well under the 500MB cap.
