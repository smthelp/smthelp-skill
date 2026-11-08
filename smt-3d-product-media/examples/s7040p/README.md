# Example: S7040P (4 heads, 4 bowls)
Put the inputs next to job.json (not stored in git, too large / internal):
- inputs/Pin Eyelet Inserter.STEP  (S7020 platform STEP, Jason 2026-11-07; Drive folder of S7000 files)
- inputs/real/r1.mp4 ... r4.mp4      (real footage cuts, 1280x720: 4-head bulk with clinch 9 s, bowls 6 s, blue PCB 4 heads 6 s, water-dispenser power board 8 s)
- inputs/deck_assets/                  (photos named in deck/spec-*.json)
Then: python3 ../../scripts/smt3dmedia.py all job.json
Output reproduces S7040P-PIN-Insertion-Machine-4-Heads-Video-EN/ZH.mp4 (69 s) and the EN/ZH product presentation.
