# Input contract

A case is a folder. Required = build fails or the page is wrong without it.

```
<case>/
  report.json          REQUIRED  report spec (below)
  photos/*.jpg         REQUIRED  ≥1 (hero); relative paths in report.json
  web/page.json        REQUIRED  page settings
  web/web_en.json      REQUIRED  SEO, quick answer, videos/catalogues, blogs, FAQ texts
  web/i18n/<l>.json    optional  translations (missing keys fall back to English)
```

## Content inputs from the user / source
| Field | Req. | Notes |
|---|---|---|
| Evaluation conclusion | required | result numbers, formulas, pass/fail, comparison, open points |
| Product / line name, machine models | required | models stay untranslated (S7900, SM-xxx …) |
| Customer alias | required | by industry: "LED Driver Manufacturer", "Surge Protection Device Manufacturer" |
| Board / part aliases | required when parts are named | Board 1…n, Module X/Y; real part numbers → `redact` |
| Industry background | required | what they make, why automation matters to them |
| Brand colours / logo | optional | default Southern Machinery (`config/brand.json`) |
| Tone | optional | `engineering-plain` default |
| Languages | optional | default 7 |

## report.json
`{"title": str, "lang": "en", "slides": [ ... ]}` — first slide `cover`, last slide `cta` (becomes the contact section).

| type | fields |
|---|---|
| cover | kicker, title, subtitle, image, metrics[{v,l}] ×4, notes |
| steps / cards | kicker, title, lead?, steps[{h,b}] / cards[{h,b}], image?, caption? |
| table | kicker, title, rows[[header…],[…]], note?, chart? `{label_col, cols[], mode: bars+table|bars|table}` |
| metrics | kicker, title, metrics[{v,l}], image?, text? |
| bullets | kicker, title, bullets[str], image?, caption? |
| gallery | kicker, title, images[{src,cap}] |
| cta | kicker, title, facts[{h,b}] ×3, text |

`notes` (never shown) carries the source and evidence label: "Concept view" → tag, "Estimate" → tag, "To be confirmed" → tag.
Numbers are written once in English format and are identical in every language. Cells matching model/alias patterns are not translated.

## web/page.json
| key | req. | meaning |
|---|---|---|
| file | required | `<keywords>-smart-ems-pcb-assembly.html` |
| canonical_base | required | public folder URL |
| storage_prefix | required | localStorage prefix, unique per page |
| langs | optional | default 7, English first |
| sections | optional | order of answer, report, videos, docs, blog, faq, contact |
| nav_slides | optional | slide indexes in the top menu |
| palette, brand | optional | overrides of config/brand.json |
| tone | optional | engineering-plain / sales-warm / executive-brief |
| about, hero_alt, breadcrumb, og_image, date_published | optional | SEO |
| videos[{id,t,d,dur}] | optional | 8 recommended, keys v1t/v1d… in web_en |
| catalogs[{url,t,d,type}] | optional | 6 recommended, keys cat1t/cat1d… |
| blogs, faq | optional | counts (8 / 6) |
| redact[] | required | every real name, part number, currency, country — build and check fail if found |

## web/web_en.json keys
seo_title, seo_desc, seo_keys · ans_h2, ans_p, qf1k…qf6v · vid_h2, vid_lead, v1t…v8d · cat_h2, cat_lead, cat1t…cat6d · blog_h2, blog_lead, bl1t, bl1s, bl1p1…bl1p6 (×8) · faq_h2, q1…q6, a1…a6 · ct_h2, ct_p. UI strings (nav_, ui_, tag_, foot_ …) come from templates/ui and may be overridden here.
