# n5_smithsonian — notes

## Fact checks
- Core quote ("nothing about Success, nothing about Brightness, nothing about the Future") is from a
  Trump Truth Social post on 2025-08-19, not a spoken remark — so every SOT here is an anchor/analyst
  *reading or reacting to* the post, not Trump's own voice. No video of Trump speaking this line exists;
  none is claimed in captions.
- "America's brightness ... how bad slavery was" (WHAS11) and "how horrible our country is, how bad
  slavery was" (ABC7 Chicago, not used) both paraphrase the same post closely but are the anchor's
  paraphrase/read, confirmed against the ABC News source article's direct quote — wording matches.
- PolitiFact "Pants Fire" claim (closing beat) is attributed and matches the source URL in beats.json.

## Judgment calls
- **n5_sot_love (GMA, 01:04.6–01:08.0)**: the footage under this line is archival, on-screen dated
  "February 2017" (Trump's actual first-term visit to NMAAHC). The GMA package's own chyron
  ("TRUMP STEPS UP ATTACKS ON SMITHSONIAN MUSEUM") persists over it, so nothing here misrepresents the
  archival clip as current — the date stamp is baked into the footage and left visible/uncropped.
  Marked `cold_open_candidate: true` for the irony (he called the same museum "done with love" in 2017).
- **n5_sot_obscene (MS NOW / Eugene Robinson)**: the YouTube channel is "MS NOW" but the on-screen
  graphics all read "MSNBC" / "morning joe" (channel rebrand transition). `channel` field in clips.json
  uses the YouTube-reported name ("MS NOW") since that's the upload source; the caption label in
  beats.json uses "via MSNBC" to match what's actually burned into the video, per the rule that captions
  must reflect what's on screen.
- **n5_sot_brightness / n5_vis_museum_interior**: no outlet bug is visible during either b-roll cutaway
  (WHAS11 evidently drops its bug over VO shots) — nothing was cropped or hidden, there was simply
  nothing there to begin with. `banner: "none"` reflects that honestly.
- Skipped AP Archive's "Smithsonian visitors respond" (sXHVt0M2kVc) — real outlet, but uploaded
  2025-09-03, over two weeks after the Aug 19 event, outside the "a few days after" allowance.
- Skipped reaction/commentary/compilation channels turned up by search (Dwann B, NewsBOT Politics,
  Jesse Dollemore, The Black History Archives, KALW documentary) per the "skip reaction, compilation and
  AI channels" rule.

## Runtime / mix
- 4 SOT beats (WHAS11, GMA ×2, MS NOW), ~15.2s combined ≈ 31% of an estimated ~50s story — within the
  25–40% SOT target, ≥3 satisfied.
- Real footage 100%, 0% stock — Smithsonian/NMAAHC exterior and interior b-roll came from the same
  Aug 2025 news packages already in use, so no Pexels fallback was needed.
- Max excerpts from one source video: 3 (GMA — two SOT + one visual), under the 6-per-source cap.
