---
name: build-fast-3d-html-viewer
description: Build fast-loading WordPress-compatible single HTML interactive 3D product pages from STEP/STP or CAD-derived product models. Use when the user asks to convert a Southern Machinery SMT/THT feeder, nozzle, machine module, or 3D drawing into a browser page and mentions speed, compression, smaller model size, text-first loading, lazy 3D startup, staged/step-by-step 3D display, SMT layout grid-floor images, product PDF references, or repeated single-HTML product viewer generation.
---

# Build Fast 3D HTML Viewer

Use this skill to create a self-contained Southern Machinery product page where sales text appears first and the optimized 3D viewer starts after the page is readable.

## Core Rules

- Prefer `.step` or `.stp` for real WebGL conversion. Use SolidWorks or 3D PDF files only as source/reference unless a verified conversion path is available.
- Preserve all original CAD files. Create derivative projects under `F:\baidunetdiskworkspace\Product Presentation\3D-PDF\output\`.
- Treat CAD, 3D PDFs, and filenames as visual/layout evidence, not final technical proof.
- Do not invent dimensions, speed, accuracy, compatibility, price, certification, lead time, or machine support. Mark unsupported values as `to be confirmed`.
- For third-party brands such as JUKI, Panasonic, FUJI, Universal, or UIC, frame the page as compatibility, retrofit, feeder/nozzle, or integration context.
- Default to Simplified Chinese progress/final reports for this user; write the generated customer-facing page in natural English unless the user requests Chinese.

## Fast Template

Use the bundled template:

`assets/viewer-template/`

It includes:

- React + TypeScript + Three.js viewer.
- `occt-import-js` STEP conversion with reduced tessellation.
- Rounded mesh positions and omitted embedded normal arrays so the browser computes normals.
- Static HTML shell inside `#root` so product text, RFQ cards, footer CTAs, and basic SEO content appear before React boots.
- Delayed JavaScript startup controlled by `performance.lazy3dBoot`.
- `Step Mode` buttons: `Step 1`, `Step 2`, `Step 3`, and `All`.
- Optional embedded SMT layout grid-floor images.
- Playwright verification for desktop and mobile.

Create a new viewer project:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill>\scripts\new_viewer_project.ps1" `
  -ProductTitle "SEO product title here" `
  -StepPath "F:\path\model.step" `
  -OutputDirectory "F:\baidunetdiskworkspace\Product Presentation\3D-PDF\output\product-fast-viewer" `
  -PdfPath "F:\path\catalog.pdf" `
  -UseDefaultSmtLayoutFloor
```

Then run from the generated project:

```powershell
npm.cmd install
npm.cmd run all
npm.cmd run verify
```

Use `.cmd` entrypoints on Windows because PowerShell `.ps1` shims can be blocked.

## Product Copy

When the user provides a product PDF or catalog URL:

- Download it into `output/_references/` with a stable product filename.
- Extract text with `pdfplumber` or `pypdf`.
- Use the PDF only to ground definition, use case, feeder mechanism, component families, machine-integration context, and RFQ requirements.
- Avoid publishing dimensions, speed, voltage, air pressure, test counts, weight, accuracy, or compatibility as confirmed specs unless the user explicitly asks for a spec table and accepts the PDF as the source.

For Southern Machinery feeder/nozzle pages, set in `viewer-config.json`:

- `companySlogan`: `Specialized in design and manufacturing SMT THT machine for smart EMS Factory`
- `productTitle`: SEO title derived from product name and use.
- `eyebrow`: `Southern Machinery customized feeder solution` for customized feeders.
- `sourceNotice`: product definition, SMT/THT use, and an engineering-confirmation boundary.
- `marketingTiles`: exactly `Features`, `Advantages`, `Benefits`, and `Applications`.
- `rfqItems`: the information a customer must provide before quotation.
- `footerLinks`: include Southern Machinery official website and social CTAs.
- `performance.embedStepDownload`: `false` unless the user explicitly needs the STEP download embedded.
- `performance.lazy3dBoot`: `true`.
- `performance.conversionProfile`: `fast-compressed`.
- `performance.stepDisplayMode`: `true`.

Default SMT layout floor image:

`https://ph.smthelp.com/images/2025/06/06/SMT-line-Single-Lane-Layout-1.png`

Use it by passing `-UseDefaultSmtLayoutFloor` for feeder pages or when the user asks for an SMT layout image, grid floor image, layout floor, or embedded floor image.

## RFQ Mapping

- `Custom Nozzle/Gripper Nozzle`: machine model, component drawing, component samples/photos, application requirement.
- `Bowl/Vibration/Bulk Feeder`: target machine, bulk component data, sorting process, production target.
- `Axial Tape Feeder`: target machine, axial component data, tape and supply state, production requirement.
- `Radial Tape Feeder`: target machine, radial component data, tape and forming requirements, production requirement.
- `Reel Terminal Feeder`: target machine, terminal material, feeding process, production target.
- `Tube Feeder`: target machine, component and tube, feeding process, samples and testing.
- `Carrier Clip/Radial Feeder spare parts`: machine and chain data, current clip details, component information, process condition.

## Workflow

Read `references/workflow.md` when executing a conversion.

1. Inspect the source asset path and verify it exists.
2. Locate a browser-convertible STEP/STP source.
3. Download and extract any product PDF reference.
4. Create the project with `scripts/new_viewer_project.ps1`.
5. Edit `viewer-config.json` for SEO title, definition, sales tiles, RFQ cards, catalog link, footer links, and optional floor image.
6. Keep `embedStepDownload=false` for faster single HTML unless the user requests source download.
7. Run `npm.cmd install`, `npm.cmd run all`, and `npm.cmd run verify`.
8. Inspect desktop and mobile screenshots.
9. Return the WordPress HTML path, browser HTML path, verification report, model compression notes, and any engineering-confirmation limits.

## Verification

Before final response, verify:

- Single HTML file exists and opens from `file:///`.
- WebGL canvas is present and nonblank.
- Static text shell exists in the raw HTML via `data-priority-text="true"`.
- `script type="text/plain" id="app-js"` exists when lazy boot is enabled.
- Step Mode buttons are present and at least one step click changes rendering or active state.
- Logo is visible.
- Footer CTAs include the official website and social links.
- Ground image is visible under the grid when configured.
- No technical spec is presented as confirmed without a current source.
