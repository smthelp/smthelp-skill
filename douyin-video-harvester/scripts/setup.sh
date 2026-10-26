#!/usr/bin/env bash
# Install runtime deps (Debian/Ubuntu). Idempotent. Usage: bash scripts/setup.sh [--bin-dir DIR]
set -euo pipefail
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"; mkdir -p "$BIN_DIR"
need() { command -v "$1" >/dev/null 2>&1; }
SUDO=""; [ "$(id -u)" -ne 0 ] && need sudo && SUDO="sudo"
pkgs=()
need chromium || need chromium-browser || pkgs+=(chromium)
need ffmpeg || pkgs+=(ffmpeg)
need montage || pkgs+=(imagemagick)
if [ ${#pkgs[@]} -gt 0 ]; then
  $SUDO env DEBIAN_FRONTEND=noninteractive apt-get update -qq
  $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "${pkgs[@]}"
fi
python3 -c "import playwright" 2>/dev/null || python3 -m pip install -q "playwright>=1.45"
# playwright's bundled browser download may 403 on arm64 — we use system chromium instead (config.chromium).
if ! need yt-dlp && [ ! -x "$BIN_DIR/yt-dlp" ]; then
  curl -fsSL -o "$BIN_DIR/yt-dlp" https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp && chmod +x "$BIN_DIR/yt-dlp"
fi
echo "chromium: $(command -v chromium || command -v chromium-browser)"
echo "yt-dlp:   $(command -v yt-dlp || echo $BIN_DIR/yt-dlp) $("$(command -v yt-dlp || echo $BIN_DIR/yt-dlp)" --version)"
echo "ffmpeg:   $(ffmpeg -version | head -1)"
python3 -c "import playwright, importlib.metadata as m; print('playwright', m.version('playwright'))"
