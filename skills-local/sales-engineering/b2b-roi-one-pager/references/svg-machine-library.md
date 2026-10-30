# Inline SVG Machine Library

This file is the **drop-in SVG schematic collection** for the hero of the ROI one-pager. Each machine has a stylized 3D-ish inline SVG that works in any PDF reader, scales perfectly, and looks professional.

**Why inline SVG and not photos?** Factory photos on smthelp.com have green annotation ovals, arrows, and Chinese teaching text baked in. They look amateur in a B2B sales PDF — they scream "I grabbed this from a Chinese PowerPoint deck." Inline SVG is the professional alternative. Trade-off: the customer doesn't see the actual machine, but they know what an inserter looks like — what they need to see is the value prop and the ROI math.

All SVGs use the same color palette to match the rest of the one-pager:

- Navy `#0E2A47` / `#1A3A5C` — chassis, control panel
- Orange `#FF6B1A` — active components, highlights, Z-axis head
- Cream `#F4F1EC` — main body fill
- Steel `#A8B0BB` — borders
- Green `#1B4D2E` / `#2D7A4A` — vibratory bowl
- PCB Green `#1F8A3E` / `#0E5A26` — PCB on conveyor
- Charcoal `#1A1A1A` — Z-axis rod, status text

All SVGs are sized at `viewBox="0 0 320 220"` and rendered with CSS `max-height: 42mm` so they always fit the hero region on A4.

---

## S-70LD — Odd-Form Inserter (the canonical schematic)

**Use this as the default.** Vibratory bowl on the left, tape feeder rail on the right, Z-axis insertion head in the middle, PCB conveyor at the bottom.

```html
<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" class="machine-svg">
  <ellipse cx="160" cy="200" rx="130" ry="6" fill="rgba(0,0,0,0.25)"/>
  <rect x="40" y="60" width="240" height="130" rx="6" fill="#F4F1EC" stroke="#A8B0BB" stroke-width="1.2"/>
  <rect x="48" y="50" width="100" height="22" rx="2" fill="#1A3A5C" stroke="#0E2A47"/>
  <circle cx="58" cy="61" r="3" fill="#FF6B1A"/>
  <rect x="68" y="58" width="60" height="6" rx="1" fill="#4A6585"/>
  <rect x="78" y="55" width="50" height="2" fill="#FF6B1A" opacity="0.8"/>
  <circle cx="115" cy="125" r="34" fill="#1B4D2E" stroke="#0E2A47" stroke-width="1"/>
  <circle cx="115" cy="125" r="28" fill="none" stroke="#2D7A4A" stroke-width="0.5" stroke-dasharray="2 2"/>
  <circle cx="115" cy="125" r="6" fill="#FF6B1A"/>
  <text x="115" y="173" text-anchor="middle" font-size="7" fill="#0E2A47" font-weight="700" font-family="Inter">VIBRATORY BOWL</text>
  <rect x="160" y="100" width="105" height="50" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <rect x="165" y="106" width="95" height="6" fill="#0E2A47"/>
  <rect x="165" y="116" width="95" height="6" fill="#0E2A47" opacity="0.7"/>
  <rect x="165" y="126" width="95" height="6" fill="#0E2A47" opacity="0.5"/>
  <rect x="165" y="136" width="95" height="6" fill="#0E2A47" opacity="0.3"/>
  <text x="212" y="173" text-anchor="middle" font-size="7" fill="#0E2A47" font-weight="700" font-family="Inter">TAPE FEEDER RAIL</text>
  <rect x="195" y="65" width="14" height="30" fill="#FF6B1A" stroke="#0E2A47" stroke-width="0.8"/>
  <rect x="192" y="92" width="20" height="10" fill="#1A1A1A"/>
  <line x1="202" y1="102" x2="202" y2="115" stroke="#1A1A1A" stroke-width="2"/>
  <rect x="198" y="115" width="8" height="5" fill="#5A6573"/>
  <rect x="60" y="175" width="200" height="14" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="80" y="178" width="160" height="8" fill="#0E5A26"/>
  <circle cx="100" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="140" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="180" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="220" cy="182" r="1.5" fill="#FF6B1A"/>
  <text x="160" y="206" text-anchor="middle" font-size="7" fill="#FF6B1A" font-weight="700" font-family="Inter">PCB INSPECTION · INSERTION ZONE</text>
  <line x1="202" y1="60" x2="202" y2="40" stroke="#FF6B1A" stroke-width="0.8" stroke-dasharray="2 2"/>
  <text x="202" y="36" text-anchor="middle" font-size="6.5" fill="#FF6B1A" font-weight="700" font-family="Inter">±0.5mm HEAD</text>
</svg>
```

**Key visual cues:**
- Green circle on the left = vibratory bowl (the "odd-form" feeder)
- Grey strip on the right = tape feeder rail (for the smaller components)
- Orange Z-axis = the insertion head (the "money shot")
- Green PCB at the bottom = the workpiece, with orange dots = insertion points

---

## S-3000 — Radial Inserter (High-Speed, CPH Heavy)

**Use for power supply / EV charger / LED driver / high-volume radial lines.**

Differences from S-70LD: NO vibratory bowl, LARGER tape feeder rail (8-12 stations), Z-axis rides on horizontal gantry not just vertical.

```html
<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" class="machine-svg">
  <ellipse cx="160" cy="200" rx="130" ry="6" fill="rgba(0,0,0,0.25)"/>
  <rect x="40" y="60" width="240" height="130" rx="6" fill="#F4F1EC" stroke="#A8B0BB" stroke-width="1.2"/>
  <rect x="48" y="50" width="100" height="22" rx="2" fill="#1A3A5C" stroke="#0E2A47"/>
  <circle cx="58" cy="61" r="3" fill="#FF6B1A"/>
  <rect x="68" y="58" width="60" height="6" rx="1" fill="#4A6585"/>
  <text x="98" y="63" text-anchor="middle" font-size="6" fill="#FF6B1A" font-weight="700" font-family="Inter">18,000 CPH</text>
  <!-- Long tape feeder rail at top -->
  <rect x="60" y="80" width="200" height="32" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <rect x="65" y="84" width="32" height="24" fill="#0E2A47" opacity="0.7"/>
  <rect x="100" y="84" width="32" height="24" fill="#0E2A47" opacity="0.85"/>
  <rect x="135" y="84" width="32" height="24" fill="#FF6B1A" opacity="0.8"/>
  <rect x="170" y="84" width="32" height="24" fill="#0E2A47" opacity="0.7"/>
  <rect x="205" y="84" width="32" height="24" fill="#0E2A47" opacity="0.85"/>
  <text x="160" y="125" text-anchor="middle" font-size="6.5" fill="#0E2A47" font-weight="700" font-family="Inter">12-STATION TAPE FEEDER RAIL</text>
  <!-- Gantry-mounted Z-axis -->
  <rect x="40" y="100" width="240" height="6" fill="#5A6573"/>
  <rect x="155" y="100" width="14" height="35" fill="#FF6B1A" stroke="#0E2A47" stroke-width="0.8"/>
  <rect x="152" y="135" width="20" height="8" fill="#1A1A1A"/>
  <line x1="162" y1="143" x2="162" y2="155" stroke="#1A1A1A" stroke-width="2"/>
  <rect x="158" y="155" width="8" height="5" fill="#5A6573"/>
  <text x="180" y="150" font-size="5.5" fill="#FF6B1A" font-weight="700" font-family="Inter">±0.001mm</text>
  <!-- PCB -->
  <rect x="60" y="175" width="200" height="14" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="80" y="178" width="160" height="8" fill="#0E5A26"/>
  <circle cx="90" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="120" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="150" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="180" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="210" cy="182" r="1.5" fill="#FF6B1A"/>
  <text x="160" y="206" text-anchor="middle" font-size="7" fill="#FF6B1A" font-weight="700" font-family="Inter">RADIAL INSERTION · 18,000 CPH</text>
</svg>
```

**Key visual cues:**
- Wide tape feeder rail with 5 visible stations, one in orange = the "live" station
- Gantry bar across the top (X-axis) with Z-axis hanging from it
- "18,000 CPH" displayed on the control panel
- Higher density of orange dots on the PCB (radial components are dense)

---

## S-4000 — Axial Inserter (Diodes, Resistors, Small Inductors)

**Use for power supply / telecom / industrial control lines with axial components.**

Differences: tape feeders run VERTICAL (axial components lead-down) instead of horizontal.

```html
<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" class="machine-svg">
  <ellipse cx="160" cy="200" rx="130" ry="6" fill="rgba(0,0,0,0.25)"/>
  <rect x="40" y="60" width="240" height="130" rx="6" fill="#F4F1EC" stroke="#A8B0BB" stroke-width="1.2"/>
  <rect x="48" y="50" width="100" height="22" rx="2" fill="#1A3A5C" stroke="#0E2A47"/>
  <text x="98" y="63" text-anchor="middle" font-size="6" fill="#FF6B1A" font-weight="700" font-family="Inter">22,000 CPH</text>
  <!-- Vertical tape feeder columns -->
  <rect x="70" y="75" width="20" height="50" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <rect x="100" y="75" width="20" height="50" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <rect x="130" y="75" width="20" height="50" rx="2" fill="#FF6B1A" opacity="0.8" stroke="#A8B0BB"/>
  <rect x="160" y="75" width="20" height="50" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <rect x="190" y="75" width="20" height="50" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <rect x="220" y="75" width="20" height="50" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <text x="155" y="138" text-anchor="middle" font-size="6.5" fill="#0E2A47" font-weight="700" font-family="Inter">VERTICAL AXIAL FEEDERS</text>
  <!-- Cut-and-clinch head -->
  <rect x="145" y="50" width="30" height="20" fill="#FF6B1A" stroke="#0E2A47" stroke-width="0.8"/>
  <line x1="160" y1="125" x2="160" y2="155" stroke="#1A1A1A" stroke-width="2"/>
  <text x="195" y="60" font-size="5.5" fill="#FF6B1A" font-weight="700" font-family="Inter">CUT &amp; CLINCH</text>
  <!-- PCB -->
  <rect x="60" y="175" width="200" height="14" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="80" y="178" width="160" height="8" fill="#0E5A26"/>
  <line x1="100" y1="178" x2="100" y2="186" stroke="#FF6B1A" stroke-width="0.5"/>
  <line x1="130" y1="178" x2="130" y2="186" stroke="#FF6B1A" stroke-width="0.5"/>
  <line x1="160" y1="178" x2="160" y2="186" stroke="#FF6B1A" stroke-width="0.5"/>
  <line x1="190" y1="178" x2="190" y2="186" stroke="#FF6B1A" stroke-width="0.5"/>
  <line x1="220" y1="178" x2="220" y2="186" stroke="#FF6B1A" stroke-width="0.5"/>
  <text x="160" y="206" text-anchor="middle" font-size="7" fill="#FF6B1A" font-weight="700" font-family="Inter">AXIAL INSERTION · 22,000 CPH</text>
</svg>
```

**Key visual cues:**
- 6 vertical tape feeder columns (axial components hang vertically)
- One column highlighted in orange = the "live" station
- Cut-and-clinch head at the top (axial components need leads cut and bent)
- Vertical orange lines on the PCB = axial component leads going through the holes

---

## S-7020 — Pin / Eyelet / Terminal Inserter

**Use for connectors, terminal blocks, eyelets, grounding pins.**

Visual: more mechanical, focuses on the insertion force / pressing action.

```html
<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" class="machine-svg">
  <ellipse cx="160" cy="200" rx="130" ry="6" fill="rgba(0,0,0,0.25)"/>
  <rect x="40" y="60" width="240" height="130" rx="6" fill="#F4F1EC" stroke="#A8B0BB" stroke-width="1.2"/>
  <rect x="48" y="50" width="100" height="22" rx="2" fill="#1A3A5C" stroke="#0E2A47"/>
  <text x="98" y="63" text-anchor="middle" font-size="6" fill="#FF6B1A" font-weight="700" font-family="Inter">PIN / TERMINAL</text>
  <!-- Tray feeder (terminal strips) -->
  <rect x="55" y="100" width="80" height="40" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <rect x="60" y="105" width="70" height="6" fill="#0E2A47" opacity="0.6"/>
  <rect x="60" y="113" width="70" height="6" fill="#0E2A47" opacity="0.5"/>
  <rect x="60" y="121" width="70" height="6" fill="#0E2A47" opacity="0.4"/>
  <rect x="60" y="129" width="70" height="6" fill="#0E2A47" opacity="0.3"/>
  <text x="95" y="153" text-anchor="middle" font-size="6.5" fill="#0E2A47" font-weight="700" font-family="Inter">TRAY / STRIP FEEDER</text>
  <!-- Pressing head with force sensor -->
  <rect x="200" y="65" width="50" height="20" fill="#FF6B1A" stroke="#0E2A47" stroke-width="0.8"/>
  <text x="225" y="78" text-anchor="middle" font-size="5.5" fill="#fff" font-weight="700" font-family="Inter">FORCE SENSE</text>
  <line x1="225" y1="85" x2="225" y2="115" stroke="#1A1A1A" stroke-width="3"/>
  <rect x="220" y="115" width="10" height="8" fill="#5A6573"/>
  <text x="290" y="100" font-size="5.5" fill="#FF6B1A" font-weight="700" font-family="Inter">±0.05mm</text>
  <!-- PCB -->
  <rect x="60" y="175" width="200" height="14" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="80" y="178" width="160" height="8" fill="#0E5A26"/>
  <rect x="140" y="180" width="6" height="4" fill="#FF6B1A"/>
  <rect x="170" y="180" width="6" height="4" fill="#FF6B1A"/>
  <rect x="200" y="180" width="6" height="4" fill="#FF6B1A"/>
  <text x="160" y="206" text-anchor="middle" font-size="7" fill="#FF6B1A" font-weight="700" font-family="Inter">PIN / TERMINAL INSERTION</text>
</svg>
```

**Key visual cues:**
- Tray feeder on the left (terminal strips / pin trays)
- Pressing head with "FORCE SENSE" label on the right
- Vertical press rod
- Small orange rectangles on the PCB = inserted pins/terminals

---

## S-WS450 — Wave Soldering Machine

**Use for full-line ROI one-pagers that emphasize the complete THT workflow.**

```html
<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" class="machine-svg">
  <ellipse cx="160" cy="200" rx="130" ry="6" fill="rgba(0,0,0,0.25)"/>
  <rect x="20" y="60" width="280" height="130" rx="6" fill="#F4F1EC" stroke="#A8B0BB" stroke-width="1.2"/>
  <rect x="28" y="50" width="100" height="22" rx="2" fill="#1A3A5C" stroke="#0E2A47"/>
  <text x="78" y="63" text-anchor="middle" font-size="6" fill="#FF6B1A" font-weight="700" font-family="Inter">WAVE SOLDER</text>
  <!-- Pre-heat zone -->
  <rect x="35" y="90" width="55" height="50" rx="2" fill="#FF6B1A" opacity="0.15" stroke="#FF6B1A" stroke-width="0.5" stroke-dasharray="2 2"/>
  <text x="62" y="115" text-anchor="middle" font-size="6" fill="#FF6B1A" font-weight="700" font-family="Inter">PRE-HEAT</text>
  <!-- Flux zone -->
  <rect x="95" y="90" width="40" height="50" rx="2" fill="#1A3A5C" opacity="0.15" stroke="#1A3A5C" stroke-width="0.5" stroke-dasharray="2 2"/>
  <text x="115" y="115" text-anchor="middle" font-size="6" fill="#1A3A5C" font-weight="700" font-family="Inter">FLUX</text>
  <!-- Solder wave (the money shot) -->
  <rect x="140" y="90" width="80" height="50" rx="2" fill="#FF6B1A"/>
  <path d="M 145 130 Q 162 122 180 130 Q 198 138 215 130" fill="none" stroke="#fff" stroke-width="2"/>
  <path d="M 145 138 Q 162 130 180 138 Q 198 146 215 138" fill="none" stroke="#FFE0CC" stroke-width="1"/>
  <text x="180" y="110" text-anchor="middle" font-size="6" fill="#fff" font-weight="700" font-family="Inter">SOLDER WAVE</text>
  <text x="180" y="155" text-anchor="middle" font-size="5.5" fill="#FF6B1A" font-weight="700" font-family="Inter">~250°C</text>
  <!-- Cooling zone -->
  <rect x="225" y="90" width="60" height="50" rx="2" fill="#1A3A5C" opacity="0.15" stroke="#1A3A5C" stroke-width="0.5" stroke-dasharray="2 2"/>
  <text x="255" y="115" text-anchor="middle" font-size="6" fill="#1A3A5C" font-weight="700" font-family="Inter">COOLING</text>
  <!-- Conveyor with PCB going through -->
  <line x1="20" y1="165" x2="300" y2="165" stroke="#5A6573" stroke-width="1"/>
  <rect x="160" y="158" width="40" height="6" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <text x="160" y="180" text-anchor="middle" font-size="6" fill="#0E2A47" font-weight="700" font-family="Inter">PCB IN PROCESS</text>
  <text x="160" y="206" text-anchor="middle" font-size="7" fill="#FF6B1A" font-weight="700" font-family="Inter">WAVE SOLDERING · NO-LEAD COMPATIBLE</text>
</svg>
```

**Key visual cues:**
- 4 distinct process zones: pre-heat, flux, solder wave (orange), cooling
- The wave itself rendered as a sine curve
- PCB traveling left-to-right on the conveyor
- Temperature callout "~250°C"

---

## SUL460 — Automatic Unloader (Magazine / Buffer)

**Use for full-line completion one-pagers.**

```html
<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" class="machine-svg">
  <ellipse cx="160" cy="200" rx="130" ry="6" fill="rgba(0,0,0,0.25)"/>
  <rect x="40" y="60" width="240" height="130" rx="6" fill="#F4F1EC" stroke="#A8B0BB" stroke-width="1.2"/>
  <rect x="48" y="50" width="100" height="22" rx="2" fill="#1A3A5C" stroke="#0E2A47"/>
  <text x="98" y="63" text-anchor="middle" font-size="6" fill="#FF6B1A" font-weight="700" font-family="Inter">UNLOADER</text>
  <!-- Lifting mechanism -->
  <rect x="50" y="80" width="20" height="80" rx="2" fill="#1A3A5C" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="55" y="85" width="10" height="70" fill="#FF6B1A" opacity="0.8"/>
  <!-- PCB magazine (stacked PCBs going up) -->
  <rect x="80" y="95" width="100" height="6" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="80" y="105" width="100" height="6" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="80" y="115" width="100" height="6" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="80" y="125" width="100" height="6" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <rect x="80" y="135" width="100" height="6" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <text x="130" y="156" text-anchor="middle" font-size="6.5" fill="#0E2A47" font-weight="700" font-family="Inter">PCB MAGAZINE STACK</text>
  <!-- Robotic arm picking PCB -->
  <rect x="200" y="80" width="14" height="14" fill="#FF6B1A"/>
  <line x1="207" y1="94" x2="207" y2="110" stroke="#1A1A1A" stroke-width="3"/>
  <rect x="200" y="110" width="14" height="8" fill="#5A6573"/>
  <text x="207" y="125" text-anchor="middle" font-size="5.5" fill="#FF6B1A" font-weight="700" font-family="Inter">PICK &amp; PLACE</text>
  <!-- Out-feed conveyor -->
  <line x1="230" y1="135" x2="290" y2="135" stroke="#5A6573" stroke-width="1.5"/>
  <rect x="265" y="131" width="20" height="8" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <text x="160" y="206" text-anchor="middle" font-size="7" fill="#FF6B1A" font-weight="700" font-family="Inter">AUTOMATIC UNLOADER · 8s CYCLE</text>
</svg>
```

**Key visual cues:**
- Vertical lifting mechanism on the left (the unloader lifts PCBs out of the line)
- Stacked magazine in the middle (PCBs accumulate here, going up)
- Robotic pick-and-place arm on the right moving PCBs to out-feed
- ~8s cycle time callout

---

## How to Customize the Schematic for Your Vertical

The SVGs above are designed to be **drop-in templates**. To customize for a specific vertical:

1. **Change the highlighted component.** In the S-70LD SVG, the vibratory bowl is the "money shot" for odd-form. In S-3000/S-4000, the tape feeder rail is. Pick the one that matches the customer's pain.

2. **Change the orange callout label.** "±0.5mm HEAD" for odd-form. "18,000 CPH" for radial. "~250°C" for wave. Pick the spec the customer cares about.

3. **Change the PCB dot density.** Dense dots = high component count (radial caps, IoT modules). Sparse dots = low component count (high-power, low-density).

4. **Add a vertical-specific arrow or annotation** if needed (e.g., an arrow pointing to the wave zone with "0% Pb" for EU compliance).

5. **Don't add too many labels** — the schematic is meant to be glanceable in 3 seconds. 2-3 labels max.

The PDFs render these SVGs perfectly in Chrome's print engine. No rasterization, no font issues, no missing assets.
