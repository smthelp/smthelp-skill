# smt-3d-animation-landing-kit

Product 3D drawing + intro documents → mechanism animation, single-file 7-language landing page with interactive 3D, 4K 16:9/9:16 videos, thumbnails, SEO, Drive.

```
smt-3d-animation-landing-kit/
├── SKILL.md                 agent instructions (start here)
├── VERSION  CHANGELOG.md  README.md
├── config/
│   ├── defaults.json        all defaults (languages, blog_count, theme, model, roi, video, brand, drive)
│   └── job.schema.json      job.json contract
├── scripts/
│   ├── smt3d.py             CLI (all steps)
│   ├── common.py            config merge, paths, browser launch
│   ├── setup_env.sh         idempotent environment setup
│   ├── extract_mesh.py      eDrawings HTML → mesh.json
│   ├── pack_mesh.py         mesh/GLB/STL/OBJ → lightweight smt3d-v1 model
│   ├── build_lp.py          content.json → single HTML
│   ├── verify_lp.py         automated page checks + screenshots
│   ├── tts.py timeline.py audio_mix.py render.py finish_video.py thumbs.py
├── templates/
│   ├── landing/             style.css, app.js, viewer3d.js, wa_svg.txt
│   ├── video/               video.html, thumb.html (stage templates)
│   └── duel/duel-skeleton.js
├── references/              input contract, workflow, output spec, config reference, checklist, extension points, upgrade path, lessons
└── examples/
    ├── stf1003-tube-feeder/ complete job (job, content, i18n ×6, duel, script, video/thumb stage, assets incl. model.b64)
    └── bowl-vs-belt/        duel.js + script.json + video.html from the first job
```

Quick test after unzip:
```bash
cd smt-3d-animation-landing-kit
bash scripts/setup_env.sh
python3 scripts/smt3d.py validate examples/stf1003-tube-feeder/job.json
python3 scripts/smt3d.py lp examples/stf1003-tube-feeder/job.json
python3 scripts/smt3d.py verify examples/stf1003-tube-feeder/job.json   # ALL PASS
```
