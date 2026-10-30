# Clean shot library. Build it from catalog.sh contact sheets; verify each entry on a cropped frame.
# Keys:
#   src   clip file name in source/ without .mp4
#   a, b  usable range in seconds (no faces, no supplier logos after blur)
#   kind  'p' portrait 720x1280 -> crop 720x864 at y0 | 'm' 540x960 -> crop 540x648 | 'l' landscape (blurred fill)
#   cw/ch optional crop size override (source px); lcrop=(w,h,x,y) for landscape
#   y0    crop top (portrait/medium)
#   blur  [(x, y, w, h[, sigma]), ...] boxes in CROPPED-frame coordinates: logos, model text, title bars, Chinese UI
#   zoom  (x, y, w) optional punch-in after blur, cropped-frame coordinates
#   note  what the shot shows (used when writing scenes)
SHOTS = {
 'A1': dict(src='clip01', a=3.0, b=6.0, kind='p', y0=150, blur=[], note='machine front'),
}
