---
name: smthelp-seo-content-generator
description: "Southern Machinery B2B SEO Content Generator — Weekly Friday 16:00 CST Cron Job. Generates multi-platform SEO diagnostics and 3 comprehensive blog content outlines per week for SMThelp.com, Alibaba, and MIC. Bridges SMT/THT industry topics to Southern Machinery equipment solutions with ROI calculations."
whenToUse: "SEO content generator，B2B blog outline，每周SEO报告，SEO诊断，cron_b2b_seo_content_generator，NEPCON Asia content"
metadata:
  source: hermes
  origin: "sales-engineering/smthelp-seo-content-generator"
---
# Southern Machinery B2B SEO Content Generator

**linked_files:** `references/seo-content-outlines-week27.md`, `references/seo-content-outlines-week28.md`, `references/seo-content-outlines-week29.md`, `references/seo-content-outlines-week30.md`, `references/pcba-cleaning-machines.md`

## Task Overview

**Schedule:** Weekly Friday 16:00 CST  
**Task ID:** `cron_b2b_seo_content_generator`  
**Inputs:** Southern Machinery product knowledge base, smthelp.com CMS state, previous week output  
**Output:** B2B multi-platform SEO diagnostics report + 3 blog content outlines

---

## Output Structure (Standard)

### Section 1: OPERATIONAL DIAGNOSTICS — B2B CHANNELS
Table with 3 columns: Platform | Health | Key Actions
Cover: Alibaba, MIC, SMThelp.com

### Section 2: HIGH-INTENT LONG-TAIL KEYWORD INTELLIGENCE
Table with 4 columns: Keyword Phrase | Search Intent | Competition | Target Page
Aim for 6-10 keywords per week. Focus on:
- Long-tail industrial keywords with purchase intent (e.g., "automatic odd-form insertion machine cost")
- Technical comparison queries (e.g., "lead-free wave soldering vs selective soldering yield")
- ROI/operational queries (e.g., "high-speed radial inserter setup time")

### Section 3: 3 BLOG CONTENT OUTLINES

Each outline follows this structure:

#### Outline Header
- **Primary Target Keyword:** [exact keyword phrase]
- **Secondary Keywords:** [2-3 supporting keywords]
- **Publication:** [platform priority order]
- **Linked Equipment:** [Southern Machinery model(s)]

#### I–VI Body
1. **HOOK** (150-200 words): Industry stat or pain point opening
2. **PROBLEM DEFINITION** (300-400 words): Technical problem anatomy
3. **TECHNICAL DEEP-DIVE** (400-600 words): Spec breakdown, comparison tables
4. **ROI CALCULATION WORKSHOP** (300-400 words): Formula block + worked example
5. **BRIDGE TO SOUTHERN MACHINERY** (150-200 words): Equipment integration, link to domain homepage
6. **CALL TO ACTION** (100-150 words): Lead-gen CTAs (download ROI calculator, schedule consultation, request sample test)

#### Image Requirements (per outline)
- [ ] **3D factory line layout with equipment highlighted (MANDATORY)**
- [ ] Machine product photo
- [ ] Infographic/chart (ROI comparison, yield comparison, timeline, etc.)
- [ ] Technical diagram or microsection where applicable

#### Internal Links
- Equipment product page(s)
- Downstream/upstream machines in the line
- Homepage CTA: `[www.SMThelp.com](http://www.SMThelp.com)`

### Section 4: SEO ENFORCEMENT CHECKLIST
Table: Requirement | Outline 1 | Outline 2 | Outline 3 | Status
All items must be ✅ across all outlines before submission.

### Section 5: PUBLICATION SCHEDULE
Table: Slot | Content | Target Platform | Status
3 rows (Week N, Week N+1, Week N+2)

### Section 6: PLATFORM CROSS-LINK MATRIX
Table: Source | Anchor Text | Target | Purpose
Maps all internal link placements across SMThelp.com, Alibaba, MIC.

---

## Format Requirements

| Rule | Enforcement |
|------|-------------|
| B2B, SMT, THT, ROI, MIC, EMS, ODM | **ALL UPPERCASE** |
| Equipment model numbers | Exact format from knowledge base (e.g., S-70LD, SUL460, SFY03) |
| Numbers and specs | Precise, pulled from knowledge base only |
| Homepage CTA | `[www.SMThelp.com](http://www.SMThelp.com)` |
| Target word count | ≥2,000 words per outline |
| 3D line layout | **MANDATORY** in every outline |
| ROI formula block | Required in every outline |
| Lead-gen CTA | Required in every outline |

---

## Data Sources

1. **smthelp-knowledge-base** — Product specs, pricing, competitive positioning
2. **smthelp-website-seo-workflow** — CMS state (listids, productids, blog section status)
3. **smthelp-daily-report references** — Week-over-week context
4. **Session history** — Previous SEO outline outputs (session_search)
5. **smthelp-image-hosting-workflow** — 3D factory line layout generation (run before each publish date, not during the report generation session)
6. **smthelp-brand-document-suite** — ROI calculator PDF/Excel creation (for pre-publication asset creation)

---

## Related Skills

- **smthelp-website-seo-workflow** — CMS product SEO optimization (separate workflow, different task)
- **smthelp-daily-report** — Sales engineer daily report (different schedule + structure)
- **smthelp-social-media-automation** — Social posting workflow (cross-links from blog content)
- **smthelp-image-hosting-workflow** — 3D factory layout image generation for blog content (pre-publication step)
- **smthelp-brand-document-suite** — ROI calculator and lead-gen asset creation (pre-publication step)
- **b2b-social-media** — Content strategy framework for LinkedIn/FB distribution

---

## Known Context

- SMThelp.com blog section: `listid=19280`, backend shows "THT Chatbots" (misleading name — actual = blog articles)
- Blog is not empty: 1 article published as of Week 27 (S-7000D Tact Switch Inserter, productid=137666)
- Blog has 2 remaining slots for Q2 publishing targets
- www.smthelp.com had an outage in June 2026 — monitor connectivity; fallback domain is www.3dsmt.com
- **NEPCON Asia 2026 (Aug 27-29, Shenzhen):** Full line live demo. Week 29-30 content should coordinate pre-show and post-show demand generation. Coordinate LinkedIn cross-posts with Jason Wu (linkedin.com/in/smtsupplier) for booth scheduling

## Rolling Content Calendar — Avoiding Topic Duplication

Track topics covered per week to prevent duplication. A rolling 6-week lookback is the minimum:

| Week | Primary Topic | Equipment | Status |
|------|-------------|-----------|--------|
| Week 27 | Active Clinching / AGV Board Handling / Line Commissioning | S-7900, SFY03, SUL460 | Covered |
| Week 28 | Radial Inserter Changeover / Wave vs Selective Soldering / AGV (DUPLICATE — do NOT repeat AGV) | S-3000, S-WS450 | AGV was duplicate |
| Week 29 | Odd-Form Changeover / PCBA Online Cleaning / LED Depaneling | S-70LD, SME6200, S-D601 | Current |
| Week 30+ | Reserved: S-320AT Lead Cutting, S-680A Stencil Cleaner, custom feeder | pending | Open |

**Topic duplication rule:** Before selecting keywords, run `session_search` on `smthelp-seo-content-generator` to confirm no identical or near-identical topic was published in the prior 4 weeks. AGV is already covered twice — do not reuse in Weeks 30-32 without a genuinely new angle (e.g., "AGV navigation in shared human-robot aisles" or "SFY03 + SUL460 line integration for automotive EMS").

## Pre-Publication Checklist (Standing Steps)

After generating the report, complete these before the next publishing cycle:

- [ ] **Site connectivity check** — verify smthelp.v5.viwolf.cn is live; if unreachable, use www.3dsmt.com fallback
- [ ] **Prior week upload verification** — confirm previous week's outlines were uploaded to CMS (`listid=19280`) before scheduling new content
- [ ] **ROI calculator creation** — each outline requires a downloadable ROI calculator (Excel/PDF). Create all 3 before the publish date. Host on `file.autoinsertion.com`
  - Outline 1: S-70LD Changeover ROI Calculator
  - Outline 2: PCBA Cleaning ROI Calculator
  - Outline 3: LED Depaneling ROI Calculator
- [ ] **3D line layout commissioning** — use `smthelp-image-hosting-workflow` to generate. Required per outline:
  - Outline 1: S-70LD + S-3000 + S-WS450 full THT line
  - Outline 2: SME6200 inline after S-WS450 wave solder
  - Outline 3: S-D601 in LED strip production flow
- [ ] **LinkedIn cross-post coordination** — for show-tied outlines, include direct booth booking link in the LinkedIn version
- [ ] **MIC certification badges** — verify ROHS/CE badges are displayed on any new equipment MIC pages before publishing

---

## Output Language
- **English** (B2B export-focused content, industrial audience)
- Chinese terms acceptable for localized Chinese market content (specify per outline)
- Hashtags: #SMT #PCBAssembly #ElectronicsManufacturing #EMS #THT #ROI

---

## Quality Gates

Before finalizing output, verify:
- [ ] Primary keyword appears in H1 title and first 100 words
- [ ] All 3 outlines have 3D factory layout listed as MANDATORY
- [ ] ROI formula block present in each outline with worked numbers
- [ ] Homepage CTA `[www.SMThelp.com](http://www.SMThelp.com)` in each outline
- [ ] Publication schedule covers 3 consecutive weeks
- [ ] Cross-link matrix covers all 3 platforms
- [ ] No spec fabricated — all numbers from knowledge base
