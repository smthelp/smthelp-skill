---
name: cad3d-animation-video-landing
description: Turn a product 3D drawing (SolidWorks eDrawings / HOOPS HTML export, or STEP/GLB) into (1) a real-time interactive mechanism animation merged into an existing product landing page as ONE new single HTML file, (2) 1–3 min 4K YouTube marketing videos in 16:9 and 9:16 Shorts with English voice-over and word-synced subtitles, (3) a YouTube thumbnail, and (4) SEO title, description, chapters and tags. Use for Southern Machinery SMT/THT nozzles, grippers, feeders and machine modules when the user asks to "把 3D 图做成动画/视频/落地页", "explain how this works", or "make a product video from the 3D drawing".
version: 2.1.0
---

# CAD 3D → Mechanism Animation, 4K Videos & Single-HTML Landing Page (v2.1.0)

> Module layout, I/O spec, config parameters and versioning rules: `README.md`, `docs/`, `config/`, `CHANGELOG.md`.
> New projects: put `product.json` (from `config/product.example.json`) in PROJ and drive stages with `scripts/pipeline.sh`.
> Start product-specific code from the closest `examples/<code>/` (cn-sm-2713 = small kinematic part; sbf1001 = large process machine; saf1001 = named multi-part mechanism with slow-mo; sir-rack = static structure + workflow story with instanced slots/LEDs).

把产品 3D 图转化为：交互式机构动画（并入现有 Landing Page，输出全新单 HTML）+ 16:9 / 9:16 4K 英文配音字幕营销视频 + 缩略图 + YouTube SEO 文案。

Reference implementation: `examples/cn-sm-2713/` (JUKI customized coil gripper nozzle, delivered 2026-10-19).
All scripts live in `scripts/`; copy them into `<PROJ>/build/` for a new product. Every script resolves paths from
`PROJ` (env var, default = parent of the script folder). Project layout:

```
PROJ/
  src/          drawing.html (3D export), landing.html (existing page), mesh.json, tree.json
  build/        scripts + node_modules (three, esbuild) + fonts/ + logo.png + audio/
  env/          venv + chromium + extra .so libs (persistent; created by setup_env.sh)
  frames_l/ frames_p/   rendered 4K JPEG frames (resumable)
  enc/          encoded segments
  deliverables/ final HTML, MP4s, thumbnail, SRTs, SEO txt
```

## When to use / not use
- Use: one product (or module) with a 3D drawing and a mechanism worth explaining; output is marketing.
- Not for: photo-only products (use `smt-brand-kit` / `html-video-product-promo`), whole-line layouts
  (use `build-3d-html-viewer` with layout grid), or when only a static 3D viewer page is wanted
  (`build-fast-3d-html-viewer` is faster).
- Do NOT invent specs. Follow repo `AGENTS.md` evidence rules: only claims the CAD shows, the existing landing page
  states (e.g. 7-day tooling, since 2011, JUKI JM/KE compatibility), or the user confirms. Visual emphasis colors
  (amber contact pins) are not materials — say so to the user.

## Inputs (ask only what is missing)
1. 3D drawing URL/file (eDrawings HTML, STEP, GLB). 2. Existing landing page URL/file to merge into.
3. Target component / application if not in the CAD. 4. Voice-over language (default English), channel (default
   youtube.com/c/Smthelping). Pick everything else yourself and state the assumptions.

## Workflow

### Phase 0 — Environment (5 min)
`bash scripts/setup_env.sh` → venv with playwright **1.47.0** (newer versions have no linux-arm64 Chromium),
Chromium 1134, and missing GTK/ATK libs extracted from Debian debs into `env/libs`. Everything sits under `PROJ`
because sandbox `/tmp` and `$HOME` can be wiped between turns (symptom: exit code 127).
`cd build && npm i three@0.169.0 esbuild`. Fonts: download Inter + JetBrains Mono woff2 (Google Fonts CSS, latin subset)
into `build/fonts/`. Logo: `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`.

### Phase 1 — Understand the mechanism (most important; 20–40 min)
1. `curl` both pages into `src/`. The eDrawings file embeds the model as base64 `modelContents` (HOOPS SCS, zstd) —
   do not try to parse it; drive the viewer instead.
2. `extract_mesh.py src/drawing.html src/` → `tree.json`, `mesh.json`, screenshot. Part names are file names
   (`E3681729000.stp` = JUKI OEM nozzle body, `39.03.556` jaws…). Bodies throwing "no mesh data" are markup/empty.
3. Compute world bounding boxes (mm) per part (numpy, apply column-major net matrix ×1000), render coloured analysis
   views (front, side, bottom, half-section with a clipping plane) with a throwaway Three.js page, and READ the images.
4. Write down the kinematic chain explicitly: driver → linkage → output, pivot centres (from pin bboxes), stroke,
   which parts move together, what is static, open/close direction (verify with a rotation sign check), contact points,
   datum surfaces. Identical part numbers used in several places usually mean standard parts (set screws, pins, E-clips).
5. Turn each mechanical fact into a selling point (feature → advantage → benefit). Record it in the project skill.

### Phase 2 — Shared 3D engine
- `pack.py`: name each body (dict id→name), world-transform to mm, int16-quantize positions, int8 normals, dedupe,
  per-part index buffers, gzip+base64 → `model.b64` (~1 MB for 100k tris). Split sub-meshes when needed (e.g. coil
  body vs leads by triangle centroid).
- `loader.js` decodes with native `DecompressionStream`. `engine.js` builds the scene: PBR materials + RoomEnvironment,
  hierarchy groups for kinematics (plunger group translates, jaw groups rotate about pivot), `apply(state)` with
  `open`, `explode` (per-part offset table), `cut` (local clipping plane + BackSide teal cap material for section faces),
  `highlight` (emissive pulse), `rigPos`/`coilAttached` for pick-and-place, props (tray, PCB). `ANCHORS` = 3D points
  for callouts. **Adapt per product:** part→material map, parent groups, pivot constants, stroke, EXPLODE table, ANCHORS, props.

### Phase 3 — Voice-over script & TTS
- 8–9 scenes, ~230 words, 95–115 s total: hook (pain) → title → plug&play/interface → mechanism (cutaway) →
  key feature 1 (e.g. 3-point grip) → feature 2 (datum/stop) → build quality (exploded) → real cycle (pick & insert)
  → CTA (brand, 7-day tooling, smthelp.com, subscribe).
- `vo.json` → `tts.py` (edge-tts, voice `en-US-AndrewMultilingualNeural`, rate +2%, WordBoundary timings →
  `audio/vo_timing.json`). edge-tts must run with proxy env vars deleted and `proxy=None` (the sandbox proxy URL breaks aiohttp).
- Write numbers TTS-friendly ("eight-point-five millimeter") and map them back for captions in `video.js`.

### Phase 4 — Video timeline (`video.js`)
- Scene start = previous end; VO starts 0.4 s into each scene; scene length = VO + 1.25 s (CTA +4.6 s end card).
- Choreography is keyed to spoken words (`wordT(scene,'down')`) so motion lands on the narration.
- Camera continuity: each scene's first camera key equals the previous scene's last key; insert a 0.3 s dip-to-black
  only where objects teleport (cycle start, CTA start).
- Layout: 16:9 product on the right third (view offset `sx=0.17, sy=-0.045`), text block left; 9:16 distance ×1.32,
  product centred lower (`sy=0.09…0.15`), text on top, captions at 79.5 % height (93 % during CTA).
- Overlays (2D canvas, logical 1920×1080 / 1080×1920 scaled ×2): brand pill, kicker + headline + sub, spec chips,
  callouts with leader lines anchored to projected 3D points, motion arrows, contact triangle, word-highlighted
  captions (chunk ≤40 chars landscape / ≤26 portrait, break at punctuation; show chunk only in [a,b) to avoid overlap).
- Preview before rendering: `preview.py l|p t1,t2,... 0.5` → contact sheets; fix overlaps (text vs product,
  callouts vs each other, captions vs leads) in both aspects.

### Phase 5 — Render 4K (the long pole)
- `run_render.sh l|p [budget_s]` → `render.py` (resumable; skips existing frames; stop before the 1200 s background
  limit and relaunch). Uses the GL-composite path (`enableGLComposite`): background baked into `scene.background`,
  overlay canvas uploaded as one texture and drawn on a full-screen quad, frame read with `glCanvas.toDataURL`.
- Measured on 2 vCPU arm64 SwiftShader: ~1.7–2.5 s per 4K frame with MSAA. 113 s @ 24 fps = 2,706 frames per
  aspect ≈ 75–90 min each. **Run ONE renderer at a time** (two in parallel were ~2× slower in total).
  Tell the user the ETA up front; deliver HTML/thumbnail/SEO first in an update.
- Don'ts that cost hours: drawing a 4K cached canvas into another 2D canvas (2 s/frame!), 30 fps without need,
  `pkill -f render.py` typed in the same shell command (kills your own shell; use `pkill -f "render[.]py"`).
- `encode.py l|p i 4` (x264 faster CRF17, 4 segments) then `encode.py l|p final` (concat + AAC 320k, faststart
  written to /tmp then copied — faststart directly on the network FS fails with "Error writing trailer").

### Phase 6 — Audio, captions, thumbnail, SEO
- `audio_mix.py`: VO clips delayed to scene `voStart`, loudnorm −16 LUFS, synthesized pad/pluck music bed, sidechain-ducked.
- `make_srt.py <CODE>` → SRTs per aspect (captions are also burned in; SRT is for YouTube CC/SEO).
- `thumb.py '{"sx":0.25,"dist":88,"el":20,"target":[0,-14,0]}'` → 4K PNG + 1280×720 JPG (<2 MB):
  3–4 huge words left ("NO SLIP. NO TILT." + teal "3-POINT GRIP"), amber product chip, logo, product right with
  highlighted feature. Check that text never overlaps the product.
- SEO txt (see example): title ≤70 chars with brand+model+benefit; description with pain → solution → bullet features,
  chapters (first 0:00, each ≥10 s), CTA links (site, landing page, channel), hashtags; tags ≤500 chars; Shorts title ≤60
  chars with #shorts.

### Phase 7 — Landing page merge (`landing.js` + `build_landing.py`)
- New section inserted after the hero (`<!-- SECTION 2 ...` marker), reusing the page's Tailwind/brand classes:
  badge, H2, sub, viewer card (canvas absolutely positioned inside a fixed-height box — otherwise ResizeObserver grows it
  forever), tour tabs, auto tour with caption + progress, play/pause, drag-orbit (OrbitControls) that pauses the tour,
  manual jaw slider, feature cards synced to tour steps, spec list, RFQ + YouTube CTAs.
- Lazy-start with IntersectionObserver; DPR ≤1.75; model as `<script type="text/plain">` base64.
- i18n: merge new keys into the page's existing `i18n` object for every language (`cn_i18n.json`), captions switch with
  the language selector. Add Product JSON-LD, keyword meta, hero link, mobile-nav link (desktop nav is usually full).
- Test in headless Chromium with the sandbox proxy (parse HTTPS_PROXY into playwright proxy dict, ignore_https_errors)
  so Tailwind CDN loads; screenshot overview, mechanism, grip, and zh language.

## Quality gates before delivery
- Mechanism direction and part grouping verified against section views; no part floats or interpenetrates in explode.
- Every claim traceable to CAD, the existing page, or the user. Emphasis colours disclosed.
- Both aspects: no text/product/caption collisions on the contact sheets; captions never overlap each other.
- `ffprobe`: 3840×2160 and 2160×3840, audio stream present, duration 1–3 min.
- Landing: loads, tour runs, tabs/slider work, language switch works, no console errors except blocked CDNs.

## Delivery
One answer with: landing HTML, 16:9 MP4, 9:16 MP4, thumbnail (JPG + 4K PNG), 2 SRTs, SEO text as a copyable template.
Offer a revision pass (VO wording, camera, scenes) — re-render cost ≈ 2–3 h CPU for both aspects.

## Lessons from product #2 (SBF1001 bowl feeder, large assembly)
- Unnamed assemblies (all nodes "instance"/"body"): dump per-body world bboxes, render id-labelled analysis views
  (ana.py pattern), then classify bodies into groups by id + geometry in pack.py. Colors from HOOPS are unreliable — pick brand materials.
- Mechanisms missing from CAD (e.g. helical bowl track) may be drawn as clearly illustrative overlays; say so in the landing lead/note.
- Large models (≈100k tris) at 4K on SwiftShader: use MeshStandardMaterial (no Physical/clearcoat), render 3D into a
  render target at R3D≈0.67 and upscale under full-res 4K overlays (video.js GLC.rt path; bg drawn as its own quad,
  rt quad toneMapped:true), and run 2 shards `SHARD=0/2|1/2 run_render.sh` (≈2.5–3 s/frame combined). Stagger shard launches ~15 s.
- Only claim numbers printed on the client's landing page; never quote frame dimensions from CAD when they differ from the spec.
- Landing pages without Tailwind: inject a self-styled section using the page's CSS variables; merge i18n into the
  page's own I18N object and wrap its global applyLang.
- thumb.py / encode.py output names come from env CODE=<product code>; enc_all.sh l|p does segments + mux resumably.

## Upgrade roadmap (next versions)
- Generic product config (`product.json`: part names, groups, pivots, stroke, explode, anchors, scenes) so engine/video/landing
  need no code edits per product.
- STEP/GLB input path (occt-import-js or trimesh) in addition to eDrawings.
- GPU or cloud render option; 1440p preview render for client approval before 4K.
- Multi-language VO + captions (es/pt/ru/ar) reusing the same timeline.

## v2.1.0 additions (SAF1001 axial tape feeder + SMT Intelligent Reel Storage Rack, 2026-10-21/22)
Examples: `examples/saf1001/` (fully named CAD, fast multi-part mechanism) and `examples/sir-rack/` (static structure + process/workflow story, 500 instanced slots).

**Mechanism & geometry**
- Named CAD (Chinese part tree): classify by name in pack.py; parts that are heavy or missing (springs 24k tris, silencers, taped components) → record bboxes in `extra.json` and draw procedurally at the exact CAD position.
- Repetitive geometry (wire dividers, stored reels, LEDs): rebuild ONE simplified geometry at each exact CAD position with `InstancedMesh` (505 dividers 531k → 44k tris). Set `frustumCulled = false` on every InstancedMesh whose matrices change — otherwise the bounding sphere from the first frame culls them forever.
- Per-instance state function: `state.slotFn(i, layer, k, occ) → [occ, pullOut, ledColor, ledK]` drives occupancy, pull-out and LED colour per slot from the timeline (store/pick/FIFO stories).
- Quantization: `S × 32767` must exceed the largest |coord| in mm (rack 1850 mm overflowed S=1300/32767 → garbage mesh). Template pack.py now asserts this. Check the hero part with `dbg.py` before writing scenes.
- Electronics / LEDs / lights / scanners not in CAD → illustrative, disclosed on page note + one line in the video (e.g. "Rack geometry from CAD · LEDs, lights and scanner shown illustratively").

**Timeline (video.js, see examples/saf1001)**
- `machineTime(t)`: integrates a per-scene playback RATE (e.g. 0.3 in mechanism scenes) so slow motion never jumps phase; label it "Slowed for clarity".
- `CAPMAP`: spoken-word sequences → caption text (`plus or minus 0.3 millimetres` → `±0.3 mm`, `smthelp dot com` → `smthelp.com`, `error prone` → `error-prone`). Print `vo_timing.json` words first to see how edge-tts splits numbers ("99.9 percent", "since 2011" come as one token).
- `scrim()` gradient behind the text column; `textBlock()` returns the y after the text → place cards/chips at `yb` so wrapped headlines never overlap.
- `callout()` auto-flips side and clamps inside the frame and above the caption band.
- Cameras as `V(landscapeCam, portraitCam)` pairs: wide products (2.5 m rack) need their own portrait framing (steeper azimuth, larger distance, target lower) instead of a fixed ×1.55.
- Portrait CTA hides captions; landscape keeps them.
- `dbgShot` + `scripts/dbg.py '[{"st":{...},"tg":[..],"d":..,"az":..,"el":..}]'` renders the bare stage — first check after pack.
- `sheet.py <l|p> <cols> <w>` builds contact sheets from preview frames; review both aspects every iteration.
- Re-voice a single scene with `IDS=build python tts1.py` (e.g. removing an unsupported claim like "strong").

**Render speed (2 vCPU SwiftShader, 4K, 24 fps)**
- One process (`rr.sh l|p`, budget 1150 s, rerun until "have N of N"); 2 shards gave no gain.
- `R3D=0.6 AA=0` landscape, `R3D=0.5` portrait. Cost is fill-rate: close-ups full of overlapping parts are 4–5 s/frame, wide shots ≈2–2.5 s. Run `bench.py <R3D>` on a close-up and a wide time first.
- Realistic ETA for ~140 s: 16:9 ≈ 2.5 h, 9:16 ≈ 2.5 h, encode 2×8 min → tell the user ~5–6 h up front.
- Don't run landing tests / encodes concurrently with a render (each halves render speed).

**Landing pages**
- Tailwind English-only page (e.g. How-it-works): insert a self-styled section (own CSS vars, `.dark` variants) before the first content section, hero button "Explore the 3D …", tabs = the page's own steps, specs card only from product sheets + CAD-derived (marked "(CAD)"), Product JSON-LD, og tags, keyword enrichment. Do not add languages the page doesn't have.
- Test with `PAGE=... SECTION=... TAB=... python testlanding.py`; in the sandbox Tailwind CDN may fail (400/407) — only own-section errors matter.

**Delivery**
- Upload to a new product subfolder under Jason's Drive output folder (1l_83yav0aSOi_M0gL3jiGzK1iFDCzIiU) with `gws drive +upload <file> --parent <id>`; verify with `files list` (8 files).

## 版本与迭代
- v1.0.0 (2026-10-19) — First version distilled from the CN-SM-2713 JUKI coil gripper project (Hark agent):
  eDrawings mesh extraction, shared Three.js engine, word-synced 4K timeline renderer (16:9 + 9:16), edge-tts VO,
  music bed, SRT, thumbnail, SEO, 7-language landing merge.
- v1.1.0 (2026-10-20) — SBF1001 vibratory bowl feeder: unnamed-body classification, illustrative overlays, render-target upscale + sharded 4K rendering, CODE-based output names, non-Tailwind landing merge.
- v2.0.0 (2026-10-21) — Standardised module: README, docs/ (IO_SPEC, CONFIG, WORKFLOW, VERSIONING), config schema + example, cfg.py + pipeline.sh, full examples for both products, CHANGELOG/VERSION.
- v2.1.0 (2026-10-22) — SAF1001 + reel storage rack: machineTime slow-mo, CAPMAP, scrim + textBlock-y layout, callout clamp, V(l,p) cameras, procedural parts for named CAD, InstancedMesh fleets + slotFn (frustumCulled=false), quant-scale assert, single-process render with per-aspect R3D (0.6/0.5, AA off), dbg.py/sheet.py/bench.py/tts1.py/rr.sh/testlanding.py, Tailwind English-only landing section, Drive delivery.
