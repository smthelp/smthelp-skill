---
name: smt-logo-looks-stickers
description: Turn a company logo STEP model into a reusable brand kit - six brand-style looks (trade-show hero, business card, email signature, social avatar + LinkedIn banner, video end-card, roll-up banner) and six animated GIF stickers (512x512 transparent, WhatsApp/Telegram size) - rendered from the real 3D logo with the Southern Machinery brand colours and Montserrat type. Use when Jason sends a logo STEP file and asks for 品牌造型, 不同造型, 动态贴纸, GIF stickers, or to make the logo work for trade shows, email, social media and video.
metadata:
  version: 1.0.0
  updated: 2026-11-14
  schema: smt-logo-looks-stickers/job@1
  entrypoint: scripts/smtlogomedia.py
  first_case: Southern Machinery logo (STEP, 2026-11-14) -> 8 looks + 6 GIF stickers
  requires: python>=3.10, numpy, numba, trimesh, cascadio, Pillow; system ffmpeg>=5
  depends_on: smt-brand-kit (brand colours, logo, circuit pattern, fonts)
  renderer_vendored_from: smt-3d-product-media 1.7.0 (scripts/smt3dlib/render.py)
---

# SMT Logo Looks + Stickers

One logo STEP in, two deliverable families out:

1. **Looks** — six static brand pieces for the occasions an export marketer
   actually uses: trade-show hero (1920x1080), business card front/back
   (1050x600), email signature (720x170), social avatar (512) + LinkedIn
   banner (1584x396), video end-card (1920x1080), roll-up banner (800x2000).
2. **GIF stickers** — six animated 512x512 transparent GIFs (spin, HELLO!,
   DEMO READY, LET'S TALK SMT, THANK YOU, SEE YOU AT THE SHOW), each under
   500 KB, ready for WhatsApp / Telegram stickers.

```
STEP ──inspect──> model.glb + parts.csv ──(job.json: brand, texts, contacts)──> looks/ + stickers/
                                                        brand-kit: colours, circuit.png, Montserrat
```

## Read first
- `references/method.md` — the pipeline: inspect, colour override, orientation, render, mark-only, compose, GIF assembly, check.
- `references/job-spec.md` — every job.json key with type, default and meaning.
- `references/troubleshooting.md` — mirrored text, swapped colours, mark fragments, cropped stickers, corrupt GIFs.
- Worked example: `examples/sm-logo/job.json` (Southern Machinery, 2026-11-14).

## Quick run
```bash
SK=<repo>/smt-logo-looks-stickers/scripts/smtlogomedia.py
python3 $SK doctor                                   # deps
python3 $SK init jobs/sm-logo --cad "Southern_Machinery_logo-SMThelp_S1.STEP" --png "Southern_Machinery_logo.png"
python3 $SK inspect jobs/sm-logo/job.json            # STEP -> GLB + parts.csv
python3 $SK all jobs/sm-logo/job.json                # looks + stickers (~1 min)
python3 $SK package                                  # skill zip for delivery
```
Edit `texts`, `contacts`, `rollup_rows` in the job for a new logo; the engine
only reads the job, never invents copy. `looks` / `stickers` in the job select
which pieces run (defaults: all).

## Hard rules
1. The logo is rendered from the real STEP model, never redrawn or traced.
   When a clean 2D logo PNG is supplied, the flat looks use it (exact
   official art); the 3D stickers still use the STEP.
   The face is never stretched; only the 1 mm extrusion is thickened (4-6x)
   so 3/4 views and spins show a solid edge — say so in the delivery.
2. STEP appearance colours are never trusted: bodies are re-coloured to the
   brand green/teal by rule (method.md step 2). If the rule is wrong for a
   file, swap the hex values in the job, never in the scripts.
3. Brand rule: the logo always sits on a white rounded card on dark
   backgrounds; never recoloured, never stretched. Colours, contacts and
   fonts come from the brand tokens, never invented.
4. GIFs are assembled only with ffmpeg palettegen/paletteuse. PIL's GIF
   writer corrupts multi-frame RGBA sequences — it is never used for output.
   Every GIF is verified with `ffprobe -count_frames` and by viewing
   first/middle/last frames.
5. Every deliverable is looked at before delivery: all looks at full size,
   3 frames per sticker on a light background (to prove transparency).
   No text may overflow its canvas; no logo may be cropped or mirrored.
6. No prices, lead times, customer names or ROI claims in any copy. Contact
   block is always the same: web · email · WhatsApp.
7. Don't edit the vendored renderer (`scripts/logo_render.py`) for one logo:
   change the job. Re-vendor it only when upstream smt-3d-product-media
   changes, and note the version in the file header.

## Upgrading
- New look or sticker -> add a function in `scripts/produce.py`, a key in
  `LOOKS` / `STICKERS`, its defaults in `config/defaults.json`, its spec in
  `references/job-spec.md`, and render the example.
- Brand change (colour, contact, font) -> `config/defaults.json` + the
  brand-kit assets; all renderers follow the job.
- Version: major = job schema change; minor = new look/sticker/output;
  patch = fixes. Add one line to the history below and sync the local
  folder with GitHub smthelp/smthelp-skill (show Jason before pushing).

## Version history
- 1.0.0 (2026-11-14) — first release from the Southern Machinery logo work:
  STEP inspect (cascadio -> GLB + parts.csv), vendored CPU renderer,
  brand colour override, mark-only extraction, 6 looks, 6 GIF stickers
  (ffmpeg assembly), doctor/init/inspect/looks/stickers/all/package CLI,
  method + job-spec + troubleshooting references, SM example job.
  Same-day v2 update: clean 2D logo PNG input for the flat looks
  (`logo_png`), corner-zone sub-line removal (`drop_zone`, SM values
  [-0.085, -0.15] remove "SMT help.com") — the skill's first real-world
  upgrade, driven by Jason's supplied PNG. Same-day fix: orientation is
  applied once in stand_upright (no axis key) after the first skill-test
  stickers rendered rotated 180° from a double transform.
