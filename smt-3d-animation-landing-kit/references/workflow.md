# Workflow in detail

1. **Deconstruct (fetch + analyze).** Read `build/analysis.md`: list each page's sections, headings, claims, images, YouTube IDs and contacts; read the PDF text.
   Write a selling-point table: pain (customer words) → feature (spec + source) → advantage → benefit. Decide the duel: two products (A vs B) or before/after (manual vs product).
   Note conflicts between sources and which wins (manual > spec sheet > landing page > brochure claims). Never use vague PDF claims (e.g. "1/39 size") that contradict dimensions.
2. **3D parse + lightweight (mesh).** `extract_mesh.py` → `mesh.json`; `pack_mesh.py` → `model.b64`. Look at `verify/v_3d.png`: orientation, scale, explode sanity.
   Use `model_groups` to merge bodies into named parts (cover, frame, track…) when you want colours/explode per assembly.
3. **Copy (content.json).** FAB copy, 6 duel chapters, 3 pain cards, how-it-works steps, specs rows quoted verbatim, fit-check ranges, 4 benefits,
   gallery, 1+ verified YouTube IDs (oEmbed), docs, FAQ, contact. Exactly `blog_count` blog articles (default 8), each: tag, title, summary, 2+ paragraphs.
   Translate with `smt3d.py i18n-todo job <lang>` → fill `i18n/<lang>.json`; at minimum UI, nav, headings, hero, ROI, contact.
4. **Mechanism animation (duel.js).** Deterministic SVG, 800×560 per side, `render(t, st)`; chapters with metrics/badges; callouts revealed by `st.step`.
   Speeds from the spec sheet only; illustrative parts flagged in `duel.note`. Test frames with a quick Playwright screenshot loop before the page.
5. **Page (lp + verify).** Fix every FAIL; eyeball `verify/*.png` (desktop, 3D, duel, zh, ar, mobile).
6. **Video.** Narration 8–10 scenes, 120–160 s; `stage` copies `video.html` (stage must expose `window.READY` + `window.seek(t)` and read `window.TIMELINE`).
   Align the duel to narration with `st.clock` offsets per scene. Preview with screenshots at key times in both formats before rendering.
   `render` 30 s segments within a budget (one renderer at a time), `finish` concatenates + muxes + checks resolution/duration.
7. **Thumbnails + SEO.** Thumbnail words ≤ 4 per side, no text over the product; SEO from `job.seo`, chapters from the timeline.
8. **Drive.** `smt3d.py drive` (or Hark: `gws drive +upload … --parent <folder>` with the Google connector). Deliver files in chat too.
9. **Publish** only after Jason confirms contacts and asks for it (WebDAV password via Hark Secured Login).
