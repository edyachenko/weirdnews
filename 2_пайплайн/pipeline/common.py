"""Shared helpers for the weirdnews episode pipeline."""
import json
import re
import subprocess
import shlex
import os
import textwrap

# repo root, computed from this file's location so the pipeline works from any clone path.
# This file lives at <ROOT>/2_пайплайн/pipeline/common.py -- three levels down.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PIPELINE_GROUP = os.path.join(ROOT, "2_пайплайн")   # pipeline/, scripts/, brand/
WORK_GROUP = os.path.join(ROOT, "1_робочі")          # episodes/, render_cache/

W, H, FPS = 1920, 1080, 30
# MoneyPrinterTurbo (its uv venv + fonts) lives outside the repo: the repo sits on an exFAT SSD, which
# can't hold a venv's symlinks. Override with WEIRDNEWS_MPT_DIR.
MPT_DIR = os.environ.get("WEIRDNEWS_MPT_DIR") or next(
    (p for p in (os.path.expanduser("~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo"),
                 os.path.join(PIPELINE_GROUP, "MoneyPrinterTurbo")) if os.path.isdir(p)),
    os.path.expanduser("~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo"))
FONT = os.path.join(MPT_DIR, "resource/fonts/BeVietnamPro-Bold.ttf")


def load_episode(episode_dir):
    """Load 1_робочі/episodes/<slug>/episode.json and resolve its story order, voice defaults,
    and intro/outro visual paths (relative to the episode dir) to absolute paths."""
    episode_dir = os.path.abspath(os.path.expanduser(episode_dir))
    with open(os.path.join(episode_dir, "episode.json")) as f:
        ep = json.load(f)
    ep["_dir"] = episode_dir
    ep["_slug"] = ep.get("slug") or os.path.basename(episode_dir)
    ep["_stories_root"] = episode_dir  # stories live at <episode_dir>/stories/<id>

    def resolve(paths):
        return [p if os.path.isabs(p) else os.path.join(episode_dir, p) for p in paths]

    for section in ("intro", "outro"):
        if section in ep:
            ep[section]["_visuals_abs"] = resolve(ep[section].get("visuals", []))
    return ep


def bumper_slot_names(n_stories):
    """Y.M.C.A.-style bumper slots for n_stories: one before the first, one between each
    consecutive pair, one after the last."""
    return ["ymca_open"] + [f"ymca_gap{i}" for i in range(1, n_stories)] + ["ymca_close"]


def get_pexels_key():
    """PEXELS_API_KEY from the environment, then .env, then MoneyPrinterTurbo/config.toml."""
    key = os.environ.get("PEXELS_API_KEY")
    if key:
        return key
    env_path = os.path.join(ROOT, ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line.startswith("PEXELS_API_KEY="):
                v = line.split("=", 1)[1].strip()
                if v:
                    return v
    cfg_path = os.path.join(MPT_DIR, "config.toml")
    if os.path.exists(cfg_path):
        m = re.search(r'pexels_api_keys\s*=\s*\[\s*"([^"]+)"', open(cfg_path).read())
        if m:
            return m.group(1)
    return None


def run(cmd, check=True, quiet=True):
    """Run a shell command (list of args). Returns CompletedProcess."""
    if quiet:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    else:
        p = subprocess.run(cmd)
    if check and p.returncode != 0:
        out = getattr(p, "stdout", "")
        raise RuntimeError(f"command failed ({p.returncode}): {' '.join(shlex.quote(c) for c in cmd)}\n{out}")
    return p


def ffprobe_duration(path):
    p = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path,
    ])
    return float(p.stdout.strip())


def exact_video_duration(path, fps=FPS):
    """Duration implied by the video stream's own frame count / fps -- the ground truth
    for what a concat filter's `fps=,setpts=PTS-STARTPTS` reset actually produces on this
    input, which can differ slightly from the container's own top-level `duration`
    (format=duration, used by ffprobe_duration): some sources carry a small start_time
    offset from upstream re-encoding, which format=duration includes but a PTS-reset
    video stream does not. Used to clamp each input's audio to the SAME length its video
    will actually occupy after the concat filter, so per-input sub-frame AV mismatches
    can't accumulate into audio-vs-video drift across dozens of concatenated inputs."""
    p = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=nb_frames",
             "-of", "default=noprint_wrappers=1:nokey=1", path], check=False)
    v = (p.stdout or "").strip()
    if v.isdigit():
        return int(v) / fps
    # container didn't carry a frame count (rare for our own re-encoded beat files) --
    # fall back to an exact (slow, decodes the stream) frame count, then to the
    # format-level duration if even that fails.
    p2 = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
              "-show_entries", "stream=nb_read_frames",
              "-of", "default=noprint_wrappers=1:nokey=1", path], check=False)
    v2 = (p2.stdout or "").strip()
    if v2.isdigit():
        return int(v2) / fps
    return ffprobe_duration(path)


def ffprobe_dims(path):
    p = run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0:s=x", path,
    ])
    w, h = p.stdout.strip().split("x")
    return int(w), int(h)


def has_audio_stream(path):
    p = run([
        "ffprobe", "-v", "error", "-select_streams", "a",
        "-show_entries", "stream=index", "-of", "csv=p=0", path,
    ], check=False)
    return bool(p.stdout.strip())


def scale_crop_filter(is_portrait_or_4x3=False):
    """Return an ffmpeg -vf filter string that fills 1920x1080.

    For normal 16:9-ish sources: scale to cover + centre crop.
    For 4:3 / vertical sources: blurred background pad instead of stretching.
    """
    if not is_portrait_or_4x3:
        return (
            f"scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H}"
        )
    # blurred pad: background = blurred/scaled-to-cover copy, foreground = fit-inside copy
    return (
        f"split=2[bg][fg];"
        f"[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=20[bg2];"
        f"[fg]scale={W}:{H}:force_original_aspect_ratio=decrease[fg2];"
        f"[bg2][fg2]overlay=(W-w)/2:(H-h)/2"
    )


def is_4x3_or_portrait(path):
    w, h = ffprobe_dims(path)
    ar = w / h
    return ar < 1.5  # 16:9 ~1.78, 4:3 ~1.33, portrait <1


def wrap_caption(text, max_chars=42, max_lines=2):
    lines = textwrap.wrap(text, width=max_chars, break_long_words=False)
    if len(lines) > max_lines:
        # merge overflow into last allowed line, then re-wrap harder if needed
        head = lines[:max_lines - 1]
        rest = " ".join(lines[max_lines - 1:])
        lines = head + textwrap.wrap(rest, width=max_chars, break_long_words=True)[:1]
    return lines[:max_lines]


def drawtext_escape(s):
    return (
        s.replace("\\", "\\\\\\\\")
        .replace(":", "\\:")
        .replace("'", "’")
        .replace("%", "\\%")
    )


def loudnorm_filter():
    return "loudnorm=I=-16:TP=-1.5:LRA=11"


NORMALIZE_V = f"scale={W}:{H},setsar=1,fps={FPS},format=yuv420p"
