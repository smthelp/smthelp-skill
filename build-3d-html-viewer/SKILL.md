---
name: build-3d-html-viewer
description: Build WordPress-compatible single HTML interactive 3D product pages from CAD or 3D visual assets. Use when the user asks to convert STEP/STP, SolidWorks SLDASM/SLDPRT, 3D PDF, or product 3D drawings into a browser-viewable page, especially Southern Machinery SMT/THT feeder/nozzle pages with catalog PDF/URL references, SEO title, product definition, Features/Advantages/Benefits/Applications cards, RFQ requirements, footer CTAs, optional SMT layout grid floors, and real browser verification.
---

# Build 3D HTML Viewer

Use this skill to turn a product CAD/3D asset into a self-contained, customer-facing HTML page with a real WebGL viewer.

## Core Rules

- Prefer a matching `.stp` or `.step` file for real browser 3D. Browser pages cannot directly render SolidWorks `.SLDASM/.SLDPRT` reliably without conversion.
- If the user gives `.SLDASM/.SLDPRT`, search the same folder and current 3D asset library for a matching `.stp/.step`, `.glb`, `.obj`, or existing 3D PDF export before asking for help.
- Treat 3D PDF, SolidWorks, and CAD filenames as visual/layout evidence, not verified technical specifications.
- Do not invent dimensions, compatibility, price, lead time, certification, or machine support. Mark unverified specs as `to be confirmed`.
- For third-party names such as JUKI, FUJI, Panasonic, Universal, or UIC, present the page as compatibility/reference context, not as a Southern Machinery-owned machine.
- Preserve original assets. Create derivative projects under an output folder.

## Reusable Template

Use the bundled template at:

`assets/viewer-template/`

It contains:

- React + TypeScript + Three.js viewer.
- `occt-import-js` STEP-to-mesh conversion.
- single HTML build script.
- Playwright verification script.
- Southern Machinery logo asset.
- optional `groundImages` support for embedding one or two local/downloaded PNG/JPG/WebP images as the 3D grid floor, including direct `https://ph.smthelp.com/images/...` URLs.
- configurable `viewer-config.json`.

Use the helper script to start a new project:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill>\scripts\new_viewer_project.ps1" `
  -ProductTitle "SEO product title here" `
  -StepPath "F:\path\model.stp" `
  -OutputDirectory "F:\path\output\product-viewer" `
  -PdfPath "F:\path\source-3d.pdf" `
  -NativePath "F:\path\source.SLDASM" `
  -GroundImagePaths "F:\path\floor-1.png","F:\path\floor-2.png" `
  -UseDefaultSmtLayoutFloor
```

Then run inside the generated project:

```powershell
npm.cmd install
npm.cmd run all
npm.cmd run verify
```

Use `.cmd` entrypoints on Windows (`npm.cmd`, `npx.cmd`) because PowerShell `.ps1` shims can be blocked.

## Page Content Pattern

For Southern Machinery pages, set these fields in `viewer-config.json` before building:

- `companySlogan`: `Specialized in design and manufacturing SMT THT machine for smart EMS Factory`
- `productTitle`: SEO-focused title derived from the filename and product use.
- `sourceNotice`: definition plus SMT/THT industry use. Explain what the product does and why customers use it.
- `marketingTiles`: exactly four customer-facing cards:
  - `Features`
  - `Advantages`
  - `Benefits`
  - `Applications`
- `rfqItems`: what the customer must provide before quotation.
  - For JUKI/custom nozzles: machine model, component drawing, component samples/photos, and application requirement.
  - For machine modules: PCB size, process route, target volume, layout limits, and automation level.
- `footerLinks`: include Southern Machinery Official Website, social links, and catalog/photo links unless the user asks otherwise.
- `groundImages`: optional list of one or two local image files copied into `assets/`; the build script embeds them as base64 and the Three.js scene places them below the grid floor.
- Default SMT layout floor image: when the user asks for `SMT layout 图片`, `grid 网格图片`, `地面图`, `layout floor`, or `包含地面grid网格图片` without giving a different image, use `https://ph.smthelp.com/images/2025/06/06/SMT-line-Single-Lane-Layout-1.png`. Embed it into `assets/` and place it below the Three.js grid, not as a hotlinked image.

When the user provides a product reference PDF or catalog URL:

- Download the PDF into `output/_references/` with a stable product filename, then pass it as `-PdfPath` so the single HTML embeds it as a downloadable `Catalog PDF` or `Reference PDF`.
- Extract text with `pdfplumber` or `pypdf` and use it only to ground definition/use, component families, feeder mechanisms, machine integration context, and RFQ fields.
- Do not present dimensions, speed, accuracy, service life, test counts, voltage, air pressure, weight, or compatibility as final confirmed specs unless the user explicitly asks for a spec table and accepts that values come from that PDF. Otherwise summarize as engineering-confirmation items.
- For Southern Machinery customized feeder pages, set `eyebrow` to `Southern Machinery customized feeder solution` and include the standard SMT layout floor by default when the request mentions a feeder and does not ask for a plain/no-floor version.
- Use `Catalog PDF` for Southern Machinery product PDFs, and `Reference PDF` for third-party compatibility or spare-part references.

For feeder/nozzle product pages, map the RFQ cards to the feeder type:

- `Axial Tape Feeder`: target machine, axial component data, tape and supply state, production requirement.
- `Reel Terminal Feeder`: target machine, terminal material, feeding process, production target.
- `Tube Feeder`: target machine, component and tube, feeding process, samples and testing.
- `Belt/Bulk/Reciprocating Feeder`: target machine, component drawing, samples and feeding state, production target.
- `Carrier Clip/Radial Feeder spare parts`: machine and chain data, current clip details, component information, process condition.
- `Custom Nozzle/Gripper Nozzle`: machine model, detailed component drawing, component samples/photos, application requirement.

Example:

```json
"groundImages": [
  {
    "label": "SMT production line floor image",
    "file": "ground-smt-production-line.png",
    "mime": "image/png",
    "sourceUrl": "https://ph.smthelp.com/album/smt-production-line.CTd"
  }
]
```

When the user gives `ph.smthelp.com/album/...` links, fetch the album page, extract the direct image URL from `og:image` or Chevereto `data-object` JSON, download the image into the generated project's `assets/`, and add it to `groundImages`. When the user gives a direct image URL such as `https://ph.smthelp.com/images/.../SMT-line-Single-Lane-Layout-1.png`, download that file directly into `assets/` and add it to `groundImages` with the original URL in `sourceUrl`. Do not hotlink the image in final HTML; embed it so the single file works offline. For new projects that should use the standard SMT layout floor, pass `-UseDefaultSmtLayoutFloor` to `scripts/new_viewer_project.ps1`; for existing projects, copy/download the file into `assets/`, change `outputSlug`/`screenshotName` to a `-layout-floor` variant, add a `groundImages` entry, then run `npm.cmd run build` and `npm.cmd run verify`.

## Workflow

1. Inspect the user-provided asset path and current workspace instructions.
2. Locate a browser-convertible source, preferably STEP/STP.
3. Create a derivative project with `scripts/new_viewer_project.ps1`.
4. Edit `viewer-config.json` for product-specific SEO, definition/use, Features/Advantages/Benefits/Applications, RFQ requirements, and optional `groundImages`. If adding the standard SMT layout image to an existing HTML, preserve the original output and create a `-layout-floor` output variant unless the user explicitly asks to overwrite the current version.
5. Run `npm.cmd install`, `npm.cmd run all`, and `npm.cmd run verify`. When adding a ground image to an already-built project, keep the existing original HTML, change `outputSlug`/`screenshotName` to a new variant such as `product-slug-layout-floor`, run `npm.cmd run build`, then `npm.cmd run verify`.
6. Inspect desktop and mobile screenshots from the verification folder.
7. Return the final single HTML path, verification report, source file used, and any limitations.

## Verification Requirements

Before final response, verify:

- The final HTML exists and opens from `file:///`.
- WebGL canvas is present and nonblank.
- Model controls work at least enough for wireframe/pixel change verification.
- Southern Machinery logo is visible.
- Footer CTAs are present, including the Official Website link.
- If `groundImages` is configured, inspect screenshots and confirm the image texture is visible under the grid. For direct SMT layout images, the floor image should be visible but subtle enough not to obscure the model or controls.
- SEO title and visible H1 match the product.
- No technical spec is presented as confirmed unless verified from a current source.

## Fallbacks

- If no STEP/STP exists but a 3D PDF exists, create a single HTML page that embeds/downloads the 3D PDF and clearly states that browser PDF viewers may not render PRC/U3D interactively.
- If Blender, FreeCAD, or another converter is installed, use it only when it can produce a verified GLB/OBJ/STL and inspect the result in browser.
- If only SolidWorks native files exist and no converter is available, ask for STEP export or permission to use an installed CAD converter. Do not pretend the SolidWorks file became real WebGL.

