---
name: product-3d-canvas-video-landing
description: Turn a Southern Machinery product's 3D viewer page (Three.js / eDrawings HTML on file.autoinsertion.com) plus its existing landing page into (1) an interactive canvas mechanism animation merged into that landing page as ONE new single HTML file, (2) 1–3 min 4K English voice-over videos in 16:9 (3840×2160) and 9:16 (2160×3840) with burned subtitles + SRT, (3) a YouTube thumbnail, (4) SEO title/description/chapters/tags/Shorts copy and VO script, and (5) uploads everything to Google Drive. Use when the user sends 3D drawing links + landing page links and asks for "动画视频 + 单 html 网页", "3D 图转动画", or a product explainer video.
version: 1.0.0
---

# Product 3D → Canvas Animation, 4K Videos & Single-HTML Landing Page (v1.0.0)

Code: `p3cv/` (Python package, one module per stage). Docs: `README.md` (quick start), `docs/ARCHITECTURE.md`
(modules, I/O, dependency graph), `docs/CONFIG.md` (every product.json key), `docs/EXTENDING.md` (plugins,
new scene types / viewers / sinks / voices), `docs/TROUBLESHOOTING.md` (error codes, sandbox gotchas).
Reference product: `examples/juki-gripper-nozzle/` (delivered 2026-10-22).

Sister skill: `cad3d-animation-video-landing` builds a real Three.js mesh engine from eDrawings data (heavier,
true 3D). Use THIS skill when a schematic 2D canvas of the mechanism + a captured 3D turntable is enough
(faster, fully config-driven, 1 product ≈ 1.5–2 h including a 40 min render).

## Inputs (ask only what is missing)
1. 3D viewer URL(s). 2. Existing landing page URL (the page the section is merged into).
3. Optional: product PDF / manual. 4. Drive parent folder (default Southern Machinery products folder).
Everything else (copy, scenes, palette from the page) you decide and state.

## Workflow (agent steps)
1. `bash scripts/setup_env.sh` (idempotent; the sandbox resets often).
2. `python3 -m p3cv init <PROJ> [--example juki-gripper-nozzle]` → edit `<PROJ>/product.json`: slug, product_name,
   brand colours (take them from the landing page's tailwind config / CSS), `sources`.
3. `python3 -m p3cv run <PROJ>/product.json download` → read `src/manifest.json`, `src/*.txt` and `img/*_b64_*`
   (embedded photos). Run `capture` in the background (3–8 min) and READ the turntable frames.
4. **Understand the mechanism** (most important): from the 3D frames + landing text + PDF write the cycle as
   5–8 steps (driver → motion → contact → result). Mark anything inferred from geometry as inferred.
5. Write the animation module `<PROJ>/anim.js` from `templates/anim-template.js` (contract: CYCLE, STEPS, stepAt,
   render(ctx,W,H,{t,theme,focus,noBox,noHud,noLabels}); pure function of t). Test frames with a quick page.
6. Write `segments` (VO, ~230–300 words, hook → brand → mechanism steps → specs → compatibility → CTA, each with a
   `chapter`), `landing.section`, `video.scenes`, `thumbnail`, `seo`. Numbers TTS-friendly in segments
   ("eleven millimetres"); `voice.replacements` fixes the subtitles ("info at smthelp dot com" → "info@smthelp.com").
7. `python3 -m p3cv run <PROJ>/product.json tts mix subtitles landing video thumbnail docs` → check
   `r/preview/sheet_169.jpg`, `sheet_916.jpg`, the landing page and thumbnail visually; fix overlaps; repeat.
8. `python3 -m p3cv run <PROJ>/product.json render` (detached workers) then `... mux --timeout 1100` repeatedly
   (each shell call ≤ 20 min) until both MP4s are verified.
9. `python3 -m p3cv run <PROJ>/product.json upload` (sink gdrive: needs `gws` + the Google account) → reply with the
   Drive folder link, what was produced, and every claim left out or inferred.

## Fact rules (non-negotiable)
- Only specs found in the sources. Do not repeat unverifiable marketing numbers (e.g. "99.99% pick-up rate",
  telemetry figures) in the video; list them in `seo.notes` as left out. Conflicts between sources → `待确认`.
- The canvas is a simplified schematic; say so in seo.notes. Machine-side features (vision check) are not product features.
- Reply to Jason in Chinese; deliverables in English.

## Outputs (PROJ/out)
`<slug>-landing-page-animated.html` · `<basename>_16x9_4K.mp4` · `<basename>_9x16_4K.mp4` ·
`youtube-thumbnail-<slug>.jpg` · `youtube-seo-title-description-<slug>.txt` · `<slug>-subtitles-en.srt` ·
`<slug>-voiceover-script-en.txt` · `delivery.json` (upload result).

## Upgrade policy
Core changes bump `VERSION` + `CHANGELOG.md` (SemVer: config-breaking = major). Product-specific behaviour goes in
product.json or a plugin, never in core. Run `python3 -m unittest discover -s tests` before committing.
