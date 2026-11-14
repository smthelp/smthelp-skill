# smt-logo-looks-stickers

Turn a company logo STEP model into a reusable brand kit: six brand-style
looks and six animated GIF stickers, rendered from the real 3D logo.

## Install
```bash
pip install -r requirements.txt   # numpy, numba, trimesh, cascadio, Pillow
# system: ffmpeg >= 5
python3 scripts/smtlogomedia.py doctor
```
Brand assets (colours, circuit pattern, Montserrat fonts) come from the
sibling skill `smt-brand-kit` (`../smt-brand-kit/assets/brand`); point
`brand_dir` in the job elsewhere if your assets live in another folder.

## Use
```bash
python3 scripts/smtlogomedia.py init jobs/sm-logo --cad logo.STEP
python3 scripts/smtlogomedia.py all jobs/sm-logo/job.json
```
Outputs land in `jobs/sm-logo/out/looks` and `jobs/sm-logo/out/stickers`.
Edit `texts`, `contacts`, `rollup_rows` in the job for a new logo.

## Deliverables
- Looks: trade-show hero 1920x1080, business card front/back 1050x600,
  email signature 720x170, social avatar 512 + LinkedIn banner 1584x396,
  video end-card 1920x1080, roll-up banner 800x2000.
- Stickers: 512x512 transparent GIFs, each under 500 KB (spin, HELLO!,
  DEMO READY, LET'S TALK SMT, THANK YOU, SEE YOU AT THE SHOW).

See `SKILL.md` for the full contract and `references/` for the method,
job spec and troubleshooting.
