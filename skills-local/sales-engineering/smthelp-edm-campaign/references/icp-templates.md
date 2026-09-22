# ICP Templates — SMT/THT Equipment EDM

## ICP Template 1: EMS Factory (EMS代工厂)

```yaml
customer_type: "EMS代工厂"
profile:
  company_description: >
    Electronic Manufacturing Services provider. Takes OEM/ODM orders,
    assembles PCBs from bare board to finished product. Runs SMT lines
    and THT insertion lines. Typically 50-500 workers.
  common_titles:
    - "Operations Manager"
    - "Production Manager"
    - "Plant Manager"
    - "CEO"
    - "Procurement Manager"
  target_countries:
    - "Vietnam (Hanoi, Ho Chi Minh City)"
    - "Mexico (Queretaro, Guadalajara)"
    - "Hungary"
    - "Poland"
    - "Brazil (Manaus)"
  hard_filters:
    - "Annual revenue: $5M - $100M"
    - "SMT/THT production confirmed"
    - "Has expansion or equipment upgrade plan"
    - "NOT using all-Japanese equipment already"
  pain_points:
    - "Manual THT insertion is expensive and inconsistent"
    - "Labor costs rising 8-12% per year"
    - "Need faster changeover for multi-product runs"
    - "Quality consistency issues with manual insertion"
  value_proposition:
    primary: "S-70LD odd-form inserter — replace 6-8 workers, payback in 12-18 months"
    secondary: "S-WS450 wave solder — reduce solder defect rate by 30%"
    proof: "Hungary EMS: 37% OEE improvement, 14-month payback"
```

---

## ICP Template 2: ODM Factory (ODM设计厂)

```yaml
customer_type: "ODM设计厂"
profile:
  company_description: >
    Original Design Manufacturer. Designs products for brand owners.
    NPI (New Product Introduction) cycles are frequent. Needs flexible
    THT insertion that handles many product variants with minimal changeover.
  common_titles:
    - "NPI Manager"
    - "Engineering Manager"
    - "R&D Manager"
    - "CEO / Founder"
  target_countries:
    - "Vietnam"
    - "Mexico"
    - "China (near-shore processing)"
    - "India"
  hard_filters:
    - "Running NPI projects with >5 product variants"
    - "Changeover time is a known bottleneck"
    - "Has design responsibility for PCB assembly"
  pain_points:
    - "Feeder changeover takes too long (hours vs <30 min target)"
    - "AI vision correction needed for multiple component types"
    - "Speed-to-production is competitive differentiator"
  value_proposition:
    primary: "S-7900 AI vision — changeover under 30 min between product families"
    secondary: "Active Clinching for automotive-grade boards"
    proof: "Mexico ODM won automotive HUD contract with 40% faster NPI turnaround"
```

---

## ICP Template 3: Automotive Electronics (汽车电子)

```yaml
customer_type: "汽车电子"
profile:
  company_description: >
    Manufactures PCBs for automotive applications. Subject to strict
    quality standards: IPC-610, IATF 16949, AEC-Q100/Q200.
    Reliability is non-negotiable. Thermal cycling resistance critical.
  common_titles:
    - "Quality Manager"
    - "Engineering Manager"
    - "Plant Manager"
    - "Procurement Director"
  target_countries:
    - "Germany"
    - "France"
    - "Czech Republic"
    - "Hungary"
    - "Mexico"
  hard_filters:
    - "IATF 16949 certified"
    - "Producing BCM, ECU, BMS, or similar automotive modules"
    - "Currently using manual THT insertion (upgrade window)"
  pain_points:
    - "Solder joint reliability under thermal cycling"
    - "Need mechanical backup to solder joint (Active Clinching)"
    - "Audit trail and process documentation requirements"
  value_proposition:
    primary: "S-7900 Active Clinching — mechanical backup to solder joint"
    secondary: "CE certified, IPC-610 compliant process documentation"
    proof: "Multiple automotive customers running 18+ months with zero major service calls"
```

---

## ICP Template 4: New Factory Setup (新厂建设)

```yaml
customer_type: "新厂建设/整线采购"
profile:
  company_description: >
    Greenfield investment. Building new SMT/THT production facility.
    Looking for turnkey line solutions. Budget-conscious but quality-aware.
    Needs complete line: Loader → Printer → Pick & Place → Reflow → AOI → THT → Wave.
  common_titles:
    - "CEO"
    - "Factory Director"
    - "Investment Manager"
    - "Operations Director"
  target_countries:
    - "Vietnam"
    - "Mexico"
    - "Indonesia"
    - "India"
    - "Ethiopia (emerging)"
  hard_filters:
    - "New factory construction confirmed (news/gov data)"
    - "Equipment budget allocated"
    - "Timeline: within next 12 months"
  pain_points:
    - "Japanese equipment too expensive for greenfield budget"
    - "Need complete line working in 4-8 months"
    - "No internal SMT engineering expertise to integrate multiple brands"
  value_proposition:
    primary: "Complete SMT/THT line — delivered in 4-8 weeks, 40-50% below Japanese"
    secondary: "SFY03 AGV for automatic material handling"
    proof: "Thailand greenfield: line installed and running in 6 weeks, $180K below budget"
```

---

## ICP Template 5: Power / Industrial Control (电源/工控)

```yaml
customer_type: "电源/工业控制"
profile:
  company_description: >
    Manufactures power supplies, motor drives, PLCs, industrial inverters.
    Heavy use of through-hole components: transformers, electrolytic capacitors,
    heatsinks. Wave solder is primary process. High volume, stable product mix.
  common_titles:
    - "Production Manager"
    - "Process Engineer"
    - "Plant Manager"
    - "Procurement Manager"
  target_countries:
    - "China (Pearl River Delta, Yangtze Delta)"
    - "Vietnam"
    - "Brazil"
    - "Eastern Europe"
  hard_filters:
    - "Running wave solder process (DIP lines)"
    - "High mix of connectors, relays, transformers"
    - "Monthly production >50K boards"
  pain_points:
    - "Wave solder defect rate (bridging, icicles)"
    - "Need nitrogen inerting to reduce oxidation"
    - "Heavy components pop off during wave"
  value_proposition:
    primary: "S-WS450 wave solder — dual wave, nitrogen option, 460KG solder pot"
    secondary: "S-7020T dual-head inserter for connectors at 12,000 CPH"
    proof: "Brazil power supply: defect rate dropped from 2.1% to 0.4%, payback in 11 months"
```
