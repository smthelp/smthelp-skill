---
name: smt-product-landing-page
description: Build a marketing-grade single-file HTML product landing page for a Southern Machinery SMT/THT product (machine, feeder, nozzle, jig, spare part), with 7-language switch (EN default, ES, PT, FR, AR rtl, RU, ZH), dark/light mode, ph.smthelp.com photos, matched YouTube videos and catalogues from file.autoinsertion.com, 8 Dan Koe six-step blogs, Chatwoot support widget, SEO/GEO JSON-LD, then push to GitHub smthelping/smt-product-landing-html. Use when Jason asks for a product landing page, 产品落地页, 营销型单页, or to update/upgrade an existing one.
metadata:
  version: 1.1.0
  updated: 2026-10-15
  reference_page: https://file.autoinsertion.com/public/Product%20landing%20Page/s-mvf01-reciprocating-belt-feeder-smart-ems-pcb-assembly.html
  first_build: sfcjf1-fuji-nxt-feeder-calibration-jig-smart-ems-pcb-assembly.html
---

# SMT Product Landing Page

One product = one product dir (`product.json` + `blogs.json` + `i18n/<lang>.json`) → `scripts/build_page.py` → one self-contained HTML file. Design, runtime and section order are fixed in `assets/base/` and the builder; only content changes per product. Copy `assets/example-fuji-nxt-feeder-calibration-jig/` as the starting point.

## Workflow

1. **Collect evidence.** Read every attachment (manual, brochure, quotation, packing list, nameplate, video, AGENTS.md). Load `learn-SMT-in-3-hours` and the product folder's AGENTS.md rules. Build a fact table: value, source document, label `Verified source` / `To be confirmed` / `Concept view`. Conflicting values go to Open points with both values; never average or pick one. Never publish price, lead time, warranty, payment terms, customer names, certifications or yield/ROI numbers. See `references/content-rules.md`.
2. **Harvest assets.** Prefer ph.smthelp.com URLs. Attached photos not yet on ph.smthelp.com go into `<product_dir>/photos/` and are referenced with `"file"` (embedded; keep it to about 8 photos, the page grows ~55 KB each). `python3 scripts/harvest_assets.py "<regex>" <image terms...>` lists ph.smthelp.com images, matching YouTube board videos and catalogue-board documents. Download the `.md.` images, make a contact sheet (`montage`) and look at it; drop photos of other machines; caption only what is visible.
3. **Write the en strings.** Copy the example `i18n/en.json` and rewrite every value for the new product. Keep the key families (see `references/page-structure.md`); add or remove numbered rows (`s18p/v/s`, `d8p/a/b/c`, `q9/a9`, `tr6` ...) freely - the builder counts them.
4. **Write 8 blogs** into `blogs.json` (English bodies, 6 paragraphs each in six-step order; titles and summaries `bl{n}t`, `bl{n}s` live in i18n). Method in `references/content-rules.md`.
5. **Fill `product.json`**: SEO file name `<model>-<product-slug>-smart-ems-pcb-assembly.html`, gallery, hero indices, fit images, videos, catalogues, `spec_evidence`, JSON-LD extras, `storage_prefix`. Schema in `references/page-structure.md`.
6. **Translate.** Dispatch one subagent per language (es, pt, fr, ar, ru, zh) in parallel with the brief in `references/translation-brief.md`; each writes `i18n/<lang>.json` with the identical key set.
7. **Build and check.** `python3 scripts/build_page.py <product_dir> --out <dir>` then `python3 scripts/check_page.py <product_dir> <dir>/<file>.html`. Optional runtime test with jsdom (`references/testing.md`).
8. **Deliver.** Save the HTML (and the product dir) in the project `output/`, show the file to Jason, then `python3 scripts/push_github.py smthelping/smt-product-landing-html <file>` (shell call with github credentials). A 403 means the connected GitHub account lacks write on that repo - tell Jason, do not retry.

## Fixed requirements (do not drop)

- Logo top-left `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`.
- Footer CTA band + LinkedIn company, LinkedIn profile, X/Twitter, Facebook, YouTube; links to file.autoinsertion.com catalogue and ph.smthelp.com photos; info@smthelp.com; WhatsApp wa.me/8613602562576. `check_page.py` enforces these.
- Chatwoot widget bottom-right (token `saMcpgSupcmd1VQwytgPLfbK`, chat.smthelp.com, protocol-adaptive BASE_URL so https pages do not block it).
- Theme + language persisted in localStorage and restored on reload; `?lang=xx` overrides; Arabic switches `dir=rtl` with bidi isolation of Latin runs.
- No heading or title in any language may contain hook, diagnosis, framework, vehicle, loop or CTA (or 钩子/诊断/框架/载体/循环/行动号召).

## Upgrading this skill

- Change design or behaviour once, in `assets/base/base.css`, `assets/base/runtime.js` or `scripts/build_page.py`; rebuild the example and run `check_page.py` before committing.
- New section = new key family in en.json + a block in `build_page.py` + a line in `references/page-structure.md`; old product dirs keep building because missing families should be guarded with `if N_x`.
- Bump `metadata.version` (major: section/key changes that need old pages re-translated; minor: new optional section; patch: fixes) and add one line to Version history.
- Sync: local copy `/workspace/smthelp-skill/smt-product-landing-page/` and GitHub `smthelp/smthelp-skill` (push each changed file with `scripts/push_github.py smthelp/smthelp-skill <file> smt-product-landing-page/<path>`).

## Version history

- 1.1.0 (2026-10-15) - gallery entries may use "file" (photo embedded once as WebP, `embed_px`/`embed_q`), SEO tags use only public URLs, lightbox falls back to the thumbnail, `calc_defaults` per product; second build: S-D508 lower cutting blade D508S4601007.
- 1.0.0 (2026-10-13) - extracted from the FUJI NXT Feeder Calibration Jig page; data-driven builder, asset harvester, quality gate, GitHub pusher.
