# notes: n1_un_meltdown

## Fact checks / judgement calls

- **"The people that did it should be arrested!"** — verified via the CNBC source article
  (playwright fetch, CNBC blocks WebFetch/browser-pane with a 403/Access-Denied). This was
  **written** in a Truth Social post, not spoken on camera. Per the sot/visual distinction in
  the contract, it is NOT used as a `sot` beat with a transcript — I left it out of the beats
  entirely rather than risk a fabricated "spoken" quote. If a future pass wants it, it should
  be a text-graphic visual (quoting the post), not a captioned SOT.
- **Escalator visual (`n1_visual_escalator`)** shows Trump and Melania climbing the *stalled*
  escalator on foot after it stopped — not the exact instant it lurched to a halt (no clean
  real angle of that exact frame surfaced in the search; several "watch it stop" titles turned
  out to be re-edited audio-only recaps, not the raw moment). This is still 100% real pool
  footage (Bloomberg, via azcentral.com syndication), dated Sept. 23 in-video, and clearly
  shows the aftermath (walking, not riding) which reads clearly on screen. Noted in `shows`.
- **"I have ended seven unendable wars."** — PolitiFact rated this Mostly False (several listed
  conflicts weren't actively raging, or the ceasefire credit belongs to other mediators). This
  is reflected in beat 9's narration, attributed to PolitiFact, not stated as fact.
- **Windmill quote trimmed**: the full line ("...so expensive to operate, and they have to be
  rebuilt all the time and they start to rust and rot") runs ~10s and can't fit the 5.0s cap.
  Used the first, funniest clause only ("Those big windmills are so pathetic and so bad.") —
  a complete sentence on its own, not a misleading truncation.
- **"Seven unendable wars" clip**: trimmed to "I have ended seven unendable wars," dropping the
  preceding "Likewise, in a period of just seven months" for time. Meaning is unchanged.
- All five SOT clips come from the same C-SPAN full-speech upload (5 of the max 6 excerpts
  allowed from one source video). Auto-caption word-level timestamps were used to find in/out
  points; each clip has ~0.1-0.3s of pre-roll silence to avoid clipping the first consonant.

## Banner placement

C-SPAN's own "TRUMP SPEAKS AT U.N. GENERAL ASSEMBLY" banner sits at the very bottom of frame on
all five SOT clips. SOT captions should be placed in the upper-to-mid frame, not stacked on that
banner (per format.md: captions "placed away from the source's own banner"). Not cropped or
hidden, just don't overlap the caption text with it.

## Runtime / mix

- 5 SOT clips (teleprompter 3.5s, escalator recap 3.8s, hell 2.1s, windmills 4.4s, wars 4.0s)
  = 17.8s of SOT.
- 6 narr beats, short (13-17 words each) to keep total story runtime near ~55s given the SOT
  total; SOT ends up ~32% of story runtime, inside the 25-40% target.
- Cold open candidate: `n1_sot_teleprompter` ("Whoever is operating this teleprompter is in big
  trouble.") — biggest, cleanest laugh line in the story (long laughter/applause follows it in
  the raw C-SPAN audio).

## Visual variety

Only one dedicated non-SOT visual b-roll clip was found (the escalator climb). Narration beats
reuse the other SOT clips muted for cutaways, as explicitly allowed by format.md ("cycle other
clips from the same story (muted SOTs too)"). No stock footage was used — this story is 100%
real event footage.

## Downloads cleaned up

Full-length source downloads (C-SPAN 57-min speech, misc candidate videos, subtitle files,
frame grabs) were kept only in the session scratchpad, not in this story folder. Only the six
final trimmed clips (~2.8 MB total) live in `clips/`.
