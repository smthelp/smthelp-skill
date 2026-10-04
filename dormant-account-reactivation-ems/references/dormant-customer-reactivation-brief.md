---
name: dormant-customer-reactivation-brief
description: Use when Jason or the sales team needs to reactivate a dormant/lost EMS customer with a full 4-section KAM reactivation deliverable.
archived: 2026-06-14
absorbed_into: sales-engineering/dormant-account-reactivation-ems (as §2)
---

# Dormant Customer Reactivation Brief

> **Archived 2026-06-14**: This skill was merged into `dormant-account-reactivation-ems` as §2. The canonical skill for dormant EMS customer reactivation is `dormant-account-reactivation-ems`.

## When to invoke this skill

Use this when the request is for a **full reactivation package** on a specific named dormant customer, NOT just a single email. Typical signals:

- A customer (European white-goods OEM, automotive Tier-1, industrial EMS, etc.) historically bought spare parts or a small line from Southern Machinery **2-10 years ago** and has gone silent since
- User provides: customer name + location + historical PO record + a contact person
- User expects a 4-section deliverable combining **market intel + pain-point diagnosis + whitepaper outline + multi-channel outreach copy**
- The deliverable is **bilingual**: Chinese for technical analysis, English for the outreach copy that goes to the prospect

If the user only wants a single cold/breakup email (not the full 4-section brief), defer to `jason-email-skill` section 4.7 instead.

## The mandatory 4-section structure

1. **🌐 一、客户背景与所在地 EMS 市场深度洞察 (Market Intelligence)**
2. **🚨 二、痛点与升级难点诊断 (Gap Analysis)**
3. **📄 三、专属行业技术白皮书大纲 (Tailored Solution Brief)**
4. **✉️ 四、高转化率多渠道复联话术 (Outreach Assets)**

## Key content unique to this skill (now in dormant-account-reactivation-ems §2)

### Reverse-flow waybill hook
When the dormant customer previously shipped something TO you, the waybill/shipping record is a **stronger reactivation hook than your own PO archive**.

### India / APAC specific patterns
- THT is GROWING in India, not declining
- CCTV/SMPS/power supply = 80% THT by component count
- India labor cost baseline: $4,500-5,500/operator/year
- E-Waste Management Rules 2022 + BIS certification = regulatory tailwind
- PLI scheme = capacity expansion tailwind

### M2M Bulgaria corrections (2026-06-08)
- S3000 speed: NEVER quote 20,000 CPH — real-world is 10,000-12,000 CPH
- Manufacturing model verification MANDATORY before pitching THT equipment
- EU market: ALWAYS add CE declaration + EU customs clause
- S-70LD first for alarm/relay/connector-heavy products, not S3000

See the canonical skill `dormant-account-reactivation-ems` for the full content.
