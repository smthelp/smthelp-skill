# Method — how one product becomes a 10-theme short-video pack

Validated on S-JVF02 (2026-10-31). Keep this logic; change only through a versioned release.

## 1. Facts before copy
1. Read every source in full (manual > spec sheet > product page > brochure > audio/video). Build `META.facts`: value + unit + source tag.
2. When two documents disagree, do not pick silently: use the value, state the conflict in `META.conflict_note`, and add it to `META.to_confirm`.
   Example: S-JVF02 manual §3 says electrical ratings/size/weight are "not stated"; the product document gives 24 V DC, 15 W, 365 × 66 × 125 mm, 6.5 kg.
3. A required topic the sources do not document (e.g. photoelectric sensor, belt drive) is never invented: the video covers what *is* documented and carries a `note_zh/note_en` saying what it does not claim; the checklist item becomes "if fitted … else NA".

## 2. Theme set (10 themes, one point each)
Map the user's required coverage first, then fill to 10 with problem-led and how-to themes. Default S-JVF02 mapping:

| # | Theme | Required topic covered | Length | Type |
|---|---|---|---|---|
| V01 | Anatomy in 30 s | 整机外观与结构 | 30 s | Product anatomy |
| V02 | Hidden bottleneck (manual bench) | 飞达供料 | 30 s | Before/after, no ROI numbers |
| V03 | Install in N moves | 安装锁定 | 15 s | How-to |
| V04 | Assembly & fastening | 机构装配与螺丝紧固 | 45 s | Factory floor |
| V05 | Material fixing points | 供料 / 上料 | 30 s | Set-up how-to |
| V06 | Tuning the drive | 振动 / 皮带机构 | 45 s | Mechanism + tuning |
| V07 | Status & detection | 传感器与光电检测 | 30 s | Status & checks |
| V08 | Electrical & safety | 接地、绝缘、急停 | 45 s | Quality proof |
| V09 | Spec check before ordering | 型号、电压、频率、适用元件范围 | 30 s | Spec checklist |
| V10 | Factory acceptance in 60 s | 汇总 | 60 s | FAT walk-through |

For other products keep the same 10 slots and swap the mechanism words (vibration → belt, pneumatic, servo; tube → reel, tray, bowl, radial/axial tape).

## 3. Shot rules
- Shot 1 ≤ 3 s and shows the machine moving (or the problem being solved by hand). No logo, gate, aerial or PPT cover.
- One number per shot on screen, ≥ 2 s, with unit and model; only numbers in `META.facts`.
- VO sentences ≤ 15 words (EN) / ≤ 25 字 (ZH); every number said once and shown once.
- Shot sizes: 特写 CU / 近景 MCU / 中景 MS / 全景 WS. Every shot names its source (manual figure, product photo, 3D viewer screen-record, YouTube clip, or NEW 待拍).
- No faces (hands only). No customer sites without written consent.
- Last shot = SM outro (logo card + smthelp.com + WhatsApp), 3 s, one-line next step.
- Durations add exactly to 15 / 30 / 45 / 60 s.

## 4. Subtitles
- Generated from VO per shot: cue starts shot+0.1 s, ends shot−0.2 s, split at sentence/clause punctuation, ≤ 42 chars EN / ≤ 16 字 ZH per line, time shared by character count.
- EN and ZH SRT per video; also a timeline table in the DOCX.

## 5. Platform copy
See `platform-guide.md`. Per video: YouTube Shorts title (≤ 70, + #Shorts) + description + disclaimer; LinkedIn post (problem → method → product → question); TikTok/Reels one-liner; 3–5 SEO keywords; 5–8 hashtags; ZH reference text for YT title and LinkedIn post.

## 6. Factory acceptance checklist
See `fat-checklist-guide.md`. Two independent files (CN, EN), same numbering, every row quantified, 推测/Assumed marked.

## 7. Review loop
Draft → `qa_copy.py` (0 errors) → `build.py` → Jason reviews → feedback to smt-brand-kit `feedback.py` and, if it changes this method, a new version of this skill.
