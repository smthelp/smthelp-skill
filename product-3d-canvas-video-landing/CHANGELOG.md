# Changelog

All notable changes to this skill. Format: [Keep a Changelog](https://keepachangelog.com), versions: [SemVer](https://semver.org).

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
