# Example: S7040E Eyelet (4 heads, 4 bowls, bulk eyelets)
Shows: props.part shape "eyelet" (hollow rivet, size [outer_d, length, flange_d], gold color), 4-head copies of the S7020 platform, scene.hide for the upper frame / lamp / monitor so the heads and feeding stay in view.
Inputs (not stored in git):
- inputs/Pin Eyelet Inserter.STEP  (S7020 platform STEP)
- inputs/real/*.mp4  (real footage cuts named in job.json real.segments)
- inputs/deck_assets/ (photos named in deck/spec-*.json)
Then: python3 ../../scripts/smt3dmedia.py all job.json  -> 70 s EN/ZH video + 17-slide EN/ZH presentation.
Specs follow S7020T baseline (AGENTS.md v2): 0.5 s/part, eyelet Ø1.3–4.0 mm, PCB 80x80–380x280 mm.
