# n5_venezuela_oil — notes

## The central claim and why there's no SOT for it
FACTS specified a Fox News interview on Aug 4, 2026 where Trump said "In Venezuela,
we're making hundreds of billions of dollars (in oil revenue), and so are they."
Despite several targeted searches, no video of that specific interview turned up —
what's findable on YouTube around this story is coverage of the *separate, later*
formal deal announcement (Trump's Truth Social post, dated **Aug 28, 2026**, covered
by Fox News and LiveNOW from Fox on Aug 28–29). The opening narr beat therefore
states the Aug 4 "hundreds of billions" quote as attributed narration (sourced to
PolitiFact's report), not as an on-screen SOT — avoiding the trap of captioning real
footage from a different date as if it were that quote.

## Date/event caveats (read before editing)
- **n5_sot_griff / n5_sot_flynn1 / n5_sot_flynn2** (Fox News, uploaded 2026-08-29):
  cover the Aug 28 Truth Social post announcing the formal deal — "biggest oil deal
  in world history," 65 billion barrels. This is a real, correctly-dated event, but
  it is **not** the Aug 4 interview or its "hundreds of billions" line. Used here to
  show the broader pattern of touting the deal in grand terms, not as direct footage
  of the fact-checked quote.
- **n5_visual_trumppost / n5_visual_whitehouse** (LiveNOW from Fox, 2026-08-28): same
  Aug 28 post/announcement, b-roll only, muted.
- **n5_reaction_oil / n5_reaction_ubers** (The Daily Show, uploaded **2026-01-06**):
  this segment reacts to Maduro's capture and the early Venezuela oil takeover
  months before the August claim/deal. It is a real satire-show reaction to the same
  overall "we grabbed Venezuela's oil" story, not a reaction to the Aug 4 or Aug 28
  claims specifically. Used because the jokes ("I think they did it for the oil")
  land squarely on the same throughline the fact-check beat makes, and no
  Aug-dated satire segment about this specific claim was found. Flagging this so the
  edit doesn't caption/label these as reacting to the August news.

## Method / search budget
- Went straight for the named leads (Fox News + LiveNOW coverage of the deal) per
  the budget instruction — found them on the first two searches.
- 4 general searches used (Fox/LiveNOW interview search, LiveNOW deal search, a
  third targeting the literal Aug 4 interview, a fourth also targeting the Aug 4
  interview — none of the three surfaced that specific interview, but the fourth
  surfaced a USA Today full press-conference video and the SNL "Gas Prices" cold
  open, and 1 dedicated reaction-beat search surfaced the Daily Show segment used
  above). That's within the ~4 general + 1 reaction budget.
- Several candidate videos (6cIm6UvKIZ8, xizBip2lDAA, f9yJINzF7AY, OQQQLjdzzPw,
  6x4naHmsLZk, 3t2dc-73uQg) had no retrievable English auto-captions (PO-token
  blocked on web_safari/ios/tv clients, or genuinely no auto-caption track) even
  after the one retry the skill calls for. Did not keep retrying beyond that —
  worked instead from clips with confirmed real transcripts (7CHGYp-iJeE,
  HDSzUfMZRHE) plus one full low-res download (6cIm6UvKIZ8) used only as muted
  visual b-roll, since its spoken words couldn't be verified.
- Hit intermittent HTTP 429s on subtitle fetches throughout (shared IP with other
  agents' concurrent yt-dlp processes, per the skill's warning) — worked around
  with the `web_safari`/`android`/`tv`/default-client rotation and spacing calls
  out with sleeps, rather than hammering retries.
- No MANUAL_DOWNLOADS.md needed — everything required came from material already
  in hand.

## Other judgment calls
- Treated the two Daily Show reaction clips as `kind: "sot"` in clips.json (they
  have real, transcribable spoken jokes, unlike a silent in-frame reaction), and as
  consecutive `sot`-type beats directly after the SOT they're punching off of, per
  format.md's "insert right after it" instruction — this means beats.json isn't a
  strict narr/sot/narr/sot alternation throughout, it's narr-led with reaction
  `sot` beats doubled up where the joke needs one.
- n5_sot_flynn2 ("it's called Venezuela") marked `cold_open_candidate: true` — it's
  the most quotable, ironic standalone line of the three SOTs.
- Both Fox clips in this story carry the same lower-third style banner
  (`banner: "bottom"`) — keep captions clear of the bottom third.

## Runtime / mix estimate
- 3 primary SOTs (griff, flynn1, flynn2): 4.9 + 4.87 + 4.9 = 14.67s
- 2 reaction inserts: 4.94 + 4.3 = 9.24s
- 3 narr beats: ~10.4s + ~9.1s + ~8.7s ≈ 28.2s
- Total ≈ 52.1s, within the ≈45–55s target.
- Primary-SOT share of runtime ≈ 28%, within the 25–40% requirement.
- Real footage: 100% (no stock used).

## Housekeeping
Deleted full-length downloads and temp files from `tmp/` after cutting clips;
story folder kept well under 500 MB. Never touched any other story's folder, and
never touched `~/pet-projects/streamstation`.
