# n1_pentagon — notes

## Story kept as assigned (no swap needed)
Two independent, on-topic real-footage sources found; no need to invoke the swap rule.

## Sources used
1. **The White House** (official, public domain), `wmRa6CGygzc`, "President Trump and the First
   Lady Participate in the 9/11 Observance Ceremony," 2026-09-11. Reused the already-cut 17s
   local file from v2 (`incoming_from_assembler/pentagon_911.mp4`, absolute 01:11:51-01:12:08 of
   the source) rather than re-downloading. Word-level auto-caption timing (`wmRa6CGygzc.en.vtt`)
   confirmed the sequence: "...September 11th," ends 01:11:58.95 -> next word "2001." doesn't
   start until the caption block reaches 01:12:00.3 -> "Very famous date, unfortunately." follows
   immediately. Ran `ffmpeg silencedetect` on the local clip as a second check: a genuine ~1.9s
   silence gap shows up right where the captions place it, corroborating the "long pause" framing
   used in `research.json` / the v2 script (auto-caption timestamps alone can lag; the silencedetect
   pass is the independent confirmation).
2. **CNN**, `y-03pMpkqDs`, "CNN fact checks Trump's 9/11 claim firefighters carried him away"
   (CNN's own title), upload date 2026-09-09 (i.e. published *before* the Pentagon speech --
   matches research.json's "earlier that week" framing for the firefighter claim). This is CNN's
   segment "The Source," and it contains genuine archival footage of Trump *in his own voice*
   making the firefighter-rescue claim at a separate 9/11 first-responders ceremony (white "USA"
   cap, firefighters/troops in dress uniform behind him) -- not just anchors talking about it. Used
   that as the 4th SOT rather than only Daniel Dale's fact-check commentary, since Trump's own
   claim is the stronger, funnier, more directly attributable soundbite. Downloaded only
   `*0:00-2:00` of this ~520s video via yt-dlp (single process, `--sleep-requests 1
   --sleep-interval 2`), then deleted the 36MB intermediate after trimming.

## Not used
- The WH-press-briefing "grasping at straws" quote (Anna Kelly) has no located video (per
  assembler's NOTE.md) -- kept as attributed narration only in beat 7, per the spec's guidance for
  this exact situation.
- Daniel Dale's on-camera fact-check lines were considered as a 5th SOT but cut to keep the SOT
  share inside the 25-40% band at the ~50s target runtime (adding a 5th ~4.9s SOT would have
  pushed SOT share to ~40%+ of a story that's supposed to stay ~45-55s total, or forced the
  runtime past the target to compensate). The claim/no-footage tradeoff already reads clearly
  without it: Trump's own claim (SOT) juxtaposed against the narrated fact ("no secondary
  corroboration") does the job.
- No stock footage used (0%, well under the 10% cap) -- real footage covered every beat.

## Clip-cutting notes
- `n1_sot_open` had to be trimmed shorter than the assembler's suggested 1.96-7.95 window (5.99s,
  over the 5.0s cap) -- cut to 53.76-58.50 absolute ("remember the victims..." rather than "We
  will always remember the victims..."), losing the first two words to fit under the limit.
- `n1_visual_podium2` is a 1.0s cutaway (the shortest clip in the set) used only as a brief bridge
  shot between the "2001" and "famous date" SOTs, which are adjacent in the real timeline; kept
  short and single-use deliberately rather than stretching it.
- All CNN and White House on-screen graphics (chyrons, "TEXT POTUS" banner, CNN bug/lower-thirds)
  left untouched, per the no-crop/no-hide rule.

## Fact-check status
Both quotes verified directly from primary video (word-level VTT + own silencedetect pass for the
Pentagon clip; CNN's own chyron text for the firefighter claim). `research.json` notes "secondary
corroboration not found" for the firefighter claim -- narration in beat 7 reflects this as "a claim
the White House dismissed," not as an established fact, and the CNN SOT itself is framed by CNN's
own on-screen chyron as a claim under fact-check, not as neutral footage.

## Runtime / mix estimate
- Narration: 78 words / 2.3 ~= 33.9s
- SOT: 4.77 + 3.20 + 4.85 + 4.96 = 17.78s
- Total ~= 51.7s (target 45-55s [OK])
- SOT share ~= 34.4% (target 25-40% [OK])
- Stock share = 0% (target <=10% [OK])
- Cold-open candidate: `n1_sot_2001` ("...2001.") -- the pause + gaffe, flagged in clips.json.
