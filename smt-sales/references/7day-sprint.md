# 7-Day Meeting Sprint — Reference

*Absorbed from `ems-global-7day-sprint`. Execution-focused sprint to book qualified EMS factory meetings within 7 days.*
*Last Updated: May 2025 | Author: Hermes / Jason Wu*

---

## 3 Cold Email Templates

### Email 1 — Subject: `{{company}} + 40% SMT CapEx cut — honest question`

```
Hi {{first_name}},

With {{company}} running aging SMT lines, you're likely watching two
numbers move in the wrong direction: labor costs up, and OEE down.

We work specifically with EMS factories in Mexico and Vietnam replacing
manual THT insertion — the 8–10 operators per shift that cost
$400K–$500K/year in labor. Our S-70LD odd-form inserter handles
radial components 3-25mm automatically, and our clients typically
see payback in under 14 months.

One question: is manual THT insertion still a line item in your
labor budget, or has it become a bottleneck?

Happy to share a quick ROI model built for Mexican EMS labor rates —
takes 15 minutes, no obligation.

Best,
Jason Wu
CEO & Chief Sales Engineer | Southern Machinery
+86-136-0256-2576 | WhatsApp: jasonwuuic | smthelp.com
```

### Email 2 — Subject: `Quick numbers for {{company}} — SMT labor cost`

```
Hi {{first_name}},

Doing quick math on something. If {{company}} is running 3 shifts
of manual THT operators at Mexican labor rates, that's roughly
$130K–$150K per operator per year fully loaded.

Our S-70LD inserter replaces that entire operation with one machine.
For an EMS in Guadalajara running our line, the typical picture:
- 9 manual THT operators replaced: $486K/year saved
- Landed cost of S-70LD + S-WS450 wave solder: $162K
- Payback: 4 months

Most factories we talk to didn't realize the payback was that fast.
What does your current THT operation cost per year?

Jason Wu
Southern Machinery | +86-136-0256-2576 | jasonwuuic
```

### Email 3 — Subject: `{{company}} — what a full SMT line actually costs vs. Japanese`

```
Hi {{first_name}},

One thing we see consistently with mid-size EMS factories in Mexico:
the assumption that Japanese equipment is the only reliable option.

The actual math tells a different story. A complete Southern
Machinery SMT/Wave line — printer, placer, reflow, wave solder,
loader, unloader — costs $344K CIF Guadalajara, landed.
That includes 25% Section 301 tariff.

A comparable Japanese line starts at $900K CIF.

The factories winning on this number aren't choosing Chinese equipment
over Japanese quality. They're choosing a real ROI calculation:
18-month payback vs. 4–6 years, full CE certification, and 7×24
remote support.

Can we schedule 20 minutes this week to walk through your current
capacity gap?

Jason Wu
Southern Machinery | jasonwu@smthelp.com | +86-136-0256-2576
```

---

## Discovery Call — The Critical Five Questions

| # | Question | Why |
|---|----------|-----|
| Q1 | "What is your current monthly PCB volume, and how many shifts are you running?" | Utilization rate and hidden capacity |
| Q2 | "If your line could run 40% faster in one area — where would you want that speed: more CPH, faster changeovers, or fewer line stoppages?" | Identifies pain type |
| Q3 | "How many operators do you currently have doing manual component insertion or hand-soldering?" | S-70LD + S-WS450 ROI — most compelling number |
| Q4 | "What are your smallest components — are you running 0201 packages or finer?" | S-PP350's 0201 capability differentiating |
| Q5 | "Are your customers asking you to be RoHS 3 / lead-free compliant by a specific date?" | Ticking clock for S-RF450 (N₂ option) |

---

## Meeting Booking Protocol

When a prospect replies positively:
1. **Reply within 2 hours** during business hours (China: 8am–10pm)
2. **Offer 2 specific time slots** — never "when are you free?"
   - "Are you free Thursday 3pm China time / 2am Mexico time, or Friday 10am China time?"
3. **Confirm video platform** — WhatsApp video, Zoom, or Google Meet
4. **Send calendar invite immediately** with agenda:
   - 5 min: {{Company}} situation understanding
   - 10 min: ROI numbers for {{Company}} specific numbers
   - 5 min: Q&A and next steps
5. **Send pre-call questionnaire** (discovery questions above) — ask them to fill it in before the call

---

## 7-Day Execution Plan

### Days 1–2: Prospect Research & List Build
- Build list of 50 EMS factories in target region (Apollo.io / LinkedIn Sales Nav)
- Filter: 100–1000 employees, SMT/PCB assembly, non-Shenzhen HQ
- Identify: decision-maker name, title, LinkedIn, email, WhatsApp
- Priority: 20 high-intent prospects (recent expansion, new contracts, aging equipment)

### Days 2–3: Email Send — Batch 1
- Send Email 1 to 20 high-priority prospects
- Use `{{first_name}}`, `{{company}}`, `{{pain_point}}` personalization
- CC Jason Wu's WhatsApp for any immediate replies
- Max: 10 emails/day (avoid spam triggers)

### Days 3–4: Follow-Up — Batch 2 + LinkedIn
- Day-3 follow-up Email 2 to non-responders from Batch 1
- Send LinkedIn connection request to 15 new prospects
- WhatsApp message to 5 highest-priority prospects (if mobile available)

### Days 5–6: Closing Outreach — Final Push
- Day-7 follow-up Email 3 to remaining non-responders
- For warm leads: send ROI calculator output (PDF)
- Book any discovery calls received

### Day 7: Review & Pipeline Update
- Count: emails sent, open rate, reply rate, meetings booked
- Classify all prospects: Stage 0→1→2→3
- Identify top 5 pipeline opportunities for Week 2

---

## ICP: Who to Target

**Hard Filters:**
- Job titles: Production Manager, SMT Manager, Operations Director, Plant Manager, Procurement Manager, Engineering Manager, CEO/Owner
- Industries: EMS, OEM/ODM, Contract Manufacturers
- Company size: 50–5,000 employees (mid-market focus)
- Geography: Mexico, Vietnam, India, Europe

**Soft Filters (prioritization):**
- Running aging Japanese equipment (Fuji, Yamaha, Panasonic)
- Labor cost pressures / high turnover
- Customers in automotive, industrial, or consumer electronics

**Red Flags (exclude):**
- Competitors selling SMT equipment
- Companies already running Southern Machinery (existing customers)
- Companies with HQ in Shenzhen/Dongguan/China

---

## Python ROI Calculator

**File:** `~/smt_roi_calculator.py`
**Usage:** `python3 ~/smt_roi_calculator.py`

Interactive CLI calculator — inputs prospect's actual numbers and outputs:
- Landed cost (with correct tariffs for Mexico/Vietnam/Poland/custom)
- Annual savings breakdown (labor, defects, maintenance, revenue uplift)
- Payback period in months
- 5-year TCO comparison vs. keeping old equipment
- Comparison vs. Japanese equipment ($915K full line)

**Pre-populate with prospect's numbers before the discovery call:**
- Current OEE
- Monthly board volume
- Number of THT operators
- Board margin

---

## PowerPoint Proposal Outline (13 Slides)

**File:** `~/SMT_Proposal_Outline.md`

1. Cover
2. Who We Are
3. Your Situation (customize to prospect's pain)
4. The Solution (6-machine line overview)
5. ROI Analysis (use calculator output)
6. TCO Comparison (vs. partial upgrade vs. keep old)
7. Competitive Comparison (SM vs. Yamaha vs. Fuji)
8. Reference Clients (2–3 in same region/vertical)
9. Technical Specifications
10. Payment Terms & Delivery
11. Acceptance Protocol (FAT + 60-day guarantee)
12. Next Steps (Full Line vs. Pilot Option)
13. Appendix (spec sheets)
