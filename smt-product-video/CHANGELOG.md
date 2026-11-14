# Changelog — smt-product-video

## v1.0.0 — 2026-11-14

First codified release. Consolidates the pipeline proven on three products (S-MVF01, S7000, Radial Splicing Tape v1/v2) into a reusable, upgradeable skill.

- Two visual modes: Mode A (AI-generated 3D-style clips) and Mode B (user's own photos only, Ken Burns motion). Mode B is the default when the user supplies photos, per Jason's 2026-11-13 boundary.
- 8-segment structure (voiceover duration ÷ 8), hand-written ASS subtitles (PlayRes 3840×2160, Noto Sans 56pt), tpad frame-rounding fix.
- Verification checklist: ffprobe + full decode of master and upload version, frame extracts, CTA link checks.
- YouTube upload runbook (browser + user login, ~2 h idle expiry, ~115 MB file-grant limit) and social captions template (LinkedIn / Facebook / X).
- Incident log in `references/lessons-learned.md`: corrupt 54 MB upload version, two empty CTA link lines, subtitle PlayRes inflation to ~420pt, 185 MB file-grant failure.

## Pre-history (unversioned practice)

- 2026-09-28 — S-MVF01: first 4K video (75 s), pipeline established.
- 2026-10-08 — S7000: 89 s 4K, 115 MB upload version; upload blocked at Google login, session expired 2026-10-18.
- 2026-11-12 — Radial Splicing Tape v1: 90.768 s 4K with 6 AI clips + 2 Ken Burns stills; subtitle PlayRes bug found and fixed; cutter link added to SEO after audit.
- 2026-11-13 — Radial Splicing Tape v2: rebuilt from Jason's 28 photos only, no AI footage; 59 MB master, 31 MB upload version; social captions delivered.
