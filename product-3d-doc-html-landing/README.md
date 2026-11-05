# product-3d-doc-html-landing

Product 3D model + product documents -> one self-contained, 7-language, 3D-interactive HTML landing page for Southern Machinery.

- Start with `SKILL.md` (Chinese, full workflow).
- Defaults: `config/default.yaml`. Project overrides: `<workdir>/config.yaml`.
- Reference build: `python3 scripts/build.py examples/pcb-loader-solution && python3 scripts/validate.py examples/pcb-loader-solution`
- Requirements: Python 3.10+, `pip install pyyaml pillow trimesh fast-simplification playwright`, Node 18+ (for `node --check` and `npx @gltf-transform/cli`), poppler-utils (pdftotext, pdfimages), ffmpeg (ffprobe). Optional: FreeCAD or cadquery (STEP), assimp (FBX).

```
SKILL.md  VERSION  CHANGELOG.md
config/default.yaml
scripts/  extract_sources.py contact_sheet.py model_prep.py inline_images.py i18n_tools.py build.py validate.py render_test.py publish_github.py ghput.py (Hark sandbox only) publish_github.py
templates/ template.html viewer_glb.js viewer_procedural_example.js page_template.py
references/ input-contract.md content-model.md i18n.md 3d-interaction.md extension-points.md validation-checklist.md upgrade-path.md
examples/pcb-loader-solution/  config.yaml en_ui.py en_blog.py page.py loader3d.js emb.json i18n/*.json
examples/glb-model/config.yaml
```
