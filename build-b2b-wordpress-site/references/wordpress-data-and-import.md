# WordPress Data And Import

## Contents

1. Product data model
2. Row grouping rules
3. Image handling
4. REST API
5. Batch import procedure
6. Editorial workflow

## 1. Product Data Model

Use a stable product post type such as `product` or a namespaced custom type. Define fields before importing data.

Core fields:

- Stable external ID or model
- English title
- Slug
- Product category
- Short description
- Full description
- Main image attachment ID
- Gallery attachment IDs
- Publish status

Common specifications (adapt to the product type; for SMT equipment include):

- Dimensions
- Equipment type and line role
- Board size range and component class
- Speed or capacity
- Power and air requirements
- Input voltage
- Materials and finish
- Installation or integration notes
- MOQ
- Lead time
- Packaging
- Warranty
- Customization notes

SEO fields depend on the selected SEO plugin. Prefer supported plugin APIs or metadata keys documented by that plugin.

## 2. Row Grouping Rules

Do not assume every spreadsheet row is a product.

Treat adjacent rows as one product when they share the same design and differ only in size, wattage, finish, or a related specification. Store these as a structured variation or specification table.

Create separate products when they have materially different designs, intended applications, model identities, or independent merchandising needs.

Determine grouping using model, image continuity, merged cells, titles, category, and explicit user notes. Preserve the source row range in the import log.

## 3. Image Handling

- Keep original files outside the generated thumbnail pipeline.
- Use descriptive ASCII filenames.
- Remove accidental duplicates while preserving intentional alternate views.
- Upload media and store returned attachment IDs.
- Set meaningful alt text based on the visible product and model.
- Avoid upscaling small source images.
- Use a neutral product-media container and `object-fit: contain` for archive cards when full-product visibility is important.
- Use focal positions or dedicated derived thumbnails for edge cases.
- Verify lazy-loaded images after scrolling and waiting for image decode.

## 4. REST API

WordPress exposes REST endpoints under `/wp-json/wp/v2/`. Use HTTPS and an authenticated method appropriate to the environment. Application Passwords are suitable for controlled automation when created for a dedicated user and revoked after use.

Typical sequence:

1. Verify authentication and permissions.
2. Fetch or create required categories.
3. Upload media to the media endpoint.
4. Create a draft product referencing media IDs and taxonomy IDs.
5. Fetch the created product and compare every mapped field.
6. Publish only after sample review.

Never print authorization headers or credentials. Do not store application passwords in the importer source.

Native REST endpoints may not expose custom metadata unless it is registered with REST support. Register durable fields in the companion plugin and enforce sanitization and authorization server-side.

## 5. Batch Import Procedure

### Preflight

- Back up the database and uploads.
- Export or snapshot current products and categories.
- Validate required columns and image paths.
- Normalize whitespace, dimensions, units, categories, and slugs.
- Detect duplicate models, slugs, image hashes, and source rows.
- Generate a dry-run report.

### Sample Batch

Import one representative product from each category as a draft. Inspect archive card, detail page, admin fields, image gallery, mobile layout, SEO metadata, and inquiry context.

### Production Batch

Import in bounded batches. Make the operation resumable and idempotent using a stable external ID. On retry, update the intended record instead of creating a duplicate.

Log:

| Field | Purpose |
|---|---|
| Timestamp | Trace execution |
| Source file and rows | Trace origin |
| External ID/model | Detect duplicates |
| WordPress post ID | Enable updates and rollback |
| Media IDs | Track uploaded assets |
| Final URL | Verify route |
| Status | Draft, published, failed, skipped |
| Error | Diagnose without exposing secrets |

### Verification

- Count source logical products against imported records.
- Confirm category counts.
- Crawl every imported URL.
- Assert card hrefs are unique and match card product IDs.
- Inspect first, last, and random products in each batch.
- Compare a sample of specifications against the source.

## 6. Editorial Workflow

Document these WordPress actions for the owner:

- Add a product
- Edit title, descriptions, specifications, category, images, and SEO
- Add or reorder gallery images
- Save as draft, preview, publish, unpublish, and delete
- Add News and Video posts using the correct category
- Change menu items and translations
- Replace temporary factory media

Use role-based accounts. Reserve Administrator for configuration; use Editor or a custom role for day-to-day content where practical.
