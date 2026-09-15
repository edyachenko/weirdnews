# Notes — n4_detroit_gaffe_fraud

## Fact checks
- Event: Trump spoke ~64 min to the Detroit Economic Club at MotorCity Casino, Jan 13, 2026. Confirmed by three full-length
  real-outlet uploads from that date (CNBC Television, Right Side Broadcasting Network, PBS NewsHour), all dated 20260113.
- "If we stop this fraud... balanced budget" quote located in CNBC's full-speech auto-subs at 00:58:18–00:58:23 and used verbatim.
  PolitiFact rated this False per episode.json/research.json — the fact-check claim itself is not re-verified here beyond trusting
  the episode's source list, per the story-footage agent's scope.
- "Results are in... economic boom" quote located at 00:19:15–00:19:20 in the same CNBC video.
- ~200 protesters fact is sourced to CBS Detroit's own reporting (its correspondent says "swell to more than 200 people" at
  00:16–00:19 in Ht3uIQdL-SI) — matches the episode.json figure. Used MLive's B-roll (no reporter/banner) instead of CBS's
  stand-up footage for the visual since it shows the march itself, not a reporter with a US city standing in front of a blurred crowd.

## Judgement calls
- **n4_sot_moan is not literal speech.** The viral moment is a wordless, guttural noise, not a quotable sentence. I marked it
  `kind: sot` (real original audio, the actual joke) but the `transcript`/`caption` field is a bracketed description
  `[wordless moaning noises]` rather than "exact words spoken," since there are no words. Flagging this explicitly since it
  deviates from the schema's literal instruction — treat as the sanctioned exception for non-verbal SOT moments.
- The RSBN clip (jLVusTgk2RU) is a short (54s) highlight upload titled "President Trump Imitates Biden," not the full 64-minute
  speech. I could not find the exact absolute timestamp of this moment inside the full-length CNBC/PBS/RSBN replays to
  double-source it, so the moan SOT is sourced only from this one RSBN upload. Confirmed real outlet, dated 20260113, content
  matches the viral description (contorted face, eyes shut, extended non-verbal noise, ~8s gap in auto-captions from 10.4s–18.9s
  where no words could be transcribed). Visually verified via extracted frames before cutting.
- Both CNBC-sourced excerpts (n4_visual_venue, n4_sot_economic_boom, n4_sot_fraud_budget) come from the same source video
  (3SQ1HzLHq_k) — 3 of the allowed max 6 excerpts from one source used.
- No stock footage used; all 5 clips are real event/protest footage from real outlets uploaded Jan 13, 2026 (same day as the event).
- Two beats reuse another beat's SOT clip muted as filler visual ahead of its own SOT reveal (per format.md's "cycle other
  clips from the same story, muted SOTs too" rule) — n4_sot_economic_boom and n4_sot_fraud_budget each appear once muted in an
  earlier narr beat's visuals before their captioned SOT beat. This is intentional, not a duplicate-caption risk, since narr
  beats never show captions.

## Runtime estimate
- narr(8.7s) + sot(4.5s) + narr(7.8s) + sot(4.9s) + narr(7.8s) + sot(4.4s) + narr(9.6s) ≈ 47.7s — within the 45–55s target.
- SOT share: 13.8s / 47.7s ≈ 29% — within the required 25–40%.
- Real footage: 100% (no stock).

## Cleanup
- Deleted all full-length/raw downloads and intermediate frame JPEGs from the scratchpad after trimming; only the 5 final
  clips remain in `clips/`.
