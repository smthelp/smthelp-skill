# Versioning, upgrades and repo sync

Semver in `VERSION` and SKILL.md `metadata.version`; brand version in `config/brand.json` (`brand_version`).
- MAJOR: incompatible content-module or project.json format (old projects need edits) - add a migration note.
- MINOR: new slide type, new shot kind, new output (e.g. 9:16 Shorts cut, other languages), brand.json change, new lint rule that can fail old content.
- PATCH: bug fixes, doc fixes, wording of defaults, new example batch.

## Release steps
1. Change code/docs; run regression on `examples/x3100-xray-counter` (lint, tts for one slug, prev, sheet; compare with a previous sheet).
2. `python3 scripts/bump_version.py patch|minor|major "what changed"` (updates VERSION, SKILL.md metadata, changelog).
3. Commit in the smthelp-skill repo: `smt-product-video-rebrand vX.Y.Z: <summary>`; tag `smt-product-video-rebrand-vX.Y.Z`; update the README table row; push.
4. Hark custom skill `smt-product-video-rebrand` points to this folder - update its version line.

## Feedback loop
Every Jason correction (wording, claim, design, title style) -> one dated rule in feedback-log.md the same day; if it changes a default, also change brand.json / templates / lint and bump.

## Planned upgrades (backlog)
- 9:16 Shorts cut from the same timeline (60 s, center crop + big subtitles).
- Multi-language voice + subtitles (es, pt, ru) via a `lang` key.
- YouTube upload as private drafts with the metadata.json (after Jason approval only).
- Automatic logo/text detection (OCR) in qc to flag supplier marks.
