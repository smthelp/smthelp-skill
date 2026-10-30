---
name: smt-product-ppt-rebrand
description: Rebuild old Southern Machinery product PDFs / PPTs (Chinese or rough English, mixed supplier material) into professional English product decks on the unified SM 16:9 brand template (2023-09), with title, contents, overview, key figures, pain points, FAB (Features-Advantages-Benefits), design details, specs / model tables, summary and the fixed After-sales + Welcome Inquiry slides, SEO file names and upload back to the source Google Drive folder. Use when Jason says 产品PPT更新/优化/统一品牌格式/重做产品介绍PPT/把文件夹里的PDF做成PPT, or gives a Drive folder of product files and asks for decks for overseas EMS customers.
metadata:
  version: 1.0.0
  updated: 2026-10-23
  brand_version: SM-PPT-202309
  first_cases: SPC950 pallet cleaner, SME5300/SME5200 fixture cleaners, ESD magazine rack, ESD PCB trolley, ESD flex arm, ESD storage board, ESD personal protection, ESD workshop solutions
  requires: python3, python-pptx, Pillow, lxml, poppler-utils (pdftotext, pdfimages, pdfinfo, pdftoppm); gws CLI for Drive I/O and for .ppt conversion / rendering when LibreOffice is absent
---

# SMT Product PPT Rebrand

Source files -> facts sheet -> one `spec.json` per product line -> validated -> built on the brand template -> QA gate -> visual check -> SEO name -> upload.
The builder never invents layout or colour: everything visual comes from `config/brand.json` and the template; everything factual comes from the sources.

```
Drive folder ──download──> sources/ ──extract.py──> extract/<file>/{text.md, images/, contact.jpg}, index.md
                                                          │  (read text + look at contact sheets)
                                                          v
                         facts.md (per product line: specs, features, claims, conflicts, images to use)
                                                          v
                         spec.json  ──validate_spec.py──> smbuild.py (template + brand.json) ──> deck.pptx
                                                          v
                         qa.py (gate) ──render.sh + sheet.py (look at every sheet) ──> fix ──> seo_name.py ──> upload.sh
```

## Read first
- `references/method.md` - the core flow step by step, grouping rules, writing and FAB rules
- `references/input-spec.md` - what the skill takes in and the `spec.json` format
- `references/slide-types.md` - every slide type, its fields and limits, with JSON snippets
- `references/brand-standard.md` - the unified brand format (template, colours, fonts, layout, fixed slides, file names)
- `references/output-spec.md` - deliverables, naming, delivery message, folder hygiene
- `references/error-handling.md` - error codes (E/Q/X/B/R) and what to do for each
- `references/versioning.md` - semver rules, release and sync with Git
- `references/feedback-log.md` - rules learned from Jason; apply all of them
- Worked example: `python3 scripts/run.py --example` (FJD250-95 storage board, 10 slides)

## Quick run
```bash
SK=<repo>/smt-product-ppt-rebrand/scripts
# 1 download the folder's PDF/PPT/PPTX (gws drive files get ... alt=media); convert .ppt
$SK/convert_ppt.sh sources/old.ppt
python3 $SK/extract.py extract sources/*.pdf sources/*.pptx
# 2 write facts.md + spec.json per product line (see method.md); images go in one assets dir
python3 $SK/run.py work/mag.json work/assets out --name "$(python3 $SK/seo_name.py 'ESD PCB Magazine Rack' 'anti static SMT loader unloader')" --render
python3 $SK/sheet.py out/<name-without-.pptx>      # then LOOK at every sheet and fix
$SK/upload.sh out/<name>.pptx <name>.pptx <drive_folder_id>
```

## Hard rules
1. Facts only from the source files. No invented specs, certifications, customers or prices. When sources disagree, pick the most specific source (model table > brochure prose), put the conflict in the slide notes and tell Jason in the delivery message.
2. Brand: use the template file as-is (logo, swoosh, circuit background, footer www.smthelp.com come from the master). Never redraw them, never change colours or fonts in a spec. Closing slides "Best After-sales service" and "Welcome Inquiry" are always the template's own slides.
3. Structure: title, contents, overview, at least one FAB slide, specs or model table, summary, then the two fixed slides. 5-14 body slides.
4. English for overseas EMS engineers: short, concrete, metric units with the source's numbers; no Chinese in the deck; no third-party/supplier brand names or logos (e.g. leenol, Shuaiyi) in text or pictures - crop or drop such images.
5. One deck per product line; merge duplicate source files of the same model; skip competitor folders, videos, CAD files unless asked.
6. Deliver .pptx (not Google Slides) to the same Drive folder, SEO file name from `seo_name.py`. Never overwrite or delete the source files.
7. Every deck passes `validate_spec.py` and `qa.py` and has been looked at as rendered sheets before upload.

## Upgrading
Change behaviour in `config/*.json` first, code second. After any change: `python3 scripts/run.py --example` must PASS, then `python3 scripts/bump_version.py patch|minor|major "<change>"` and run the git commands it prints. Log new user preferences in `references/feedback-log.md`.

## 版本与迭代
- 1.0.0 (2026-10-23) first release - see references/changelog.md
