# n1_venezuela_run_it — notes

## Source
All 5 SOT clips come from one video: USA TODAY, "Full Trump press conference on
Maduro capture mission, attack on Caracas and vision for Venezuela"
(https://www.youtube.com/watch?v=_VMddyKM7fE), uploaded 2026-01-03 — matches the
event date in episode.json. Confirmed via auto-sub grep with word-level timestamps
before cutting, so no clip crosses a sentence boundary awkwardly.

Other real-outlet uploads of the same presser were confirmed live and dated
2026-01-03 (Reuters `plX1rO-CzuY`, Guardian News `cQdRlS4uf0E`, Fox News
`qXYsJtMPAq4`, Sky News `nEU01Pvvwh4`) but not used — USA TODAY's upload alone
had everything needed and using one source keeps captioning/banner handling
consistent. Max 6 excerpts/video rule: only 5 used.

## Fact-check judgement call: "fentanyl"
episode.json's `facts` field paraphrases Trump as saying Maduro was "flooding
America with deadly fentanyl" (this is the PolitiFact/Al Jazeera fact-checked
claim). I grepped auto-subs on all 4 fetched pressers (USA TODAY, Fox, Reuters,
Sky) for "fent*" and got **zero literal matches** — Trump never says the word
"fentanyl" on camera in this press conference. What he actually says is:
"[Cartel de los Soles] flooded our nation with lethal poison responsible for
the deaths of countless Americans."

Per the contract (SOT captions = exact spoken words, no invented quotes), the
`n1_sot_poison` clip is captioned with his real words ("lethal poison"), not
"fentanyl". The narr beat right before it does the attribution work instead,
crediting PolitiFact's characterization/fact-check by name rather than putting
"fentanyl" in Trump's mouth as an on-screen quote.

## Other judgement calls
- No B-roll of the Caracas strikes/aircraft was sourced (footage_ideas
  suggested it as a visual option). Time was spent instead verifying the
  precise wording of Trump's own quotes; all visuals under narration reuse the
  muted press-conference SOT clips, which is within the format's fallback rule
  ("cycle other clips from the same story, muted SOTs too"). This also keeps
  100% of the story's footage real, dated Jan 3 2026, no stock used.
- Kept language to Trump's rhetoric and the press conference itself; no
  claims about strike casualties, military tactics, or outcomes beyond what
  the sources state (capture of Maduro + wife, indictments, oil-seizure plan).
  Satire targets "we're going to run it" / "safe, proper, judicious
  transition" phrasing, not the operation's human cost.
- `n1_sot_darkdeadly` ("It was dark. And it was deadly.") marked
  `cold_open_candidate: true` — it's the most quotable/absurd line and stands
  alone without extra context.

## Runtime estimate
5 SOTs = 16.1s. 6 narr beats ≈ 86 words ≈ 37.4s. Total ≈ 53.5s, SOT ≈ 30% of
story runtime — within the 45–55s / 25–40% SOT targets.
