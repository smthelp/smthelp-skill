# Example: AI Radial Splicing Tape (reference + regression fixture)

Reproduces the page published 2026-10-13 at
`smthelping/smt-product-landing-html/materials-consumables/ai-radial-splicing-tape-3-5-6-hole-masking-kraft-paper-splice-cutter-southern-machinery.html`.

| File | What it holds |
|---|---|
| `product.json` | structure: section order, counts, hero/gallery images, 20 videos, 10 catalogs, family links, calculator, JSON-LD products/HowTo/terms |
| `i18n/en.json` | 381 English master strings (keys follow references/i18n-guide.md) |
| `i18n/{es,pt,fr,ar,ru,zh}.json` | translations; model codes and numbers (m1v, mc1t ...) are left out on purpose and fall back to English |
| `blogs.json` | 8 English articles, six-step brief, no brief words in headings |
| `illustration.svg` + `product.css` | the 3-hole splice concept drawing in "How it works" |
| `assets/rolls.jpg`, `assets/strip.jpg` | two tape photos cropped clear of supplier watermarks, inlined as base64 |

Sources used: smthelp.com product pages (SCT codes, packing, delivery, cutter 12.7/15.0 mm) and six
Taobao listing PDFs (hole counts, 42x36 mm, synthetic rubber, steps). Supplier names and prices omitted.

Build: `python3 ../../scripts/build.py . --out dist` — Verify: `bash ../../scripts/regress.sh`
