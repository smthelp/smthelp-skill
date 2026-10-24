# Feedback log (rules learned from Jason - apply all)

- 2026-10-23 · Make videos in English, 16:9 4K, with English subtitles; no people in frame (hands only OK); remove supplier marks (rmi / 瑞茂光学 / XC-3100 / RMI) and large Chinese UI text.
- 2026-10-23 · Do not publish to YouTube; deliver to the Drive folder of the source clips; rename originals only when asked, never delete.
- 2026-10-23 · Claims not on the official product page (BGA voids, "3 days -> 2 hours", AI/zero programming, ESD/zero-loss absolutes, standards) are rewritten as hedged statements without absolute numbers; example numbers labelled on screen (approved by Jason).
- 2026-10-23 · Supplier software title bars (e.g. "RMI X160T 2.2.2") count as supplier marks - check the top strip of every software screen.
- 2026-10-23 · A second batch on the same footage must look different: mirrored layout, zoom variants, new slide designs, own intro still and music per video.
- 2026-10-24 · YouTube rejects < and > in titles/descriptions: write "below 1 µSv/h", not "< 1 µSv/h" (on-screen graphics may keep the symbol).

## 2026-10-24 S7020T batch (10 videos)
- Landscape / 4K-rotated sources: normalize first (bake rotation, max 1920 px, -g 15) into norm/ and set project source_dir; shots now take `x0` to crop any region (not just left edge). Helper functions per resolution in shots.py keep the 5:6 window crop.
- Check the first seconds of every clip for supplier logos (c34 had "拓伟业" at 0-5 s even though the rest was clean).
- Search the company's own landing pages before softening a claim: the S7020T turnkey page confirmed SMEMA, track width and force monitoring. Note conflicts between sources (weight/power) and state neither.
- Custom slides must `from gfx import _i` (underscore names are not exported by `import *`).
- Example calculations: recompute totals in code before writing narration (a labour total was first written 2x too high).
- upload.py --doc failed: gws only uploads from the current directory -> script now chdirs to final/<batch>.
- Sandbox can reset mid-batch (numpy missing): rerun setup.sh and the failed slug.
