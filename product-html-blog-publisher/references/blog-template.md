# Blog Template & SEO Field Rules

English, 1,000–1,500 words, Dan Koe 6-step flow, GEO+SEO/AEO optimized. Audience: global EMS / ODM / automotive / medical / industrial-control buyers and manufacturing engineers.

## Hard heading rule

The words **Hook, Diagnosis, Vehicle, Loop, CTA must NOT appear in any heading** (user rule, 2026-09-02). Keep the 6-step *logic* but title sections naturally. Verified-safe example (S-EPCOS post):

| 6-step role | Natural heading used |
|---|---|
| Hook | "One Operator, 1,000 Shaped Capacitors Per Hour" |
| Diagnosis | "Why Hand-Forming Fails Your Through-Hole Line" |
| Framework | "The 8-Station Cycle to Judge Any Forming Machine" |
| Vehicle | "The S-EPCOS Capacitor Lead Cut & Forming Machine" |
| Loop | "From Drawing to Running Line in Five Steps" (+ next-post teaser sentence) |
| CTA | "Send Your Drawing for a Tooling Review" |

## Skeleton

```markdown
# <Main keyword> by Southern Machinery

**What is <machine> used for?** <2-3 sentence direct answer: what it does, headline number, one-operator context, built-to-drawing point.> (AI-overview quotable)

![<main keyword + product category>](<validated coverImage>)

## <Hook: counter-intuitive claim / data / pain scenario>            (keyword in first 100 words)

## <Diagnosis: the reader's hidden cost, "this is us"> 
### <failure mode 1> 
### <failure mode 2>

## <Framework: reusable checklist / evaluation model>
1. **<station/step 1>** — <what/why>
2. ... (numbered, machine-mappable)
### Selection parameters that actually matter  (input checklist buyers must pin down)

## <Vehicle: the product>
### <differentiator, evidence from source (drawing/project reference)>
![<inline image>](<validated url>)
### <Model> key specifications (from the technical agreement)
| Parameter | Value |
|---|---|        (every value verbatim from source; suspicious values keep source's flag)
### Where it sits in your PCB assembly line  (internal links: verified www.smthelp.com pages only)
### The ROI math (example — depends on configuration)
```
<formula lines>
```
Example (illustrative only ... subject to final technical confirmation): <worked example with explicit assumptions; missing data = "not specified in source — contact Southern Machinery to confirm">

## <Loop: repeatable path / series hook>  (5-step process from source + next-post teaser)

## FAQ: What Buyers Ask Before Ordering
**<Q1 from source FAQs>** <A>
**<Q2>** <A>        (4–6 pairs, schema-ready, all from source doc)

## <CTA: exact next action>
Email/WhatsApp + drawing + volume → tooling review & quote; links: quote page, file.autoinsertion.com, ph.smthelp.com, about page. "Your Shenzhen-based SMT & THT equipment partner since 2011."
```

## SEO/API field rules

| Field | Rule |
|---|---|
| `title` | Main keyword front-loaded + product category/model + "by Southern Machinery" |
| `seoTitle` | ≤60 chars, `"Main keyword | Southern Machinery"` |
| `seoDescription` | 140–160 chars, buyer-intent (cost/yield/delivery/line-integration) |
| `slug` | lowercase-hyphen, main keyword/product category, unique vs all state-file slugs; conflict → add model/use suffix |
| `excerpt` | 80–160 words, AI-quotable summary: labor saving, quality stability, line-integration value |
| `tags` | pick from: SMT Line, THT Automation, Wave Soldering, Board Handling, PCB Assembly Automation, EMS Manufacturing, Factory ROI, Terminal Insertion, Odd Form Insertion |
| `locale` | `en` |
| `status` / `source` | `published` / `ai` |

Keyword rules: main keyword in H1 + first 100 words + ≥1 H2; LSI terms natural spread; no stuffing.

Link discipline: only verified official pages — www.smthelp.com product/line pages (verify HTTP 200 first), file.autoinsertion.com, ph.smthelp.com. Never invent URLs. Log every verified link in the run.

Brand facts allowed anywhere: Shenzhen manufacturer since 2011; 237+ global customers; complete SMT/THT/wave/board-handling/inspection line capability; global service, spare parts, training. No invented specs/prices/certs/ROI/cases.

## 14-item quality gate (self-check before POST)

Title / Meta description / Keywords / URL slug / H1–H3 hierarchy / image Alt (keyword+category) / UX readability / FAQ schema-ready / canonical present (CMS handles) / OG (CMS) / Twitter Card (CMS) / breadcrumb internal links / alternate-keyword coverage / content richness — plus ≥1 citable data point or comparison table, plus images: 1 coverImage + 2–4 inline, all pre-validated HTTP 200 `image/*`.
