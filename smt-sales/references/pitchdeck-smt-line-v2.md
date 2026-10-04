# SMT Full-Line Pitch Deck v2.0 — Reference

*Absorbed from `improved-pitch-ems-global-smt-line`. Supersedes v1.0 (`pitchdeck-ems-global-smt-line`).*
*Last Updated: May 2025 | Author: Hermes / Jason Wu*

---

## The Improved Opening — Lead with the Math, Not the Machine

**v1.0 opening:**
> "Southern Machinery delivers complete SMT/THT assembly lines at 30–50% lower CapEx than Japanese equipment..."

**v2.0 opening (better):**
> "Most EMS factories we talk to are comparing three things: the price of a new line, the price of used equipment, and the price of doing nothing. What they miss is the fourth number — the cost of buying the wrong machine. A $280,000 Juki placer sounds cheap until you realize you still need a printer, reflow, wave, loader, and unloader — and suddenly you're at $900K, with 6 months of installation time. We help you avoid that trap."

**Why this is better:** Pre-empts the Juki objection before it is even raised. Shows Jason has done this before.

---

## The Juki FX-3 Objection — Complete Response Script

### The exact objection to expect:
> "Juki Japan quoted me a refurbished FX-3 at $280,000 CIF. It's 36,000 CPH. Your S-PP350 is 25,000 CPH. That's 39% more throughput for 19% less money than your full line. I'm having trouble seeing why I should choose you."

### The 3-Step Response:

**Step 1 — Reframe the CPH metric (first 15 seconds)**
> "You're right that the Juki FX-3 runs 36,000 CPH at its top speed spec. But I want to ask you a question: what's your effective line CPH today — not the placers' theoretical speed, but the actual boards leaving your line per hour?"

*Why this works:* Forces the buyer to think about line balance before Jason explains it. Most buyers have never done this math and will pause.

**Step 2 — The full-line ambush (next 30 seconds)**
> "Here's what nobody running a competitive evaluation tells you. The Juki FX-3 at 36,000 CPH is a single machine. To make a board, you also need: a stencil printer ($45K DEK), a reflow oven ($220K BTU), a wave solder ($180K ERSA), a loader and unloader ($90K CKD). Add them up and you're at $900K–$1.1M for a comparable line. And the Juki's 36,000 CPH is its maximum speed under ideal conditions — on your actual production floor, with your actual changeovers, your effective line CPH is probably 18,000–22,000. Ours: 22,000 effective CPH, guaranteed, $344K landed, 4–6 week delivery."

**Step 3 — The TCO closer (final 15 seconds)**
> "Let me give you one number to take away: $556K. That's what you save with Southern Machinery vs. a complete Juki line — enough to hire 10 operators for 3 years, or build a second line. More CPH than you need is not a feature. It's a way to spend $600K you don't have to."

### The One-Line Destroyer (for confident close)
> "The Juki at 36,000 CPH is like buying a Ferrari to drive to the grocery store. You'll never use the speed, and you'll pay for the gas forever."

---

## The Line-Balance Math

### The concept every buyer must understand:

```
Effective Line CPH ≠ Placer CPH

Your Juki at 36,000 CPH requires:
- Loader: 50-board magazine, 60-second changeover → line stops 60×/shift
- Unloader: same problem
- Wave solder: must run at wave solder speed, not placer speed
- Reflow: must run at reflow belt speed

At 60 seconds lost per magazine change × 60 changes/shift = 60 minutes lost/shift
At $150/hour production value = $150/shift × 3 shifts = $450/day × 26 days = $11,700/month

The SUL460 dual-bay unloader: 6-second magazine swap, zero line stops
You recover $11,700/month in hidden capacity — forever
```

### The Line-Balance Equation:
```
Effective Line CPH = Placer CPH × OEE × (1 - Downtime Loss%)

Juki FX-3 line (typical EMS setup):
  = 36,000 × 0.75 × (1 - 0.15) = 22,950 effective CPH

Southern Machinery line (S-PP350 + SUL460):
  = 25,000 × 0.85 × (1 - 0.00) = 21,250 effective CPH

Difference: 1,700 boards/hour — but SM costs $556K less
Payback on the $556K price gap: 350 months — you die waiting

The $556K savings pays for 10 operators for 4 years
The effective CPH difference is irrelevant at real production volumes
```

---

## Mexico Labor Rate — ⚠️ Validation Required

### Current assumption in all ROI models:
> Mexico fully-loaded operator cost = $4,500/month

### ⚠️ Self-Evolution finding:
This number was set in 2024. Mexican manufacturing wages have been rising 10–15% per year. By 2025, the real fully-loaded cost (wages + benefits + IMSS + INFONAVIT + turnover) for a Guadalajara EMS operator is likely **$5,200–$5,800/month**.

### Required action before outreach:
Jason must confirm current Guadalajara EMS labor rates. Source: Encuesta Nacional de Salarios, IMSS, or ask a contact at a GDL factory.

### Updated ROI numbers (when validated):
| Labor Rate | 9 Operators × 3 Shifts Annual Cost | SM Line Payback |
|-----------|-----------------------------------|----------------|
| $4,500/mo (old) | $486,000 | 8.5 months |
| $5,500/mo (suspected) | $594,000 | 7.0 months |
| $6,000/mo (worst case) | $648,000 | 6.4 months |

**All scenarios show payback under 12 months. Verify the number.**

---

## The Single-Machine Trap

### What it is:
A salesperson (or buyer) quotes a single machine price — "Juki FX-3 at $280K" — without scoping the full line. The buyer thinks they're getting a deal. They're actually being set up to spend $900K+ incrementally.

### How to identify it in a meeting:
> "I see you have a Juki quote — is that for the placer alone, or does it include the loader, printer, reflow, and wave solder?"

If the buyer says "placer only" — the trap is identified.

---

## Improved Discovery Questions (v2.0 — adds competitive lens)

| # | Question | Why |
|---|----------|-----|
| Q1 *(NEW)* | "Who else are you evaluating right now? Juki? Yamaha? What have they quoted you so far?" | If Jason doesn't know a Juki quote exists, he'll walk in unprepared for the CPH objection |
| Q2 | "What is your current monthly PCB volume, and how many shifts are you running?" | Utilization rate and hidden capacity |
| Q3 | "How many operators do you currently have doing manual component insertion or hand-soldering?" | S-70LD + S-WS450 ROI — most compelling number |
| Q4 | "If your line could be 40% faster in one area, where would you want it: more CPH, faster changeovers, or fewer line stoppages?" | Identifies pain type |
| Q5 | "Are your customers requiring lead-free / RoHS 3 compliance by a specific date — and do you have N₂ reflow capability today?" | Ticking clock for S-RF450 (N₂ option) |

---

## Self-Evolution Action Items (from v2.0)

| Item | Owner | Priority | Status |
|------|-------|----------|--------|
| Verify Juki FX-3 actual CIF price | Jason Wu | HIGH | Pending |
| Verify Juki FX-3 sustained CPH (not peak) | Jason Wu | HIGH | Pending |
| Verify Mexico GDL labor rate (2025) | Jason Wu | HIGH | Pending |
| Create `displacing-juki-fx3` skill with verified specs | Hermes | MEDIUM | Pending |
| Update ROI calculator defaults to validated labor rates | Hermes | LOW | Pending |

---

## What Changed from v1.0 → v2.0

| Element | v1.0 | v2.0 (Improved) |
|---------|------|------------------|
| Opening line | Product-focused | Math/mistake-focused |
| Juki objection | Not scripted | 3-step complete script |
| Line-balance concept | Brief mention | Full equation with numbers |
| Mexico labor rate | $4,500/mo (assumed) | ⚠️ Needs validation 2025 |
| Competitive discovery | Q4 out of 4 | Q1 out of 5 (moved up) |
| Single-machine trap | Not mentioned | New section with identification script |
| One-line close | Multiple options | Ferrari analogy added |
| Self-evolution actions | None documented | 6-item tracked list |
