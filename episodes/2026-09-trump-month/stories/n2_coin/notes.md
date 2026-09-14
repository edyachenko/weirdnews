# n2_coin — notes

## Story kept as-is (no swap needed)
Good real footage was available: a New York Post B-roll piece showing the actual
US Mint minting/stamping process plus the official Mint 3D renders of both coin
faces, and a WION "Fineprint" broadcast segment (real anchor, on-camera, real
audio) that covers the coin's price, the "no real gold" gag, and the exact legal
loophole (2020 law bans living portraits on the REVERSE of the 250th-anniversary
coins but never repeats that ban for the OBVERSE, where Trump's portrait is).

## Facts used, per corrections.md
Followed the v2 correction: did NOT describe this as an "unwritten norm" being
broken. Narration states it accurately — 31 U.S.C. 5114(b)/Presidential $1 Coin
Act of 2005 restrict living portraits generally and on that coin series, and the
Mint relies on the Circulating Collectible Coin Redesign Act of 2020's gap
(reverse ban only, no obverse ban). WION's own reporting independently confirms
the same reading almost word-for-word ("Treasury officials stated it did not
explicitly forbid a living person's portrait on the obverse despite prohibiting
it on the reverse" — seen in a sister WION cut, https://www.youtube.com/watch?v=3VnG0O30KTw,
not used directly but cross-checked against).

## Catherine Rampell joke
No broadcast video of Rampell delivering the "birth as 1776, death as 2026" line
was found, so it is delivered as narration with clear attribution ("Columnist
Catherine Rampell joked...") rather than as a false SOT. Matches research.json's
quote field exactly in substance.

## Footage sourcing decisions
- Used: New York Post (2.56M subs) — https://www.youtube.com/watch?v=MlPS540U6WY
  (real B-roll of the minting press + official US Mint 3D coin renders; no
  narration/dialogue in this cut, used as "visual" kind).
- Used: WION (10.5M subs) — https://www.youtube.com/watch?v=BQzoMasQkdw
  ("Fineprint" segment, real anchor on camera, real broadcast audio, matches
  auto-captions verbatim; used for all 4 "sot" clips).
- Rejected: a "Forbes Breaking News" clip (72dhj130Rwc) that surfaced in search
  with a coin-related title — no captions were available, and a local Whisper
  transcription of its audio track came back as music/silence with no coherent
  speech about the coin, so it could not be verified as on-topic. Dropped
  rather than risk misattributing a quote.
- Avoided: a "News of the World" YouTube channel (zvzvvmBGW10) with excellent,
  detailed narration text — but only ~5,900 subscribers and a name reused from
  a defunct UK tabloid, which reads as a possible low-effort/AI news-aggregator
  channel rather than a real outlet per SPEC's "skip ... AI channels" rule.
  Its factual content was accurate (cross-checked against WION and
  research.json) but not used as a source video.
- Did not use the official USMINT YouTube video (KGIj4jO5GIo) — same coin
  renders already covered by the NY Post cut, and its upload date (20251211)
  falls outside the Aug 14–Sep 16 2026 window.
- v2's `assets/n2_coin/coin_obverse.jpg` and `coin_reverse.jpg` were corrupted
  (HTML error pages, not real images) — not usable, not needed since the NY
  Post video already contains clean high-res renders of both faces.

## Numbers
8 clips total: 4 visual (New York Post, no dialogue, kept audio per spec) + 4
sot (WION, real anchor voice). All ≤5.0s. Max clips from one source video: 4
(WION) — under the 6-clip cap. Estimated story runtime ≈55s, SOT ≈26% of
runtime (4 SOT beats spanning the requirement of ≥3).

## incoming_from_assembler
Checked `stories/n2_coin/incoming_from_assembler/` — empty, nothing to
incorporate.
