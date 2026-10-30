#!/bin/bash
# One-time (or after a sandbox reset): Python deps + ffmpeg check. Fonts ship in assets/fonts.
set -e
pip install -q numpy pillow edge-tts
command -v ffmpeg >/dev/null || { echo "E02 ffmpeg missing (apt-get install -y ffmpeg)"; exit 1; }
ffmpeg -hide_banner -filters 2>/dev/null | grep -q " ass " || echo "W01 ffmpeg has no libass: subtitles cannot be burned in"
echo "setup ok"
