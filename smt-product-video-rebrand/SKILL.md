---
name: smt-product-video-rebrand
description: Turn raw supplier / factory product demo clips (phone videos, Chinese UI, supplier logos, people in frame) into Southern Machinery branded English marketing videos for YouTube - 16:9 4K, English voice-over, burned-in subtitles + .srt, generated music, branded motion-graphic slides, 1280x720 thumbnail, SEO title / description / chapters / tags, and a copy Google Doc - one video per marketing theme, delivered to Google Drive (never auto-published). Use when Jason says 把产品视频做成营销视频/品牌化视频/YouTube 视频/再做 N 条视频/按主题做视频/视频二次创作, gives a Drive folder of product clips plus topics or titles, or asks for more videos of a product already done (add a batch).
metadata:
  version: 1.0.0
  updated: 2026-10-24
  brand_version: SM-VIDEO-2026-10
  first_case: Smart EMS X3100 X-ray SMD counter - batch1 7 videos, batch2 10 videos (Oct 2026)
  requires: python3, ffmpeg with libass, numpy, Pillow, edge-tts (scripts/setup.sh); gws CLI with a Google credential for Drive I/O
---

# SMT Product Video Rebrand

Raw product clips + a list of themes -> one branded English YouTube video per theme, plus its SEO copy.
The engine never invents layout, colour or contact data (config/brand.json); it never invents facts
(every claim must be in the project's `content/facts.md`).

```
Drive clips ──download──> <project>/source/ ──catalog.sh──> contact sheets ──> content/shots.py (clean shot library)
product page / brochure ─────────────────────────────────> content/facts.md (approved / example-only / not-allowed)
themes + titles from Jason ──────────────────────────────> content/<batch>.py (VIDEOS scenes + SLIDES + SEO)
                                   run.sh lint ─> tts ─> prev ─> sheet (LOOK) ─> fix ─> 4k ─> qc (LOOK) ─> thumbs ─> meta
                                   upload.py ─> Drive folder (mp4 + srt + thumbnail) + copy Google Doc ─> report to Jason
```

## 1. When to use / boundaries
Use for: product promo, explainer, use-case, comparison, FAQ, "how to choose", ROI-style videos of 1-3 min built from existing demo footage of one Southern Machinery product (any SMT/THT machine or accessory).
Do not use for: talking-head or presenter videos; footage that must be newly filmed; CAD/3D animation (use `cad3d-animation-video-landing`); vertical Shorts as the main output (use `b2b-short-video`; a 9:16 cut is a future extension, see references/versioning.md); publishing to YouTube (separate step, only after Jason approves - `smthelp-video-to-youtube`).
Stop and ask Jason when: no usable clean footage for a theme (> 60 % of screen time would be slides); a theme needs a claim not in facts.md (offer a hedged phrasing - never invent numbers, standards, AI features, customer cases or savings); the product's Southern Machinery model name is unknown.

## 2. Inputs (full spec: references/input-spec.md)
Required
- **Product source material**: Drive folder or files of demo clips (any orientation, 720p+), plus the official facts source (landing page URL, brochure or spec sheet).
- **Themes**: N topics, each = one video; optional suggested English title per topic.
Optional
- Brand preferences: CTA wording, outro headline, landing page / UTM, accent colours or logo (`brand_overrides`), voice, mirrored layout, music per video.
- Allowed / forbidden claim list beyond facts.md; target length; Drive output folder (default: the source folder).

## 3. Outputs (full spec: references/output-spec.md)
Per video, in `final/<batch>/` and uploaded to Drive:
- `<prefix>-<slug>-4k.mp4` - 3840x2160, 30 fps, H.264 yuv420p CRF 20 + AAC 192k 48 kHz, 60-180 s, -15 LUFS, burned-in English subtitles.
- `<prefix>-<slug>-4k.srt` - same cues as the burned subtitles.
- `<prefix>-<slug>-thumbnail.png` - 1280x720.
Per batch: `metadata.json` + one Google Doc "<Model> YouTube Video Copy - <batch>" with, per video: SEO title (40-70 chars), full description (keyword first line + WhatsApp CTA, summary, chapters, UTM link, contact footer, hashtags), 13-15 tags, thumbnail text, narration script; production notes and sources.
SEO and copy rules: references/output-spec.md (titles/descriptions/tags) and references/design-copy-standard.md (screen design, callouts, narration, claims).

## 4. Run
```bash
SK=<repo>/smt-product-video-rebrand/scripts
bash $SK/setup.sh                                   # after any sandbox reset
python3 $SK/new_project.py /workspace/work/<product>-videos --model X3100 --name "X-ray SMD component counter" --prefix x3100-x-ray-smd-counter
# copy clips to <project>/source/ ; bash $SK/catalog.sh <project>/source/<clip>.mp4 ; LOOK at every sheet
# write content/facts.md, content/shots.py, content/batch1.py   (references/method.md steps 2-5)
export SMV_PROJECT=/workspace/work/<product>-videos SMV_BATCH=batch1
$SK/run.sh lint && $SK/run.sh tts && $SK/run.sh prev && $SK/run.sh sheet     # LOOK at each sheet, fix, repeat
$SK/run.sh 4k <slug>          # background job, 1-2 at a time, ~7 min each; keep the session alive
$SK/run.sh qc <slug>          # PASS + LOOK at the 12-frame sheet (logos? faces? title bars? cut text?)
$SK/run.sh thumbs && $SK/run.sh meta
python3 $SK/smv/upload.py <drive_folder_id> && python3 $SK/smv/upload.py <drive_folder_id> --doc
```
Worked example (all 17 X3100 videos): `examples/x3100-xray-counter/` (project.json, facts, shot library, batch1 + batch2 content, custom slides).

## 5. Hard rules
1. Facts only from `content/facts.md`. Example numbers are labelled "example" on screen and in narration; brochure accuracy figures say "brochure example - test with your own parts". No AI / zero-programming / guarantee / "replaces X" claims unless facts.md says so (lint enforces `forbidden_claims`).
2. Brand: Southern Machinery logo, colours, fonts, footer (WhatsApp +86 136 0256 2576 · smthelp.com) and outro card come from config/brand.json. Never show supplier logos, supplier model numbers, software title bars, watermarks, large Chinese UI/subtitles, or faces/bodies (hands only) - blur, crop, zoom or drop the shot.
3. Every video: intro card (4 s) -> 5-9 scenes (each = narration + footage/slide window + callout card + optional chapter) -> outro CTA card; 60-180 s.
4. Vary a batch: different shot order/crops, `mirror` on about half, own intro still, music progression and slide designs per video; no shot more than twice in one video.
5. Gates before delivery: lint passes; every preview sheet and every 4K QC sheet was looked at; ffprobe PASS; meta passes the SEO checks.
6. Deliver to Drive only. Never publish to YouTube, never overwrite or delete source clips; replace a delivered file in place (`upload.py --replace`) so links stay valid.
7. Report to Jason: table of slug, title, duration, Drive link; the Doc link; every compromise (claims softened, footage gaps, residual marks).

## 6. Upgrade and maintenance
- Read `references/feedback-log.md` before every run and apply every rule; append new rules from Jason's feedback the same day.
- Versioning (semver), what counts as MAJOR/MINOR/PATCH, release steps and repo sync: `references/versioning.md`; history in `references/changelog.md`; bump with `scripts/bump_version.py`.
- Engine changes must keep `examples/x3100-xray-counter` rendering identically (regression: `run.sh lint` + one `prev` + sheet compare).
- New slide type, new shot kind or new output format = MINOR; brand.json change = MINOR with brand_version bump.

## Read first
references/method.md · references/input-spec.md · references/output-spec.md · references/design-copy-standard.md · references/shot-library.md · references/qa-checklist.md · references/error-handling.md · references/versioning.md · references/feedback-log.md
