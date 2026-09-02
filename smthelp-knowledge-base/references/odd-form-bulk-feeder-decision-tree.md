# Bulk Odd-Form Feeder Case Reference — KEMX RHEEM0527 (2026-06-04)

> **Purpose**: Real case study showing how to handle a "we have bulk X, automate it" inquiry from a Tier-1 EMS. Use as a template for similar RFQs.

---

## 1. Case Snapshot

| Field | Value |
|-------|-------|
| Customer | **Kimball Electronics Mexico (KEMX)** — Tier-1 EMS, automotive/industrial/medical, Reynosa + Juarez plants |
| Inquiry date | 2026-06-04 |
| Part | **RHEEM0527 cube-shaped screw terminal block** (top: Phillips clamping screw, bottom: PCB mounting tab) |
| Application | Rheem HVAC control board (high-voltage, safety-relevant) |
| Qty per board | 2 pcs |
| Packaging | Bulk (loose parts) — NOT tape/tube/tray |
| Trigger phrase | "墨西哥客户Kimball Electronics Mexico (KEMX) 需求定制Feeder处理散装的螺丝组件" |

## 2. Part Analysis Heuristics (Cube + Top Screw)

When the part is **cube-shaped with a top protrusion**:

1. **Cannot use standard vacuum nozzle** — top is occupied by the screw shaft → need custom Gripper Nozzle that grabs the side faces
2. **Polarity / orientation is mandatory** — must verify screw faces UP and terminal hole faces the right direction (vision required)
3. **THT vs SMT** — if a PCB mounting tab is present at the bottom, this is a THT insertion task (tab goes through hole) → consider S-70LD / S-7900 with Active Clinching
4. **Wave soldering concern** — the clamping screw on top MUST remain functional after soldering (no solder wicking into threads) → pre-solder mask or selective solder

## 3. Recommended Path (drop-in for existing P&P)

**Primary: BF-2002D double-deck vibratory bowl feeder + custom gripper nozzle + customer's existing P&P.**

Why this and not alternatives:
- BF-2002D catalog explicitly lists "terminals, hardware parts" → exact match
- Compatible with all major mounters KEMX might run (Panasonic/Juki/Fuji/ASM)
- Drop-in → minimum line disruption
- Fastest payback (12–18 months typical)

Alternative: SBF1001 single bowl if space is not constrained or if KEMX has an existing SBF platform.

## 4. High-Reliability Path (safety-critical boards)

**SBF1001 + S-70LD odd-form inserter with Active Clinching** — for HVAC safety circuits, IPC-A-610 Class 3, or vibration/thermal-cycling environments. Active Clinching adds a mechanical lead-form backup to the wave solder fillet.

## 5. The 8 Must-Ask Questions (use verbatim in your proposal)

1. **Part dimensional drawing** (2D or STEP) — without this we cannot finalize bowl tooling or nozzle design
2. **50–100 sample parts** for bowl tuning and nozzle prototyping
3. **Existing P&P make/model** at the target line
4. **Target monthly/annual volume**
5. **Current placement method** (manual / semi-auto) + current first-pass yield
6. **Shift pattern + operator headcount** currently on this station
7. **Wave soldering line details** (lead-free / leaded, single / dual wave, flux type)
8. **Target delivery date + site support** (Reynosa vs Juarez)

## 6. ROI Snapshot (Mexico-specific, ~2026)

Mexico operator fully-loaded cost: **$5,000–$6,000/year** (wages + benefits + supervision).

Manual hand-placement of through-hole terminals: **~8–12 seconds per board for 2 terminals** (typical).

Direct labor savings with BF-2002D:
- 1–2 operators per shift × 2 shifts × $5,500/yr = **$11K–$22K/yr**
- Plus yield improvement (typically +2–5% first-pass on a 80–120 component board)
- **Payback: 12–18 months on BF-2002D solution**

> Reminder from MEMORY.md: Always confirm the actual operator cost before quoting ROI. The default $3,600/yr figure is too low for Mexican/US labor markets — use $5,200+ for realistic numbers.

## 7. Compliance Notes for Mexico Shipments

- **CE** — Southern Machinery equipment is CE certified (always include DoC in shipment)
- **NOM** (Normas Oficiales Mexicanas) — support documentation on request; some electrical items require local testing
- **Spanish-language manuals** — required for operator training; provide O&M manual in English + Spanish
- **UL recognition** — for safety-critical installations (HVAC control boards may need UL 1998 / IEC 60730 functional safety documentation)
- **Process validation** — IQ/OQ/PQ templates available if KEMX needs them for their own quality system

## 8. Proposal Structure That Worked

The 10-section proposal structure that landed well with KEMX-style customers:

1. Executive Summary (3 sentences: their problem → our solution → why us)
2. Component Analysis (with table of estimated specs + 4 "key handling challenges")
3. Solution A — recommended (architecture diagram + spec table + BOM)
4. Solution B — alternative (when to choose, BOM, performance)
5. Comparison Matrix (CapEx / cycle time / yield / recommendation stars)
6. ROI Snapshot (with assumptions stated, payback range)
7. Compliance & Documentation (CE / NOM / UL / manuals / validation)
8. **Information Requested to Proceed** (the 8 questions — this is where you make the sale)
9. Next Steps (6-step timeline with concrete week numbers)
10. Contact

**Key principle**: Never send a Proposal without Section 8 (the 8 questions). It forces the customer to share the data you need, positions you as thorough, and gives them a reason to reply even if they're not ready to buy.

## 9. Pitfalls to Avoid

- ❌ **Quoting without seeing the part drawing** — bowl tooling and nozzle design are part-specific; without dimensions you cannot give a firm number
- ❌ **Recommending a vacuum nozzle for a cube-with-screw part** — physically impossible; always default to Gripper Nozzle for this geometry
- ❌ **Skipping the polarity/orientation step** — without it, the bowl feeder will feed parts randomly and P&P will place upside-down blocks
- ❌ **Forgetting wave-solder implications** — top screw must stay functional; if customer is doing wave solder on the terminal, mention pre-solder masking
- ❌ **Using default low-wage ROI numbers** for Mexico/US/EU customers — they'll see through it; use $5,200+ labor cost for credible math
- ❌ **Sending the proposal without asking for the 8 things** — gives the customer an out to ignore you; the questions force engagement

## 10. Source Materials

- Southern Machinery **Customized Feeder & Nozzle Catalog V03** (PDF) — primary spec source
- Southern Machinery **Innovative SMT/THT Odd Form Feeder Solution** marketing PDF — BF-2002D promotion + case photos
- Internal proposal documents (this case): `KEMX_RHEEM0527_定制Feeder方案_内部分析.md` (Chinese internal) + `KEMX_RHEEM0527_Customized_Feeder_Proposal.md` (English customer-facing)
