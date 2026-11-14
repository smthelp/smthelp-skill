# job.json reference (schema `smt-logo-looks-stickers/job@1`)

Paths in a job are relative to the job file, except `brand_dir` when it is
the repo default `../smt-brand-kit/assets/brand` (resolved against the skill
folder). Colours are hex without `#`. Defaults live in `config/defaults.json`;
a job only needs to set what differs (normally just `cad`).

## logo
| key | type | meaning |
|---|---|---|
| cad | str, required | logo STEP file (AP214). `init` sets it from `--cad`. |
| logo_png | str, optional | clean 2D logo PNG (transparent). When set, the flat looks use it instead of a 3D render (exact official art); the 3D stickers still use the STEP. `init` sets it from `--png`. |
| drop_zone | [z_below, x_below], optional | corner zone to drop from the stood-up meshes (face centroid z < z_below AND x < x_below), e.g. a sub-line under the wordmark that the clean logo does not carry. SM logo: [-0.085, -0.15] removes "SMT help.com" and leaves MACHINERY intact (verified 2026-11-14). Always check the first preview after setting it. |

Orientation is fixed inside the skill (`stand_upright` in logo_cad.py):
there is no axis/scale key. If a render reads mirrored, the stand mapping
is wrong for that file — fix it in the script, never by adding a second
axis transform (that double-transforms and renders the logo rotated 180°;
caught 2026-11-14).

## brand
| key | type | meaning |
|---|---|---|
| brand_dir | str | folder with brand.json, circuit.png, fonts/. Default: sibling smt-brand-kit assets. Missing circuit.png -> plain navy background; missing fonts -> DejaVu fallback. |
| colors | {name: hex} | navy, navy_deep, navy_mid, green, teal, grey, light, muted, white. The two logo bodies are re-coloured to `green` / `teal` (see method.md step 2). |

## company / contacts / person
| key | type | meaning |
|---|---|---|
| company.short / .full | str | "Southern Machinery" / "Shenzhen Southern Machinery Sales and Service Co., Ltd." |
| contacts.web / .email / .whatsapp | str | web without scheme, email, WhatsApp with country code |
| person.name / .title | str | email-signature person, e.g. Jason Wu / CEO |

## texts (all optional, SM defaults in config/defaults.json)
hero_kicker, hero_headline_1, hero_headline_2, hero_sub, card_tagline,
sig_line, banner_kicker, banner_headline, banner_sub,
endcard_headline, endcard_sub_1, endcard_sub_2,
rollup_kicker, rollup_headline_1, rollup_headline_2, rollup_cta.

## rollup_rows
[[kicker, line], ...] — the four benefit rows on the roll-up banner.

## looks / stickers
Arrays of keys to run. Defaults run all.
looks: hero, business_card, email_signature, social, endcard, rollup.
stickers: spin, hello, demo_ready, lets_talk, thank_you, see_you.

## out_dir / work_dir
Output folders, relative to the job file. Defaults: `out`, `work`.
`out/looks`, `out/stickers`; `work/model.glb`, `work/parts.csv`, `work/gif-*`.
