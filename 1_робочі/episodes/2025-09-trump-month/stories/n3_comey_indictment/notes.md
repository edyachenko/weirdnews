# n3_comey_indictment — notes

## Sourcing
- All footage is from real-outlet YouTube uploads dated 2025-09-26 (one day after the
  Sept 25 indictment), well inside the "a few days after is fine" allowance.
- `n3_sot_others`, `n3_sot_hope`, `n3_sot_dirtycop`, and `n3_visual_oval` are all cut from
  the SAME source video (C-SPAN, `Fsti0Xq6NaU`, "President Trump on James Comey
  Indictment") — a raw, unedited South Lawn gaggle clip. That's 4 excerpts from one
  source video, under the max-6 cap. Using a single continuous C-SPAN take (rather than
  a network's edited package) was a deliberate choice: it's unedited/unnarrated real
  footage of Trump's actual on-camera words, so every SOT caption is exactly what he
  said, not a paraphrase read by an anchor.
- `n3_sot_comey_innocent` is Comey's own Instagram video statement, replayed by NBC News
  (`Lg3-PHvKL3c`). NBC overlays its own breaking-news banner, but the words are Comey's,
  not NBC's — captioned/labeled accordingly.

## Judgment calls / things NOT used
- The research brief's quote "He placed a cloud over the entire nation" and "I can only
  say that Comey is a bad person. He's a sick person..." could not be located as an
  on-camera Trump SOT in any real-outlet video searched (PBS NewsHour, Economic Times,
  LiveNOW from FOX, TODAY, CBS New York, MS NOW). Every version found was an anchor or
  narrator PARAPHRASING Trump's Truth Social post/remarks, not Trump's own voice. Per
  the "no invented quotes" and "exact spoken words" rules, this line was dropped rather
  than mis-captioned as a direct quote. The actual on-camera Trump lines used instead
  ("they're corrupt," "he's a dirty cop," "I hope there are others") make the same
  factual point (Trump publicly disparaging Comey and hoping for further prosecutions)
  and are verbatim.
- Did not use a graphic/text-card of the Truth Social post as a visual, per format.md's
  "Never: Full-screen text cards as visuals" rule, even though footage_ideas suggested
  it. Relied on real muted South Lawn footage instead.
- No stock footage used (0%) — real footage covers 100% of this story.
- `n3_visual_oval.mp4` is named to match the filename already referenced by the
  episode's intro/outro visual list in episode.json, even though the setting is
  technically the White House South Lawn, not the Oval Office itself — the id was kept
  as given for consistency with the rest of the assembly.

## Fact check
- Indictment date (Sept 25, 2025), two counts (false statements to Congress + obstructing
  a congressional proceeding), and the "hopes more opponents are prosecuted" framing all
  match the NBC News / PBS NewsHour sourcing in episode.json.
- Comey's "I'm innocent...let's have a trial" line is from his own Sept 26 Instagram
  video (as captioned by both NBC News and separately confirmed via PBS NewsHour's
  package covering the same clip) — this is Comey's own public statement, correctly
  attributed to him, not narration.

## Runtime / mix
- 4 SOTs, ~15.7s combined (~33% of story runtime) — within the 25-40% requirement.
- Estimated total story runtime: ~48s (within 45-55s target).
- `n3_sot_dirtycop` marked `cold_open_candidate: true` — the funniest/sharpest line.
