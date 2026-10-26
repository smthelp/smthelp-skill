# Architecture

## Stage graph

```
download ──► capture ──┬──────────────► landing ──► out/<slug>-landing-page-animated.html
                       │
tts ──► mix ──► subtitles ──► video ──► render ──► mux ──► out/<basename>_16x9_4K.mp4, _9x16_4K.mp4
         │                     (previews)  (workers)  ▲
         └──────────────────────────────────────────┘ (master.wav)
         └──► docs ──► out/ SEO txt + VO script
thumbnail ──► out/youtube-thumbnail-<slug>.jpg      (needs only anim.js + config)
upload   ──► sink (gdrive | rclone | local | plugin)   (uploads whatever is in out/)
```

The runner (`p3cv/pipeline.py`) refuses to run a stage whose dependencies are not `done` in `state.json`
(error `E_STAGE_ORDER`) unless they run earlier in the same command. A full `p3cv run product.json` skips
stages already done (except render/mux); naming stages explicitly always re-runs them; `--force` re-runs all.

## Stage I/O

| Stage | Reads | Writes | Notes |
|---|---|---|---|
| download | `sources.*` URLs | `src/<id>.html|pdf`, `src/<id>.txt`, `src/manifest.json`, `img/<id>_b64_N.*` | retries, size limit, sha256, kind detection; stand-alone CLI |
| capture | manifest, drawing with `capture:true` | `img/tt/v00..vNN.png`, `r/capture/<id>/raw_*.jpg` | adapter per viewer kind; SwiftShader WebGL |
| tts | `segments[].text` | `vo/sNN.mp3`, `vo/sNN.json` (word timings) | skips unchanged segments |
| mix | `vo/sNN.mp3` | `vo/timeline.json`, `vo/master.wav` | lead-in/gap/tail, loudnorm −14 LUFS |
| subtitles | timeline, word timings | `vo/cues.json`, `out/<slug>-subtitles-en.srt` | ≤42 chars, punctuation breaks, replacements |
| landing | `src/<landing.base>.html`, anim.js, `img/tt`, photo | `out/<…>.html` | section template + brand tokens; unique marker required |
| video | timeline, cues, scenes, anim.js, `img/tt` | `build/video_built.html`, `r/preview/*.png`, `sheet_*.jpg` | JS errors fail the stage |
| render | `build/video_built.html` | `TMP/<ar>_<k>.mp4` + `.done` + `.log` | detached workers, chunked, resumable |
| mux | chunks, `master.wav` | `out/<basename>_16x9_4K.mp4`, `_9x16_4K.mp4` | waits, relaunches dead workers, ffprobe check |
| thumbnail | anim.js, `thumbnail` | `build/thumb.html`, `out/youtube-thumbnail-<slug>.jpg` | 1920×1080 |
| docs | timeline, `seo` | `out/youtube-seo-…txt`, `out/<slug>-voiceover-script-en.txt` | chapters from `segments[].chapter` |
| upload | `out/*` | sink + `out/delivery.json` | gdrive: folder reuse, skip same-size, verify |

## Module responsibilities

- `config.py` — merges `DEFAULTS` with product.json, validates required keys/scene ranges, resolves paths
  (absolute → PROJ → skill root). Nothing else reads raw JSON.
- `errors.py` — `P3VError(code, message, hint)`; codes listed there and in TROUBLESHOOTING.md.
- `log.py` — console + `logs/p3cv.log`; `logs/events.jsonl` (stage_start / stage_done / stage_fail / artifact).
- `state.py` — `state.json`: status, time, outputs, seconds, error per stage.
- `stages/*` — pure functions `run(cfg, state, **opts) -> dict`; no stage imports another stage's internals except
  shared helpers (`landing.anim_js`, `video.ensure_logo`, `render.plan`).
- `adapters/`, `tts/`, `sinks/` — registries (`ADAPTERS`, `PROVIDERS`, `SINKS`) that plugins can extend.
- `templates/` — HTML/JS with `__TOKENS__` (filled by Python) and `{{fields}}` (landing copy).

## Video page model

`templates/video.html` builds one layer per `video.scenes[i]`; a scene runs from the start of segment
`from_segment` (scene 0 from t=0) to the next scene's start, with 0.45 s cross-fades. `renderAt(t)` is a pure
function of time, so every frame is reproducible and chunks can render in parallel. `?ar=169|916` switches layout.
The mechanism scene maps voice segments to animation-cycle windows (`map: [[segment, cycle_from, cycle_to], ...]`)
so each step is shown exactly while it is narrated.
