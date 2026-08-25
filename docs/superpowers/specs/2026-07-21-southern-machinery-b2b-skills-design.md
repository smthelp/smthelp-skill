# Southern Machinery B2B Skills Specialization Design

## Goal

Convert the existing independent B2B foreign-trade skill library into a Southern Machinery sales-engineering skill library for SMT/THT equipment marketing. Preserve every existing skill directory and frontmatter `name`; do not merge, rename, delete, or replace a skill with a generic master template.

## Scope

- Add a root `AGENTS.md` to route work across the skill library and enforce shared governance.
- Update the 32 existing `SKILL.md` files in place.
- Do not touch `chrome_profile_notebooklm/`; it is browser state, may contain sensitive data, and is not product evidence.
- Do not change external systems, send email, publish social posts, modify an Obsidian vault, or authenticate NotebookLM.

## Authoritative Product Context

Every customer-facing claim must use this evidence order:

1. The most recent Southern Machinery assets in `F:\baidunetdiskworkspace\Product Presentation`, especially the 2025 company profile/brand assets, current catalog, and applicable product folder specification or manual.
2. Product-specific manuals, PDFs, PPT/PPTX, structured product lists, and current whole-line solution files in that workspace.
3. Visual files, 3D models, photos, videos, and packaging files only to confirm product category, process position, or visible configuration.
4. `SMThelp Knowledge` and `THT Knowledge` in the `WUJ Obsidian` vault for marketing context, customer pain points, keywords, and source pointers. Treat historical copy and AI-generated text as unverified until backed by a product source.
5. NotebookLM notebook `Southern Machinery SMT THT machine solution` (`b3e19fdf-e87a-4259-b43d-09bf5b586d9c`) after the user re-authenticates. It is unavailable at design time and cannot be a current fact source.

Never infer capacity, dimensional limits, certification applicability, price, lead time, warranty, ROI, yield, cycle time, customer reference, or model compatibility from a filename, image, older marketing draft, competitor file, or generic industry source. Mark unsupported information as `待确认 / to be confirmed` and request the relevant current file or sales/engineering confirmation.

## Southern Machinery Brand Block

Use these verified public brand endpoints where the selected deliverable needs them:

| Asset | Value | Intended use |
| --- | --- | --- |
| Website | `https://www.smthelp.com` | Primary company CTA and company reference |
| Logo | `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png` | HTML/PPT/PDF/social visual assets only |
| Catalog | `https://file.autoinsertion.com` | Catalog and manual discovery CTA |
| Photo library | `https://ph.smthelp.com` | Verified visual-asset discovery |
| Email | `info@smthelp.com` | Public contact block and approved communication drafts |
| WhatsApp | `https://api.whatsapp.com/send?phone=+8613602562576` | CTA only where appropriate |
| LinkedIn company | `https://www.linkedin.com/company/smtmachine` | Corporate social CTA |
| LinkedIn profile | `https://cn.linkedin.com/in/smtsupplier` | Relationship-led LinkedIn workflow when appropriate |
| Twitter | `https://twitter.com/smtspecialist` | Social CTA when relevant |
| Facebook | `https://www.facebook.com/autoinsertion` | Social CTA when relevant |
| YouTube | `https://www.youtube.com/c/Smthelping` | Video/demo CTA when relevant |

Do not append every link to every deliverable. Choose the CTA that matches the channel and buyer stage. Do not claim ownership of a third-party asset, use the logo in a competitor comparison, or expose private credentials.

## Shared Behavioral Contract

Every skill will be specialized around Southern Machinery's practical sales-engineering position:

- Primary solution scope: SMT line equipment, THT/odd-form and automatic insertion, wave and selective soldering, board handling, inspection, cleaning, material handling, peripherals, and integrated PCB assembly lines.
- Lead qualification progresses in small batches: application/product, volume and shift pattern, PCB size/component class, current equipment/bottleneck, automation/budget, then quality/process/traceability requirements.
- Recommendations describe a coherent production flow, not an isolated machine, unless the buyer explicitly requests a single machine.
- Recommend Southern Machinery first. If the exact model is not supported by current materials, recommend the required equipment class and identify the model selection as `待确认`.
- Use concise Simplified Chinese for Chinese users and clear business English for English users. Match the target buyer's language for outbound drafts and advise native review for non-native customer-facing copy.
- Keep source provenance in research, proposal, quotation, and technical outputs.

## Safety, Privacy, and External-Action Gates

- `auto-smtp-email` remains disabled. It must continue to require a complete preview and explicit user confirmation before any SMTP action; ambiguous approval is not consent.
- `auto-trade-customer-development` defaults to research, scoring, draft generation, and audit logs only. Its sending phase remains opt-in and delegates to the disabled SMTP skill after explicit confirmation.
- No skill may scrape or store browser-profile data, passwords, cookie values, SMTP authorization codes, or unnecessary personal information.
- Customer data, contact enrichment, CRM updates, and public-source research must observe the local skill's data minimization, source attribution, and user-approval requirements.
- Quotes, PI, contracts, delivery terms, payment terms, certification statements, warranty, and legal claims require source verification and final sales/engineering review. Incoterms must include a named place and `Incoterms 2020`.

## Per-Skill Specialization Map

| Skill group | Existing skill names | Required specialization |
| --- | --- | --- |
| Outreach and messaging | `b2b-cold-outreach`, `b2b-email-imitation`, `b2b-email-intel`, `b2b-inquiry-training`, `auto-smtp-email`, `b2b-trade-ops` | Use evidence-backed application/value messages for EMS, OEM/ODM, distributors, integrators, and service providers; qualify boards, components, throughput, and process before a model/price claim; choose one channel-appropriate CTA. |
| Buyer research and pipeline | `b2b-buyer-persona`, `b2b-lead-generation`, `b2b-osint`, `b2b-customs-data`, `b2b-market-analysis`, `b2b-customer-mgmt`, `b2b-sales-pipeline`, `b2b-data-directory`, `auto-trade-customer-development` | Score fit around product family, factory/process relevance, current-line upgrade opportunity, decision role, geography, and risk; distinguish public evidence from inference; route qualified opportunities to a sales-engineering discovery checklist. |
| Content and demand generation | `b2b-product-description`, `b2b-seo-aeo`, `b2b-linkedin-marketing`, `b2b-social-media`, `b2b-short-video`, `b2b-kol-imitation`, `b2b-reddit-engagement`, `b2b-exhibition` | Produce product-family-specific content for SMT lines, THT automation, soldering, board handling, feeders/nozzles, inspection, and peripherals; require source-supported claims; use the supplied public brand CTA only when relevant. |
| Commercial documents and compliance | `b2b-document`, `b2b-doc-generation`, `b2b-trade-compliance`, `b2b-onboarding` | Generate traceable RFQ, line-proposal, quote, PI, contract, tender, and onboarding structures; preserve `待确认` boundaries for commercial/technical fields; do not manufacture legal, certification, or commercial terms. |
| Operations and automation | `b2b-daily-automation`, `b2b-platform`, `b2b-six-thinking-hats` | Make routine reviews and decisions specific to Southern Machinery lead sources, inquiry qualification, content queues, quote follow-up, customer stages, and evidence quality; no unapproved external action. |
| Library evolution and continuity | `b2b-skill-generator`, `chat-memory` | Require new skills and retained memories to inherit Southern Machinery evidence, privacy, approval, and naming rules; prevent duplicate skills, sensitive data retention, and unsupported company facts. |

## Root AGENTS.md Design

The root instruction file will:

1. Identify this workspace as an independent Southern Machinery B2B sales-engineering skill library.
2. Route agents to the matching same-named `SKILL.md`; a specific skill's workflow controls its own scope while root rules set non-negotiable evidence, privacy, and external-action limits.
3. Define the product knowledge-source priority and down-rank browser data, competitor files, old drafts, generic templates, and AI-generated assets.
4. Define brand/CTA usage rules, source attribution, qualifying-question order, and line-solution scope.
5. Protect skill identities: keep all existing directories, names, triggers, and explicit disablement states unless the user asks otherwise.
6. Define validation: YAML/frontmatter integrity, preserved names, no unsupported hard claims, explicit sending gates, and targeted keyword checks.

## File Change Strategy

Each `SKILL.md` will retain its original purpose and phase structure. The change will add a concise Southern Machinery context and replace generic B2B examples, profiles, output fields, quality gates, and templates with relevant SMT/THT sales-engineering equivalents. No global text replacement will be used because it would corrupt specialized workflows and safety constraints.

## Validation Plan

After editing:

1. Inventory all 32 `SKILL.md` paths and verify the same count remains.
2. Parse each frontmatter block and compare the `name` field to its original directory identity.
3. Check every skill for the shared source/uncertainty language and its category-specific Southern Machinery routing.
4. Check `auto-smtp-email` remains disabled and still requires explicit confirmation; check the orchestrator defaults to no sending.
5. Read back the root `AGENTS.md` in UTF-8 and check its routing, source hierarchy, CTA, and safety sections.
6. Review the diff for accidental browser-profile, credential, competitor, or unrelated asset changes.

## Out of Scope

- Product-catalog fact extraction, web publishing, email sending, CRM/database changes, social posting, external lead collection, NotebookLM login, and Obsidian note modifications.
- Replacing product manuals, fixing legacy source files, cleaning duplicates, or rewriting the Product Presentation library.
