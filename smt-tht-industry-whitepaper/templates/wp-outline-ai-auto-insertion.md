================================================================
TEMPLATE: Topical Industry White Paper Outline (SMT/THT)
================================================================

Purpose: Starter file for a Lead Magnet outline covering an
industry-wide topic in SMT/THT electronics manufacturing.
Copy and modify the structure, the 8-section backbone, and the
TCO model template — replace topic-specific data with values
verified against `wiki/entities/machines/<model>.md` and
`wiki/entities/concepts/capex-vs-roi.md`.

Source: Generated 2026-06-07 for WP-2026-001 (AI Auto Insertion
Transformation). Updated 2026-07-04 with corrected content-library
save path and dual TCO configurations. All numbers verified against
the wiki; re-verify before reuse.

================================================================
WHITE PAPER OUTLINE / LEAD MAGNET
================================================================

Title: [Topic — e.g., From Manual THT to AI-Driven Auto Insertion]
Subtitle: [Economic and Technical Transformation Playbook, 2026 Ed.]
Version: 1.0  /  Last Updated: {date}
Issuer: Shenzhen Southern Machinery Sales And Service Co., Ltd.
Author: Jason Wu, CEO & Chief Sales Engineer
Classification: Public  /  Lead Magnet Asset

Target Audience: EMS / ODM factory owners, plant managers, SMT / THT
process engineers, CFO / procurement directors evaluating CapEx
decisions for 2026-2027 capacity expansion.

================================================================
ABSTRACT
================================================================

[150-250 words] Executive elevator pitch covering:
- The structural shift this paper addresses
- Why 2026 is the tipping point
- The anchor product and its key differentiator
- The TCO outcome (payback + 5yr saving)
- The transformation roadmap outcome
- Lead Magnet gating call-to-action

================================================================
SECTION 1   INDUSTRY CONTEXT AND MACRO TRENDS (2024-2026)
================================================================

1.1  The Three Structural Forces
    - Force 1: Unidirectional labor cost inflation (CN +6-9%/yr,
      MX $5.5-7.5/hr, SEA +4-7%/yr); THT is the most
      wage-sensitive EMS process step
    - Force 2: ESG / supply chain audit pressure (RBA, EU CSRD,
      Tier-1 automotive automation-rate scoring in supplier audits)
    - Force 3: Quality standard escalation (IATF 16949 per-joint
      traceability, IPC-A-610 Class 3, AEC-Q100/Q104)

1.2  THT Demand is Reshaping, Not Declining
    - SMT 60-75% of PCBA; THT holds 25-40% (power electronics,
      automotive, industrial control, white goods)
    - Growth drivers: EV BMS (+30%/yr), industrial automation PLC,
      charging infrastructure — all need high-reliability THT
    - Key correction: "THT is dying" is a myth; THT is migrating
      to high-reliability applications that DEMAND automation

1.3  2026 EMS Industry Key Benchmarks
    [Insert data table: wage inflation curve, automation-rate
    thresholds by region, defect rate benchmarks]

================================================================
SECTION 2   INDUSTRY PAIN POINTS  (CURRENT STATE DIAGNOSIS)
================================================================

2.1  Labor Cost Trap
    - Real cost structure table: monthly operating cost of a
      manual 8-operator THT line vs. 1-operator auto line
      (use Configuration A TCO numbers)
    - Turnover cost: 35-45%/yr at THT stations; hidden
      recruitment + training + supervision overhead

2.2  Quality Trap — The PPM Iceberg Effect
    - Three failure modes: polarity reversal, lead deformation,
      float-up
    - IPC-A-610 Class 1/2/3 PPM comparison table (manual vs auto)
    - The iceberg: rework cost on books ($0.50-2.00/joint) is
      just the tip; latent costs = customer rejection, recall,
      expedited shipping

2.3  OEE Trap
    - Changeover time: 45-120 min (manual) vs <30 min (auto)
    - OEE: 45-55% (manual) vs 65-80% (auto)
    - Daily throughput gap quantified

2.4  NPI Trap
    - Manual line: 2-4 weeks per new SKU for training + tooling
    - Automotive Tier-1 RFQ NPI windows compressing to 3-4 weeks
    - Consequence: losing competitive RFQ bids due to THT
      flexibility constraints

================================================================
SECTION 3   TECHNICAL BOTTLENECKS — WHY THT AUTOMATION WAS
              HISTORICALLY UNDERESTIMATED
================================================================

3.1  The 2015-Era Barriers and 2024-2026 Breakthroughs
    [4-row table: barrier | 2015 state | 2026 breakthrough | who]

3.2  The Active Clinching Technical Moat
    - Why Japanese/European THT inserters lack it (optional or absent)
    - How Active Clinching creates a mechanical cold-joint backup
    - Thermal cycling data: 1,000 cycles at -40°C to +125°C,
      zero fatigue cracks in clinched joints
    - Applicable standards: IPC-A-610 Class 3, IPC-J-STD-001,
      ISO 16750

3.3  MES Integration Gap
    - Legacy THT: paper-based or manual scan per-board traceability
    - S-7900: REST API + XML batch + Modbus TCP; per-joint
      birth certificate; 15-year retention for automotive records

================================================================
SECTION 4   THE AI AUTO INSERTION PARADIGM
================================================================

4.1  Definition — Five Technology Pillars
    a) Multi-head parallel kinematics (3-4 heads)
    b) AI Vision with deep-learning part recognition
    c) Closed-loop force / depth monitoring (1 kHz)
    d) Active Clinching as in-process mechanical interlock
    e) Native MES / ERP data handshake (REST API, OPC UA)

4.2  What AI Auto Insertion UNLOCKS
    - NPI changeover: 45-120 min → <30 min
    - Per-joint digital traceability: force, angle, depth,
      clinch parameters logged for 15-year records
    - Self-diagnosis: feeder jam prediction, nozzle wear alerting
    - Zero-defect escape: AI Vision rejects non-compliant leads
      before insertion

4.3  S-7900 AI Vision Details
    - Trained on 50,000+ odd-form images
    - Handles reflective leads, color variation, packaging
      tolerance without re-teach
    - 360-degree lead inspection per head (not one shared camera)

================================================================
SECTION 5   SOUTHERN MACHINERY S-7900 SERIES — TECHNICAL ADVANTAGE
================================================================

5.1  Product Positioning
    [Target industries: automotive ECU/BCM/HUD, EV BMS, industrial
    drives, medical devices (IPC-A-610 Class 3), power supply]
    [Complementary lineup: S-70LD (general EMS), S-4000 (axial,
    22,000 CPH), S-3000 (radial, 10,000-12,000 CPH real speed),
    S-7020T (terminal/pin/eyelet, ±0.015mm)]

5.2  Verified Hardware Specifications (2026 Q2 Engineering Datasheet)
    [Full spec table: S-7900 standard vs S-7900 Pro]

5.3  Five Competitive Differentiators vs. Japanese Tier-1

    a) Active Clinching: STANDARD on Pro (Yamaha/Fuji: absent/optional)
    b) AI Vision: every head, independent (Japanese: shared camera, extra cost)
    c) Lead time: 4-8 weeks (vs 16-24 weeks for Fuji/Yamaha)
    d) Field service: 24-48 hr SLA (vs 1-2 weeks)
    e) CapEx: 55-65% of Japanese tier-1 at parity functional scope

5.4  Full-Line Integration Ecosystem
    [Table: upstream loader (SUL460) → feeder (BF-2002D/SBF1001) →
    S-7900 → wave soldering (S-WS450) → downstream unloader (SUL460)
    → AGV (SFY03)]

5.5  Field-Proven Use Cases (anonymized)
    - Mexican Tier-2 ODM automotive HUD: NPI 3 weeks → 30 min
    - China EV BMS IATF 16949: passed first submission
    - European white goods: OEE 62% → 81% in 6 months

================================================================
SECTION 6   FIVE-YEAR TCO ANALYSIS
================================================================

NOTE: Two TCO configurations. Use Configuration A (single-machine
entry point) for most Lead Magnet use cases. Use Configuration B
(full line) only when the prospect is evaluating a complete THT
line replacement from scratch.

----------------------------------------------------------------
6.1  CONFIGURATION A — Single-Machine Entry Point
     (1x S-7900 + 1x SUL460 + 1x SFY03 AGV)
----------------------------------------------------------------
Reference: Mexico factory, 3-shift, $6.5/hr fully-loaded wage.

    Line M: Manual THT Line (5 years)
    ---------------------------------
    Labor (8 ops x 3 shifts x $6.5/hr x 300 days):
        $2,340,000
    Internal rework / quality cost ($0.50/joint est.):
        $150,000-$200,000
    5-year total:  $2,490,000-$2,540,000

    Line A: S-7900 Auto Line (5 years)
    ---------------------------------
    CapEx (S-7900 + SUL460 + SFY03 AGV, Mexico CIF):
        $200,000
    Labor (1 op x 3 shifts x $6.5/hr x 300 days):
        $292,500
    Maintenance / spares:
        $30,000-$45,000
    Energy increment:
        $18,000-$25,000
    Feeder / fixture amortisation:
        $15,000-$25,000
    Internal rework ($0.50/joint):
        $37,500-$45,000
    5-year total:  $593,000-$632,500

    5-year net saving:  $1,881,000-$1,924,000
    Payback:  14-20 months

    Sensitivity:
      Wage +15% (e.g., peso devaluation) -> 12-16 months
      2-shift instead of 3-shift          -> 22-30 months
      China coastal ($1.5-2.5/hr)         -> 18-36 months
      All scenarios remain ROI-positive.

----------------------------------------------------------------
6.2  CONFIGURATION B — Full Line (4 Inserters + Wave Soldering)
----------------------------------------------------------------
Use when prospect is replacing or spec'ing a complete THT line.

    Line J: Japanese Reference (Fuji/Yamaha equivalent tier)
    --------------------------------------------------------
    CapEx (4 inserters + Wave Soldering + Unloader):
        $2,000,000
    Installation:
        $80,000
    Annual preventive maintenance:
        $80,000 / year
    Initial spares:
        $120,000
    Energy / consumables:
        $45,000 / year
    5-year TCO:  $2,825,000

    Line S: Southern Machinery Full Line
    --------------------------------------------------------
    CapEx:
        $1,100,000  (45% saving)
    Installation:
        $35,000
    Annual preventive maintenance:
        $25,000 / year
    Initial spares:
        $45,000
    Energy / consumables:
        $40,000 / year
    5-year TCO:  $1,505,000

    5-year TCO saving:  $1,320,000 (47% reduction)
    Adjusted payback (throughput +20%, defect -35%):  14-18 months

----------------------------------------------------------------
6.3  Strategic / Intangible Benefits (Quantified Where Possible)
----------------------------------------------------------------
    - IATF 16949 audit prep time:       -60%
    - Customer audit pass rate:          +25 pts
    - Worker comp. claim exposure:        -40%
    - ESG social pillar score:           +12 pts typical
    - Insurance premium renegotiation:    -8% site-wide
    - NPI changeover improvement:         45-120 min -> <30 min
    - New project win rate:              +15-25%

================================================================
SECTION 7   18-MONTH TRANSFORMATION ROADMAP
================================================================

Phase 1  (Month 0-3)  ASSESSMENT AND CELL DESIGN
    - Process audit: CPH, PPM, changeover time, labor cost
    - Component taxonomy: which parts need Bowl Feeder vs standard
    - Competitor comparison scoring (Yamaha / Fuji / Universal /
      S-7900)
    - ROI model with LOCAL labor cost (never use defaults)
    Output: TCO Calculator + ROI report, free, 1 week turnaround

Phase 2  (Month 3-6)  PILOT CELL
    - Install 1x S-7900 + AI Vision on highest-volume SKU
    - MES line integration + FAI (First Article Inspection)
    - MES data handshake validation
    - Train 2 process engineers + 4 operators
    Output: equipment acceptance report, FAI report

Phase 3  (Month 6-12)  FULL LINE DEPLOYMENT
    - Add S-4000 (axial) + S-3000 (radial) for full coverage
    - Integrate S-WS450 Wave Soldering (N2 option)
    - Connect all machines to MES via REST API
    - Replace remaining manual THT stations
    Target: OEE >= 70%

Phase 4  (Month 12-18)  OPTIMIZATION AND SCALE
    - Cpk >= 1.67 per joint type (IATF 16949 target)
    - Add SFY03 AGV multi-station material flow
    - 15-year traceability data retention setup
    - Second-line feasibility validation (replicate to shift 2
      or adjacent plant)

================================================================
SECTION 8   CONCLUSION AND CALL TO ACTION
================================================================

8.1  Five Core Conclusions
    [Bullet points: structural trend | technical breakthrough |
    S-7900 value prop | TCO outcome | 2026 timing window]

8.2  Lead Magnet Gating
    Full 25-page white paper (TCO worksheets, 2D/3D cell layout
    drawings, IATF 16949 traceability templates, S-7900 full
    datasheet) available in exchange for:
      a) Company name and plant location
      b) Current THT volume (CPH or components per shift)
      c) Named decision-maker and projected CapEx timeline
      d) [Optional] Current equipment brand (for legacy hook)
    Delivery: PDF download + optional 30-min technical consultation

8.3  Three-Step Action Plan
    Step 1 (this week): Contact Jason Wu to schedule free
      factory walkthrough (remote video audit or onsite)
    Step 2 (2 weeks): Complete THT data collection; receive
      free TCO model calibrated to YOUR labor cost
    Step 3 (1 month): Receive custom proposal + ROI report +
      competitor comparison; make CapEx decision

    Contact: Jason Wu | jasonwu@smthelp.com
             +86-136-0256-2576 (WhatsApp / WeChat)
             https://www.smthelp.com

================================================================
APPENDIX A  GLOSSARY — ENGLISH TERMS (UPPERCASE REQUIRED)
================================================================

SMT      Surface Mount Technology
THT      Through-Hole Technology
PCB      Printed Circuit Board
PCBA     Printed Circuit Board Assembly
CPH      Components Per Hour
Feeder   Component supply device on Pick and Place or inserter
Nozzle   Pick and Place vacuum pickup tool
Reflow Oven     SMT soldering oven (controlled thermal profile)
Wave Soldering Bulk soldering process for THT components
Pick and Place SMT component placement machine
SPI       Solder Paste Inspection
AOI       Automated Optical Inspection
MES       Manufacturing Execution System
OEE       Overall Equipment Effectiveness
CapEx     Capital Expenditure
TCO       Total Cost of Ownership
CPk       Process Capability Index
NPI       New Product Introduction
NPV       Net Present Value
IATF 16949     Automotive Quality Management System
IPC-A-610      Acceptability of Electronic Assemblies
AEC-Q100       Automotive IC Stress Test Qualification
ESG             Environmental, Social, Governance
EU CSRD         EU Corporate Sustainability Reporting Directive
EV BMS          Electric Vehicle Battery Management System
EMS             Electronics Manufacturing Services
ODM             Original Design Manufacturer
HUD             Head-Up Display
ECU             Electronic Control Unit
BCM             Body Control Module
AGV             Automated Guided Vehicle
FAI             First Article Inspection
PPAP            Production Part Approval Process
RFQ             Request for Quotation

================================================================
APPENDIX B  CITATIONS AND SOURCES
================================================================

- IPC-A-610 (Acceptability of Electronic Assemblies), IPC, latest
- IATF 16949:2016 (Automotive Quality Management System)
- IPC-J-STD-001 (Requirements for Soldered Electrical and
  Electronic Assemblies)
- IEC 61249 (PCB base material specifications)
- ISO 16750 (Road vehicles — Environmental conditions and
  testing for electrical and electronic equipment)
- Southern Machinery 2026 Q2 Engineering Datasheet,
  S-7900 High-End Odd-Form Inserter Series
- Southern Machinery 2026 Q2 Engineering Datasheet,
  S-WS450 Wave Soldering System
- Southern Machinery 2026 Q2 Engineering Datasheet,
  BF-2002D Bowl Feeder
- Southern Machinery 2026 Q2 Engineering Datasheet,
  SFY03 Magnetic Navigation AGV
- Southern Machinery Field Deployment Report (anonymized),
  12+ customer sites, 2024-2026
- World Electronics Industry Council, EMS Labor Cost Index 2024-2026
- Responsible Business Alliance (RBA) Code of Conduct, v7.0
- EU Corporate Sustainability Reporting Directive (CSRD), 2022

================================================================
END OF OUTLINE TEMPLATE
================================================================

REUSE NOTES
- For a new anchor product: keep Sections 1-2 (context + pain),
  rewrite Sections 3-5 (technical bottleneck + AI paradigm + new
  anchor product), use correct TCO configuration, tailor Section 7
  roadmap phases, keep Section 8 CTA + Lead Magnet gating.
- Always re-verify ALL numbers against the wiki before reuse.
  Do not carry the S-7900 specs verbatim if the anchor product
  is a different model.
- File naming: `THT-Automation-Whitepaper-Outline_v{YY.MM.DD}_{version}.md`
- Save path: `~/SMThelp-Content-Library/Lead-Magnets/`
- Also copy the final outline to `references/wp-{topic-slug}_v{date}.md`
  inside this skill's directory so future agents have a real example.
- Dual TCO note: Configuration A (single-machine) is for first
  contact / Lead Magnet gating. Configuration B (full line) is for
  later-stage prospect conversations when they are evaluating a
  complete line replacement.
