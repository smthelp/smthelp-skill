# S-3000 Radial Inserter — CPH Verification Record

## The Problem

Multiple internal documents cited **18,000 CPH** for the S-3000 radial inserter.
This figure is WRONG for radial (through-hole) insertion use cases.
Using it in prospect-facing documents damages engineer credibility.

## The Correction

| Claim | Correct Value | Context |
|-------|--------------|---------|
| S-3000 throughput | **10,000–12,000 CPH** | Production-realistic radial insertion speed |
| 18,000 CPH | **WRONG for S-3000** | That is the theoretical maximum for AXIAL (S-4000) components only |

## Source of the Error

The 18,000 CPH figure originated from catalog marketing copy that
did not distinguish between:
- **Axial insertion** (components fed along their axis — resistors, diodes):
  lower insertion resistance → higher theoretical speed
- **Radial insertion** (components fed from the side — capacitors, LEDs,
  switches): higher insertion resistance → lower real-world speed

Southern Machinery catalog specs:
- S-4000 (axial inserter): 22,000 CPH theoretical — this is the machine
  that can approach 18,000+ CPH under ideal conditions
- S-3000 (radial inserter): 18,000 CPH was stated in some catalog versions
  but represents THEORETICAL MAXIMUM ONLY. Production-realistic speed is
  10,000–12,000 CPH.

## Confirmed Source

- Wiki log (2026-06-29): "wiki `index.md` 写'4,000 CPH'为保守宣传值；
  NotebookLM 源（084 号笔记）记 S7900IV 实测 4,700 件/小时（继电器），
  理论极限 0.7s/件 ≈ 5,142/hr。白皮书采用 4,700/hr 较准确。"
- S-3000 entity file confirms: "S3000 PCB Dip Assembly Radial Insertion Machine"
- Anti-hallucination checklist (s-7900-verified-specs.md): explicitly
  calls out "S-3000 (radial) is 10,000–12,000 CPH real production speed
  — NOT the S-7900 figure"

## Verified S-Series Speed Reference Table

| Model | Type | Catalog-Theoretical Max | Production-Realistic |
|-------|------|------------------------|---------------------|
| S-7900 | Odd-form | ~5,000 CPH (0.7s/件极限) | 4,000 CPH |
| S-70LD | Odd-form | ~4,500 CPH | ~4,000 CPH |
| S-4000 | Axial | 22,000 CPH | 18,000–20,000 CPH |
| S-3000 | Radial | 18,000 CPH (AXIAL MAX) | **10,000–12,000 CPH** |
| S-7020T | Terminal | 12,000 CPH | 10,000–12,000 CPH |

## Rule for Future Documents

When citing S-3000 throughput in ANY document (white paper, ROI one-pager,
email, LinkedIn post, spec sheet), always use **"10,000–12,000 CPH"**
and include the qualifier **"production-realistic radial insertion speed"**.

If you encounter 18,000 CPH cited for S-3000 in any existing document,
treat it as an error and correct it before use.
