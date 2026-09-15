---
name: smt-sales
description: Southern Machinery SMT/THT equipment sales playbook — objection handling, product pitches, and trade optimization for global EMS/ODM clients.
tags: [SMT, EMS, THT, sales, objection-handling, ROI, global-trade]
---

# Southern Machinery Sales Playbook

Full-cycle sales guidance for Southern Machinery SMT/THT automation equipment targeting global EMS/ODM manufacturers. Covers product positioning, objection handling, tariff optimization, and competitive displacement.

## Submodules

### [Objection: Quality of Chinese Equipment](./objection-quality-cnequipment/)
Handles the #1 objection: Chinese equipment quality skepticism vs. Fuji/Yamaha/Panasonic.
- Feel-Felt-Found framework
- Technical spec comparisons (accuracy, MTBF, defect rates)
- CE certification, FAT protocol, 60-day acceptance period
- Displacement scripts vs. Japanese competitors
- Verification checklist

### [Objection: Tariff & Import Cost](./objection-tariff-optimization/)
Handles tariff, HTS code, and rules-of-origin objections for non-China EMS clients.
- Section 301 tariff math (25% on China equipment)
- HTS code reference table for all SM equipment
- SKD optimization (5-10% duty vs. 25%)
- IMMEX/Maquiladora strategy for Mexico
- Vietnam FTA eligibility (EVFTA, CPTPP, ASEAN)
- Landed cost vs. Japanese alternatives

### [Pitch: S-70LD Odd-Form Insertion Machine](./references/pitch-s70ld.md)
Flagship THT automation product pitch — specs, ROI calculators, competitive displacement.
- 30-second elevator pitch
- Key specifications table
- Perfect applications / NOT suitable for
- ROI calculator examples (Mexico, Vietnam)
- Competitive displacement vs. Panasonic/Universal
- Pilot order offer script
- BOM review checklist

### [Pitch: S3000 Radial Insertion Machine](./references/pitch-s3000.md)
High-speed THT radial inserter — 18,000 CPH peak, servo-driven clinch, dual-span 2.5/5.0mm.
- 30-second elevator pitch
- Key specifications (confirmed from smthelp.com, May 2026)
- Component spectrum (capacitors, transistors, LEDs, relays, connectors)
- Competitive displacement vs. Universal / Panasonic radial inserters
- ROI comparison: manual vs. S3000 auto (labor cost / PPM / payback)
- Full SMT line integration (S3000 → Wave Solder → AOI → Unloader)
- PPT template: 9-slide structure ready for re-use

### [Full SMT Line Pitch Deck v2.0](./references/pitchdeck-smt-line-v2.md)
Complete Feynman-level pitch for all 6 machines — S-SP500, S-PP350, S-RF450, S-WS450, SUL460, S-3500.
Covers the Juki FX-3 CPH objection response, line-balance math, Mexico labor rate validation, and the single-machine trap.
**Supersedes:** `pitchdeck-ems-global-smt-line` v1.0

### [7-Agent Sales Orchestration System](./references/7-agent-system.md)
Installing and operating Southern Machinery's 7 Hermes profiles (orchestrator + 6 specialists). Covers profile architecture, directory structure, multi-agent collaboration patterns, and 3 test cases. **Added June 2026.**

### [7-Agent Installation Fixes](./references/7-agent-install-fixes.md)
Critical installation troubleshooting discovered June 2026. Documents 4 must-apply fixes: (1) data directories provisioning script, (2) config.yaml model config, (3) distribution install duplicate-profile issue, (4) shell alias argument order. Includes verification commands and the provisioning script at `/Users/mac/.trade/fix_profiles.py`.

### [7-Day Meeting Sprint](./references/7day-sprint.md)
Execution sprint to book qualified EMS factory meetings within 7 days.
Covers 3 cold email templates, 5 discovery questions, Python ROI calculator, 13-slide PowerPoint outline, and day-by-day execution plan.
**Priority:** Meeting booked within 7 days.

## Shared Sales Framework

### Core Value Propositions (use across all products)
1. **CapEx Savings** — 30-50% vs. Fuji/Yamaha/Panasonic
2. **Fast Delivery** — 4-6 weeks vs. 6+ months for Japanese
3. **Labor ROI** — S-70LD pays back in 8-14 months via operator reduction

### 3 First Line Strategies (cold outreach)
1. **Problem Sniffing** — "I noticed your line is running [equipment brand]..."
2. **Billboard (Whole Offer)** — "We help EMS factories in Mexico cut SMT CapEx by 40%..."
3. **AI Generic** — "Quick question about {{company}}'s production setup..."

### Objection Handling Universal Rules
1. Never dismiss the competitor — show respect, then redirect to value gap
2. Always lead with pain, never with price
3. Reference clients are the #1 trust-builder — have 2+ ready per prospect vertical
4. Redirect to Total Cost of Ownership (TCO), never just CIF price

### Key Facts (Southern Machinery)
- **Founded:** 2011, Shenzhen China
- **Certifications:** CE certified, multiple patents
- **Flagship:** S-70LD odd-form insertion (3-25mm radial components)
- **Contact:** jasonwu@smthelp.com / +86-136-0256-2576 / WhatsApp/WeChat: jasonwuuic
