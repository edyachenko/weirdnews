# weirdnews: Weird News USA

Repo location: `/Volumes/Extreme SSD/ютуб/політики/weirdnews` (exFAT SSD). Git uses `core.fileMode false`, and `._*` files are ignored.

Automated English news-commentary YouTube episodes built from **real footage**: short excerpts of news and
official videos, a sarcastic TTS host, and the channel's own brand transitions. The first episode ("Trump's Month",
Aug 14 – Sep 14 2026) was built on 2026-09-14. The plan is a series where each video covers one month of Trump's 2nd term.

- Format bible (read before making anything): `4_доки/docs/format.md`
- SEO packages (titles/description/tags/chapters/thumbnail): `4_доки/docs/seo-playbook.md`
- Channel identity (name, logo, avatar, banner, description): `4_доки/channel/branding.md`
- What worked, what failed, and why: `4_доки/docs/retrospective-2026-09-14.md`
- How to make an episode end to end: skill `.claude/skills/new-episode/SKILL.md`

## The rules everything rests on

1. **Real footage is the product.** Stock or text cards got v1 and v2 rejected. Target 100% real footage and ≥25% SOT (original audio).
2. **Every excerpt ≤5.0 s.** The user considers this rule proven by experience. Enforce it and don't argue or add legal caveats.
3. **Brand assets come from the user only**: `2_пайплайн/brand/ymca_*.mp4` (transitions, random order) and
   `2_пайплайн/brand/biden_end.mp4` (after the last story, every episode). Never replace them with clips you found yourself.
4. **Facts sourced, opinions as opinions**, no invented quotes, no medical diagnoses.
5. **Thumbnails use real freeze-frames of the actual people involved, never an AI-generated likeness of a real person**
   — same fair-use logic as the video itself. Crop out the source's own chyron before adding our own text.
6. **Nothing is published without the user's explicit ✅.**

## Working style (the user's limits matter)

- **Opus plans, Sonnet executes.** Heavy work (footage search, downloads, renders) goes to subagents with
  `model: sonnet`: `.claude/agents/story-footage.md`, one per story, run in parallel, and `.claude/agents/episode-assembler.md`.
  Opus writes the episode spec, launches the agents, and reviews results.
- Subagent prompts must say: work autonomously, use blocking waits, don't end the turn while renders or downloads run.
- If the user says stop, stop every agent immediately (TaskStop) and kill leftover yt-dlp/ffmpeg processes.
- Talk to the user in Ukrainian. Keep it short.

## Layout — 4 top-level groups, nothing else at repo root

```
3_продакшн/<slug>/       ⭐ FINISHED, ready to upload. The only folder that matters for shipping a video: video.mp4,
                         thumbnail.jpg, seo.md, credits.txt. One episode = one folder here, nothing work-in-progress.
                         video.mp4 is git-ignored (large); thumbnail.jpg/seo.md/credits.txt are committed.
                         Folder names are prefixed by release order (01_, 02_, ...), not just the content-period slug.

1_робочі/                Working/production material — never shipped, never uploaded.
  episodes/<slug>/       episode.json, research.json, stories/<id>/{beats.json,clips.json,notes.md}
    stories/<id>/clips/  downloaded excerpts (git-ignored, reproducible from clips.json)
  render_cache/<slug>/   render intermediates: TTS cache, per-beat renders, verify frames, throwaway master/phone
                         copies (git-ignored, regenerable — see episode-assembler.md). Was called `work/` before 2026-09-15.

2_пайплайн/              The machinery — code and the fixed assets it consumes.
  pipeline/              render code: common, tts, render_beat, plates, assemble, verify, drift_check, run_all,
                         build_beats, build_intro_outro, build_brand_bumpers
  scripts/               setup.sh
  brand/                 user's fixed brand clips (committed): ymca_*.mp4 transitions, biden_end.mp4

4_доки/                  Reference material — rules, docs, channel identity. Consulted, not executed or shipped.
  docs/                  format bible, SEO playbook, retrospectives
  research/              month ranking and research scripts
  channel/               branding.md, avatar/logo/banner PNGs, thumbnail template know-how

(outside repo) ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo: uv venv (edge-tts, Pillow) + fonts. The repo lives on
the exFAT SSD, which can't hold a venv; override with WEIRDNEWS_MPT_DIR.
```

`.claude/`, `CLAUDE.md`, `README.md`, `.gitignore`, `.env`/`.env.example` stay at the repo root — required there by
tooling convention (Claude Code loads `.claude/` and `CLAUDE.md` from cwd root) or by GitHub convention (`README.md`).

## Commands

```bash
2_пайплайн/scripts/setup.sh                          # clone MPT + uv sync, brew yt-dlp/ffmpeg
uv run --project ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo python 2_пайплайн/pipeline/build_brand_bumpers.py      # re-roll transition order
uv run --project ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo python 2_пайплайн/pipeline/run_all.py \
  --episode 1_робочі/episodes/2026-09-trump-month \
  --voice en-US-BrianMultilingualNeural --rate=-8% --pitch=-2Hz \
  --out 1_робочі/render_cache/2026-09-trump-month/render_out/video.mp4   # TTS (cached) → beats → assemble → phone+youtube copies → credits → verify
```

That `--out` command produces, next to `video.mp4`: `video_youtube.mp4` (the one that actually ships), `video_phone.mp4`
(<29 MB, for review), `video_credits.txt`. The `episode-assembler` agent's job is to then copy just
`video_youtube.mp4` → `3_продакшн/<slug>/video.mp4` and `video_credits.txt` → `3_продакшн/<slug>/credits.txt` once verify passes.

`--rate=` and `--pitch=` need the `=` form, because argparse misreads a leading `-`.

## Watch out for

- **YouTube downloads:** run one yt-dlp process per agent, with `--sleep-requests 1 --sleep-interval 2`, and download **only sections**
  (`--download-sections "*START-END"`). Find timestamps from auto-subs (`--skip-download --write-auto-subs`).
  If blocked, try `--extractor-args "youtube:player_client=web_safari"`. If still blocked, write MANUAL_DOWNLOADS.md for the user.
- **Never print song lyrics** (subs of music videos included). The output filter kills the agent mid-task.
- **CNN pages return HTTP 451 to WebFetch.** Use the Playwright MCP browser to read them.
- **Pexels/urllib needs an explicit User-Agent** (Cloudflare 403). Keys live in `.env` (see `.env.example`), never print them.
- **Frozen frames** come from narr beats with too little footage. `verify.py` fails any freeze >1 s outside SOTs.
- Concatenating independently encoded shots with `-c copy` creates stalled frames. Re-encode at concat.
- **Audio drifting behind video, worse by the end (fixed 2026-09-15).** Root cause: both
  concat points (`render_beat.py concat_shots`, `assemble.py concat_and_normalize`) used
  the ffmpeg concat **demuxer**, which is only reliable for homogeneous-parameter inputs —
  source clips have heterogeneous native frame rates (29.97/25/30/60fps), and per-splice
  timing imprecision compounded across ~65-70 beats into ~300ms-2s of drift by the end of
  a ~380s episode (worst case measured: 2.19s on `2026-09-trump-month`). Fixed by
  switching both to the concat **filter** (`concat=n=N:v=1:a=1` in `-filter_complex`,
  `assemble.py` batches ~10 inputs at a time). That alone wasn't enough: even with the
  filter, a beat's audio (continuous PCM) and video (frame-quantized) can differ by a
  fraction of a frame, which still compounded across beats — fixed by hard-clamping each
  input's audio (`atrim`+`apad`) to that input's own `exact_video_duration` (frame
  count/fps, in `common.py` — NOT `ffprobe_duration`'s container-level `format=duration`,
  which can include a stray `start_time` offset) before concat. **`2_пайплайн/pipeline/drift_check.py`**
  (wired into `verify.py`) cross-correlates each checkpoint beat's own cached audio against
  the final file to catch this class of bug — the old duration/freeze checks passed on all
  four buggy episodes. Also needed `setsar=1` per input: sources with mismatched SAR abort
  the concat filter graph outright (`Failed to configure output pad`).
- The final concat file used to be huge (~700 MB) from a per-shot noise dither added to defeat freezedetect;
  that dither is removed and `verify.py`'s freeze threshold tightened instead — a passing render is now ~100–150 MB.
  If it balloons again, check for a reintroduced dither before touching concat settings.
- Disk is tight (SSD sits at ~14 GB free most of the time). Delete `1_робочі/render_cache/<slug>/` after a render passes
  verify and ships to `3_продакшн/`; each episode's `stories/*/clips/` (git-ignored, reproducible from `clips.json`)
  can also be deleted once the episode ships.
- **`edge-tts` intermittently raises `NoAudioReceived` under parallel load.** `tts.py` retries 4x with backoff; if
  a render still fails on TTS, just rerun `run_all.py --resume` — it skips beats already rendered.
- **A story-footage agent may refuse to download**, reading even an explicit human instruction relayed through a
  planner or a `.claude/agents/*.md` file as not-real user consent, and demand the user say so directly in chat.
  This is a permission-boundary rule the agent won't waive for itself — coach it in a fresh subagent turn instead of
  retrying the same one, or the user/orchestrator does that one story's footage by hand (see episode 2's n1 story).
- **Blocking `until pgrep -f "run_all.py" ...; do sleep 20; done` loops can self-match.** If the loop's own command
  line contains the literal string being grepped for, `pgrep -f` matches the loop itself and it never exits. Prefer
  waiting on a PID (`while kill -0 $PID 2>/dev/null; do sleep 20; done`) or a marker file over grepping for a
  process-name substring that appears in your own command.
- **This repo was reorganized twice after the fact** (2026-09-15: scattered `out/`/`episodes/`/`channel/thumbnails/`
  consolidated into one `videos/<slug>/` per episode; then that whole tree regrouped into the 4 top-level categories
  above). If you're reading an older transcript or a stale doc that says `out/`, `work/`, or bare `episodes/`/`pipeline/`/
  `brand/`/`docs/`/`channel/`/`research/` at repo root, trust the Layout section here instead — it's current.
- **Episode status:** four episodes shipped and living in `3_продакшн/`: `01_2026-09-trump-month`, `02_2025-08-trump-month`,
  `03_2025-09-trump-month`, `04_2026-01-trump-month` — each has `video.mp4`, `thumbnail.jpg`, `seo.md`, `credits.txt`, all
  reviewed and approved. No episode is in progress right now. Next step: pick month 5 from
  `4_доки/research/trump_months_ranking.md` (April 2025, ranked #4) and run the `new-episode` skill.
