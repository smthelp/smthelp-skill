# SVG Process Flow — Layout Cheatsheet

When building the `.flow` SVG in an explainer page, the station positions and visual hierarchy matter. This is the reference for the standard 7-station SMT line (Loader → Printer → Pick and Place → SPI → Reflow Oven → AOI → Unloader). 1100×360 viewBox, 7 stations, with optional off-line THT/Wave branch.

## Station x-coordinates (7 stations, 100px wide, ~40px gap)

| # | Station | x | width | y | height | Notes |
|---|---------|---|-------|---|--------|-------|
| 1 | Loader | 60 | 100 | 130 | 100 | Left margin 60, start of line |
| 2 | Printer | 200 | 100 | 130 | 100 | Gap 40 from station 1 |
| 3 | **Pick and Place** | 340 | **115** | 125 | 110 | First "core" machine — width 115, height 110, neon-green stroke |
| 4 | SPI | 495 | 100 | 130 | 100 | After P&P, gap 40 |
| 5 | **Reflow Oven** | 635 | **160** | 125 | 110 | Second "core" machine — width 160 (wider because it spans zones), neon-green stroke |
| 6 | AOI | 835 | 100 | 130 | 100 | Gap 40 from Reflow |
| 7 | Unloader | 975 | 90 | 130 | 100 | Right edge — 90 wide to fit before x=1060 right margin |

Track line: `M 40 180 L 1060 180` (stroke `#13283f`, stroke-width 6, stroke-linecap round)
Pulse line: same coords, stroke `#00e5ff`, stroke-width 2, `stroke-dasharray="8 28"`, opacity 0.7, animation `flowDash 2.2s linear infinite` (animates `stroke-dashoffset: -36`)

## Arrows (small triangles at each gap)

Five arrows between 7 stations — coordinates match the gaps:

```
160,175  175,180  160,185
300,175  315,180  300,185
455,175  470,180  455,185
595,175  610,180  595,185
795,175  810,180  795,185
935,175  950,180  935,185
```

Fill `#00e5ff`, opacity 0.7.

## Visual hierarchy rules

- **Cyan stroke (#00e5ff) + width 100** = standard station (Loader, Printer, SPI, AOI, Unloader)
- **Neon-green stroke (#39ff7a) + width 115–160** = "core" machine (Pick and Place, Reflow Oven)
- **Orange stroke (#ffb84d) + dashed lines** = off-line THT/Wave Soldering branch (visually separate from the main cyan flow)

## Off-line THT/Wave branch (always at the bottom, drops from Reflow Oven center x=715)

```
vertical drop:   M 715 240 L 715 290  (orange, dashed 4 4)
horizontal run:  M 715 290 L 200 290  (orange, dashed 4 4, opacity 0.5)
label box:       rect x=80 y=305 w=240 h=44, stroke orange
title text:      x=200 y=332, fill orange, font-weight 700
subtitle text:   x=200 y=350, fill #7fa3c7
```

## Title block at the top of the SVG

```
title:    x=550 y=40  (font-size 14, weight 700, letter-spacing 2)
subtitle: x=550 y=60  (font-size 11, fill #7fa3c7)
```

Example title: `SMT FRONT-END · LED TUBE LINE`
Example subtitle: `Loader → Printer → Pick and Place → SPI → Reflow Oven → AOI → Unloader`

## Animation classes

```css
.machine {
  transform-origin: center;
  transform-box: fill-box;
  animation: machineFloat 3.4s ease-in-out infinite;
}
@keyframes machineFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}
```

Stagger the animation across stations using `style="animation-delay: 0.2s"`, `0.4s`, `0.6s`, etc. on each `<g class="machine">` block — creates a gentle wave that suggests production flow direction.

## Common alternative line configurations (drop-in station swaps)

| Industry / Use case | Station swap |
|---------------------|--------------|
| **Automotive THT-heavy** | Replace AOI station with a second THT Insertion machine; emphasize the off-line Wave Soldering branch |
| **LED tube long-board** | Add 2-pane Printer (because PCB > 1200mm); widen Loader/Unloader by 20px each |
| **Power supply high-mix** | Insert a second Pick and Place (multi-function) between P&P and SPI for odd-form components |
| **Selective solder line** | Replace Reflow Oven with Selective Soldering module (different model, same x-position) |

## Pitfall: text overflow on long machine names

If a machine name > 14 chars (e.g. "Selective Soldering"), the text will wrap past the rect bounds. Workarounds:
- Shorten label to 2 words ("Selective Sold.")
- Reduce font-size to 10 for that station only
- Widen the rect to 130 (and shift neighbors)

## Pitfall: SVG <text> alignment

Always use `text-anchor="middle"` and place x at the station's horizontal center, not the rect's x. Common mistake: `<text x="60">` instead of `<text x="110">` (rect at 60 + half width 50 = 110).
