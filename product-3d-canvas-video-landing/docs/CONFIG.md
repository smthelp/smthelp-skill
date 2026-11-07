# product.json reference

Defaults: `p3cv/config.py` → `DEFAULTS`. Schema (editor hints): `config/product.schema.json`.
Templates: `config/product.example.json` (blank), `examples/juki-gripper-nozzle/product.json` (complete, real).
Paths in config are resolved: absolute → relative to the project folder → relative to the skill folder.
HTML is allowed in video scene text (`<br>`, `&amp;`); landing copy is escaped automatically.

## Required
| key | example | meaning |
|---|---|---|
| `slug` | `juki-gripper-nozzle` | prefix of output file names |
| `product_name` | `JUKI Gripper Nozzle SM-2070 / SM-2071` | used in titles, script header, folder name |
| `segments` | `[{"text": "...", "chapter": "Intro"}]` | voice-over, one item per sentence group; `chapter` → YouTube chapter |
| `anim.module` / `anim.global` | `jaw-anim.js` / `JawAnim` | animation module file and the window global it defines |

## brand
`name`, `logo_url`, `primary`, `primary_dark`, `dark_bg`, `dark_glow` (optional radial highlight), `accent`,
`email`, `whatsapp` (digits, for wa.me), `website`, `bar_label` (brand bar text in video/thumbnail).

## sources
`drawings[]`: `{id, url, viewer: threejs|edrawings, capture: bool, refresh: bool}` — the first drawing with
`capture: true` that succeeds becomes the turntable. `landing[]`, `docs[]`: `{id, url}`. URLs need `%20` for spaces.

## download
`timeout` 120 s · `retries` 3 · `max_mb` 80 · `extract_base64_images` true · `user_agent`.

## capture
`enabled` (false = supply `img/tt/v*.png` yourself) · `frames` 24 · `viewport` [1000,1000] · `settle_s` 30 ·
`zoom_steps` 5 · `zoom_delta` −200 · `drag_px` 40 · `click_buttons` ["Pause","Grid"] · `hide_ui` · `crop` [x0,y0,x1,y1] ·
`whiten` {min_bright 212, max_chroma 28} (pixels lighter + greyer than this become white) · `aspect` "4:3" ·
`zoom_out_steps` 0 (eDrawings: wheel out for big machines) · `drag_at` null ([fx,fy] drag point as viewport fraction; put it
off the model, e.g. [0.5,0.93], so no part-name tooltip appears) · `recenter` false (centre the model in every frame when the
viewer orbits around an off-centre point).

## voice
`provider` edge · `voice` en-US-AndrewNeural · `rate` −2% · `lead_in` 1.2 s · `gap` 0.9 s · `tail` 2.6 s ·
`lufs` −14 · `true_peak` −1.5 · `replacements` {spoken: shown} for subtitles · `max_cue_chars` 42.

## landing
`base` (id of the landing source to merge into) · `insert_before` (exact, unique HTML snippet; the section is
inserted before it) · `nav_after_href` (+ optional `nav_after_text`) where to add the nav link · `nav_label` ·
`output` file name · `section`:
`eyebrow, title, intro, canvas_label, steps[[name, description]] (one per anim STEP), tt_panel{title,text,alt},
photo_panel{title,text,image,alt,fit}, cards[[big, heading, text]], cta{whatsapp_text, email_subject, whatsapp_label, email_label}`.

## video
`fps` 30 · `formats` ["169","916"] · `scale` 2 (CSS 1920×1080 × 2 = 4K; 1 = 1080p) · `jpeg_quality` 92 · `crf` 19 ·
`chunks` 2 (parallel workers per format) · `tmp_dir` (/tmp/p3cv-<slug>) · `basename` · `max_seconds` (smoke tests) ·
`max_relaunch` 3 · `scenes[]`:

| type | keys (times are seconds from scene start) |
|---|---|
| `hero` (dark) | `kicker, headline, chips[[text,colour]], chip_times[], grid` |
| `turntable` | `kicker, title, subtitle, chips[[text,colour]], chip_times[], sweep_rate` |
| `mechanism` (dark) | `kicker, map[[segment, cycle_from, cycle_to]], focus{169:{x,y,s},916:{…}}, track{916:[x per step]}, opts{916:{noHud:true}}, theme` |
| `cards` | `kicker, title, cards[[big, text]], card_times[], photo, photo_fit` |
| `chips` (dark) | `kicker, title, chips[text or [text,colour]], chip_start, chip_step, card[big,text], card_time, photo` |
| `cta` | `kicker, title, checklist[], check_times[], contacts[[text,colour]], contact_times[], sweep_rate` |

Every scene: `type`, `from_segment` (index into segments), optional `theme` (dark | studio).

## thumbnail
`headline_html` (`<span>` = yellow highlight) · `badges[[text, bg, fg]]` · `subline` · `anim_t` · `anim_focus{x,y,s}` ·
`anim_opts{}` · `output`.

## seo
`title, alt_titles[], shorts_title, description, hashtags[], tags[] (≤500 chars total), shorts_description, notes[]`.
Chapters are generated from `segments[].chapter`.

## upload
`sink`: `gdrive` (`parent_id`, via `gws`) | `rclone` (`remote`, e.g. `gdrive:Marketing`) | `local` (`local_dir`) | plugin ·
`folder_name` with `{product_name} {slug} {date}` · `auto` (include upload in a full `p3cv run`).

## hooks / plugins
`hooks`: `{"pre": "...", "post_landing": "python3 my_check.py"}` — shell commands run in PROJ with env
`P3CV_PROJ`, `P3CV_STAGE`, `P3CV_WHEN`; non-zero exit = `E_HOOK`. `plugins`: list of .py files (see EXTENDING.md).

## Added in 1.2.0 (all optional, defaults keep 1.1 behaviour)
- `schema_version` (int, current **1**): product.json format. Files without it are treated as 1.
  A newer value than the installed skill reads fails with `E_CONFIG` ("upgrade the skill"). `p3cv migrate` upgrades.
- `landing.replacements`: list of `[find, replace]` or `{"find", "replace", "count"}` applied to the base page
  before the section is inserted. Use it to turn an existing model page into a new model / customer variant
  (title, meta description, JSON-LD, hero, KPIs, spec table, FAQ, advisor facts). Each snippet must match exactly
  `count` (default 1) times, otherwise `E_ASSEMBLE` - copy snippets verbatim from `src/<base>.html`.
- `landing.forbid`: strings that must not survive (e.g. the old model "S7020"); found ones are logged and
  returned as `leftovers` in the stage output (links to sibling product pages may legitimately remain).
- `video.upscale` (bool): with `video.scale: 1`, frames render at 1080p (~2-4x faster than scale 2) and `mux`
  lanczos-upscales each chunk to 3840x2160 / 2160x3840, one chunk at a time with low-memory x264 settings.
- `privacy.confidential` (list of source names/paths under NDA, e.g. customer drawings) and `privacy.notes`
  (publishing cautions): copied into the SEO file's CONFIDENTIALITY block; `check` warns when a confidential
  file is referenced in product.json.
