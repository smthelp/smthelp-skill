# Upgrade paths and compatibility policy

## Versioning
- Skill version: SemVer in `VERSION`, `SKILL.md` front matter, `config/defaults.json.skill_version` and the page `<meta name="generator">`.
  - PATCH: fixes, copy, styling — no file or key changes.
  - MINOR: new optional keys/sections/presets/commands; old jobs build unchanged.
  - MAJOR: a key renamed/removed or a data format changed; bump `config_version` and ship a migration note in `CHANGELOG.md`.
- `config_version` (defaults.json) = job/config contract version (now 1). `validate` will warn when a job targets another version.
- 3D data format id `smt3d-v1` is versioned separately; the viewer must keep reading every older `smt3d-vN`.
- Every release: update `CHANGELOG.md`, run `smt3d.py lp` + `verify` on `examples/stf1003-tube-feeder`, zip, push to `smthelp/smthelp-skill`.

## Adding a language (MINOR)
1. Add the code to `config.languages` and its native name to `language_labels` (RTL → `rtl_languages`).
2. `smt3d.py i18n-todo <job> <code>` → translate → `i18n/<code>.json`.
3. Add UI keys (`ui.*`) for the new code to the example so the skill ships translated controls. Missing keys fall back to English, so older jobs never break.

## Adding a page template (MINOR)
1. New renderer `s_<name>()` in `build_lp.py` (or a template file under `templates/landing/` loaded by it).
2. Content keys optional; absent content → section returns `''` (old jobs unaffected).
3. Add to `sections` default only in a MINOR release and note it in the changelog; job-level `sections` lists keep their order.
4. For a different whole-page layout, add `templates/landing/<layout>/` and a `config.layout` key (default `standard`), never change the default layout's markup ids (`#v3d`, `#duelRoot`, `#roi_*`, `#lang`) — verify relies on them.

## Adding 3D interaction (MINOR unless the data format changes)
- New controls (section cut, hotspots, part list, measure) go into the viewer API as new methods; default off, enabled by new `model.*` keys.
- Data needs (part names, hotspot anchors) go into new optional fields of `smt3d-v1`; a breaking layout change becomes `smt3d-v2` with the viewer reading both.
- Planned: `viewer_mode: turntable` (image sequence fallback for drawings without extractable meshes), section plane, hotspot callouts synced to duel chapters, GLB/Draco input.

## Compatibility guarantees
- A job that built with 1.x builds with any later 1.y.
- Pages produced by older versions stay standalone (nothing is loaded from the skill at runtime).
- The CLI keeps command names; new commands are additive.
