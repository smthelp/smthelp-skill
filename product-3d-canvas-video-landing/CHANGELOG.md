# Changelog

All notable changes to this skill. Format: [Keep a Changelog](https://keepachangelog.com), versions: [SemVer](https://semver.org).

## [1.2.0] - 2026-11-07
### Added
- `skill.json`: machine-readable record (scope, inputs, outputs, contract, dependencies, compatibility, agent loading).
- Uniform invocation contract (`docs/CONTRACT.md`, contract_version 1): `run --json-out FILE` result envelope,
  exit codes 0 ok / 2 error / 3 pending / 1 environment; `p3cv manifest` (out/manifest.json with sha256);
  `p3cv info`; `p3cv migrate` + `schema_version` (CONFIG_SCHEMA 1) with fail-fast on newer files.
- `landing.replacements` (exact-count rewrites of the base page: new model / customer variant) and
  `landing.forbid` (old-name leftovers reported).
- `video.upscale`: render 1080p, lanczos-upscale chunks to 4K in mux with low-memory x264 settings.
- `privacy.confidential` / `privacy.notes`: confidentiality block in the SEO file, `check` warning.
- `p3cv relabel`: replace the model name on a machine badge in a photo.
- `docs/UPGRADING.md` (SemVer, schema/contract rules, release steps, compatibility matrix).
- Example `s7040p-pin-insertion` (variant workflow reference + 4-head SVG inserter module).
- `tests/test_contract.py` (version agreement across VERSION / skill.json / SKILL.md / CHANGELOG, contract features).
### Changed
- mux timeout raises `E_PENDING` (was `E_RENDER`) so callers can tell "call again" from failure.
- SKILL.md rewritten as a context-free spec: scope, inputs/outputs, parameters, variant workflow, fact rules.
### Migration
- None required; v1.0/1.1 product.json files run unchanged (`p3cv migrate` only adds `schema_version`).
### Origin
- S7020 (2-head), S7040 T/P/E (4-head) and S7040P customer variant builds, Nov 2026.

## [1.1.0] - 2026-11-03
### Added
- download: `.pptx` / `.docx` sources are saved with their real extension (kind `office`) and get a text dump
  (python-pptx in presentation order when installed, slide XML otherwise); PDFs get a `pdftotext -layout` dump.
- capture: `zoom_out_steps`, `drag_at` (drag off the model so eDrawings shows no part-name tooltip; cursor is parked
  and Escape pressed after each drag), `recenter` (centre the model per frame for viewers that orbit off-centre;
  speck-tolerant bbox).
### Notes
- Found on S3010A radial inserter (eDrawings, whole machine): default zoom-in framing clipped the model.

## [1.0.0] - 2026-10-26
### Added
- `p3cv` Python package with 12 independent, resumable stages: download, capture, tts, mix, subtitles,
  landing, video, render, mux, thumbnail, docs, upload; dependency graph enforced by the pipeline runner.
- Stand-alone download module (`python -m p3cv download URL... --out DIR`) with retries, size limits,
  sha256, viewer-type detection (eDrawings / Three.js / landing / PDF), text dumps and embedded-image extraction.
- Capture adapters for Three.js viewers (drag turntable) and eDrawings exports, white-background cleanup.
- Data-driven video template with 6 scene types (hero, turntable, mechanism, cards, chips, cta), 16:9 + 9:16.
- Chunked, detached, resumable 4K render workers; mux waits, relaunches dead workers, verifies with ffprobe.
- Brand tokens (colours, logo, contacts) from config; landing section template with steps, turntable, photo, cards, CTA.
- Sinks: Google Drive via `gws` (folder reuse + size verification), rclone, local. TTS provider: edge-tts.
- Plugins (`"plugins": [...]` in product.json) to add stages / sinks / adapters / TTS without editing core.
- Structured logs (`logs/p3cv.log`, `logs/events.jsonl`), `state.json`, stable error codes with hints.
- Example: JUKI gripper nozzle SM-2070 / SM-2071 (delivered 2026-10-22), offline unit tests.
### Origin
- Generalised from the Hark project "产品 3D图转动画视频和单 html 网页" (E-cap gripper, SIR5000B rack,
  Bulk Terminal Feeder NXT, JUKI gripper nozzle; Oct 2026).
