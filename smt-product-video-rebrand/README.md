# smt-product-video-rebrand (v1.0.0)

Raw supplier/factory product demo clips + marketing themes -> Southern Machinery branded English 4K YouTube videos
(voice-over, subtitles, music, motion-graphic slides, thumbnail) + SEO title/description/chapters/tags + copy Google Doc.

- Entry point for agents: `SKILL.md`
- Engine: `scripts/smv/` (cfg, build, gfx, tts, thumbs, meta, lint, upload) driven by `scripts/run.sh`
- Brand: `config/brand.json` · project template: `config/project.example.json` (+ schema) · content templates: `templates/`
- Standards: `references/` (method, input/output spec, design & copy, shot library, QA, errors, versioning, feedback log)
- Worked example: `examples/x3100-xray-counter/` (17 videos, Oct 2026; source clips not stored in git)

Quick start
```bash
bash scripts/setup.sh
python3 scripts/new_project.py ~/work/p --model X3100 --name "X-ray SMD component counter" --prefix x3100-x-ray-smd-counter
export SMV_PROJECT=~/work/p SMV_BATCH=batch1
scripts/run.sh lint && scripts/run.sh tts && scripts/run.sh prev && scripts/run.sh sheet
scripts/run.sh 4k && scripts/run.sh qc && scripts/run.sh thumbs && scripts/run.sh meta
```
Fonts: Inter (SIL OFL) and JetBrains Mono (SIL OFL), licences in assets/fonts.
