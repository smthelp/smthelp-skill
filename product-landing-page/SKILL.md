---
name: product-landing-page
description: Generate a single-file responsive HTML landing page for a Southern Machinery SMT/THT product (auto insertion, mounters, peripheral equipment, board handling, etc.) from local product folder content. Use when the user asks for a "landing page", "产品落地页", "single-page HTML", "product page", "marketing page", or wants to turn datasheets / brochures / quotation folders / NotebookLM notes / PPT decks for a specific machine model (e.g., S-680A, S3010A, S4000, S7020, S-600SV, S-V8) into one self-contained `.html` file with header logo, hero, features, specs, gallery, video, FAQ, and footer with social links.
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
- **Extract candidate URLs from the returned HTML:**
  ```bash
  curl -sS -L -A "Mozilla/5.0" --max-time 20 "https://ph.smthelp.com/search/images/?q=<keyword>" \
    | grep -oE '"https://ph\.smthelp\.com/images/[^"]+\.md\.(jpg|png)"' | sort -u
  ```
- **Image URL conventions:**
  - `...md.jpg` / `...md.png` — medium thumbnail (~30-200 KB). **Use these in the LP** for fast loading.
  - Same path without `.md` (e.g. `PCB-loader-SLD-400B---1.jpg`) — original full-resolution image. Use only when a hero needs print-quality detail.
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

## Workflow
1. **Inventory** the project folder for the model: read `AGENT.md`, datasheet PDF, manual PDF, FAQ markdown, existing `*.html`. Record specs verbatim into a values dict.
2. **Build copy** for each section using only catalog-backed bullets; mark uncertain items `TBC`.
3. **Render HTML** using `templates/landing_template.html` as a structural reference (copy its skeleton then fill placeholders). If the workspace blocks direct writes, write to `/tmp/<MODEL>-LP.html` then `cp` into the project folder.
4. **Self-check** against `templates/qa_checklist.md` (logo present, all 5 social links, file.autoinsertion.com + ph.smthelp.com sentence, no invented prices/lead time, mobile breakpoints, alt text, lazy iframes, CTA links work).
5. **Emit final answer**: file path + a 5-bullet summary of what's in each major section + a "下周必做动作" line.

For remote-share mode, add these self-checks before step 5:
- Every `<img>` URL is from `https://ph.smthelp.com` and was validated with HTTP `200` + non-zero size.
- Every catalog/manual/3D-model URL is either a verified public deep link or the stable `https://file.autoinsertion.com` portal with exact search terms shown in the page.
- No local filesystem paths or local documents are referenced in the HTML.

## Output filename convention
`<MODEL>-<short-product-name>-Landing.html` written to the project root, e.g.:
- `S-680A-SMT-Scrap-Tape-Cutter-Landing.html`
- `S3010A-Radial-Auto-Insertion-Landing.html`

## After every artifact
End with a one-line `下周必做动作:` reminder telling the salesperson what to do with the page (e.g., "把 LP URL 嵌进 Day 7 跟进邮件 + LinkedIn DM").
