# Input contract

## 1. Product 3D drawing
| Format | Status | How it is read |
|---|---|---|
| eDrawings / HOOPS Communicator `.html` | **preferred** (Southern Machinery standard export) | `extract_mesh.py` drives the embedded viewer in headless Chromium (SwiftShader WebGL) and reads every body's tessellation + net matrix |
| `.glb` / `.gltf` | supported | `pack_mesh.py` via `pip install trimesh` |
| `.stl` / `.obj` | supported | `pack_mesh.py` via trimesh |
| `.step` / `.stp` | convert first | FreeCAD/`occt-import-js` (see `build-fast-3d-html-viewer`) → GLB, then as GLB |
| SolidWorks native, 3D PDF | reference only | ask for an eDrawings HTML export |

Source: `https://file.autoinsertion.com/public/SMT%20machine%203D%20Drawing%20in%20Html/<name>.html` or a local file.
Naming: keep the exporter's name (`SMT Tube Feeder S-Designed by Southern Machinery.html`); `fetch` stores it as
`src/drawing_<safe-name>`. Units: eDrawings matrices are metres → converted to mm. Unnamed bodies ("instance/body") become one part per body (`<name>#<id>`).
Large models: `model.triangle_budget` (default 120 000) triggers vertex-clustering decimation.

## 2. Introduction documents
| Kind | Format | Source | Used for |
|---|---|---|---|
| Spec sheet / catalog page | PDF with text layer | `file.autoinsertion.com/public/Southern Machinery Product/` | specs table, every number, FAQ |
| User manual | PDF/DOCX→PDF | Jason | "not suitable" limits (manual wins conflicts) |
| Existing landing pages (1–2) | HTML | `file.autoinsertion.com/public/Product landing Page/` | structure, selling points, images, YouTube IDs, contacts, links |
| Photos | jpg/png/webp, ph.smthelp.com URLs | ph.smthelp.com, PDF images (`analyze` → `assets/pdf/`) | hero, gallery, video, thumbnails |

## 3. Task parameters
All parameters are files in the job folder (scaffold with `smt3d.py init`):
- `job.json` – inputs, slug, sections, duel class, video keywords/phrases, SEO, Drive folder, `config` overrides. Schema: `config/job.schema.json`.
- `content.json` – every visible English string, structured by section (see `examples/stf1003-tube-feeder/content.json`).
- `i18n/<lang>.json` – `{ "<content path>": "translation" }`; missing keys fall back to English.
- `script.json` – narration `[{id, text}]`, scene ids = video chapters; numbers spelled for TTS, mapped back with `video.phrases`.
- `duel.js`, `video.html`, `thumb.html` – product-specific animation, video stage and thumbnail layout.
CLI only takes the job path plus `169|916` and `--budget <s>`.
