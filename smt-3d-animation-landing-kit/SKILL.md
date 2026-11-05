---
name: smt-3d-animation-landing-kit
description: Turn a Southern Machinery product 3D drawing (eDrawings HTML, GLB/GLTF, STL, OBJ; STEP via conversion) plus its introduction documents (spec PDF, existing landing pages) into (1) a side-by-side mechanism animation, (2) ONE self-contained English-first HTML landing page with an interactive 3D model (rotate/zoom, material + lighting presets, explode), 7-language switch, 8 blog articles and an ROI calculator, (3) 4K YouTube explainer videos in 16:9 and 9:16 with English voice-over and word-synced subtitles, thumbnails and SEO copy, and (4) a Google Drive copy. Use when Jason sends a 3D drawing link plus one or two product/landing pages and says "用同样的方法做动画视频和落地页", "3D 图做成动画/视频/单 HTML", or asks for a product explainer video + interactive page.
version: 1.0.1
metadata:
  author: Southern Machinery (Jason Wu) · built with Hark
  repo: https://github.com/smthelp/smthelp-skill/tree/main/smt-3d-animation-landing-kit
  origin: SBF1001 vs S-MVF01 bowl/belt feeder job (2026-10-21) and STF1003 tube feeder job (2026-11-04)
  changelog: CHANGELOG.md
  related: cad3d-animation-video-landing (Three.js 3D camera videos), smt-product-landing-page (brand blocks), smt-evaluation-web-page (7-language pattern)
---

# smt-3d-animation-landing-kit (v1.0.1)

3D drawing + intro documents → mechanism animation → single-file 7-language landing page with interactive 3D → 4K 16:9 + 9:16 videos, thumbnails, SEO → Drive.
Everything is driven by one `job.json`; defaults live in `config/defaults.json`. Run `python3 scripts/smt3d.py` for the command list.

## When to use / not use
- Use: a product (or two products to compare) with a 3D drawing and a mechanism worth explaining, for export marketing.
- Use the **duel** (side-by-side) form when comparing two products (bowl vs belt) or "before vs after" (manual vs automatic).
- Not for: a 1688 link with photos only (`smt-product-landing-page`), a camera-flown 3D video of one part (`cad3d-animation-video-landing`),
  an evaluation report page (`smt-evaluation-web-page`).

## 1. Input contract (details: `references/input-contract.md`)
| Input | Format | Source | Naming |
|---|---|---|---|
| 3D drawing | eDrawings/HOOPS `.html` (preferred), `.glb/.gltf`, `.stl`, `.obj`; `.step` → convert to GLB first | `https://file.autoinsertion.com/public/SMT machine 3D Drawing in Html/` or local file | `<Product name>-Designed by Southern Machinery.html`; fetched copy saved as `src/drawing_<name>` |
| Intro documents | spec PDF (text layer), existing landing pages `.html` (1–2), optional manual PDF | `file.autoinsertion.com/public/Southern Machinery Product/`, `.../Product landing Page/` | saved as `src/doc_<name>.pdf`, `src/page_<name>.html` |
| Photos | `ph.smthelp.com` URLs or local jpg/png/webp (brand watermark only) | ph.smthelp.com search, PDF images (`analyze` extracts them) | `assets/<model>-<view>.jpg` |
| Task parameters | `job.json` (+ `content.json`, `script.json`, `i18n/<lang>.json`, `duel.js`, `video.html`, `thumb.html`) | `smt3d.py init <dir>` scaffolds them | slug = kebab-case, e.g. `stf1003-automatic-tube-feeder-vs-manual-tube-feeding` |

Parameters are passed **only through files**: `job.json` names the inputs and overrides any default under `"config"`; CLI arguments are just the job path, the video format and a time budget. Ask Jason only for what is missing (3D link, page links, which product is "A" vs "B", contact person if the source pages use a different salesperson).

## 2. Workflow (details: `references/workflow.md`)
| # | Step | Command | Output |
|---|---|---|---|
| 0 | Environment | `bash scripts/setup_env.sh` | chromium + playwright + edge-tts + numpy/pillow (re-run after a sandbox reset) |
| 1 | Scaffold + validate | `smt3d.py init jobs/<slug>` → edit → `smt3d.py validate job.json` | contract errors/warnings |
| 2 | **Deconstruct** 3D + 2 pages + docs | `smt3d.py fetch` → `smt3d.py analyze` | `build/analysis.md`: sections, headings, images, videos, contacts, PDF text, PDF images |
| 3 | 3D parse + lightweight | `smt3d.py mesh` | `assets/model.b64` (smt3d-v1: mm, int16, gzip; decimated to `model.triangle_budget`) |
| 4 | Copy extraction + structure | write `content.json` from analysis (FAB: pain → feature → advantage → benefit; facts only from spec sheets) | `content.json`, `i18n/<lang>.json` (`smt3d.py i18n-todo job <lang>`) |
| 5 | Mechanism animation | write `duel.js` (start from `examples/*/duel.js` or `templates/duel/duel-skeleton.js`) | deterministic `render(t, state)` SVG animation reused by page + video |
| 6 | Single HTML page | `smt3d.py lp` → `smt3d.py verify` | `out/<slug>.html` + `out/verify/` screenshots + report |
| 7 | 4K videos, thumbnails, SEO | `stage` → `tts` → `timeline` → `audio` → `render <169|916>` (repeat until done) → `finish <fmt>` → `thumbs` → `seo` | `out/<slug>-16x9-4k.mp4`, `-9x16-4k.mp4`, `subtitles_en.srt`, thumbnails, `youtube-seo-<slug>.txt` |
| 8 | Drive sync | `smt3d.py drive job.json` (Hark: run with the Google connector) | Drive folder under `config.drive.parent_folder_id` |
| 9 | Publish (optional, ask first) | `smt-product-landing-page` → `scripts/publish_webdav.sh` | needs WebDAV password from Jason via Hark Secured Login; never store it |

`smt3d.py all job.json` runs steps 1–7 except the long render. Render is resumable: each call renders missing 30 s segments within a time budget (background jobs stop at 20 min).

## 3. Output spec (details: `references/output-spec.md`)
- **One `.html` file**, no external CSS/JS/fonts/images; opens by double-click (file://). Network only on user action: YouTube iframe on click, links; Chatwoot only on http/https.
- **Interactive 3D** (`templates/landing/viewer3d.js`, dependency-free WebGL): drag rotate, wheel/pinch zoom, double-click reset, auto-rotate, material presets (industrial / matte / x-ray), lighting presets (studio / warm / top), explode slider; image fallback without WebGL.
- **Side-by-side mechanism animation** with 6 chapter tabs, play/pause, slow motion, per-chapter metric cards.
- **7 languages** (en, es, pt, fr, ar RTL, ru, zh) via `data-i18n` keys = content paths; `?lang=xx`, remembered in localStorage; untranslated keys fall back to English and are reported as coverage %.
- **8 blog articles** (count enforced = `blog_count`), **ROI calculator** (labour + extra output, payback from the buyer's own quote), fit check, specs table, gallery lightbox, docs, FAQ (+ FAQPage JSON-LD), brand header/footer, WhatsApp FAB, dark mode, print-safe, reduced-motion.
- **Videos**: 3840×2160 and 2160×3840, 30 fps H.264 + AAC, −14 LUFS, 1–3 min, burned-in captions + SRT; thumbnails 1280×720 (+4K) and Shorts cover 1080×1920; SEO txt with title ≤100, chapters from the timeline, tags ≤500 chars.

## 4. Configuration (defaults: `config/defaults.json`, reference: `references/config-reference.md`)
| Key | Default | Notes |
|---|---|---|
| `languages` | `["en","es","pt","fr","ar","ru","zh"]` | order = selector order; add a code + `language_labels` entry |
| `default_language` / `rtl_languages` | `en` / `["ar"]` | |
| `blog_count` | `8` | build fails if `content.blogs.items` differs |
| `theme` | brand `#0c665c`, deep `#073f39`, accent `#009fa5`, lime `#82bf32`, gold `#e0a63b`, radius 14 | CSS variables; `dark_mode_toggle: true` |
| `model.accepted_formats` | edrawings-html, glb, gltf, stl, obj, step | step must be converted (see input contract) |
| `model.triangle_budget` / `quantize_bits` | 120000 / 16 | lightweight target |
| `model.material_presets` / `lighting_presets` | industrial, matte, xray / studio, warm, top | first = initial |
| `sections` | hero, duel, why, how, model3d, specs, fit, roi, benefits, gallery, videos, blogs, docs, faq, contact | job may reorder/omit |
| `roi.defaults` | 1 operator, 6 USD/h, 8 h × 2 shifts × 300 days | no price ever published |
| `video` | 169+916, 30 fps, scale 2, voice en-US-AndrewMultilingualNeural, −14 LUFS, 30 s segments, 60–180 s | |
| `brand` | logo, +86 136 0256 2576, wa 8613602562576, info@smthelp.com, socials, Chatwoot | per required-blocks of `smt-product-landing-page` |
| `drive.parent_folder_id` | `1mHq3OaE-RS5vMWd0pWJcM-0kQfZSncNb` | "Southern Machinery 3D Animation" |

Override any key in `job.json → "config"` (deep merge). `config_version` changes only on breaking key changes.

## 5. Usage examples
```bash
bash scripts/setup_env.sh
python3 scripts/smt3d.py init jobs/s-xyz --example stf1003-tube-feeder
python3 scripts/smt3d.py validate jobs/s-xyz/job.json
python3 scripts/smt3d.py fetch    jobs/s-xyz/job.json && python3 scripts/smt3d.py analyze jobs/s-xyz/job.json
python3 scripts/smt3d.py mesh     jobs/s-xyz/job.json
python3 scripts/smt3d.py lp       jobs/s-xyz/job.json && python3 scripts/smt3d.py verify jobs/s-xyz/job.json
python3 scripts/smt3d.py stage    jobs/s-xyz/job.json && python3 scripts/smt3d.py tts jobs/s-xyz/job.json
python3 scripts/smt3d.py timeline jobs/s-xyz/job.json && python3 scripts/smt3d.py audio jobs/s-xyz/job.json
python3 scripts/smt3d.py render   jobs/s-xyz/job.json 169 --budget 1000   # repeat until "all segments rendered"
python3 scripts/smt3d.py finish   jobs/s-xyz/job.json 169                  # same for 916
python3 scripts/smt3d.py thumbs   jobs/s-xyz/job.json && python3 scripts/smt3d.py seo jobs/s-xyz/job.json
python3 scripts/smt3d.py drive    jobs/s-xyz/job.json
# override a default for one job: in job.json  "config": {"blog_count": 6, "languages": ["en","es","zh"], "theme": {"brand": "#1d4ed8"}}
```
The bundled example `examples/stf1003-tube-feeder/` builds and verifies as-is (`smt3d.py lp/verify examples/stf1003-tube-feeder/job.json`).

## 6. Rules that keep the output honest
- Facts only from spec sheets / manuals / PDFs; write the source in `specs.source`. When two sources conflict, the manual wins and the conflict is noted in `build/analysis.md`.
- The "A" side of a before/after duel is qualitative: no invented speeds, counts or percentages; label illustrative timing.
- No price on export pages; ROI uses the buyer's quote. Brand photos only (reject other brands' watermarks).
- Contacts: default Jason/info@ blocks; if source pages use another salesperson (e.g. Leon), ask which to use before publishing.
- Reply to Jason in Chinese; deliverables in English (other languages via i18n files).

## 7. Validation checklist
See `references/validation-checklist.md` (tick every box before delivery). `smt3d.py verify` automates the page items.

## 8. Extension and upgrades
- Extension points: `references/extension-points.md` (new section renderer, material/lighting preset, duel class, video stage, ROI formula, language).
- Upgrade paths + compatibility policy (SemVer, `config_version`, content schema migration): `references/upgrade-path.md`.
- Field lessons (render speed, sandbox resets, TTS quirks): `references/lessons.md`.
