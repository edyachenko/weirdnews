#!/usr/bin/env bash
# One-time setup on a fresh machine (macOS): tools, the vendored MoneyPrinterTurbo venv, .env.
set -euo pipefail
cd "$(dirname "$0")/../.."

brew list ffmpeg >/dev/null 2>&1 || brew install ffmpeg
brew list yt-dlp >/dev/null 2>&1 || brew install yt-dlp
command -v uv >/dev/null || brew install uv

# MoneyPrinterTurbo lives outside the repo: an exFAT drive can't hold a venv (symlinks).
MPT="${WEIRDNEWS_MPT_DIR:-$HOME/pet-projects/weirdnews-mpt/MoneyPrinterTurbo}"
if [ ! -d "$MPT" ]; then
  mkdir -p "$(dirname "$MPT")"
  git clone --depth 1 https://github.com/harry0703/MoneyPrinterTurbo.git "$MPT"
fi
(cd "$MPT" && uv python install 3.11 && uv sync --frozen)

[ -f .env ] || cp .env.example .env
echo "Done. Fill in .env (PEXELS_API_KEY, GEMINI_API_KEY)."
