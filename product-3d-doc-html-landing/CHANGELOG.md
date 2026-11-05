# Changelog

## 1.0.1 - 2026-11-05
- build.py drops the Drive clips heading when `CLIPS` is empty.
- Known issue documented: SolidWorks eDrawings HTML exports hold no extractable GLB; render them headless (Playwright, SwiftShader) and crop stills, then use a procedural 3D scene. First used on the S-RF1001 radial feeder page.

## 1.0.0 - 2026-11-05
- First packaged release, distilled from five live pages (THT charger line, SIS7200A, SIS5210A, LED T8 line, PCB loader solution).
- Config-driven build (`config/default.yaml` + project `config.yaml`, deep merge): languages, blog/FAQ/station counts, theme colours, model mode and lightweight parameters, ROI, Chatwoot, publish target.
- Two 3D adapters: `viewer_glb.js` (GLB/GLTF with meshopt + draco, camera presets, explode, embedded animations, 5 material modes, 3 light presets) and a procedural Three.js example (9 animated PCB loader mechanisms).
- `model_prep.py`: GLB/GLTF/STL/OBJ/PLY, STEP via FreeCAD or cadquery, FBX via assimp, PPTX-embedded GLB; vertex merge, decimation, gltf-transform optimize. Tested 48.9 MB -> 214 KB.
- `extract_sources.py`, `contact_sheet.py`, `inline_images.py`, `i18n_tools.py` (mk-en, reuse, merge, add-lang), `validate.py` (15 hard checks), `render_test.py` (Playwright).
- Example `examples/pcb-loader-solution` rebuilds the published page byte-for-byte in content.
