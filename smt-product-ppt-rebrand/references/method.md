# Method - core flow

## 0. Scope (ask at most one question)
- List the Drive folder (`gws drive files list`, q = "'<id>' in parents and trashed=false").
- Group files by product line / model. Duplicates (`x.ppt`, `x 2.ppt`, `x.pdf`, `_Conflict` copies) are one source set; prefer the newest .pptx, use the PDFs to fill gaps.
- Skip: competitor folders, videos, STEP/CAD, pure company catalogues of other brands (use them only as data sources for an overview deck).
- If Jason already said "all products", do not ask - propose the grouping in one line and start.

## 1. Extract
- `convert_ppt.sh` for every .ppt; `extract.py` for all files.
- Read every `text.md`. Look at every `contact.jpg` - for image-only PDFs (flag NEEDS_VISUAL_READ) also open the key pages/images to read spec tables in pictures (model tables are often images).
- Note per product line in `facts.md`: model names, parameter table, features/selling points, applications, options, certifications, customers, company claims, and **conflicts between sources**.

## 2. Plan the deck (per product line)
Default order (drop what the sources cannot support, never pad):
1. Title (eyebrow category, product name with model, one-line subtitle, tagline of 3 benefits, hero image)
2. Contents (4-6 items mirroring the sections actually present)
3. Overview - what it is + 3 applications + image
4. Key figures - 3-4 numbers straight from the spec table
5. Pain points - what goes wrong without it (3-8 cards)
6. FAB 1 / FAB 2 - 3 rows each: Feature (spec-backed) -> Advantage (what it does) -> Benefit (business outcome for the EMS customer)
7. Design details / gallery - 2-4 real photos with 2 bullets each
8. Process / installation / workflow (if the source has one)
9. Before-after, global-brand components (if the source has them)
10. Specs (2 columns) or model selection table (multi-column)
11. Summary - 3 takeaways + "Why Southern Machinery" + a call to action
12-13. Template slides: Best After-sales service, Welcome Inquiry (automatic)

## 3. Writing rules
- Titles <= 44 characters, sentence-like claims beat labels ("Unprotected PCB Handling Costs Yield").
- Numbers exactly as the source (keep units, use x for dimensions, en dash for ranges, 10⁶ superscripts).
- FAB: Feature = what it has (with a number), Advantage = what it does, Benefit = what the customer gains (yield, uptime, labour, space, safety, compliance, cost).
- Concise business English, no hype words ("best", "No.1") unless the source proves it.
- Put sources, conflicts and assumptions in `notes` (speaker notes), not on the slide.

## 4. Images
- Use photos from the sources only; pick sharp, product-centred ones; `fit: true` for cut-out product shots on white, cover-crop for scene photos.
- Remove pictures that carry another brand's logo/name, Chinese labels or watermarks (crop them out with PIL or drop).
- Keep assets <= 1600 px; deck size target < 30 MB.

## 5. Build, check, fix
- `run.py spec assets out --name <seo> --render` -> validation, build, QA gate, render.
- Look at every sheet: wrapped big numbers, overflowing boxes, empty areas, wrong crops. Fix the spec (shorter text, fewer items, other image) and rebuild. Google rendering uses a wider substitute font: if a line only wraps in the preview, shortening is still preferred.

## 6. Deliver
- `upload.sh` each deck to the source folder. Reply to Jason with the list of decks (links) and every source conflict you resolved.
- Record new preferences in `feedback-log.md`.
