#!/bin/bash
# verify.sh — ffprobe + full-decode checks for the 4K master and the YouTube upload version
# Usage: ./verify.sh <product>-4K-final.mp4 <product>-4K-youtube.mp4
# Exits non-zero on any failure. Run before delivering anything to Jason.
set -e
MASTER="${1:?usage: verify.sh <master.mp4> <youtube.mp4>}"
YOUTUBE="${2:?usage: verify.sh <master.mp4> <youtube.mp4>}"

check() {
  local f="$1" label="$2"
  echo "=== $label: $f ==="
  ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate \
    -show_entries format=duration,size -of default=noprint_wrappers=1 "$f"
  ffmpeg -v error -i "$f" -f null - && echo "$label DECODE OK"
}

check "$MASTER" MASTER
check "$YOUTUBE" YOUTUBE

# Resolution + fps guard on the master (nokey=1 gives bare values, no commas)
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 "$MASTER")
H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 "$MASTER")
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 "$MASTER")
[ "$W" = "3840" ] && [ "$H" = "2160" ] && [ "$FPS" = "30/1" ] \
  || { echo "FAIL: master is ${W}x${H} @ ${FPS}, expected 3840x2160 @ 30fps"; exit 1; }
echo "RESOLUTION OK: 3840x2160 @ 30fps"
echo "ALL CHECKS PASSED"
