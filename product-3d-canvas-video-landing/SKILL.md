---
name: product-3d-canvas-video-landing
description: Turn a Southern Machinery product's 3D viewer page (Three.js / eDrawings HTML on file.autoinsertion.com) or real photos, its existing landing page and its catalog/manual into (A) ONE self-contained landing HTML with an interactive mechanism animation, 3D turntable and CTA, and (B) 1–3 min 4K English voice-over videos in 16:9 (3840×2160) and 9:16 (2160×3840) with burned subtitles + SRT, a YouTube thumbnail, SEO/chapters/VO script, optionally uploaded to Google Drive. Also rewrites an existing model page into a new model or customer variant. Use for "产品 3D 图转化为动画视频和单 html 网页", "3D 图转动画", "动画视频 + 单 html 网页", product explainer videos.
version: 1.3.1
---

# Product 3D → Mechanism Animation, 4K Videos & Single-HTML Landing Page (`p3cv` v1.3.1)

Self-contained: everything below works without any earlier conversation. Machine-readable record: `skill.json`.
Call contract: `docs/CONTRACT.md`. Parameters: `docs/CONFIG.md`. Upgrades: `docs/UPGRADING.md`.
Internals: `docs/ARCHITECTURE.md`, `docs/EXTENDING.md`, `docs/TROUBLESHOOTING.md`. Repo-wide rules: `../AGENTS.md`.

## Scope
Use for: one product/machine (feeder, nozzle, inserter, rack…) with a 3D drawing viewer or real photos/renders,
an existing landing page to extend (or a model page to turn into a new model / customer variant), and a
marketing explainer video. Not for: real-mesh WebGL engines or exploded views (`cad3d-animation-video-landing`,
`smt-3d-animation-landing-kit`), 7-language pages with blogs (`product-3d-doc-html-landing`), publishing.

## Inputs (ask only for what is missing, one short question)
| Input | Required | Notes |
|---|---|---|
| 3D viewer URL(s) or photos/renders | yes (one of) | eDrawings export / Three.js page → turntable; photos → `img/` |
| Existing landing page (URL or file) | yes for product A | merged into, never rebuilt from scratch |
| Catalog / manual / PDF / PPTX / DOCX | strongly advised | the ONLY source of numbers |
| Model/variant definition from the user | when given | user statements are a source (e.g. "4 heads, 0.5 s/part") |
| Customer RFQ / BOM / PCB photos | optional | customer variant; treat drawings as confidential |
| Delivery folder (Drive id) | optional | default sink `local` |

## Outputs (`PROJ/out`)
A: `<slug>-landing-page-animated.html` (single file, images inlined, works offline).
B: `<basename>_16x9_4K.mp4`, `<basename>_9x16_4K.mp4` (H.264 + AAC, −14 LUFS, burned subs),
`youtube-thumbnail-<slug>.jpg` (1920×1080), `youtube-seo-title-description-<slug>.txt`, `<slug>-subtitles-en.srt`,
`<slug>-voiceover-script-en.txt`. Plus `manifest.json` (sha256 + versions) and `delivery.json` (upload).

## Configurable parameters (all in `PROJ/product.json`, defaults in `p3cv/config.py`)
`brand` colours/logo/contacts · `sources` · `capture` (frames, zoom, drag, crop) · `anim` (module, global) ·
`voice` (edge-tts voice, rate, gaps, LUFS, TTS→subtitle replacements) · `segments` (VO + chapters) ·
`landing` (base, insert_before, nav, section copy, **replacements**, **forbid**) · `video` (formats, fps, scale,
**upscale**, chunks, scenes) · `thumbnail` · `seo` · `upload` (sink, parent) · **`privacy`** · `hooks` · `plugins`.

## Workflow
1. `bash scripts/setup_env.sh` (idempotent; re-run after a sandbox reset).
2. `python3 -m p3cv init PROJ [--example juki-gripper-nozzle|s3010a-radial-inserter|s7040p-pin-insertion]`; fill slug, product_name,
   brand colours (from the landing page CSS), sources. `python3 -m p3cv check PROJ/product.json`.
3. `p3cv run PROJ/product.json download` → read `src/manifest.json`, `src/*.txt`, `img/`. Run `capture` in the
   background (3–8 min) and LOOK at the turntable frames; drop dark/edge-on/glitch frames.
4. **Understand the mechanism**: write the cycle as 5–11 steps (driver → motion → contact → result) from frames +
   docs. Mark geometry-only inferences as inferred.
5. Write `PROJ/anim.js` from `templates/anim-template.js` (pure function of t). Variants of one platform (e.g.
   T/P/E models, 2 vs 4 heads, customer part set) are ONE module with a model switch, not copies.
6. Write `segments` (230–330 words: hook → brand → mechanism → specs → CTA, each with `chapter`), landing section
   copy, `video.scenes`, `thumbnail`, `seo`. Numbers TTS-friendly; `voice.replacements` fixes subtitles.
7. `p3cv run … tts mix subtitles landing video thumbnail docs` → check `r/preview/sheet_169.jpg`, `sheet_916.jpg`,
   a full-page screenshot of the landing page and the thumbnail; fix overlaps/clipping; repeat.
8. `p3cv run … render`, then `p3cv run … mux --timeout 1100` until exit 0 (exit 3 = still rendering).
   Sandboxes ≤ 8 GB: `video.scale: 1` + `video.upscale: true`; never encode two 4K files at once.
9. `p3cv manifest …`; `p3cv run … upload` if a sink is set. Reply with what was produced, every claim left out
   or inferred, and confidentiality cautions.

### Variant of an existing model page (new model name, customer configuration)
- Base = the closest model's landing page; rewrite its own copy with `landing.replacements` (title, meta, JSON-LD,
  hero, KPI strip, FAB, spec table, FAQ, advisor facts) and list the old model name in `landing.forbid`.
- Same machine body, new badge: `python3 -m p3cv relabel photo.jpg --bbox x0,y0,x1,y1 --text NEWMODEL`, inspect at
  300 %, and note "badge digitally edited" in `seo.notes`.
- Customer variant: parts table (part, max Ø, hole, feeder) + fit table "published data vs your need"; put customer
  drawings/3D models in `privacy.confidential` (never shown), add `privacy.notes` for photos/dimensions that are
  shown, and ask the user before anything is published. Customer data never goes into the public skill repo.

## Fact rules (non-negotiable)
- Only numbers from the product's spec sheet/catalog/landing page or stated by the user. Sister-model numbers
  (other series, other head count) are not this model's - drop them or label them as the reference model.
- Unverifiable marketing numbers stay out of the video; list them in `seo.notes`. Conflicts → `to be confirmed`.
- Values outside published ranges (e.g. a part smaller than the published pin range) → "proven on samples first".
- The animation is a schematic; say so on the page and in `seo.notes`.
- Reply to the user in their language (Jason: Chinese); deliverables in English unless asked.

## Upgrade policy (summary of docs/UPGRADING.md)
SemVer. `VERSION` = `skill.json.version` = front matter `version` (tested). Config-breaking or contract-breaking =
MAJOR with a `migrate` step. Product logic lives in product.json / anim module / plugins, never in core.
Run `python3 -m unittest discover -s tests` before committing; tag `p3cv-vX.Y.Z`.
