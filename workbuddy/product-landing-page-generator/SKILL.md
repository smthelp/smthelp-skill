---
name: product-landing-page-generator
description: Use when generating a single-file HTML product landing page from product documents, images, and video links. Triggers on requests like "create landing page", "product page", "landing HTML" with product source URLs, or FAB model content requirements.
---

# Product Landing Page Generator

Generate production-ready single-file HTML landing pages for industrial/commercial products using FAB (Feature-Advantage-Benefit) sales model.

## When to Use

- User provides product source documents (PDFs, URLs, specs) + video/image links
- Request includes "landing page", "落地页", "FAB模型", "单HTML文件" keywords
- Reference template URL is provided (Southern Machinery style preferred)
- Output must be self-contained: one HTML file with embedded CSS/JS, runs in browser directly

## Workflow

### Step 1 — Gather Inputs

Collect these before starting:

| Input | Source | Required |
|-------|--------|----------|
| Product name & model | User request / source docs | ✅ |
| Product category | User request | ✅ |
| Reference landing page URL(s) | User request | Preferred |
| Product source URLs (official pages) | User request | ✅ |
| PDF/spec documents | User request | Preferred |
| YouTube/video URLs | User request | Preferred |
| Company logo URL | User request | ✅ |
| CTA/contact info (email, WhatsApp, social) | User request | ✅ |
| Smart customer service embed code | User request | Optional |

### Step 2 — Fetch & Analyze Sources

Use `WebFetch` to extract from:
- **Reference template**: full HTML structure, CSS classes, color scheme, typography, component patterns
- **Product pages**: images (`img src`), specifications table, feature descriptions, pain points, functions
- **PDFs** (if accessible): use `pdfkit-py` skill or extract text via `WebFetch`
- **Image CDN** (e.g., `ph.smthelp.com`): search product keyword + "image" or "photo" for matching visuals

Extract structured data:
```
ProductInfo = {
  name: string,
  model: string,
  description: string[],
  features: [{title, description}],
  specs: [{item, value}],
  pain_points: [{problem, solution}],
  benefits: [{feature, advantage, benefit}],
  images: [url, ...],
  videos: [{youtube_id, title}]
}
```

### Step 3 — Design Structure (FAB Model)

Layout sections in this order:

```
1. Header — Logo (top-left) + Navigation + CTA button
2. Hero Carousel — 5 auto-rotating images (6-8s interval), overlay with title/subtitle/stats
3. Core Metrics Cards — 3-4 key numbers at a glance
4. FAB Section — Feature · Advantage · Benefit 3-column comparison table
5. Pain Points → Solutions — Problem/solution pairs as cards
6. Feature Grid — 6 cards with icon + title + description
7. Specifications Table — Full spec parameters
8. Video Gallery — Embedded YouTube iframes (responsive 16:9)
9. Product Photo Gallery — Horizontal scrollable image strip
10. FAQ Accordion — 5-7 common questions with expand/collapse
11. CTA Banner — Primary action + secondary contact links
12. Footer — Logo, social links, catalog links, contact email
13. Chat Widget — Fixed bottom-right (user-provided code)
```

### Step 4 — Style Guidelines

Based on Southern Machinery template reference:

| Property | Value |
|----------|-------|
| Primary color | `#0057A8` (deep industrial blue) |
| Accent color | `#FF6B00` (orange highlight) |
| Background | `#FFFFFF` / `#F5F7FA` alternating |
| Text dark | `#1A1A2E` |
| Text mid | `#4A5568` |
| Font stack | `"Noto Sans SC", "PingFang SC", "Helvetica Neue", sans-serif` |
| Max container width | `1200px` |
| Border radius | `12px` / `8px` |
| Card shadow | `0 4px 24px rgba(0,87,168,0.10)` |

### Step 5 — Build Single HTML File

All CSS and JS inline in `<style>` and `<script>` tags. No external dependencies except:
- YouTube iframe API (for videos)
- Chatwoot SDK (if provided)
- External images (CDN URLs are acceptable)

**Carousel implementation:**
```js
// Auto-advance every 6s, pause on hover, arrow navigation, dot indicators
```

**FAQ accordion:**
```js
// Toggle active class on click, collapse others
```

### Step 6 — Verify & Deliver

Before presenting:
- [ ] File is self-contained (one `.html`)
- [ ] Hero carousel has 5+ images and auto-rotates
- [ ] Logo appears in header top-left
- [ ] All required CTAs present (LinkedIn, Twitter, Facebook, YouTube, email, catalog links)
- [ ] Chatwoot/widget code is embedded (fixed bottom-right)
- [ ] Responsive: works on desktop + mobile (use `clamp()`, flexbox, media queries)
- [ ] Double-click to open in browser works (no build step needed)

Save to workspace root: `{ProductName}-{Model}-Landing.html`

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Using external CSS/JS CDNs that break offline | Embed everything inline; only YouTube/chat widget can be external |
| Carousel images not loading (broken CDN) | Always verify `ph.smthelp.com` image URLs first; have fallback placeholder colors |
| FAB section too verbose | Keep each column to 1 sentence; use table format |
| YouTube embeds blocking interaction | Use `pointer-events: auto` wrapper; ensure responsive `aspect-ratio: 16/9` |
| Forgetting company social links in footer | Cross-check against user-provided link list explicitly |

## Image Sourcing Strategy

When official product images are scarce:
1. First try: `https://ph.smthelp.com` — search by product name/keyword
2. Second try: `https://hk03-1251009151.file.myqcloud.com/smthelp.com/desc/` — official desc images
3. Fallback: generate colored placeholder blocks with product name text overlay
