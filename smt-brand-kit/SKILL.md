---
name: smt-brand-kit
description: Turn a supplier's product material (Chinese or English manuals, brochures, quotations, photos, videos) into a complete Southern Machinery branded kit - single-file HTML landing page, marketing PPT, poster, promo video + Shorts, and English operation manual - with one fact table, one master copy, the SM voice and visual system, a brand/evidence quality gate and a feedback loop. Use when Jason sends supplier files and asks for 品牌物料, 全套物料, landing page + PPT + poster + video + manual, a rebrand of supplier material, or any one of these outputs for a new product.
metadata:
  version: 1.0.0
  updated: 2026-10-18
  first_kit: X3100 X-ray counter (supplier XC-3100E)
  depends_on: smt-product-landing-page (HTML page), learn-SMT-in-3-hours (evidence rules)
---

# SMT Brand Kit - supplier material -> Southern Machinery kit

One product = one kit folder. Facts and copy are written once; five renderers turn them into the outputs; one gate checks them all.

```
sources/ -> extract -> facts.json (evidence) -> copy.json (SM voice) -> deck.json / manual.json / poster.json / video-*.json / landing/
                                                                     -> make_deck / make_poster / make_video / build_page -> out/ -> qa_kit -> Jason -> feedback.py
```

## Read first
- `references/brand-guide.md` - voice, naming, never-publish list, colours, type, layout grammar
- `references/extraction-rewrite.md` - source priority, facts.json, versions vs conflicts, supplier scrub, copy.json fields
- `references/deliverables.md` - section order and rules for each output, delivery checklist
- `references/feedback-log.md` - rules learned from Jason; apply all `done` rules, ask about `open` ones
- Example kit with every spec filled: `assets/example-x3100/` (photos included; clips referenced as videos/... are not bundled)

## Workflow
1. **Kit**: `python3 scripts/init_kit.py <kit> --model X3100 --name "X-ray Counter with Inspection" --supplier-terms "RMI,瑞茂,Sxray,..." --supplier-model XC-3100E`. Copy every supplier file into `<kit>/sources/`.
2. **Extract**: `python3 scripts/extract_sources.py <kit>` -> text, page renders, images, video frame sheets, `extracted/report.md` (supplier marks, emails, phones, CJK share). Look at every contact sheet. Add newly found supplier terms to kit.json.
3. **Facts**: write `facts.json` from the extracted text - value, unit, source, evidence (v/c/t); versions and conflicts handled per extraction-rewrite.md. Ask Jason only what the documents cannot answer (version naming, which options he sells).
4. **Rebrand media**: `scripts/rebrand_media.py photo|video|web` into `<kit>/photos` and `<kit>/videos`; check each result visually; drop what cannot be cleaned.
5. **Copy**: write `copy.json` in the SM voice (brand-guide.md). This is where quality is decided - every output reuses it.
6. **Specs**: fill `deck.json`, `manual.json`, `poster.json`, `video-promo.json`, `video-short.json` (formats in each script's docstring and the example kit) and the landing product dir in `<kit>/landing/` (smt-product-landing-page workflow, including 6 parallel translation subagents).
7. **Render** (independent - run in parallel; videos in background):
   - `python3 scripts/make_deck.py <kit>/deck.json <kit>/out/<Model>-Marketing-Deck.pptx --preview <kit>/out/prev-deck`
   - `python3 scripts/make_deck.py <kit>/manual.json <kit>/out/<Model>-Operation-Manual-EN.pptx --preview <kit>/out/prev-manual`
   - `python3 scripts/make_poster.py <kit>/poster.json <kit>/out/<Model>-Poster`
   - `python3 scripts/make_video.py <kit>/video-promo.json <kit>/out/<Model>-Promo-EN.mp4 --build /tmp/<model>_p` (and video-short.json; needs `pip install edge-tts`, direct internet)
   - landing: `python3 ../smt-product-landing-page/scripts/build_page.py <kit>/landing --out <kit>/out` (+ videos/ folder, zip)
   Renderers exit 1 on overflow or missing media - shorten the copy, never shrink below the set sizes.
8. **Gate**: `python3 scripts/qa_kit.py <kit>` -> 0 errors; read WARNs. Look at deck/manual previews (montage), posters and 3 frames per video.
9. **Deliver** to Jason: HTML zip, deck, manual, poster PNG/PDF, promo + Shorts MP4 + SRT; list open To-be-confirmed points in one line. GitHub push of the landing page per smt-product-landing-page (403 = no write access).
10. **Learn**: every remark from Jason -> `python3 scripts/feedback.py add <area> "<remark>" --product <model> --rule "<general rule>"`. Fix the rule in the right reference/script/brand.json, re-render the affected output, `feedback.py done FB-nnn "<file> v1.x.y"`, bump the version below.

## Fixed rules (do not drop)
- Supplier name, logo, contacts, domain and model code never appear (model code only if Jason asks); SM contact block on every output.
- Never publish price, lead time, stock, warranty, payment terms, customer names, unbacked certificates, saving/yield/ROI percentages.
- Every number traceable to facts.json; conditions kept; conflicts shown as To be confirmed or By version.
- English is the source; landing page in 7 languages; other outputs translated only on request.
- Headings never contain hook/diagnosis/framework/vehicle/loop/CTA (or the Chinese equivalents).

## Upgrading
- Brand change (colour, contact, voice, TTS) -> `assets/brand/brand.json` + brand-guide.md; all renderers follow.
- New slide/scene/poster element -> add a type in the script, document it in its docstring and deliverables.md, add it to the example kit, render the example, run qa_kit.
- Version: major = spec format change (old kits need edits); minor = new type/output/check; patch = fixes. Add one line to the history and sync local `/workspace/smthelp-skill/smt-brand-kit/` with GitHub smthelp/smthelp-skill (show Jason before pushing).

## Version history
- 1.0.0 (2026-10-18) - first release from the X3100 work: kit layout, extract_sources, rebrand_media, data-driven deck/manual renderer on the SM 2025 A4 template, poster renderer (A3/social/story), storyboard video renderer (16:9 promo + 9:16 Shorts, edge-tts, burned subs + SRT), qa_kit gate, feedback log seeded with Jason's rules since 2026-10-13.
