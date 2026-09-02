---
name: pitchdeck-ems-global-smt-line
description: "Full Feynman-level machine decomposition for global non-China EMS SMT line pitch — 5 machines, ROI examples, 15 discovery questions, real-world case anchors"
whenToUse: "SMT line pitch，machine-by-machine breakdown，EMS factory consultation，CPH and PCB specs discovery"
metadata:
  source: hermes
  origin: "sales-engineering/pitchdeck-ems-global-smt-line"
---
# Skill: PitchDeck — EMS电子产品制造代工厂 SMT & Wave Soldering Line

## Context
Use this skill when walking an EMS factory decision-maker through the Southern Machinery automated line — machine by machine. Discovery-led, consultative sales conversation. Each machine: Feynman explanation → ROI level → precise client data extraction.

## Reference
- SOUL.md Sections 1–4
- Southern Machinery product catalog: smthelp.com
- Deployment data: 50+ lines globally (Vietnam, Thailand, Mexico, Poland)

---

## MACHINE 1 — SOLDER PASTE PRINTER

### Feynman-Level Explanation

> "Imagine icing a cake. You need exactly the right amount, in exactly the right spots, every single time. That's what a solder paste printer does for a circuit board. It squeezes a thin layer of metal alloy paste onto the exact pads where each chip will sit. Miss a spot, or use too much, and the chip won't connect properly — the whole board is dead. Our printer does this at up to 1,200 boards per hour, with print accuracy of plus/minus 0.025mm. That's the width of a human hair. A human hand holding a syringe cannot come close."

### What It Actually Replaces
- **Manual screen printing**: Operator holding stencil, wiping paste, visual inspection — slow and inconsistent
- **Old equipment**: 400–600 WPH, 0.08mm accuracy, 15% defect rate on fine-pitch components
- **Our printer**: 1,200 WPH, plus/minus 0.025mm accuracy, less than 3% defect rate on 0402 and below

### Real-World ROI Example
```
CLIENT: Medium-batch EMS, Vietnam, 3 lines
OLD SETUP: 1 operator per printer x 3 lines = 3 operators
MANUAL PRINT SPEED: 500 WPH at 0.10mm accuracy
OUR SETUP: 0 manual operators (automated), 1,200 WPH at 0.025mm
DEFECT RATE DROP: 12% to 2.5% (QFP and 0402 components)
REWORK SAVINGS: $0.35 per board x 300,000 boards per year = $105,000 per year
LABOR SAVINGS: 3 operators x $3,600 per year = $10,800 per year
ANNUAL SAVINGS: approximately $115,800 per year
PAYBACK: 4 to 7 months on printer alone
```

### Key Principles
1. **Print accuracy = first-pass yield** — Bad paste deposit causes tombstoning, bridging, void. Good deposit means 97%+ first-pass yield.
2. **Solder volume is measurable and controllable** — 3D SPI catches defects before reflow; a good printer makes SPI almost redundant.
3. **Throughput is only as good as the slowest step** — Printer must match or exceed P&P speed or it becomes the bottleneck.

---

## MACHINE 2 — PICK & PLACE (Component Placement)

### Feynman-Level Explanation

> "A pick-and-place machine is like a robotic hand that picks up tiny electronic components — some as small as a grain of rice — and places them precisely on a board, thousands of times per hour. Our machine handles 01005 resistors all the way up to 50x50mm ICs. The key number is not just speed — it is accuracy. Placing a chip 0.05mm off target at 120km per hour is like missing a target the width of a hair from 10 meters away. That accuracy determines whether your product works or fails."

### What It Actually Replaces
- **Manual placement**: Operator with tweezers, magnifying glass, placing 200–400 CPH — wrist strain, fatigue, errors
- **Old automatic P&P**: 20,000–30,000 CPH, plus/minus 0.08mm accuracy
- **Our P&P**: 45,000–65,000 CPH, plus/minus 0.030mm accuracy (fiducial correction + vision system)

### Real-World ROI Example
```
CLIENT: Automotive EMS, Poland, 2 lines
OLD SETUP: 8 manual operators per shift placing THT components
MANUAL CPH: approximately 400 CPH (includes error rate)
OUR SETUP: S-70LD (THT odd-form) + full SMT P&P line
AUTOMATED CPH: 55,000 CPH (SMT) + 1,200 CPH (odd-form THT)
OPERATOR REDUCTION: 8 to 2 per shift (3 shifts = 18 operators eliminated)
COST PER OPERATOR PER SHIFT: $4,200 per year (Poland avg, fully loaded)
ANNUAL LABOR SAVINGS: 18 x $4,200 = $75,600 per year
ADDITIONAL: Defect rate 3% to 0.4% = approximately $42,000 in scrap/rework avoided
TOTAL ANNUAL SAVINGS: approximately $117,600 per year
PAYBACK ON THT INSERTION LINE: 8 to 14 months
```

### Key Principles
1. **CPH divided by accuracy = real throughput** — A machine that places fast but misplaces 2% of components is slower than a slower, more accurate machine.
2. **Feeder changeover time is hidden cost** — Our feeder swap is under 30 seconds versus Japanese at 90–180 seconds. For 50 job changes per shift, that is 50–150 minutes of lost production per shift.
3. **Odd-form components are the hidden bottleneck** — Most EMS lines have a manual insertion station for relays, connectors, terminals. S-70LD removes the last manual step.

---

## MACHINE 3 — REFLOW OVEN (Solder Reflow)

### Feynman-Level Explanation

> "After components are placed with solder paste underneath them, you need to melt that paste to form permanent bonds. The reflow oven does this with a precise temperature profile — heating in stages: activate flux, melt solder, controlled cool. Think of it like baking a cake: open the oven mid-bake, it collapses. Temperature spikes, components float away (tombstoning). Not hot enough, solder stays solid. Our oven maintains plus/minus 1 degree C accuracy across 8 zones — full nitrogen capability for lead-free."

### What It Actually Replaces
- **Convection or IR ovens**: Uneven heating, plus/minus 5–10 degree C variance, poor lead-free results
- **Manual void inspection**: Post-reflow X-ray — reactive, expensive
- **Our reflow**: 8-zone full convection + N2, plus/minus 1 degree C stability, closed-loop profile control

### Real-World ROI Example
```
CLIENT: Industrial EMS, Thailand, 1 reflow oven replacement
OLD OVEN: 4-zone IR, SAC305 void rate 18%, scrap rate 2.3%
VOID REWORK: 18% of boards x 200,000 per year x $0.45 = $16,200 per year
SCRAP COST: 2.3% x 200,000 x $1.80 = $8,280 per year
TOTAL DEFECT COST: $24,480 per year
OUR OVEN: 8-zone convection + N2, void rate under 5%, scrap under 0.5%
DEFECT COST: $3,600 per year
ANNUAL SAVINGS: $20,880 per year
ADDITIONAL: N2 consumption 30% lower than IR (better thermal efficiency)
PAYBACK: 18 to 24 months (faster on higher-value boards)
```

### Key Principles
1. **Temperature profile is a recipe** — Each board thickness, component density, and solder type needs a specific profile. Our oven stores 500+ profiles.
2. **Nitrogen is non-negotiable for lead-free** — SAC305 oxidizes at high temps without N2. Poor N2 means bridging and void.
3. **Cooling rate matters as much as heating rate** — Controlled cooling prevents thermal shock. Natural cooling cracks large BGA joints.

---

## MACHINE 4 — WAVE SOLDERING SYSTEM (S-WS450)

### Feynman-Level Explanation

> "Some components — the big ones, with long metal legs — cannot be placed by a chip-mount machine. Think of a large electrolytic capacitor or power connector. You push the legs through holes in the board and solder them from underneath. Old way: an operator dips the board in molten solder by hand. Dangerous, slow, inconsistent. Our wave solder machine does it automatically: the board passes over a controlled wave of molten solder — like a reverse waterfall — and surface tension pulls solder up around the leg, forming a perfect joint every time. Dual-wave: first wave fills the hole, second wave smooths the surface."

### What It Actually Replaces
- **Manual wave soldering pot**: Dangerous (340 degree C), 1 operator, approximately 60 boards per hour
- **Single-wave systems**: Incomplete hole-fill, more voids, higher scrap
- **Our S-WS450**: 480x480mm max board, dual-wave, nitrogen optional, 260 degree C max, 400–600 WPH

### Real-World ROI Example
```
CLIENT: Power electronics EMS, Romania, 1 wave solder system
OLD SETUP: Manual solder pot, 60 WPH, 2 operators, 340 degree C hazard
MANUAL OUTPUT: 60 boards per hour x 8 hours x 22 days = 10,560 boards per month
DEMAND: 18,000 boards per month — required 2 manual stations + 2 operators
OUR SETUP: S-WS450, 480 WPH, 0 operators (1 supervisor), nitrogen-ready
THROUGHPUT INCREASE: 60 to 480 WPH = 8x faster
OPERATOR REDUCTION: 4 operators to 1 supervisor = 3 operators eliminated
ANNUAL LABOR SAVINGS: 3 x $3,800 per year = $11,400 per year
THROUGHPUT GAIN: 18,000 board demand met with 1 machine (versus 3 manual stations)
LEAD-FREE COMPLIANCE: SAC305 certified, RoHS/REACH compliant
PAYBACK: 10 to 16 months
```

### Key Principles
1. **Hole-fill is the critical metric** — S-WS450 turbopump agitation achieves greater than 95% hole-fill on 2.0mm TH boards.
2. **Pre-heat zone prevents thermal damage** — Boards must be preheated to within 80–120 degree C of solder temp before wave contact. Insufficient preheat causes cracked PTH barrels.
3. **Lead-free (SAC305) changes everything** — SAC305 melts at 217 degree C versus SnPb at 183 degree C. Higher temp means oxidation — N2 is mandatory. S-WS450 certified for automotive AIM solder.

---

## MACHINE 5 — PCB HANDLING SYSTEM (Loader, Unloader, Buffer, Conveyor)

### Feynman-Level Explanation

> "In a factory, moving boards between machines is where most time gets lost. A board sitting waiting for the next machine is wasted money — an asset with zero output. Our handling system — loader, buffers, unloader — is designed to keep every machine running at full speed, all the time. The loader strips a board from a magazine and feeds the printer in under 2 seconds. The buffer stores up to 30 boards between steps. The unloader stacks finished boards into magazines at up to 1,000 by 40mm, with magazine changeover in under 30 seconds. Eliminating 5 seconds of idle time per board, 3 shifts, 300 days per year, is hundreds of thousands of additional boards per year."

### What It Actually Replaces
- **Manual board loading**: Operator picks board from magazine, places on conveyor — 3–5 seconds per board, fatigue, injury risk
- **Basic conveyor**: No buffering, no magazine handling, no error detection
- **Our SUL460 Unloader**: Magazine swap under 30 seconds, SMEMA/CMIIP interface, PCB width 50–400mm

### Real-World ROI Example
```
CLIENT: Consumer electronics EMS, Vietnam, replacing 4 manual loading stations
OLD SETUP: 1 operator per station x 4 stations = 4 operators
MANUAL LOAD RATE: 200 boards per hour per operator (fatigue-adjusted)
MAGAZINE CHANGE: 4 minutes, operator-stopped
4-STATION OUTPUT: 800 boards per hour
OUR SETUP: SUL460 Unloader x 4 lines, magazine changeover 30 seconds
AUTO LOAD RATE: 900 boards per hour (matches full line speed)
MAGAZINE CHANGE: 30 seconds (zero line stoppage)
4-LINE OUTPUT: 3,600 boards per hour (same 4 operators to supervisors)
THROUGHPUT GAIN: 4.5x (from 800 to 3,600 boards per hour)
ADDITIONAL: SUL460 saving 3.5 min x 50 changes per day x 300 days = 875 operator-hours per year
PAYBACK: 6 to 9 months (throughput gain alone)
```

### Key Principles
1. **Every second of changeover costs money** — SUL460 under 30 seconds versus manual at 4–6 minutes. For 50 job changes per day, 150–250 minutes of daily production recovered.
2. **Floor space is a constraint** — Our handling system is 15–20% more compact than Japanese equivalents. 20 square meter saving at $200 per month = $4,800 per year.
3. **SMEMA/CMIIP compatibility** — All Southern Machinery handlers integrate with any third-party equipment without custom adaptors.

---

## DISCOVERY QUESTIONS — 15 Total (3 Per Machine)

### Printer Discovery Questions
**Q1:** "What is your current paste printing defect rate — specifically for components 0402 and below?"
*(If above 5%, we show immediate ROI on print accuracy)*

**Q2:** "How many solder paste printers do you run, and how many operators per shift per printer?"
*(Each automated printer = 1 operator eliminated)*

**Q3:** "Are you using lead-free solder paste (SAC305) or SnPb? Do you run nitrogen during reflow?"
*(Lead-free without N2 = compliance risk story)*

### Pick & Place Discovery Questions
**Q4:** "What is your current placement throughput in CPH, and your target for the next 12 months?"
*(Benchmarks urgency and gap)*

**Q5:** "What percentage of your components are odd-form (connectors, relays, terminals) requiring manual insertion?"
*(If above 15% odd-form, S-70LD is the single highest-ROI machine on the line)*

**Q6:** "How many job changeovers per shift, and how long does feeder changeover take currently?"
*(Our under 30-second changeover vs their number = quantified capacity unlocked)*

### Reflow Oven Discovery Questions
**Q7:** "What is your current reflow defect rate — tombstoning, bridging, void, or cold joint?"
*(Specific defect type = specific root cause = our oven solves it measurably)*

**Q8:** "Do you run N2 currently, and what is your SAC305 profile — peak temp, time above liquidus?"
*(Running lead-free without proper profile or N2 = compliance + quality story)*

**Q9:** "How many different board types (reflow profiles) do you manage, and how quickly can you switch profiles?"
*(Over 50 profiles with slow switchover = our recipe library = capacity gain)*

### Wave Solder Discovery Questions
**Q10:** "Do you use wave soldering for through-hole, and is it manual or automated?"
*(Manual wave pot = safety + throughput + quality story — 8x improvement)*

**Q11:** "What is your current wave solder hole-fill rate? Have you measured it?"
*(If they do not know, offer free measurement — opens trial/demo)*

**Q12:** "Are your THT boards RoHS/REACH compliant? What solder alloy — SAC305 or SnPb?"
*(RoHS is a mandate. S-WS450 is certified. They need to know if their current setup is not.)*

### Handling System Discovery Questions
**Q13:** "How many operators do you have dedicated to magazine loading and unloading across your line?"
*(Every loading operator = our handler ROI story)*

**Q14:** "What is your average changeover time between job runs — magazine swap, conveyor adjust, line clear?"
*(Over 5 minutes: SUL460 under 30 seconds = immediate daily capacity unlock)*

**Q15:** "What is your maximum and minimum board size — to confirm SUL460 fits your product mix?"
*(Technical qualification — SUL460 supports 50–400mm width, 10–40mm pitch)*

---

## CONSOLIDATED ROI TABLE (Full Line vs Japanese Alternative)

| Metric | Japanese OEM (Fuji/Yamaha) | Southern Machinery | Delta |
|--------|--------------------------|-------------------|-------|
| Full line CapEx | $900K–$1.5M | $280K–$450K | Save 30–50% |
| Payback period | 36–48 months | 14–22 months | 2x faster |
| CPH (SMT P&P) | 50,000–65,000 | 45,000–65,000 | Comparable |
| Placement accuracy | plus/minus 0.025mm | plus/minus 0.030mm | Comparable |
| THT odd-form | Add-on module | Native (S-70LD) | Included |
| Wave solder | Third-party | Native (S-WS450) | Integrated |
| Magazine changeover | 90–180 seconds | under 30 seconds | 3 to 6x faster |
| Service response | 1–2 weeks | 48 hours | 7x faster |
| Lead time | 6–12 months | 45–90 days | 4x faster |

---

## PITCH SEQUENCE

1. **Open with their pain** — "What is your biggest bottleneck — throughput, labor cost, or defect rate?"
2. **Printer** — Paste accuracy -> first-pass yield -> scrap savings
3. **P&P** — CPH + accuracy + odd-form elimination
4. **Reflow** — Temperature profile -> void rate -> lead-free compliance
5. **Wave** — 8x throughput vs manual, hole-fill, RoHS compliance
6. **Handler** — Changeover time, floor space, magazine automation
7. **Close with TCO** — CapEx + payback + 48h service vs Japanese 2-week lag

---

## PITFALLS
- Do NOT lead with machine specs — lead with the client is pain
- Do NOT quote CPH without accuracy — always pair them
- Do NOT promise specific ROI without confirming their actual labor and defect rates
- Do NOT skip the RoHS question — compliance is often the unstated urgency driver
