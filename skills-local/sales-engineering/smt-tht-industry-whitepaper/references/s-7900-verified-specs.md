# S-7900 Series — Verified Hardware Specifications
## Source: Southern Machinery Engineering Datasheet, 2026 Q2
## Location in skill: `references/s-7900-verified-specs.md`

---

## S-7900 Standard vs S-7900 Pro — Full Spec Table

| Parameter | S-7900 Standard | S-7900 Pro (Active Clinching) |
|---|---|---|
| Insertion Heads | 4-head parallel kinematic | 4-head + Clinching Module |
| Placement Accuracy | ±0.05mm | ±0.05mm |
| Insertion Force | 98N, closed-loop, independently monitored per joint | 98N + Clinching force monitoring |
| Force Monitoring Rate | 1 kHz | 1 kHz |
| AI Vision | Deep-learning, 50,000+ odd-form images, 360° lead inspection, independent per head | AI Vision + Clinching quality monitoring |
| Component Range | 3–25mm (relays, connectors, terminals, transformers, cylindrical capacitors) | same |
| Rated Throughput | 4,000 CPH (continuous, post warm-up) | 3,800 CPH (continuous, with Active Clinching) |
| Active Clinching | — | **Standard**: 30°±1° bend angle, 50ms cycle |
| MES Interfaces | REST API, XML batch, Modbus TCP (standard); OPC UA (optional) | same |
| CE Certification | ✅ | ✅ |
| Target Industry | Consumer electronics, industrial control, comms equipment | **Automotive ECU, EV BMS, medical (Class 3), rail, safety modules** |

---

## Active Clinching — Technical Moat Explanation

Active Clinching is the mechanical deformation of the component lead at the PCB land surface immediately after insertion — creating a 45°–90° cold-formed interlock between lead and PCB barrel wall. This is a **physical backup joint** independent of and in addition to the solder fillet.

**Why this is a moat:**
- Yamaha YV100X-THT and Fuji NXT odd-form equivalent tier: Active Clinching is either absent or a costly optional module
- Universal GSM series: no Active Clinching module available
- S-7900 Pro: **Active Clinching is standard** — no upcharge

**Validated performance data (internal + third-party test reports):**
- Thermal cycling: –40°C to +125°C, 1,000 cycles, zero fatigue cracks at clinch point (per ISO 16750 environmental test profiles)
- Dual-protection structure: if solder joint develops micro-crack under thermal cycling, the clinch point maintains electrical continuity
- Void reduction: because the joint does not rely on solder filling the entire barrel void, void-induced failure rate is significantly reduced
- Standards compliance: IPC-A-610 Class 3, IPC-J-STD-001, ISO 16750

**When to recommend S-7900 Pro (Active Clinching):**
- Automotive ECU / BCM / airbag control modules
- EV battery management systems (BMS)
- Any application requiring IATF 16949 or AEC-Q100/Q104 qualification
- Medical devices requiring IPC-A-610 Class 3
- Rail / transportation controllers with wide temperature range requirements

---

## S-7900 vs S-70LD — When to Use Which

| Scenario | Recommended Model |
|---|---|
| Automotive / EV BMS / medical / any application needing Active Clinching | **S-7900 Pro** |
| General EMS, industrial control, power supply, white goods (no Active Clinching needed) | **S-70LD** |
| High-volume radial components (LED strips, capacitors,晶体管,轻触开关) | **S-3000** (10,000–12,000 CPH real production speed) |
| High-volume axial components (resistors, diodes) | **S-4000** (22,000 CPH theoretical) |
| Terminal / pin / eyelet insertion requiring ultra-high precision | **S-7020T** (dual-head, ±0.015mm) |

---

## Field-Proven Use Cases (Anonymized)

### Case 1 — Mexican Tier-2 ODM, Automotive HUD Module
- Problem: 3-week NPI cycle losing deals to faster competitors
- Solution: S-7900 + AI Vision; 30-minute changeover between product families
- Outcome: won automotive HUD module contract; NPI speed became competitive sales weapon
- Audit result: IATF 16949 audit passed on first attempt

### Case 2 — China EV BMS Manufacturer
- Problem: IATF 16949 audit required per-joint Cpk data; traditional THT joint data was not auditable
- Solution: S-7900 with Active Clinching + MES data export (per-joint force, angle, depth, clinch parameters)
- Outcome: IATF 16949 audit passed on first submission using per-joint CPK report

### Case 3 — European White Goods OEM
- Problem: 62% line OEE on legacy THT line
- Solution: S-7900 + S-WS450 full-line replacement
- Outcome: OEE improved to 81% in 6 months; 3 operators displaced per shift

---

## Anti-Hallucination Checklist (read before writing any S-7900 claim)

- [ ] Throughput: S-7900 is **4,000 CPH** (S-7900 Pro is 3,800 CPH with Active Clinching)
- [ ] S-3000 (radial) is 10,000–12,000 CPH real production speed — NOT the S-7900 figure
- [ ] Accuracy: **±0.05mm** (not ±0.04 — that is the Universal GSM figure)
- [ ] Insertion force: **98N** (programmable, 1kHz monitoring — verify before quoting)
- [ ] Active Clinching: 30°±1° bend, 50ms cycle — cite from datasheet, not memory
- [ ] Lead time: **4–8 weeks** (not 2–4 — that understates; not 8–12 — that overstates)
- [ ] Field service SLA: **24–48 hours** (Shenzhen factory direct — not via代理商)
- [ ] CapEx comparison: S-7900 line is **55%–65%** of Japanese equivalent (not a flat 50%)
- [ ] If asked about S-3000 speed: say "10,000–12,000 CPH" not "18,000 CPH" (18,000 is the theoretical maximum under ideal axial conditions per catalog, not the production-realistic figure)
