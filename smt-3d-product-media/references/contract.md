# Calling contract (stable within major version 1)

Any agent (Hark, Claude Code, Codex, Cursor, a person in a shell) uses the skill the same way:

```
python3 <repo>/smt-3d-product-media/scripts/smt3dmedia.py <command> <job.json> [--set key.path=JSON]... [options]
```

## Discovery
- Repo root `README.md` (技能清单 table) lists every skill; this skill`s row is kept current by `tools/publish_to_repo.sh`.
- Each skill folder has `SKILL.md` (front-matter `name`, `description`, `metadata.version`) and `skill.json` (machine-readable manifest). `VERSION` holds the semver.
- `python3 scripts/smt3dmedia.py --version` prints the installed version; `doctor` checks the environment.

## Input (one file)
`job.json`, schema `smt-3d-product-media/job@1` (see job-spec.md). All relative paths resolve against the job file's folder, so a job folder is self-contained and portable:
```
jobs/<MODEL>/
  job.json
  inputs/<model>.STEP            CAD (STEP AP214 with colours; Parasolid .x_t / native CAD must be exported to STEP first)
  inputs/real/*.mp4              optional real footage
  inputs/deck_assets/            optional photos for the deck (file names used by the deck spec)
  deck/spec-en.json, spec-zh.json   optional deck specs (smt-product-ppt-rebrand format, may use {video} {poster} {still:x} {model})
```
Values in `config/defaults.json` fill anything the job leaves out.

## Commands
| command | needs | writes | notes |
|---|---|---|---|
| doctor | - | - | exit 1 if a dependency is missing |
| init `<dir> --cad F --model M` | CAD | `<dir>/job.json` | copies the S7040P example as a starting point |
| check | job | - | schema + file checks only |
| inspect | CAD | `out/work/model.glb`, `out/work/parts.csv` | prints part count, bbox, group sizes |
| preview `[--t s ...]` | inspect | `out/work/preview.jpg` | 3 frames per row |
| render `[--workers N]` or `--worker i --of N` `[--limit K]` | scene | `out/work/frames3d/f00000.jpg...` | resumable; skips existing frames |
| stills | scene | `out/stills/<name>.jpg` | from `job.stills` |
| real | real_clips | `out/work/real/r<k>/f*.jpg` | fit `cover`, `blur_pad` or `auto` |
| voice | voice.enabled | `out/work/voice_<lang>.m4a` | edge-tts; cached per line (text+voice) |
| compose | render (+real, +voice) | `out/video/<name>-<LANG>.mp4` | captions + sequence + audio |
| deck | compose, deck.enabled | `out/deck/<slug>-Product-Presentation-<LANG>-Southern-Machinery.pptx` | via smt-product-ppt-rebrand |
| publish | gws CLI, publish.drive_folder | Drive files | prints file ids |
| all | job | everything above except publish | |

## Output (fixed layout under `output.dir`, default `out/`)
```
out/video/<slug>-<video_variant>-<LANG>.mp4     H.264 + AAC, 1280x720 default, faststart
out/deck/<slug>-Product-Presentation-<LANG>-Southern-Machinery.pptx (+ .qa.json, build-log.json from the builder)
out/stills/<name>.jpg
out/manifest.json        skill version, schema, CAD sha1, per-stage time and result (traceability)
out/work/                intermediates (frames, glb, parts.csv, captions, voice) - cache, safe to delete
```
File names: `output.name_pattern` (default `{slug}-{variant}-{LANG}`), slug = `product.seo_slug`.

## Exit codes and messages
`0` ok, `2` invalid input (job, CAD, environment), `3` a stage failed. Error lines start with a code (J.. job, C.. CAD, R.. render, M.. media, V.. voice, D.. deck, P.. publish); see troubleshooting.md. Warnings start with `WARN` and do not stop the run.
The **last stdout line is one JSON object** an agent can parse: `{"ok": true|false, "command": "...", "skill_version": "1.2.0", "results": {stage: ...}, "errors": [...], "manifest": "out/manifest.json"}`.

## Guarantees
- Same job + same skill version -> same frames (deterministic renderer, no randomness).
- New minor versions only add optional keys; a job@1 file keeps working through all 1.x releases.

### props.pcb.cad (1.3.0)
`{"file": "inputs/board.STEP|.glb", "array": [nx, ny], "gap": 0.004, "board_color": [r,g,b], "rot_deg": 0, "flip": false, "insert": [{"groups": ["NAUO18"], "head": "1"}], "absent": []}` — see smt3dlib/pcbcad.py docstring.

### props.feeder_cad (1.4.0)
`{"models": {"key": {"file": "inputs/feeder.STEP|.glb", "fwd": "-x", "up": "z", "color": [r,g,b], "max_body_faces": 20000, "min_body": 0.004}}, "items": [{"model": "key", "out": [x, y_outlet, z_top], "vib": 0.0004}], "hide_bowls": true}` - see smt3dlib/feedercad.py docstring.

### tools/align_feeder_cad.py (1.7.0)
Multi-bowl feeder carts (one STEP with several bowls + linear tracks) aligned so every track outlet sits at its head's pick-up point. `python3 tools/align_feeder_cad.py config.json` -> one world-placed GLB (machine coords) + JSON with each head's `junction`, `seat`, `yaw_deg`, the GLB `bbox` and the `out` point for props.feeder_cad. Config keys: `cad`, `axes` {lateral, up, fwd}, `tracks` {name: lateral coord}, `seat_fwd`, `junction_fwd`, `seat_top_up`, `pick` [y, z], `shared_keywords`, `drop_keywords`, `colors`/`color_keywords`, `carts` [{mirror, targets {track: head_x}, heads {track: "H1"}, fill [{center, r, floor_up, shape pin|clip, d, L, color}]}], `out_glb`, `out_json`. Example: examples/feeder_align/vbf_x2_s7040p.json. Warns when a track yaw exceeds 5 deg.
