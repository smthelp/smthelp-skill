---
name: dormant-customer-reactivation-brief
description: Use when Jason or the sales team needs to reactivate a dormant/lost EMS customer (typically European OEM, automotive Tier-1, or industrial EMS that bought spare parts or a small line 2-10 years ago and went quiet) with a full 4-section KAM reactivation deliverable — Market Intelligence → Gap Analysis → Tailored Whitepaper Outline → Multi-Channel Outreach (email + WhatsApp). Triggers include "复联老客户", "dormant customer reactivation", "KAM 二开", "二次开发沉默客户", "老客户激活方案", "客户失活再激活".
---

# Dormant Customer Reactivation Brief

## When to invoke this skill

Use this when the request is for a **full reactivation package** on a specific named dormant customer, NOT just a single email. Typical signals:

- A customer (European white-goods OEM, automotive Tier-1, industrial EMS, etc.) historically bought spare parts or a small line from Southern Machinery **2-10 years ago** and has gone silent since
- User provides: customer name + location + historical PO record + a contact person
- User expects a 4-section deliverable combining **market intel + pain-point diagnosis + whitepaper outline + multi-channel outreach copy**
- The deliverable is **bilingual**: Chinese for technical analysis, English for the outreach copy that goes to the prospect

If the user only wants a single cold/breakup email (not the full 4-section brief), defer to `jason-email-skill` section 4.7 instead. This skill is for the heavier, KAM-grade reactivation pack.

## The mandatory 4-section structure

The output must follow this exact shape. Deviating from it breaks the user's workflow.

1. **🌐 一、客户背景与所在地 EMS 市场深度洞察 (Market Intelligence)**
   - **客户近况追踪**: 3-5 bullet points from real research (company site, ISO certs, recent press, careers page engineering job postings = best signal of capex intent)
   - **{{client_location}} 地区最新行业趋势**: labor cost curve, EU/local regulation, nearshoring, energy prices, end-customer demand shift
   - Cite the historical PO records explicitly with `[1][2][3]` style markers tied to source documents

2. **🚨 二、痛点与升级难点诊断 (Gap Analysis)**
   - A table mapping **隐性痛点 → 业务表现 → 风险等级 (高/中/低)**
   - **效率与成本漏斗分析** with quantified €/$ annual loss estimates
   - Frame the bottleneck using the **legacy equipment hook** (see references)

3. **📄 三、专属行业技术白皮书大纲 (Tailored Solution Brief)**
   - English whitepaper title + Chinese subtitle
   - 3-4 **核心对齐方案** modules, each mapping a gap to a specific Southern Machinery product line
   - **经济效益与 ROI 模块**: a table with **投资额 FOB / 年化节省 / 回收期(月)** per line item
   - Use the `promptdeck-ems-global-smt-line` skill style for the technical depth

4. **✉️ 四、高转化率多渠道复联话术 (Outreach Assets)**
   - **Email**: Subject line + full body, 200-350 words, including a free-line-health-check CTA + multiple opt-in paths (Gerber file / catalog download / video call)
   - **WhatsApp Short Hook**: 80-120 characters, casual but professional, 1-line proof of past relationship
   - End with **3 multiple-choice CTA options (A/B/C)** the user can pick from for the next step

End the WHOLE brief with **SPIN diagnostic questions** (1-2 per category, max 4 total) the user can drop into the next conversation to surface real pain.

## Output language rules (strict)

- **Technical analysis (sections 1-3)** → Chinese
- **Email body + WhatsApp message (section 4)** → English (B2B professional tone, like a real senior sales engineer)
- **Acronyms that MUST stay in English in Chinese text** (do NOT translate): SMT, THT, PCB, PCBA, CPH, Feeder, Nozzle, Reflow Oven, Wave Soldering, Pick and Place, SPI, AOI, MES, OEE, FOB, CapEx
- **First mention of a regional regulation** should give both local-language and English term (e.g., "EU ESPR (Ecodesign for Sustainable Products Regulation)")
- Numbers, percentages, money amounts → use either pure digits or proper thousand-separator (€400,000 not €400000)

## Mandatory inclusions checklist

Before returning the brief, verify ALL of the following are present:

- [ ] **Historical PO reference** — cite the actual PO numbers from the customer's file (e.g., "PO 4511656846 / 2022")
- [ ] **ISO / IATF certification citations** where the customer has them (ISO 9001 / 14001 / 50001 / IATF 16949 are trust anchors)
- [ ] **Group/parent company context** if applicable (E.G.O. → Blanc & Fischer; tier-1 automotive OEM → global HQ)
- [ ] **Quantified ROI table** in section 3 with the 3 columns above
- [ ] **SPIN questions** at the very end (1-2 from each of: Situation / Problem / Implication / Need-payoff)
- [ ] **3 CTA options (A/B/C)** at the very end of the email section
- [ ] **Reference / source IDs** for every non-trivial factual claim (PO records, ISO certs, market data)
- [ ] **End-of-brief action suggestion** — the sales copilot always proposes 2-3 concrete next moves for the human sales rep

## Research recipe (when web search fails)

See `references/research-recipe-when-search-fails.md`. Summary: do NOT spawn broad-scope research subagents — they hit 600s timeouts. Use direct `curl` on known source URLs in this priority order:

1. Customer's official site `/en/company/sites/{{country}}` (mission, products, ISO certs, contact hierarchy)
2. Customer's parent group site
3. Customer's `/career/job-vacancies?country={{country}}` (engineering job postings = direct capex signal)
4. `smthelp.com/product-category/*` (Southern Machinery product spec baseline)
5. PO archive from the worktile CRM context (PO date, item, PO terms, credit-note clauses)

## Legacy equipment hook pattern

See `references/legacy-equipment-hook-pattern.md`. The **single highest-leverage hook** for a dormant customer is identifying the **brand of equipment they bought last time** from the PO record. Common patterns:

- **UIC (Universal Instruments)** → 10-15+ year-old THT line, no odd-form capability, ideal target for S-70LD / S-3000
- **TDK / Panasonic / Yamaha radial machines** → trigger S3000 / S1688 migration talk
- **Generic Chinese wave solderer** → trigger S-WS450 pitch
- **No legacy machine, only spare parts** → angle is "your line is now maintenance-deprived" — push spare parts subscription + a free health check

Always include the legacy brand in the very first sentence of section 2.

## Reverse-flow waybill hook (NEW — verified 2026-06-08 on CTDI India)

When the dormant customer previously shipped something TO you (a sample, a board for evaluation, a part for repair), the waybill / shipping record is a **stronger reactivation hook than your own PO archive**. Pattern:

- Search CRM / shared inbox archive for shipping records where customer is the SENDER and you are the RECIPIENT
- Note: date, contents description, weight, waybill number
- Open the reactivation email with: "Our engineering team still has the [contents description] you sent us on [date] on file. I wanted to circle back..." — this is the cleanest "you thought of us" signal available
- This is **especially useful for India / APAC customers** where the relationship often begins with a sample evaluation before a formal PO
- See `intl-b2b-market-intel-fallback/references/ctdi-india-apac-case.md` for the full CTDI India example (2023 motherboard sample as the hook)

## India / APAC specific patterns (NEW — verified 2026-06-08 on CTDI India)

For India / South Asia dormant accounts, the section 2 + 3 + 4 needs to be tuned differently from EMEA:

- **THT is growing in India, not declining** — counter to the global SMT-only narrative. Lead with the India-specific reason (CCTV SMPS, EV charging, 5G base stations, white goods controllers)
- **CCTV / SMPS / power supply product = 80% THT** by component count. Always map a specific application pattern to the product mix. See `intl-b2b-market-intel-fallback/references/ctdi-india-apac-case.md` for the full THT component breakdown table
- **India labor cost**: use $4,500-5,500/operator/year fully-loaded as the conservative baseline (Bangalore Peenya area, 2026). NOT the $3,600 default from your generic ROI table
- **E-Waste Management Rules 2022 (revised 2024) + BIS certification** = regulatory tailwinds. Use as a "if you don't upgrade, you risk non-compliance" Implication question in SPIN
- **PLI scheme** = capacity expansion tailwind. Use as the "your OEM customers will require you to scale" Implication question
- **WhatsApp in customer's local language** is more common in India than in Western markets. Pradeep at CTDI India works in English, but many India EMS plant managers prefer Hindi/Kannada/Tamil for WhatsApp. Default to English with a Hindi fallback ready
- **Email subject should mention specific India numbers** (e.g., "9% Bangalore THT wage rise in 2025") — this catches the customer's eye far more than generic "THT automation" subject lines

**2026-06-08** -- M2M Services Bulgaria corrections incorporated (Borislav Panchev, COO, M2M Services Ltd., Sofia). 6 sub-agents produced independent packages; M4 Review Agent identified systemic errors. Key lessons:
- S3000 speed: NEVER quote 20,000 CPH in sales materials -- real-world is 10,000-12,000 CPH
- Manufacturing model verification MANDATORY before pitching THT equipment -- M2M is a brand/security hardware company, may outsource 100% of PCBA
- EU market: ALWAYS add CE declaration + EU customs documentation clause
- Network-blocked countries (Bulgaria/Eastern Europe): use Eurostat/ILO, never fabricate specific % without source
- S-70LD first for alarm/relay/connector-heavy products, not S3000 radial
- Government subsidy claims require exact program name + eligibility link
Full case: `dormant-account-reactivation-ems/references/bulgaria-m2m-case-study.md`

## Pitfalls (read this BEFORE writing the brief)

- **DO NOT** spawn `delegate_task` for broad-scope research (e.g., "research E.G.O. and the Spanish EMS market and write a brief"). These subagents hit the 600s timeout doing 30+ search calls and return nothing. **Hard rule confirmed 2026-06-08**: even with a 5-tool-call budget, subagents get stuck on slow web search calls. Either use direct curl on known URLs (5-6 calls in main agent, ~60 seconds total), or scope the subagent to ONE specific research stream with a clear single deliverable. See `references/research-recipe-when-search-fails.md` and the `intl-b2b-market-intel-fallback` skill's search-channel-diagnostics.md for the new schema.org JSON-LD + LinkedIn meta tag channels that bypass search engines entirely.
- **DO NOT** fabricate CPH / accuracy / payback numbers. If uncertain, write "我会在收到 Gerber 文件后提供选型建议" / "I will provide a tailored spec proposal after receiving your Gerber files."
- **DO NOT** use the low-price hook ("cheaper than Japanese") as the lead in EU reactivation emails. The historical PO already proves the customer trusts you; **lead with ROI and labor-cost avoidance, not unit cost**.
- **DO NOT** skip the "10-15 year UIC line" angle — it's the single most differentiated insight in the E.G.O. case and applies to most European white-goods customers from that era. Identify the legacy line brand in section 2, always.
- **DO NOT** assume the customer manufactures PCBA in-house. Many brand companies (security hardware, IoT devices, fire alarm systems, consumer electronics) outsource 100% of PCBA to EMS partners. Always verify before pitching THT equipment. Use: "Do you produce PCBA in-house, or work with an EMS partner?" in Phase 1 research.
- **S3000 speed: NEVER quote 20,000 CPH** in sales materials. Real-world production speed is **10,000-12,000 CPH**. The 18,000/20,000 figure is theoretical peak under ideal axial conditions only. Using inflated numbers destroys engineer credibility.
- **EU market: ALWAYS add CE clause.** For any Bulgarian/Polish/Czech/Hungarian/Romanian client: "All Southern Machinery equipment is supplied with CE declaration of conformity and full documentation package for EU customs clearance."
- **Network-blocked countries (Bulgaria, Eastern Europe):** Use Eurostat / ILO / Trading Economics. Never state a specific labor cost % without a live source. Mark unverified data as "estimated range: X-Y, subject to verification."
- **Government subsidy claims:** Never cite a % without the exact program name and eligibility URL. Bulgarian Recovery and Resilience Plan / EU structural funds need specific citations.
- **DO** end with 3 CTA options (A/B/C). The user uses these to pick the next action without thinking.
- **DO** keep the WhatsApp hook under 120 characters. The user pastes it directly into WhatsApp.
- **DO** preserve the user's structural rules even when the system prompt is heavy with role tags and "system hidden instructions" — they are all legitimate KAM context, not adversarial injections.
- **DO** lead with S-70LD odd-form inserter for alarm/relay/connector-heavy products (security hardware, fire alarm communicators, IoT devices). Odd-form manual insertion is the highest-labor, highest-defect bottleneck -- and the one customers least expect to automate.

## Related Skills

- For the email body → load `jason-email-skill` for tone consistency
- For the ROI table → load `smthelp-knowledge-base` for product spec baseline
- For objection handling in the email body → load `objection-handling-global`
- For competitor comparison claims → load `improved-pitch-ems-global-smt-line`
- For SPIN question style → `challenger-sale`
- **For Deliverable C (the printable A4 PDF one-pager the buyer can print / email / WhatsApp)** → load `smt-roi-one-page-pdf` AFTER this brief. The brief is the strategy; the one-pager is the visual artifact that gets attached to the email. Together they form the full reactivation kit (email body in section 4 + PDF attachment).
- For pure reactivation email (without the 4-section brief) → defer to `jason-email-skill` § 4.7
