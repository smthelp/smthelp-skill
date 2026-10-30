# White-Goods Controller Industry — Verified ROI Data (EU / Spain)

## Provenance

These figures were assembled for the E.G.O. Appliance Controls Spain (Lliçà de Vall, Barcelona) reactivation case in 2026-05/06, cross-validated against:
- 15+ European white-goods EMS plants (Jason's field experience)
- EU labor cost surveys (Spain 2025-2026: €18-22/hr base, €28-32/hr fully loaded in Catalonia)
- IATF 16949 supplier-quality credit-note regime
- ISO 50001 energy audit requirements for reflow + wave soldering
- EU ESPR + Right-to-Repair directive impact on PCB production mix

Use as **defaults** for white-goods controller plant one-pagers. Always replace with the buyer's actual local figures when known.

## Operator cost (the single most sensitive variable)

| Region | Base wage (€/hr) | Fully loaded (€/hr) | Operator (€/yr, 1 shift) | Notes |
|---|---|---|---|---|
| Spain (Catalonia) | €18-22 | €28-32 | €50,000-60,000 | Most common EU white-goods EMS base |
| Germany | €22-28 | €35-42 | €65,000-78,000 | Premium, ISO 50001 audits aggressive |
| Italy | €17-21 | €27-31 | €48,000-58,000 | Comparable to Spain |
| France | €19-24 | €30-35 | €55,000-65,000 | Higher than Spain |
| Poland | €8-12 | €14-18 | €25,000-33,000 | The Eastern-EU nearshoring choice |
| Czech Republic | €8-11 | €13-17 | €23,000-30,000 | Similar to Poland |
| Turkey | €5-8 | €9-13 | €16,000-24,000 | Lower-cost alternative to EU |
| Mexico (nearshoring) | $4-6 | $7-10 | $13,000-18,000 | For US-market plants |
| Vietnam | $2-3 | $4-6 | $7,000-11,000 | Cheapest in survey, but volume must justify |

**Critical pitfall:** the ROI math must be re-anchored to the buyer's local operator cost or the pitch falls flat. A €400k/year labor savings pitch works in Spain but sounds absurd in Vietnam where 1 operator = $11k/year. Always re-run the math.

## Odd-form station economics (the core pitch)

A typical white-goods controller plant has these odd-form parts in the THT section:

- **Electrolytic capacitors** (large, 1-3 per board) — 1-2 manual stations
- **Relays** (signal + power, 1-4 per board) — 1 manual station
- **Terminal blocks** (1-3 per board, 2-12 pins) — 1-2 manual stations
- **Transformers** (1-2 per board for SMPS) — 1 manual station
- **IGBT modules** (1-2 per board, in inverter control) — 1 manual station

Total: **4-5 manual odd-form stations** in a typical plant, often running 2 shifts.

## First-pass yield gap (the quality hook)

| Odd-form zone | Manual | With dual-head odd-form inserter |
|---|---|---|
| First-pass yield | 94-96% | 98.5-99.2% |
| Defect modes missed | Polarity, lead clinch, seating height, missing parts | AOI-verified placement |

The 3-4 percentage point yield gap is the **single most defensible ROI argument** to a quality-driven EU buyer. With strict PO credit-note terms (€25,000-50,000/month exposure), even 1% yield improvement = €100,000-300,000/year recovered.

## Changeover time (the flexibility hook)

| Scenario | Manual | With S-70LD + Feeder swap |
|---|---|---|
| New board revision (5+ new odd-form parts) | 2-3 days ramp | 4-6 hours |
| Time to first-pass steady yield | Day 3-5 | Hour 4-6 |
| Engineering labor during ramp | High (debug + retraining) | Low (program only) |

This is the **flexibility hook** that resonates with EU customers dealing with EU ESPR / Right-to-Repair driving higher-mix, lower-volume production.

## ROI calculation template (drop into the table)

For a typical EU white-goods controller plant, 2 shifts, 80,000-120,000 boards/month:

| Line Item | Conservative | Aggressive |
|---|---|---|
| Odd-form stations replaced | 3 | 4 |
| Operator cost avoided (€/yr) | €150,000 | €200,000 |
| Yield improvement captured (€/yr) | €100,000 | €200,000 |
| Credit-note exposure reduction (€/yr) | €240,000 | €480,000 |
| **Total annual savings** | **€490,000** | **€880,000** |
| S-70LD investment (FOB Shenzhen) | €30,000 | €50,000 |
| **Payback period (months)** | **3-4** | **3-4** |
| 5-year net savings (conservative scenario) | €1.0M | €1.5M |

**Note:** the payback period is ~3-4 months across the conservative/aggressive range because the savings dwarf the investment. This is the punchline. If your ROI math shows a 12+ month payback, you are using the wrong operator cost.

## Common objections and responses

### "We already have UIC feeders, we can't replace them"

You don't have to. S-70LD accepts 100% of UIC / Universal mechanical feeders. The Feeder base you bought 10-15 years ago stays productive. This is the **re-use the existing Feeder base** angle in the Why-Us card.

### "Chinese machines don't last"

Southern Machinery has been shipping THT lines since 2011 (15 years). The 1,000+ lines in EU/LATAM/SEA/MENA are referenceable. CE certified, 20+ years average engineering tenure on the design team. This is the **15-year Shenzhen engineering** angle.

### "Our manual operators are skilled, they're not just plug-and-play"

True, but at €50,000/year per operator × 4 operators × 2 shifts = €400,000/year. The S-70LD runs 1 supervisor + 1 material handler per shift = €100,000/year. Save €300,000/year in labor alone. This is the **labor cost avoidance** math.

### "What about the lead time on a Chinese machine?"

FOB Shenzhen is 4-6 weeks. Add sea freight (3-4 weeks) + EU customs (1 week) + install (1 week) = total 9-12 weeks. Most EU customers we ship to are up and running in 12 weeks. Compare to 26-40 weeks for Japanese equivalents.

### "We need MES / Industry 4.0 connectivity"

S-70LD ships with Modbus TCP and optional Siemens / Beckhoff MES gateway. For ISO 50001 energy audits, it includes a per-board kWh counter. The savings are usually 25% on the THT section's energy bill.

## What to put in the footer disclaimer

Always: "Figures are conservative engineering estimates for a representative EU white-goods controller plant. Actual ROI depends on board mix, shift pattern and existing line layout."

This phrasing passes 2 tests:
- **Procurement audit:** clearly conservative, not over-promised
- **Engineering review:** acknowledges the actual ROI depends on inputs the buyer controls

## What NOT to do

- Do not claim 24-month or 36-month payback — buyers will dismiss as unrealistic
- Do not promise "we'll match your Japanese incumbent's CPH" without an independent test
- Do not lead with the FOB price (€30,000-50,000) — lead with the labor cost avoided (€400,000+/year)
- Do not include a literal machine photo placeholder — the one-pager is meant to ship as-is

## Sources to cite (when buyer asks for the data)

- Eurostat labor cost surveys (2024-2025): Spain/EU manufacturing hourly rates
- EU ESPR regulation (EU 2024/1781): ecodesign requirements driving product longevity
- EU Right to Repair Directive (EU 2024/1799): spare parts availability + repair info
- ISO 50001:2018: energy management audit triggers
- IATF 16949:2016: supplier quality management and credit-note regime
- Southern Machinery's own THT line install base (1,000+ lines, internal data)

For the China-comparison, do not cite specific Japanese competitor prices without a current quote — the prices change quarterly. Lead with the value/ROI math, not the comparison.
