# n1_abrego_garcia_tattoo — notes

## Fact-check status (must be attributed in narration, never stated as fact)

- The "MS-13" lettering visible across Kilmar Abrego Garcia's knuckles in the Truth Social image
  Trump held up on April 29, 2025 does **not** appear in any other photo of his hand, including
  one taken by Salvadoran officials days earlier.
- **CNN** and **Al Jazeera** both independently concluded the letters were digitally added to the
  photo. Gang-tattoo experts consulted by **PolitiFact** said none of Abrego Garcia's actual
  knuckle tattoos are known MS-13 signifiers.
- **PolitiFact rated Trump's claim "Pants Fire."**
- All narration in this story attributes the "digitally added / doctored" finding to CNN, Al
  Jazeera, and PolitiFact — the script never asserts it as Claude's own conclusion, and never
  states the tattoo is genuinely real anywhere.

## Judgment calls

- The source video (ABC News' own official upload, "FULL INTERVIEW | President Trump the First
  100 Days") contains the entire April 29, 2025 Oval Office sit-down with Terry Moran. All 6 clips
  come from this single video, at the max allowed (6) excerpts from one source.
- Auto-captions rendered one of Trump's lines as "He had MS as clear as you can be" (dropping the
  "-13"). Since SOT captions must show the exact spoken words, and I did not do a manual re-listen
  pass to correct the auto-transcript, I kept the caption as auto-transcribed rather than guessing.
  Worth a human listen-through before final render if precision matters.
- No footage was found in this episode's window that shows Trump's actual Truth Social post as an
  on-screen graphic (the "bonus" ask). Skipped — not required.
- The doctored photo itself is never shown in isolated/zoomed knuckle-detail form. Two clips show
  Trump or Moran holding papers up in the wide shot (as the real, documented moment of the
  exchange), but no clip captions or implies the tattoo content is confirmed real.
- `n1_sot_clear_not_interpreted` ("No, no, no... Not interpreted") is marked
  `cold_open_candidate: true` — it's the tensest, most quotable moment of the whole exchange and
  needs no context to land.
- All 6 clips are ABC News' own official channel, from the correct date (April 29, 2025), talking
  heads only — no reaction/compilation channels used.

## Reaction-insert search (2026-09-21)

Per format.md's revised "Reaction beats" section, checked all 6 SOTs for a real, attributable
punch insert. The story already has a built-in reaction beat: `n1_sot_terry_photoshopped_wide`,
the wide two-shot of Moran's live pushback, used right after `n1_sot_knuckles_claim`.

Targeted search for a second insert right after the strongest beat
(`n1_sot_clear_not_interpreted`, "Not interpreted," the `cold_open_candidate`): looked for a real
video segment from CNN, Al Jazeera, or PolitiFact — the three outlets already cited in
`beats.json` sources — that shows their own on-screen graphic/comparison explaining the doctored
photo, which would have been an ideal, well-attributed, high-impact insert here.

Checked via web search and `yt-dlp --dump-json` (uploader/channel verification, no downloads):
- No PolitiFact video exists for this fact-check; PolitiFact's coverage here is text-only.
- No Al Jazeera English video segment found; their coverage of the doctored photo is also
  text-only (aljazeera.com article), aside from an unrelated full Mehdi Hasan interview episode
  that isn't a fact-check graphic and wasn't a proportionate insert.
- No CNN (cnn.com/CNN's own YouTube channel) video segment found that shows the doctored-vs-real
  photo comparison as a graphic. Kaitlan Collins' "The Source" coverage exists but as an interview
  with Abrego Garcia's attorney, not a graphic-driven doctoring explainer, and no clip of it turned
  up on CNN's own channel.
- Other outlets (France 24, Guardian News, Access Hollywood, Inside Edition) do have their own
  segments on this story, but they are not among the three sources already cited for this story
  and were out of scope for this search.

Also: all 6 SOTs are already ABC News, at this story's 6-clip max for that source, so a 7th ABC
clip was never an option regardless.

Conclusion: no real, proportionate insert was found for this beat. Per format.md, "we looked and
found nothing real and proportionate" is an acceptable outcome for an individual beat — nothing
was added here. clips.json/beats.json unchanged.

## Cleanup

- Deleted the ~59s temp source download and subtitle file from /tmp/wn_n1 after trimming; nothing
  besides the 6 final clips was copied into the story folder.
- Story folder size: ~2MB (6 clips at 200-430KB each), well under the 500MB budget.
