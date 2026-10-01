# n3_pope_funeral_nap — notes

## CRITICAL fact-check framing (read before touching this story)

Per **Snopes** (cited in episode.json), it is **not confirmed** that Trump was actually asleep at
Pope Francis's funeral. Low-resolution livestream screenshots and harsh shadows make it impossible
to distinguish "asleep" from "bowing his head in prayer / squinting in the sun." This is a real,
documented ambiguity, not a minor caveat.

**Every beat in `beats.json` is written to preserve this ambiguity.** The narration never states
as fact that he was asleep. It always frames the claim as: "a photo went viral, and the internet
decided ...", "the internet ran with it", "that didn't slow the pile-on" — i.e. an attributed
internet/social reaction, not the narrator's own conclusion. The Kimmel line ("either went deep in
prayer or deep asleep, I don't know") is used specifically because Kimmel's own joke *keeps the
ambiguity open* rather than asserting the nap as fact — it's a real quote that does the
attribution work for us.

**If anyone edits this story's narration later: do not change "the internet decided he napped" to
"he fell asleep" or similar as fact.** That would break the one thing this note exists to protect.

## Why no raw Vatican broadcast footage was used

Initial approach was to scrub the ~2-hour Vatican News full Mass broadcast for the live moment.
After burning real time downloading and frame-sampling two ~30-40 minute windows (procession /
entrance rites and the homily) without finding a clean, identifiable front-row shot of Trump with
eyes closed, the coordinator correctly redirected: this moment is famous enough that pre-cut news
segments already exist showing exactly this shot as B-roll. Applying format.md's "search before
scan" method (already mandated for reaction inserts) to the *core* visual too immediately turned up
what was needed in a **Times Now** segment and an **ETimes** segment, both real broadcasters'
own uploads from the days right after the funeral (April 27–28, 2025). All raw Vatican
broadcast downloads (~280MB across two chunks) and intermediate frames were deleted; nothing from
that scrub is in the final story.

## Source notes per clip

- `n3_visual_photo_wide` / `n3_visual_photo_closeup`: Times Now's own segment
  ("'Sleeping' Trump In Blue Suit Breaks Vatican Protocol...") shows two different real viral
  social-media screenshots of the same photo (one a side-by-side photo comparison, one a tighter
  single crop) as B-roll while reporting on the backlash. **The tweet authors' names/handles/avatars
  were cropped out of frame** in both clips before trimming — these were ordinary private
  individuals' posts, and there was no editorial reason to identify them; only the newsworthy photo
  itself and the outlet's own on-screen chyron remain visible.
- `n3_visual_standing_ceremony`: same Times Now segment, but this portion is real funeral pool
  video (not a screenshot) — Trump standing upright and attentive among other world leaders
  (Macron visible beside him) with the coffin in frame. Used as the "wide awake minutes later"
  contrast beat.
- `n3_visual_gum_phone`: ETimes segment, explicitly credited on-screen "SOURCE: US NETWORK POOL/AP,
  VATICAN, APRIL 26, 2025" — real, dated pool footage of Trump chewing gum in his seat, Melania
  beside him. This corroborates the gum-chewing detail from The Tab/NewsX without relying on a
  screenshot.
- `n3_reaction_kimmel_prayer_or_asleep`: found via format.md's reaction-beat search method
  (`ytsearch` variants for "reaction"/"SNL"/"daily show"/"meme" on this exact story). No SNL or
  Daily Show segment specifically on this moment turned up in a few query variations. Jimmy
  Kimmel's own real monologue segment about the funeral (uploaded April 29, 2025, the same week)
  did have a direct, on-point joke about it, located via auto-caption grep for "asleep" —
  "the president either went deep in prayer or deep asleep, I don't know." Used per format.md's
  "named show's own real segment" preference (source #1 in the Sources list).
- No second/third reaction insert was found beyond the Kimmel line after a few search variations
  (`SNL`, `daily show`, `colbert`, `meme`, `shorts`) came up empty for this specific moment (as
  opposed to the broader "blue suit" controversy, which had unrelated hits). Per format.md, "we
  looked and found nothing real and proportionate" for a second insert is an acceptable outcome.

## Kind classification

Per the task brief, the four Vatican-footage clips are marked `kind: "visual"` rather than `"sot"`
since Trump never speaks in any of them — `transcript` is `"(no dialogue, silent visual...)"` for
all four, honestly noting when ambient outdoor/liturgical sound is present versus true silence.
Only the Kimmel clip is `kind: "sot"`, since that's an actual spoken quote.

## Cold open candidate

`n3_visual_photo_wide` is marked `cold_open_candidate: true` — it's the clearest, most immediately
legible version of the eyes-closed photo (side-by-side comparison, unambiguous even at a glance),
and needs zero context to land as a cold open.

## Cleanup

- Deleted: both raw Vatican News broadcast download chunks (~280MB total), all extracted frame
  batches and contact sheets, the AP Archive "world leaders greet" clip (checked, not used), and
  full downloads of the Times Now and ETimes source videos after trimming.
- Final story folder contains only 5 clips (all ≤5.0s) plus this notes file, clips.json,
  beats.json, and DONE — well under the 500MB budget (clips total well under 2MB).
- The old `stories/n3_ymca_dance/` folder was not touched.
