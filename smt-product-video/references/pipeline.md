# Pipeline — exact ffmpeg recipes

All commands assume the working directory is `~/workspace/<product>-video/`, with `assets/voiceover.mp3` and `assets/` photos present. Measure the voiceover first; every timing derives from it.

## 0. Measure the voiceover

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/voiceover.mp3
# e.g. 90.768 s → segment length = 90.768 / 8 = 11.346 s
# SEG = voiceover_duration / 8 ; FRAMES_PER_SEG = round(SEG * 30)
```

## 1. Mode A — AI clips to segment length

Each generated clip is ~10 s; slow it to SEG seconds (11.346 s needs `setpts=PTS*1.1346`):

```bash
ffmpeg -y -v error -i clips/clip1.mp4 -filter_complex \
  "[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,setpts=PTS*1.1346,fps=30,trim=0:11.346,settb=AVTB[v]" \
  -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an segments/seg1.mp4
```

Video generation tools cap at 6 clips per message — generate in two batches if 7–8 segments are needed, and fill remaining segments with Ken Burns stills (Mode B).

## 2. Mode B — Ken Burns stills

Slow zoom-in (zoom range 1.00 → 1.12 over the segment):

```bash
ffmpeg -y -v error -loop 1 -framerate 30 -t 11.346 -i assets/product.png -filter_complex \
  "[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='1.0+0.12*on/340':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=3840x2160:fps=30,trim=0:11.346,settb=AVTB[v]" \
  -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an segments/seg1.mp4
```

- Zoom-out: `z='1.12-0.12*on/340'`.
- Left-to-right pan at fixed zoom (wide render): upscale first, then `zoompan=z='1.15':x='(iw-iw/zoom)*on/340':y='(ih-ih/zoom)/2'`.
- A how-to panel that must stay fully readable: zoom out from 1.15 to 1.00 (`z='1.15-0.15*on/340'`).
- A specs segment may split into two half-length stills (SEG/2 each), joined with the concat demuxer.
- `on` counts output frames; `340` = frames in 11.346 s at 30fps. For a different SEG, use `round(SEG*30)` and the half-segment count for split stills.

## 3. Concat

```bash
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\nfile 'seg5.mp4'\nfile 'seg6.mp4'\nfile 'seg7.mp4'\nfile 'seg8.mp4'\n" > segments/concat_all.txt
ffmpeg -y -v error -f concat -safe 0 -i segments/concat_all.txt -c copy segments/video_nosub.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 segments/video_nosub.mp4
```

**Frame-rounding fix:** if the concatenated video is shorter than the voiceover (e.g. 90.667 s vs 90.768 s — 340 frames per segment rounds down), pad the last frame with `tpad` before the final encode, or accept a final video stream up to 1 frame (0.033 s) shorter than the audio. Never let the last subtitle cue get cut.

## 4. Final 4K master — voiceover + burned-in subtitles

**Use hand-written ASS, not the `subtitles` filter.** The `subtitles` filter defaults PlayRes to 384×288, which inflates a 56pt font to ~420pt and covers the picture. Generate `subtitles.ass` from the SRT (template in `templates/subtitles.ass`): PlayResX 3840, PlayResY 2160, Noto Sans 56pt, outline 3, shadow 1, bottom margin 70, centered bottom.

```bash
ffmpeg -y -v error -i segments/video_nosub.mp4 -i assets/voiceover.mp3 -filter_complex \
  "[0:v]ass=subtitles.ass[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -t 90.768 -movflags +faststart <PRODUCT>-4K-final.mp4
cp subtitles.srt <PRODUCT>-4K-final.srt
```

Replace `-t 90.768` with the measured voiceover duration.

## 5. YouTube-ready compressed version

```bash
ffmpeg -y -v error -i <PRODUCT>-4K-final.mp4 -c:v libx264 -preset medium -crf 24 \
  -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart <PRODUCT>-4K-youtube.mp4
```

Target ~100–120 MB. Still-photo masters compress far smaller (Radial v2: 31 MB) — that is fine; the size target is an upper bound for the browser file grant, not a goal.

## 6. Thumbnail

1280×720 PNG: a product frame or user photo + navy banner (`#0B2A5B`) + white product name. Build with ffmpeg drawbox/drawtext or an image editor; always look at the result. Keep the bottom clear where burned subtitles would sit in video frames (not an issue for a still, but keep the composition clean).

## 7. Verify (also see `verification-checklist.md`)

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate \
  -show_entries format=duration,size -of default=noprint_wrappers=1 <PRODUCT>-4K-final.mp4
ffmpeg -v error -i <PRODUCT>-4K-final.mp4 -f null - && echo MASTER_DECODE_OK
ffmpeg -v error -i <PRODUCT>-4K-youtube.mp4 -f null - && echo YOUTUBE_DECODE_OK
# frame extracts at 4+ points (e.g. t=2/40/60/85) — check subtitles are burned in, ~56pt, bottom, full-frame, no black bars
```

`scripts/verify.sh` runs the ffprobe + decode checks for both files.
