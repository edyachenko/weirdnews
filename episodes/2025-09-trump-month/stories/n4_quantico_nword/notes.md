# n4_quantico_nword -- notes

## Fact checks
- Event: Trump's address to hundreds of generals and admirals summoned to Marine Corps
  Base Quantico, Sep 30, 2025 (Defense Secretary Hegseth's event). Confirmed by CNN,
  LiveNOW from FOX, Washington Post and others all uploading same-day (20250930).
- "You never heard Biden say that" (re: strongest military claim) -- PolitiFact rated
  the underlying claim pants-fire; CNN's Daniel Dale fact-check (same source video used
  for the wide establishing shot) independently found Biden said it repeatedly, citing
  a 2023 quote found "in about five seconds on Google." Source URL in beats.json sources.
- "I moved a submarine or two" / nuclear submarine to "the coast of Russia" -- Trump's own
  claim, not independently verified by any source consulted; presented as his own quote,
  not asserted as fact.
- "I call it the N-word... there are two N-words and you can't use either of them" --
  Trump's own self-censoring euphemism for the word "nuclear" (and, unstated but implied,
  the actual slur). No slur is spoken, printed, or implied in our captions -- we only
  quote Trump's own coy phrasing, matching how CNN, Newsweek and PolitiFact reported it.

## Judgment calls
- Auto-generated captions on the LiveNOW video transcribe the punchline as "There **were**
  two N-words..." (past tense). Newsweek's headline, the PalmBeachPost clip title, and
  research.json all independently transcribe it as "There **are** two N-words..." (present
  tense). Went with "are" -- auto-ASR misheard a fast "there're" as "there were"; three
  independent published transcripts agree on "are."
- Split the N-word joke into two separate SOT clips (setup: "I call it the N-word." /
  punch: "There are two N-words...") because the full unbroken quote runs ~6.8s, over the
  5.0s per-excerpt cap. Inserted a one-line narr bridge between them ("Turns out there's a
  second one, too.") rather than cutting the joke short.
- Could not find any wide shot or reaction shot of the officers' faces in the LiveNOW feed
  (single tight camera on Trump throughout). Sourced the "packed auditorium" wide shot from
  CNN's fact-check package instead (ecfkCzZfW_k), which re-airs event pool footage. It is
  presented inside CNN's own split-screen frame (with their banner and a Daniel Dale inset)
  -- left uncropped per the never-crop-logos rule, so the CNN chyron/banner is visible in
  that visual clip. No genuine reaction shot of the officers' silence was found in any
  candidate source, so the "dead silence" line is carried by narration only, not a visual.
- No stock footage used; all clips are real event footage (LiveNOW from FOX, CNN). 0% stock.
- Story runtime estimate ~53s (narration ~39s + SOT ~14s), SOT share ~26% of runtime --
  within the 25-40% requirement but toward the low end because two of the four SOTs
  (submarine, N-word setup) are intentionally very short (2-4s) punchlines.

## Deleted after use
- Full-length CNN fact-check download (cnn_factcheck.mp4, ~90MB) and all padded segment
  downloads (seg_*.mp4) and subtitle/frame scratch files -- all lived in the session
  scratchpad, not in the story folder, and were not copied in.
