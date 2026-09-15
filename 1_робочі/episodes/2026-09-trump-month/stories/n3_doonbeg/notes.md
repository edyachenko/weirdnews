# n3_doonbeg — notes

## Fact check (confirmed against research.json + own verification)
- Trump said, in a bilateral meeting with Taoiseach Micheal Martin (White House video,
  2026-09-12): "I built it about 22 years, right on the ocean." Exact transcript per
  YouTube auto-captions on oaWMke0cdLo, word-timed 00:04:21.0-00:04:25.9.
- He did not build it. Per research.json: he bought the Doonbeg resort around 2014; the
  course was designed by Greg Norman and opened in 2002, under a different developer.
  Sources: Irish Star, Irish Times (both linked in beats.json `sources`).
- Rory McIlroy's actual on-camera quote — "that brings more attention and eyeballs to the
  Irish Open, and I think that can only be a good thing" — was located and used as a real
  SOT (see below), not just narration.

## Footage used (all real, no stock/Pexels — 0% stock)
1. **The White House** — oaWMke0cdLo (bilateral meeting w/ Taoiseach, 2026-09-12): the
   "I built it" quote. Cold-open candidate.
2. **The White House** — en8TnC1qy4w (first-tee gaggle, Doonbeg, 2026-09-13): arrival
   visual + a bonus SOT ("He's having a good time. Great course. Nice hotel.") — Trump
   unprompted-plugging his own resort, good comedic beat after the fact-check.
3. **The White House** — JlRgnCKEu3Q (Shannon departure gaggle, 2026-09-13): tarmac
   visual + closing SOT ("The tournament was record setting. The attendance was number
   one.").
4. **Irish Independent** — h6aUkOiKX4o ("Trump struggles to get golf ball uphill at
   Doonbeg golf course"): two b-roll shots — Trump on a cart in red pullover, and a wide
   ocean-side fairway shot (genuinely right on the Atlantic, which is the one part of his
   claim that's true).
5. **Forbes Breaking News** — hGHQY23qcRE ("President Trump Spotted Watching Irish Open
   In Doonbeg, Ireland", dated on-screen 2026-09-12): clubhouse-balcony b-roll.
6. **The FOREcast Golf** — ViYViQ9SGXQ (Rory McIlroy press conference, Amgen Irish Open):
   presser-room establishing shot + the real McIlroy SOT quoted above. This is the
   quote the assembler's incoming note said it could not find real footage for (it only
   turned up clickbait/reaction channels on its search) — found here on a legitimate golf
   media outlet's own upload of the press conference.
7. **RTÉ News** — sBWqpo1AUeU ("Trump's focus turns to golf in Doonbeg amid protests"):
   live cross from Doonbeg, reporter interviewing two women about the protest against the
   visit — covers the "protests" footage idea from the brief.

Max excerpts from any one source video: 2 (well under the 6 cap).

## Deviation from assembler's incoming note
`incoming_from_assembler/NOTE.md` suggested splitting the Taoiseach-meeting quote into two
separate sub-5s clips ("I've owned it for -- I built it" / "about 22 years right on the
ocean") because the full phrase looked like it might run past 5.0s. Word-level caption
timing showed the full quote "I built it about 22 years, right on the ocean" only spans
~4.9s, so it was kept as a single, more natural SOT instead.

## Technical notes
- `n3_sot_teebox_hotel.mp4` needed a fresh, wider yt-dlp download (local intermediate,
  since deleted) rather than trimming v2's pre-cut 12s teebox clip, because the phrase
  "Nice hotel." runs right up against — and per caption timing possibly just past — the
  boundary of v2's original 00:00:04-00:00:16 cut. Re-downloaded 00:00:10-00:00:18 of
  en8TnC1qy4w and cut from that instead, so the full word is safely inside the clip.
- All clips re-encoded to h264/aac via ffmpeg; audio kept on every clip including visuals,
  per spec (assembler/renderer can duck it under narration).
- No manual downloads needed; yt-dlp was not blocked at any point this session.

## Swap
Not used — n3_doonbeg had ample real footage (4 usable SOTs across 5 outlets), no swap to
another story was necessary.
