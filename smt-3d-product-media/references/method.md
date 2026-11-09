# Method: CAD to video and deck

## 0 Collect
- CAD: STEP AP214 with colours (ask for STEP when given .x_t/.sldasm). One assembly of the whole machine is best.
- Facts: confirmed specs only (AGENTS.md v2 for S70xx, KB). Note what the CAD does NOT show (e.g. 2 heads in CAD, 4 on the product) -> disclosure.
- Optional: real footage (phone video is fine; vertical clips use `fit: blur_pad`), logo body in the CAD, deck spec + photos.

## 1 Inspect
`inspect` converts STEP -> GLB and writes `parts.csv` (node number, name, colour, bbox, faces). Sort/filter it to find:
moving table (X, Y), heads (gripper parts that press down), clinch/anvil under the board, feeders (bowls), tracks, logo bodies, camera parts.
Name-based selectors are unreliable for Chinese/GBK names; prefer node ranges + bounding boxes.

## 2 Write the job
1. `scene.groups` in priority order (table groups first, then heads/clinch/bowls by box).
2. Missing units: `copies` (moving groups) and `static_copies` (their frames/tracks) with an offset equal to the real pitch.
3. Logo: if the CAD logo sits on a hidden face, copy it with `logos.extra` to a visible face (offset by the plate thickness so it sits on the surface, not inside).
4. `props`: board home = centre of the clamp when the table is at zero; heads xy = gripper tip; points spread over the board, alternating heads.
5. `animation.scenes`: intro orbit (5 s) -> board in (5) -> feed close-up (5) -> insert (12-16) -> board out (4) -> outro orbit (5). Use `"prev"` for smooth camera moves.
6. `render.flip_x: true` when the machine's real flow is the mirror of the CAD view (S70xx: PCB flows left to right on screen).

## 3 Preview loop
`preview --t` at the middle of each scene; check: groups move as one, nothing floats, logos read correctly, board sits on the clamp, camera never clips through the frame. Fix job, repeat. Costs ~10 s per frame.

## 4 Render
~1.2 s per 1280x720 frame on one core (supersample 2). 40 s x 24 fps = 960 frames ~ 20 min on 2 workers. Run workers as separate background processes when a tool limits run time; the render resumes.

## 5 Real footage, captions, voice
- Pick 4-10 s clips that each show one thing; caption each in one line; label as real footage. Customer cases without names.
- Voice: one line per scene/clip, written to fit the slot (Chinese ~4.5 chars/s, English ~2.7 words/s for these voices). Numbers spelled as spoken ("零点五秒", "half a second").
- `sequence`: 3D steps, then real clips, then the 3D outro as end card.

## 6 Check and deliver
- Contact sheet of the final video (one frame from each segment) before sending.
- Delivery message: what is 3D illustration vs real, what was copied/assumed, voice is synthetic, where the files are (Drive id), and the open questions.

## 7 Deck
Write `deck/spec-en.json` (+zh) in smt-product-ppt-rebrand format with a `video` slide using `{video}` / `{poster}`; `deck` embeds this run's video. Follow smt-product-ppt-rebrand rules (facts only, fixed closing slides, SEO name).

## 8 Real feeder CAD with several bowls per cart (1.7.0)
When Jason sends a feeder STEP with more than one bowl and track on one cart and asks for the outlets to line up with the heads:
1. Convert to GLB, list bodies (name + bbox). Find the model axes (up = feet to bowl rim, fwd = along the tracks), each track's lateral centre, the seat (接料座) fwd position and floor height, the junction where the front linear track starts, the plates shared by both tracks, and demo parts to drop (e.g. 白色端子).
2. Pick head x: tracks of one cart are closer than the head pitch, so re-pitch heads to the platform's real pair pitch (S7020: 0.1 m) and let the tool yaw each front track a few degrees; mirror the second cart so the carts sit side by side.
3. Pick point: just behind the head's own feed-rail entry (S7020 [-0.650, 0.269]); never under the head, the board travels there.
4. Run the tool, put its GLB in props.feeder_cad (fwd y, up z, out = tool `out`, vib 0) with hide_bowls, hide the old bowl stands, drop bowl copies/groups, and add feed_tracks junction->seat plus seat->gripper.
5. Preview overview, feeder close-up and every insertion camera (copied heads and table can block transitions after re-pitching), then render. Disclose: feeder CAD real, second cart mirrored, track angles adjusted; tell Jason the cart height vs machine base.
