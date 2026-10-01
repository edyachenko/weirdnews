# n4_easter_autopen — notes / fact checks / judgment calls

## Facts vs. framing
- Trump's autopen story about Biden being "incapable of signing" and followed around by "a big
  machine" is a fabrication per BuzzFeed / Daily Beast / AOL coverage of the April 21, 2025
  Easter Egg Roll — video of Biden's real bill signings shows him signing by hand. Beats.json
  frames this explicitly as a false claim, attributed to the sources, not as our own assertion.
- The "confused kid" detail from episode.json ("audibly asked What?") could not be pinned to an
  exact, isolated, transcribable line. I pulled subtitles (YouTube auto-captions) and ran
  OpenAI Whisper on the two best source videos (The Independent, Reuters) and on isolated
  sub-segments; in both, only Trump's mic'd audio and a couple of adjacent adult voices ("Somebody
  wrote it," "Oh, that's nice") are clearly transcribable — no child's voice comes through clearly
  enough to quote as a verified SOT line. Per the "no invented quotes" rule I did NOT fabricate a
  "What?" quote. Instead I used the visibly puzzled/scrunched-face reaction of a small child at the
  table (clearly visible in the Reuters footage around 0:08–0:11) as a **muted visual beat**
  (`n4_visual_confused_kid`), which still delivers the comedic beat visually without a bogus
  transcript.
- Marked `n4_sot_autopen_bigmachine` as the `cold_open_candidate: true` clip — it's the tightest,
  funniest self-contained line ("this big machine, you know what it's called? An auto pen") and
  includes the exact "big machine" phrase called out in the footage brief.

## Footage sourcing
- Two independent pool-video re-uploads of the same coloring-table moment were used (The
  Independent, Reuters) — both are legitimate news outlets with same-day (20250421) uploads, and
  the two together let me stay under the 6-clips-per-source cap while getting 3 distinct SOT
  lines and 2 muted visual cutaways from different framings/angles of the same scene.
- Contrast footage: real archival clip of Biden actually signing a bill by hand (The Independent,
  "Biden signs burn-pits bill into law," 2022). This is genuine footage of Biden himself, not
  generic Pexels stock, so it does not count against the story's stock budget — it directly
  illustrates the fact-check ("video of Biden's actual bill signings shows him using a pen
  himself") while Biden is being discussed, which stock footage would not be allowed to do.
- Did not use the White House's own NBC News live-stream (2600s+) or the ABC News podium-remarks
  video (432s) — neither contains the autopen tangent (that happened at the coloring table, a
  separate segment from the podium remarks ABC/other outlets carried).
- Skipped "Diario AS," "Sweet Hot T," and other aggregation/reaction-style channels per the
  "skip reaction/compilation channels" rule.

## Runtime / mix
- 3 SOT beats totalling 14.7s, narration totalling roughly 34s of intended TTS runtime at
  words/2.3 → story runs approximately 48–49s, SOT ≈ 30% of runtime — inside the 25–40% target.
- 100% real footage; the one non-SOT clip without original dialogue (Biden signing) is real
  archival video, not stock, so overall the story uses 0% Pexels/generic stock.

## Cleanup
- All full-length source downloads and intermediate frames/subtitle files were deleted from the
  scratchpad after trimming; only the six final clips remain in `clips/`.
