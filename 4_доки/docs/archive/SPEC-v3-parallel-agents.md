# trump_month_v3: shared spec for parallel agents

Video: "Trump's Month: The Greatest Hits" (Aug 14 – Sep 14, 2026), English, 5–6 min, sarcastic
late-night-host commentary over REAL footage. The user rejected v1 (text cards) and v2 (66% stock).

Facts and sources: `~/pet-projects/weirdnews/trump_month/research.json`, `trump_month/script/script.md`
(corrections: `trump_month_v2/notes/corrections.md`). Old v2 script split into setup/commentary:
`trump_month_v2/script/`. v2 already-cut White House clips: `trump_month_v2/work/clips_raw/`.

## Roles
- **Story agents** (one per story, in parallel) find and cut footage and write the beat sheet for ONE story.
- **Assembler agent** writes the pipeline code (TTS, render, verify), builds the intro and outro from the stories'
  cold-open candidates, waits for all `DONE` markers, then renders the final video.

## Story ids
| id | story |
|---|---|
| n6_fed | Trump threatens to halt trade unless the Fed cuts rates (Sep 4) |
| n5_carlson | Trump–Tucker Carlson feud, Vance won't disavow (Sep 3–9) |
| n4_convention | GOP midterm convention in Dallas: "no empty seats", "almost every item", "every single promise" (Sep 9–10) |
| n3_doonbeg | Doonbeg / Irish Open: "I built it about 22 years ago" (Sep 12–13) |
| n2_coin | US Mint $1 Trump coin "1776–2026", living-portrait loophole (Sep 2) |
| n1_pentagon | Pentagon 9/11 speech: pause, "twenty-O-one", "very famous date, unfortunately" (Sep 11) |

A story agent MAY replace its story with another verified story from the window if its own has no usable
video. It needs ≥2 sources, must keep the same id folder, and must note the swap in `notes.md`.

## Output of a story agent: `~/pet-projects/weirdnews/trump_month_v3/stories/<id>/`
- `clips/<clip_id>.mp4`: trimmed excerpt, **duration ≤ 5.0 s**, h264 + aac (keep audio even for visuals),
  source resolution OK (the renderer normalizes).
- `clips.json`: list of objects:
  ```json
  {"id": "n1_sot_2001", "file": "clips/n1_sot_2001.mp4", "kind": "sot|visual|stock",
   "source_url": "https://www.youtube.com/watch?v=...", "channel": "The White House", "title": "...",
   "upload_date": "20260911", "in": "01:11:55.2", "out": "01:11:59.9", "duration": 4.7,
   "transcript": "exact words spoken (sot only)", "shows": "what is on screen",
   "banner": "none|bottom|top", "cold_open_candidate": false}
  ```
- `beats.json`:
  ```json
  {"id": "n1_pentagon", "number": 1, "headline": "short lower-third headline (≤40 chars)",
   "sources": [{"outlet": "...", "url": "..."}],
   "beats": [
     {"type": "narr", "text": "≤35 words (≈15 s of speech)", "visuals": ["clip ids, kind visual/stock, 2–4 s each on screen"]},
     {"type": "sot", "clip": "clip id", "caption": "exact spoken words", "label": "via <Outlet>"}
   ]}
  ```
  The first beat is `narr` (the story open). Alternate narr/sot. Provide enough visuals per narr beat to cover its speech at
  2–4 s per shot (≈ words/2.3 = seconds). A visual clip may be reused once within a story.
- `notes.md`: fact checks, swaps, problems.
- `MANUAL_DOWNLOADS.md`: only if YouTube blocked you. List URL + exact time ranges still needed.
- `DONE`: empty file, created LAST, when everything above is final.

## Hard requirements per story (~45–55 s of runtime)
- **≥3 SOT beats** (real voices: Trump, reporters, anchors, crowd). SOT ≈ 25–40% of the story runtime.
- **Every excerpt ≤ 5.0 s.** Max 6 excerpts from any single source video.
- Real footage of the actual event under narration. Stock (Pexels) ≤10% of the story runtime and never
  shown while a specific named person is being discussed.
- No narr beat longer than ~35 words.
- Facts attributed to sources; opinions clearly opinions; no medical diagnoses. Jokes land right after SOTs.
- Mark 1 funniest SOT as `cold_open_candidate: true`.

## Footage method (yt-dlp + ffmpeg installed)
- Search: `yt-dlp "ytsearch10:<query>" --flat-playlist --print "%(id)s|%(channel)s|%(title)s|%(duration)s|%(upload_date)s"`.
  Keep real outlets and official channels with uploads between 20260814 and 20260916. Skip reaction, compilation and AI channels.
- Locate moments: `yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt -o "<dir>/%(id)s" <url>`, grep phrases.
- Download only sections: `yt-dlp --download-sections "*START-END" -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 --force-keyframes-at-cuts <url>`,
  then trim precisely with ffmpeg to ≤5.0 s. Look at a frame of each clip to fill `shows` and `banner`.
- Politeness (several agents share one IP): run **one yt-dlp process at a time** and add `--sleep-requests 1 --sleep-interval 2`.
- If blocked (403 / "Sign in to confirm you're not a bot"): retry once with `--extractor-args "youtube:player_client=web_safari"`.
  If still blocked, write `MANUAL_DOWNLOADS.md`, finish with what you have, and create `DONE`.
- Pexels key: `~/pet-projects/weirdnews/MoneyPrinterTurbo/config.toml` (`pexels_api_keys`). Never print it.
- Python with Pillow and edge-tts: `uv run --project ~/pet-projects/weirdnews/MoneyPrinterTurbo python ...`.
- Do NOT hide or crop outlet logos, and do NOT mirror or pitch-shift clips.

## Rules for everyone
- This task was explicitly requested by the user.
- The session cwd being `~/pet-projects/streamstation` is incidental: never touch that repo.
- Don't ask for confirmation.
- No git commits, no uploads, no accounts.
- Delete full-length downloads and intermediates.
- Keep each story folder under 500 MB.
- Use blocking waits; don't end your turn while work runs.
