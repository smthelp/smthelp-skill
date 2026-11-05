#!/usr/bin/env bash
# Idempotent environment setup (re-run after a sandbox reset: apt/pip installs can vanish).
# Needs: chromium (system), ffmpeg, imagemagick, poppler-utils; python: playwright, edge-tts, numpy, pillow (trimesh optional).
set -e
need_apt=""
command -v chromium >/dev/null 2>&1 || command -v chromium-browser >/dev/null 2>&1 || need_apt="$need_apt chromium"
command -v ffmpeg  >/dev/null 2>&1 || need_apt="$need_apt ffmpeg"
command -v convert >/dev/null 2>&1 || need_apt="$need_apt imagemagick"
command -v pdftotext >/dev/null 2>&1 || need_apt="$need_apt poppler-utils"
if [ -n "$need_apt" ]; then
  SUDO=""; [ "$(id -u)" != 0 ] && command -v sudo >/dev/null && SUDO=sudo
  $SUDO apt-get update -qq && DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq $need_apt fonts-dejavu fonts-liberation fonts-noto-core fonts-noto-cjk
fi
python3 -c "import playwright, edge_tts, numpy, PIL" 2>/dev/null || python3 -m pip install -q playwright edge-tts numpy pillow
# no system chromium (e.g. macOS/Windows): fall back to Playwright's own browser
command -v chromium >/dev/null 2>&1 || python3 -m playwright install chromium || true
python3 -c "import playwright, edge_tts, numpy, PIL; print('python deps ok')"
command -v chromium || echo "using Playwright bundled chromium"
