# Invocation contract (contract_version 1)

The same steps work in any environment and any agent (Hark, Claude Code, Codex, OpenCode, Hermes, a CI job or a
person at a terminal). Nothing depends on a chat history: every input lives in the project folder, every result
is a file.

## 1. Discover
- `SKILL.md` front matter (`name`, `description`, `version`) is the discovery record for skill-aware agents.
- `skill.json` is the machine-readable record: scope, inputs, outputs, contract, dependencies, compatibility.
  `python3 -m p3cv info` prints it.

## 2. Load
- Read `SKILL.md` (workflow + fact rules). Read `docs/CONFIG.md` for parameters and this file for I/O.
- Environment: `bash scripts/setup_env.sh` (idempotent), then `python3 -m p3cv check PROJ/product.json`.
- Install anywhere: run from the skill folder (`python3 -m p3cv ...`) or `pip install -e .` and use `p3cv`.

## 3. Invoke
```
python3 -m p3cv init  PROJ [--example NAME]                      # once: product.json + anim.js
python3 -m p3cv run   PROJ/product.json [stage ...] --json-out PROJ/logs/result.json
python3 -m p3cv manifest PROJ/product.json                       # out/manifest.json
```
- PROJ = one folder per product. Stages read and write only inside PROJ (render scratch: `video.tmp_dir`).
- Stages: `download capture tts mix subtitles landing video render mux thumbnail docs upload`
  (`python3 -m p3cv stages` shows the dependency graph). No stage list = all except upload (unless `upload.auto`).
- Product A (landing page) only: `download capture landing`. Product B (videos) only:
  `download capture tts mix subtitles video render mux thumbnail docs`.
- Idempotent: re-running a finished stage is skipped unless named explicitly or `--force`. Render/mux resume.

## 4. Result envelope (stdout and `--json-out`)
```json
{"skill": "product-3d-canvas-video-landing", "version": "1.3.0", "config_schema": 1,
 "status": "ok | pending | error", "exit_code": 0, "project": "/abs/PROJ", "at": "2026-11-07T15:00:00+0800",
 "stages": {"landing": {"html": "out/x-landing-page-animated.html", "kb": 2068, "nav_links": 1, "leftovers": []}},
 "error": null}
```
| exit | status | meaning | caller does |
|---|---|---|---|
| 0 | ok | all requested stages finished | read `stages`, run `manifest` |
| 2 | error | `error.code` from `p3cv/errors.py` with `hint` | fix per hint / docs/TROUBLESHOOTING.md |
| 3 | pending | `E_PENDING`: 4K render still running | call the same `run ... mux --timeout 1100` again |
| 1 | - | bad arguments / missing tool | `scripts/setup_env.sh`, `p3cv check` |

## 5. Deliverables (`PROJ/out`, see skill.json `outputs`)
`<slug>-landing-page-animated.html` · `<basename>_16x9_4K.mp4` · `<basename>_9x16_4K.mp4` ·
`youtube-thumbnail-<slug>.jpg` · `youtube-seo-title-description-<slug>.txt` · `<slug>-subtitles-en.srt` ·
`<slug>-voiceover-script-en.txt` · `manifest.json` · `delivery.json` (after upload).
`manifest.json` lists every file with kind, bytes and sha256 and `missing` kinds; exit 3 when something is missing.

## 6. Side effects
Only `upload` writes outside PROJ (Drive/rclone/local sink). Nothing is published to YouTube or a website.
Uploading, publishing and sending stay explicit user requests (repo `AGENTS.md`).

## 7. Stability promise
Within contract_version 1: command names, stage names, envelope keys, exit codes and output file patterns do not
change. New keys may be added. A breaking change raises `contract_version` and the skill's MAJOR version.
