# n3_six_wars — notes

- **Event date vs. clip framing:** the quote ("I've done six wars...") is from the Aug 18, 2025 Oval
  Office session with Zelenskyy (ANI News, pool footage, uploaded same day). `n3_visual_1` is real
  footage from the *same visit* but a different, later portion of it — the East Room multilateral
  table meeting with European leaders (CBS News full video, also uploaded Aug 18, 2025) — used as
  scene-setting b-roll under narration, not captioned as the moment the quote was said.
- **n3_sot_4 double duty:** the clip's audio is a WION anchor's narration ("India has repeatedly
  rejected...") over real b-roll of the White House group photo (Trump/Zelenskyy/Macron). Treated as
  an anchor SOT (kind: sot) since the spoken audio is a real, on-air, attributable statement, even
  though the on-screen face isn't the speaker.
- **India-Pakistan claim not independently verified in-frame:** episode.json's facts note India's
  government disputes Trump's credit-taking; I did not find a clip of an Indian official denying it
  within the Aug 2025 window from real-outlet channels in the time available, so the "dispute" side is
  carried by the WION anchor SOT (n3_sot_4) + narration, both attributed to WION, rather than a direct
  Indian-government soundbite. Sourced further in Axios/Deccan Herald (see beats.json sources).
- **ANI overlay graphics:** n3_sot_1 / n3_sot_2 carry ANI's own added "SOURCE: UNRESTRICTED POOL VIA
  REUTERS" caption plus a REC/battery HUD frame — this is ANI's own on-screen branding (kept uncropped
  per the never-hide-logos rule), not an editorializing chyron; underlying footage is real pool video
  of the Oval Office meeting.
- **Only 2 source videos used** (ANI: 2 excerpts, WION: 2 excerpts), well under the 6-per-source cap.
- **Runtime estimate:** ~50s (SOT ≈16.5s / ~33%, narration ≈33.5s across 5 beats, all ≤35 words).
- Full-length downloads and temp working files were deleted from /tmp after trimming; only the five
  final clips (≤5.0s each, all real footage, no stock) remain in `clips/`.
