# Changelog

## 1.7.0 - 2026-11-09
- tools/align_feeder_cad.py: multi-bowl feeder carts (STEP) aligned so each track outlet meets its head's pick-up point; example config vbf_x2_s7040p.json; method section 8; docs synced for 1.5.0/1.6.0

## 1.6.0 - 2026-11-09
- props.heads[id].part: per-head part shape; new part shapes press_pin (shoulder pin) and clip (spring clip); props.pcb hole pad rings (`hole`). First used for the S7040P customer PIN job (2 pin sizes + 2 clip sizes).

## 1.5.0 - 2026-11-09
- scene.points (per-scene insert point ranges), scene.cut (hard cut instead of ease), props.feed_tracks from/to (straight 3D track between two points, rail on/off, part box + colour), props.clinch_leads (under-board clinch close-ups: inward / outward / N-style). Used for YouTube batch 4 feeder combos.

## 1.2.0 - 2026-11-08
- scene.explode: teardown / exploded view (groups move apart and back, curves out|in|hold|outin)

## 1.1.0 - 2026-11-08
- props.part eyelet shape (hollow rivet) + part color; blade shape for flat terminals; preview --t parse fix; S7040E eyelet example (4 heads, upper frame hidden)

## 1.0.0 - 2026-11-07
- First release, distilled from the S7040P work of 2026-11-07 (2-head 3D animation, 4-head version with real footage, logo and EN/ZH voiceover, S7040P product presentation). One job file (schema job@1), one CLI (doctor, init, check, inspect, preview, render, stills, real, voice, compose, deck, publish, all), CPU renderer, xy_table kinematics + plugin hook, edge-tts voice, deck via smt-product-ppt-rebrand, manifest.json traceability, smoke test, example job.

## 1.3.0 (2026-11-08)
- props.pcb.cad: embed a real PCBA STEP/GLB in the animation (smt3dlib/pcbcad.py). Board laid flat by PCA and squared up, panel array, board_color, per-head insert list by STEP group (NAUOxx); inserted parts appear when pressed in, the carried part rides under the head; props.points is generated. `pcbcad.inspect(job)` writes work/pcb_groups.csv.

## 1.4.0 (2026-11-08)
- props.feeder_cad: real feeder CAD models (STEP/GLB) on the rear feeding platform, one per head slot (smt3dlib/feedercad.py). Model axes mapped by fwd/up, outlet face placed at item.out, heavy bodies drawn as convex hulls, screws dropped, small vibration along the feed direction, explode keys F0..F3. hide_bowls skips props.bowls; hide the bowl stands with scene.hide.
- Only STEP/GLB can be read. Parasolid (.x_t) and SolidWorks (.SLDASM/.SLDPRT) must be exported to STEP AP214 first.
