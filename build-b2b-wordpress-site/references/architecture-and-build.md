# Architecture And Build

## Contents

1. Architecture decisions
2. WordPress ownership boundaries
3. Design system
4. Page composition
5. Plugin policy
6. Performance and accessibility

## 1. Architecture Decisions

Use a custom theme plus companion plugin for a branded B2B catalog unless the project requirements point elsewhere.

| Need | Preferred solution |
|---|---|
| Branded catalog and inquiries | Custom theme + custom post types |
| Cart, payment, orders, tax, shipping | WooCommerce |
| Frequent drag-and-drop campaign pages | Controlled page builder templates |
| Multiple frontends consuming one CMS | Headless WordPress after explicit justification |
| Simple editorial company site | Native blocks or lightweight custom templates |

Avoid mixing several page builders or duplicating the same responsibility across plugins.

## 2. WordPress Ownership Boundaries

Keep in the theme:

- Layout templates
- Typography, spacing, color, and component styles
- Header, navigation, footer, banners, cards, and presentation helpers
- Responsive behavior

Keep in a companion plugin:

- Product and project post types
- Product categories and other taxonomies
- Durable metadata definitions
- REST extensions
- Import rules and validation
- Inquiry data behavior when implemented in WordPress

Use native WordPress data and APIs for pages, posts, media, users, menus, revisions, and taxonomies where practical.

## 3. Design System

Define tokens before individual pages:

- Font families and fallback stacks
- Body, label, navigation, heading, and display sizes
- Text, background, border, accent, success, warning, and error colors
- Spacing scale
- Content and wide container widths
- Grid tracks and gaps
- Button, input, card, media, banner, and modal states
- Breakpoints based on content failure, not device brand

Keep cards at restrained radii. Use familiar icons for icon actions and text buttons for clear commands. Do not hide essential labels behind ambiguous icons.

## 4. Page Composition

### Home

Show the actual product category and positioning in the first viewport. Follow with buyer-relevant proof, priority collections, customization or project workflow, factory evidence, featured projects or products, useful content, and a conversion section.

Avoid repeating the hero's statement in the first statistics band. A capability band can use verified signals such as years, countries, clients, exhibitions, certifications, capacity, QC stages, or delivery regions.

### Collection Archive

- Use a stable grid with predictable card dimensions.
- Fill complete rows where practical. For a four-column desktop grid, use 12 items per page unless requirements justify another count.
- Use `object-fit: contain` for product images when preserving the whole fixture matters.
- Apply a dedicated thumbnail crop only for exceptional images; do not replace the original product media.
- Keep model, title, category, and link targets aligned with the current product.

### Product Detail

Include a media gallery, model, title, concise positioning, structured specifications, customization options, applications, installation or technical notes, related products, and an inquiry action carrying the product identity.

### About And Factory

Use owned factory evidence to establish authenticity: exterior, workshop, material preparation, assembly, inspection, aging tests, packaging, warehouse, showroom, team, exhibitions, and certifications. Captions should explain what the buyer is seeing.

### Inner-Page Banners

Use a consistent banner system while varying imagery and copy by page intent. Keep the banner height restrained enough to show the next section. Set intentional image position per page so the product or subject is not cropped incorrectly.

## 5. Plugin Policy

Before installing a plugin, check:

- Active maintenance and WordPress/PHP compatibility
- Data ownership and uninstall behavior
- Performance and asset loading scope
- Security history and permissions
- REST, theme, cache, multilingual, and SEO compatibility
- Whether the same need already exists in the theme, plugin, or host

Typical categories include SEO, multilingual, forms, SMTP, caching, image optimization, security, backups, redirects, and WhatsApp. Install only the categories required by the project.

Prevent global plugin output from breaking the header. Place language selectors and chat controls in deliberate theme regions, then verify desktop and mobile states.

## 6. Performance And Accessibility

- Use responsive images and appropriate compression.
- Reserve image dimensions to prevent layout shift.
- Lazy-load below-the-fold media, not the primary hero image.
- Minimize render-blocking assets and load plugin assets conditionally where possible.
- Provide visible focus, keyboard navigation, sufficient contrast, labels, errors, and reduced-motion behavior.
- Use semantic landmarks and heading order.
- Test with cache both enabled and bypassed.
- Verify web fonts do not hide content while loading.
