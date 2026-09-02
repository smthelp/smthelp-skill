# Fast 3D HTML Viewer Workflow

## Source Priority

1. `.step` or `.stp`: best source for real WebGL conversion.
2. `.glb`, `.gltf`, `.obj`, `.stl`: usable only if the template is adapted.
3. 3D PDF: keep as downloadable reference; browser PDF viewers usually do not render PRC/U3D interactively.
4. `.SLDASM` or `.SLDPRT`: treat as native CAD reference unless a verified converter is available.

## Speed Defaults

Use the fast profile unless the user explicitly asks for full-detail geometry:

```json
"performance": {
  "embedStepDownload": false,
  "lazy3dBoot": true,
  "conversionProfile": "fast-compressed",
  "stepDisplayMode": true
}
```

Expected behavior:

- Do not embed the original STEP download in the final HTML by default.
- Convert STEP using reduced tessellation.
- Round mesh positions to reduce JSON size.
- Omit normal arrays and compute normals in the browser.
- Render a static text-first shell before React and WebGL start.
- Delay bundled JS execution briefly so title, product description, tiles, RFQ cards, and footer can paint first.
- Show 3D geometry in `Step 1`, `Step 2`, `Step 3`, and `All`.

## Project Creation

Use the helper:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill>\scripts\new_viewer_project.ps1" `
  -ProductTitle "SBF1001 Vibration Bowl Feeder for SMT THT Bulk Component Automation - Fast Interactive 3D Viewer" `
  -StepPath "F:\path\source.step" `
  -OutputDirectory "F:\baidunetdiskworkspace\Product Presentation\3D-PDF\output\sbf1001-fast-viewer" `
  -PdfPath "F:\path\catalog.pdf" `
  -UseDefaultSmtLayoutFloor
```

The helper copies `assets/viewer-template`, copies source assets into the generated project's `assets/`, downloads the default SMT layout floor when requested, and updates `viewer-config.json`.

## Product PDF Handling

When given a public product PDF URL:

1. Download it into `F:\baidunetdiskworkspace\Product Presentation\3D-PDF\output\_references\`.
2. Use a stable filename such as `SBF1001-Vibration-Bowl-Feeder-Catalog-V03.pdf`.
3. Extract text with `pdfplumber` or `pypdf`.
4. Ground only product definition, application, component families, feeder/process concept, and RFQ items.
5. Keep dimensions, speed, accuracy, voltage, pressure, weight, test counts, service life, and compatibility behind an engineering-confirmation boundary unless the user specifically requests a PDF-sourced spec table.

## Southern Machinery Defaults

Use these defaults for feeder/nozzle product pages:

- Slogan: `Specialized in design and manufacturing SMT THT machine for smart EMS Factory`
- Footer links: official website, LinkedIn company page, LinkedIn profile, Twitter, Facebook, YouTube.
- Catalog paragraph: `file.autoinsertion.com` and `ph.smthelp.com`.
- Sales tiles: `Features`, `Advantages`, `Benefits`, `Applications`.
- RFQ cards: four specific data groups that a customer must provide for quotation.

For customized feeders, describe Southern Machinery's scope as feeder/nozzle/fixture/integration support, not ownership of third-party machines.

## Default SMT Layout Floor

Use this image when the user asks for a grid-floor image or when making a feeder page with layout floor:

`https://ph.smthelp.com/images/2025/06/06/SMT-line-Single-Lane-Layout-1.png`

Rules:

- Download it into `assets/ground-smt-line-single-lane-layout.png`.
- Add it to `groundImages`.
- Embed it as a base64 data URI during build.
- Place it below the Three.js grid.
- Do not hotlink it in the final HTML.

## Build And Verify

Run:

```powershell
npm.cmd install
npm.cmd run all
npm.cmd run verify
```

If dependencies are already installed, `npm.cmd run all` and `npm.cmd run verify` are enough.

Verification signals:

- `hasCanvas: true`
- `hasWebgl: true`
- `nonBackgroundPixels` meaningfully above zero.
- Wireframe click changes pixels.
- `logoPresent: true`
- footer link count matches expected links.
- Step Mode controls exist.
- Raw HTML includes `data-priority-text="true"` and `script type="text/plain" id="app-js"` when lazy boot is enabled.
- Desktop and mobile screenshots show no major overlap and the floor image remains subtle.

## Final Report

Report in Simplified Chinese:

- Final WordPress HTML path.
- Browser/dist HTML path.
- Verification report path.
- Source STEP used.
- Product PDF used, if any.
- Final HTML size.
- Mesh count, vertex count, and triangle count from conversion output.
- Fast optimizations used.
- Limits: compressed model is for browser visualization, not dimensional inspection or final engineering acceptance.
