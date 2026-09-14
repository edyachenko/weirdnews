# weirdnews: Weird News USA

Repo location: `/Volumes/Extreme SSD/ютуб/політики/weirdnews` (exFAT SSD). Git uses `core.fileMode false`, and `._*` files are ignored.

Automated English news-commentary YouTube episodes built from **real footage**: short excerpts of news and
official videos, a sarcastic TTS host, and the channel's own brand transitions. The first episode ("Trump's Month",
Aug 14 – Sep 14 2026) was built on 2026-09-14. The plan is a series where each video covers one month of Trump's 2nd term.

- Format bible (read before making anything): `docs/format.md`
- What worked, what failed, and why: `docs/retrospective-2026-09-14.md`
- How to make an episode end to end: skill `.claude/skills/new-episode/SKILL.md`

## The rules everything rests on

1. **Real footage is the product.** Stock or text cards got v1 and v2 rejected. Target 100% real footage and ≥25% SOT (original audio).
2. **Every excerpt ≤5.0 s.** The user considers this rule proven by experience. Enforce it and don't argue or add legal caveats.
3. **Brand assets come from the user only**: `brand/ymca_*.mp4` (transitions, random order) and `brand/biden_end.mp4`
   (after the last story, every episode). Never replace them with clips you found yourself.
4. **Facts sourced, opinions as opinions**, no invented quotes, no medical diagnoses.
5. **Nothing is published without the user's explicit ✅.**

## Working style (the user's limits matter)

- **Opus plans, Sonnet executes.** Heavy work (footage search, downloads, renders) goes to subagents with
  `model: sonnet`: `.claude/agents/story-footage.md`, one per story, run in parallel, and `.claude/agents/episode-assembler.md`.
  Opus writes the episode spec, launches the agents, and reviews results.
- Subagent prompts must say: work autonomously, use blocking waits, don't end the turn while renders or downloads run.
- If the user says stop, stop every agent immediately (TaskStop) and kill leftover yt-dlp/ffmpeg processes.
- Talk to the user in Ukrainian. Keep it short.

## Layout

```
brand/                   user's fixed brand clips (committed)
docs/                    format bible, retrospectives
pipeline/                render code: tts, render_beat, plates, assemble, verify, run_all, build_brand_bumpers
episodes/<slug>/         one episode: episode.json, research.json, stories/<id>/{beats.json,clips.json,notes.md}
  stories/<id>/clips/    downloaded excerpts (git-ignored, reproducible from clips.json)
research/                month ranking and research scripts
(outside repo) ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo: uv venv (edge-tts, Pillow) + fonts. The repo lives on the exFAT SSD, which can't hold a venv; override with WEIRDNEWS_MPT_DIR
out/, work*/             renders and intermediates (git-ignored)
```

## Commands

```bash
scripts/setup.sh                                   # clone MPT + uv sync, brew yt-dlp/ffmpeg
uv run --project ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo python pipeline/build_brand_bumpers.py      # re-roll transition order
uv run --project ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo python pipeline/run_all.py \
  --episode episodes/2026-09-trump-month \
  --voice en-US-BrianMultilingualNeural --rate=-8% --pitch=-2Hz \
  --out out/2026-09-trump-month.mp4                # TTS (cached) → beats → assemble → phone copy → credits → verify
```

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
- The final concat file used to be huge (~700 MB) from a per-shot noise dither added to defeat freezedetect;
  that dither is removed and `verify.py`'s freeze threshold tightened instead — a passing render is now ~100–150 MB.
  If it balloons again, check for a reintroduced dither before touching concat settings.
- Disk is tight (SSD sits at ~14 GB free most of the time). Delete `work/<slug>/` after a render passes verify;
  each episode's `stories/*/clips/` (git-ignored, reproducible from `clips.json`) can also be deleted once the episode ships.
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
- **Episode status:** `2026-09-trump-month` and `2025-08-trump-month` are both rendered, verified, and delivered
  to the user (see `docs/retrospective-2026-09-14.md` for the full story). No episode is in progress right now —
  the next step is picking month 3 from `research/trump_months_ranking.md` (or a Gemini-grounded month digest)
  and running the `new-episode` skill.
