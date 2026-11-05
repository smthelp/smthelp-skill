# Changelog

## 1.0.1 — 2026-11-05
- Fix: landing CSS defined no `--max`, so `.wrap` had no side margins on desktop (now 1200px).
- Fix: `stage` now refreshes job assets that changed since the last stage (previously kept stale copies in `_work/assets`, so video/thumbs used old images).
- New: `lp` warns when the page exceeds 2,000,000 bytes (the old SAF1001 page on file.autoinsertion.com is cut off at exactly 2 MiB).
- Added example `saf1001-axial-tape-feeder` (manual cut-and-form vs SAF1001, `AxialDuel`).

## 1.0.0 — 2026-11-05
- First release, generalised from the SBF1001 vs S-MVF01 (2026-10-21) and STF1003 tube feeder (2026-11-04) jobs.
- `smt3d.py` CLI: init, validate, fetch, analyze, mesh, lp, verify, i18n-todo, stage, tts, timeline, audio, render (resumable segments), finish, thumbs, seo, drive, all.
- Dependency-free WebGL viewer (smt3d-v1 data): rotate/zoom/reset/auto-rotate, materials industrial/matte/x-ray, lighting studio/warm/top, explode.
- Page: 7 languages (RTL Arabic), 8 blogs (enforced), ROI calculator, fit check, duel animation, dark mode, zero requests on load.
- Config: `config/defaults.json` (config_version 1) + `config/job.schema.json`; examples `stf1003-tube-feeder` (complete, builds as-is) and `bowl-vs-belt` (duel + narration).
