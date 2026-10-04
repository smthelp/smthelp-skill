# ROI Content Patterns by Industry Vertical

This file is the **content drop-in for the base template** (`templates/roi-one-pager-base.html`). When building a new one-pager for a different machine × vertical × region, copy the matching section below, fill the placeholders, render. Each section includes the hero sub, challenge bullets, ROI table, KPI numbers, and line flow for one validated scenario.

The labor rates in the ROI tables reflect the **fully-loaded operator cost** (wages + benefits + management overhead, x 2080 hours x shifts). Always state the source as an assumption in the footer.

The currency follows the region. Use ISO codes + symbol (€, $, R$).

---

## Vertical 1: White-Goods Controllers (Washing / Dishwasher / Oven)

**Validated scenario:** E.G.O. Appliance Controls S.L.U., Lliçà de Vall, Barcelona, Spain (2026-06-05). Machine: S-70LD.

### Hero

- `MACHINE_TITLE`: "S-70LD Dual-Head"
- `MACHINE_TAGLINE`: "Odd-Form Inserter"
- `EYEBROW`: "2026 ROI Brief · White-Goods Controllers"
- `HERO_SUB`: "Replace 6&ndash;8 manual odd-form insertion operators on your <b>inverter / main control / IoT controller PCBA</b> line. Engineered in Shenzhen since 2011, 50% CapEx saving vs Japanese equivalents, <b>4&ndash;8 week delivery</b>, <b>24&ndash;48h</b> global service response."
- `PILL_1` (orange): "For Spain · EU White-Goods EMS"
- `PILL_2`: "2 Shifts · ~100k PCBA / month"
- `PILL_3`: "IPC-A-610 Class 2 / 3"
- `PILL_4`: "MES Ready"

### Challenge bullets

- "<b>Manual odd-form bottleneck.</b> Transformers, large E-CAPs, terminal blocks, relays &amp; IGBT modules still inserted by hand on most 2015&ndash;2020 era THT lines."
- "<b>EU labor cost squeeze.</b> Catalonia fully-loaded operator cost &asymp; &euro;28&ndash;32 / hour, pushing manual odd-form stations to &euro;45&ndash;55k / year each."
- "<b>ESPR &amp; Right-to-Repair</b> force higher-mix, lower-volume production, where hand insertion ramp-up eats margin."
- "<b>Yield &amp; traceability</b> gaps from manual stations &mdash; a single missed insertion triggers credit-note / rework penalties under strict PO terms."
- "<b>UIC-era Feeder</b> base is still solid (good!) &mdash; you don't need a rip-and-replace, you need a smart <b>add-on</b>."

### ROI table

```
ROI_CONTEXT: 2-Shift White-Goods Controller Line (Spain)
TODAY_LABEL: Manual
MACHINE_SHORT: S-70LD

Row 1: "Odd-form operators per shift"  | "4&ndash;5" | "1 + 1 feeder" | "6&ndash;8 staff" (bold)
Row 2: "Fully-loaded operator cost / yr" | "&euro;50,000" | "&euro;55,000" | "&minus;&euro;55k"
Row 3: "Annual direct labor (2 shifts)" | "&euro;800k&ndash;1.0M" | "&euro;110k&ndash;165k" | "&minus;&euro;690k" (bold)
Row 4: "First-pass yield (odd-form)" | "96.5 %" | "99.2 %" | "+2.7 pp"
Row 5: "Credit-note / rework cost" | "&euro;180k / yr" | "&euro;55k / yr" | "&minus;&euro;125k"
Row 6 (highlight): "5-Year Net Savings" | "&mdash;" | "&mdash;" | "&euro;3.8M&ndash;4.5M" (bold)
```

### KPI numbers

- `PAYBACK_VALUE`: "3&ndash;4"
- `PAYBACK_UNIT`: "months"
- `PAYBACK_NOTE`: "On a single S-70LD dual-head cell vs manual station labor in Catalonia"
- `SAVINGS_VALUE`: "&euro;3.8&ndash;4.5"
- `SAVINGS_UNIT`: "M"
- `SAVINGS_NOTE`: "After S-70LD CapEx, training, integration &amp; service"
- `CAPEX_DELTA`: "&minus;50"
- `CAPEX_NOTE`: "vs Yamaha YS24 / Fuji NXT odd-form head benchmark"

### Footer assumptions

"ROI assumptions: 2 shifts, fully-loaded operator cost &euro;28&ndash;32/h, output ~100k PCBA / month. Your actual payback will be confirmed in the line health check."

---

## Vertical 2: Automotive Electronics (BMS, ECU, IGBT Inverter)

**Validated scenario:** Not yet field-tested — use the structure below as the template.

### Hero

- `MACHINE_TITLE`: "S-7900 High-Precision" (or S-70LD for cost-sensitive Tier-2)
- `MACHINE_TAGLINE`: "Odd-Form Inserter"
- `HERO_SUB`: "Solve the odd-form insertion bottleneck on <b>BMS, ECU, IGBT inverter modules</b> for EV / Tier-1 automotive. Active clinching, insertion force control, ±0.05mm precision, 100% traceability to meet IATF 16949 audits."
- `PILL_1`: "For EU Tier-1 / OEM Auto-Electronics"
- `PILL_2`: "IATF 16949 / PPAP Ready"
- `PILL_3`: "3 Shifts · 50-200k PCBA / month"
- `PILL_4`: "Insertion Force Data Logging"

### Challenge bullets (car variants)

- "<b>IGBT / connector insertion</b> requires controlled force to prevent substrate cracking — manual stations cannot guarantee this and create scrap risk."
- "<b>Audit-trail gap.</b> IATF 16949 requires full traceability of insertion force per component. Manual stations log nothing."
- "<b>Automotive labor cost &euro;35-45/h</b> in Germany / €18-22 in Eastern Europe, 3 shifts on a Tier-1 line = manual odd-form station at &euro;220-330k/year."
- "<b>PPAP revalidation pain.</b> Every new connector requires 5-8 weeks of manual setup. Automated S-7900 with vision cuts this to days."
- "<b>End-of-line test failures</b> trace back to insertion defects — credit note exposure on a 50k-€/yr BMS line is &euro;100-200k/yr."

### ROI table (rough structure — adjust for actual line)

```
Row 1: "Odd-form operators per shift" | "5-6" | "1 + 1 supervisor" | "8-12 staff"
Row 2: "Loaded operator cost / yr" | "€55,000-65,000" | "€70,000" | "-€550k"
Row 3: "Annual direct labor (3 shifts)" | "€1.5-2.0M" | "€210-280k" | "-€1.4M" (bold)
Row 4: "PPAP revalidation time" | "5-8 weeks" | "1-2 weeks" | "Faster time-to-market"
Row 5: "Insertion-defect credit notes" | "€180k/yr" | "€30k/yr" | "-€150k"
Row 6 (highlight): "5-Year Net Savings" | "—" | "—" | "€6-9M"
```

### KPI numbers

- `PAYBACK_VALUE`: "4&ndash;6"
- `PAYBACK_UNIT`: "months"
- `SAVINGS_VALUE`: "&euro;6&ndash;9"
- `SAVINGS_UNIT`: "M"
- `CAPEX_DELTA`: "&minus;45"

### Footer assumptions

"ROI assumptions: 3 shifts, fully-loaded operator cost &euro;35-45/h (DE) or &euro;18-22/h (PL/CZ), output 50-200k PCBA / month. IATF 16949 audit-trail value not included in € figure."

---

## Vertical 3: Power Supplies / EV Chargers

**Validated scenario:** Use the structure below.

### Hero

- `MACHINE_TITLE`: "S-3000 High-Speed" (or S-4000 for axial-heavy PSUs)
- `MACHINE_TAGLINE`: "Radial Inserter"
- `HERO_SUB`: "Replace 40+ manual radial insertion operators on your <b>EV charger / industrial PSU / telecom power supply</b> line. 18,000 CPH throughput, ±0.001mm precision, 3-4 week delivery, 24-48h service."
- `PILL_1`: "For PSU / EV Charger / Telecom OEM"
- `PILL_2`: "1-3 Shifts · 30-500k PCBA / month"
- `PILL_3`: "IPC-A-610 Class 2"
- `PILL_4`: "Feeder Base Compatible with Panasonic CM602 / NPM / Fuji NXT"

### Challenge bullets

- "<b>Radial cap / diode / small relay</b> insertion on PSU lines is the highest-volume THT task — 20-40 components per board, 30-500k boards per month."
- "<b>Manual radial stations</b> at 800-1,200 components / hour / operator — even with 20 operators you're capped at 24k components / hour / shift."
- "<b>PSU labor cost</b> in Mexico $5-7/h, Vietnam $3-4/h, India $2-3/h. 20 operators × 2 shifts = annual cost $150-280k."
- "<b>Panasonic CM era Feeder</b> base still works (good!) — Southern Machinery provides drop-in compatible Feeder at 50% OEM list."
- "<b>Yield drag</b> on manual radial insertion: 1.5-3% miss rate × 30 components = near-certain defect per board."

### ROI table

```
Row 1: "Radial operators per shift" | "8-12" | "1 + 2 feeders" | "20-30 staff" (bold)
Row 2: "Loaded operator cost / yr" | "$8,000-18,000" | "$10,000-20,000" | "Region-dependent"
Row 3: "Annual direct labor (2 shifts)" | "$250-500k" | "$40-80k" | "-$200-420k" (bold)
Row 4: "First-pass yield (radial)" | "97.0%" | "99.5%" | "+2.5 pp"
Row 5: "Rejection / rework cost" | "$80-150k/yr" | "$20-40k/yr" | "-$60-110k"
Row 6 (highlight): "5-Year Net Savings" | "—" | "—" | "$1.2-2.8M"
```

### KPI numbers

- `PAYBACK_VALUE`: "4&ndash;8"
- `PAYBACK_UNIT`: "months"
- `SAVINGS_VALUE`: "$1.2&ndash;2.8"
- `SAVINGS_UNIT`: "M"
- `CAPEX_DELTA`: "&minus;50"

---

## Vertical 4: LED Drivers / Lighting

**Validated scenario:** Not yet field-tested. Use as starting template.

### Hero

- `MACHINE_TITLE`: "S-3000 High-Speed"
- `MACHINE_TAGLINE`: "Radial LED-Driver Inserter"
- `PILL_1`: "For LED Driver / Luminaire OEM"
- `PILL_2`: "1-2 Shifts · 50-200k PCBA / month"
- `PILL_3`: "High-Mix / Frequent Changeover"
- `PILL_4`: "30-min New-Board Setup"

### Challenge bullets

- "<b>LED driver lines are high-mix / low-volume</b> — 5-15 SKUs per shift, frequent changeover erodes OEE on any dedicated machine."
- "<b>Radial cap + bridge rectifier + MOV</b> insertion dominates; manual stations handle it but at the cost of changeover time."
- "<b>Seasonal demand spikes</b> (Q4 holiday, summer construction) make flexible capacity critical. Manual scales linearly with labor; automation gives instant flex."
- "<b>MCPCB and FR4 hybrid boards</b> require different handling — verify your inserter supports both."
- "<b>Energy efficiency / EU SLR</b> on luminaires drives demand for high-frequency drivers with more THT components."

### ROI table

```
Row 1: "Radial operators per shift" | "4-6" | "1 + 1 feeder" | "6-10 staff" (bold)
Row 2: "Loaded operator cost / yr" | "$8,000-15,000" | "$10,000-18,000" | "Region-dependent"
Row 3: "Annual direct labor (2 shifts)" | "$120-220k" | "$40-72k" | "-$80-150k" (bold)
Row 4: "Changeover time (new SKU)" | "30-60 min" | "5-10 min" | "Faster, less scrap"
Row 5: "First-pass yield" | "96.0%" | "99.3%" | "+3.3 pp"
Row 6 (highlight): "5-Year Net Savings" | "—" | "—" | "$0.6-1.2M"
```

### KPI numbers

- `PAYBACK_VALUE`: "5&ndash;8"
- `PAYBACK_UNIT`: "months"
- `SAVINGS_VALUE`: "$0.6&ndash;1.2"
- `SAVINGS_UNIT`: "M"
- `CAPEX_DELTA`: "&minus;50"

---

## Vertical 5: IoT / Connectivity Modules

**Validated scenario:** Not yet field-tested. Use as starting template.

### Hero

- `MACHINE_TITLE`: "S-70LD Compact"
- `MACHINE_TAGLINE`: "Odd-Form Inserter for IoT Modules"
- `PILL_1`: "For IoT Module / Wearable / Smart Home OEM"
- `PILL_2`: "High-Mix · 1-2 Shifts"
- `PILL_3`: "Small Batch / 100-1,000 PCBA per SKU"
- `PILL_4`: "30-min New-Board Setup"

### Challenge bullets

- "<b>Small batch / high-mix</b> is the IoT norm — 20-50 SKUs per month, 100-1,000 boards each. Manual stations absorb this; dedicated automation is too rigid."
- "<b>WiFi / BLE / LoRa module sockets, SIM holders, antenna connectors</b> are all odd-form and change every product gen."
- "<b>Skilled operator shortage</b> in tech hubs (Shenzhen, Hsinchu, Austin, Eindhoven) drives labor cost up 8-12%/year."
- "<b>Time-to-market pressure</b> on every new product — manual setup eats 1-2 weeks; S-70LD with vision-guided changeover is <1 day."
- "<b>Traceability for FCC / CE certification</b> requires logging every insertion; manual stations cannot."

### ROI table

```
Row 1: "Odd-form operators per shift" | "3-5" | "1 + 1 feeder" | "4-8 staff" (bold)
Row 2: "Loaded operator cost / yr" | "$15,000-30,000" | "$18,000-35,000" | "Region-dependent"
Row 3: "Annual direct labor (2 shifts)" | "$90-180k" | "$36-70k" | "-$54-110k" (bold)
Row 4: "Time-to-market on new SKU" | "1-2 weeks" | "1-2 days" | "Revenue acceleration"
Row 5: "First-pass yield" | "95.5%" | "99.0%" | "+3.5 pp"
Row 6 (highlight): "5-Year Net Savings" | "—" | "—" | "$0.4-0.9M"
```

### KPI numbers

- `PAYBACK_VALUE`: "6&ndash;10"
- `PAYBACK_UNIT`: "months"
- `SAVINGS_VALUE`: "$0.4&ndash;0.9"
- `SAVINGS_UNIT`: "M"
- `CAPEX_DELTA`: "&minus;50"

---

## Vertical 6: Telecom Infrastructure (Base Station PSUs)

**Validated scenario:** Not yet field-tested. Use as starting template.

### Hero

- `MACHINE_TITLE`: "S-4000 Heavy-Duty"
- `MACHINE_TAGLINE`: "Axial Inserter for Base Station PSUs"
- `PILL_1`: "For Telecom OEM / Base Station PSU"
- `PILL_2`: "1-2 Shifts · 10-50k PCBA / month"
- `PILL_3`: "IPC-A-610 Class 3 / High-Reliability"
- `PILL_4`: "Full Traceability + 100% AOI"

### Challenge bullets

- "<b>Base station PSUs</b> are high-reliability, low-volume, high-margin. 1 bad board per 10k = 100k€+ warranty exposure."
- "<b>Axial diodes, large inductors, transformers</b> dominate the BOM. S-4000 inserts up to 22,000 CPH, ±0.001mm."
- "<b>Manual insertion of axial</b> is one of the highest-injury tasks in THT (repetitive wrist motion). OSHA / EU-OSHA exposure is real."
- "<b>5G rollout</b> in EU + APAC is driving capex into base station PSU lines 2025-2027."
- "<b>Telecom buyer consolidation</b> (Ericsson, Nokia, Huawei, Samsung) means supplier audits are brutal — automated traceability is the price of admission."

### ROI table

```
Row 1: "Axial operators per shift" | "6-10" | "1 + 2 feeders" | "12-18 staff" (bold)
Row 2: "Loaded operator cost / yr" | "$25,000-40,000" | "$28,000-45,000" | "Region-dependent"
Row 3: "Annual direct labor (2 shifts)" | "$400-800k" | "$56-90k" | "-$340-710k" (bold)
Row 4: "Warranty exposure on field defect" | "$200-400k/yr" | "$20-50k/yr" | "-$180-350k"
Row 5: "First-pass yield" | "97.5%" | "99.6%" | "+2.1 pp"
Row 6 (highlight): "5-Year Net Savings" | "—" | "—" | "$2.5-5.0M"
```

### KPI numbers

- `PAYBACK_VALUE`: "4&ndash;6"
- `PAYBACK_UNIT`: "months"
- `SAVINGS_VALUE`: "$2.5&ndash;5.0"
- `SAVINGS_UNIT`: "M"
- `CAPEX_DELTA`: "&minus;45"

---

## Labor Cost Quick Reference (2026-06-05)

Always use **fully-loaded** rates (wages + benefits + management overhead, x 2080 hours). This is the table to quote in the footer of every one-pager when you've made a labor-cost assumption.

| Region | Loaded Rate | Notes |
|--------|-------------|-------|
| Spain (Catalonia) | €28-32 / hour | 2025-2026 manufacturing |
| Germany (Bavaria, BW) | €32-38 / hour | Southern DE higher |
| France | €25-30 / hour | |
| Italy (north) | €22-28 / hour | |
| Poland | €12-15 / hour | Skilled THT operator |
| Czechia | €11-14 / hour | |
| Hungary | €10-13 / hour | |
| Romania | €8-11 / hour | |
| Vietnam (HCMC, Hanoi) | $3-4 / hour | Skilled in ZES/Hi-Tech zones |
| Thailand (EEC) | $3.5-4.5 / hour | |
| Indonesia (Jakarta) | $2.5-3.5 / hour | |
| Mexico (Monterrey, BJ) | $5-7 / hour | IMMEX zone, near-shoring premium |
| Brazil (Manaus ZFM) | R$25-35 / hour | ZFM tax-incentivized |
| India (Tamil Nadu, KA) | $2-3 / hour | Skilled in Chennai / Bangalore belt |
| USA (Texas, AZ) | $22-28 / hour | |
| Canada (Ontario) | $24-30 / hour | |

Annual cost = rate × 2080 hours. 2 shifts = 2x. 3 shifts = 3x.
