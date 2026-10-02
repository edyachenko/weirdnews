# n2_reflecting_pool — notes

## Sourcing
- Went straight for the named candidates from the brief. First `ytsearch10` turned up AP,
  CBS News, NBC News, PBS NewsHour, Forbes Breaking News, ABC7, Global News, WPLG — all
  real outlets, uploaded in the episode period (Aug 3–4, 2026).
- Used **AP** (`nhN9HVdrH18`) as the primary SOT source: a single continuous press-pool
  clip of Trump at the Oval Office desk that happens to contain both the "there was
  vandalism" claim and the "choked" / "folded like an umbrella" attack on Pirro in one
  take — no separate July clip needed.
- Used **CBS News** (`MAplg7QIRgU`, "The Takeout with Major Garrett") for: the anchor line
  stating the factual reveal, a reaction aside, and a real broadcast split-screen graphic.
- **NBC News** (`e67ZvGmxuEA`) subs were fetched and read (its "sink or swim" exchange and
  "you're fake news" moment are solid material) but the video itself returned HTTP 403 on
  download, and a retry with `--extractor-args youtube:player_client=web_safari` only
  offered images, no video streams. Per the method, retried once then moved on — CBS's own
  "factual conclusion" anchor line covers the same story beat, so nothing was lost.
- PBS NewsHour had no auto-subs available; not pursued further since AP+CBS already covered
  the story's needs.

## Date caveat
- yt-dlp's `--flat-playlist` printed `upload_date: NA` for all results (common for very
  recent uploads). Both AP and CBS videos are unambiguously about the Aug 3, 2026 charge
  drop and Trump's same/next-day on-camera rebuke of Pirro (confirmed by on-screen CBS
  lower-thirds: "TRUMP BLASTS PIRRO..." / "DOJ BLAMES REFLECTING POOL DAMAGE ON 'BOTCHED
  INSTALLATION'"). `clips.json` records `20260803` (AP) / `20260804` (CBS) as best-estimate
  event dates, not confirmed upload metadata — flagging in case precise upload dates matter
  downstream.

## No dedicated pool b-roll
- Despite checking the AP press-pool clip and the CBS package's opening ~26s, neither
  contains actual footage of the physical Reflecting Pool (peeling liner, green water) —
  CBS's "The Takeout" is a studio interview show, not a field package with on-location
  shots. Per format.md's "no frozen frames" rule, the opening beat reuses muted Trump-at-desk
  footage as b-roll instead of matching pool visuals. If a field package with real pool
  shots turns up later, swap it into beat 1's visuals.

## Reaction beats (2, per format.md)
- Search step: one combined query (`ytsearch15:folded like an umbrella Trump reaction`,
  plus an earlier variant that returned zero results — both counted toward the capped
  budget). No named satire show (SNL/Daily Show/etc.) had covered this specific story;
  two unrelated hits ("Trump can't use an umbrella!", a Navbharat clip about a literal
  umbrella mishap) were skipped as off-topic.
- **Insert 1** (`n2_sot_jobsecurity`): CBS anchor Major Garrett's own in-broadcast dry aside,
  "Sounds like real job security for Jeanine Pirro," delivered right after Trump's
  soundbite plays on air — a real, already-sourced reaction (format.md's preference #2),
  calibrated small/dry to match a mid-size gaffe. Placed directly after the umbrella SOT
  as its own `sot` beat (not separated by a narr line) — this is a deliberate read of
  format.md's explicit instruction to land the reaction "right after" the SOT it reacts to,
  taking precedence over the general narr/sot alternation shape for this one placement.
- **Insert 2** (`n2_visual_graphic`): CBS's own real split-screen broadcast graphic
  (Trump photo / Pirro photo, lower-third "DOJ BLAMES REFLECTING POOL DAMAGE ON 'BOTCHED
  INSTALLATION'") used as a silent cutaway — format.md's preference #3 (contrasting real
  archival/graphic material), reused once as a cutaway right after the "factual conclusion"
  SOT and again as a cycled visual later.

## Judgment calls
- `n2_sot_choked`'s caption starts mid-sentence ("unfriendly to Janine...") because the
  clean sentence start ("the judge was extremely") would have pushed the excerpt over 5.0s;
  trimmed to stay under the hard limit while keeping the core "I think she choked" line.
- Max 6 excerpts/source respected: AP used 4 times (vandalism, choked, umbrella, oval
  muted visual), CBS used 3 times (factual-conclusion, job-security, graphic).
