#!/bin/bash
# build_segments_ai.sh — Mode A: slow AI-generated clips to segment length, then concat
# Adapted from the proven S7000 / Radial Splicing Tape v1 builds.
# Usage: edit the CONFIG section, then run from the product video working directory.
set -e

# ---------- CONFIG: edit per product ----------
WORKDIR="$HOME/workspace/<product>-video"
VO_DUR=90.768                                # measured voiceover duration (ffprobe)
SEG=11.346                                   # VO_DUR / 8
SLOW=1.1346                                  # SEG / 10 (for ~10 s source clips)
C="$WORKDIR/clips"                           # generated clips live here
S="$WORKDIR/segments"
OUT="$WORKDIR/<product>-4K-final.mp4"
# ----------------------------------------------

cd "$WORKDIR"
mkdir -p "$S"

# $1 input $2 output : ~10 s clip -> SEG seconds (gentle slow-down)
build_clip() {
  ffmpeg -y -v error -i "$1" -filter_complex \
    "[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,setpts=PTS*$SLOW,fps=30,trim=0:$SEG,settb=AVTB[v]" \
    -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an "$2"
  echo "built $2"
}

# One clip per segment; remaining segments use Ken Burns stills (see build_segments_original.sh)
build_clip "$C/clip1.mp4" "$S/seg1.mp4"   # pain point
build_clip "$C/clip2.mp4" "$S/seg2.mp4"   # product reveal
build_clip "$C/clip3.mp4" "$S/seg3.mp4"   # mechanism close-up
# seg4 / seg6: Ken Burns stills (specs, how-to) — build with build_segments_original.sh patterns
build_clip "$C/clip5.mp4" "$S/seg5.mp4"   # tool / cutter
build_clip "$C/clip7.mp4" "$S/seg7.mp4"   # benefits
build_clip "$C/clip8.mp4" "$S/seg8.mp4"   # closing hero shot

# Concat all 8 segments (seg4 and seg6 must exist as stills-built files first)
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\nfile 'seg5.mp4'\nfile 'seg6.mp4'\nfile 'seg7.mp4'\nfile 'seg8.mp4'\n" > "$S/concat_all.txt"
ffmpeg -y -v error -f concat -safe 0 -i "$S/concat_all.txt" -c copy "$S/video_nosub.mp4"
echo "=== concat done ==="
ffprobe -v error -show_entries format=duration -of csv=p=0 "$S/video_nosub.mp4"

# Final: voiceover + burned-in subtitles from hand-written ASS (PlayRes 3840x2160, 56pt)
ffmpeg -y -v error -i "$S/video_nosub.mp4" -i "$WORKDIR/assets/voiceover.mp3" -filter_complex \
  "[0:v]ass=subtitles.ass[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -t "$VO_DUR" -movflags +faststart "$OUT"

cp subtitles.srt "${OUT%.mp4}.srt"
echo "=== FINAL ==="
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT"
