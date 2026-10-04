---
name: 3d-pdf-html-landing
description: Convert 3D PDF product presentation files into single-file HTML marketing SEO landing pages with browser-native WebGL product viewers. Use when Codex needs to scan folders of .pdf/.PDF assets for embedded 3D streams such as PRC/U3D, generate Southern Machinery or industrial product landing pages, preserve original PDF files, create an HTML index, or batch-convert 3D PDF catalogs into SEO pages.
---

# 3D PDF HTML Landing

Use this skill to turn 3D PDF product assets into deployable single-file HTML landing pages. The output is intended for marketing and SEO: each page includes metadata, schema data, product copy, a lightweight interactive WebGL reconstruction, CTA blocks, logo placement, and footer social links.

## Core Rule

Browsers do not natively render PRC/U3D streams embedded inside 3D PDFs. Do not claim that the generated WebGL model is the original CAD mesh unless an external converter has produced a verified glTF/GLB. Default wording: "browser-native WebGL reconstruction derived from the 3D PDF source."

## Recommended Workflow

1. Inspect the target folder with `rg --files` and identify candidate `.pdf` / `.PDF` files.
2. Detect true 3D PDFs by searching binary content for `/Subtype/3D`, `/3DD`, `/Subtype/PRC`, `/Subtype/U3D`, or `RichMedia`.
3. Classify each source from its filename: insertion machine, feeder, nozzle, conveyor, loader, unloader, wave soldering, SMT mounter, PCBA demo, or generic equipment.
4. Generate one standalone `.html` file per detected 3D PDF under an output directory such as `_exports/3d_pdf_html_landing_pages/`.
5. Generate a searchable index page and a manifest for review.
6. Validate a representative sample in a browser. Check that the canvas renders, no horizontal overflow appears, logo/footer links are present, and console errors are absent.

## Batch Script

Use `scripts/convert_3d_pdfs_to_html.py` for deterministic batch conversion:

```bash
python3 /Users/mac/.codex/skills/3d-pdf-html-landing/scripts/convert_3d_pdfs_to_html.py \
  --input "/path/to/3D-PDF" \
  --output "/path/to/3D-PDF/_exports/3d_pdf_html_landing_pages" \
  --brand southern-machinery
```

Useful options:

- `--limit N`: convert only the first N detected 3D PDFs for a smoke test.
- `--sort size`: process smaller PDFs first.
- `--geo-seo`: add generative-engine-friendly answer blocks, FAQ, qualification questions, and FAQ schema.
- `--include-all-pdfs`: generate pages for all PDFs, not only files with detected 3D markers.
- `--force`: overwrite existing generated pages.
- `--manifest-name NAME`: change the manifest filename.

## Output Requirements

- Keep original PDF files untouched.
- Use single-file HTML: inline CSS, inline JavaScript, no build step.
- Use the Southern Machinery logo URL when the brand is Southern Machinery:
  `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`
- Add footer links for LinkedIn Company Page, LinkedIn Profile, Twitter, Facebook, YouTube, `file.autoinsertion.com`, and `ph.smthelp.com`.
- Include SEO title, description, canonical-friendly filename slug, Open Graph tags, Twitter card, and Product JSON-LD.
- Use conservative product claims. Mark output, labor reduction, dimensions, delivery, and price as "to be confirmed" unless a verified catalog source is available.
- Do not add external libraries or CDN scripts unless the user explicitly allows them.

## Copy Guidance

Default audience: EMS factories, PCB assembly engineers, production managers, and automation buyers.

Default CTA:

- Send PCB sample
- Request automation feasibility review
- Share BOM and component photos
- Schedule a technical call

Default Southern Machinery positioning:

- Automation Partner, Not Supplier
- SMT + THT + wave soldering + board handling line solutions
- Shenzhen manufacturing and engineering response
- High-mix EMS automation support

Read `references/page-rules.md` when writing custom copy or modifying the generator.
