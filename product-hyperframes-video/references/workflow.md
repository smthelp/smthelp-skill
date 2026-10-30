# Reusable Workflow For Product HyperFrames Videos

## Source Intake

1. Read the local project instructions such as `AGENTS.md` or product-folder notes.
2. Search the folder for product PDFs, PPTs, landing pages, scripts, manuals, ROI reports, and existing HTML pages.
3. If NotebookLM is requested, use the relevant notebook to ask for a short video script, key facts, and citation-friendly claim boundaries.
4. Extract only claims that are supported by source material. Mark uncertain details as `TBC`, `subject to final technical confirmation`, or `case-by-case`.

## Script Pattern For A 30s B2B Product Intro

Use five scenes, each about 6 seconds:

1. Problem: name the bottleneck or cost driver.
2. Product: introduce the machine and the main automation capability.
3. Technical proof: vision, feeders, heads, process control, or integration.
4. Quality/process value: clinching, stability, accuracy, reduced defects, or line readiness.
5. ROI/CTA: show conservative metrics and ask for BOM, PCB, component package, target UPH, or line design request.

For other durations, keep the same arc and scale the beat count:
- 15s: 3 scenes, 5s each.
- 45s: 6 scenes, 7-8s each.
- 60s: 7-8 scenes, 7-8s each.

## Visual Direction

Create `DESIGN.md` before composition HTML. Include:

- Style prompt: domain-specific mood and audience.
- Colors: background, surface, brand, accent, text, muted text.
- Typography: display and body fonts or safe fallback.
- Motion rules: transition style, energy level, and readability constraints.
- What not to do: overclaiming, generic stock images, cluttered spec tables, or off-brand palettes.

For Southern Machinery automation videos, a reliable direction is: dark precision-engineering canvas, real machine imagery, restrained data graphics, Southern Machinery blue, amber ROI highlights, and high-contrast industrial typography.

## HyperFrames Project Steps

1. Initialize or create a project folder: `<Product>-HyperFrames-<duration>s`.
2. Use `package.json` scripts like:
   - `npm run dev` -> `npx --yes hyperframes@<version> preview`
   - `npm run check` -> `npx --yes hyperframes@<version> lint && npx --yes hyperframes@<version> validate && npx --yes hyperframes@<version> inspect`
   - `npm run render` -> `npx --yes hyperframes@<version> render`
3. Write a standalone `index.html` with one root composition in `<body>`; do not wrap root standalone compositions in `<template>`.
4. Use timed scene divs with `class="clip scene"`, unique IDs, and non-overlapping track indices.
5. Use actual remote URLs for shareable product imagery. Add `alt` text. Do not use local images for customer-shareable HTML.
6. Use captions or on-screen text for customer-facing videos. Add TTS only if explicitly requested or if a voiceover deliverable is needed.
7. Keep all GSAP timeline construction synchronous.

## Validation And Fixes

Run checks before render:

```bash
npm run check
```

Fix these hard failures first:

- Missing `clip` class on timed visual elements.
- Missing root composition attributes.
- Unregistered `window.__timelines` timeline.
- Remote image CORS failures caused by unnecessary `crossorigin` attributes.
- Text overflow, clipped captions, or off-canvas elements reported by `inspect`.

Warnings that are often acceptable for intentionally animated sales videos:

- GSAP studio edit warnings when many elements are deliberately timeline-controlled.
- Duplicate media discovery warnings caused by repeated logo images.
- Overlap warnings on unresolved selectors when visual inspection passes and `overwrite: "auto"` is set.

## Rendering And QA

Render standard review MP4:

```bash
npm run render -- --output <Product>-<duration>s.mp4 --quality standard --fps 30
```

Verify duration and size:

```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 <file>.mp4
```

Start preview:

```bash
npm run dev -- --port <port>
```

Return the Studio URL as:

```text
http://localhost:<port>/#project/<project-folder-name>
```

## S7900 Example Claim Boundaries

For S7900 Odd Form Insertion Machine-style videos, use this pattern when supported by the product sources:

- Four insertion heads.
- Flexible feeders such as tape, tube, tray, and bowl when supported by the configuration.
- Top mark CCD and bottom component CCDs for alignment/inspection.
- Lead clinching as configuration-specific; lead diameter and exposed lead rules must be sourced and treated as subject to final design.
- Metrics such as `4,700/H`, `1 machine = 5 operators`, or `< 2 years ROI` must be presented as source examples or case-by-case, not as universal guarantees.

