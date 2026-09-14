# n5_carlson — notes

## Story kept as-is (no swap needed)
Plenty of usable real footage was found for both halves of the story. No swap to another
story from `research.json` was necessary.

## Sourcing
- **Tucker Carlson's Sep 9 video** — found on his own official YouTube channel
  ("Tucker Carlson"), titled "Trump Betrayed His Voters on Behalf of a Foreign Country.
  This Is Why Republicans Will Get Crushed." (uploaded 2026-09-10, streamed 2026-09-09,
  https://www.youtube.com/watch?v=mEPMm6ZZOe8). This is the exact video research.json's
  `carlson_feud` entry cites for the "Republicans are going to lose" line. The video is
  a ~68-minute monologue; I pulled auto-subs and located two usable moments:
  - ~00:00:11.5 "Republicans are definitely going to lose the House of Representatives."
    (cold-open candidate — deadpan, definitive, funny out of context)
  - ~00:36:07.4 "...because he followed not their wishes but the wishes of a foreign
    government." (the "chose a foreign country over his own voters" claim, in his own words)
  I did not find the exact string from the X-post quote in research.json spoken verbatim
  in the video audio (research.json itself notes it was confirmed via Carlson's own X post,
  not a mainstream outlet's article on this specific livestream) — the two spoken lines
  above carry the same substantive claim and are directly attributable to Carlson on camera.

- **JD Vance's Sep 3 press-briefing remarks** — sourced from two outlets covering the same
  White House briefing-room exchange:
  - USA TODAY (https://www.youtube.com/watch?v=eK4KoZXlbYM, uploaded 2026-09-03): reporter
    Kerry Pickett's on-camera question ("Mr. Vice President, Tucker Carlson has called for
    the president's impeachment...") and Vance's "I'm not going to play the game where I
    throw friends under the bus" line.
  - PBS NewsHour (https://www.youtube.com/watch?v=pQeOq9Pta7c, uploaded 2026-09-03): used
    for the "Tucker is a friend of mine... despite the fact that we disagree" line. This
    clip was pre-fetched by the assembler and left in `incoming_from_assembler/` — I
    independently found and verified the same USA TODAY exchange myself before checking
    that folder, and it also flagged the PBS angle as a way to diversify sourcing beyond
    a single outlet, so I used it for one of the three Vance/reporter SOTs. This gives the
    story 3 distinct real-world channels (Tucker Carlson's own channel, USA TODAY, PBS
    NewsHour) instead of 2.
  - I did not end up using the assembler's suggested `carlson_lose_house.mp4` /
    `carlson_betrayed.mp4` pre-cut files directly (their in/out points were close to but
    not identical to what I'd already cut from a fresh download by the time I checked the
    folder) — their timestamps closely corroborate mine, which was a useful independent
    check. Research note: Washington Times (cited in research.json for the Vance quote)
    was not used as a video source since I could not find a YouTube upload of its own
    footage of the briefing; its reporting is credited in `beats.json.sources` instead.

## Facts / attribution
- Carlson's claim that Trump "betrayed his voters" / followed "the wishes of a foreign
  government" is Carlson's own opinion/framing, presented as his on-camera quote — not
  asserted as fact by the narrator.
- Vance's quotes are presented as his own on-camera words, correctly attributed via the
  `label` field on each SOT beat.

## Numbers
- 5 SOT beats (3.07s + 3.77s + 3.87s + 4.9s + 3.67s = 19.28s of SOT)
- Estimated total runtime: ~52.8s (narration ~33.5s @ words/2.3 + SOT ~19.3s)
- SOT ≈ 36.5% of runtime
- 0% stock/Pexels footage used — real footage covered every beat, no stock needed
- Max excerpts from one source video: 5 (mEPMm6ZZOe8 and eK4KoZXlbYM), both under the 6 cap
- 1 clip marked `cold_open_candidate: true`: `n5_sot_carlson_house`

## Problems
None blocking. No manual downloads needed — yt-dlp worked cleanly on all three source
videos, no bot-check triggered.
