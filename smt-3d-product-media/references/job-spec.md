# job.json reference (schema `smt-3d-product-media/job@1`)

Coordinates: metres, after `model.axis` is applied, with +z up. Times: seconds. Colours: rgb 0-1 unless noted.
Defaults: `config/defaults.json`. Full example: `examples/s7040p/job.json`.

## product
| key | type | meaning |
|---|---|---|
| model | str, required | model name, e.g. `S7040P` |
| seo_slug | str | file-name stem, e.g. `S7040P-PIN-Insertion-Machine` |
| name | {lang: str} | display name |

## model
| key | default | meaning |
|---|---|---|
| cad | required | STEP/STP (converted with cascadio) or GLB/GLTF/OBJ/STL |
| axis | [1,-1,-1] | per-axis sign (and scale) mapping CAD axes to animation axes; SolidWorks Y-down exports need [1,-1,-1] |
| scale | 1.0 | extra scale (CAD in mm via GLB already comes in metres) |

## scene
| key | meaning |
|---|---|
| groups | ordered {name: selector}. First match wins; unmatched parts are `static`. Names are referenced by props/animation |
| copies | [{group, as, offset}] duplicate a moving group (add heads/feeders the CAD does not have) |
| static_copies | [{match, offset, why}] duplicate static sub-assemblies (frames, tracks, stands) |
| hide | [selector] parts dropped from the scene |
| logos.match | selector of logo bodies; pre-mirrored when render.flip_x is true |
| logos.extra | [{match, offsets:[[dx,dy,dz]], premirror:false}] copy a logo body to visible faces |
| palette | name in `config/palettes.json` or an inline rule list |

Selector keys (all given keys must match): `nums`, `ranges` [[a,b]], `node_prefix`, `name_contains`, `box` [[x0,y0,z0],[x1,y1,z1]] (part bbox fully inside), `any` [selectors], `not` selector. Node numbers/names/bboxes come from `out/work/parts.csv`.

## props (kinematics `xy_table`)
| key | meaning |
|---|---|
| pcb | {size [x,y], thickness, top_z, home [x,y] (board centre with table at 0), enter_from, exit_to, travel (fraction of scene), color} |
| heads | {id: {xy, group, clinch_group, pin_z, press, clinch_lift}} - head groups move down by `press`, clinch groups up by `clinch_lift` |
| points | [[u, v, head_id]] insertion points in board coords, in insertion order |
| bowls | [{group, dir, amp_deg=0.6, speed=37}] vibrating bowls |
| feed_tracks | [{x, y:[from,to], z, count=4, speed=0.35}] parts flowing to the heads |
| pin | {hr: [height, radius]} inserted pin size |
| part | {shape: "pin" (default), "blade" size [width, thickness, height] (flat terminals, S70xxT) or "eyelet" size [outer_d, length, flange_d] (hollow rivet, S70xxE); optional color [r,g,b] 0-1} |

## animation
| key | meaning |
|---|---|
| kinematics | `xy_table` (built in). Other machines: `plugin` = python file with `state(t, job, renderer)` and optional `extra_meshes(t, s, job, renderer)` |
| x_groups / y_groups | groups moved by the table X / X+Y offset |
| scenes | [{id, dur, action, camera, caption, return}] in time order |

`action`: idle | board_in | feed | insert | board_out. `return` (insert only): seconds for the table to go home.
`camera`: `eye` [from,to] or `orbit` {center, angle [deg,deg], radius [a,b], height [a,b]}; `target` [from,to]; `fov` [from,to]; `ease_time`; `sway` [dx,dy,dz]. A `from` value may be `"prev"` = end of previous scene (smooth cuts).
`caption`: {lang: {head, sub, step}} shown in the top bar / subtitle box / step counter.

## render
width 1280, height 720, fps 24, supersample 2, flip_x false (mirror the final image, e.g. so the PCB flows left to right), background, edges true, jpeg_quality 92, workers 2.

## real_clips / sequence
`real_clips`: [{src, start, dur, fit: cover|blur_pad|auto, caption {lang}, head {lang}, step}].
`sequence`: [{type:"3d", from, to, caption?} | {type:"real", clip:k}] - order of the final video. Empty = whole 3D animation.

## overlay, disclosure
`overlay`: enabled, logo, footer_url, colors {bar, accent, title, box_outline} (0-255), font_bold/font_regular (else Noto Sans SC is found or downloaded), real_note, real_head.
`disclosure`: {lang: text} bottom note on every 3D frame. Required whenever the 3D is not the exact machine.

## voice
enabled, engine `edge-tts`, voices {lang: voice} (zh-CN-YunyangNeural, zh-CN-YunxiNeural, en-US-AndrewNeural, en-US-GuyNeural ...), rate "+0%", max_tempo 1.35, loudness -16 LUFS, lines [{at, until, en, zh}] in final-video time. A line longer than its slot is sped up up to max_tempo, beyond that a V10 warning asks you to shorten it.

## deck
enabled, name_pattern (`{slug}-Product-Presentation-{LANG}-Southern-Machinery`, matches the builder SEO check), builder (default `../smt-product-ppt-rebrand/scripts/run.py`), spec {lang: path}, assets (folder), poster_t (s), render (bool: builder renders sheets; needs its renderer). Placeholders in specs: `{video}`, `{poster}`, `{still:<name>}`, `{model}`.

## stills, encode, publish, output
`stills`: [{name, t, eye?, target?, fov?, width?, height?}].
`encode`: crf 21, preset veryfast, audio_bitrate 160k.
`publish`: drive_folder (Google Drive folder id), account (informational).
`output`: dir `out`, langs ["en","zh"], name_pattern `{slug}-{variant}-{LANG}`, video_variant (default `Video`).
