# Verification checklist — run before anything reaches Jason

## Video

- [ ] ffprobe: 3840×2160, 30fps, H.264 yuv420p, audio AAC present, video + audio streams.
- [ ] Duration ≈ voiceover duration (within 0.1 s). Video stream not shorter than the voiceover minus 1 frame.
- [ ] Full decode passes, master and upload version: `ffmpeg -v error -i <file> -f null -` with no errors.
- [ ] Frame extracts at 4+ points (e.g. t=2/40/60/85): subtitles burned in, ~56pt, bottom, ≤2 lines, no black bars, picture full-frame.
- [ ] Last subtitle cue is not cut off (check the final 2 seconds).
- [ ] Upload version: ~100–120 MB target (still-photo masters may be far smaller — fine), faststart set, full decode passes.

## Subtitles

- [ ] SRT entry count matches the script beats; ≤2 lines, ≤42 chars/line.
- [ ] ASS file: PlayResX 3840, PlayResY 2160, Noto Sans 56pt, outline 3, MarginV 70.
- [ ] SRT and burned-in subtitles carry the same text.

## Thumbnail

- [ ] 1280×720, product frame or user photo, readable product name, looked at by a human.

## SEO package

- [ ] Title, description, chapters, tags present; chapters match the video's actual segment times.
- [ ] Every CTA link opened and confirmed to point at the right page (product page, shop, tool/accessory, website). No empty link line.
- [ ] All specs and prices match the product page (or are stated as a range / `per the product page`).

## Files and records

- [ ] Deliverables copied to the goal's `files/` directory and `~/workspace/your_files/` (upload version, SRT, thumbnail, SEO text; master only if small enough).
- [ ] Old versions kept intact when a new version is made (v1 files never overwritten).
- [ ] Upload status recorded honestly: "not attempted" / "blocked at login" / "published: <URL>". Never record "published" without the URL.
