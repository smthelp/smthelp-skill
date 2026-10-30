# Legacy Equipment Hook Pattern

## The insight

For any dormant customer whose PO archive is 2-10+ years old, **the single most penetrating hook** in the reactivation brief is **identifying the brand of equipment they bought last time** and using it as the launchpad for section 2 (Gap Analysis).

Reason: a 2-10 year gap means that line is now in mid-life. The customer is feeling the pain of:

- Spare parts getting harder to source
- Mechanical wear driving up defect rates
- New product mix no longer fitting the old machine's envelope
- ISO 50001 / IATF 16949 audits flagging lack of MES connectivity

…and they are **silently shopping for a refresh or augmentation**. Naming the legacy line in the first 30 seconds of section 2 is the equivalent of saying "I remember exactly what you bought, and I know what's breaking about it now."

## Common legacy brand → upgrade pattern mapping

| Historical PO line | What the customer feels in 2026 | Southern Machinery upgrade |
|---|---|---|
| **UIC (Universal Instruments) THT line** | 10-15 yr old, no odd-form, can't handle new power-electronics boards | **S-70LD** dual-head odd-form inserter + S3000 radial |
| **TDK radial insertion** | Lost support post-TDK exit, can't get feeders | **S3000** + custom Feeder/Nozzle replacement |
| **Panasonic / Yamaha / Fuji (older gen)** | Newer boards need flexibility the old gen can't provide | Full line augmentation — keep old Pick & Place, add Southern THT + Wave |
| **Generic Chinese wave solderer** | Process window unstable, no MES | **S-WS450** with energy profile + optional MES module |
| **No machine, only spare parts** | Line is now maintenance-deprived, no roadmap | Push spare-parts subscription + **free Line Health Check** |
| **ESD / consumables only** | Not a capex customer — keep low-touch, push consumables | 季度备件订阅 + 30-min check-in call |
| **Cleaning machine (e.g. older S-100A)** | RoHS / ESPR regulation tightening, residue specs tighter | **S1688** or upgraded **S-100A** with water-based cycle |

## How to phrase the hook in the brief

Open section 2 with one of these patterns (Chinese):

> "基于贵司历史采购记录（PO 4511656846 / 2022，UIC Auto Insertion Spare Parts），E.G.O. Spain 当前的 THT 段应仍为 **UIC 时代产线（10-15 年前装机）**。该平台对径向/轴向仍可胜任，但面对 2026 年新板型（变频控制器、IoT 模组、热泵控制器）中的异形件（继电器、接线端子、变压器、IGBT 模块）几乎无解——"

Translate to the customer's specific legacy line. If unknown, write "基于贵司 20XX 年的 PO 记录" and pick the most likely category from the table.

## Pitfall: don't overspec

- DO NOT invent a UIC model number you can't verify from the PO archive
- DO NOT promise "your old UIC line is obsolete" — frame it as "supplement, not replace"
- DO reference the **feeder compatibility** as a feature: "100% 利旧现有 UIC 飞达" is the single most powerful ROI argument in EU THT reactivation
