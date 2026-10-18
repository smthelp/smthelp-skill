# Deliverables: content frameworks and style rules

All five draw words from `copy.json` and numbers from `facts.json`. Example specs for every output: `assets/example-x3100/`.

## 1. Single-file HTML landing page
- Tool: specialty `smt-product-landing-page` (build_page.py, check_page.py, 7 languages, Chatwoot, SEO/GEO JSON-LD, 8 Dan Koe blogs). Put its product dir in `<kit>/landing/`.
- Map: copy.headline -> hero_h1a; subhead -> hero_sub; metrics -> m1-m4; one_paragraph_answer -> ans_p; pains -> w1-w3; steps -> h1-h4; facts.json rows -> s{n}p/v/s with spec_evidence; versions -> d{n} (disc_status "By version"); faq -> q/a; before_you_order -> f3 list + ct_lead.
- A themed variant (e.g. "ROI: 99.99 % accuracy & MES sync") = copy the landing dir, rewrite hero/why/fit/roi/faq/blog keys and the file name around the theme; numbers stay identical.
- Self-hosted clips (rebranded) go in `landing/videos/`, published next to the HTML; deliver a zip with the HTML + videos/.

## 2. Marketing PPT (deck.json -> make_deck.py)
Sales deck, 8-14 A4 slides on the 2025 template. Default order:
1. cover - headline, subhead, hero photo, 4 metrics
2. cards - the problem (3 pains) + photo
3. steps - how it works (3-4 steps) + process photo / X-ray image
4. metrics - key specifications (8 tiles) + evidence note
5. table - versions or full spec with sources
6. bullets or cards - fit / applications / what it handles
7. gallery - 4 photos with factual captions
8. cards - service after delivery (installation, training, integration, whole line)
9. cta - five facts to send; template contact slide follows automatically
Rules: one message per slide title (a full sentence of the benefit, <= 60 chars); slide notes carry the sources; no price; render with `--preview` and fix every overflow before delivery.

## 3. Operation manual (manual.json -> make_deck.py)
Same renderer, manual tone. Chapters follow the supplier manual but in this order:
cover -> toc -> 1 Safety (warning slides, banner) -> 2 Specifications (table) -> 3 Parts and functions (photo + numbered table) -> 4 Installation & software setup -> 5 Daily operation (steps) -> 6 Settings -> 7 Troubleshooting (symptom -> first check table, last row "contact Southern Machinery service") -> 8 Maintenance (daily / monthly) -> appendix (I/O, wiring summary - full drawings "available on request").
Rules: imperative sentences, one action per step, every warning kept (never shortened), screenshots cropped to the relevant panel, Chinese UI labels explained in English captions, supplier contact replaced, front line "Read this manual before installing or operating the machine".

## 4. Poster (poster.json -> make_poster.py)
Formats: `a3` print (300 dpi PNG + PDF), `social` 1080x1350 (benefits dropped automatically), `story` 1080x1920. Structure: kicker -> 2-line headline (<= 22 chars a line) -> one-sentence sub -> hero photo -> 4 metrics -> 3 benefits -> CTA + contacts + optional WhatsApp QR + evidence footnote.

## 5. Video (video-*.json -> make_video.py)
- Promo 16:9, 60-130 s, 7-11 scenes: problem -> introducing -> step 1..4 -> what it handles (grid) -> extra mode -> version/automation -> key specs -> outro.
- Shorts 9:16, 30-45 s, 5-6 scenes: problem question -> core action with number -> data/label -> bonus -> outro.
- Each scene: kicker, 2-line head, (promo) 3 bullets, 1-3 voice lines. Clips: rebranded footage only, `crop` rows remove burned subtitles. Outputs subtitled MP4, clean MP4, SRT; add YouTube title/description/tags and a thumbnail (poster renderer, story or social format) when publishing.

## Delivery checklist
- `qa_kit.py <kit>` = 0 errors; read every WARN.
- Look at: deck/manual previews, poster PNGs, 3 frames per video, the HTML in a browser preview if possible.
- Hand over: HTML zip, deck PPTX, manual PPTX (and PDF if asked), poster PNG/PDF, promo + Shorts MP4 + SRT.
- Log what Jason says with `feedback.py add` before changing anything.
