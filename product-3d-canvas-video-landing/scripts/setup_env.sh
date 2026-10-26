#!/usr/bin/env bash
# One-time environment setup (Debian/Ubuntu). Safe to re-run: every step is idempotent.
# Needs: python3 >= 3.9, ffmpeg. Optional: gws (Google Drive sink), rclone (rclone sink).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
echo "[setup] python packages"
python3 -m pip install --user -q -r "$HERE/requirements.txt"
if command -v apt-get >/dev/null; then
  echo "[setup] system libraries for headless chromium + fonts + ffmpeg"
  SUDO=$(command -v sudo || true)
  $SUDO apt-get update -q >/dev/null 2>&1 || true
  for pkg in libatk1.0-0 libatk-bridge2.0-0 libxcomposite1 libxdamage1 libatspi2.0-0 libnss3 libxkbcommon0 \
             libgbm1 "libasound2|libasound2t64" fonts-inter ffmpeg; do
    ok=0; IFS='|' read -ra alts <<< "$pkg"
    for p in "${alts[@]}"; do $SUDO apt-get install -y -q "$p" >/dev/null 2>&1 && { ok=1; break; }; done
    [ $ok = 1 ] || echo "[setup] WARN could not install $pkg"
  done
fi
echo "[setup] chromium for playwright"
python3 -m playwright install chromium 2>&1 | grep -v BEWARE || true
command -v ffmpeg >/dev/null || { echo "[setup] ERROR ffmpeg missing"; exit 1; }
echo "[setup] done - try: python3 -m p3cv check examples/juki-gripper-nozzle/product.json"
