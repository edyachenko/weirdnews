# n1_vaccine_soda — notes

## Framing (non-negotiable rule, confirmed followed)
Both false claims are paired with their real correction in the very next beat,
never left standing alone:
- Beat 2 (sot, Trump "quite lethal") -> Beat 3 (narr) states PolitiFact's
  Pants Fire rating and that MMR has decades of safety data and isn't lethal
  combined.
- Beat 4 (sot, Trump "soda bottle") -> Beat 5 (narr) gives the real math
  (≈0.5 mL dose vs. ≈591 mL soda bottle, 600-1200x overstatement) -> Beat 6
  (sot, AP medical expert) reinforces it on camera: "So I don't know where he
  got this example with the soda bottle."
No beat shows a false claim as the final word; every false-claim beat is
immediately followed by a correction beat.

## Fact checks / sourcing
- Both Trump quotes verified verbatim against LiveNOW from FOX's unedited
  signing-event footage (IVKZ0wy72lA), auto-captions cross-checked against
  CNN's own on-air replay of the same clips (O4sBG32XN3Q) — wording matches.
- "Quite lethal" claim occurs ~00:02:23 in the LiveNOW video (Trump discussing
  splitting MMR into 3 doses); "soda bottle" claim occurs ~00:02:57, same
  continuous remarks, same event, same date (Aug 10, 2026 Oval Office signing).
  Not pulled from a different day — same unbroken take.
- AP Archive clip (dZi8r8_zsCg) is a separate, later upload (20260816) reacting
  to the EO — used only for the expert's spoken assessment, not claimed to be
  from the signing day itself.
- The AP Archive speaker is not named in the auto-captions and I did not
  independently verify his identity, so `shows` intentionally does NOT name
  him (avoided a tempting but unverified match to a differently-sourced CNN
  interviewee "Dr. Chris Parnell" seen in the same CNN video — different
  person/segment, would have been a misattribution).
- CNN's Erin Burnett syringe-vs-soda-bottle demo (same video, ~00:02:06) cites
  "the single dose 0.5 mL in one MMR vaccine" on air, consistent with the
  0.5-1 mL figure in the brief.

## Judgement calls
- Dropped the Trump "...they could be explosive" follow-up line (same video,
  ~00:34:40, a reporter later asks him to defend the "lethal" claim and he
  doubles down) to keep the story within the ~45-55s budget and avoid a second,
  redundant lethal-claim/correction pairing. Noting it here in case a future
  edit wants it — timestamps: reporter challenge 00:34:11.4-00:34:16.4,
  Trump's reply 00:34:39.9-00:34:42.9, same source video.
- Reaction inserts: searched once (`ytsearch15: Trump vaccine soda bottle
  reaction SNL Daily Show meme`) per the format.md method — no SNL/Daily Show
  segment on this specific story turned up (generic SNL back-catalog only).
  Did not re-search. Used tier 2/3 instead: CNN's own on-air reaction
  ("Now that's nonsense") and Erin Burnett's real prop demo (soda bottle next
  to the actual tiny syringe) as the two reaction/punch inserts — both real
  broadcast footage, both proportionate rather than meme-amplified, matching
  the calibration note for a medical-misinformation story (undersell, don't
  bolt on fake energy).
- SOT share of runtime lands at ~24% (12.3s of ~52s), just under the 25-40%
  band. Kept at 3 SOTs rather than adding a 4th purely to hit the percentage,
  per the budget instruction to stop once requirements are met (≥3 SOT clear,
  ≥2 reaction inserts clear).
- Host narration never diagnoses Trump personally — all correction language
  is about the claims ("that claim", "his math") and sourced to PolitiFact/
  CNN/FactCheck.org, not a medical opinion about him.

## Technical
- All 3 source videos required `--extractor-args "youtube:player_client=android"`
  for subtitle fetch (default client hit HTTP 429, shared-IP rate limit noted
  in the agent contract); actual video section downloads worked fine with the
  default client.
- Folder size well under 500 MB; raw full-length downloads were never made
  (only `--download-sections` ranges), and those section-raw files live in
  the scratch dir, not the story folder.
