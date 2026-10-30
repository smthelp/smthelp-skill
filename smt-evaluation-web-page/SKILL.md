---
name: smt-evaluation-web-page
description: Turn a customer product / sample evaluation result, line proposal or quotation into ONE anonymous, multilingual (EN default + ES, PT, FR, AR rtl, RU, ZH), self-contained marketing HTML page for Southern Machinery — report sections, bar charts, quick answer (GEO), matched YouTube videos, catalogue viewer, 8 blogs, FAQ, JSON-LD, dark/light mode, Chatwoot. Use when Jason sends an evaluation/sample-test result, solution proposal or quotation and asks for a web page, landing page, HTML report or "the same multilingual single-HTML method".
version: 1.0.0
metadata:
  author: Southern Machinery (Jason Wu) · built with Hark
  repo: https://github.com/smthelp/smthelp-skill/tree/main/smt-evaluation-web-page
  origin: generalised from smt-sample-evaluation-report v2.2.0 render_web.py (LED driver THT line, LED T8 SMT line, odd-form SPD insertion cases, 2026-10-27)
  changelog: references/changelog.md
---

# smt-evaluation-web-page

Customer evaluation result → one `.html` file that opens offline by double-click, reads well on a phone, switches between 7 languages and never shows who the customer is or what they paid.

## When to use
- An evaluation / sample-test result, a line proposal or a quotation should become a public or shareable web page.
- Jason says "same method / 同样的方法 / 多语言单 HTML" for a new case.
- Not for: a single product landing page (use `smt-product-landing-page`), a PPT deck (use `smt-sample-evaluation-report`), a full supplier brand kit (use `smt-brand-kit`).

## Input contract (details: references/input-contract.md)
| Input | Req. | Where it goes |
|---|---|---|
| Evaluation conclusion (result numbers, cycle/capacity, pass/fail, open points) | **required** | `report.json` slides (table/metrics/bullets) |
| Product / line name and machine models | **required** | cover title, `seo_title`, `about` |
| Customer alias (never the real name) and board/part aliases (Board 1…, Module X…) | **required** | all texts; real names go to `redact` |
| Industry background (what the customer makes, why it matters) | **required** | cover subtitle, quick answer, blogs |
| Source documents (PDF/PPT/photos) | **required** | facts table, `photos/` |
| Brand colours / logo / contacts | optional (default `config/brand.json`) | `page.json → brand`, `palette` |
| Section order, menu items, chart form, tone | optional | `page.json → sections`, `nav_slides`, slide `chart`, `tone` |
| Videos, catalogues | optional (recommended 8 / 6) | `page.json → videos`, `catalogs` |
| Languages | optional (default all 7) | `page.json → langs` |

## Output contract (details: references/output-contract.md)
- Exactly **one** `.html` file, name `<keywords>-smart-ems-pcb-assembly.html`, all CSS/JS/images/logo inlined (base64). No build step to view it.
- Works offline: every report section, chart, table, language and theme switch. Online-only extras (YouTube player and thumbnails, catalogue iframe, Chatwoot) load only from `brand.cdn_whitelist` hosts and fail silently.
- Semantic HTML (`header/nav/main/section/figure/table/details/footer`), responsive at 360–1440 px, print stylesheet, Arabic `dir=rtl`.
- Language and theme remembered in localStorage (`page.json → storage_prefix`), `?lang=xx` overrides.
- SEO/GEO: title, description, keywords, canonical, hreflang × langs, OG/Twitter, JSON-LD (Organization, Report, FAQPage, Blog, VideoObject list, BreadcrumbList), quick-answer block.
- Contains none of the `redact` terms, no prices, payment terms, lead times, contacts or destination country of the customer.

## Workflow
1. **Read every source** (OCR scanned PDFs: `pdftoppm -r 200` + `tesseract`; view slides as contact sheets). Build a facts list with labels *Verified source / Concept view / Estimate / To be confirmed*. Recompute every derived number (cycle, capacity, refill counts); where the source disagrees with itself, keep the source value, add it to the open-points slide and tag the slide `To be confirmed`.
2. **Anonymise**: choose customer alias by industry (e.g. "Surge Protection Device Manufacturer"), rename boards/parts, write a competitor as "reference machine". Put every real name, part number, currency and country into `page.json → redact`.
3. **Scaffold**: `python3 scripts/new_case.py <case_dir>` (copies `examples/_template`). Crop photos from the source (`photos/`), blur customer logos/names, check each crop visually before captioning.
4. **Write `report.json`** (slide types in references/input-contract.md). Cover → how it works → inputs → results (table + `chart`) → comparison → method/tech → specs → design rules → gallery → support → accuracy & open points → next steps (`cta`, last).
5. **Write `web/web_en.json`**: SEO, quick answer (`ans_*`, `qf1..6`), 8 video and 6 catalogue texts, 8 blogs in the six-step order (references/copywriting.md), 6 FAQ, `ct_*`. Match videos from the YouTube board and catalogues from the catalogue board (references/sources.md).
6. `python3 scripts/build_page.py export <case_dir>` → `web/strings_en.json`.
7. **Translate in parallel**: one sub-agent per 1–2 languages with references/translation-brief.md → `web/i18n/<lang>.json` (same keys). UI strings are already in `templates/ui/`.
8. `python3 scripts/build_page.py build <case_dir> <out_dir>` (exit 1 on forbidden title words or redact hits).
9. `python3 scripts/check_page.py <out_dir>/<file>.html --case <case_dir>` → all checks PASS, then the jsdom smoke test (`scripts/smoke_test.js`).
10. Deliver the file to Jason; list open points as questions. Copy the case into `examples/` only with his OK.

## Configuration (all optional, in `web/page.json`)
- `sections`: order/selection of `answer, report, videos, docs, blog, faq, contact`.
- `nav_slides`: slide indexes shown in the top menu (default `[1,2]`).
- `palette`: `{"light":{...},"dark":{...}}` overrides of CSS variables (`navy, teal, green, bg, fg, card, line, head, sub, hero1-3`).
- `brand`: deep-merge over `config/brand.json` (logo, contacts, socials, Chatwoot, CDN whitelist, forbidden words).
- slide `chart`: `{"label_col":0,"cols":[3,5],"mode":"bars+table"|"bars"|"table"}` — horizontal CSS bar chart, no chart library.
- `tone`: `engineering-plain` (default) | `sales-warm` | `executive-brief` — governs copy (references/copywriting.md), not code.
- `about`, `hero_alt`, `breadcrumb`, `og_image`, `storage_prefix`, `date_published`, `redact`.

## Quality gate — check before delivery (references/qa-checklist.md)
check_page.py automates: single file, no external CSS/JS except whitelisted hosts, all `<img>` data-URIs except YouTube thumbnails, viewport meta, semantic tags, 7 languages with equal key sets, numbers identical across languages, forbidden title words, redact terms, Chatwoot token, hreflang, JSON-LD parses, size < 3 MB.
Manual: crops checked visually, open points listed, alias consistent, no price/terms/contacts/country.

## Upgrading
Change `templates/` or `scripts/`, rebuild `examples/odd-form-spd-line`, run check + smoke test, bump `version` here (`python3 scripts/bump_version.py minor "note"`), add a line to references/changelog.md, commit `smt-evaluation-web-page vX.Y.Z: <what>` and tag `smt-evaluation-web-page-vX.Y.Z`.

## Files
- `config/brand.json` brand defaults · `templates/page.html|page.css|page.js` page shell · `templates/ui/<lang>.json` UI strings
- `scripts/build_page.py` export/build · `scripts/check_page.py` QA · `scripts/new_case.py` scaffold · `scripts/bump_version.py` · `scripts/smoke_test.js`
- `examples/_template` empty case · `examples/odd-form-spd-line` full 7-language case
- `references/` input/output contracts, copywriting, translation brief, sources, QA checklist, changelog
