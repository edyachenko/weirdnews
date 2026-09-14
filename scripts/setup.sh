#!/usr/bin/env bash
# One-time setup on a fresh machine (macOS): tools, the vendored MoneyPrinterTurbo venv, .env.
set -euo pipefail
cd "$(dirname "$0")/.."

brew list ffmpeg >/dev/null 2>&1 || brew install ffmpeg
brew list yt-dlp >/dev/null 2>&1 || brew install yt-dlp
command -v uv >/dev/null || brew install uv

if [ ! -d MoneyPrinterTurbo ]; then
  git clone --depth 1 https://github.com/harry0703/MoneyPrinterTurbo.git
fi
(cd MoneyPrinterTurbo && uv python install 3.11 && uv sync --frozen)

[ -f .env ] || cp .env.example .env
echo "Done. Fill in .env (PEXELS_API_KEY, GEMINI_API_KEY)."
