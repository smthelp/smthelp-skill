#!/bin/bash
# build_segments_original.sh — Mode B: Ken Burns segments from the user's own photos
# Adapted from the proven Radial Splicing Tape v2 build (2026-11-13).
# Usage: edit the CONFIG section, then run from the product video working directory.
set -e

# ---------- CONFIG: edit per product ----------
WORKDIR="$HOME/workspace/<product>-video"   # e.g. radial-splicing-tape-video
VO_DUR=90.768                                # measured voiceover duration (ffprobe)
SEG=11.346                                   # VO_DUR / 8
FRAMES=340                                   # round(SEG * 30)
A="$WORKDIR/assets"                          # photos live here
S="$WORKDIR/segments-v2"
OUT="$WORKDIR/<product>-4K-v2-original.mp4"
# ----------------------------------------------

cd "$WORKDIR"
mkdir -p "$S"

# $1 input $2 output $3 zoom-expr $4 x-expr $5 y-expr $6 extra-filter (may be empty)
build_still() {
  local extra=""
  if [ -n "$6" ]; then extra=",$6"; fi
  ffmpeg -y -v error -loop 1 -framerate 30 -t "$SEG" -i "$1" -filter_complex \
    "[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='$3':x='$4':y='$5':d=1:s=3840x2160:fps=30,trim=0:$SEG,settb=AVTB$extra[v]" \
    -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an "$2"
  echo "built $2"
}

CTR_X="iw/2-(iw/zoom/2)"
CTR_Y="ih/2-(ih/zoom/2)"

# --- Map one photo per segment (edit the file names and motions) ---
build_still "$A/photo1.jpg" "$S/seg1.mp4" "1.0+0.12*on/$FRAMES" "$CTR_X" "$CTR_Y" ""          # 0:00 pain: slow zoom in
build_still "$A/photo2.png" "$S/seg2.mp4" "1.12-0.12*on/$FRAMES" "$CTR_X" "$CTR_Y" ""        # 0:11 reveal: slow zoom out
build_still "$A/photo3.png" "$S/seg3.mp4" "1.0+0.12*on/$FRAMES" "$CTR_X" "$CTR_Y" ""          # 0:23 mechanism
# Seg 4 (specs): two half-length stills
HALF=$(python3 -c "print($SEG/2)")
HALF_FRAMES=$((FRAMES/2))
ffmpeg -y -v error -loop 1 -framerate 30 -t "$HALF" -i "$A/specs1.png" -filter_complex \
  "[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='1.0+0.10*on/$HALF_FRAMES':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=3840x2160:fps=30,trim=0:$HALF,settb=AVTB[v]" \
  -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an "$S/seg4a.mp4"
ffmpeg -y -v error -loop 1 -framerate 30 -t "$HALF" -i "$A/specs2.png" -filter_complex \
  "[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='1.10-0.10*on/$HALF_FRAMES':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=3840x2160:fps=30,trim=0:$HALF,settb=AVTB[v]" \
  -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an "$S/seg4b.mp4"
printf "file 'seg4a.mp4'\nfile 'seg4b.mp4'\n" > "$S/concat4.txt"
ffmpeg -y -v error -f concat -safe 0 -i "$S/concat4.txt" -c copy "$S/seg4.mp4"
# Seg 5 (tool): left-to-right pan at fixed zoom on a wide render
ffmpeg -y -v error -loop 1 -framerate 30 -t "$SEG" -i "$A/tool.png" -filter_complex \
  "[0:v]scale=4316:2160,zoompan=z='1.15':x='(iw-iw/zoom)*on/$FRAMES':y='(ih-ih/zoom)/2':d=1:s=3840x2160:fps=30,trim=0:$SEG,settb=AVTB[v]" \
  -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an "$S/seg5.mp4"
build_still "$A/photo6.png" "$S/seg6.mp4" "1.15-0.15*on/$FRAMES" "$CTR_X" "$CTR_Y" ""        # 0:57 how-to: slow zoom out, all steps visible
build_still "$A/photo7.png" "$S/seg7.mp4" "1.0+0.12*on/$FRAMES" "$CTR_X" "$CTR_Y" ""          # 1:08 benefits
build_still "$A/photo8.png" "$S/seg8.mp4" "1.12-0.12*on/$FRAMES" "$CTR_X" "$CTR_Y" \
  "drawbox=x=0:y=0:w=3840:h=150:color=0x0B2A5B:t=fill,drawtext=fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:text='smthelp.com':fontsize=76:fontcolor=white:x=(w-text_w)/2:y=32"  # 1:19 closing + top navy bar

# Concat all 8 segments
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\nfile 'seg5.mp4'\nfile 'seg6.mp4'\nfile 'seg7.mp4'\nfile 'seg8.mp4'\n" > "$S/concat_all.txt"
ffmpeg -y -v error -f concat -safe 0 -i "$S/concat_all.txt" -c copy "$S/video_nosub.mp4"
echo "=== concat done ==="
ffprobe -v error -show_entries format=duration -of csv=p=0 "$S/video_nosub.mp4"
# If concat is shorter than the voiceover (frame rounding), pad the last frame:
# add tpad to the final encode, e.g. [0:v]tpad=stop_mode=clone:stop_duration=0.1

# Final: voiceover + burned-in subtitles from hand-written ASS (PlayRes 3840x2160, 56pt)
ffmpeg -y -v error -i "$S/video_nosub.mp4" -i "$A/voiceover.mp3" -filter_complex \
  "[0:v]ass=subtitles.ass[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -t "$VO_DUR" -movflags +faststart "$OUT"

cp subtitles.srt "${OUT%.mp4}.srt"
echo "=== FINAL ==="
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT"
