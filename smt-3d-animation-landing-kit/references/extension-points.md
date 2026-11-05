# Extension points

| What | Where | How |
|---|---|---|
| New page section | `scripts/build_lp.py` | add `def s_<name>()` returning HTML (use `T(path, text, tag)` so it is translatable); add `<name>` to `config.sections` and the enum in `config/job.schema.json` |
| Section styling | `templates/landing/style.css` | use theme CSS variables only (`--brand`, `--deep`, `--line`…) so palettes keep working |
| Material preset | `templates/landing/viewer3d.js` → `MATERIALS` | `{spec, shin, alpha, tint, label}`; add the name to `model.material_presets`; add `ui.mat.<name>` translations |
| Lighting preset | `viewer3d.js` → `LIGHTS` | `{amb, l1, c1, l2, c2, bg}`; add to `model.lighting_presets` and `ui.light.<name>` |
| Viewer feature (section plane, hotspots, part picking) | `viewer3d.js` | add a method on the returned API + a control in `s_model3d()`; keep the `smt3d-v1` data format readable (new fields optional) |
| 3D input format | `scripts/pack_mesh.py` | add a loader branch producing triangles in mm; output must stay `smt3d-v1` |
| Mechanism animation | `<job>/duel.js` | class with `render(t, st)`, `METRICS`, `BADGE` (see `templates/duel/duel-skeleton.js`) |
| Video stage | `<job>/video.html` | must set `window.READY` and `window.seek(t)`; reads `window.TIMELINE` (scenes, cues) |
| ROI formula | `templates/landing/app.js` (ROI block) + `s_roi()` labels | keep input ids `roi_<key>` and outputs `roiR_<key>` |
| Language | `config.languages` + `language_labels` + `i18n/<code>.json` | RTL: add to `rtl_languages` |
| Theme | `job.json → config.theme` | any key of `config.theme` |
| Publishing target | `smt-product-landing-page/scripts/publish_webdav.sh` | keep credentials out of files |
