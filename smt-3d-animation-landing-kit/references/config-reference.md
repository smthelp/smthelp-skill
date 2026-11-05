# Configuration reference (`config/defaults.json`, config_version 1)

Merge order: `config/defaults.json` ← `job.json.config` (deep merge; arrays replace).

| Key | Type | Default | Effect |
|---|---|---|---|
| `languages` | string[] | en, es, pt, fr, ar, ru, zh | selector + verify; translations from `i18n/<lang>.json` |
| `default_language` | string | en | source language of content.json |
| `rtl_languages` | string[] | ar | sets `dir=rtl` |
| `language_labels` | map | native names | selector labels |
| `blog_count` | int | 8 | enforced in `validate`, `lp`, `verify` |
| `theme.brand/brand2/deep/accent/lime/gold/bg/bg2/fg/line` | hex | Southern teal palette | CSS variables |
| `theme.radius_px` | int | 14 | card radius |
| `theme.dark_mode_toggle` | bool | true | ◐ button |
| `model.accepted_formats` | string[] | edrawings-html, glb, gltf, stl, obj, step | `validate` rejects others |
| `model.preferred_format` | string | edrawings-html | documentation + validate |
| `model.triangle_budget` | int | 120000 | decimation target |
| `model.quantize_bits` | int | 16 | int16 positions (fixed in smt3d-v1) |
| `model.viewer_mode` | auto | auto | reserved: `webgl`, `turntable` (v1.1) |
| `model.material_presets` | string[] | industrial, matte, xray | buttons; names must exist in `SMT3D.MATERIALS` |
| `model.lighting_presets` | string[] | studio, warm, top | names must exist in `SMT3D.LIGHTS` |
| `sections` | string[] | 15 sections | order on the page |
| `roi.currency` / `roi.defaults.*` | | USD; 1 operator, 6/h, 8 h, 2 shifts, 300 days | ROI inputs |
| `video.formats/fps/scale/voice/rate/loudness_lufs/segment_seconds/target_duration_s` | | 169+916, 30, 2, AndrewMultilingual, +0%, −14, 30, [60,180] | render + audio |
| `brand.*` | | Southern Machinery blocks | header, footer, CTAs, JSON-LD, Chatwoot |
| `drive.parent_folder_id/account` | | 1mHq3OaE-RS5vMWd0pWJcM-0kQfZSncNb / smtmachine88@gmail.com | `drive` |
| `publish.webdav/folder/user` | | file.autoinsertion.com/dav, Product landing Page, smtfile | password never stored |
