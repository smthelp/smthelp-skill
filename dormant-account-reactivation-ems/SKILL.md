---
name: dormant-account-reactivation-ems
description: "Use this skill when reactivating a dormant (1-3+ year silent) EMS/OEM customer who has historical purchase records with Southern Machinery. Triggers on inputs like 复联老客户 / 唤醒沉睡客户 / 二次开发 / reactivate dormant account, or when the user provides a past-buyer company profile with named contacts plus historical purchase data plus geographic location. Produces a complete 4-phase activation package -- market intelligence brief, gap analysis with quantified ROI, tailored micro-whitepaper outline, and multi-channel outreach drafts (Email + WhatsApp). Born from the Liteon Brazil Manaus engagement (Panasonic spare parts customer, 2+ years silent, R$50M SMT expansion underway)."
metadata:
  source: hermes
  origin: "sales-engineering/dormant-account-reactivation-ems"
---
# Dormant Account Reactivation for EMS Customers

This skill codifies the proven 4-phase framework for turning dormant, inactive, or past-buyer EMS/OEM accounts into active re-orders of Southern Machinery spare parts, peripheral upgrades, or new line expansions. Born from real engagement with Liteon Brazil Manaus (Panasonic spare parts history, 2+ years silent, R$50M SMT expansion 2024-2025, new GM hire, EV charger product line launch).

## When to Use This Skill

Use this skill when the user provides ALL of the following:

- A specific past-buyer company name (and ideally website)
- At least 2 named contacts with email/phone
- Historical purchase record (machine brand, model, or spare parts category)
- A geographic location (city + country)

Do NOT use this skill for:

- Brand new cold outreach (no purchase history) -> use `cold-email-templates-ems-global`
- Active hot leads requiring quotation -> use `smt_roi_calculator`
- Internal product spec questions -> use `smthelp-knowledge-base`
- Generic market research without a specific account -> use `smt_market_intelligence`

---

## Phase 1: Real-Time Market Intelligence (全网情报检索)

**Why this matters:** A dormancy gap of 1-3 years means the customer's reality has changed dramatically. You CANNOT write a credible re-engagement without knowing:

- Their current capex trajectory (expanding? contracting? pivoting products?)
- New leadership (new GM = new supply chain audit window, 90-day opportunity)
- Local labor/policy shocks (this is your urgency driver)
- New product lines (this is your technical wedge into new equipment sales)

**Mandatory 5-Channel Parallel Search:**

Run these searches in parallel using `web_search` or `opencli browser`:

1. **Customer corporate news** (English + local language)
   - `"<Company Name>" <City> expansion OR investment OR new line`
   - `"<Company Name>" <Year> factory OR plant announcement`
   - Search their IR / press release / LinkedIn company page

2. **Customer leadership changes**
   - `"<Company Name>" <City> new director OR new GM OR new COO`
   - LinkedIn search: `"<Company Name> <City>" plant manager`
   - High-priority if a new GM/plant head was hired in the last 6 months

3. **Local EMS market dynamics**
   - `EMS <Country/Region> <Year> labor cost OR salary increase`
   - `<Country/Region> electronics manufacturing workforce shortage`
   - `<Country/Region> industrial automation policy`
   - Brazil-specific: `<Country/Region> ZFM OR tax incentive OR local content rule`

4. **Industry-specific pain drivers**
   - `EV charger manufacturing THT insertion automation`
   - `power supply PCB assembly radial insertion machine`
   - `<Vertical> EMS <Country> certification OR quality standard`

5. **Competitor activity in region**
   - `"<Company Name>" <City> Panasonic OR Fuji OR Yamaha supplier`
   - `EMS <Country> Chinese equipment supplier`

**Network-Blocked Countries (e.g., Bulgaria, parts of Eastern Europe, Central Asia):**

When Google/Bing are blocked or return 403/blank pages:
- Use **Eurostat** (https://ec.europa.eu/eurostat) for EU labor force data
- Use **ILO** (https://www.ilo.org) for international labor statistics
- Use **Trading Economics** (alternative domain or cached version)
- If data cannot be verified live, state explicitly: "estimated range: X–Y [currency], based on [source], subject to verification"
- NEVER fabricate specific percentages (e.g., "13% YoY increase") without a source link
- For Bulgaria-specific data: try Wikipedia mirror sites or use archived versions from web.archive.org

**MANDATORY Pre-Outreach Verification Step:**

Before writing any email or whitepaper, answer these 3 questions:

1. **Does the customer manufacture in-house or outsource PCBA?** Many brand companies (security hardware, IoT devices, consumer electronics) outsource 100% of PCBA to EMS partners. If outsourced, THT equipment pitch is irrelevant. Confirm by: checking their website for "our factory" vs "our partners" language; checking LinkedIn for manufacturing vs design roles; checking industry databases.

2. **Has the customer's core equipment been identified?** If the historical purchase was peripheral equipment only (loaders/unloaders/conveyors = <$20K total), do NOT frame it as "we've been your machine supplier." Frame as "your board handling equipment partner."

3. **Are all labor cost figures sourced?** For any country with network restrictions, explicitly note which data is estimated vs verified. A wrong number destroys credibility more than no number.

**Output:** A 200-300 word intel brief covering customer moves, local market shocks, and 1-2 quantified urgency drivers. Every fact must be sourceable or explicitly marked as estimated.

---

## Phase 2: Gap Analysis & Pain Diagnosis (痛点诊断)

**Why this matters:** Customers ignore generic "we can help you automate" pitches. They engage only when you name a specific bottleneck they are already feeling. The diagnostic must connect their historical purchase to their current gap.

**The 5-Pain Diagnostic Framework:**

For any dormant EMS account, check these 5 pain vectors against their historical purchase signal:

| # | Pain Vector | Diagnostic Signal (from history) | Quantified Impact |
|---|-------------|----------------------------------|-------------------|
| 1 | THT/DIP capacity ceiling | Old SMT line w/ manual DIP, expanding SMT capacity | 8-12 manual operators/shift = $180K-$275K/yr labor cost |
| 2 | Feeder/Nozzle wear | History of spare parts purchase = old equipment still running | 1-3% pick error rate = $50K+/yr material loss |
| 3 | New leadership audit window | New GM/plant manager hired in last 6 months | 90-day supply chain review = make-or-break window |
| 4 | MES / Industry 4.0 gap | Old equipment + new factory expansion in progress | Blocks company-wide digitalization roadmap |
| 5 | New product line process gap | New EV / automotive / power product launch | Standard machines cannot handle new component types |

**ROI Funnel Calculation (standard formula):**

```
Annual labor cost saved   = (operators removed) x (shifts) x (loaded hourly wage x 2080 hrs)
Annual defect savings     = (current PPM - target PPM) x annual volume x (cost per defect)
Total annual savings      = Labor saved + Defect saved + Throughput uplift value
Capex                     = Equipment + Integration + Training + Spare parts buffer
Payback period (months)   = (Capex / Total annual savings) x 12
```

**Benchmark case (Liteon Brazil, validated 2026-06-04):**

- 12-16 manual operators removed x 2 shifts x $5/hr loaded x 2080 hrs = $250K-$330K/yr labor saved
- PPM reduction from 1,000 -> 100 = ~$70K/yr defect savings
- Capex: $120K-$180K for S3000 + S70LD + S7020 + SBF1001 + integration
- **Payback: 6-11 months**

**IMPORTANT (S3000 speed correction, validated 2026-06-08):**
- S3000 actual production speed = **10,000–12,000 CPH** (real-world radial insertion)
- "20,000 CPH" is the theoretical peak spec under ideal axial conditions only
- NEVER quote 20,000 CPH in customer-facing sales materials -- engineers will challenge it
- Always use "up to 12,000 CPH" for real-world ROI calculations

**IMPORTANT (S-70LD first recommendation, validated 2026-06-08):**
- For alarm/IoT/security hardware products, lead with S-70LD odd-form inserter, NOT S3000 radial
- S-70LD solves the highest-cost, highest-defect bottleneck first (relays, connectors, transformers)
- S-70LD with STF1001 Tube Feeder is the softest technical conversation opener for tube-pack components

**CRITICAL:** Always use LOCAL labor cost, not the default $3,600/yr in the ROI calculator. For Manaus, Poland, Vietnam, Mexico -- verify the actual loaded operator cost (wages + benefits + management overhead) before quoting payback. If you cannot verify, challenge the assumption and explicitly state the range.

---

## Phase 3: Tailored Micro-Whitepaper (白皮书大纲)

**Why this matters:** A whitepaper gives you a reason to reach out that is NOT a sales pitch. It positions you as a peer-level engineering expert and creates a content asset the customer can share internally with their GM and procurement.

**Whitepaper Title Formula:**

`<Vertical> Automation for <Region/Country>'s <Trend> Sector: Solving the <Specific Bottleneck> at <Customer Name>`

Subtitle: `How Southern Machinery's Complete SMT + THT Line Solutions Enable Rapid Capacity Doubling with 50% Lower Labour Dependency`

**Mandatory 7-Section Structure:**

### Section 1: Opening Hook (1 paragraph)
- Name the customer's specific recent expansion move (proves homework)
- Name the specific bottleneck (THT section, NOT generic "automation")

### Section 2: The Math That Keeps Factory Managers Up at Night
- Show the conflict between new SMT capacity and old THT section
- Quantify labor cost trajectory in their region
- Show the OEE gap (typical 55-65% manual vs 80-90% automated)

### Section 3: Solution Module A -- Core THT Automation
Pick the right Southern Machinery machine based on the customer's products:

| Customer Product | Primary Machine | Secondary Machine | Peripheral |
|------------------|-----------------|-------------------|------------|
| Power supplies / chargers | S3000 Radial Insertion | S4000 Axial Insertion | S-100A Stencil Cleaner |
| Alarm / security / IoT hardware (relays, connectors, buzzers) | **S-70LD Odd-Form Inserter FIRST** | S3000 Radial | S-1688 PCBA Cleaner |
| EV / automotive odd-form | S70LD Odd-Form Inserter | S7020 Pin Terminal Inserter | S-1688 PCBA Cleaner |
| Consumer electronics (high-mix) | S3000 Radial + S70LD | SBF1001 Bowl Feeder | SME-6200 |
| LED / lighting | S3000 Radial | S-100A | SUL460 Unloader |

**Machine priority rule (M2M Bulgaria case lesson, 2026-06-08):** For alarm/relay/connector-heavy products (like security hardware, fire alarm communicators, IoT devices), lead with S-70LD odd-form inserter FIRST, not S3000 radial. The logic: odd-form manual insertion has the highest labor cost, highest defect rate, and customers often don't know automation exists for these components. The S-70LD with custom STF1001 Tube Feeder is the natural conversation opener: "Do you have tube-pack connectors or relays? Our S-70LD with custom tube feeder handles those automatically."

For each machine, 3-4 bullets: speed (CPH), accuracy (placement tolerance), what it replaces (operators), MES integration capability.

### Section 4: Solution Module B -- Spare Parts & Feeder Replacement
For accounts with spare parts history:

- Southern Machinery Universal-Compatible Feeder series
- Compatibility with Panasonic CM602 / NPM / Fuji NXT / Yamaha YS / Siemens SX
- Price vs OEM: 50-60% of OEM list
- Lead time: Shenzhen warehouse 1-day dispatch vs OEM 8-12 weeks
- Custom Odd-Form Feeder capability: STF1001 Tube, SBF1001 Bowl, SDF1001 Shaking

### Section 5: ROI Module
- Use the formula from Phase 2
- Add regional tax/regulatory angle:
  - Brazil: ZFM IPI / ICMS import duty credit
  - Mexico: IMMEX program savings
  - Poland: EU structural fund eligibility
  - Vietnam: Hi-Tech zone incentives

### Section 6: Industrial 4.0 / MES Integration
- EtherCAT + Windows native interface (vs old equipment's closed architecture)
- Real-time OEE, CPH, PPM data export
- Direct MES / ERP integration without middleware
- Production traceability, Andon alarm, SPC statistics

### Section 7: Why Southern Machinery vs Used / Refurbished Alternatives

| Comparison Dimension | Used OEM Refurb | Southern Machinery New |
|---------------------|-----------------|------------------------|
| Upfront price | Lower (but hidden refurb cost) | Clear FOB price + 12-month warranty |
| Spare parts availability | Discontinued models = no parts | 1-day dispatch from Shenzhen |
| MES integration | Closed software, needs hack | Native EtherCAT + Windows |
| Service support | OEM refuses to service used | 24/7 WeChat / WhatsApp remote |
| Customization | Cannot customize Feeder / Nozzle | Full custom in 3-4 weeks |
| Energy efficiency | 10-15 yr old motors | New servo, 30%+ energy saving |

---

## Phase 4: Multi-Channel Outreach (话术创作)

**Why this matters:** The customer has ignored you for 1-3 years. A single email will fail. You need coordinated multi-channel touch with strong, low-friction CTAs.

### 4.1 Email Draft (Primary Touch)

**Subject line formula:**

`Re: <Customer City> Factory Expansion - <Specific Bottleneck> Strategy for <New Product Line>`

**Body structure (4 paragraphs):**

**Para 1 -- The Homework Paragraph (2-3 sentences)**
- Open with a SPECIFIC, RECENT, VERIFIABLE fact about them (new line, new GM, new product launch)
- Show this is not a mass blast

**Para 2 -- The Pain Paragraph (3-4 sentences)**
- Name the specific bottleneck their expansion creates
- Quantify it (labor cost %, defect rate, capacity gap)
- Use the language of THEIR factory manager

**Para 3 -- The Value Offer Paragraph (3-4 sentences)**
- Offer a NO-COST, NO-OBLIGATION engineering asset:
  - "Complimentary Line Health Check" (45-min video audit)
  - "Free line layout proposal" (need Gerber file)
  - "Free ROI study" (need monthly volume + component list)
- Explicitly say: "no sales pitch, just engineering assessment"

**Para 4 -- The CTA Paragraph (3 bullet options)**
- Option A: Reply with [specific data 1 -- e.g., monthly volume + labor headcount]
- Option B: Send Gerber / CAD for free line layout proposal
- Option C: Visit www.SMThelp.com to download the 2026 digital product catalog
- Sign off with full contact + WhatsApp / WeChat
- **Optionally attach a 1-page A4 ROI one-pager PDF** for the most-likely-purchased machine — see `b2b-roi-one-pager` skill for the standardized attachment. This converts 3-5x better than text-only emails for senior procurement readers who scan, not read.

**CC strategy:** Always CC the engineering buyer, indirect contacts, AND new leadership (if any) in the first email. Personalize the To: line.

### 4.2 WhatsApp Short Hook (Secondary Touch)

**Formula:** 80-120 words, bilingual (local language + English), one specific pain + one specific outcome + one low-friction CTA.

**Template:**

`<Name>, congrats on the <specific move>! New <product line>, and now the real challenge: <bottleneck>. Your new <SMT line> will double capacity, but if <THT section> stays manual you will cap the ROI. We have <specific solution> that replaces <N operators> per machine -- and integrates with your existing <old brand> line. Can I send a quick automation study? Just reply with <one piece of data>. www.SMThelp.com`

**Language mapping:**
- Brazil -> Portuguese opening, English technical terms
- Mexico -> Spanish opening, English technical terms
- Poland / Czech -> English (technical buyers prefer it)
- Vietnam -> Vietnamese opening, English technical terms
- India -> English throughout

### 4.3 SPIN Follow-Up Question Matrix

After the customer responds (or as LinkedIn DM follow-up), use these SPIN questions to deepen the pain:

| SPIN Stage | Question Template |
|------------|-------------------|
| **Situation** | "How many operators are currently running on your DIP line per shift, and what is your target volume for <new product> by Q3 <year>?" |
| **Problem** | "What is your current defect rate on manual odd-form insertion -- particularly for <specific component type>?" |
| **Implication** | "If <X>% annual labor cost increase continues in <region>, how does that impact your margin on <product> over the next 3 years?" |
| **Need-payoff** | "If you could run the DIP section with 2 operators monitoring automated machines, what would that mean for your capacity doubling plan?" |

### 4.4 Multi-Round Follow-Up Sequences (3-Round Framework)

After the Round 1 first-touch email, do NOT send the same email again. Each round must use a different hook angle. Full templates, WhatsApp compression variants (60 chars), and pitfall rules are in `references/follow-up-email-sequences.md`.

| Round | Timing | Hook Angle | Core Change from Round 1 |
|-------|--------|------------|--------------------------|
| 1 | Day 0 | Pain + Value offer | Standard first-touch (see 4.1) |
| 2 | Days 3-5, no reply | **Subsidy scarcity** | Government grant deadline creates urgency — verifiable data required |
| 3 | Days 7-10, no reply | **Competitor FOMO** | Real regional reference case — verifiable before using |
| 4 | 30+ days | **New information** | Trade show, news release, new product — prove they're active |

---

### 4.5 Feel-Felt-Found Objection Handling Templates

For the most common EMS equipment objections, use the Feel-Felt-Found framework documented in `references/feel-felt-found-objections.md`. The canonical objections covered are:

| Objection | Core Response Frame |
|-----------|-------------------|
| "We already use Panasonic/Universal" | Add, don't replace — targeted THT upgrade alongside existing SMT line |
| "Budget is tight right now" | Delay cost > machine cost; grant + payback math |
| "Chinese equipment quality concerns" | Engineering discipline vs country of origin; video factory tour offer |
| "Our team is trained on Universal" | 3-day training; operators prefer machine over manual labor |

**Rule:** Always end with a micro-CTA question, never a closing statement. The goal is one reply, not a commitment.

---

## Output Delivery Format

When delivering the final activation package to the user, use this exact structure (all Chinese headers, English content blocks for email/WhatsApp):

```
## 一、老客户背景与所在地 EMS 市场深度洞察 (Market Intelligence)
## 二、客户产线潜在痛点与升级难点诊断 (Gap Analysis)
## 三、专属行业技术白皮书大纲 (Tailored Solution Brief)
## 四、高转化率多渠道复联话术 (Outreach Assets)
   ### 1. High-Conversion Email Draft
   ### 2. WhatsApp Short Hook
```

The package must be 100% focused on sales execution. No filler, no "hope this helps", no end-of-message menu. Deliver and stop.

---

## Pitfalls & Anti-Patterns

**NEVER do these:**

- Start with "Hope this email finds you well" or any filler greeting
- Pitch a specific machine before establishing the pain
- Use generic superlatives ("revolutionary", "best-in-class", "cutting-edge")
- Fabricate specs, certifications, CPH numbers, or ROI figures
- Send identical copy to multiple contacts without personalizing the To: line
- Use a hard sales CTA in the first touch (must be value-led)
- Skip the local-language version in WhatsApp for non-English markets
- Quote a payback period using default labor cost -- always verify local loaded cost first
- CC unrelated contacts or expose the full contact list to a single recipient
- Send without human approval (per SOUL.md: external actions require permission)
- Assume the customer operates in-house manufacturing -- many brand companies (alarm, IoT, security hardware) outsource 100% of PCBA to EMS partners. ALWAYS verify manufacturing model before pitching equipment
- Cite specific local labor cost increase percentages (e.g., "13% YoY") without a verifiable source link
- Cite specific government subsidy programs (e.g., "50% CapEx coverage") without the exact program name and eligibility link
- Use "your PCB Loader/Unloader supplier" framing when SM only supplied peripheral equipment (creates false intimacy)
- Say "those systems are still serving reliably" -- if equipment was scrapped, this backfires badly
- Quote S3000 at 20,000 CPH in sales materials -- engineers will challenge this. Use "up to 12,000 CPH (real-world production speed)"
- Include CE certification claims if not confirmed with Jason Wu -- for EU markets this is a legal issue, not a marketing point

**ALWAYS do these:**

- Open with a SPECIFIC, RECENT, VERIFIABLE fact about the customer
- Quantify the pain in their local currency / cost basis
- Offer a FREE, NO-OBLIGATION engineering asset (Health Check / Layout / ROI)
- Provide 3 CTA options in the email
- Include www.SMThelp.com and reference the 2026 digital product catalog
- CC engineering buyer + indirect contacts + new leadership in the first email
- Mirror their language: local language for the WhatsApp hook, English for technical email
- State any unverified number as a range with explicit assumption caveat
- Run a final verification pass against the "Verification Checklist" below
- For EU countries with network-blocked sources (Bulgaria, parts of Eastern Europe): use Eurostat (https://ec.europa.eu/eurostat) or ILO (https://www.ilo.org) as fallback data sources, and always state "estimated" when data cannot be verified live
- For brand companies (security hardware, IoT, consumer electronics with no in-house SMT): confirm manufacturing model BEFORE pitching THT equipment -- ask "do you produce PCBA in-house or work with an EMS partner?"
- For WhatsApp outreach: target 60-80 words max. Bulgarian/Polish/Czech B2B buyers scan, they do not read
- Always add for EU-bound equipment: "All Southern Machinery equipment is supplied with CE declaration of conformity and full documentation package for EU customs clearance"
- Lead with S-70LD odd-form inserter (NOT S3000 radial) for alarm/relay/connector-heavy products -- odd-form is the highest-labor, highest-defect manual bottleneck
- Use STF1001 Tube Feeder as the technical conversation opener for tube-pack components (connectors, relays) -- much softer entry than "buy a new machine"
- Mirror their language: local language for the WhatsApp hook, English for technical email
- State any unverified number as a range with explicit assumption
- Run a final verification pass against the "Verification Checklist" below

---

## §2 — dormant-customer-reactivation-brief (Legacy Skill Notes)

> This section documents the relationship between `dormant-customer-reactivation-brief` and this skill. The two skills are nearly identical in scope — both produce the 4-section KAM reactivation deliverable. `dormant-customer-reactivation-brief` was the earlier skill; `dormant-account-reactivation-ems` is the canonical continuation with additional case studies and corrections incorporated.

### Reverse-Flow Waybill Hook (from dormant-customer-reactivation-brief)
When the dormant customer previously shipped something TO you (sample, board for evaluation, part for repair), the waybill/shipping record is a **stronger reactivation hook than your own PO archive**:
- Search CRM / shared inbox archive for shipping records where customer is SENDER
- Note: date, contents description, weight, waybill number
- Open email with: "Our engineering team still has the [contents] you sent us on [date]. I wanted to circle back..."
- Especially useful for India/APAC where relationships often begin with sample evaluation
- Full CTDI India example at: `intl-b2b-market-intel-fallback/references/ctdi-india-apac-case.md`

### India / APAC Specific Patterns (from dormant-customer-reactivation-brief)
- THT is GROWING in India (counter to global SMT-only narrative) — lead with India-specific reasons
- CCTV/SMPS/power supply = 80% THT by component count
- India labor cost baseline: $4,500-5,500/operator/year fully-loaded (Bangalore Peenya, 2026)
- E-Waste Management Rules 2022 (revised 2024) + BIS certification = regulatory tailwind
- PLI scheme = capacity expansion tailwind
- WhatsApp in local language more common in India than Western markets
- Email subject should mention specific India numbers (e.g., "9% Bangalore THT wage rise in 2025")

### M2M Bulgaria Corrections (incorporated from dormant-customer-reactivation-brief, validated 2026-06-08)
- S3000 speed: NEVER quote 20,000 CPH in sales materials — real-world is 10,000-12,000 CPH
- Manufacturing model verification MANDATORY before pitching THT equipment
- EU market: ALWAYS add CE declaration + EU customs documentation clause
- Network-blocked countries: use Eurostat/ILO, never fabricate specific % without source
- S-70LD first for alarm/relay/connector-heavy products, not S3000
- Government subsidy claims require exact program name + eligibility link

For the archived dormant-customer-reactivation-brief full content, see `references/dormant-customer-reactivation-brief.md`.

## Verification Checklist

Before delivering the activation package, verify:

- [ ] All customer contact names are spelled correctly (cross-check email addresses)
- [ ] Every fact in Phase 1 is sourced (cite the URL or news source)
- [ ] ROI numbers use LOCAL labor cost, verified or stated as assumption range
- [ ] Email subject does NOT contain spam triggers (all caps, multiple exclamation marks, "FREE")
- [ ] WhatsApp message is under 120 words
- [ ] All 3 CTAs are concrete and actionable
- [ ] Language register matches the recipient's role (engineer = technical, buyer = ROI, GM = strategic)
- [ ] No fabricated specs -- if unsure of a model spec, say "we will select a suitable model from our catalog"
- [ ] The package is saved to MEMORY.md or referenced in the sales log for follow-up tracking

---

## Linked Skills & Resources

- `dormant-customer-reactivation-brief` -- nearly identical scope to this skill. Both produce the same 4-phase deliverable (market intel + gap analysis + whitepaper outline + outreach). The main difference: this skill includes the India/APAC reverse waybill pattern and Bulgaria/Eastern Europe network-blocked protocol. Consolidate into one skill in a future curation pass.
- `improved-pitch-ems-global-smt-line` -- for full line pitch AFTER reactivation succeeds
- `smthelp-knowledge-base` -- for exact product specs when writing the whitepaper
- `xiaoman-crm-wave-solder-prospecting` -- for finding regional prospect data from customs records
- `smt_market_intelligence` -- for the macro market trend component in Phase 1
- `smt_roi_calculator` -- for the payback math in Phase 2 (but always override labor cost with local data)
- `b2b-roi-one-pager` -- for generating the **1-page A4 PDF attachment** referenced in Phase 4 Email Draft "Optionally attach" line. Use when the reactivation email needs a visual asset for a senior procurement reader who won't click through an HTML link. The first validated output of this pairing is `S-70LD_WhiteGoods_Spain_OnePager_v2.pdf` for E.G.O. Appliance Controls S.L.U. (2026-06-05). **NOTE:** This skill generates 1-page A4 ROI one-pagers via Playwright + Chromium headless shell rendering. For multi-page (2-3 page) PDF proposals with full whitepaper content, write a custom HTML template using the same rendering pipeline and save as `/Users/jasonwu/Downloads/<Company>_<Country>_THTStrategyBrief_<Year>.pdf` — see `references/bulgaria-m2m-case-study.md` for the M2M Bulgaria 3-page brief example (saved at `/Users/jasonwu/Downloads/M2M_Bulgaria_THTStrategyBrief_2026.pdf`).

---

## Provenance & Update Log

- **2026-06-04** -- Initial creation, validated against Liteon Brazil / LITE-ON MOBILE INDUSTRIA E COMERCIO DE PLASTICOS LTDA (Jaime Quinco, Leandro Santos, Ademir Souza, Allen Perea, Jedson Silva, Ricardo Cavalcante). Historical purchase: Panasonic spare parts. Location: Manaus, Brazil. The 4-phase framework produced a complete reactivation package in a single session, including a 5-pain diagnosis, $120K-$180K Capex / 6-11 month payback calculation, and bilingual (PT/EN) outreach drafts.
- **2026-06-05** -- Validated against E.G.O. Appliance Controls S.L.U. (Lliçà de Vall, Barcelona, Spain) dormant engagement. Historical purchase: UIC Auto Insertion Spare Parts (PO 2018 + 2022). Output: full 4-phase reactivation package + the first validated ROI one-pager PDF (`S-70LD_WhiteGoods_Spain_OnePager_v2.pdf` at /Users/jasonwu/Downloads/). The one-pager generation workflow was extracted into the new `b2b-roi-one-pager` umbrella skill.
- **2026-06-08** -- Critical corrections from M2M Services Bulgaria engagement (Borislav Panchev, COO). 6 sub-agents produced independent reactivation packages; M4 Review Agent identified 7 systemic errors: (1) S3000 speed double-counting (20,000 CPH theoretical vs 12,000 CPH real-world), (2) fabricated/unverifiable Bulgaria labor cost data (13% YoY with no source), (3) false assumption M2M operates in-house SMT line (M2M is a brand company, may outsource 100% PCBA), (4) "PCB Loader/Unloader supplier" framing overstated SM's historical role ($16,400 peripheral order vs partnership), (5) missing CE certification mention for EU market, (6) WhatsApp hook too long (110 words vs 60-80 target), (7) government subsidy claim without source link. Post-review corrections incorporated into Pitfalls, Phase 1 (network-blocked countries protocol), Phase 2 (S3000 speed correction), Phase 3 (S-70LD-first for alarm/IoT products). Full case details: `references/bulgaria-m2m-case-study.md`.
