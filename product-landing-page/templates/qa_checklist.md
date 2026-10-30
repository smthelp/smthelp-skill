# Product Landing Page — QA Checklist

Run through every item before delivering the file.

## Brand
- [ ] Southern Machinery logo (https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png) present in **header top-left** at ~48px height.
- [ ] Same logo also in footer (white-bg pill).
- [ ] Brand color tokens in `:root` (--brand #1C64F2, --brand-dark #0d3b8c, --accent #f59e0b).

## Footer social links (all five, in this order)
- [ ] LinkedIn Company → https://www.linkedin.com/company/smtmachine
- [ ] LinkedIn Profile → https://cn.linkedin.com/in/smtsupplier
- [ ] Twitter → https://twitter.com/smtspecialist
- [ ] Facebook → https://www.facebook.com/autoinsertion
- [ ] YouTube → https://www.youtube.com/c/Smthelping
- [ ] Each `<a>` has `aria-label` and `target="_blank" rel="noopener"`.

## Footer resources sentence
- [ ] Includes the exact phrasing: "Browse our machine catalog at file.autoinsertion.com and find machine photos at ph.smthelp.com."

## Sections (in order)
- [ ] Top bar (phone + email)
- [ ] Sticky header with nav
- [ ] Hero (image + stats + 2 CTAs)
- [ ] Pain → Solution grid (6 cards)
- [ ] Features grid (6-9 cards)
- [ ] Benefits dark strip (4 stats, ROI marked indicative)
- [ ] Specifications table (datasheet values only)
- [ ] Compatibility chips
- [ ] Gallery (2-3 product photos)
- [ ] Working video (lazy-loaded YouTube embeds)
- [ ] Service strip (4 service tiles)
- [ ] FAQ accordions (6-8)
- [ ] Final CTA section
- [ ] Footer (4 columns)
- [ ] Floating WhatsApp FAB

## Tech
- [ ] Single file, no external CSS/JS deps (Inter from Google Fonts is OK).
- [ ] Mobile breakpoint at `max-width:860px` collapses nav.
- [ ] All `<iframe>` have `title=` and `loading="lazy"`.
- [ ] All `<img>` have descriptive `alt`.
- [ ] `<title>`, `<meta description>`, `<meta keywords>` populated.

## Content integrity
- [ ] No invented prices, delivery times, ROI figures, or customer names.
- [ ] Every spec value is in the datasheet / project AGENT.md.
- [ ] Every claim carries an evidence label: `Verified data` / `Illustrative` / `To be confirmed`.
- [ ] **Datasheet vs manual conflicts are published**, not silently resolved — one row per disagreement in a `To be confirmed` table with a "what to do" column.
- [ ] ROI claim has an asterisk + footnote "validated case-by-case during quotation".
- [ ] Customer-facing copy in English (unless Chinese explicitly requested).

## SEO / GEO
- [ ] `<title>` fits the SERP width budget (<= 60 width units, where a CJK glyph counts as 2). A plain character count is the wrong test in both directions.
- [ ] `<meta name="description">` <= 160 width units.
- [ ] `<link rel="canonical">` present and pointing at the final slug.
- [ ] `hreflang` alternates for every supported language **plus `x-default`**.
- [ ] JSON-LD `@graph` present with Organization / Product / FAQPage / BreadcrumbList.
- [ ] `FAQPage.mainEntity` count **equals** the number of visible FAQ entries — mismatched FAQ markup is a manual-action risk.
- [ ] Product node carries the published specs as `additionalProperty`.
- [ ] Filename is a lowercase SEO slug (model + function + category), not the internal working name.

## Multi-language layer (only if the page ships with i18n)
- [ ] No `data-i18n` element renders its own key name, in **any** language.
- [ ] No `data-i18n-ph` / `data-i18n-title` element renders its own key name.
- [ ] `placeholder` and `title` attributes are translated, not just visible text.
- [ ] `<html lang>` and `dir` are set on every switch; Arabic resolves to `rtl`.
- [ ] SEO title and meta description change per language (a title that never changes is not localised).
- [ ] **JS-generated strings are translated too** — calculator units, prompts, and dynamic card titles never appear in the markup, so they need an explicit merge block. Assert that no `unit_*` / `calc_*` literal key leaks in any language.
- [ ] Long-form body copy is allowed to stay English; headings and standfirsts are translated.
- [ ] Language choice persists in `localStorage` and survives a refresh.
- [ ] `?lang=xx` overrides the stored preference; an unknown `?lang=` falls back instead of breaking.
- [ ] Language menu lists all languages in the documented order and marks the active one with `aria-current`.

## Theme layer (only if the page ships with a toggle)
- [ ] Clicking the toggle flips `data-theme` on `<html>`.
- [ ] Choice persists in `localStorage` and survives a refresh.
- [ ] First visit follows `prefers-color-scheme`.
- [ ] `<meta name="theme-color">` updates with the theme.
- [ ] Dark mode reuses the existing CSS variables — no second palette was authored.

## Headless verification (mandatory)
- [ ] `templates/verify_landing_page.js` runs and prints `ALL CHECKS PASSED`.
- [ ] Every reported SKIP was reviewed and is expected for this page.
- [ ] Runtime `<script>` extracted and passed through `node --check` (a stray ASCII `"` inside a translated string is the most common syntax killer).
- [ ] Calculator arithmetic verified against a hand computation, including the degenerate inputs (zero labour, zero price, out-of-range feed) — they must show a prompt, never `Infinity` or `NaN`.
- [ ] No banned word appears in any heading, summary, or title (scanned programmatically, not by eye).

## External assets
- [ ] Every image / video thumbnail / embed URL returned HTTP `200` with non-zero size.
- [ ] Video thumbnails use `i.ytimg.com/vi/<id>/hqdefault.jpg`; embeds use `youtube-nocookie.com/embed/<id>`.
- [ ] No eager `<iframe>` in the video grid — the player is injected on click.
- [ ] Below-the-fold images are `loading="lazy"`; the header logo and the `fetchpriority="high"` hero are deliberately exempt.
- [ ] Support widget base URL follows the page protocol (an `http://` widget on an `https://` page fails silently).

## Output
- [ ] File saved as `<MODEL>-...-Landing.html` (or the SEO slug) in the project folder.
- [ ] If pushed to a repository: correct account confirmed via `gh auth status`, correct repo confirmed, README index row added.
- [ ] If the file was touched by a visual editor, any editor-injected attributes (e.g. `data-page-node-id`) were stripped before publishing.
- [ ] Final assistant message includes file path + 5-bullet section summary + 下周必做动作 line.
