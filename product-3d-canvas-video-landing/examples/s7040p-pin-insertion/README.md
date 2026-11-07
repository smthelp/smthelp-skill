# Reference: S7040P PIN insertion machine, customer configuration (2026-11-07)

Variant workflow reference (see SKILL.md "Variant of an existing model page"). Built before 1.2.0 with the
project's bespoke scripts; the patterns it established are now core features.

| Pattern | Now in p3cv |
|---|---|
| S7020 FAB page rewritten into S7040P copy by ~45 exact text replacements + old-name scan | `landing.replacements`, `landing.forbid` |
| "S7020T" badge on 3 real photos replaced by "S7040P" | `python3 -m p3cv relabel` |
| Frames at 1080p, lanczos-upscaled to 4K in 730-frame chunks, `-threads 1 rc-lookahead=0` (4K encode OOM at 7.9 GB) | `video.scale: 1` + `video.upscale: true` |
| Customer drawings under NDA kept out; PCB photos + part sizes shown with a caution | `privacy.confidential`, `privacy.notes` |

Configuration (user + customer RFQ): 4 vibration bowl feeders → 4 heads, one part per head, all bulk:
H1 medium pin Ø1.60 / hole 1.20 · H2 large pin Ø4.80 / 3.45 · H3 medium multi-finger clip Ø0.87 / 0.78 ·
H4 large clip Ø2.75 / 2.62 (mm). Press-fit flush (pins on the rim only, clips on the collar), PCB pedestal,
miss check, force detection option; about 0.5 s per part (user statement).
Specs from the S7040P proposal deck (S7000P data): P2P 0.025 mm, repeatability 0.05 mm, MARK correction
0.015 mm, PCB 50×50–480×390 mm, 0.79–2.36 mm, floor unit 2,160×1,330×1,530 mm, 1,200 kg, 220 V std / 120 V option.
Published pin range 1.2–4.0 mm → Ø0.87 clip and Ø4.80 pin "proven on samples first".

`insert-anim.svg.js` is the SVG mechanism module (`new InsertAnim(svg,{model})`, `render(t, focus, amt)`,
models `T`/`P`/`E`/`cycle` = example 4-head configurations, `C` = this customer, `press:true` switches clinch
bases to PCB pedestals). It predates the canvas contract in `templates/anim-template.js`: reuse its drawing
and timing logic when porting a multi-head inserter to a canvas `anim.js`.
