# n2_dc_crime — notes

## Fact checks used
- MPD's own 2024 stats: violent crime at a 30-year low; the Aug 11 press event repeatedly
  claims the opposite ("complete and total lawlessness"). Confirmed via NBC News' own
  reporter line in the same package: "crime statistics from the US attorney's office in
  January said violent crime in DC was at a 30-year low... down 26% since last year."
- The "41 per 100,000 / No. 1 in the world" homicide claim from episode.json's facts was
  NOT captured on camera in any of the source videos checked (NBC News E7Z5OB9nq2w, AP
  Archive 585IJcaKMTM, CNN uGzBrzs8nbc, CBS News qPBu5p2_sU4, WRAL HZ0W4msiLiI). Those
  videos cover the Aug 11 announcement and its immediate fact-check, not the specific
  international-comparison remark. Used the two claims that ARE on camera instead
  ("complete and total lawlessness" and the "bloodshed, bedlam, and squalor" line), which
  are covered by the same PolitiFact/Al Jazeera source set (both fact-check the general
  "lawlessness" framing against MPD's actual numbers).

## Judgement calls
- n2_sot_squalor (AP Archive) and n2_sot_lawlessness / n2_sot_liberation / n2_sot_gonedown /
  n2_sot_autonomy (NBC News) are ALL from the same Aug 11, 2025 White House press briefing
  (confirmed by identical backdrop/podium and by AP's own upload date 20250817 packaging
  footage from that Aug 11 event — AP Archive dates its fact-check package, not the event
  itself). Captions/dates in clips.json use each outlet's own upload_date, not the event
  date, per the format's "not up for discussion" rule on excerpt limits, but the story text
  avoids claiming a specific news date beyond "he announced."
- Speaker correction: I initially assumed the "gone down from what" NBC segment was Trump
  by transcript position; a frame check showed it's Jeanine Pirro (US Attorney for DC), so
  clips.json/beats.json attribute it to her, not Trump. Re-trimmed to the funnier, more
  self-contained "Nambi Bambi response" line from the same clip for the cold-open candidate.
- n2_sot_autonomy speaker is DC Mayor Muriel Bowser (lower third confirmed via frame grab),
  matching footage_ideas' expectation of local pushback.
- n2_visual_patrol (AP Archive, National Guard on the National Mall) is a portrait/vertical
  source clip with pillarboxing — used muted purely as b-roll under narration, not as a SOT,
  so the aspect mismatch shouldn't be visible as more than a soft-edged crop depending on
  the render pipeline. Flagging in case the assembler wants to crop/scale it instead.
- Visual variety is limited: only one dedicated b-roll clip (National Guard patrol) was
  found within a reasonable search budget. Narr-beat visuals lean on muted reuse of the
  story's own SOT clips per the "cycle other clips from the same story (muted SOTs too)"
  rule, rather than a wider stock-free b-roll set.

## Runtime estimate
- SOT total: ~20.65 s (5 clips) — comfortably >3 SOTs.
- Narration: ~79 words ≈ 34 s.
- Story total: ≈55 s, SOT ≈37% of runtime (within the 25–40% band).

## Not used
- CNN (uGzBrzs8nbc) and WRAL (HZ0W4msiLiI) transcripts were pulled and reviewed but turned
  out to be panel discussion / anchor narration without a clean standalone Trump or
  official SOT under 5 s, so no clips were cut from them.
