# Changelog - taobao-to-sm-marketing
Semantic versions: major = workflow or I/O change, minor = new output / parameter / script, patch = fixes, wording, never-publish terms.
Add entries with `python3 scripts/bump_version.py <part> "note" --kit <product>`.

<!-- new entries -->
## 1.0.0 - 2026-11-20
- First release, distilled from three Taobao -> SM kits built 2026-11-19: stencil storage rack (S-Series), printer squeegees (all brands), stencil wiping paper rolls.
- Outputs: facts.md, models.py SKU list, 17-slide PPT (smt-product-ppt-rebrand), 7-language landing page + zip (smt-product-landing-page), promo + Shorts + SRT + YouTube SEO txt (smt-brand-kit make_video.py), separate USD price list XLSX + PDF.
- Scripts: new_kit.py, scrub_check.py, price_usd.py, bump_version.py; templates/kit with quote and landing-src builders.
- Known issues: edge-tts sometimes returns NoAudio for one line (re-run or reword); no LibreOffice in the sandbox, so PPT preview needs Drive render or local check; ppt validator needs meta.allow_brands for brands such as Panasonic.
