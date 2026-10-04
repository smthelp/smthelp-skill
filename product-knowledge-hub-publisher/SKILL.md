---
name: product-knowledge-hub-publisher
description: "Build, govern, and publish a maintainable public B2B industrial product knowledge hub from scattered catalogs, spreadsheets, presentations, PDFs, 3D assets, photos, videos, and existing web pages. Use when converting product evidence into English Markdown records and a searchable website; setting up GitHub and Cloudflare Pages; adding official media, SEO/GEO, contact paths, chat widgets, custom domains, or release governance."
metadata:
  source: codex
  origin: "product-knowledge-hub-publisher"
---
# Product Knowledge Hub Publisher

Create an evidence-controlled, English-language public product hub for B2B industrial buyers. Treat the repository as the durable source of published content; use the website as a generated presentation layer.

## Outcome

Deliver a repository and public website with:

- One structured Markdown record per approved product/version.
- Product-family taxonomy, source links, public media, evaluation guidance, integration requirements, and publication dates.
- Searchable, indexable HTML with canonical URLs, sitemap, robots, structured data, and `llms.txt`.
- GitHub review/release workflow and Cloudflare Pages production deployment.

## Gate 1: Establish Scope And Evidence

1. Identify the allowed public product families, models, markets, language, contact routes, YouTube channel, official image host, repository, domain, and deployment account.
2. Inventory sources narrowly. Prefer current product-specific manuals, approved catalog pages, and dated current assets over historical presentations or filenames.
3. Create a source matrix before publishing. For every model, record the source URL/file, date/version, public status, photo search URL, video URL, and unresolved fields.
4. Never infer specifications, certifications, prices, output, PCB limits, electrical requirements, delivery terms, or compatibility. State that engineering confirmation is required when evidence is absent or conflicted.
5. Do not upload archives, customer information, private quotations, credentials, or historical public-media buckets merely to make them accessible.

Read [references/product-record-contract.md](references/product-record-contract.md) before designing the records.

## Gate 2: Build The Content System

1. Normalize each allowed product into its own English Markdown document and stable URL slug.
2. Keep source-controlled fields separate from generic selection guidance. Include upstream/downstream dependencies rather than presenting an isolated machine as a full solution.
3. Preserve original source assets. Generate derivatives in a distinct output directory or repository; do not reorganize archives as a side effect.
4. Build a site from data/templates so product cards, pages, JSON-LD, Markdown records, sitemap, `robots.txt`, and `llms.txt` are generated consistently.
5. Use genuine approved product imagery. Search the official host with the model keyword and verify the resulting direct image URL before embedding it.

## Gate 3: Public Website Requirements

1. Use semantic HTML, stable responsive layout, image dimensions/aspect ratio, accessible controls, descriptive `alt` text, and keyboard-operable carousels.
2. Add title, description, canonical URL, Organization/Product JSON-LD, sitemap, `robots.txt`, and `llms.txt`. Do not put unverified claims into metadata.
3. Put brand logo, sales/contact links, catalog, photo library, social channels, and approved messaging in shared layout templates so they appear on every page.
4. Treat third-party widgets as production dependencies. Use HTTPS only, load once globally, verify the origin and token are user-authorized, and confirm the launcher's live iframe/network state. Do not paste secrets into source.
5. Use real photos instead of generated imagery for specific industrial products unless the user explicitly permits a non-product illustrative asset.

## Gate 4: GitHub And Cloudflare Release

1. Verify the active GitHub account, repository owner, default branch, working-tree status, and Cloudflare account/project/domain before mutating remote state.
2. Work in an isolated worktree and feature branch. Stage only intended files, run build/static checks, push, and create a PR.
3. Default to a draft PR. Merge production only with explicit authorization. Record the merge commit and deployment URL.
4. Configure Cloudflare Pages with an explicit build command, output directory, production branch, Node version, and custom domain. Confirm DNS and TLS are active before declaring launch complete.
5. Do not expose R2 object listings or bind an image subdomain if the existing bucket contains unreviewed historical data. Publish only an allowlisted asset surface.

Read [references/release-and-cache.md](references/release-and-cache.md) before configuring production.

## Gate 5: Validate The Rendered Production Site

Use the available Browser skill first. Test this flow:

`Homepage loads -> Hero and first meaningful content render -> product filtering/carousel or requested control changes state -> product page and global footer/chat load -> mobile layout remains within viewport.`

Check all of the following before handoff:

- Desktop and mobile screenshots show no clipping, overlap, or horizontal overflow.
- Page title, canonical URL, visible brand, official media, footer CTAs, and product count are correct.
- Product claims link to their allowed source and no sensitive/publication-excluded data is visible.
- Browser console has no relevant errors; explain any third-party warning.
- The live custom domain serves the current release, not only a preview deployment.
- Long-lived immutable asset caching uses content-hashed filenames or a newly incremented version query for every CSS/JS release. Never rely on unchanged `/assets/site.css` or `/assets/site.js` URLs after changing their content.

## Decision Rules

- If facts conflict, use the newest verified source and flag the conflict; do not blend values.
- If public-release authority is missing, prepare the branch/preview but do not publish, bind a domain, or open access.
- If an HTTP third-party widget redirects to HTTPS, use the verified HTTPS endpoint. Do not deploy mixed active content on an HTTPS site.
- If an external source is unavailable, retain a source link and mark the field for engineering confirmation instead of fabricating a fallback.
- If a build output is ignored by Git, commit its source generator and validation only, unless the hosting model explicitly requires committed build artifacts.

## Handoff

Report the source files changed, repository branch/PR/merge commit, preview and production URLs, checks run, responsive/browser evidence, and residual business-side configuration such as chat inbox routing. Do not claim that a contact workflow is operational merely because its widget loads.
