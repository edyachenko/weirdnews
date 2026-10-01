# Weird News USA: episode format bible

What a finished episode must look like. Every rule here was paid for by a rejected version, see
`docs/retrospective-2026-09-14.md`.

## Shape (≈5–6.5 min, 1920x1080, 30 fps, English)

```
cold open: best 3 real SOT moments back to back (each ≤5 s)
title plate (with motion)
host intro (≤15 s)
YMCA transition
#6 story   → YMCA → #5 → YMCA → #4 → YMCA → #3 → YMCA → #2 → YMCA → #1
YMCA transition
Biden end gag (2_пайплайн/brand/biden_end.mp4, identical every episode)
outro narration + subscribe line
```

Transitions are the user's own clips `2_пайплайн/brand/ymca_1..4.mp4`, randomly assigned with no clip twice in a row, and used whole with
their own audio. Never cut or source transition clips yourself.

## One story (≈45–55 s)

- Alternate `narr` (host voice over **real muted footage of the event**) and `sot` (real clip with original audio).
- **≥3 SOTs per story.** SOT = 25–40% of story runtime. Across the episode SOT should be ≥25% and real footage ≥85% (target 100%).
- **Every excerpt ≤5.0 s.** Max 6 excerpts from one source video. This rule is not up for discussion.
- Host never talks longer than ~15 s (≤35 words per narr beat). Shots under narration change every 2–4 s.
- No frozen frames. When a narr beat runs out of footage, cycle other clips from the same story (muted SOTs too),
  then fall back to a slow zoom on moving footage.
- Stock (Pexels) is a last resort, ≤10%, and never shown while a specific named person is discussed.
- Lower-third plate "#N + headline" for the first ~3.5 s of the story. Persistent "WEIRD NEWS USA" bug top-right.
- SOT captions show the exact spoken words, placed away from the source's own banner, with the label "via <Outlet>".
  Never hide or crop outlet logos, and never mirror or pitch-shift clips.

## Reaction beats (punch inserts) — default, not optional

Every story needs **at least two** short (2-4 s) real reaction/punch inserts, spread across the story — not just one
token beat after the single strongest SOT. This is what turns "he said X, that's dumb" into an actual string of jokes
instead of a dry news recap with one comedic beat bolted on. Added 2026-09-21, revised same day after the user
watched a rough cut with one insert per story and said it wasn't enough: "казав що б вставляти під кожне відео і не
одну реакцію вставку" — under every real moment that can carry one, not one per story as a checkbox.

In practice: look at every SOT in the story, not just the marked `cold_open_candidate`. Any SOT that lands a real
punch deserves its own reaction beat right after it if a proportionate, real one exists. A 45-55s story with 3-4 SOTs
should end up with 2-3 reaction inserts, not 1. It is fine for a story to end up with fewer only after a real search
for each SOT came up empty — "we looked and found nothing real and proportionate" is an acceptable outcome for an
individual beat, but skipping the search because one insert already went in is not.

**Method — search before you scan.** Added 2026-09-21 after burning a lot of agent budget frame-scanning raw
source footage for reactions that mostly weren't there. Do this in order, and stop at the first hit:
1. **Search first, download nothing yet.** `yt-dlp "ytsearch15:<event/quote keywords> reaction"`, and separately
   `ytsearch15:<event/quote keywords> SNL` / `... Daily Show` / `... meme` / `... shorts`. Known viral moments almost
   always already have a named satire show's segment or a widely-clipped reaction upload — Shorts included, they're
   fine as a *source to find*, you still trim from the original full segment, not the Shorts re-edit. This is one
   search call, cheap, and finds most of what you need.
2. Only if that turns up nothing: re-check the footage your story already downloaded for an in-frame reaction
   (a face, a groan) you didn't use — free, no new download, but don't go frame-hunting a video that doesn't have
   people in frame to react (check the shot type first).
3. Only if both of those come up empty: consider a contrasting archival clip (the autopen story's real Biden-signing
   footage is the template).
Do **not** re-download and manually frame-scan a full source video hoping a reaction is hiding in it — that's the
expensive path and it's usually a dead end. If step 1's search finds nothing in a couple of query variations, it's a
real "nothing exists" outcome, not a signal to dig harder by hand.

**Sources, in order of preference (all still real footage, nothing generated):**
1. A named satire/comedy show's own real segment reacting to the *same* event (SNL Weekend Update, Daily Show, a
   late-night monologue) — the search in the Method above usually finds this fastest. This is the one exception to
   "skip reaction channels" above: a named show's own upload of its own segment is a real primary source, not a
   reaction-channel clip of someone else's footage.
2. A reaction already sitting in the same source clip — a crowd groan/laugh, a reporter's face, someone on stage
   rolling their eyes. Free if it's there, but check the shot type before spending time scanning for it.
3. A real contrasting archival clip (the autopen story's real Biden-signing footage is the template) shown as a silent
   3-4 s cutaway right after the claim.

**Calibration — this is the part that goes wrong if rushed:** the insert's energy must match how absurd the actual
moment was, not how absurd the editor wishes it were. A flat, minor gaffe gets a small reaction (a raised eyebrow,
one dry aside) or none at all. Bolting a huge "everyone's losing it" meme reaction onto a mid joke doesn't read as
funnier, it reads as the video lying to the viewer about how funny its own content is — and the viewer notices and
resents being played. When in doubt, undersell.

## Writing

- Tone: sharp late-night-host sarcasm. Trump is the clown; calling him a dumbass is fine **as opinion**; swearing OK.
- The real clip is the joke. The host sets it up in one line and lands a one-line punch **right after** the SOT.
- Facts are attributed ("according to CNN…"), opinions read as opinions, no medical diagnoses, no invented quotes.
  Every factual claim has a source URL in the story's `beats.json`.
- Written for TTS: numbers spelled the way they're spoken, no emojis or stage directions.

## Voice

Edge TTS `en-US-BrianMultilingualNeural`, rate `-8%`, pitch `-2Hz`.

## Sources of footage

Any real outlet or official channel on YouTube (White House, C-SPAN, CNN, NBC, Fox, ABC, CBS, PBS, MS NOW, Forbes Breaking News,
local TV, the person's own channel). Uploads must come from the episode's period. Skip reaction, compilation and AI channels.

## Never

- Full-screen text cards as visuals.
- Music from `MoneyPrinterTurbo/resource/songs`.
- Printing or quoting song lyrics anywhere: it triggers the output filter and kills the agent.
- Publishing anything without the user's explicit approval.
