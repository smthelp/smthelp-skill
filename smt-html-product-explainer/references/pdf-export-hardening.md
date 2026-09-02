# PDF Export Hardening — Quick Reference

Pocket reference for the most common pitfalls when exporting the `smt-html-product-explainer` family of pages to PDF. The full discussion is in `../SKILL.md` (PDF Export Variant section). This file is a quick lookup for during a build.

## The 5 bugs that survive a naive `chrome --headless --print-to-pdf`

| # | Bug | Symptom | Fix |
|---|-----|---------|-----|
| 1 | **Gradient text via `background-clip: text`** | H1/H2/H3 render as colored rectangles with no text | `@media print` block forces solid color (see SKILL.md) |
| 2 | **SVG `viewBox`-only collapse** | All SVG illustrations render at 0×0 — page looks empty inside the panels | JS: `s.setAttribute('width','100%')` on every `<svg>` before snapshot |
| 3 | **Dark theme stripped to white** | Body background goes white, accent card colors gone | `-webkit-print-color-adjust: exact` on body, .scene, .panel, .lead-form-section, .reader-action-callout |
| 4 | **Live `<form>` in PDF** | Form fields render but you can't submit — looks broken in a printable | Replace `.lead-form-section` with a static 4-field summary + READER ACTION callout (see SKILL.md Form-replacement pattern) |
| 5 | **CTA callout split across pages** | URL is on page N, WhatsApp/email on page N+1 | Inline `page-break-inside: avoid` on the callout div; `page-break-inside: avoid` on `.lead-form-section` |

## The 3 CSS properties that MUST be on every print-hardened page

```css
@media print {
  html, body {
    background: #020617 !important;     /* or whatever your dark base is */
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  /* SVG panels — defense in depth (the JS fix is the real fix) */
  .scene-art svg, .scene-art-full svg {
    width: 100% !important;
    height: auto !important;
  }
}
```

## The 5 Playwright steps for a clean lead-magnet PDF

```python
# Step 1: launch headless Chrome (Playwright bundled + system Google Chrome)
browser = await p.chromium.launch(
    headless=True,
    executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args=['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none'],
)
context = await browser.new_context(
    viewport={'width': 1240, 'height': 1754},   # A4 at 150dpi
    device_scale_factor=2,                      # retina-quality output
)
page = await context.new_page()

# Step 2: load HTML and let webfonts settle
await page.goto(f'file://{html_path}', wait_until='networkidle', timeout=60000)
await page.wait_for_timeout(3000)

# Step 3: SVG width fix (the viewBox-only collapse bug)
await page.evaluate("""() => {
  document.querySelectorAll('svg').forEach(s => {
    s.setAttribute('width', '100%');
    s.setAttribute('height', 'auto');
    s.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    s.style.width = '100%';
    s.style.height = 'auto';
    s.style.maxWidth = '100%';
    s.style.display = 'block';
  });
}""")

# Step 4: inject print CSS + switch to print emulation BEFORE DOM mutation
await page.add_style_tag(content=PRINT_CSS)
await page.emulate_media(media='print')

# Step 5: optional form replacement, then render
await page.evaluate(build_form_replace_js(slug))
await page.wait_for_timeout(1000)
await page.pdf(
    path=pdf_path, format='A4', print_background=True,
    margin={'top': '10mm', 'right': '8mm', 'bottom': '10mm', 'left': '8mm'},
    prefer_css_page_size=True, display_header_footer=False,
)
```

## Verification — the 3-page spot-check

Don't render every page to PNG and check. Just check 3:

- **Page 1** (cover): H1 text is **readable** (not a colored block), dark background is preserved, hero KPI numbers display, no animation ghosts
- **Middle page** (most SVG-heavy scene): all SVG storyboard panels contain **visible illustrations** (not empty boxes)
- **Last page** (footer + form): social links render, lead form fields visible, READER ACTION callout (URL + WhatsApp + email) is **fully on the page**, footer social links all clickable-looking

Render all pages to PNGs with `pdftoppm -png -r 110 output.pdf /tmp/preview/page` (one `brew install poppler` away, no pymupdf install needed), then `vision_analyze` the 3 critical pages.

## File location

- The full Playwright recipe is in `../scripts/playwright-html-to-pdf.py`. Run it with `python3 ../scripts/playwright-html-to-pdf.py <input.html>` and it produces `<input>.pdf` next to it, with the page-count sanity check and pdftoppm rendering already done.
- The full `@media print` block is in the SKILL.md's "PDF Export Variant" section.
- The form-replacement JS template is in the SKILL.md's "Form-replacement pattern" section.
