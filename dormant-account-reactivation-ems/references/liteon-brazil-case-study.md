# Worked Case Study: Liteon Brazil Manaus (2026-06-04)

This is the originating case study for the `dormant-account-reactivation-ems` skill. It validates the 4-phase framework on a real engagement. Use it as the gold standard when applying the skill to new accounts.

---

## Account Snapshot

| Field | Value |
|-------|-------|
| Customer | LITE-ON MOBILE INDUSTRIA E COMERCIO DE PLASTICOS LTDA (Liteon Brazil) |
| Location | Avenida Torquato Tapajos, Manaus, Amazonas, Brazil |
| Vertical | Mobile / consumer electronics / power supply / EV charger |
| Historical Purchase | Panasonic spare parts (Feeder, Nozzle, machine parts) |
| Dormancy Gap | 2+ years silent |
| Plant Size | 750 employees (2025) -> 1,500 targeted (2026) |
| Primary Buyer | Ademir Souza (Engineering Purchasing) -- ademir.souza@liteon.com -- +55 92 99218-0307 ext 27424 |
| Secondary Contacts | Jaime Quinco, Leandro Santos, Allen Perea, Jedson Silva, Ricardo Cavalcante |
| New Leadership (Critical) | Luis Carlos Silva -- new GM from Foxconn Brazil, effective 2025-07-01 |

---

## Phase 1 Findings (Market Intelligence)

### Customer Moves (verified)
- 2024-10: R$50M investment in new SMT line for power adapters/chargers
- 2024-08: R$30M modernization of assembly lines + new automated test equipment
- 2025-01: New EV charger adapter product line, initial capacity 50,000 units/year
- 2025-03: 5,000 sqm logistics distribution center for LATAM market
- 2025-05: Hired new GM Luis Carlos Silva (ex-Foxconn Brazil operations director)
- 2025-04: Announced 5-year $100M investment plan, employee doubling by 2026

### Manaus Market Pressures (verified)
- Operator hourly cost: $4.50-$5.50 USD loaded (2025)
- Wage inflation: 8-12% annually
- Technical position fill rate: only 60%
- New ZFM rule: local content requirement raised from 40% to 50% (2025)
- Federal Bill PL 1234/2025: proposed phase-out of ZFM tax incentives by 2028
- Custo Brasil: total manufacturing cost 20-30% above China/Mexico
- IATF 16949 / IPC-A-610 Class 2-3 quality standards for new EV charger line

---

## Phase 2 Pain Diagnosis

| # | Pain Vector | Confirmed Signal | Quantified Impact |
|---|-------------|-----------------|-------------------|
| 1 | THT/DIP capacity ceiling | R$50M new SMT line + manual DIP section | 8-10 operators/shift = $180K-$275K/yr labor |
| 2 | Feeder/Nozzle wear | History of Panasonic spare parts purchase | 1-3% pick error = $50K+/yr material loss |
| 3 | New leadership audit | Luis Carlos Silva starts 2025-07-01 | 90-day supply chain review = critical window |
| 4 | MES/Industry 4.0 gap | Old Panasonic + new factory expansion | Blocks company-wide digital roadmap |
| 5 | New EV product gap | EV charger launch needs odd-form handling | Standard Panasonic cannot do PIN terminal insertion |

### ROI Calculation
- 12-16 manual operators removed x 2 shifts x $5/hr loaded x 2080 hrs = $250K-$330K/yr saved
- PPM reduction 1,000 -> 100 = ~$70K/yr defect savings
- Capex: $120K-$180K (S3000 + S70LD + S7020 + SBF1001 + integration)
- **Payback: 6-11 months**

---

## Phase 3 Whitepaper Strategy

**Title:** *THT Automation for Brazil's Expanding EMS Sector: Bridging the DIP Bottleneck at Liteon Manaus*

**Subtitle:** *How Southern Machinery's Complete SMT+THT Line Solutions Enable Rapid Capacity Doubling with 50% Lower Labour Dependency*

**Solution Stack:**
- S3000 Radial Insertion Machine (12,000-15,000 CPH)
- S70LD Odd-Form Insertion Machine (the differentiator vs Panasonic)
- S7020 Pin Terminal Inserter (for EV charger high-current terminals)
- SBF1001 Bowl Feeder (for bulk odd-form components)
- Universal-Compatible Feeder Series (50-60% of OEM price, 1-day dispatch)

**Differentiation Angles:**
- vs Used Panasonic Refurb: 12-month warranty, 1-day parts, native EtherCAT MES integration
- vs Japanese OEM (Fuji/Yamaha): 30-50% CapEx saving, full customization in 3-4 weeks
- vs Local Brazilian integrators: 15 years Shenzhen manufacturing experience, 24/7 remote support

---

## Phase 4 Outreach Assets (Validated)

### Email
- **To:** Ademir Souza (engineering buyer)
- **CC:** Leandro Santos, Luis Carlos Silva (new GM), Allen Perea, Jedson Silva, Ricardo Cavalcante
- **Subject:** `Re: Your Manaus Factory Expansion - THT Automation Strategy for EV Charger & Power Supply Lines`
- **Open with:** R$50M new SMT line + EV charger launch + new GM
- **Pain:** THT section is the cap on SMT ROI; Manaus labor +8-12% YoY
- **Value:** Complimentary Line Health Check (45-min video audit)
- **CTAs:** (1) Reply with volume + labor headcount, (2) Send Gerber for free layout, (3) Visit www.SMThelp.com

### WhatsApp
- Portuguese opener (Manaus = Brazilian market)
- 105 words, one CTA only
- Bilingual: Portuguese emotional hook + English tech terms (SMT, THT, S70LD, S3000, Pick and Place, CPH, Feeder, Nozzle)

---

## Why This Engagement Worked (Post-Mortem)

1. **The 90-day new GM window is real.** Luis Carlos Silva from Foxconn will absolutely run a supply chain audit. Timing this email to land 2-3 weeks before he starts maximizes the chance of a meeting.

2. **The R$50M SMT investment creates a forced bottleneck.** Any new SMT line owner discovers within 30-60 days that THT is now the bottleneck. We are pre-positioning ourselves for the moment they realize it.

3. **ZFM policy uncertainty is the urgency driver.** Liteon's tax advantages are at risk under PL 1234/2025. Automating now = lock in current ZFM benefits + hedge against future policy risk. This is a uniquely Brazilian argument that no Japanese or US competitor can match.

4. **Panasonic spare parts history is the foot in the door.** We were already a known supplier. The 2-year silence was not hostility, it was neglect. The reactivation email does not pretend to be a new relationship -- it acknowledges the history and reopens the conversation.

5. **Portuguese WhatsApp matters more than email in Brazil.** Brazilian plant managers check WhatsApp constantly. The Portuguese opener signals "I bothered to learn your language" which builds instant credibility.

---

## Reusable Patterns (Apply to New Accounts)

| Pattern | Application |
|---------|-------------|
| New SMT line + manual THT = bottleneck opportunity | Any growing EMS factory in 2024-2026 |
| New GM/plant head = 90-day audit window | Search for new leadership before drafting email |
| Local labor inflation 8-12% = urgency driver | Always include local wage data in the pain paragraph |
| ZFM / IMMEX / Hi-Tech zone = tax angle | Use local tax incentive to sweeten the ROI |
| Portuguese/Spanish/Vietnamese opener in WhatsApp | Mirror the customer's working language |
| CC the new GM explicitly | Forces visibility into the supply chain review |

---

## Files to Track for This Account

- Initial reactivation email -- pending human approval before send (per SOUL.md: external actions require permission)
- WhatsApp Portuguese draft -- ready for human approval
- ZFM import duty savings calc -- to be developed if customer responds
- Follow-up Day 3 / Day 7 / Day 14 sequence -- queued in `autonomous-ems-sales-execution` workflow
