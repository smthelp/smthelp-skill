#!/bin/bash
# Render N x 30s segments with html-video, mix narration, concat, optional BGM.
# Usage: render_and_assemble.sh <work_dir> <seg_count> [bgm_file]
set -euo pipefail

NODE="${NODE:-$(command -v node)}"
BIN="${BIN:-/Users/jasonwu/.workbuddy/tools/html-video/packages/cli/dist/bin.js}"
WDIR="${1:?work_dir}"; N="${2:?segment_count}"; BGM="${3:-}"

cd "$WDIR"
for i in $(seq 1 "$N"); do
  id="srt3min-s$i"   # override via env SEG_PREFIX if needed
  out=$($NODE "$BIN" project-create --name "$id" --aspect 16:9 --commercial --cwd . 2>&1)
  pid=$(printf '%s' "$out" | sed -n 's/.*"project_id":"\([^"]*\)".*/\1/p')
  echo "[$id] project=$pid"
  $NODE "$BIN" project-set-template "$pid" --template "$id" --cwd . >/dev/null
  $NODE "$BIN" project-render "$pid" --output "$WDIR/silent_$i.mp4" --cwd . 2>&1 | tail -1
  ffmpeg -y -v error -i "$WDIR/silent_$i.mp4" -i "$WDIR/vo/s$i.wav" \
    -filter_complex "[1:a]adelay=800|800,apad=whole_dur=30[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k "$WDIR/seg_$i.mp4"
done
: > "$WDIR/concat.txt"
for i in $(seq 1 "$N"); do printf "file '%s/seg_%d.mp4'\n" "$WDIR" "$i" >> "$WDIR/concat.txt"; done
ffmpeg -y -v error -f concat -safe 0 -i "$WDIR/concat.txt" -c copy "$WDIR/final_vo.mp4"
if [ -n "$BGM" ] && [ -f "$BGM" ]; then
  D=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$WDIR/final_vo.mp4")
  ffmpeg -y -v error -i "$WDIR/final_vo.mp4" -stream_loop -1 -i "$BGM" \
    -filter_complex "[1:a]volume=0.12,afade=t=in:d=2,afade=t=out:st=$(awk "BEGIN{print $D-7}"):d=6,apad=whole_dur=${D}[bg];[0:a][bg]amix=inputs=2:duration=first:normalize=0[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$WDIR/final.mp4"
else
  cp "$WDIR/final_vo.mp4" "$WDIR/final.mp4"
fi
echo "FINAL=$WDIR/final.mp4"
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name -of default=noprint_wrappers=1 "$WDIR/final.mp4"
