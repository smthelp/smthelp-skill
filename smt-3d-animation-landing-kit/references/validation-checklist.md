# Validation checklist (tick every item before delivery)

## Inputs and facts
- [ ] `smt3d.py validate` prints `valid` (no ERROR lines)
- [ ] Every number on page, video and SEO appears in a spec sheet/manual/PDF (`build/analysis.md`), source named in `specs.source`
- [ ] Source conflicts recorded; manual wins; no contradicted "not suitable" limits
- [ ] Before/after "A" side has no invented numbers; illustrative timing disclosed in `duel.note`
- [ ] No price anywhere; only Southern Machinery watermarked photos
- [ ] Brand/compatibility claims (Panasonic, JUKI, YAMAHA…) traced to a document, not only a logo

## 3D model
- [ ] `mesh` ran; triangles ≤ `model.triangle_budget`; `model.b64` < 1.5 MB
- [ ] Orientation and scale look right in `verify/v_3d.png`; explode does not fly parts off-screen
- [ ] Material and lighting buttons visibly change the render; fallback image present

## Page (`smt3d.py verify` automates the ✱ items)
- [ ] ✱ no page/console errors · ✱ no broken images · ✱ zero network requests on load (file://)
- [ ] ✱ 3D viewer ready, material + light buttons switch
- [ ] ✱ all configured languages switch `<html lang>`; ✱ Arabic sets `dir=rtl`
- [ ] i18n coverage ≥ UI + headings + hero + ROI + contact for every language (`build/i18n_report.json`)
- [ ] ✱ exactly `blog_count` blog articles; each has title, summary, ≥ 2 paragraphs
- [ ] ✱ ROI outputs numeric; payback appears once an investment is entered
- [ ] ✱ duel tabs + both SVG panels render; play/pause/slow work; reduced-motion shows a still frame
- [ ] ✱ mobile 390 px has no horizontal overflow
- [ ] Header logo, footer CTAs, WhatsApp FAB, phone `+86 136 0256 2576`, `wa.me/8613602562576`, info@smthelp.com match the brand blocks (or the confirmed salesperson)
- [ ] YouTube IDs verified via oEmbed

## Video
- [ ] Narration 60–180 s; captions in sync; numbers shown as digits
- [ ] Contact-sheet preview in both formats: no text/caption/callout collisions
- [ ] `finish` prints OK: 3840×2160 and 2160×3840, audio present, duration = timeline
- [ ] Thumbnail: big words, logo, product visible, < 2 MB; Shorts cover 1080×1920
- [ ] SEO: title ≤ 100 (aim ≤ 70 visible), chapters start 0:00 and ≥ 10 s apart, tags ≤ 500 chars, landing URL correct

## Delivery
- [ ] Drive folder created; all deliverables uploaded (not the segments)
- [ ] Files attached in chat; deviations from the request stated (e.g. new page instead of editing the old ones, contacts used)
- [ ] Project/skill notes updated; publish only on request
