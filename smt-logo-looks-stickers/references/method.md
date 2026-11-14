# Method: logo STEP -> brand looks + GIF stickers

## 0 Collect
- Logo CAD: STEP AP214 with colours (ask for STEP when given .x_t/.sldasm).
  A logo is usually 2 bodies (one per brand colour) extruded ~1 mm.
- Brand tokens: colours, contacts, fonts, circuit pattern — from smt-brand-kit
  (`../smt-brand-kit/assets/brand`), or `brand_dir` in the job. Never invent
  a colour: the skill reads `brand.json` / `config/defaults.json` only.
- Copy: every headline, kicker and contact line lives in the job (`texts`,
  `contacts`, `rollup_rows`). Nothing buyer-facing is invented by the scripts.

## 1 Inspect
`smtlogomedia.py inspect job.json` converts STEP -> GLB (cascadio) and writes
`work/parts.csv` (node, name, colour, bbox, faces). Read it before writing the
job: confirm the body count (a two-colour logo has 2 bodies) and the bbox
(logo is wide x, tall y, thin z, in metres after the axis mapping).

## 2 Colour override
A logo STEP stores arbitrary SolidWorks appearance colours. The engine
re-colours by rule, it never trusts the STEP colours:
- the STEP body whose green channel is higher (`color[1] > 0.5`) -> brand green
- the other body -> brand teal
Check the first preview: if green/teal are swapped, the rule is wrong for
that file — swap the two hex values in the job's `colors` and re-run.
(2026-11-14 SM logo: STEP stored near-black (0,13,0) + bright green
(27,196,0); the rule maps them to teal #0097B2 + green #93AC3E.)

## 2b Sub-line removal (drop_zone) and the clean 2D logo
The STEP may carry a sub-line the clean logo does not (SM: "SMT help.com"
under MACHINERY). Two things, both in the job:
- `drop_zone: [z_below, x_below]` drops faces in the bottom corner of the
  stood-up logo (face centroid z < z_below AND x < x_below). SM values
  [-0.085, -0.15] remove the sub-line completely and leave MACHINERY intact
  (verified by rendering the filtered logo, 2026-11-14). Find the values by
  rendering the logo with candidate thresholds and looking: the sub-line
  must be gone, the wordmark untouched.
- `logo_png`: when Jason supplies the clean 2D logo PNG (transparent), the
  flat looks use it instead of a 3D render — exact official art, sharper
  than any render. The 3D stickers still use the STEP (with drop_zone),
  because a flat PNG cannot spin or bounce in 3D.

## 3 Orientation
SolidWorks Y-down exports need the stand mapping `(x,y,z) -> (-x, z, y)`:
it un-mirrors the export, keeps the top up, and puts the front face toward
the +y camera. It is applied exactly once, inside `stand_upright`
(logo_cad.py). Never add a second axis transform before it — applying an
axis map in `load_parts` AND the stand mapping double-transforms the logo
and renders it rotated 180° (text backwards, lines swapped; caught
2026-11-14 when the first skill-test stickers came out flipped). Verify
with the first preview: if the text reads backwards, the stand mapping is
wrong for that file — fix it in the script, not in the job.

## 4 Render
CPU renderer (vendored `logo_render.py` from smt-3d-product-media 1.7.0):
numba z-buffer, no GPU/OpenGL. Two render modes:
- `render_rgba` (stickers, cards): render on white AND on black, recover
  alpha + colour by difference matting. Clean edges, real transparency.
- Front stills for the looks use the same path, then sit on a white rounded
  card (brand rule: the logo always sits on a white rounded card on dark
  backgrounds; never recoloured, never stretched).
- The logo face is never stretched. Only the extrusion thickness is scaled
  (`thicken`, 4-6x) so 3/4 views and spins show a solid edge.
- Framing: a wide logo needs a pulled-back camera on a square canvas —
  eye distance 1.9 for 512x512 stickers (0.95 crops the text). The mark is
  scaled to 0.8 wide and 0.865 tall, so its square renders also need a
  pulled-back camera: eye distance 1.5 (visible width 0.95 at fov 35°).
  At 0.95 the view only shows 0.60 wide and the mark is cropped on all
  sides — caught 2026-11-14 when the v2 thank-you frames showed the mark
  bleeding off the edges (v1 had the same crop, unnoticed at chat size).
  Wide canvases (logo cards) keep 0.95: the horizontal fov covers the
  full logo there.

## 5 Mark-only
The graphic mark is the image-left part of the logo. `logo_cad.mark_only`
keeps faces whose centroid x > 0.18, then re-centres and scales to 0.8 wide.
Threshold 0.18 splits the mark from the first letter at their gap. If the
mark render shows letter fragments ("HE"/"IN"), the threshold caught the
text side — flip the comparison (see troubleshooting.md).

## 6 Compose the looks
Six looks, all brand grammar (kicker green uppercase -> headline ExtraBold
-> short sub -> evidence -> contact strip, navy + faint circuit pattern):
hero 1920x1080, business card front/back 1050x600, email signature 720x170,
social avatar 512 + LinkedIn banner 1584x396, video end-card 1920x1080,
roll-up 800x2000. Every look is checked visually before delivery: no text
overflowing its canvas, no element clipped, logo fully inside its card.

## 7 GIF stickers
512x512, transparent, one animation each (spin / drop-bounce / pulsing ring /
slide-in / mark spin / wobble), 14-20 frames, text in Montserrat ExtraBold
with a navy stroke. Assemble with ffmpeg palettegen/paletteuse
(`max_colors=128:reserve_transparent=1`) — never PIL's GIF writer (it writes
corrupt LZW data for multi-frame RGBA; verified 2026-11-14). Verify every
GIF with `ffprobe -count_frames` (frame count must match the design) and by
viewing first/middle/last frames composited on a light background. Keep each
file under 500 KB (WhatsApp sticker limit).

## 8 Check and deliver
- Contact sheet of all looks + 3 frames per sticker before sending.
- Delivery: the `looks/` + `stickers/` folders + a README listing sizes and
  uses; zip with `tools/package.sh`.
- Tell Jason what is 3D (the renders are illustrations of the real logo
  model) and what was assumed (thickness scaled for the 3D views; STEP
  colours overridden to brand colours).
