---
name: product-blog-geo-seo
description: Generate a single-file responsive HTML GEO/SEO blog article for a Southern Machinery SMT/THT product (auto insertion, mounters, peripheral equipment, board handling, scrap tape cutters, etc.) from local product folder content. Use when the user asks for a "blog", "GEO/SEO blog", "营销博客", "产品博客", "SEO article", "long-form article", "ROI 博客", "5S 博客", "labor saving 文章", or wants to turn datasheets / quotation folders / NotebookLM notes for a specific machine model (e.g., S-680A, S3010A, S4000, S7020, S-600SV, S-V8) into one self-contained `.html` blog file with header logo, hero, body sections, FAQ schema, JSON-LD, and footer social links. Distinct from product-landing-page (which is a sales LP) — this skill produces an editorial article optimized for organic search and AI-assistant retrieval (GEO).
---

# Skill: product-blog-geo-seo

Build **one self-contained `<MODEL>-<topic>-Blog.html`** GEO/SEO blog article for a Southern Machinery product. Output must be a single file (inline CSS, no external JS, no Tailwind) so it can be uploaded to any CMS or hosted standalone. Article must be grounded in the project folder's catalog/datasheet/manual; never invent specs, prices, lead times, certifications, ROI figures, or customer names.

## When to use
Trigger on phrases like: `blog`, `GEO blog`, `SEO blog`, `营销博客`, `产品博客`, `long-form article`, `ROI blog`, `5S blog`, `labor saving article`, `case-study article`, plus any Southern Machinery model code. Do **not** use this skill for: short LinkedIn posts (use `gen-outreach`), full landing pages (use `product-landing-page`), proposal documents (use `gen-proposal`), or NotebookLM exports.

## Source-of-truth order (read in this order before writing any HTML)
1. Project-level `AGENT.md` / `AGENTS.md` — model identity, specs table, pain→value map, competitor map, red lines.
2. Datasheet PDF for the model (often `*<MODEL>*.pdf`).
3. Operating manual PDF (e.g., `S-680A SCRAP  TAPE  CUTTER.pdf`).
4. ROI / sales-playbook layers in `outputs/<MODEL>_Sales_Playbook/` (especially Layer 3 Value/ROI).
5. NotebookLM / FAQ markdown in the folder (`* 视频文案-PPT-开发信.md`, `* – Smart EMS factory partner.md`).
6. Existing per-product skill (e.g., `outputs/<MODEL>_Skill/SKILL.md`) — reuse its hard rules.
7. Existing legacy HTML in the folder (`*.html`) — extract reusable copy, but **rewrite the layout from scratch** using the template below.

If a value is not in sources 1-5, mark it `TBC` or omit it. Never invent. Wage / payback figures must be presented as illustrative scenarios with assumptions transparently listed.

## Required brand assets (always include verbatim)

- **Logo (header top-left + footer):** `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`
- **Footer social links (all five, in this order):**
  - LinkedIn Company Page — https://www.linkedin.com/company/smtmachine
  - LinkedIn Profile — https://cn.linkedin.com/in/smtsupplier
  - Twitter — https://twitter.com/smtspecialist
  - Facebook — https://www.facebook.com/autoinsertion
  - YouTube Channel — https://www.youtube.com/c/Smthelping
- **Footer resources line:** `Browse our machine catalog at file.autoinsertion.com and find machine photos at ph.smthelp.com.`
- **Contact block:** `jasonwu@smthelp.com` · `+86 13602562576` · `www.smthelp.com` · Shenzhen, China.

## Topic angles (pick 1–2 per blog)
- 5S in SMT / lean factory floor
- Labor saving / headcount per line
- ROI / payback months / CFO conversation
- Pickup-fault / downtime reduction
- Compatibility with Yamaha / FUJI / JUKI / Samsung / Panasonic / Universal
- Competitor compare (Universal EU570SA / EU900SA, JUKI, OEM cutters) — factual, no disparagement
- Free Trial / Conditional PO program
- Industry segment (LED, automotive, consumer, industrial control)

## Required page sections (in this order)
1. **`<head>`** — semantic title (≤ 65 chars), meta description (140-170 chars), canonical, Open Graph + Twitter cards, JSON-LD (`Article` + `Product` + `FAQPage`), Inter web font.
2. **Sticky header** — logo (left, h≈56px) linked to `https://www.smthelp.com`, nav (SMT / THT / Peripheral / Blog), `Get Quote` mini-CTA mailto.
3. **Hero** — eyebrow meta (series + date + read-time + author), H1 with model + benefit verb, lead paragraph, 4 hero stats from the datasheet.
4. **Article body** in a centered white card overlapping the hero (negative margin) with these subsections:
   - Search-friendly summary paragraph (1 paragraph, italic).
   - **Table of contents** (anchor list).
   - 1-2 problem-framing sections ("Why now").
   - "What the product is" — datasheet specs as `<table class="spec">`.
   - 5S / labor / ROI / compatibility / competitor sections per chosen topic angles.
   - **Transparent ROI math**: formula in `<blockquote>`, scenario table, source-of-truth callout.
   - Deployment checklist + FAQ (`<details class="faq">` × 4–6, mirroring JSON-LD `FAQPage`).
   - Inline CTA box (gradient brand background, mailto with prefilled subject + body).
   - Closing "Next steps" ordered list + disclosure note.
5. **Footer** with three columns: brand+contact, Resources (smthelp.com, file.autoinsertion.com, ph.smthelp.com, product page, blog), Connect (5 social pills + the resources line).

## Visual & code rules
- Single `.html` file. Inline `<style>` + inline `<script type="application/ld+json">`. No external CSS/JS files (Google Fonts allowed).
- Color tokens (CSS variables): `--brand:#1C64F2`, `--brand-dark:#0d3b8c`, `--accent:#f59e0b`, `--ink:#0f172a`, `--ink-2:#334155`, `--muted:#64748b`, `--bg:#f8fafc`.
- Font: `Inter` (300/400/500/600/700/800).
- Responsive at 700/780/860 px breakpoints.
- Use `<table class="spec">` for spec tables, `.callout` boxes for source-of-truth notes, `.cta-box` for inline CTAs, `<details class="faq">` for FAQ, `<blockquote>` for formulas.
- All anchors must work (TOC IDs match section IDs).
- Validate with a balanced-tag check before finishing.

## Output rules
- File name: `outputs/<MODEL>_Blog_GEO_SEO/<MODEL>-<topic-slug>-Blog.html` (or another agreed path).
- Article length: 1,400-2,200 English words.
- All English (customer-facing). Chinese only inside in-line code-comment notes if the user asks.
- Word counts to enforce: H1 ≤ 14 words; meta description 140-170 chars; alt text for every `<img>`; 1 primary CTA mailto + 1 secondary action.
- Disclose at end: figures illustrative, pricing/lead-time per quotation, no customer names.

## Hard rules (red lines — never violate)
- Never invent specs, prices, lead times, certifications, customer names, payback months as a single number — always show the formula.
- Never disparage competitors. Compare on facts only.
- Never claim a docking-kit fit not yet confirmed by Southern Machinery engineering.
- Never paste internal quotation PDFs / customer survey responses into the blog.
- Never name a customer; anonymize as "Tier-1 EMS in {{region}}".
- Always include the JSON-LD `Article + Product + FAQPage` block.
- Always include the logo in header AND footer.
- Always include all 5 social links + the file.autoinsertion.com / ph.smthelp.com line in footer.

## Workflow
1. Confirm `<MODEL>` and topic angle(s) with the user (or infer from cwd folder name).
2. Read the source-of-truth files in order. Build a fact sheet (specs, pain→value, ROI variables, competitor map).
3. Pick H1 + meta description + URL slug.
4. Generate the HTML by appending sections in this order: head → ld+json → header → hero → article (TOC, body sections, ROI, compatibility, competitor, deployment, FAQ, CTA) → footer.
5. Validate balanced tags (`python3 -c` HTMLParser open/close stack).
6. Save under `outputs/<MODEL>_Blog_GEO_SEO/`.
7. Tell the user the output path + 1 follow-up suggestion (LinkedIn post, YouTube description, ROI calculator email).

## Templates
- `templates/blog_skeleton.html` — copy-pasteable skeleton with all required sections, `{{TOKENS}}` for product fields.
- `examples/S-680A-5S-Labor-ROI-Blog.html` — reference reading: 5S + labor + ROI angle for the S-680A scrap tape cutter (≈ 35 KB, ~1,800 words).

## Default closing line (in user-facing reply)
> 下周必做动作：把这篇博客切成 1 条 LinkedIn 帖 + 1 条 YouTube 视频描述 + 1 封 Day 7 跟进邮件，三处复用同一组数字。
