# Visual modes — AI clips vs original materials

## Mode A — AI-generated clips

Use when: no usable product photos exist, or the product's mechanism is best shown as 3D animation.

- 6–8 clips, ~10 s each, one per script beat: pain point → feed/load → key mechanism close-up → detection/check → full line panorama → manual-vs-auto contrast → hero shot.
- Video generation tools cap at 6 clips per message: generate in two batches; fill any remaining segment with a Ken Burns still.
- Each clip is slowed to segment length (see `pipeline.md` §1).
- Prompts must describe the product's real mechanism and colours from the landing page — never invent features, gauges, or brand marks.

## Mode B — Original materials only (default when the user supplies photos)

Use when: the user uploads photos, links product images, or supplies a video/photo set. **This is the default whenever originals exist.**

- All picture content comes from the user's attachments and linked pages. No AI-generated images or video. No stock photos. No images from the web.
- Allowed processing only: slow zoom/pan (Ken Burns), 16:9 crop, concat, subtitle burn-in, title bars (e.g. a top navy bar with "smthelp.com" on the closing segment — bottom kept clear for subtitles).
- Never alter the content of a photo (no removing logos, people, or backgrounds; no recolouring).
- If a segment has no matching photo, use the closest product photo or a spec/diagram image — do not generate a filler image. Tell the user which segment reused which photo in the delivery report.

### Proven Mode B mapping (Radial Splicing Tape v2, 8 × 11.346 s)

| Seg | Time | Script beat | Photo used |
|---|---|---|---|
| 1 | 0:00 | Pain point: reel runs out, line stops | Tape rolls / reel photo, slow zoom in |
| 2 | 0:11 | Product reveal | 3/5/6-hole rolls side by side, slow zoom out |
| 3 | 0:23 | Mechanism: holes align, sprocket drives through | Splice tape close-up, slow zoom in |
| 4 | 0:34 | Specs | Dimensions diagram (5.673 s) + roll photo (5.673 s) |
| 5 | 0:45 | Tool / cutter | Cutter CAD render, slow left-to-right pan |
| 6 | 0:57 | Four-step method | 4-panel how-to, slow zoom out (all steps visible) |
| 7 | 1:08 | EMS benefits | Cutter in-use photo, slow zoom in |
| 8 | 1:19 | Closing + CTA | Hero shot + top navy bar "smthelp.com" |

## Decision rule

1. User supplies photos/video → Mode B, always. (Jason's 2026-11-13 boundary.)
2. User asks for "3D animation" and supplies no photos → Mode A, and say so in the delivery.
3. User asks for a new version of an existing video → keep the mode of the version being replaced unless told otherwise; a mode change is a new version (v1 → v2), with the old files kept intact.
4. Mixed: AI clips for mechanism close-ups + photos for the rest is allowed only when the user has not restricted the job to originals.
