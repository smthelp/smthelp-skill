---
name: smt-short-video-copy
description: Turn Southern Machinery SMT/THT product material (manual, brochure, spec sheet, product page, 3D drawings, audio/video) into a bilingual (EN source + ZH) short-video copy pack for YouTube Shorts, LinkedIn and TikTok/Reels — storyboard, voice-over, timeline subtitles/SRT, titles, SEO keywords and hashtags — plus separate Chinese and English factory acceptance (FAT) checklists. Use when Jason asks for 短视频文案, 分镜脚本, 口播稿, 字幕, 视频标题标签, Shorts/LinkedIn/TikTok copy, or 出厂验收检查表 for an SMT/THT machine, feeder or accessory.
version: 1.0.0
metadata:
  updated: 2026-10-31
  first_product: S-JVF02 vibration stick feeder for JUKI RS-1
  depends_on: smt-brand-kit (brand voice, never-publish list, feedback log), smthelp-video-script (shot rules), b2b-short-video (one point per video)
  changelog: CHANGELOG.md
---

# SMT/THT short-video copy pack (+ FAT checklist)

One product = one kit folder with two data files. Facts and copy are written once; `scripts/build.py` renders every output; `scripts/qa_copy.py` gates it.

```
sources/ --fetch_sources.py / transcribe_audio.py--> facts (META.facts)
  -> videos.py (10 themes, shots, VO, platform copy) + checklist.py (FAT rows)
  -> qa_copy.py (0 errors) -> build.py -> out/ (DOCX + 2 XLSX + SRT zip) -> Jason review -> feedback
```

## 1. Triggers (call automatically when)
- Jason sends SMT/THT product material or links and asks for short-video copy, a storyboard, voice-over, subtitles/SRT, video titles, tags or hashtags.
- He names YouTube Shorts, LinkedIn video, TikTok, Instagram Reels, 视频号 or "N 个主题的视频文案".
- He asks for a 出厂验收检查表 / FAT checklist together with (or derived from) the same product material.
- Not for: a rendered MP4 (hand the approved kit to smt-brand-kit `make_video.py`), landing pages (smt-product-landing-page), long-form YouTube scripts (smthelp-video-script).

## 2. Scope
SMT/THT equipment, feeders and accessories sold by Southern Machinery (pick-and-place feeders, stick/tube, bowl, belt, radial/axial feeders, insertion machines, separators, conveyors, ovens/wave, spare parts). Export marketing; English is the source language, Chinese mirrors it 1:1; other languages only on request.

## 3. Inputs
| Field | Format | Required |
|---|---|---|
| Product / SM model | text, e.g. `S-JVF02` | required |
| Source material | URLs or files: manual PDF, spec sheet, brochure, product page HTML, 3D HTML, audio WAV/MP3, video MP4/YouTube | required (≥ 1 spec source) |
| Host machine / compatibility | text, e.g. `JUKI RS-1` | required if the product mounts on a third-party machine |
| Number of themes | integer, default 10 | optional |
| Required coverage topics | list (e.g. 外观结构, 装配紧固, 供料机构, 传感器, 电气安全, 规格核对) | optional — default = the 10-slot map in `references/method.md` |
| Platforms | YouTube Shorts / LinkedIn / TikTok / Reels | optional — default all three |
| Languages | EN + ZH default; ES/PT/FR/DE/VI on request | optional |
| Lengths | 15 / 30 / 45 / 60 s | optional — mix by theme |
| FAT checklist | yes/no; CN and EN as separate files | optional — default yes |
| Next-step offer | e.g. free sample test | optional — "free" only if Jason confirms |

Ask Jason only what the documents cannot answer (offer wording, which options he sells, conflicting values). One short message, at most two questions.

## 4. Outputs
1. **Copy pack DOCX** `<MODEL>_短视频文案包_<n>主题_CN-EN.docx` (A4 landscape):
   sources & access table (incl. links that could not be opened), skills applied, platform tone table, theme overview, then per video:
   - header: theme ZH/EN, length, 9:16, type, audience, opening shot, notes on what it does not claim
   - **A. Storyboard**: 镜号 · time/duration · 景别 (CU/MCU/MS/WS) · visual ZH/EN · on-screen text ZH/EN · VO point ZH/EN · media source
   - **B. Voice-over**: full EN and full ZH script (EN ≤ 15 words per sentence)
   - **C. Subtitles**: EN and ZH timeline table (≤ 42 chars EN / ≤ 16 字 ZH per line)
   - **D. Titles & tags**: YouTube Shorts (title ≤ 70 chars + #Shorts, description, contact, non-affiliation line), LinkedIn post (+ ZH), TikTok/Reels one-liner, 3–5 SEO keywords, 5–8 hashtags
   - closing: shots to film list, points to confirm before publishing
2. **SRT**: `V01_EN.srt`, `V01_ZH.srt` … zipped as `<MODEL>_SRT_字幕.zip`.
3. **FAT checklists**: `<MODEL>_出厂验收检查表_中文.xlsx` and `<MODEL>_Factory_Acceptance_Checklist_EN.xlsx`, identical numbering, sections A–K, quantified criteria, ☐/☑ drop-downs, record columns, 推测/Assumed marking, print-ready.

Style: SM engineering voice — shop-floor scenes, real numbers with units, no hype adjectives; problem → method → product; one point per video; first shot ≤ 3 s with the machine moving; SM outro last. Full rules: `references/brand-rules.md`, `references/platform-guide.md`.

## 5. Steps
1. **Kit**: `mkdir -p <kit>` and copy `templates/kit/videos.py` and `templates/kit/checklist.py` into it.
2. **Sources**: `python3 scripts/fetch_sources.py <kit> <url> …` → `sources/` + `access_report.md`. Transcribe audio/video speech with `python3 scripts/transcribe_audio.py <file>`. Read every source in full (`references/source-intake.md`). Record unreachable links.
3. **Facts**: fill `META.facts` (value + unit + source tag) and `META.conflict_note` / `META.to_confirm` (`references/method.md` §1).
4. **Themes**: map required topics to the 10 slots (`references/method.md` §2); fill `META.coverage`.
5. **Write** `V` and `PLAT` in `videos.py` (shot rules `references/method.md` §3, snippets `references/prompt-snippets.md`). EN first, then ZH 1:1 using the glossary in `references/brand-rules.md`.
6. **Checklist**: write `checklist.py` from `references/fat-checklist-guide.md`; documented values first, general practice tagged G.
7. **Gate + render**: `python3 scripts/qa_copy.py <kit>` (must exit 0, read WARNs) → `python3 scripts/build.py <kit>` → open the DOCX/XLSX once to check layout.
8. **Deliver** to Jason: DOCX, two XLSX, SRT zip; in the message say which links opened, which values conflict, what is marked 推测. Nothing is published before his OK. Remarks → smt-brand-kit `feedback.py`; method changes → new version of this skill (CHANGELOG).

Worked example with all fields and rendered outputs: `examples/s-jvf02/` (`python3 scripts/build.py examples/s-jvf02`).

## 6. Constraints
- Every on-screen number is in `META.facts` with unit and model, conditions kept; calculated values say "calculated"; unknown → not shown.
- Never publish: price, discount, lead time, stock, warranty, payment terms, customer names, unbacked certificates, saving/yield/ROI %, competitor names, supplier names/logos/model codes/contacts.
- A required topic the sources do not document is not invented: the video states only what is documented and carries a note; the checklist row reads "if fitted … else NA".
- Third-party brands and models (JUKI, RS-1 …) and SM identifiers (S-JVF02, smt-brand-kit …) stay verbatim, never translated; non-affiliation line on YouTube/LinkedIn.
- Headings/titles/labels never contain hook, diagnosis, framework, vehicle, loop, CTA (钩子, 诊断, 框架, 载体, 循环, 行动号召).
- ZH and EN are 1:1 everywhere (same shots, same rows, same numbering); glossary terms fixed (飞达 = Feeder, 振动 = Vibration, 供料 = Feeding …).
- No faces in footage (hands only); customer sites only with written consent.
- Draft only: no upload, post or send without Jason's explicit approval.

## 7. Files
| Path | Role |
|---|---|
| `SKILL.md` | this guide |
| `VERSION` | current version (SemVer) |
| `CHANGELOG.md` | release history |
| `references/method.md` | the validated method: facts, 10-slot theme map, shot, subtitle, platform, FAT, review rules |
| `references/brand-rules.md` | naming, never-publish list, evidence tags, banned words, contact block, ZH↔EN glossary |
| `references/platform-guide.md` | per-platform tone, format, title/text rules, SEO pattern, hashtag bank, next-step line |
| `references/fat-checklist-guide.md` | checklist files, columns, sections A–K with thresholds and basis tags |
| `references/prompt-snippets.md` | reusable prompts for reading, planning, drafting, self-check |
| `references/source-intake.md` | how to read each source type; what to do when a link fails |
| `templates/kit/videos.py` | blank kit: META, CTA, disclaimer, OUTRO, V, PLAT with field comments |
| `templates/kit/checklist.py` | blank kit: META_FAT, standard sections A–K, ITEMS row format |
| `scripts/fetch_sources.py` | download links, extract HTML text, write access report |
| `scripts/transcribe_audio.py` | timestamped transcript of audio/video (faster-whisper) |
| `scripts/qa_copy.py` | quality gate (exit 1 on error) |
| `scripts/build.py` | renderer: DOCX copy pack, CN + EN XLSX, SRT + zip |
| `examples/s-jvf02/` | full worked kit + rendered outputs (v1.0.0 reference quality) |

Dependencies: `pip install python-docx openpyxl` (render); `faster-whisper` + ffmpeg (transcription only); Noto Sans SC or YaHei font for viewing.

## 8. Upgrading
- Bump `VERSION`, the `version:` line above and add a CHANGELOG entry. MAJOR = kit format change; MINOR = new output/field/check/template; PATCH = wording or bug fix.
- Re-run `scripts/qa_copy.py examples/s-jvf02` and `scripts/build.py examples/s-jvf02` after every change; the example must stay at 0 errors.
- Sync: repo `smthelp/smthelp-skill`, folder `smt-short-video-copy/`, commit as "Hark (smthelp002)", never force-push.
