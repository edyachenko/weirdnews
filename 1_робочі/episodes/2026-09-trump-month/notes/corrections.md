# v2 fact-check corrections (2026-09-14)

1. **#2 coin**: v1 said "the old, unwritten rule about not putting living presidents on
   American currency." This was wrong on two counts: it's not unwritten (31 U.S.C. 5114(b)
   requires currency portraits to be of deceased people; the Presidential $1 Coin Act of 2005
   separately bars living presidents from that coin series), and the coin isn't simply
   breaking a norm -- the Mint is using a specific drafting gap in the Circulating Collectible
   Coin Redesign Act of 2020: it bans living portraits on the REVERSE of the 250th-anniversary
   coins but never repeats the ban for the OBVERSE, where Trump's portrait actually is.
   Reworded script + research.json to describe the loophole accurately, added
   news.meaww.com's "legal loophole" explainer and TIME as sources.

2. **#4 and #6 (CNN)**: opened both CNN fact-check pages (night-1 and night-2 of the
   convention) and the CNN trade/Fed piece directly with the Playwright browser (WebFetch
   returns HTTP 451 for cnn.com). All three script quotes -- "no empty seats" (night-2),
   "almost every item"/"every single promise" (night-1), and the trade-for-rate-cuts threat
   (Trump's Truth Social post, quoted directly in the CNN piece) -- are confirmed verbatim in
   the live article text. No changes needed to the underlying claims; added the exact Truth
   Social quote to research.json/script for #6 since it reads better than the paraphrase.

3. **#5 Carlson**: was sourced only to Wikipedia + two blogs. Added
   washingtontimes.com's Sep 3, 2026 report on JD Vance's comments (a mainstream outlet,
   with Vance quoted directly: "Tucker is a friend ... I'm not going to play the game where
   I throw friends under the bus"). The Sep 9 Carlson quote itself is confirmed via Carlson's
   own X post of the line, which matches every secondary source found (no mainstream US
   outlet's dedicated article on that specific Sep 9 livestream was found in search, despite
   multiple queries -- Newsweek/Mediaite/Axios pieces found were about earlier Carlson
   interviews, not this video).
