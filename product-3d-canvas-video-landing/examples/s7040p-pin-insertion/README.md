# Example: S7040P PIN insertion machine, 4 vibration bowl feeders (runnable)

A complete, runnable p3cv project for a **variant page**: the public S7020 FAB landing page is rewritten into an
S7040P page (4 bowls → 4 heads → 4 press-fit parts), with an interactive 4-head mechanism animation, the
S7000-platform 3D turntable and 4K 16:9 / 9:16 videos.

```bash
python3 -m p3cv init ~/work/s7040p --example s7040p-pin-insertion     # product.json, anim, img/
python3 -m p3cv run ~/work/s7040p/product.json download capture tts mix subtitles landing video thumbnail docs
python3 -m p3cv run ~/work/s7040p/product.json render
python3 -m p3cv run ~/work/s7040p/product.json mux --timeout 1100      # repeat while exit code is 3
python3 -m p3cv manifest ~/work/s7040p/product.json
```
Outputs (`out/`): `s7040p-pin-insertion-machine-landing-page-animated.html`, `S7040P_PIN_Insertion_4_Bowl_Feeders_16x9_4K.mp4`,
`..._9x16_4K.mp4`, thumbnail, SEO txt, SRT, VO script, manifest.json. Video ≈ 2:21; render at 1080p + upscale
(`video.scale 1`, `video.upscale true`) ≈ 40–60 min on a 2-core sandbox.

## What it demonstrates
| Feature | Where |
|---|---|
| Rewrite an existing model page: ~70 exact replacements (title, meta, JSON-LD, hero, KPIs, FAB, specs, FAQ, advisor, alts) | `landing.replacements` |
| Swap hero/gallery pictures by alt text | `landing.images` → `img/real1-3.jpg` (badge edited with `p3cv relabel`), renders |
| Old model name must not survive | `landing.forbid: ["S7020"]` (leftovers = links to the S7020 sister page, if any) |
| Existing SVG animation reused under the canvas contract | `s7040p-anim.js` = `templates/svg2canvas.js` + `insert-anim.svg.js` + `anim-wrapper.js` |
| Low-memory 4K | `video.scale: 1` + `video.upscale: true` |
| Privacy | public example keeps customer data out; see "Customer version" |

## Sources (public)
- 3D: `THT PIN Eyelet Insertion machine.html` (eDrawings, S7000-platform body) on file.autoinsertion.com.
- Base page: `S7020-Pin-Eyelet-Terminal-Insertion-Machine-FAB.html`. Catalog: S7020 series 202303 PDF.
- S7040P figures (P2P 0.025 mm, repeat 0.05 mm, MARK 0.015 mm, PCB 50×50–480×390 mm, 0.79–2.36 mm, footprint,
  power, interfaces) come from Southern Machinery's S7040P proposal deck (S7000P data) - not public; quoted in
  `seo.notes`. "About 0.5 s per part" is Southern Machinery's statement.

## Customer version (kept out of this public repo)
Real projects add, in their own product.json: the customer's part table and "published vs. your need" table
(an extra `landing.replacements` entry inserting a section before `#specs`), part dimensions in segments and
video cards, `InsertAnim.MODELS.C.dia/hole` appended to the anim module, and `privacy.confidential` /
`privacy.notes` for NDA drawings and customer photos. Never commit customer data here: this repo is public.

## Rebuild the anim module after editing its parts
`cat ../../templates/svg2canvas.js insert-anim.svg.js anim-wrapper.js > s7040p-anim.js`
