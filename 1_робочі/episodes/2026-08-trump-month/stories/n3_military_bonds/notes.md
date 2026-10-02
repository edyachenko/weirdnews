# n3_military_bonds -- notes

## Fact check
- Exact quotes verified against the official CNN NewsNight rush transcript
  (transcripts.cnn.com/show/cnap/date/2026-08-21/segment/01), which matches the Mediaite/Raw
  Story reporting word for word:
  - REPORTER: "Did you direct Secretary Bessent to intervene in the bond market? Was that your idea?"
  - TRUMP: "No, not at all. No, he's a very capable man... and he did that, yes."
  - REPORTER: "The yields have come back up since then. Have you talked to him about another
    type of intervention? Is that something he will be doing?"
  - TRUMP: "We have many types of intervention. That's one. The ultimate intervention is our
    military, and if we have to use that, we will."
  - PHILLIP (on air): "Not sure what that's about... He's going to sic the military on the bond
    market. What is he talking about??"
- Source footage (Forbes Breaking News, L1807w6hybE) is dated on-screen AUGUST 21 2026 and
  matches the transcript's air date -- same real event (Trump at the tarmac before boarding
  Air Force One), not a different-day mismatch.
- Clip timestamps were located by transcribing the downloaded audio locally (YouTube
  auto-subs were HTTP 429-blocked all session -- shared IP across agents), then cross-checked
  word-for-word against the official CNN transcript for exact wording. Cut points use the
  transcribed timing; exact word boundaries could be off by a few hundred ms since no silence
  gaps were detectable in the audio (airport/engine noise).

## Reaction beat -- judgement call (read this)
The brief named a specific lead: CNN NewsNight's Abby Phillip reacting on air with "What is
he talking about??" I could NOT find downloadable video of that reaction after a real search:
- yt-dlp ytsearch for "CNN NewsNight Abby Phillip bond market/military" (several phrasings)
- yt-dlp ytsearch for the exact quote
- WebSearch for the clip on YouTube
- Browsed CNN's official YouTube channel's recent uploads for a match
- Checked cnn.com/videos/title-2444792 directly with yt-dlp (not extractable)
- Confirmed the exact exchange via CNN's own transcript site (text only, no video embed)

CNN appears not to have put this specific segment on YouTube as a standalone clip, and it
wasn't in a plain re-upload I could find within budget. Per the format bible's reaction-beats
section, a real search that comes up empty is an acceptable outcome -- I did not fabricate or
reuse a lookalike clip, and I did not use a text card.

**What I did instead (fallback #3 in the format bible: "a real contrasting archival clip...
shown as a silent cutaway"):**
- After "The ultimate intervention is our military" -> real Pexels stock of soldiers (not
  Pentagon-specific, but genuinely real military footage, not generated) as a deadpan,
  undersold cutaway.
- After "if we have to use that, we will" -> real Pexels stock of the actual New York Stock
  Exchange building (clearly legible signage) as the "bond market" punch, paired with the
  Abby Phillip quote in narration (attributed, sourced, not shown as video).
- Abby Phillip's real quote is still used -- just narrated/attributed rather than shown as
  unobtainable video, which keeps the facts honest without inventing footage.

This keeps the ≥2 reaction/punch insert requirement met with real (if generic) footage rather
than skipping it, but flagging for your review: these two are stock cutaways, not an in-frame
reaction to this specific event, which is a weaker version of the brief's intent. If you later
find the actual CNN clip, swap it in for one or both inserts.

Stock share: ~5.0s of cutaways out of ~47s total runtime (~10.6%) -- at the edge of the ≤10%
guideline, both used as deliberate contrast cutaways, never while Trump's specific claim is
being shown (they land right after each SOT, not during).

## Budget used
- yt-dlp ytsearch calls: 5 (Forbes search: 1 hit; Abby Phillip reaction: 3 variants, no hit;
  Bloomberg/CNN search: 1, found the Bloomberg Q&A upload named in the brief, unused in the
  final cut since the Forbes clip alone covered all needed SOTs).
- WebSearch calls: 2 (locating the Abby Phillip clip; did not find a YouTube video, did find
  the CNN transcript page used for fact-checking).
- Downloaded and used only the Forbes Breaking News clip (full 57s, since yt-dlp
  --download-sections kept hitting 429s and the full clip was small anyway) plus two short
  Pexels stock clips. Bloomberg's 541s Q&A video and the CNN official channel were checked for
  subs/listings but never downloaded in full.

## Housekeeping
- Deleted tmp/ (full downloads, frames, subs) after cutting final clips -- story folder is
  clips.json + beats.json + notes.md + clips/ only.
