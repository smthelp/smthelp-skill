# Building the shot library (content/shots.py)

1. `bash scripts/catalog.sh source/<clip>.mp4 1` -> `<clip>.catalog.jpg` with a timestamp on every frame. Look at all of them.
2. For each usable moment write an entry: `'F7': dict(src='v2', a=25.0, b=27.3, kind='p', y0=150, blur=[...], note='inspection screen')`.
   - Ids: a letter per product area (F = offline machine, I = inline, H = other application ...) + number; variants: `z` zoomed, `b` extra blur, `h` hands.
   - `kind`: `p` portrait 720x1280 (crop 720x864 at y0), `m` 540x960 (crop 540x648), `l` landscape (lcrop=(w,h,x,y), fitted over blurred fill). Other sizes: set `cw`, `ch`.
   - `blur` boxes are in cropped-frame pixels `(x, y, w, h[, sigma])`.
3. Check each entry: from scripts/smv with SMV_PROJECT set, `python3 -c "import build; build.shot_still('F7b', 0.5, '/tmp/F7b.png')"`, then look at the still at full size - especially software title bars (e.g. "RMI X160T 2.2.2" was missed once), corner watermarks, stickers, reflections, faces in glass.
4. Prefer 4-8 s ranges of steady action; drop shaky or out-of-focus parts. Note what each shot proves (count result, label, robot, X-ray image) - scenes are written against the notes.
5. Keep a list of themes that have no footage; tell Jason and ask for clips (or use slides).
