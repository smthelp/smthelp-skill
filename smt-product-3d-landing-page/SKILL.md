---
name: smt-product-3d-landing-page
description: Use when Southern Machinery / SMTHELP product photos, dimensions, drawings, catalogs, samples, or product notes need to become an interactive 3D product HTML and a customer-facing English B2B product landing page.
---

# SMT Product 3D Landing Page

## Core rule

This workflow has **two hard-gated stages**:

1. **Build and review the interactive 3D product first.**
2. **Only after explicit 3D approval, research the market and build the Southern Machinery landing page.**

Never skip the 3D review gate. Never start the final landing page merely because enough marketing information is available.

## Stage 1 — Interactive 3D first

### Intake behavior

Inspect everything the user already supplied before asking questions: photos, screenshots, drawings, PDFs, CAD, dimensions, materials, colors, and prior corrections.

Ask **one missing-information question at a time**. Do not ask for information already provided. Prioritize questions in this order:

1. Product name and actual function/use.
2. Overall dimensions and units: L × W × H.
3. Critical internal/working dimensions.
4. Reference views: front, rear, left/right, top, bottom; drawing/CAD if available.
5. Material, color, surface finish, transparent/opaque areas.
6. Moving structures: doors, lids, drawers, shafts, grippers, wheels, rails, hinges, covers, etc.
7. Details that must be geometrically accurate.
8. Whether the item is a standard product or a customer-specific/custom project.
9. If dimensions are still missing, ask whether photo-proportion inference is acceptable for the 3D concept.

If the user supplies a CAD/3D file, prefer using or converting real geometry when practical. Otherwise build the object from Three.js geometry and grouped meshes.

### 3D construction contract

The 3D must be **real interactive geometry**, not a product photo pasted onto a box.

Model meaningful physical structures as separate meshes/groups where relevant, e.g. body, frame, panels, walls, partitions, guards, rails, doors, handles, screws, rivets, wheels, covers, moving parts.

Default technical format:

- Single `.html` file.
- Three.js via CDN unless the task requires another method.
- OrbitControls.
- Responsive desktop/mobile canvas.
- Real dimensional scale when dimensions are supplied.
- Pure white 3D scene background by default.
- No ground plane that can occlude the model.
- Avoid shadows that hide internal structures; disable shadow maps by default for inspection models.
- Camera must allow practical inspection of internal geometry.

Default controls:

- ISO
- Top
- Front
- Side
- Rotate / drag
- Zoom
- Auto Rotate
- Reset

Add only when useful:

- Exploded View
- Wireframe
- Component visibility toggles
- Dimension/bounding helper
- Moving-part animation

### Internal assumptions vs customer facts

Internal modeling may use photo-based proportions only when necessary and allowed. Keep those assumptions internal during Stage 1 review.

Do not turn inferred geometry into confirmed product specifications.

### Stage 1 deliverable

Output:

`PRODUCT_NAME_Interactive_3D.html`

Then stop and request **3D MODEL REVIEW**. Ask the user to confirm:

- overall shape
- proportions
- internal structure
- colors/material appearance
- important details
- camera/view behavior
- whether more detail is needed

**Do not start Stage 2 until the user explicitly approves the 3D.**

---

## Stage 2 — Research + Southern Machinery landing page

Start only after the user approves Stage 1.

### A. Research before writing

Use current web research for the specific product. Determine:

- natural international/industry product names
- Google/B2B search terms and synonyms
- common material terminology
- typical applications
- normal market sizes / footprints / capacities / model families
- standard vs custom market conventions
- common buyer concerns and selling points
- relevant standards or classifications
- competitor/supplier terminology when useful

Prefer professional industrial terminology over literal Chinese translations. Example rule: do not translate a local packaging term literally if international buyers normally use `divider`, `partition`, `grid divider`, `insert`, etc.

### B. Separate facts into three buckets

Every claim used in the page must belong to one of these:

**1. CONFIRMED PRODUCT / PROJECT DATA**  
Data supplied by the user or verified from source material. May be stated directly.

**2. MARKET REFERENCE**  
Industry-standard or commonly sold sizes/options found through research. Must be labeled as `Reference Size Options`, `Common Market Footprints`, etc. Never present these as Southern Machinery stock unless confirmed.

**3. CUSTOMIZATION OPTIONS**  
Capabilities or selectable features that may be offered for a project. Label clearly as customization, not as features already present on the shown product.

### C. Customer-facing certainty rule

The final customer page must not expose internal modeling uncertainty.

Do not write customer-facing phrases such as:

- approximately
- assumed
- estimated
- tentative
- based on the supplied photo
- may be / probably
- still need confirmation
- temporarily modeled as

If a customer-facing specification is not confirmed, either:

1. omit it,
2. move it into a clearly labeled customization option, or
3. ask the user before publishing it.

Never invent performance, accuracy, resistance, temperature, load, material grade, lifetime, certification, cycle time, or safety data.

### D. Standard product vs custom case

Determine positioning before writing.

For a standard catalog product, build a normal `Product Landing Page`.

For a customer-specific/non-standard item, label the shown unit as:

**CUSTOM PROJECT EXAMPLE**

and make the core message about Southern Machinery's engineering/customization capability, e.g. `Designed Around Your Component`, rather than pretending the shown dimensions are a stock SKU.

### E. Landing-page information architecture

Default order:

1. Navigation + Southern Machinery logo
2. Hero value proposition + CTA + approved interactive 3D
3. 1–3 core selling points
4. Interactive 3D product/project section
5. Confirmed specifications or project dimensions
6. Material + industry terminology
7. Reference sizes / model options from market research
8. Customization capability
9. Typical applications
10. Engineering/custom development process
11. RFQ input checklist
12. Leon Hong contact CTA
13. Footer + contact links

Do not mechanically force every section if it adds no value, but preserve the logic: **problem → proof → engineering facts → options → customization → contact**.

### F. Southern Machinery visual language

Use the approved SMTHELP/Southern Machinery style:

- dark industrial technology theme
- Southern green + Southern cyan + dark navy/slate
- restrained glow/grid effects
- high contrast engineering cards
- white interactive 3D viewer
- real product imagery/video when available
- English-only customer page unless the user requests another language

Use `assets/southern-machinery-logo.png` as the default logo. For a standalone HTML deliverable, embed the logo as Base64 so the page remains one file.

### G. SEO / structured data

Every landing page should include appropriate:

- `<title>`
- meta description
- meta keywords
- robots
- theme color
- Open Graph title/description/image when an image is available
- semantic H1/H2 hierarchy
- JSON-LD appropriate to the page (`Product`, `Service`, or both when justified)
- primary product keyword + natural long-tail variants

Do not keyword-stuff visible copy.

### H. Default sales contact

Use these unless the user overrides them:

- **Leon Hong**
- Southern Machinery / SMTHELP
- WhatsApp / Tel: **+86 136 3277 9310**
- Email: **leon@smthelp.com**
- LinkedIn: **https://www.linkedin.com/in/leon-hong-southern-machinery/**
- Website: **https://www.smthelp.com/**

Default conversion placements:

- WhatsApp CTA in hero
- email CTA in final contact section
- Leon Hong contact card
- WhatsApp / Email / LinkedIn buttons
- floating WhatsApp button
- footer contact links

Generate a product-specific WhatsApp opening message and email subject/body. RFQ copy should ask only for useful engineering inputs such as product dimensions, quantity per tray/fixture, orientation, available space, material/ESD requirement, drawings/photos/CAD, and application process.

### I. Final technical format

Default final output:

`PRODUCT_NAME_Southern_Machinery_3D_Landing_Page.html`

Requirements:

- single HTML file
- no npm/build step
- no React/Vue dependency unless explicitly requested
- can be opened directly in a browser
- suitable for hosting, GitHub Pages, WordPress HTML integration, server upload, or sending to a customer
- preserve the approved Stage 1 3D geometry and interaction; marketing changes must not silently alter approved geometry

## Verification gate

Before claiming completion, verify the generated HTML freshly.

Check at minimum:

- file exists and is non-empty
- logo renders or is correctly embedded
- 3D engine/CDN references exist
- Three.js scene background remains white unless user changed it
- Orbit/zoom + requested view controls exist
- no ground-plane occlusion
- approved dimensions/geometric constants were not changed
- responsive CSS exists
- all internal anchors resolve
- WhatsApp number is `+8613632779310`
- email is `leon@smthelp.com`
- LinkedIn URL is correct
- no `TBD`, placeholder, lorem ipsum, or forbidden uncertainty language in customer copy
- SEO metadata + JSON-LD exist
- inline JavaScript passes syntax checks where tooling permits

If browser preview is available, inspect desktop and mobile rendering and exercise the 3D controls before declaring success.

## Quick trigger example

User:

`调用 SMT Product 3D Landing Page Skill。产品：XXX。附件是我现有的照片、尺寸和资料。`

Required first behavior:

1. Inspect supplied materials.
2. State that Stage 1 will build the 3D first.
3. Ask only the highest-priority missing question.
4. Build the interactive 3D once enough data is available.
5. Wait for 3D approval.
6. Only then perform market research and create the final landing page.
