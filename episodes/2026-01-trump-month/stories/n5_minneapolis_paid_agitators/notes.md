# Notes — n5_minneapolis_paid_agitators

## Fact checks / judgement calls

- All three SOTs come from the same Fox News upload (`3bAzIFO0Xjs`, published 2026-01-20),
  which is Fox's own edited package of Trump's Jan-20 White House anniversary briefing. The
  three quotes are pulled from different points in that same 12-minute package (~01:54, ~07:15,
  ~08:00), so the story leans on one press event rather than multiple. This is the same briefing
  referenced by story n2 (anniversary_presser) — different excerpts, no overlapping clip ids or
  timecodes, so no double-booking.
- Dropped a candidate source: video `YoeeizyNP9k`, listed by yt-dlp under channel "News24," is
  actually a re-upload of a **Sky News Australia** graphics package (on-screen bug reads
  "sky news .com.au / First Edition"). Since the channel metadata doesn't match the outlet
  actually shown on screen, it reads as a mirror/aggregator upload rather than a real outlet's
  own channel — skipped per the "skip reaction/compilation channels" rule, and to avoid a
  wrong "via News24" attribution.
- The Jan 18 Truth Social quote ("highly paid professional agitators and anarchists") in
  episode.json/research.json is a text post, not something Trump says on camera — no matching
  spoken SOT was found, so the story uses only the two verified spoken variants ("paid agitators
  and insurrectionists" / "professional agitators") from the Jan 20 presser instead. Facts text
  should not be treated as a direct quote in a SOT caption anywhere else.
- `n5_v_cold1` / `n5_v_cold2` (KARE 11, "Why protestors braved the bitter cold...") carry a small
  "AP IMAGES" watermark top-right — that's wire footage KARE 11 itself used in its package, not
  something introduced here. Left uncropped per the never-hide-logos rule.
- Upload dates: Fox News clip and both KARE 11 clips are Jan 20/23/24 2026 — all in or right
  after the episode window, per the "a few days after is fine" allowance for `oYoZ_zF1mh4`
  (Jan 24, i.e. one day after the Jan 23 day-of-action it covers).
- No reporter/anchor SOT was used (all three SOTs are Trump) — no clean, correctly-attributed
  anchor/reporter clip on this topic turned up that wasn't the rejected Sky News mirror upload.
