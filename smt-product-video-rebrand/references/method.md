# Method - step by step

## 0. Set up
- `bash scripts/setup.sh` (numpy, Pillow, edge-tts; checks ffmpeg/libass). Fonts and logo ship with the skill.
- `python3 scripts/new_project.py <dir> --model <SM model> --name "<generic product name>" --prefix <seo-file-prefix>`.
  The prefix is model + 3-5 search words, kebab-case (e.g. `x3100-x-ray-smd-counter`).
- Download the clips (`gws drive files get --params '{"fileId":"..","alt":"media"}' -o source/<name>.mp4`). Keep originals untouched in Drive. Short names (v1, v2 ...) are fine locally.

## 1. Facts sheet (content/facts.md)
- Read the official source (landing page, brochure, spec sheet). Copy every usable fact with its source.
- Three lists: **Confirmed**, **Brochure example** (must be labelled), **Not confirmed** (never claim; offer "send samples, we test").
- For a non-product claim (safety, physics, standards), web-search, open the page and add it to `SOURCES` in the batch module. Never cite a page only seen in search snippets as proof; mark it "abstract only".
- Anything Jason suggests that is not on the list: tell him and propose the hedged phrasing before writing (do not silently drop or silently claim).

## 2. Shot library (content/shots.py) - see shot-library.md
- `bash scripts/catalog.sh source/<clip>.mp4 1` for every clip; look at each sheet.
- Record clean ranges `a..b` (>= 0.7 s), crop (`kind`, `y0`), blur boxes for logos / model text / software title bars / Chinese UI, optional `zoom` variants (suffix `z`) and blurred variants (suffix `b`).
- Verify every entry on a cropped still (`python3 -c "import build; build.shot_still('F7b', 0.5, '/tmp/x.png')"` from scripts/smv with SMV_PROJECT set) and LOOK at it, including the top 80 px (title bars) and corners (watermarks).

## 3. Plan the batch
- One video per theme; slug = short kebab topic (`mes-erp-integration`); add a batch prefix (`b2-`) from batch 2 on.
- Arc per video (5-9 scenes, about 15-25 s each): problem / question -> what it is -> how it works (footage) -> proof facts (stat callout) -> use cases / comparison (slides) -> limits or "test with your parts" -> CTA outro.
- Assign footage first, slides where footage is missing. Target >= 50 % footage time. Mirror about half the videos; give each its own `intro_shot`, `music` (0-5) and slide set.

## 4. Write content/<batch>.py
- `VIDEOS` (scenes), `SLIDES` (data slides), `SEO`, `OUTRO_TEXT`, `NOTES`, `SOURCES` - format in input-spec.md, rules in design-copy-standard.md and output-spec.md.
- Bespoke diagrams that the 8 slide types cannot express go in `content/slides.py` (`make_slide(sid, S)` returning a list of PIL images; import primitives with `from gfx import *`).
- `run.sh lint` until 0 errors; read every warning.

## 5. Voice, preview, look
- `run.sh tts` (edge-tts; unset proxies - run.sh does). Add pronunciations for model numbers and acronyms in project.json (`"X3100" -> "X thirty-one hundred"`).
- `run.sh prev` renders 960x540 previews (~30-40 s each), `run.sh sheet` makes 12-frame sheets. LOOK at every sheet: text overflow, callout fits, right footage under the right sentence, nothing forbidden in frame, slide timing.
- Fix in content, re-run prev for that slug only.

## 6. 4K render
- `run.sh 4k <slug>` ~6-8 min per 2-min video on 2 CPUs. Run as a background job, one or two at a time, each job < 20 min; background jobs die when the agent session ends, so wait for them before finishing. If a job dies, delete `build/<slug>/4k` and rerun that slug.
- `run.sh qc <slug>`: must print PASS; LOOK at the sheet (zoom into any software screen for title bars / supplier names).

## 7. Thumbnails, copy, delivery
- `run.sh thumbs`, LOOK at each (text fits left of the picture, gold highlight word, no supplier marks).
- `run.sh meta` -> metadata.json + copy.html; must exit 0.
- `python3 scripts/smv/upload.py <folder>` then `--doc`; get `webViewLink`s (`gws drive files list` with `fields=files(name,webViewLink)`).
- Fix after delivery: re-render, then `upload.py <folder> --replace <slug>` (same file ids and links).
- Report (output-spec.md "Delivery message"). Update the project tracker and feedback-log.md.
