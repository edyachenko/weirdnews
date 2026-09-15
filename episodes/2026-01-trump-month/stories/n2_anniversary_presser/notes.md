# Notes: n2_anniversary_presser

## Sources used
- India Today, `RooB56TkGl0` (21s clip, uploaded 2026-01-21) -- shows the actual thick bound
  "White House / Accomplishments / AS OF JANUARY 20, 2026" book being held up. Video is only
  ~9-10s of real content before its own like/share/subscribe outro card kicks in; only the first
  4.3s (book reveal) was used.
- KARE 11, `YXVuxNoIhME` (5:56 real content, titled with a Jan 20, 2026 date in the title itself,
  no separate upload-date subtitle needed) -- the main footage source for this story. Has no
  YouTube captions (auto or manual), so timestamps were located by downloading a low-res scout
  copy and transcribing locally with `openai-whisper` (base model), then verified by eye against
  extracted frames before downloading the real 1080p sections.

## Fact-check / judgment calls
- The KARE 11 title says "worst of the worst" but that exact phrase is never spoken by Trump in
  the audio -- it's text printed on the physical mugshot card he holds up (see
  `n2_visual_mugshot_reveal`, confirmed by frame inspection: card reads "MINNESOTA WORST OF THE
  WORST" over a booking photo and "FIRST DEGREE CRIMINAL SEXUAL CONDUCT"). Used only as a visual,
  not captioned as a Trump quote, to avoid misattributing text-on-card as spoken word.
  `episode.json`'s footage_ideas also said to grep for "worst of the worst" as if spoken; it isn't
  -- it's a chyron/prop, which the beats.json narration for that section works around by not
  quoting it directly as speech.
- The "book falls / hits his finger" bit: at 00:03:53-00:04:00 in the KARE 11 audio Trump says
  "oh, I'm glad my finger wasn't in. That's so good... that could have done some damage, but you
  know what, I wouldn't have shown the pain" -- this is the "book thrown/dropped" moment referenced
  in the India Today title, caught here on a second angle/outlet. No visual of an actual "throw"
  was found in any of the 4 candidate videos; what's captured is Trump's verbal joke immediately
  after something (binder or page) caught his hand. Captioned only with his exact words, and the
  narration beats avoid claiming a literal on-camera "throw" for this specific clip.
- Did not use the India Today or "10 News" full uploads beyond what's listed; the 10 News
  (`dN_Gp0Qt2DQ`) candidate was not needed once KARE 11 supplied both the book/page quotes and the
  mugshot slideshow visual from a single continuous 6-minute excerpt of the same briefing.
- All 5 SOT clips and both visual clips come from the same Jan 20, 2026 White House briefing
  (real event footage, no stock used). SOT share of total clip runtime is ~37% (20.44s SOT out of
  ~28.2s of usable footage / ~55s estimated story length), within the 25-40% target.
- Funniest SOT marked `cold_open_candidate: true`: `n2_sot_finger_joke1` ("Oh, I'm glad my finger
  wasn't in. That's so good.").

## Cleanup
- Scratch/scout files (low-res scout downloads, whisper transcripts, full-length source videos)
  were kept only in the session scratchpad outside the repo, not in the story folder. Story folder
  is ~19MB (7 clips only), well under the 500MB budget.
