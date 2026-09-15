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
- [ ] ROI claim has an asterisk + footnote "validated case-by-case during quotation".
- [ ] Customer-facing copy in English (unless Chinese explicitly requested).

## Output
- [ ] File saved as `<MODEL>-...-Landing.html` in the project folder.
- [ ] Final assistant message includes file path + 5-bullet section summary + 下周必做动作 line.
