# Troubleshooting

## Text reads backwards in the preview
The stand mapping in `logo_cad.stand_upright` is wrong for this file.
Fix the mapping in the script — never add a second axis transform in the
job or in `load_parts`, or the logo renders rotated 180° (text backwards,
lines swapped). Verify with the first preview. Never ship a mirrored logo.

## Green and teal are swapped
The colour-override rule (greener STEP body -> brand green) does not fit
this file. Swap the `green` / `teal` hex values in the job's `colors` and
re-run. Do not edit the scripts for one logo.

## Mark render shows letter fragments ("HE" / "IN" / "SMT")
`mark_only` kept the text side. The mark is the image-left part of the logo
(positive x after `stand_upright`); the threshold keeps faces with centroid
x > 0.18. If fragments appear, the logo's mark/text split is elsewhere:
render the full logo, find the x gap between mark and first letter, and set
the threshold there (edit the `threshold` argument in `logo_cad.mark_only`
callers, or pass it through the job).

## Logo is cropped left/right in a sticker
The camera is too close for the wide logo on a square canvas. Full-logo
sticker renders use eye distance 1.9 (`(0.0, 1.9, 0.0)`); the mark renders
use 1.5 (the mark is 0.8 wide and 0.865 tall after scaling, and the view at
0.95 only shows 0.60 — the mark bleeds off all edges). If a different logo
is wider, pull the eye back further. Check square renders at full size,
not at chat thumbnail size, where a crop is easy to miss.

## GIF plays as a still image / has 1-2 frames / will not open
The GIF was written by PIL's GIF writer, which corrupts multi-frame RGBA
sequences (LZW init failures, bogus frame counts). This skill assembles GIFs
only with ffmpeg palettegen/paletteuse (`save_gif` in scripts/produce.py).
Verify with: `ffprobe -v error -count_frames -select_streams v:0
-show_entries stream=nb_read_frames -of csv=p=0 file.gif` — the count must
match the design (spin 20, hello 14, demo_ready 16, lets_talk 14,
thank_you 14, see_you 16).

## GIF is over 500 KB (WhatsApp sticker limit)
Drop frames (spin 20 -> 16), shorten the animation, or lower
`max_colors` in the palettegen filter (128 -> 96). Keep 512x512.

## Text overflows its canvas (email signature / banner)
The look functions use fixed positions; a longer headline needs a shorter
text or a smaller font size in the job's `texts`. Check every look visually
before delivery — never trust coordinates alone.

## `cascadio` / `numba` import errors
Run `pip install -r requirements.txt` in a venv (`python3 -m venv
--system-site-packages venv` works; system numpy/Pillow are reused).
`doctor` lists exactly what is missing.

## `ffmpeg` not found
`apt install ffmpeg` (needs ffmpeg >= 5). The looks render without it, but
no GIF can be assembled.

## Colours look wrong on a dark background
The logo must sit on a white rounded card on dark backgrounds (brand rule).
If a look places the raw render on navy, add the card via
`logo_on_white_card` instead of pasting the render directly.
