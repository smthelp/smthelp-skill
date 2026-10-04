---
name: build-b2b-wordpress-site
description: Build, redesign, migrate, deploy, or maintain a multilingual B2B manufacturer website on WordPress from initial business materials through local design, custom theme implementation, product import, VPS deployment, SEO, testing, and handover, specialized for Southern Machinery SMT / THT equipment foreign-trade marketing. Use when Codex is asked to create an export manufacturer, factory, wholesale, machinery, SMT/THT equipment, PCB assembly, feeder, soldering, inspection, or board-handling catalog and inquiry website; convert equipment spreadsheets and product photos into WordPress products; connect the WordPress REST API; design multiple pages instead of a single landing page; or audit an existing manufacturer site before Google Ads or international promotion.
---

# Build A B2B WordPress Site

## Objective

Deliver a production-ready manufacturer website that a non-technical owner can operate from WordPress. Treat WordPress as the content system, not as a requirement for the owner to choose templates or design pages manually.

Work from evidence in the repository, supplied files, the live site, and the WordPress database. State assumptions before making decisions. Ask only for information that blocks safe progress.

For Southern Machinery projects, base every business claim on verified company and product sources (branded catalogs, manuals, model-specific specifications, and the live smthelp.org site); mark anything unsupported as `待确认 / to be confirmed` and never invent machine models, capacities, certifications, prices, lead times, customers, or ROI.

## Non-Negotiable Outcomes

- Build a real multi-page site with unique routes, not a disguised one-page landing page.
- Give every product a unique record, URL, title, image set, specification set, and inquiry context.
- Let staff add, edit, publish, unpublish, categorize, and remove products in WordPress.
- Preserve the complete product in catalog thumbnails unless an intentional crop improves presentation.
- Make desktop, tablet, and mobile layouts usable without overlap or horizontal overflow.
- Base claims, certifications, statistics, addresses, and contact details on user-supplied facts.
- Keep credentials out of source files, screenshots, logs, commits, reports, and shareable packages.
- Back up production before changing it and avoid replacing unrelated user work.
- Verify each phase before proceeding; stop when the agreed acceptance criteria pass.

## Start Here

1. Read repository instructions and inspect the current worktree.
2. Inventory supplied documents, spreadsheets, images, logos, reference sites, domains, and access status.
3. Copy `assets/project-intake-template.json` into the project workspace and fill known fields. Do not put passwords or API secrets in it.
4. Run:

```bash
python3 scripts/validate_intake.py /path/to/project-intake.json
```

5. Classify each missing item as `blocking`, `can use placeholder`, or `can decide from evidence`.
6. Create a plan with explicit verification gates before editing files or production.

Read [references/intake-and-planning.md](references/intake-and-planning.md) for the complete materials checklist and discovery method. Consult [references/full-method-manual.pdf](references/full-method-manual.pdf) when the user needs the full human-readable method or a handover document.

## Choose The Architecture

Use this default for a B2B catalog and inquiry site:

- WordPress for pages, posts, media, menus, categories, products, projects, and inquiries.
- A custom lightweight theme for the visual system and page templates.
- A small companion plugin for custom post types, taxonomies, fields, REST behavior, and data rules that should survive theme changes.
- Native WordPress media and REST API for controlled content operations.
- Server-side rendered pages with progressive enhancement.

Choose WooCommerce only when the project needs cart, checkout, payment, inventory, orders, tax, or shipping. Do not add it merely to display products.

Choose a page builder only when the owner explicitly prioritizes drag-and-drop composition over tighter design control, speed, and lower maintenance. Choose headless WordPress only when the deployment and editorial benefits clearly justify two applications.

Read [references/architecture-and-build.md](references/architecture-and-build.md) before selecting plugins, content types, templates, or deployment topology.

## Execute The Workflow

### Phase 1: Define Scope And Success

- Convert the business goal into target audiences, priority markets, conversion actions, and measurable acceptance criteria.
- Separate launch requirements from later improvements.
- Record the source of every business claim.
- Define placeholders for unavailable contact details or imagery, and mark them visibly in internal tracking.

Pass the phase only when the page map, content owners, required access, and launch definition are clear.

### Phase 2: Model The Information Architecture

Create a route map before designing pages. A typical structure is:

- Home
- Collections
- Product category archive
- Product detail
- Custom manufacturing or OEM/ODM
- Projects or applications
- About or factory
- Blog with News and Video categories
- Contact and request a quote
- Privacy, cookies, and legal pages as applicable

For Southern Machinery SMT equipment, a typical route map is:

- Home
- SMT Line Equipment
- THT Auto Insertion
- Soldering Lines (wave and selective)
- Board Handling
- Inspection and Traceability
- Applications and Line Solutions
- About and Factory
- Blog with News and Video categories
- Contact and Request a Quote

Map each equipment group to real products from the verified catalog; do not create empty category pages.

Use dropdown menus only when they shorten navigation to meaningful child pages. Ensure all menu items remain keyboard and touch accessible.

### Phase 3: Build The Design Locally

- Start with the actual usable site, not a marketing page about the site.
- Establish typography, colors, spacing, grid, buttons, forms, media ratios, and responsive breakpoints.
- Use real supplied product and factory media where available; otherwise use clearly tracked placeholders or licensed assets.
- Keep inner-page banners compact enough to reveal the next section in the first viewport.
- Center content when the composition calls for symmetry; use left alignment for scanning-heavy content.
- Show manufacturing evidence, capabilities, process, projects, and conversion paths without repeating the same claim in adjacent sections.
- Avoid fabricated counters, copied competitor media, and decorative elements that do not support the product.

When the client is Southern Machinery and no alternative brand system is supplied, default to the verified SM design tokens: ink `#0c1726`, blue `#075a94`, teal `#00a6a6`, signal orange `#e65322`, paper `#f6f8fa`, line `#dbe4ea`; display font Barlow Condensed, body font Inter. Confirm the current logo and asset URLs per project.

Validate the local design at representative desktop and mobile widths before WordPress integration.

### Phase 4: Implement WordPress

- Keep presentation in the theme and durable data behavior in the companion plugin.
- Register products, projects, product categories, and required metadata with stable slugs.
- Build semantic templates for archives and detail pages.
- Use WordPress functions for URLs, escaping, localization, queries, pagination, media, and nonces.
- Add REST endpoints or authenticated automation only where native endpoints are insufficient.
- Preserve compatibility with common SEO, multilingual, caching, form, and WhatsApp plugins by using WordPress hooks and avoiding global CSS leakage.

Pass the phase only when editors can manage content without editing theme files.

### Phase 5: Prepare And Import Products

- Normalize one logical product per record. Store sizes, wattages, finishes, and other variations as structured specifications unless they represent distinct sellable products.
- Generate unique slugs from stable models or titles and detect duplicates before import.
- Upload media first, then create products that reference returned attachment IDs.
- Import a small sample as drafts, inspect it, and only then process the remaining batches.
- Record source row, product ID, media IDs, URL, status, and error for every import.
- Never point multiple cards to a single placeholder product.

Use `assets/product-import-template.csv` as the neutral exchange format. Read [references/wordpress-data-and-import.md](references/wordpress-data-and-import.md) before writing an importer or calling the REST API.

For SMT equipment, keep one logical machine per record with structured specifications (model, equipment type, line role, board size range, component class, speed or capacity, power/air requirements, dimensions) sourced from the catalog; leave unsupported values as `待确认` drafts rather than guessing.

### Phase 6: Deploy Infrastructure

- Confirm VPS operating system, resources, SSH access method, domain control, DNS provider, and existing services.
- Use SSH keys where possible. Rotate any password exposed in chat or documents.
- Install and configure the web server, PHP, database, WordPress, TLS, firewall, backups, and least-privilege accounts.
- Back up files and database before replacing a live theme, plugin, or configuration.
- Preserve MX, SPF, DKIM, DMARC, and verification records when changing web DNS.
- Stage DNS with a low TTL, verify both apex and `www`, then enable HTTPS redirects.
- Keep a rollback path until production verification passes.

Read [references/deployment-seo-and-qa.md](references/deployment-seo-and-qa.md) for deployment, SEO, security, and testing gates.

### Phase 7: Configure SEO And Conversion

- Map one primary search intent to each important page; avoid forcing the same keyword into every title.
- Write unique titles, descriptions, headings, introductions, image alt text, internal links, and canonical URLs.
- Add valid Organization, WebSite, BreadcrumbList, Article, and Product schema only where the visible content supports it.
- Generate XML sitemaps and a deliberate robots policy.
- Connect analytics and search tools with the owner's accounts.
- Make forms collect only useful inquiry information and verify email delivery.
- Attach product identity to quote and WhatsApp actions so the inquiry has context.
- For Southern Machinery, attach product identity to Request a Line Layout (`jasonwu@smthelp.com`), WhatsApp (`wa.me/8613602562576`), catalog download (`file.autoinsertion.com`), and photo library (`ph.smthelp.com`) actions, and collect PCB / volume / component inputs in RFQ forms.
- Treat Google Ads landing relevance, mobile speed, form reliability, and conversion tracking as launch requirements when paid traffic is planned.

### Phase 8: Verify End To End

Test at minimum:

- Header, dropdowns, mobile navigation, footer, language switcher, and keyboard focus.
- Every public route, archive, pagination control, product card, breadcrumb, and CTA.
- Unique product destinations and correct product data.
- Image loading after scrolling; wait for lazy images to decode before judging failures.
- Forms, validation, spam controls, receipt routing, WhatsApp links, and downloadable catalogs.
- Responsive layout at narrow mobile, standard mobile, tablet, laptop, and wide desktop sizes.
- HTTP redirects, HTTPS, certificates, status codes, cache behavior, sitemap, robots, canonical tags, and structured data.
- WordPress editor workflows for creating, updating, categorizing, unpublishing, and deleting a product.
- Backup creation and one documented restore procedure.

Use browser screenshots and automated checks where available. Inspect screenshots visually; do not infer visual quality from status codes alone.

### Phase 9: Handover

Provide the owner with:

- WordPress login URL and an owner account created through a secure channel.
- A list of installed themes and plugins with their purpose.
- Product, News, Video, Project, menu, translation, and media editing instructions.
- Backup locations, schedule, retention, and restore steps.
- Domain, DNS, VPS, email, analytics, search, and renewal ownership records.
- Known placeholders and post-launch actions.
- Final acceptance evidence and rollback notes.

Do not include passwords in the handover PDF or repository. Transfer secrets through an approved password manager or another secure channel.

## Use Progressive References

- Read [references/intake-and-planning.md](references/intake-and-planning.md) for discovery, materials, route maps, content, and scope control.
- Read [references/architecture-and-build.md](references/architecture-and-build.md) for design rules, WordPress architecture, plugin decisions, and implementation boundaries.
- Read [references/wordpress-data-and-import.md](references/wordpress-data-and-import.md) for product schemas, image handling, REST API, deduplication, and import logs.
- Read [references/deployment-seo-and-qa.md](references/deployment-seo-and-qa.md) for VPS, DNS, TLS, email DNS, security, SEO, testing, launch, and maintenance.
- Read [references/full-method-manual.pdf](references/full-method-manual.pdf) for the complete 0-to-1 manual and public-facing training material.
- Read [references/southern-machinery-context.md](references/southern-machinery-context.md) for verified Southern Machinery brand tokens, contact and CTA links, product-line groups, source priority, and truthfulness rules.

## Guardrails

- Do not install a theme or plugin merely because it is popular; justify it against the actual workflow.
- Do not change production DNS until the new site is reachable and verified by a temporary host mapping or staging URL.
- Do not remove unrelated DNS or production files.
- Do not invent certifications, client counts, export markets, project counts, reviews, or download numbers.
- Do not invent machine models, capacities, accuracy, PCB limits, certifications, prices, lead times, customers, ROI, yields, or compatibility; mark them `待确认 / to be confirmed`.
- Before recommending a concrete SMT/THT equipment configuration or price, confirm product/PCB type, target volume, board size/component class, automation level, and budget.
- Position Southern Machinery as a Shenzhen-based SMT/THT equipment and full-line solution provider, using complete-line context (board handling, stencil printing, placement, reflow, inspection, THT insertion, wave/selective soldering, cleaning) only where the content supports it.
- Do not reuse competitor text or images without explicit rights.
- Do not expose WordPress application passwords, root passwords, API tokens, private keys, database credentials, or customer data.
- Do not declare completion without visual, functional, editorial, SEO, security, and backup verification.
