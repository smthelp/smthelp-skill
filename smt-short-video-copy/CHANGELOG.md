# Changelog — smt-short-video-copy

Format: [Keep a Changelog](https://keepachangelog.com/). Versioning: SemVer —
MAJOR = kit file format change (old kits need edits) · MINOR = new output, field, check or template · PATCH = wording/bug fixes.

## [1.0.0] — 2026-10-31
### Added
- First release, distilled from the S-JVF02 vibration stick feeder (JUKI RS-1) job delivered 2026-10-31.
- SKILL.md: triggers, scope, input list, output definition, 8-step workflow, constraints.
- Kit format: `videos.py` (META, V, PLAT, CTA, disclaimer; 10-field shot tuple) and `checklist.py` (META_FAT, SECTIONS A–K, ITEMS with basis tags M/P/G).
- `scripts/build.py`: one kit -> bilingual copy-pack DOCX (storyboard, VO, timeline subtitles, platform titles/tags, shots to film, points to confirm), CN and EN FAT checklists as separate XLSX (☐/☑ drop-downs, record columns, A4 landscape print set-up), EN + ZH SRT per video, SRT zip.
- `scripts/qa_copy.py`: gate for durations, 3-second opening, SM outro, ZH/EN pairing, never-publish terms, banned heading words, YouTube title length, tags, on-screen numbers vs META.facts, checklist basis tags.
- `scripts/fetch_sources.py` (download + text extraction + access report) and `scripts/transcribe_audio.py` (faster-whisper, numpy input to avoid the PyAV `metadata_errors` crash).
- References: method, brand rules and glossary, platform guide, FAT checklist guide, prompt snippets, source intake.
- Worked example `examples/s-jvf02/` with rendered outputs.
### Changed versus the first S-JVF02 delivery
- Copy-pack label 「开场钩子」 renamed 「开场画面 / Opening shot」 and 「统一 CTA」 renamed 「统一结尾联系方式」 to respect the banned-heading-word rule (FB-001). Content otherwise unchanged.
