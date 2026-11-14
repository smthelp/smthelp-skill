---
name: smt-product-video
description: Turn a Southern Machinery product landing page into a finished 60–180 second 4K marketing video with English voiceover, burned-in English subtitles, a custom thumbnail, and a YouTube SEO package, then publish it to the Smthelping channel. Two visual modes: AI-generated 3D-style clips, or the user's own photos only. Use when Jason asks for a product marketing video, a YouTube video for a product, or to continue the product-video series from the landing-page list.
metadata:
  version: 1.0.0
  updated: 2026-11-14
  first_case: S-MVF01 (75 s, Sep 2026); S7000 (89 s, Oct 2026); Radial Splicing Tape v1 AI clips + v2 original photos only (Nov 2026)
  requires: ffmpeg with libass, Noto Sans, TTS (spoken-audio skill), live browser for YouTube Studio
---

# SMT Product Marketing Video

One product landing page from file.autoinsertion.com becomes a finished 4K YouTube marketing video: English voiceover, burned-in English subtitles, thumbnail, SEO package, upload to the Smthelping channel, plus ready-to-post social captions. Proven three times: S-MVF01, S7000, Radial Splicing Tape (v1 and v2).

## 1. When to use / boundaries

Use for: a product marketing video from a landing page; the next product in the series from the landing-page list; a new version of an existing video (new visuals, same script).

Do not use for: rebranding raw supplier demo clips (use `smt-product-video-rebrand`, which delivers to Google Drive and never publishes); CAD/3D-animation landing pages (use `cad3d-animation-video-landing` or `smt-3d-product-media`); API-based YouTube upload from stored OAuth tokens (use `smthelp-video-to-youtube` — different environment, macOS tokens); vertical Shorts as the main output (future extension).

Two visual modes (see `references/modes.md`):
- **Mode A — AI clips.** 6–8 AI-generated 3D-animation-style clips (~10 s each). Use when no usable product photos exist.
- **Mode B — original materials only.** Ken Burns motion (slow zoom/pan) on the user's own photos. **Default whenever the user supplies photos.** Jason's standing boundary (2026-11-13): when he supplies originals, no additional images or videos are generated and all material must be strictly based on the attachments and links he provided.

Stop and ask Jason when: the landing page has no usable specs (offer a `待确认` list, never invent numbers); the product's Southern Machinery model name is unknown; a video needs a claim no source supports.

## 2. Inputs

Required:
- **Product source**: a landing page URL on file.autoinsertion.com (`/public/Product landing Page/<file>.html`), or a product chosen from the landing-page list at https://file.autoinsertion.com/#/Product%20landing%20Page (hash routing — enumerate with the live browser; plain text fetch 404s).
- **Target**: 60–180 s, 4K 16:9, English voiceover + burned-in English subtitles, for the Smthelping channel (https://www.youtube.com/c/Smthelping).

Optional:
- User-supplied photos/video (→ Mode B), reference YouTube videos, product codes and prices, cutter/tool variants, target length, thumbnail preference.

## 3. Pipeline

### Step 1 — Extract the product
Fetch the landing page via its `/public/...` path. Extract: product name, hook/pain point, working steps, core specs, variants, prices, CTA. Record the source URL. Download the page's product images; keep the clearest as `assets/product.png`. Copy user-supplied photos into `assets/` (never modify their content).

### Step 2 — Script, voiceover, subtitles
- English script, 190–230 words for 75–90 s (scale proportionally for other lengths). Structure: hook → what it is → specs → how to use → EMS benefits → CTA (Visit smthelp.com / Contact Southern Machinery). See `references/script-template.md`.
- Write all numbers as spelled-out English words for TTS (e.g. "zero point zero one five", "twelve point seven").
- Generate the English voiceover (spoken-audio skill); measure the real duration with ffprobe and record it — every later timing derives from it.
- Write `subtitles.srt`: ≤2 lines per entry, ≤42 characters per line, time-aligned to the voiceover.

### Step 3 — Visuals (8 segments)
Segment length = voiceover duration ÷ 8 (e.g. 90.768 s → 11.346 s each). Map segments to script beats: 1 pain point, 2 product reveal, 3 mechanism, 4 specs, 5 tool/cutter, 6 how-to, 7 benefits, 8 closing. See `references/modes.md` and `references/pipeline.md`.
- Mode A: generate 6–8 clips (~10 s each), slow each to segment length (`setpts=PTS*1.1346` for a 10 s clip → 11.346 s).
- Mode B: one Ken Burns still per segment (zoompan, ±0.10–0.15 zoom range); a specs segment may split into two half-length stills; a how-to panel stays fully visible while zooming out.

### Step 4 — 4K assembly
ffmpeg: concat segments → scale 3840×2160, 30fps → pad with last frame (`tpad`) or trim (`-t`) to the exact voiceover length → mix voiceover as main audio (AAC 192k) → burn subtitles from **hand-written ASS** (PlayRes 3840×2160, Noto Sans 56pt — see `references/pipeline.md` for why the `subtitles` filter must not be used). Outputs: `<PRODUCT>-4K-final.mp4` (H.264/yuv420p) + `<PRODUCT>-4K-final.srt`.

### Step 5 — Thumbnail, YouTube version, SEO
- Thumbnail 1280×720: product frame or user photo + navy banner + product name. Verify by looking at it.
- YouTube-ready version: libx264 CRF 24, AAC 128k, faststart, target ~100–120 MB. **Always verify it decodes fully** (`ffmpeg -i file -f null -`) before handing it over.
- SEO package (`youtube-description-final.txt`): English title, description with chapters and key specs, tags. **Verify every CTA link opens and points at the right page before sending** — never leave an empty link line. See `references/seo-template.md`.
- Social captions (`social-posts-radial-splicing-tape.txt` pattern): English LinkedIn / Facebook / X drafts, ready to post, with a `[YouTube link]` placeholder until the video is published. See `references/social-captions-template.md`.

### Step 6 — Publish to the Smthelping channel
See `references/upload-runbook.md`. Upload via the live browser (YouTube Studio) with the compressed file and thumbnail, filling title/description/tags, language English, category Science & Technology, visibility Public.
- The managed/server browser never shares the user's own device login: the upload stops at the Google sign-in page. The user takes over the browser, logs in to the Smthelping channel's Google account, and signals to continue. Idle sessions close after ~2 hours; if expired, reopen one stopped at the login page on the user's say-so.
- **Never record a video as published until the published URL is confirmed.**
- Fallback: hand the user the upload file + thumbnail + copy-paste SEO package for self-upload on a logged-in device.

## 4. Hard rules (from real incidents — see `references/lessons-learned.md`)

- **Specs as measured.** Quote the page's own numbers; when sources disagree, publish the range (e.g. 4,000–12,000 CPH), never a single promised figure. Efficiency claims carry their source ("per the product page"). Prices only as listed on the product page. Anything unverified is marked `待确认 / to be confirmed`.
- **Verify every CTA link** in SEO copy before sending — twice a description went out with a dead link line.
- **Verify every compressed file decodes fully** before delivery — a 54 MB version once shipped corrupt (missing moov atom).
- **Subtitle size**: hand-written ASS with PlayRes 3840×2160. The `subtitles` filter's default PlayRes (384×288) inflates 56pt to ~420pt.
- **File-size limit**: the browser's file grant fails around 185 MB; ~115 MB passes. The master may be 200 MB+ — the compressed version is the uploadable one.
- **User-supplied originals take precedence**: when the user provides photos, use only those (Mode B). Never re-propose AI-generated footage for that product after the user has corrected it.
- **Chat in Simplified Chinese, deliverables in English.**

## 5. Workspace layout

- `~/workspace/<product>-video/` — script.txt, subtitles.srt, subtitles.ass, assets/ (voiceover.mp3, product.png), `<PRODUCT>-4K-final.mp4`, `<PRODUCT>-4K-final.srt`, `<PRODUCT>-thumbnail.png`, `<PRODUCT>-4K-youtube.mp4`, youtube-description-final.txt, social-posts-<product>.txt
- `~/workspace/goals/<product>-marketing-video-and-youtube-publication/files/` — the same deliverables as the goal's documents (track the job as a goal: production → delivery → upload)
- `~/workspace/your_files/` — copies for the user to download (upload version, SRT, thumbnail, SEO text; master only if small enough)

## 6. Verification before delivery

Run `references/verification-checklist.md` end to end: ffprobe (3840×2160, 30fps, duration ≈ voiceover, audio + video streams), full decode of master and upload version, frame extracts at 4+ points confirming burned-in subtitles are ~56pt and the picture is full-frame, thumbnail dimensions, every CTA link opened, SRT entry count vs script. Self-audit before anything reaches Jason.

## 7. Versioning and upgrades

- Version lives in this file's frontmatter (`metadata.version`), in `VERSION`, and in `CHANGELOG.md`. Bump on any pipeline change; record the case that proved it.
- Add new lessons to `references/lessons-learned.md` with the date and the job — never silently drop a hard rule.
- Keep the skill backward compatible: new modes and options are additive; never rename the deliverable filenames an existing job depends on.
- Related skills stay separate: this skill does not absorb `smt-product-video-rebrand` (raw clips → Drive) or `smthelp-video-to-youtube` (API upload). Cross-link them here instead.
