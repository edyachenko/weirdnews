# n5_liberation_day — notes

## Source
Single source video for all clips: FOX 5 Washington DC, "FULL SPEECH: President Donald
Trump announces Trump Tariffs on 'Liberation Day'" (youtube.com/watch?v=c2bZto8YvEc),
uploaded 2025-04-02 — a real local-news broadcast affiliate carrying the full Rose Garden
event live, correct period. C-SPAN's own upload of the same event did not surface with a
usable full-length transcript in search, but this FOX 5 upload is the same live feed
(same camera angles/pool footage used by all outlets that day) and subtitles were
available for exact-quote timing. 5 excerpts pulled, under the 6-per-source-video cap.

## Fact checks / attribution
- "Declaration of economic independence" and "This is Liberation Day" are Trump's own
  words, spoken on camera — used as direct SOT quotes, not paraphrased.
- The claim that the "reciprocal" tariff formula was actually (trade deficit / exports)
  halved, not a real reciprocal-tariff calculation, is attributed to NPR per episode.json
  sources — stated in narration as "according to NPR," not asserted as the host's own claim.
- "One of the most mocked props of his second term" is attributed to Wikipedia per
  episode.json sources.
- No invented quotes; all sot captions are exact transcript text pulled from the video's
  auto-captions, cross-checked visually/audibly against the trimmed clip.

## Judgment calls
- Used a FOX 5 affiliate upload instead of hunting further for a C-SPAN-specific upload,
  since the poster-board reveal moment ("first row China 67% that's tariffs") needed to be
  visually identical to what's described in episode.json's footage_ideas regardless of
  which outlet's feed carries it — confirmed via frame grab that this is the exact
  "Reciprocal Tariffs" board with country rows and percentages.
- Marked n5_sot_poster_reveal as cold_open_candidate: true — it's the single most visual,
  most quotable moment (poster board fully in frame, Trump reading off tariff numbers
  like a game-show host), matching the brief's "best shot" note.
- No named-person-on-screen conflicts: all visuals are of Trump himself, who is the
  subject being discussed throughout — no stock footage was needed or used (0% stock).
- Two extra muted "visual" clips (chart_bring, gesture_numbers) were cut from the same
  broadcast, immediately before/after the poster-reveal SOT, to give narration real
  moving footage instead of a frozen frame, per format.md's no-frozen-frame rule.

## Runtime / composition
- 4 SOT beats (incl. reaction insert), ~15.8s combined (~31% of story runtime).
- 4 narr beats, ~33.9s combined at words/2.3 pacing.
- Total estimated story runtime: ~50s — within the 45–55s target.
- 100% real footage, 0% stock.

## Reaction insert (added 2026-09-21, per format.md "Reaction beats")
User watched the rough cut and called it "сухувато" (dry) — no comedic beat between the
poster-reveal SOT and the next narration line. Added one 2.6s real reaction insert
(`n5_reax_economist`) landing right after `n5_sot_poster_reveal`.

- Checked source 1 first: re-pulled the FOX 5 broadcast around the poster reveal
  (00:19:20–00:20:25) frame by frame. It's a single fixed pool camera the whole time —
  no cutaway to Cabinet, crowd, or press exists in that footage to recut. Ruled out.
- Went to source 2: CNN's own YouTube channel, "Erin Burnett breaks out whiteboard to
  explain Trump's tariff math" (youtube.com/watch?v=XTwNUl-v57s, uploaded 2025-04-09,
  same news cycle). Real primary source, not a reaction/meme channel. Guest is Brent
  Neiman, University of Chicago economist whose own research the White House cited (and
  misapplied) to justify the tariff formula — exactly the "economist reacting" case
  format.md calls out.
- Clip used (00:01:09.3–00:01:11.9): Neiman recounting seeing the Rose Garden poster blow
  up his phone mid-seminar — "...with apologies to the speaker, I couldn't really focus."
  CNN's own on-screen chyron reads "ECONOMIST: WH USED MY TARIFF RESEARCH AND GOT IT
  'VERY WRONG'" — native to the source, not added by us.
- Calibration: this is a moderately absurd moment (a real, widely-mocked prop built on
  fake math), not a maximally absurd one. A dry, real admission from the economist whose
  own work got mangled is proportionate — undersold on purpose, no meme energy, no
  editorializing beyond what CNN itself aired.
- Encoded h264 + aac from the original YouTube source, ≤5s (2.6s), matches existing
  clips.json/beats.json schema.

## Second reaction insert (added 2026-09-21, per revised format.md — at least 2 inserts per story, spread across SOTs)
Format.md was revised same day to require at least two reaction/punch inserts per story,
spread across different SOTs, not stacked after only the strongest moment. This story had
one (`n5_reax_economist`, after the poster-reveal SOT); searched for a second one landing
on one of the two earlier, less-visual SOTs ("This is Liberation Day" / "Declaration of
economic independence").

- Source 1 (same-clip reaction) ruled out again: the FOX 5 broadcast around both of these
  lines (00:00:26–00:00:30 and 00:02:13–00:02:19) is the same single fixed pool camera —
  no Cabinet/crowd cutaway exists to recut.
- Source 2 (named satire show reacting to the same event) found: SNL's own YouTube
  channel, "Trump Tariff Cold Open - SNL" (youtube.com/watch?v=VEle3pZRqmI), uploaded
  2025-04-06 — same news cycle, four days after the actual speech. James Austin Johnson's
  Trump impression, in the cold-open Rose Garden recreation, punches the exact
  self-congratulatory "great/wealthy" framing of the real speech with "Make America Great
  Depression again" (00:01:10.3–00:01:12.7, 2.6s). This is the show's own official upload
  of its own segment — a real primary source per format.md's exception, not a reaction-
  channel clip of someone else's footage.
- Added as `n5_reax_snl_magda`, placed right after `n5_sot_declaration` ("It's our
  Declaration of economic independence") — the other still-bare SOT that hadn't gotten a
  reaction beat. Now inserts land after 2 of the 3 original SOTs, not just the strongest
  one.
- Calibration: SNL's joke targets the same grandiosity the real line invites (dry pun on
  MAGA landing right where Trump promises prosperity), not a bigger claim than the source
  moment supports — proportionate, no invented exaggeration beyond what SNL itself aired.
- Only the 5-second needed section was fetched via `yt-dlp --download-sections`, never the
  full 396s video; re-encoded to h264 (yuv420p) + aac, 2.57s, matches existing
  clips.json/beats.json schema (`"banner": "none"`).
- Story now has 2 reaction inserts across 2 different SOTs; the third SOT (poster reveal)
  already carries the CNN economist insert. No further search was done for a third insert
  since 2 is the target floor and both remaining un-reacted moments (this one, and general
  visual beats) don't call for it as urgently — could revisit if the user wants a third.

## Cleanup
All full-length source downloads and intermediate segment files were removed from
/tmp after trimming; only the seven final ≤5s clips remain in clips/.
