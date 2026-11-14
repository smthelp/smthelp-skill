# smt-product-video

Product landing page → finished 4K YouTube marketing video for Southern Machinery.

## What it does

Takes one product landing page from file.autoinsertion.com and produces:
- 60–180 s 4K (3840×2160, 30fps) 16:9 video, English voiceover, burned-in English subtitles + separate SRT
- Custom thumbnail (1280×720)
- YouTube SEO package: title, description with chapters, tags
- YouTube upload to the Smthelping channel (browser + user login)
- Ready-to-post English social captions (LinkedIn / Facebook / X)

Two visual modes: **AI-generated 3D-style clips** (no photos available) or **the user's own photos only** (Ken Burns motion) — the latter is the default whenever Jason supplies photos.

## When to use

Jason asks for a product marketing video, a YouTube video for a product, the next product in the video series, or a new version of an existing video.

## Quick start

1. Pick the product (landing-page URL or from the list at file.autoinsertion.com/#/Product%20landing%20Page).
2. Follow `SKILL.md` steps 1–6. The detailed ffmpeg recipes live in `references/pipeline.md`; the pre-delivery checks in `references/verification-checklist.md`.
3. Deliver the master + upload version + thumbnail + SEO text; upload only after Jason logs in to the Smthelping Google account in the browser session.

## Proven cases

| Product | Date | Result |
|---|---|---|
| S-MVF01 belt feeder | 2026-09-28 | 75 s 4K, voiceover + subtitles |
| S7000 odd-form insertion | 2026-10-08 | 89 s 4K, 115 MB upload version verified |
| Radial Splicing Tape v1 | 2026-11-12 | 90.768 s 4K, AI clips, 111 MB upload version |
| Radial Splicing Tape v2 | 2026-11-13 | 90.768 s 4K, original photos only, 31 MB upload version |

## Install

Copy this directory to the agent's skills directory (e.g. `~/.nanobot/workspace/skills/smt-product-video/`), or install the repo zip as a `.skill` file. See the repo root README.

## Version

v1.0.0 (2026-11-14). Version history: `CHANGELOG.md`. Bump the version in `SKILL.md` frontmatter, `VERSION`, and `CHANGELOG.md` on any pipeline change.
