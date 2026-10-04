---
name: smt-edm-campaign
description: >
  EDM (Email Direct Marketing) campaign skill for Southern Machinery SMT/THT 
  equipment foreign trade. Combines coldoutboundskills methodology with SMT/EMS 
  industry expertise to run full-cycle outbound campaigns targeting EMS/ODM manufacturers
  in Mexico, Vietnam, India, Europe and other growth markets.
  
  Use when: Jason says "start EDM campaign", "run email campaign", "send batch",
  "target [market]", "write email template for [country]", "onboard new ICP".
  For personalized 1:1 replies, inbox triage, meeting booking, and quote drafting,
  use `jason-personal-email` instead (it has Jason's authentic voice + 8 modules).
  Prerequisites: himalaya configured with 6 sending accounts.
  Primary sending account: jasonwu@smthelp.com (smtp.exmail.qq.com:465 SSL ✅).
  Other accounts (IMAP only — SMTP blocked on this machine): sale@3dsmt.com,
  service@3dsmt.com, info@3dsmt.com, support@3dsmt.com, info@smthelp.eu.
  ⚠️ NOTE: 3dsmt.com series SMTP is blocked by network (port 465/587 outbound
  is unreachable). ALL actual sends must use jasonwu@smthelp.com via smtp.exmail.qq.com.
category: sales
tags: [SMT, EMS, EDM, cold-email, B2B-manufacturing, outbound]
---

# SMT-EDM Campaign Skill

End-to-end cold email campaign system for Southern Machinery SMT/THT automation equipment targeting global EMS/ODM manufacturers.

**Built on:** coldoutboundskills methodology (GrowthEngineX) + Southern Machinery product knowledge  
**Sending infrastructure:** himalaya CLI + 5 configured SMTP accounts  
**Target market:** EMS/ODM factories in Mexico, Vietnam, India, Europe, and emerging manufacturing hubs

---

## Workflow Overview

```
ICP Definition → Market Segmentation → Template Selection → 
Personalization → Batch Send (himalaya) → Reply Handling → Follow-up
```

### ICP: Who We Target

**Hard Filters:**
- Job titles: Production Manager, SMT Manager, Operations Director, Plant Manager, 
  Procurement Manager, Engineering Manager, CEO/Owner
- Industries: Electronics Manufacturing Services (EMS), OEM/ODM, Contract Manufacturers
- Company size: 50-5,000 employees (mid-market focus)
- Geography: Mexico, Vietnam, India, Europe, Southeast Asia

**Soft Filters (prioritization):**
- Recently expanded production capacity
- Running aging Japanese equipment (Fuji, Yamaha, Panasonic)
- Labor cost pressures / high turnover
- Customers in automotive, industrial, or consumer electronics
- Newfactory setup / line transfer from Asia

**Red Flags (exclude):**
- Competitors already selling SMT equipment
- Companies already running Southern Machinery equipment (existing customers)
- Companies with HQ in Shenzhen/Dongguan/China (domestic market)

---

## Market Segment Templates

| Market | Core Pain | Primary CTA | Angle |
|--------|-----------|-------------|-------|
| Mexico Automotive EMS | Legacy Japanese lines, USMCA compliance | 10-min line assessment | Nearshore CapEx savings + local support |
| Vietnam Electronics | Rising labor costs, speed to market | Free automation ROI analysis | China+1 diversification + fast delivery |
| India Manufacturing | High custom duty on equipment, localization | Government scheme compliance guide | FDI-friendly + 30-50% CapEx reduction |
| Europe Industrial | ESG/sustainability, energy efficiency | Green manufacturing audit | CE certification + energy savings |
| Southeast Asia EMS | Competitive pricing, aftersales support | Competitive quote comparison | Total cost of ownership analysis |

---

## 4-Step Email Sequence (Standard)

| Day | Step | Subject Strategy | Goal |
|-----|------|-----------------|------|
| Day 0 | Email 1 | Problem-pain / ROI billboard | Hook + awareness |
| Day 3 | Email 2 | Threaded follow-up (no subject) | Persistence signal |
| Day 7 | Email 3 | New thread, case study angle | Social proof |
| Day 14 | Email 4 | Breakup email / final offer | Urgency + unsubscribe signal |

**Standard constraints:**
- 50-90 words per email (extend to 125 only with strong AI personalization)
- Single CTA per email
- 3:1 ratio (them:us sentences)
- No em dashes (—), no ALL CAPS, no excessive punctuation!!!
- Personalization variables: `{{first_name}}`, `{{company}}`, `{{city}}`, `{{product_line}}`, `{{pain_point}}`

---

## Sending Infrastructure

### 5 Configured Accounts (himalaya)

```
sale@3dsmt.com      ← Default (primary campaigns)
service@3dsmt.com   ← Service/technical follow-ups  
info@3dsmt.com      ← Info/lead magnet campaigns
support@3dsmt.com   ← Support-focused outreach
info@smthelp.eu     ← Europe-specific campaigns
```

### How to Send

**Send via default account (sale@3dsmt.com currently):**
```bash
cat << 'EOF' | himalaya template send
From: sale@3dsmt.com
To: {{recipient}}
Subject: {{subject}}

{{body}}
EOF
```

**Switch active sending account** by editing `~/.config/himalaya/config.toml` 
and changing `default = true` to the desired account, then re-run.

**Batch send (rotate accounts manually between batches):**
```bash
# Step 1: Set default = true for sale_3dsmt in config.toml, then send batch 1
# Step 2: Change default = true to service_3dsmt, send batch 2
# Step 3: Change to info_3dsmt, etc.
```

### Available Accounts

> **Note on multi-account sending:** himalaya v1.2.0 doesn't support `--account` globally. 
> For batch sending across multiple accounts, use separate config files:
> ```bash
> # Create per-account configs
> himalaya account list  # verify all 5 accounts exist
> himalaya -c ~/.config/himalaya/config.toml --account sale_3dsmt envelope list
> ```
> Actually, since v1.2.0 doesn't support `--account`, the workaround is to change 
> `default = true` in the config.toml to switch active sending account, OR use separate 
> config files per account and specify with `-c /path/to/config.toml`.
>
> **Recommended approach for batch rotation:**
> - Run each account's send in separate terminal sessions  
> - Change `default = true` to the next account between batches
> - Or maintain `config-sale.toml`, `config-service.toml`, etc.

- **Week 1-2 warmup:** Send max 10 emails/day/account from sale@3dsmt.com only
- **Week 3-4:** Scale to 20 emails/day/account across 2 accounts
- **Week 5+:** Full rotation across all 5 accounts, 30 emails/day/account max
- **Golden rule:** Never exceed 30 emails/day/inbox — this is the #1 deliverability safeguard

---

## Step-by-Step Campaign Execution

### Step 1: Define ICP and Market Segment

Ask the user:
1. Which market? (Mexico / Vietnam / India / Europe / Other)
2. Target job title? (SMT Manager / Operations / Procurement / CEO)
3. Any specific product focus? (SMT line / THT insertion / Wave soldering / full line)
4. Campaign goal? (Generate quotes / Book demo / Get meeting)

### Step 2: Select Template

Load the appropriate template from `templates/`:
- `cold_email_mexico_ems.md` — Mexico automotive EMS (default)
- `cold_email_vietnam_ems.md` — Vietnam electronics
- `cold_email_india_ems.md` — India manufacturing
- `cold_email_europe_ems.md` — Europe industrial
- `follow_up_sequence.md` — Day 3/7/14 follow-ups

### Step 3: Personalize with AI Variables

Before sending, inject personalization:
- `{{first_name}}` — Contact's first name
- `{{company}}` — Company name
- `{{city}}` / `{{country}}` — Location
- `{{product_line}}` — Relevant equipment (S-70LD, SUL460, etc.)
- `{{pain_point}}` — Market-specific pain (labor cost, legacy lines, etc.)

**For high-value targets:** Run auto-research to find specific details 
(annual revenue, recent expansion news, current equipment brands).

### Step 4: Verify Lead List Quality

Use list-quality checklist before any batch send:
- [ ] No role-based emails (info@, support@, admin@ — these are not people)
- [ ] No duplicates
- [ ] Country/region filter applied correctly
- [ ] Competitor domains excluded
- [ ] Existing customer domains excluded
- [ ] Bounced/unsubscribed suppressed

### Step 5: Execute Batch Send

```bash
# Send test to self first
cat << 'EOF' | himalaya --account sale_3dsmt template send
From: sale@3dsmt.com
To: jasonwu@smthelp.com
Subject: [TEST] Mexico EMS Campaign - CapEx Reduction

Hi Jason,
This is a test email from our EDM campaign system.
Best,
Jason Wu | Southern Machinery
EOF
```

After test approval, send in batches of 15 per account per day.

### Step 6: Monitor Reply Handling

**Positive reply (wants to talk):** Reply within 30 seconds, hand off to Jason Wu via WhatsApp
**Negative/hostile reply:** Log and suppress from future campaigns  
**OOO (out of office):** Add to re-engagement list in 30 days  
**Bounce:** Remove from list immediately, investigate (wrong email / company closed)

---

## Core Copywriting Principles (from campaign-copywriting)

### 3 Value Angles
1. **Save Money** — 30-50% CapEx reduction vs. Japanese equipment
2. **Save Time** — Faster delivery (4-6 weeks vs. 6+ months), reduced setup time
3. **Make Money** — Higher OEE, better quality yield, ability to take on more complex work

### 3 First Line Strategies
1. **Problem Sniffing** — "I noticed your line is running [equipment brand]..."
2. **Billboard (Whole Offer)** — "We help EMS factories in Mexico cut SMT CapEx by 40%..."
3. **AI Generic** — "Quick question about {{company}}'s production setup..."

### What Good SMT Cold Email Looks Like

```
Subject: [Company] + 40% SMT CapEx cut — valid?

Hi {{first_name}},

With {{company}} ramping up automotive electronics production, 
you're likely evaluating how to modernize without blowing the CapEx budget.

Most mid-size EMS factories we work with are running a mix of aging 
Fuji and Yamaha lines — high maintenance, long lead times for parts, 
and support that can't visit without 2 weeks notice.

Our S-70LD odd-form insertion machine handles radial components 
(3-25mm) at 0.8s placement accuracy — replacing the manual 
insertion that's eating {{company}}'s labor budget.

Would a 10-minute remote walkthrough of your current line setup work 
this Thursday?

Best,
Jason Wu
CEO & Chief Sales Engineer | Southern Machinery
+86-136-0256-2576 | jasonwu@smthelp.com | smthelp.com
```

### QA Checklist (before every send)
- [ ] No em dashes (—) — Gmail flags these
- [ ] No ALL CAPS
- [ ] Word count: 50-90 (125 max)
- [ ] Single clear CTA
- [ ] Personalization variables resolved (no `{{unsolved}}` vars)
- [ ] From name: "Jason Wu" not "Sales Team"
- [ ] Physical address included (CAN-SPAM compliance)
- [ ] Test email sent to self first

---

## Common Objections + Responses

### "Your equipment quality is not as good as Japanese brands"
> "I understand the concern — it's the first thing most buyers ask. 
> What we've found is that for 80% of SMT applications, the gap is 
> imperceptible in actual production output, while the CapEx 
> difference is very perceptible. Which product line are you currently running?"

### "Juki / Yamaha is faster / has higher CPH" (⚠️ Most Dangerous Objection)
> "You're right that the Juki FX-3 runs 36,000 CPH. But let me ask: 
> what's your effective line CPH — not the placer's theoretical speed, 
> but the boards actually leaving your line per hour? The Juki quote 
> is for the placer alone. Add the loader, printer, reflow, wave, 
> unloader — you're at $900K+, not $280K. We give you 22,000 
> effective line CPH in a complete $344K line. More CPH than you 
> can use is not a selling point — it's a $600K overpayment."

### "We tried Chinese equipment before and it failed"
> "I understand — there are a lot of low-quality players in the market. 
> The difference is in the support infrastructure. We have dedicated 
> field engineers and 7×24 remote support. Would a 30-day OEE 
> performance guarantee help mitigate that concern?"

### "We don't have budget right now"
> "Totally understand — CapEx cycles can be long. Would it help 
> if I put together a rough ROI model so you have it ready 
> when the next budget window opens?"

---

## Key Southern Machinery Facts (for personalization)

- **Founded:** 2011, Shenzhen China
- **Core products:** SMT full-line solutions (Loader, Printer, Pick&Place, Reflow, AOI), 
  THT auto-insertion (S-70LD flagship), wave soldering (S-WS450), board handling (SUL460)
- **Certifications:** CE certified, multiple invention/utility model patents
- **Competitive advantage:** 30-50% CapEx savings vs. Fuji/Yamaha/Panasonic, 
  4-week fast delivery for custom equipment, global field engineer network
- **Flagship:** S-70LD odd-form insertion machine (3-25mm radial components)
- **Contact:** jasonwu@smthelp.com / +86-136-0256-2576 / WhatsApp/WeChat: jasonwuuic

---

## Legal Compliance

- **CAN-SPAM:** Include physical address (Southern Machinery, Shenzhen, China), 
  opt-out mechanism, truthful subject lines
- **GDPR (EU leads):** Only contact B2B addresses, legitimate interest basis, 
  include unsubscribe link
- **General rule:** Never email consumers, honor unsubscribes immediately, 
  include real physical address

---

## Related Skills

- `smt-marketing-campaign` — higher-level campaign orchestration
- `himalaya` — email CLI reference for send/read operations

---

## Files

- `templates/` — Market-specific email templates
- `references/` — ICP guide, copywriting framework, sequence structure, deliverability guide
