---
name: product-hyperframes-video
description: Create short product introduction videos with HyperFrames from local product folders, NotebookLM product notes, remote image/catalog/model links, and verified product facts. Use when Codex is asked to generate, adapt, preview, validate, or render a 15-60 second product promo/explainer video, especially for Southern Machinery SMT/THT equipment, ROI-driven product introductions, or reusable HTML/MP4 sales videos.
---

# Product HyperFrames Video

## Overview

Use this skill to turn product materials into a validated HyperFrames video project and MP4 export. Favor concise B2B storytelling: product problem, automation capability, proof points, ROI framing, and a clear next step.

Also load these skills when available and relevant:
- `hyperframes:hyperframes` for composition authoring.
- `hyperframes:hyperframes-cli` for init, lint, inspect, preview, render, and TTS.
- `hyperframes:gsap` when writing or debugging timeline animation.
- `notebooklm` when the user asks to use NotebookLM notes or product notebooks.

## Workflow

1. Gather source facts from the product folder and NotebookLM notes before writing claims.
2. Build a 5-7 beat script for 15-60 seconds. For a 30s product intro, prefer five 6-second scenes.
3. Create a HyperFrames project folder named `<Product>-HyperFrames-<duration>s`.
4. Write `DESIGN.md` before `index.html`. Define exact palette, typography, visual tone, motion rules, and claim limits.
5. Author `index.html` as the source of truth: timed `clip` scenes, remote image URLs, GSAP timeline, captions, and CTA.
6. Run `npm run check` or the equivalent `hyperframes lint && validate && inspect`; fix hard errors before rendering.
7. Render MP4 with `hyperframes render`, then verify duration and output file size.
8. Start `hyperframes preview` and give the Studio URL plus MP4 path in the final response.

For the exact reusable procedure, read [references/workflow.md](references/workflow.md) when executing a real video task.

## Content Rules

- Use verified product specifications only. If a number comes from a case example, label it as an example or case-by-case.
- Do not present ROI, UPH/CPH, labor replacement, price, lead time, or yield as unconditional guarantees.
- Keep sales videos customer-facing in English unless the user asks otherwise.
- Use remote product images and links when the output must be shareable. Do not embed local files in customer-facing HTML unless explicitly requested.
- For Southern Machinery product videos, use real product visuals from `https://ph.smthelp.com` when suitable and catalog/model links from `https://file.autoinsertion.com` when required.

## HyperFrames Requirements

- Every timed visual scene must include `class="clip"`, `data-start`, `data-duration`, and `data-track-index`.
- The root composition must include `data-composition-id`, `data-start="0"`, `data-duration`, `data-width`, and `data-height`.
- Register a paused GSAP timeline as `window.__timelines["<composition-id>"]`.
- Use CSS for final layout positions; animate from or to those positions with transforms and opacity.
- Avoid `crossorigin="anonymous"` on remote images unless the host provides CORS headers; it can break local validation/rendering.
- Prefer stable text sizes, bounded panels, and captions that remain readable for at least 2 seconds.

## Output Checklist

Before final response, confirm:
- HyperFrames check passed with no validation or layout errors.
- MP4 duration matches the requested length.
- Final file path exists and is accessible.
- Preview server is running, or explain why it could not be started.
- ROI and performance claims are qualified when they are examples.

