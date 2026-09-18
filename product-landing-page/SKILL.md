---
name: product-landing-page
description: Generate a single-file responsive HTML landing page for a Southern Machinery SMT/THT product (auto insertion, mounters, peripheral equipment, board handling, etc.) from local product folder content. Use when the user asks for a "landing page", "产品落地页", "single-page HTML", "product page", "marketing page", or wants to turn datasheets / brochures / quotation folders / NotebookLM notes / PPT decks for a specific machine model (e.g., S-680A, S3010A, S4000, S7020, S-600SV, S-V8, S380A) into one self-contained `.html` file with header logo, hero, features, specs, gallery, video, FAQ, and footer with social links. Also covers the optional multi-language + dark/light theme layer (多语言切换 / 明暗模式 / i18n), spec-vs-manual discrepancy disclosure, the Chatwoot support widget, and the mandatory headless verification pass before delivery.
---

# Skill: product-landing-page

Build **one self-contained `<MODEL>-Landing.html`** for a Southern Machinery product, using only catalog-grounded content from the project folder, plus the brand assets and social links below. Output must be a single file (no external CSS/JS files) using Tailwind-free hand-written CSS so it works offline by default.

When the user explicitly says the HTML will be shared directly with customers, remotely opened, or must not depend on local files, switch to **remote-share mode**: keep CSS inline, but reference only verified public URLs for product photos, videos, catalogs, manuals, and 3D HTML models. Do not embed local `/Volumes/...`, `file://`, extracted local images, or local PDF paths in the final HTML.

## When to use
Trigger on phrases like: `landing page`, `产品落地页`, `落地页`, `product page`, `single-file HTML`, `single-page HTML`, `marketing page`, `LP`, plus any Southern Machinery model code. Do **not** use this skill to build full multi-page sites or PPT decks — for slide decks use the `presentations` skill, for proposals use `gen-proposal`.

## Source-of-truth order (read in this order before writing any HTML)
1. Project-level `AGENT.md` / `AGENTS.md` (model identity, specs table, pain→value map, competitor map, file inventory).
2. Datasheet PDF for the model (often `*<MODEL>*.pdf` such as `S-680A SMT Reel Scrap Tape cutter  machine.pdf`).
3. Operating manual PDF (e.g., `S-680A SCRAP  TAPE  CUTTER.pdf`).
4. NotebookLM / FAQ markdown in the folder (`* 视频文案-PPT-开发信.md`, `* – Smart EMS factory partner.md`).
5. Existing per-product skill (e.g., `outputs/<MODEL>_Skill/SKILL.md`) — reuse its rules.
6. Existing legacy HTML in the folder (`*.html`) — extract any reusable copy, but **rewrite the layout from scratch** using the template below.

If a value is not in sources 1-4, mark it `TBC` or omit it. **Never** invent specs, prices, lead times, ROI numbers, customer names, or certifications.

## Required brand assets (always include verbatim)

- **Logo (header top-left + footer):** `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`
- **Footer social links (all five, in this order):**
  - LinkedIn Company Page — https://www.linkedin.com/company/smtmachine
  - LinkedIn Profile — https://cn.linkedin.com/in/smtsupplier
  - Twitter — https://twitter.com/smtspecialist
  - Facebook — https://www.facebook.com/autoinsertion
  - YouTube Channel — https://www.youtube.com/c/Smthelping
- **Footer resources line:** `Browse our machine catalog at file.autoinsertion.com and find machine photos at ph.smthelp.com.`
- **Contact block:** `jasonwu@smthelp.com` · `+86 13602562576` · `www.smthelp.com` · `Xixiang, Bao'an District, Shenzhen, China`
- **General inbox:** `info@smthelp.com` — use this for the public-facing contact/CTA when the user asks for a company address rather than a personal one. Both are valid; `jasonwu@` is the direct line, `info@` is the front door.

## Remote-share mode for customer-facing HTML

Use this mode when the user asks for a page they can send as a standalone HTML file and customers can open from another machine.

- **Images:** use `https://ph.smthelp.com/...` URLs only. Search by exact model code first, then product family keywords. Validate every embedded URL with `curl -sS -L -A "Mozilla/5.0" --max-time 40 -o /dev/null -w "%{http_code} size=%{size_download}"`. Embed only `200` responses with non-zero size.
- **Catalog/manual/3D resources:** use `https://file.autoinsertion.com` only after checking the exact link. Do not guess direct PDF or HTML paths. If a guessed file URL returns `404`, timeout, auth-gated content, or zero bytes, link to the stable product drive homepage and show the exact search phrase beside the button, such as `Search: S7900 ODD FORM MACHINE CATALOG 2025` or `Search: S7900 3D HTML model`.
- **NotebookLM:** when a matching product notebook exists, query it for customer-facing benefits, FAQ, and video/source URLs. Treat NotebookLM as a synthesis layer, not a substitute for catalog verification; hard specs still need catalog/PDF support.
- **No local embeds:** before delivery, scan the HTML for `file://`, `/Volumes/`, local project folder names, `./`, and `../`. Remove or replace any local references.
- **Link honesty:** never present an unverified catalog/manual/3D direct URL as a customer resource. Use a stable portal link plus search terms rather than a broken deep link.
- **Final resource section:** include a compact "Remote Resources" or "Catalog / Manual / 3D Model" section with `file.autoinsertion.com`, `ph.smthelp.com`, and exact search terms when public deep links are unavailable.

## Required page sections (in this order)
1. Top utility bar (phone + email).
2. **Sticky header** — logo (left, ~h:48px), nav anchors (Features / Specs / Gallery / Videos / FAQ / Contact), and a `Get a Quote` mini-CTA.
3. **Hero** — eyebrow tag, H1 with model + value verb, lead paragraph, 2-3 hero stats from the datasheet (e.g., 4× blade life, 76 mm/sec, < 6 mo payback), primary CTA + secondary `Watch It Run` button, hero image from `ph.smthelp.com`.
4. **Pain → Solution grid** (6 cards) — pull pain/value map from project `AGENT.md`.
5. **Features grid** (6-9 cards with icon, title, one-line description) — only catalog-backed features.
6. **Benefits / Operational Impact strip** (dark gradient) — 4 outcome stats; mark indicative ROI with an asterisk + footnote.
7. **Specifications table** — single column key/value, datasheet values only.
8. **Compatibility chips** — brand list (Yamaha / FUJI / JUKI / Samsung / Panasonic / Universal / Siemens-ASM) + tape/material list.
9. **Gallery** — at least 6 distinct product photos sourced via the **Sourcing product images** workflow below (local folder first, then `ph.smthelp.com`).
10. **Working video** — 2-6 YouTube embeds (lazy-loaded `iframe loading="lazy"`).
11. **Service strip** — Free Installation & Training · 1-Day Spare Parts · Worldwide Support · 12-Month Warranty.
12. **FAQ** — 6-8 `<details>` accordions sourced from NotebookLM markdown.
13. **Final CTA section** — "Email for Quote" + "WhatsApp Jason" buttons.
14. **Footer** — 4 columns: brand+social (5 icons), Product nav, Resources (file.autoinsertion.com, ph.smthelp.com, smthelp.com, original product page), Contact (email/phone/web/address). Bottom strip with the catalog/photos sentence and copyright.
15. **Floating WhatsApp FAB** bottom-right with deep-link to `https://api.whatsapp.com/send?phone=8613602562576&text=...`.

## Hard build rules
- **Single file.** Inline `<style>`. No Tailwind CDN, no external JS. SVG icons inline.
- **Responsive.** Mobile-first; collapse nav under `max-width:860px`; grids `auto-fit minmax(...)`.
- **Brand color tokens:** `--brand:#1C64F2`, `--brand-dark:#0d3b8c`, `--accent:#f59e0b`, `--ink:#0f172a`, `--bg:#f8fafc`. Use them via CSS variables.
- **Typography:** `Inter` from Google Fonts (`preconnect` + `display=swap`).
- **SEO:** `<title>`, `<meta name="description">`, `<meta name="keywords">` filled from the model's pain/value map.
- **Accessibility:** every `<a>` social/icon-only link gets `aria-label`; images get descriptive `alt`; `<iframe>` has `title` and `loading="lazy"`.
- **Output language:** customer-facing copy in **English** by default. Only switch to Chinese if the user explicitly requests `中文落地页`.
- **CTAs:** mailto with subject `Subject: <MODEL> Quote Request`; WhatsApp link `https://api.whatsapp.com/send?phone=8613602562576&text=Hi%20Jason%2C%20...`.
- **No invented numbers.** ROI shown only as ranges from the AGENT.md / Sales Playbook, with an asterisk pointing to a "validated case-by-case" footnote.
- **Every claim carries an evidence label.** `Verified data` / `Illustrative` / `To be confirmed`, applied inline. A number with no source in the folder does not go on the page.
- **Conflicting sources get a disclosure table**, never a silent pick. See "Evidence labels and document discrepancy disclosure".
- **YouTube embeds use `youtube-nocookie.com/embed/<id>`** with `loading="lazy"` and a `title`. Verify both the thumbnail (`i.ytimg.com/vi/<id>/hqdefault.jpg`) and the embed URL return `200` before shipping.
- **Interactive elements must degrade.** If a section ships as `<details>` accordions (long-form articles, FAQ), the content must be present in the DOM, not fetched — so the page still works opened from a local file with no network.
- **Never leave a raw i18n key on screen.** If the multi-language layer is present, an untranslated key must fall back to English, and the verification pass must prove it in all seven languages.

## Sourcing product images (always before writing the gallery / model cards)

Always inject **real product photos** — never use brand-logo placeholders or stock images. Resolve images in this order, then verify each URL returns HTTP 200 with `curl -sS -L -o /dev/null -w "%{http_code}"` before embedding:

### 1. Local product folder first
- Walk the project folder for image files: `*.jpg`, `*.jpeg`, `*.png`, `*.webp` (skip `Thumbs.db`, `~$*`, `._*` macOS resource forks).
- Open per-model PPT / PPTX / DOCX / PDF if needed (`pptx` -> `unzip -p ... ppt/media/*`, `pdf` -> `pdfimages` or render with `pdftoppm` / `pypdf` + `Pillow`).
- Prefer photos showing the actual machine front view, line install, HMI, magazine slot, NG/OK rack, etc. Save extracted images alongside the LP so the page works offline if needed.

### 2. Southern Machinery photo bank `https://ph.smthelp.com` (the brand image bank)
Use this when the local folder has no suitable image, or when richer real-factory shots are needed.

- **Search endpoint:** `https://ph.smthelp.com/search/images/?q=<keyword>` (URL-encode spaces as `+`). Run multiple specific queries — for BHS try: `loader`, `unloader`, `magazine`, `buffer`, `shuttle`, `conveyor`, `vacuum`, `destacker`, `telescopic`, `board+handling`, `SMT+line`, plus the exact model code (e.g. `SLD`, `SBH`, `SBM`).
- **Recent uploads:** `https://ph.smthelp.com/explore/recent` for the latest factory photos.
- **⚠️ Path gotcha (cost a full dead end on 2026-09-17):** the search path is `/search/images/?q=`, **not** `/search?q=`. The latter returns `404` with a valid-looking 25 KB HTML body, which reads like "the search feature is gone" and sends you off harvesting URLs from other pages instead. Verified 2026-09-18: `/search/images/?q=PCB+separator` → `200`, 24 results; `/search?q=PCB+separator` → `404`.
- **Extract candidate URLs from the returned HTML:**
  ```bash
  curl -sS -L -A "Mozilla/5.0" --max-time 20 "https://ph.smthelp.com/search/images/?q=<keyword>" \
    | grep -oE 'https://ph\.smthelp\.com/images/[^"'"'"'<> ]*\.(jpg|jpeg|png|webp|avif)' | sort -u
  ```
  **Include `webp` in the extension list.** As of 2026 the bank's newer uploads are served as `.md.webp` (e.g. `.../2026/09/14/smthelp-automatic-insertion-s7900-front-053a8ddbf9bc04a152.md.webp`). An extension list limited to `jpg|png` silently returns **zero** results for every recent upload — the query looks like it "found nothing" when it actually found 20+ images. Confirmed 2026-09-18: `.webp` returns `200` with `content-type: image/webp`.
- **Image URL conventions:**
  - `...md.jpg` / `...md.png` / `...md.webp` — medium thumbnail (~13-200 KB). **Use these in the LP** for fast loading.
  - Same path without `.md` (e.g. `PCB-loader-SLD-400B---1.jpg`) — original full-resolution image. Use only when a hero needs print-quality detail.
  - Some paths carry a content hash before `.md` (e.g. `...-front-053a8ddbf9bc04a152.md.webp`). Keep the hash exactly as returned — dropping it yields a 404.
  - The path itself encodes upload date + product, so URLs are stable and can be embedded directly without rehosting.
- **Validate before embedding:** `HEAD` is unreliable on this server — always use `GET` with `-o /dev/null -w "%{http_code} size=%{size_download}"` to confirm 200 + non-zero size.
- **Network-restricted environments:** if outbound `curl` is sandboxed, request escalation with prefix rule `["curl"]` and justification "需要从 ph.smthelp.com 拉取产品图片".

### 3. Per-machine BHS image cheat-sheet (proven URLs)
For Board Handling Equipments, these `ph.smthelp.com` images are pre-validated and can be reused:

| Module | Suggested image |
|---|---|
| Magazine loader (SLD) | `/images/2023/05/05/PCB-loader-SLD-400B---1.md.jpg` |
| Magazine unloader (SUL/SULD) | `/images/2025/10/20/PCB-unloader.md.png` |
| NG/OK dual unloader (SBH) | `/images/2023/05/05/Southern-Machinery-Board-Handling-System-NGOK-buffer.md.jpg` |
| Vacuum loader 1.5 m LED (SVL330) | `/images/2023/05/05/1.5m-LED-vacuum-loader-drawing.md.png` |
| Destacker / bare-board loader (SLC) | `/images/2023/05/05/Destacker--Magazine-Combo-PCB-loader-2.md.jpg` |
| Inline conveyor / buffer | `/images/2023/07/23/1-Hour-200-boards-storage-Buffer-Conveyor.md.png` |
| 10-layer buffer | `/images/2023/07/23/10-layer-Buffer-conveyor-Front-view.md.png` |
| Shuttle / translation (SPD) | `/images/2023/04/10/SMT-Shuttle-conveyor-1.md.png` |
| Magazine buffer (SBM) | `/images/2023/05/05/Southern-Machinery-Board-Handling-System-Magazine-buffer.md.jpg` |
| NG/OK buffer in customer line | `/images/2023/05/05/BufferNGOK-unloader-in-SK.md.jpg` |
| Telescopic gate (SAC460) | `/images/2023/05/05/Telescopic-gate-conveyor.md.jpg` |
| Full SMT/THT line hero | `/images/2025/12/06/THT-Auto-Insertion-production-line-1.md.png` |

When sourcing for other product families (S3010A radial, S4000 axial, S7020 odd-form, S-600SV / S-V8 mounters, S-680A scrap-tape cutter, etc.), run `https://ph.smthelp.com/search/images/?q=<MODEL>` first; the photo bank already hosts thousands of real-factory shots.

### 4. Embedding rules
- Each `<img>` must have a descriptive `alt` (model + view, e.g. `alt="SBH390 NG OK dual unloader front view"`).
- All non-hero `<img>` elements use `loading="lazy"` and a fixed aspect-ratio container so the page does not jump while loading.
- For model cards, embed the photo above the headline in a 4:3 `.pic` wrapper with `object-fit:cover`.
- Aim for ≥ 6 distinct photos in the gallery and 1 photo per model card. If fewer than 6 unique photos are available, fall back to a 3-photo gallery rather than reusing the same shot.
- Never inline base64 images larger than 50 KB; reference `https://ph.smthelp.com/...` directly.

### 5. Red lines
- Do not embed images from the `Competitor/` directory or any customer-supplied PDFs (Vestel, etc.).
- Do not embed CE/RoHS report screenshots into marketing pages — keep those as PDF attachments.
- Do not crop/edit images that contain customer logos or operator faces without explicit clearance.

## Evidence labels and document discrepancy disclosure

Every page carries three evidence labels, applied inline wherever a claim appears:

| Label | Means | Use for |
|---|---|---|
| `Verified data` (已验证资料) | Has a citable source in the folder | Datasheet / manual values, real photos, tested video IDs |
| `Illustrative` (概念示意) | Rendered or indicative | CAD renders, workflow diagrams, illustrative layouts |
| `To be confirmed` (待确认) | Conflicting or unproven | Values the sources disagree on, unconfirmed options |

**When the datasheet and the operating manual disagree, do not pick one, do not average, and do not stay silent.** Publish a dedicated disclosure table:

```md
| Parameter | Datasheet | 2023 manual | Status | What to do |
|---|---|---|---|---|
| Machine length | 1180 mm | 1230 mm | To be confirmed | Confirm against the final outline drawing before ordering |
```

Real example — the S380A spec sheet and its 2023 manual disagreed on four points (overall length 1180 vs 1230 mm; working area 350×550 vs L350×W330 mm; automatic tool change listed as a Q380A-only configuration; outline-drawing dimensions matching neither document). All four were published in a `To be confirmed` table with a "what to do" column.

**This is a trust asset, not an embarrassment.** A buyer who discovers an inconsistency you disclosed trusts the rest of the page more; a buyer who discovers one you hid questions everything. It also protects the salesperson — the page itself now carries the "confirm before ordering" instruction.

## Multi-language + theme layer

Add this layer when the user asks for 多语言切换 / 语言切换 / i18n / multi-language, or 暗黑模式 / 明暗模式 / dark mode / theme toggle. Skip it for a single-market internal page.

### Languages and order
Default **English**, then in this order: `es` Spanish, `pt` Portuguese, `fr` French, `ar` Arabic (**RTL**), `ru` Russian, `zh` Chinese.

### Markup contract
Write the **English original directly in the markup** — it is the fallback source. Do **not** extract strings into a separate JSON file.

```html
<h2 data-i18n="s02_h">The machine</h2>
<input data-i18n-ph="calc_price_ph" placeholder="Machine investment (USD)">
<a data-i18n-title="soc_li_t" title="LinkedIn company page">
```

Three attributes cover `textContent`, `placeholder`, and `title`.

### Runtime contract

```js
const LANGS=[{code:"en",label:"English",short:"EN"},/* es,pt,fr,ar,ru,zh */];
const DIRS={en:"ltr",es:"ltr",pt:"ltr",fr:"ltr",ar:"rtl",ru:"ltr",zh:"ltr"};
const I18N={en:{},es:{},pt:{},fr:{},ar:{},ru:{},zh:{}};
const EN_SNAPSHOT={};

// 1) Capture the English originals BEFORE any swap happens
function snapshotEnglish(){
  document.querySelectorAll("[data-i18n]").forEach(function(el){
    EN_SNAPSHOT[el.getAttribute("data-i18n")]=el.textContent;
  });
  /* same for data-i18n-ph / data-i18n-title */
}

// 2) Resolve: current language -> English snapshot -> key name
function T(lang,key){
  var d=I18N[lang]; if(d&&d[key]!==undefined) return d[key];
  if(EN_SNAPSHOT[key]!==undefined) return EN_SNAPSHOT[key];
  var e=I18N.en[key]; return e===undefined?key:e;
}
```

`EN_SNAPSHOT` fallback is what makes "translate half of it" viable: an untranslated key degrades to readable English instead of leaking `s02_h` onto the page. With 500+ keys × 7 languages this is the only realistic path.

### JS-generated strings must be merged separately
Anything the renderer writes itself — calculator units, video card titles — **never appears in the markup**, so `EN_SNAPSHOT` cannot capture it and `T()` returns the bare key. Merge it explicitly:

```js
(function(){
  var EXTRA={
    en:{ unit_sec:"s", unit_h:"h", unit_month:"months", unit_year:"years",
         calc_needinput:"Enter the labour cost to see a payback period" },
    zh:{ unit_sec:"秒", unit_h:"小时", unit_month:"个月", unit_year:"年",
         calc_needinput:"填入人工成本即可看到回本周期" }, /* ... */
  };
  Object.keys(EXTRA).forEach(function(l){
    if(!I18N[l]) I18N[l]={};
    Object.keys(EXTRA[l]).forEach(function(k){ I18N[l][k]=EXTRA[l][k]; });
  });
})();
```

This bug shipped once already: the English UI rendered `40.0 unit_sec`. A headless check caught it — not a human reading the page.

### Long-form body copy may stay English
Translate **headings and standfirsts** of long articles; leave the body English and say so in a code comment. Machine-translated B2B technical prose reads worse than plain English and damages credibility. Do not chase 100% key coverage at the cost of that.

### Persistence and override
- `localStorage` keys: `<model>_lang` and `<model>_theme`.
- `?lang=xx` in the URL **wins over** the stored preference (lets you send a targeted link to a Spanish buyer).
- First visit picks up the theme from `prefers-color-scheme`.
- `applyLang` must also set `document.documentElement.lang` and `dir` (from `DIRS`).
- Re-render JS-generated content (video grid, calculator) inside `applyLang`, otherwise it stays in the previous language.

### Theme
The template already defines `html[data-theme="dark"]` token overrides, so the toggle only has to:

```js
function applyTheme(mode,persist){
  document.documentElement.setAttribute("data-theme",mode);
  themeIcon.textContent = mode==="dark" ? "☀" : "☾";
  themeColorMeta.setAttribute("content", mode==="dark" ? "#0e1116" : "#ffffff");
  if(persist) localStorage.setItem(THEME_KEY,mode);
}
```

**Reuse the existing CSS variables — never author a second palette for dark mode.**

## Support widget (Chatwoot)

When the user supplies a Chatwoot snippet, keep their `websiteToken` and hostname, but make the base URL follow the page protocol:

```js
var BASE_URL=(location.protocol==="https:"?"https://":"http://")+"chat.smthelp.com";
```

A user-supplied `http://` base URL on an `https://` page is blocked as mixed content and the launcher **fails silently** — no error, no widget, and it looks like the snippet was never added. Also add CSS pinning the launcher to the bottom-right so page layout cannot displace it.

## Headless verification (required before delivery)

Do not sign off on a landing page by scrolling it. Run the runtime in `jsdom` and assert on the DOM.

**Do not copy and edit the script.** The harness takes a second argument: a JSON config whose keys deep-merge into `CFG`. Page-specific values live in that file, so the script itself stays identical across models and can be updated in one place.

```bash
# jsdom must be installed somewhere writable. The managed node workspace under
# ~/.workbuddy-ai/binaries/node/workspace is often READ-ONLY inside the sandbox:
# npm reports "up to date" and silently creates no node_modules. Install next to
# the page instead, and point NODE_PATH at it.
mkdir -p <work>/verify && cd <work>/verify && npm init -y && npm install jsdom

NODE_PATH=<work>/verify/node_modules \
/Users/jasonwu/.workbuddy-ai/binaries/node/versions/22.22.2-2/bin/node \
  verify_landing_page.js "/abs/path/to/<MODEL>-...-Landing.html" \
  <work>/verify/<model>.config.json
```

`templates/example.config.json` is a complete worked example (the S7020T terminal-insertion calculator). JSON has no regex literal, so **write every regex with slashes** — `"/^400$/"`, `"/216[.,]?\\s?000/"`, `"month"`. A bare `"^400$"` stays a string and the harness dies with `s.re.test is not a function`.

Config keys worth setting per page:

| Key | Why it is page-specific |
|---|---|
| `langKey` / `themeKey` | each page namespaces its `localStorage` (e.g. `s7020t_lang`) |
| `chatwoot.token` / `launcherTitle` | the widget is per-site |
| `calc.inputs` / `outputs` | the field ids differ per machine |
| `calc.steps[]` | `{out, re, label}` — the arithmetic assertions. **Recompute by hand from the page's own formula** and put the expected value in `re`; the label states the formula so a future reader can re-derive it. |
| `calc.degenerate[]` | `{label, set, watch}` — drive inputs to zero / absurd values and assert the watched output never renders `Infinity` or `NaN` |
| `minStepsPerPost` | a **floor**, not an exact count (see below) |

Checks for features the page does not have are reported as `SKIP`, not `FAIL`, so one harness covers a plain English page and a full 7-language build. **Read the SKIP list before signing off** — a page that was supposed to ship the language layer but reports 20 skips is a defect, not a pass.

Minimum coverage — all twelve groups must pass:

1. **Boots clean** — load with `runScripts:"dangerously"`, capture `window.onerror`.
2. **No raw keys** — for every language, every `data-i18n` / `data-i18n-alt` / `data-i18n-ph` element must render something other than its own key name. Also assert the localised SEO title and description fit the SERP width budget.
3. **Translations are real** — spot-check with CJK / Cyrillic / Arabic regexes so a "translated" table that is still English fails.
4. **Video grid** — expected card count, non-empty titles.
5. **Theme toggle** — `data-theme` flips and `localStorage` is written.
6. **Persistence across reload** — rebuild the DOM with the same storage object, and check `?lang=` overrides it.
7. **Calculator arithmetic** — recompute by hand and compare; then push degenerate inputs.
7b. **Calculator localisation** — assert the output contains **no** `unit_*` / `calc_*` literal key names, in all seven languages.
8. **Language menu** — entry count, order, `aria-current`.
9. **Content integrity** — article count × step floor, banned-word scan, FAQ count, JSON-LD node types, **FAQPage count equals the visible FAQ count**, hreflang with `x-default`.
10. **Images** — at least N served from `ph.smthelp.com`, zero base64 placeholders, every `img` has `alt`, below-the-fold images lazy.
11. **Print `ALL CHECKS PASSED`.** **If any check is red, fix it before delivery** — that is the whole point.

### Two failure modes this harness exists to catch

**A key referenced only from JavaScript.** A `T(lang, "key")` call inside the runtime — or a key reached through a data array like `VIDEOS = [{id, t:"v1t", d:"v1d"}]` — never appears in the markup. An extractor that reads `data-i18n` attributes only will not see it, `I18N.en` will not contain it, and `T()` will fall back to the **bare key name** in every language. The page looks fine in English until you notice a card titled `v1t`. Guard it: after extraction, scan the runtime for `T(<lang>, "key")` and for `t:"..." / d:"..."` array fields, and fail the build if any key is absent from `I18N.en`.

**An exact-count structural assertion.** `article.querySelectorAll(".step").length === 6` fails on legitimate editorial variance (one article is tighter, another runs longer), and the usual response is to lower the number until it passes — at which point it catches nothing. Assert a **floor** (`>= N`) instead: it still catches the failure that matters (an article that lost its body) without punishing a short article. And make sure the selector actually matches your markup: a paragraph written `<p><b>Question…</b></p>` is not matched by `<p>(?=[^<\s])`, so nine paragraphs of a nine-question article silently stay unmarked.

### SERP width is not character count
`displayWidth()` counts CJK as 2, narrow characters (`iljtfrI.,'|:;()[]-/ `) as 0.5, uppercase as 1.15, else 1. Limits: title ≤ 60 units, description ≤ 160 units. **This must be applied per language** — a translated title that fits in Chinese can overflow badly in Russian or French. Budget for it when you write the translation, not after.

### Banned-word scan
When the brief forbids certain words in titles (e.g. hook / diagnosis / framework / vehicle / loop / CTA), scan `h1,h2,h3,h4,title,summary` `textContent` case-insensitively in the script. Never eyeball it.

## Workflow
1. **Inventory** the project folder for the model: read `AGENT.md`, datasheet PDF, manual PDF, FAQ markdown, existing `*.html`. Record specs verbatim into a values dict.
2. **Cross-check the datasheet against the manual.** List every parameter where the two disagree. Do not resolve them silently — they become the `To be confirmed` disclosure table (see above). Extract PDF text with `pdftotext -layout` rather than a Python PDF library; it is already installed and does not need a venv.
3. **Build copy** for each section using only catalog-backed bullets; tag uncertain items with an evidence label.
4. **Render HTML** using `templates/landing_template.html` as a structural reference (copy its skeleton then fill placeholders). If the workspace blocks direct writes, write to `/tmp/<MODEL>-LP.html` then `cp` into the project folder.
5. **Add the optional layers** if requested: multi-language + theme, Chatwoot widget. Reuse the template's existing CSS variables and component classes — do not author a parallel design system.
6. **Verify headlessly** with `templates/verify_landing_page.js`. All checks must pass. Extract the runtime `<script>` and run `node --check` on it first — a stray ASCII `"` inside a Chinese translation string is the single most common syntax killer.
7. **Self-check** against `templates/qa_checklist.md` (logo present, all 5 social links, file.autoinsertion.com + ph.smthelp.com sentence, no invented prices/lead time, mobile breakpoints, alt text, lazy iframes, CTA links work).
8. **Emit final answer**: file path + a 5-bullet summary of what's in each major section + a "下周必做动作" line.

For remote-share mode, add these self-checks before step 8:
- Every `<img>` URL is from `https://ph.smthelp.com` and was validated with HTTP `200` + non-zero size.
- Every catalog/manual/3D-model URL is either a verified public deep link or the stable `https://file.autoinsertion.com` portal with exact search terms shown in the page.
- No local filesystem paths or local documents are referenced in the HTML.
- Every external asset URL (images, video thumbnails, embeds) was checked with `curl -sS -L -o /dev/null -w "%{http_code} size=%{size_download}"` and returned `200` with non-zero size.

### Pushing the page to a repository
- Landing pages go to `smthelping/smt-product-landing-html`. ⚠️ `smthelp111/smt-product-landing-html` is a **same-named public repo** — verify the account and the target before pushing, or private content can land in a public repo.
- Run `gh auth status` first. `smthelping` holds write access to the landing-page repo; `smthelp` holds it for `smthelp-skill`. Switch with `gh auth switch --user <name>`, push, then switch back. `gh api user --jq .login` is the reliable check — the active account can differ from what you last set.
- A `403 Permission ... denied to <account>` on push means you are on the wrong account — switch, do not force.
- Update `README.md` with an index row for the new page in the same commit.
- **Strip visual-editor metadata before publishing.** If the HTML was ever opened in a WYSIWYG/visual editor, every element gains a `data-page-node-id="..."` attribute — roughly 40 KB of editor bookkeeping on a 400 KB page. It is not part of the artifact. Remove it in the push copy only, leaving the working file untouched so the editor can still open it:
  ```bash
  python3 -c "import re,sys;s=open(sys.argv[1],encoding='utf-8').read();open(sys.argv[2],'w',encoding='utf-8').write(re.sub(r'\s+data-page-node-id=\"[^\"]*\"','',s))" in.html out.html
  ```
  Verify the cleaned copy before pushing — the regex must not touch anything else.

## Output filename convention
`<MODEL>-<short-product-name>-Landing.html` written to the project root, e.g.:
- `S-680A-SMT-Scrap-Tape-Cutter-Landing.html`
- `S3010A-Radial-Auto-Insertion-Landing.html`

When the page is intended to rank (public URL, indexed, linked from the site), use a lowercase SEO/GEO slug instead — model + core function + category keywords, no stop words:
- `s380a-vision-pcb-separator-machine-v-cut-curve-depaneling.html`

The slug should read as the search query a buyer would type. Keep the `hreflang` alternates and the JSON-LD `@graph` in sync with whatever slug you choose.

## Version history
- **v1.2** (2026-09-18) — Verification harness made genuinely reusable: `verify_landing_page.js` now takes a **JSON config** as a second argument (deep-merged into `CFG`, with `/…/` strings revived as regexes), so the page-specific ids, storage keys and calculator arithmetic live beside the page instead of being edited into the script. Group 7 no longer hardcodes the S380A conveyor formula — `calc.steps[]` / `calc.degenerate[]` drive it. Exact `stepsPerPost` replaced by a floor `minStepsPerPost`. Added `templates/example.config.json`. Documented two failure modes this harness exists to catch: a key referenced only from JavaScript (invisible to a `data-i18n` extractor, falls back to the bare key name in every language) and an exact-count structural assertion that gets weakened until it catches nothing. Also documented that the managed node workspace is read-only inside the sandbox — `npm install jsdom` there reports "up to date" and creates nothing, so install next to the page. Distilled from the S7020T terminal insertion machine build.
- **v1.1** (2026-09-18) — Added: evidence labels and datasheet-vs-manual discrepancy disclosure; multi-language + theme layer; Chatwoot support widget; mandatory headless verification pass; repository push rules. Fixed two image-sourcing defects: the documented search path `/search?q=` 404s (correct path is `/search/images/?q=`) and the extraction regex omitted `webp`, which is what the bank now serves for all recent uploads. Added `templates/verify_landing_page.js`. Distilled from the S380A vision curved & V-cut PCB separator build.
- **v1.0** — Initial skill: single-file build, brand assets, remote-share mode, 15 required sections, image sourcing, QA checklist.

## After every artifact
End with a one-line `下周必做动作:` reminder telling the salesperson what to do with the page (e.g., "把 LP URL 嵌进 Day 7 跟进邮件 + LinkedIn DM").
