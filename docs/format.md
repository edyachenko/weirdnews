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
Biden end gag (brand/biden_end.mp4, identical every episode)
outro narration + subscribe line
```

Transitions are the user's own clips `brand/ymca_1..4.mp4`, randomly assigned with no clip twice in a row, and used whole with
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
