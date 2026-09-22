# Research Recipe — When Web Search Fails

## Why this exists

In the 2026-06-04 E.G.O. Spain session, **every** traditional search engine blocked the research subagent or returned noise:

- **Google** → JS-rendered, no text result extracted via curl
- **Bing HTML + RSS feed** → returned totally unrelated content (e.g., "e - Euler's number")
- **DuckDuckGo HTML** → bot challenge page blocking automated fetch
- **Subagent research (`delegate_task` with broad scope)** → timed out at 600s with 29-34 API calls, no result

The fallback that worked: **direct `curl` on known source URLs**. This document captures the recipe.

## The 5-tier URL priority list

For any dormant customer, fetch in this order:

### Tier 1 — Customer's official site (always first)

```
curl -sL --max-time 30 "https://www.{{customer-domain}}/en/company/sites/{{country}}"
curl -sL --max-time 30 "https://www.{{customer-domain}}/en/products"
curl -sL --max-time 30 "https://www.{{customer-domain}}/en/company/about"
```

What to extract:
- **Mission statement** → frame the customer's identity for section 1
- **Product categories** → identify the THT-heavy product lines (motor control, power electronics, etc.)
- **Certifications listed in footer** (ISO 9001, 14001, 50001, IATF 16949) → trust anchors for section 1 + section 3
- **Contact hierarchy** (HR, Procurement, Engineering) → section 4 email target

### Tier 2 — Customer's parent group site

```
curl -sL --max-time 30 "https://www.{{parent-domain}}/en/company"
```

Extract: group structure (subsidiaries, divisions), recent group press releases, group-level strategy shifts (e.g., Blanc & Fischer's 5 subgroups).

### Tier 3 — Customer's careers page (this is the gold mine)

```
curl -sL --max-time 30 "https://www.{{customer-domain}}/en/career/job-vacancies?country={{country}}"
curl -sL --max-time 30 "https://www.{{customer-domain}}/de/karriere/stellenangebote?tx_solr[filter][0]=country:Germany"
```

**Why this is the best capex signal**: when a factory posts engineering jobs for "Production Engineer — THT," "Process Specialist — Wave Soldering," "MES / Industry 4.0 Lead," they are 1:1 signaling capex intent in exactly those areas. Map each open role to a Southern Machinery product line in section 3.

### Tier 4 — Southern Machinery's own catalog

```
curl -sL --max-time 30 "https://www.smthelp.com/product-category/tht-machine"
curl -sL --max-time 30 "https://www.smthelp.com/product-category/feeder"
curl -sL --max-time 30 "https://www.smthelp.com/product-category/peripheral-equipment"
```

Use as the spec baseline for section 3 product recommendations. Do NOT fabricate specs; if not listed on smthelp.com, write "我会在确认后提供具体选型" in the brief.

### Tier 5 — PO archive (internal context)

Already injected in the conversation as `<source id="1">`, `<source id="2">`, `<source id="3">` blocks. Extract:

- **PO number + date** → cite in email subject or body as proof of past relationship
- **Items purchased** → e.g., "UIC Auto Insertion Spare Parts" → feeds the legacy hook pattern
- **PO terms / credit-note clauses** → these reveal the customer's quality regime (strict credit terms = IATF-style supplier quality management)

## Local-market research (the tier that DOES work for this)

Instead of searching for "Spain EMS labor cost 2025," rely on the **agent's own knowledge cutoff (Jan 2026)** for these well-known facts:

- Spain manufacturing labor cost 2025-2026: **€18-22/hr base, €28-32/hr fully loaded** (Catalonia)
- EU ESPR (Ecodesign for Sustainable Products Regulation) entered force 2024
- EU Right to Repair Directive effective 2021, scope expanding 2025-2027
- IATF 16949:2016 still the automotive EMS standard
- ISO 50001 energy management → drives Reflow Oven / Wave Soldering energy audits

Write these as confident facts, citing "based on industry knowledge" if no specific URL is verified. Do NOT pretend you searched and found them.

## Anti-patterns (what NOT to do)

- ❌ `delegate_task` with `goal="research E.G.O. and the Spanish EMS market"` → guaranteed 600s timeout
- ❌ `curl` Bing/Google/DuckDuckGo without proper headers → useless noise
- ❌ Fabricating PO numbers or ISO cert years the customer doesn't have
- ❌ Using the customer's competitor as a "case study" without verifying
- ❌ Skipping the careers page — it gives the cleanest capex signal with no search required
