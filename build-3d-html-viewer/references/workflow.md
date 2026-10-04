# 3D HTML Viewer Workflow Reference

## Source Priority

1. Matching `.stp` or `.step`: best for real WebGL conversion via `occt-import-js`.
2. Existing `.glb`, `.gltf`, `.obj`, or `.stl`: can be loaded if the template is adapted.
3. 3D PDF: useful as source download/visual evidence; browser PDF viewers usually do not render PRC/U3D as true interactive 3D.
4. `.SLDASM/.SLDPRT`: keep as source/reference unless a converter is available.

## Optional Grid-Floor Images

Use `groundImages` when the user asks to embed photos, line-layout images, or `ph.smthelp.com` album images into the 3D grid floor.

Default SMT layout floor: if the user asks for an `SMT layout 图片`, `地面grid网格图片`, `layout floor`, or a grid-floor image without supplying a different image, use:

`https://ph.smthelp.com/images/2025/06/06/SMT-line-Single-Lane-Layout-1.png`

Embed it as a local asset, place it below the Three.js grid, and do not hotlink it in the final single HTML.

Supported pattern:

```json
"groundImages": [
  {
    "label": "SMT production line floor image",
    "file": "ground-smt-production-line.png",
    "mime": "image/png",
    "sourceUrl": "https://ph.smthelp.com/album/smt-production-line.CTd"
  },
  {
    "label": "Auto insertion line floor image",
    "file": "ground-auto-insertion-line.png",
    "mime": "image/png",
    "sourceUrl": "https://ph.smthelp.com/album/auto-insertionmachine.5Vv/?page=17&seek=NpN6d"
  }
]
```

Process:

1. If the user provides a direct image file, copy it into the generated project's `assets/`.
2. If the user provides a Chevereto/ph.smthelp album link, fetch the page and extract a direct image URL from `og:image` or the first matching `data-object` JSON block.
3. Download the chosen full-size or medium-size image into `assets/` with a clear name such as `ground-smt-production-line.png`.
4. Add one or two entries to `viewer-config.json` under `groundImages`.
5. Rebuild the HTML so `scripts/build-single-html.mjs` embeds the images as base64 data URIs.
6. Verify screenshots manually because pixel checks only prove the WebGL canvas is nonblank, not that the selected image texture is visually useful.


### Direct image URL variant

When the user provides a direct image URL such as:

`https://ph.smthelp.com/images/2025/06/06/SMT-line-Single-Lane-Layout-1.png`

Use it as a grid-floor source without scraping an album page:

1. Download the file into the generated project's `assets/` directory with a stable name, for example `ground-smt-line-single-lane-layout.png`.
2. Add a `groundImages` entry with `label`, `file`, `mime`, and the original URL in `sourceUrl`.
3. If updating an existing product page, preserve the prior HTML and change `outputSlug` and `screenshotName` to a variant such as `product-slug-layout-floor` before building.
4. Run `npm.cmd run build` and `npm.cmd run verify`.
5. Inspect desktop and mobile screenshots manually to confirm the floor image is visible under the grid and does not obscure the product, controls, RFQ cards, or footer.

### Default SMT layout floor variant

For a new project, pass the helper flag:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill>\scripts\new_viewer_project.ps1" `
  -ProductTitle "SEO product title here" `
  -StepPath "F:\path\model.step" `
  -OutputDirectory "F:\path\output\product-viewer" `
  -UseDefaultSmtLayoutFloor
```

For an existing project:

1. Copy or download the default image into `assets/ground-smt-line-single-lane-layout.png`.
2. Add this config:

```json
"groundImages": [
  {
    "label": "SMT single-lane layout floor image",
    "file": "ground-smt-line-single-lane-layout.png",
    "mime": "image/png",
    "sourceUrl": "https://ph.smthelp.com/images/2025/06/06/SMT-line-Single-Lane-Layout-1.png"
  }
]
```

3. Preserve the old HTML by changing `outputSlug` and `screenshotName` to a `-layout-floor` variant.
4. Run `npm.cmd run build`, then `npm.cmd run verify`.
5. Inspect desktop and mobile screenshots to confirm the layout image sits below the grid and remains subtle.

## Southern Machinery Page Defaults

Use a practical sales-engineering tone. Avoid exaggerated claims. For unsupported facts, use `to be confirmed`.

### Product PDF and Feeder Copy

When the user provides a Southern Machinery product PDF or `file.autoinsertion.com/public/...pdf` reference:

1. Download the PDF into `output/_references/` with a stable product filename.
2. Pass it into the viewer project as `-PdfPath` so the final HTML embeds it as a downloadable `Catalog PDF`.
3. Extract text with `pdfplumber` or `pypdf`.
4. Use extracted facts to ground product definition, component families, feeder mechanism, integration context, and RFQ fields.
5. Avoid publishing dimensions, speed, feeding accuracy, service life, voltage/current, air pressure, test counts, weight, or compatibility as final confirmed specs unless the user explicitly asks for a spec table and accepts that the source is the PDF.

For Southern Machinery customized feeder pages, use:

- `eyebrow`: `Southern Machinery customized feeder solution`
- `sourceNotice`: explain what the feeder automates, which component supply form it handles, where it fits in SMT/THT/robot/odd-form automation, and that final interface and parameters require samples/drawings/engineering review.
- `marketingTiles`: exactly `Features`, `Advantages`, `Benefits`, `Applications`.
- Default SMT layout floor when the request mentions a feeder and does not ask for a plain/no-floor version.

Recommended RFQ card mapping:

- `Axial Tape Feeder`: target machine, axial component data, tape and supply state, production requirement.
- `Radial Tape Feeder`: target machine, radial component data, tape and forming requirements, production requirement.
- `Reel Terminal Feeder`: target machine, terminal material, feeding process, production target.
- `Tube Feeder`: target machine, component and tube, feeding process, samples and testing.
- `Belt/Bulk/Reciprocating Feeder`: target machine, component drawing, samples and feeding state, production target.
- `Carrier Clip/Radial Feeder spare parts`: machine and chain data, current clip details, component information, process condition.
- `Custom Nozzle/Gripper Nozzle`: machine model, detailed component drawing, component samples/photos, application requirement.

Default top slogan:

`Specialized in design and manufacturing SMT THT machine for smart EMS Factory`

Default footer links:

- Official Website: `https://www.smthelp.com`
- LinkedIn Company Page: `https://www.linkedin.com/company/smtmachine`
- LinkedIn Profile: `https://cn.linkedin.com/in/smtsupplier`
- Twitter: `https://twitter.com/smtspecialist`
- Facebook: `https://www.facebook.com/autoinsertion`
- YouTube Channel: `https://www.youtube.com/c/Smthelping`
- Catalog: `https://file.autoinsertion.com`
- Photos: `https://ph.smthelp.com`

## JUKI Gripper Nozzle Example

SEO title pattern:

`JUKI 2583 C SMT Gripper Nozzle for Pick-and-Place Machines`

Definition/use copy pattern:

`A gripper nozzle is a custom SMT pick-and-place end effector used to hold components that are difficult for a standard vacuum nozzle, such as connectors, terminals, odd-form parts, and tall components.`

RFQ required information:

- JUKI machine model, head/nozzle station, and current nozzle reference if available.
- Detailed component drawing with dimensions and pick area.
- Component sample/photos, weight, material, surface condition, and packaging direction.
- Target output, pickup problem, orientation requirement, and PCB clearance limits.

## Browser Verification Signals

Keep the verification report and screenshots:

- `hasCanvas: true`
- `hasWebgl: true`
- `nonBackgroundPixels` meaningfully above zero
- wireframe click changes pixels
- `logoPresent: true`
- footer link count matches expected links
- configured ground images are visible under the grid and do not obscure the model or controls

