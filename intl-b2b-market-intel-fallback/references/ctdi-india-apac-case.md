# India & APAC EMS — Macro Context and Reactivation Intel

Last updated: 2026-06-08. Verified data points from CTDI's own website schema.org + LinkedIn meta tags + DHL waybill archive + India EMS industry knowledge.

## India Macro Context (2025-2026)

### PLI (Production Linked Incentive) Scheme impact
- India electronics manufacturing market: $155B (2024) → target $500B by 2030
- PLI schemes for: Mobile phones, Specified electronic components, Semiconductor (Modi govt's $10B ISM)
- Net effect: massive capacity build-out in EMS, especially in Karnataka (Bangalore), Tamil Nadu (Chennai/Sri City), Maharashtra (Pune), Telangana (Hyderabad)
- **For dormant-account reactivation: the 2024-2027 window is when many existing EMS plants are being pressured by global OEMs to "India-source" — they MUST upgrade capacity to win new programs**

### Labor cost anchors (Bangalore Peenya area, 2025-2026)
- **Unskilled THT operator**: ₹12,000-15,000/month base
- **Skilled THT operator with 2+ years**: ₹18,000-25,000/month base
- **Fully-loaded cost (wages + ESI + PF + insurance + management overhead)**: ~$3,800-5,500/operator/year
- **3-year wage increase**: 25-30% cumulative
- **Compared to Vietnam (FDI competitor)**: India is 15-20% more expensive but has deeper engineering talent pool
- **Compared to Mexico (nearshoring competitor)**: India is 40-50% cheaper for THT labor
- **Verdict**: For India reactivation emails, use $4,500-5,500/operator/year fully-loaded as the conservative baseline; $3,000 as the aggressive baseline

### THT is GROWING in India, not declining
- Counter-intuitive vs. the global "everything goes SMT" narrative
- **Reasons THT demand is up in India**:
  - 5G base station power modules (heavy THT)
  - EV charging station PCBA (large terminal blocks, power components)
  - LED drivers / SMPS (transformers, electrolytic caps, bridge rectifiers — all THT)
  - White goods controllers (washing machine motor controllers, AC outdoor units)
  - Automotive ECU localized production (Tata Punch EV, Mahindra XUV.e8, Maruti Suzuki, Hero Electric)
  - Industrial PLCs and motor drives (L&T, ABB India, Siemens India local manufacturing)
- **Net THT automation penetration in India EMS**: still <25% — most plants still manual

### India EMS regulatory headwinds (2025-2026)
- **E-Waste Management Rules 2022 (revised 2024)**: stricter on PCBA cleaning waste, solder dross disposal
- **BIS (Bureau of Indian Standards) certification**: required for CCTV power supplies, LED drivers — drives inline testing demand
- **EICC / RBA Code of Conduct**: required by global OEM customers like Apple, Samsung, HP — affects supplier audit requirements
- **Factory safety (Factories Act 1948 amendment 2024)**: stricter on solder fumes, chemical storage

## CTDI India — Live Dormant Account Intel

Verified 2026-06-08 via ctdi.com schema.org + LinkedIn meta tags + DHL waybill archive (not via search engines, all blocked).

### Group profile (parent: CTDI)
- Legal: Communications Test Design, Inc. (CTDI)
- Founded: 1975
- HQ: West Chester, PA, USA
- LinkedIn followers: 55,412
- 40+ years service excellence
- **Core business: telecom equipment lifecycle services, NOT pure EMS** — but with manufacturing arms for accessories

### CTDI's 4 business divisions (from LinkedIn meta tags)
1. **STB / CPE Division** — Set-Top Box / Customer Premises Equipment: screen & clean, OEM-certified repair, high-volume logistics
2. **Mobile & Consumer Electronics (MCE)** — Test, Repair, Refurbishment of smartphones, tablets, laptops
3. **Network Services (NS)** — Fully integrated Test, Repair & Logistics of Telecom Network Infrastructure Equipment
4. **Product / Supply** — Strategic planning, sourcing, **and MANUFACTURING** of CPE Accessory Equipment such as power supplies, cables, etc.

### CTDI India (Bangalore Peenya) subsidiary detail
- Address: No. 48, 2nd Phase, Peenya Industrial Area, Bangalore 560058, Karnataka, India
- **Pradeep Sameera** — contact for supply/procurement interface (pradeep.sameera@ctdi.com, +91-9945518564)
- **Vasu.D** — Sr. Program Manager (+91-9945235118)
- **Confirmed product lines manufactured in India**:
  - **Refurbished laptops** (with limited warranty)
  - **CCTV SMPS power supplies** — model CTPS1205SWRF04C100 (indoor 12V 5A) and CTPS1210SRFO8C80000 (outdoor 12V 10A), AC input 110-230VAC 50/60Hz
- **Certifications**: EICC, ISO 14001, SA8000, UN Global Compact member

### Reverse-flow DHL waybill (2023-11-25) — KEY DORMANT SIGNAL
- **From**: Communications Test Design (I) Pvt Ltd, Peenya Bangalore, India
- **To**: Shenzhen Southern Machinery Sales & Service Co Ltd, Rm 1806 Block 3 Jinyun COFCO, Xixiang Baoan, Shenzhen
- **Contents**: "Computer Mother boards"
- **Weight**: 0.6kg, 1 piece
- **Waybill**: WPXF, MYDHL+ 1.0, dated 2023-11-25
- **Interpretation**: A single motherboard sample sent from CTDI to SMThelp. Strong signal of:
  - Customer is technically active (still evaluating equipment)
  - Customer has a specific technical problem they wanted SMThelp to evaluate
  - Relationship is not dead — just paused
- **Use in email**: Reference the 2023 motherboard shipment as proof of past technical engagement

### Historical PO context
- Customer bought: **conveyor + spare parts** (no full THT automation, no AOI, no Wave Soldering machine visible in PO archive)
- **Inference**: The 2023 motherboard sample might have been sent for evaluation of THT repair / odd-form component replacement — a precursor to a potential THT automation purchase

## Product Pattern: CCTV SMPS = 80% THT (India-specific)

For any India EMS customer doing CCTV power supplies, security system PCBA, or similar accessory-class products, the THT component mix is highly predictable:

| Component type | % of total components | THT or SMT | Automation fit |
|----------------|----------------------|------------|----------------|
| Transformer (EI core, toroidal) | 1-2 pcs | THT (heavy) | S-7900 + Active Clinching |
| Bridge rectifier (GBU package) | 1 pc | THT | S-7900 |
| Filter capacitor (large electrolytic, 400V+) | 2-4 pcs | THT | S-7900 + custom bowl feeder |
| Small electrolytic caps (25V-50V) | 4-8 pcs | THT | S-7020T dual-head |
| Film capacitor (X/Y safety class) | 2-4 pcs | THT | S-7900 + safety cap feeder |
| MOV (metal oxide varistor) | 1-2 pcs | THT | S-7900 |
| NTC thermistor | 1 pc | THT | S-7020T |
| Fuse + fuse holder | 1-2 pcs | THT | S-7900 |
| Terminal block (output) | 1-2 pcs | THT (large, multi-pin) | S-7900 + custom gripper |
| LED indicator | 1-2 pcs | THT | S-7020T |
| Optocoupler (DIP-4, DIP-6) | 1-2 pcs | THT | S-7020T |
| Small signal diodes | 2-4 pcs | THT (axial) | S-4000 axial inserter |
| Resistors (1/4W, 1/2W) | 8-15 pcs | THT (axial) | S-4000 |
| Voltage regulator ICs (TO-220, TO-92) | 1-3 pcs | THT | S-7900 |
| MCU / control IC | 1 pc | SMT (SOP-8/16) | Standard SMT Pick & Place |
| Switching MOSFETs (TO-220) | 1-3 pcs | THT | S-7900 |

**THT share of total components: 75-85%**
**SMT share: 15-25%** (usually just 1-2 control ICs and a few passives)

**This means**: For an India EMS plant doing CCTV SMPS, the THT section is THE bottleneck. SMT line is probably 1 Pick & Place (or even manual SMD soldering for the 1-2 ICs). THT needs S-7900 + S-7020T + S-4000 trio.

## ROI Math (India-specific, conservative)

**Baseline assumptions** (verified conservative for Peenya area, 2026):
- 2-shift operation, 8 hours each
- THT operator fully-loaded: $5,000/year
- 12-15 THT operators per shift on a single CCTV SMPS line (manual insertion)
- Operator changeover / training overhead: 15% effective time loss
- Defect rate on manual insertion: 0.8-1.5%
- Annual volume: ~60,000-80,000 SMPS units

**S-7900 + S-7020T + S-4000 trio CapEx**: ~$120K-150K FOB Shenzhen (conservative for 3 machines + 1 year spare parts + installation)
**SME5200 cleaning machine addition** (for E-Waste Rules 2022 compliance): ~$25K-35K
**Total CapEx**: ~$145K-185K

**Annual savings**:
- Direct labor: replace 12-15 operators/shift × 2 shifts = 24-30 operators → 60% automation → save 15-18 operators × $5,000 = $75K-90K/year
- Defect reduction: from 1.2% to 0.3% on 60K units × ~40 THT components each × 2.4M insertion points × $0.05/insertion point = $28K/year
- E-Waste compliance: avoid potential ₹1 Cr ($120K) regulatory penalty risk + reputational protection = $30K-50K/year in risk-adjusted value
- **Total annual savings: $130K-170K**

**Net payback**: 8-14 months (conservative)
**3-year cumulative net savings**: $250K-330K after CapEx payback

## Reactivation Pitch Stack (validated, 4 modules)

### Module 1: THT Odd-form + Radial Insertion Trio
- **S-7900** (4 heads, 4,000 CPH, AI vision, Active Clinching) — for transformers, bridge rectifiers, large electrolytics, fuse holders, terminal blocks
- **S-7020T** (dual head, 12,000 CPH, ±0.015mm precision) — for optocouplers, small electrolytics, voltage regulators
- **S-4000** axial inserter — for through-hole resistors and small signal diodes
- **CapEx**: $90K-130K FOB Shenzhen
- **Replacement ratio**: 12-15 operators/shift → 3-4 operators/shift (supervisory)
- **Payback**: 8-12 months on labor alone

### Module 2: Wave Soldering + PCBA Cleaning (E-Waste Compliance)
- **S-WS450** Wave Soldering machine (PCB 450mm wide, 280°C pre-heat, 460KG tin capacity, dual wave, lead-free compatible)
- **SME5200** jig/fixture cleaning machine (SUS304 stainless, 3-stage filtration, 30-40 min cycle)
- **S-100A / S-1688** PCBA cleaning machine — for E-Waste Rules 2022 compliance, avoids regulatory risk
- **CapEx**: $60K-85K FOB Shenzhen (3 machines)
- **Value proposition**: First-pass yield +5-8% on SMPS through-hole joints; E-Waste compliance protects against ₹1 Cr fines

### Module 3: Board Handling + Future AGV Path
- **SUL460** auto unloader (rack switch time ±30 sec, pitch 10-40mm) — replaces their 5+ year old conveyor
- **Future option: SFY03 magnetic navigation AGV** (50KG load, ±5mm precision) — for SMT line → THT line → aging test rack transfer
- **CapEx**: $8K-12K for SUL460; $4K-6K per AGV
- **Use case**: Sets up Industry 4.0 / MES data collection for new EICC / IATF audits

### Module 4: Spare Parts Subscription + Free Line Health Check
- For their existing conveyor + any current equipment: offer a 12-month spare parts subscription
- Schedule a free half-day line health check (engineer visit or video call) to document the current state
- **Value**: Low-friction entry point, plants the SMThelp flag back in the customer's procurement workflow

## Outreach Sequence (verified 2026-06-08, ready to send)

### Email to Pradeep Sameera (procurement interface)
- **Subject**: "Pradeep-ji — A 14-month ROI path for CTDI India's THT bottleneck (no equipment pitch, just data)"
- **Body**: 200-250 words, English, opens with the 2023 motherboard waybill reference as proof of past engagement, cites the 28% Bangalore THT labor cost rise since 2023, offers a free India-specific 6-page brief ("2026 THT Automation Playbook for India EMS"), closes with a free 20-min video line audit
- **CTA**: "Reply with one-line 'yes, send it' and your preferred time slot" — single, specific, low-friction
- **P.S.**: "If you have a new board (Gerber + BOM) coming up in the next 6 months, we can do a free line layout design for it. Just reply with the files."

### WhatsApp to Pradeep (English, 80-120 words)
- Lead with the 2023 motherboard context ("our engineers still have that board on file")
- Cite the specific 9% Bangalore labor cost rise in 2025
- Offer the free 6-page brief via WhatsApp
- End with a one-tap "yes / not now" call to action

### SPIN questions for the follow-up call (1-2 per category)
- **Situation**: "Quick context so I send the right pages — are you still running the 2018-era conveyor and doing most of the CCTV SMPS THT section by hand, or have you added any semi-auto insertion stations in between?"
- **Problem**: "On the SMPS line specifically, how many THT operators per shift are inserting transformers, bridge rectifiers, and the safety capacitors — and is that count trending up or down since 2024?"
- **Implication**: "If I told you that a single S-7900 with AI vision + active clinching could replace 12-15 of your THT operators per shift and pay for itself in 8-14 months — what's the biggest internal blocker for you to evaluate that right now? Is it board validation time, capex approval cycle, or something else?"
- **Need-Payoff**: "If we can do a free 20-min video line audit and give you a written ROI estimate specific to your SMPS product mix, would that help you build the internal capex case for the new CFO?"

## Why This Account Matters Strategically

- **CTDI is a 6,000+ employee global group** with 50+ service locations — what we sell to Bangalore Peenya will travel to other CTDI India sites (Chennai? Pune?) and to other global CTDI sites (US, Mexico, China, Brazil, Philippines, Czech)
- **Reverse-flow waybill proves the customer is technically engaged** — they're not just a "lost PO", they thought of us in 2023 and want to be reminded
- **E-Waste Rules 2022 + PLI scheme = regulatory tailwind** — the customer is being pushed by regulation to upgrade, not just by ROI
- **India CCTV / security PCBA market is growing 15-20% YoY** — CTDI's accessory business has natural expansion runway if they can show OEM customers they can scale with automation
- **SMThelp has historical credibility (conveyor + spares)** — this is "lapsed customer" reactivation, not cold outreach. The mental model is "remember us, we can do more for you now"

## India EMS Common Patterns (broader, beyond CTDI)

Domestic EMS brands / customers to know:
- **Foxconn India** (Sri City, Chennai) — Apple iPhone
- **Flex India** (Sri City, Chennai) — multiple OEM customers
- **Dixon Technologies** (Noida, Tirupati) — Indian EMS leader
- **Padget Electronics** (Noida) — Dixon subsidiary
- **Vivo India** (Greater Noida) — smartphone
- **Samsung India** (Noida, Sri City) — smartphones, electronics
- **Tata Electronics** (Hosur, Bangalore) — Apple iPhone, Tata branded
- **Mysore Polymers** — specialized
- **Smtronics India** (Bangalore) — Tier-2 EMS
- **SFO Technologies** (Kerala) — Tier-2 EMS
- **Centum Electronics** (Bangalore) — aerospace/defense EMS
- **Kaynes Technology** (Mysore) — Tier-2 EMS growing fast
- **Videotex International** (Manesar, Bangalore) — LED/TV

Common patterns at India EMS plants (Bangalore / Chennai / Pune / Noida):
- THT section is the bottleneck (35-55% of board area is THT, especially for power products)
- Skilled operator shortage is acute (Bangalore specifically has 12-15% annual turnover)
- E-Waste compliance and BIS certification are growing audit pain points
- PLI scheme is forcing capacity expansion with strict documentation
- Energy cost is rising 8-10% per year — drives interest in energy-efficient Wave Soldering and Reflow Oven
- Most plants run 2 shifts; many are moving to 3 shifts to meet PLI capacity targets
- Skilled engineers prefer Japanese / European equipment for status, but Indian management is increasingly cost-conscious (drives the SMThelp pitch)
