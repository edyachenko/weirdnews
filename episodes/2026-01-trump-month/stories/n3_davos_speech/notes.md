# n3_davos_speech notes

## Source
Single source video for all 6 clips: The White House (official channel), "President Trump Delivers a
Special Address to the World Economic Forum", uploaded 2026-01-21 (id `prdSj9caeQw`), duration 1h35m.
It's a single fixed camera on the podium for the whole speech, so all clips share the same framing,
backdrop (WORLD ECONOMIC FORUM step-and-repeat), and a persistent bottom lower-third
("TEXT 'POTUS' TO 45470..." / "THE WHITE HOUSE" bug) -- not hidden or cropped, per the never-list.
6 excerpts pulled from this one video, at the contract's per-video cap.

Other candidates found (AP, WSJ, NBC, Times Now) were not needed since the official WH upload already
had clean audio, correct date, and no overlay graphics of its own layered on top of the speech.

## Quote/timing judgment calls
- The AI line in research.json ("We're leading the world in AI by a lot. We're leading China by a lot.")
  runs ~5.9s in the source with a rhetorical pause after "AI" -- too long for the 5.0s cap even trimmed.
  Used only the second half, "We're leading China by a lot." (1.6s), which is the specific claim
  PolitiFact fact-checked. The "leading the world in AI" framing is carried by narration instead.
- The credit-card SOT is trimmed to start at "cap credit card interest rates..." rather than "I'm asking
  Congress to cap...": at <=5.0s the full sentence didn't fit cleanly on a word boundary starting from
  "I'm". Caption reflects only the words actually audible in the clip.
- "in violation of the law" (the Truth Social claim) is not a video SOT -- it was posted on Truth Social,
  not spoken on camera. Handled as an attributed narration fact instead (research.json/episode.json both
  describe it as a Truth Social post, not a broadcast remark), so no risk of implying it's the Davos SOT.
- Greenland SOT uses the "I don't have to use force / I don't want to use force / I won't use force"
  triple repetition (4.5s) rather than the single "won't use force" line quoted in episode.json's facts
  paragraph -- it's the same claim, verified against the source captions, and reads stronger on screen.
- All timings verified two ways: yt-dlp auto-sub word-level timestamps, then ffmpeg silencedetect on the
  cut clips to confirm no word is truncated at either edge (checked n3_sot_ai, n3_sot_force,
  n3_sot_creditcard specifically).
- Visual (muted) cutaways are all from the same single-camera feed at timestamps away from the three SOT
  lines. One early candidate frame (00:00:00-00:00:05) turned out to show the WEF host introducing Trump,
  not Trump himself -- discarded and replaced with a Trump-only moment (n3_v_open, now 17:56.0-17:58.6,
  immediately before the AI SOT) so every visual clip actually shows Trump per the facts being narrated.

## Runtime estimate
~54.6s (4 narr beats, ~101 words / 2.3 ~= 44s; 3 SOTs totaling 10.7s -> SOT is ~20% of runtime).
Note: SOT share is below the 25-40% target range because the available clean, on-topic quotes for this
story are inherently short (1.6s, 4.5s, 4.6s) once trimmed to the 5.0s cap and to words actually spoken;
padding them further would have meant including adjacent unrelated sentences.

## Cleanup
Full-length source download was never made -- only --download-sections buffers (5-7s each) were pulled,
trimmed with ffmpeg, and the buffers deleted from scratch space afterward. Story folder is ~15 MB total.
