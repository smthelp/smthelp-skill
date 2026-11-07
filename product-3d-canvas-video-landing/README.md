# product-3d-canvas-video-landing (`p3cv`) v1.2.0

Product 3D viewer + existing landing page → **interactive canvas mechanism animation inside one self-contained
landing HTML**, **4K English voice-over videos (16:9 and 9:16) with burned subtitles + SRT**, **YouTube thumbnail**,
**SEO / Shorts copy**, **VO script**, **upload to Google Drive** — driven by one `product.json`.

```
3D viewer URL ─┐            ┌─ landing page HTML (with "How it works" section)
landing URL ───┼─ p3cv ─────┼─ 16:9 4K MP4 + 9:16 4K MP4 (VO + burned subs)
product.json ──┘            ├─ thumbnail JPG · SRT · SEO txt · VO script
                            └─ Google Drive folder (or rclone / local)
```

## Contract in one minute

```bash
python3 -m p3cv info                                         # skill.json: scope, I/O, deps, versions
python3 -m p3cv run PROJ/product.json [stages] --json-out PROJ/logs/result.json
#   exit 0 ok | 2 error (envelope.error.code + hint) | 3 pending (render running: call again) | 1 env
python3 -m p3cv manifest PROJ/product.json                   # out/manifest.json with sha256
python3 -m p3cv migrate  PROJ/product.json                   # after upgrading the skill
```
Details: `docs/CONTRACT.md` (I/O), `docs/CONFIG.md` (parameters), `docs/UPGRADING.md` (versions, releases).

## Quick start

```bash
cd product-3d-canvas-video-landing
bash scripts/setup_env.sh                                   # python deps, chromium, system libs, ffmpeg
python3 -m p3cv init ~/work/juki --example juki-gripper-nozzle
python3 -m p3cv check ~/work/juki/product.json
python3 -m p3cv run   ~/work/juki/product.json download capture tts mix subtitles landing video thumbnail docs
#   -> look at ~/work/juki/r/preview/sheet_169.jpg + sheet_916.jpg, the landing page and thumbnail
python3 -m p3cv run   ~/work/juki/product.json render       # launches detached 4K workers
python3 -m p3cv status ~/work/juki/product.json             # progress per chunk
python3 -m p3cv run   ~/work/juki/product.json mux --timeout 1100   # repeat until done
python3 -m p3cv run   ~/work/juki/product.json upload
```

Run from the skill folder (or `pip install -e .` once, then use the `p3cv` command anywhere).
Smoke test without waiting 40 minutes: set `"video": {"scale": 1, "max_seconds": 3}` → renders 3 s at 1080p.

## New product in 7 steps

1. `p3cv init ~/work/<slug>` (blank template) — copies `product.json` and `anim.js`.
2. Fill `slug`, `product_name`, `brand` colours (from the landing page CSS), `sources` (3D viewers, landing pages).
3. `p3cv run … download capture` and study `src/manifest.json`, `src/*.txt`, `img/` and `img/tt/` frames.
4. Write the mechanism as 5–8 steps; implement `anim.js` (see the contract at the top of `templates/anim-template.js`).
5. Write `segments` (voice-over, with `chapter` labels), `landing.section`, `video.scenes`, `thumbnail`, `seo`.
6. `p3cv run … tts mix subtitles landing video thumbnail docs`, review previews, iterate.
7. `render` → `mux` → `upload`.

## Layout

```
SKILL.md                agent instructions (scope, I/O, workflow, fact rules) - discovery front matter
skill.json              machine-readable record (version, contract, deps, outputs)
p3cv/                   core package
  cli.py pipeline.py    CLI + runner (deps, hooks, plugins, state, events)
  config.py             product.json loading, DEFAULTS, validation, paths
  errors.py log.py      error codes + structured logging
  state.py util.py brand.py
  stages/               one module per stage (download … upload)
  adapters/             3D viewer capture: threejs.py, edrawings.py
  tts/                  voice providers: edge.py
  sinks/                delivery: gdrive_gws.py, rclone.py, local.py
  render_worker.py      detached chunk renderer
templates/              section.html (landing), video.html (scenes), thumb.html, anim-template.js
config/                 product.example.json, product.schema.json
examples/               juki-gripper-nozzle/ (product.json + jaw-anim.js), plugins/example_plugin.py
docs/                   CONTRACT, CONFIG, UPGRADING, ARCHITECTURE, EXTENDING, TROUBLESHOOTING
  p3cv/contract.py      envelope, manifest, migrate · p3cv/tools/relabel.py  photo badge edit
scripts/setup_env.sh    environment setup
tests/                  offline unit tests  (python3 -m unittest discover -s tests)
```

A project folder (PROJ, outside the skill) holds: `product.json`, `anim.js`, `src/` (downloads + manifest),
`img/` (photos, `tt/` turntable), `vo/` (mp3, timings, timeline, master.wav, cues), `build/` (generated pages),
`r/` (previews, raw captures), `out/` (deliverables), `logs/`, `state.json`.

## Versioning & contributing

- `VERSION` + `CHANGELOG.md`, SemVer. A change that needs existing product.json files to be edited is a **major** bump.
- Keep product-specific logic in product.json or a plugin (`docs/EXTENDING.md`); core stays generic.
- Before committing: `python3 -m unittest discover -s tests` and a smoke render of the example.
- Commit message: `product-3d-canvas-video-landing vX.Y.Z: <what changed>`; tag `p3cv-vX.Y.Z`.
