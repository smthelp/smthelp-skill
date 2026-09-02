# Southern Machinery B2B Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Specialize every existing B2B skill for Southern Machinery's SMT/THT equipment foreign-trade marketing while preserving all skill identities and external-action safeguards.

**Architecture:** A root `AGENTS.md` establishes immutable product-evidence, privacy, brand-CTA, qualification, and approval rules. Each same-named `SKILL.md` then retains its individual workflow but replaces generic B2B inputs, examples, outputs, and quality gates with Southern Machinery sales-engineering behavior.

**Tech Stack:** Markdown with YAML frontmatter, PowerShell validation, existing Southern Machinery Product Presentation knowledge library, WUJ Obsidian reference notes.

## Global Constraints

- Keep all 32 directories and every existing frontmatter `name` unchanged; do not merge or rename skills.
- Do not modify `chrome_profile_notebooklm/` or use it as evidence.
- Prefer current Southern Machinery product materials in `F:\baidunetdiskworkspace\Product Presentation`; label unsupported facts `待确认 / to be confirmed`.
- Preserve `auto-smtp-email` as disabled and require complete preview plus explicit confirmation before any sending action.
- No external sending, publishing, CRM/database mutation, NotebookLM login, or Obsidian write is in scope.
- Use only relevant public brand CTAs: `https://www.smthelp.com`, `https://file.autoinsertion.com`, `https://ph.smthelp.com`, `info@smthelp.com`, `https://api.whatsapp.com/send?phone=+8613602562576`, and supplied social channels.

---

### Task 1: Create Root Governance

**Files:**
- Create: `AGENTS.md`
- Reference: `docs/superpowers/specs/2026-07-21-southern-machinery-b2b-skills-design.md`

**Interfaces:**
- Consumes: Southern Machinery product-source hierarchy and public brand assets from the approved design.
- Produces: Root-level instructions that every `SKILL.md` inherits without changing its identity.

- [ ] **Step 1: Write the governance acceptance checklist**

Create the checklist in the working notes before drafting: product source order; no-invention rule; browser-profile exclusion; relevant CTA-only rule; user confirmation gate for external actions; existing skill names/disablement preservation; skill-local workflow precedence.

- [ ] **Step 2: Confirm the checklist is not already implemented**

Run: `Test-Path -LiteralPath 'AGENTS.md'`

Expected: `False` or an explicit decision to patch, not overwrite, an existing root instruction file.

- [ ] **Step 3: Write `AGENTS.md`**

Include sections for project role, authoritative source order, product/line scope, qualification order, brand assets and CTA selection, privacy/external-action gates, child-skill routing, source-file handling, and validation. State that a local `SKILL.md` controls its specific workflow but cannot weaken root evidence or approval rules.

- [ ] **Step 4: Validate root governance**

Run: `Get-Content -LiteralPath 'AGENTS.md' -Encoding UTF8` and targeted `Select-String` checks for `待确认`, `auto-smtp-email`, `chrome_profile_notebooklm`, `SMThelp`, `file.autoinsertion.com`, and `explicit confirmation`.

Expected: Every required governance boundary is present and readable in UTF-8.

### Task 2: Specialize Prospecting, Research, and Pipeline Skills

**Files:**
- Modify: `b2b-buyer-persona/SKILL.md`
- Modify: `b2b-lead-generation/SKILL.md`
- Modify: `b2b-osint/SKILL.md`
- Modify: `b2b-customs-data/SKILL.md`
- Modify: `b2b-market-analysis/SKILL.md`
- Modify: `b2b-data-directory/SKILL.md`
- Modify: `b2b-customer-mgmt/SKILL.md`
- Modify: `b2b-sales-pipeline/SKILL.md`
- Modify: `auto-trade-customer-development/SKILL.md`

**Interfaces:**
- Consumes: Root evidence rules and public/company-provided buyer information.
- Produces: Source-attributed, risk-aware, sales-engineering-qualified prospects and handoffs.

- [ ] **Step 1: Capture original names and safety clauses**

Read each file's YAML frontmatter and its existing data/sending instructions. Record the exact `name` values and the orchestrator's default send behavior for post-edit comparison.

- [ ] **Step 2: Add Southern Machinery buyer-fit dimensions**

For every file, add product-family and process relevance: EMS/OEM/ODM/distributor/integrator/service-provider fit; SMT/THT process; line upgrade/new-line opportunity; PCB and component characteristics; volume/shift pattern; current equipment/bottleneck; automation and budget; quality/traceability needs. Require public-source attribution and label inference.

- [ ] **Step 3: Make pipeline handoff concrete**

Require qualified outputs to recommend the next smallest discovery question or a product-family/line-solution route. Do not choose exact equipment models without current product evidence.

- [ ] **Step 4: Preserve the orchestrator's external-action gate**

In `auto-trade-customer-development/SKILL.md`, retain `自动发送` defaulting to no, preserve preview/explicit confirmation, and specify that research, scoring, and drafts may complete without any message being sent.

- [ ] **Step 5: Validate the batch**

Run a frontmatter name comparison and targeted searches for `Southern Machinery`, `SMT`, `THT`, `待确认`, `source`, and `确认发送` in the nine files.

Expected: Names are unchanged, every skill is SMT/THT-specific, and no sending gate was weakened.

### Task 3: Specialize Outreach, Inquiry, and Trade-Operations Skills

**Files:**
- Modify: `b2b-cold-outreach/SKILL.md`
- Modify: `b2b-email-imitation/SKILL.md`
- Modify: `b2b-email-intel/SKILL.md`
- Modify: `b2b-inquiry-training/SKILL.md`
- Modify: `b2b-trade-ops/SKILL.md`
- Modify: `auto-smtp-email/SKILL.md`

**Interfaces:**
- Consumes: A prospect or inquiry with evidence, stage, and product/line context.
- Produces: Channel-appropriate drafts, qualification questions, and approved follow-up workflows.

- [ ] **Step 1: Preserve original mailing and follow-up safeguards**

Read the current preview, explicit-consent, anti-spam, unsubscribe, and logging clauses. Keep `auto-smtp-email` frontmatter description and disabled status unchanged.

- [ ] **Step 2: Replace generic content patterns**

Add Southern Machinery messaging patterns for complete SMT/THT lines, wave/selective soldering, board handling, feeders/nozzles, inspection, cleaning, and upgrade/retrofit discussions. Require one product-relevant observation or a clearly generic opening; prohibit invented model/spec/customer proof.

- [ ] **Step 3: Add sales-engineering inquiry gates**

Use small-batch questions: application, monthly/shift demand, PCB dimensions/component mix, existing line/process bottleneck, automation/budget, and quality/traceability. For quote/model requests, defer unsupported fields to `待确认`.

- [ ] **Step 4: Add CTA selection rules**

Use the company website for a general company CTA, catalog for manuals/products, photo library for visual reference, YouTube for a relevant demo, and email/WhatsApp only where a direct-contact CTA is appropriate. Never append all links by default.

- [ ] **Step 5: Validate outreach behavior**

Search all six files for `Southern Machinery`, `SMThelp`, `待确认`, `preview`, `explicit confirmation`, and at least one relevant public CTA. Confirm the SMTP file still states disabled and requires explicit user consent.

### Task 4: Specialize Content, SEO, Social, Video, and Exhibition Skills

**Files:**
- Modify: `b2b-product-description/SKILL.md`
- Modify: `b2b-seo-aeo/SKILL.md`
- Modify: `b2b-linkedin-marketing/SKILL.md`
- Modify: `b2b-social-media/SKILL.md`
- Modify: `b2b-short-video/SKILL.md`
- Modify: `b2b-kol-imitation/SKILL.md`
- Modify: `b2b-reddit-engagement/SKILL.md`
- Modify: `b2b-exhibition/SKILL.md`

**Interfaces:**
- Consumes: A verified product source, target buyer, region/language, channel, and desired business outcome.
- Produces: Claim-safe, channel-specific Southern Machinery marketing drafts and content plans.

- [ ] **Step 1: Add product-family selection**

Require a content request to identify one supported family or a broad solution: SMT line, THT/odd-form insertion, wave/selective soldering, board handling, inspection, cleaning, feeders/nozzles, material handling, or peripherals. Reject ungrounded model-specific copy by requesting source material.

- [ ] **Step 2: Add evidence and visual-use rules**

Require the source file/path or catalog reference for technical claims. Permit logo and `ph.smthelp.com` images only in appropriate visual deliverables, with no claim inferred solely from image appearance.

- [ ] **Step 3: Replace generic buyer language and examples**

Tailor personas, problem statements, keywords, hooks, event questions, and CTAs to EMS, OEM/ODM, PCB assemblers, distributors, system integrators, and service providers. Cover process stability, labor, changeover, integration, inspection, and expandable automation without unsupported numeric promises.

- [ ] **Step 4: Add channel-specific CTA routing**

Use LinkedIn company/profile, YouTube, Facebook, Twitter, catalog, website, email, or WhatsApp only when appropriate to the platform and stage. Prohibit fabricated engagement, testimonials, views, follower counts, or customer deployments.

- [ ] **Step 5: Validate content batch**

Check all eight files for source-bound claim language, `Southern Machinery`, product-family routing, relevant CTA rules, and `待确认` handling.

### Task 5: Specialize Documents, Compliance, and Onboarding Skills

**Files:**
- Modify: `b2b-document/SKILL.md`
- Modify: `b2b-doc-generation/SKILL.md`
- Modify: `b2b-trade-compliance/SKILL.md`
- Modify: `b2b-onboarding/SKILL.md`

**Interfaces:**
- Consumes: Current source files, customer requirements, commercial inputs, and verification status.
- Produces: Traceable RFQs, line proposals, quotations, PI/contracts, tender responses, and onboarding materials.

- [ ] **Step 1: Add equipment-line document structures**

Add RFQ/proposal sections for product application, PCB/part details, volume, line flow, process/inspection requirements, utilities/interface constraints, automation level, layout, assumptions, and confirmation items.

- [ ] **Step 2: Require source provenance and uncertainty flags**

Put a source/verification column or section in technical and commercial outputs. Any price, lead time, payment, warranty, certification, exact spec, or final model without current support remains `待确认` and requires sales/engineering sign-off.

- [ ] **Step 3: Apply formal trade and language gates**

Keep each trade term as `named place + Incoterms 2020`; retain translation review, tender-format, and market compliance checks. Never turn general regulatory guidance into a certification claim.

- [ ] **Step 4: Validate document/compliance batch**

Search for `Incoterms 2020`, `待确认`, `source`, `Southern Machinery`, and commercial-final-review language. Verify existing document generation references remain intact.

### Task 6: Specialize Daily Operations, Platform, and Decision Skills

**Files:**
- Modify: `b2b-daily-automation/SKILL.md`
- Modify: `b2b-platform/SKILL.md`
- Modify: `b2b-six-thinking-hats/SKILL.md`

**Interfaces:**
- Consumes: Work queues, approved research, lead stage, content status, and open sales-engineering questions.
- Produces: Internal review, prioritization, and decision artifacts with no unauthorized external actions.

- [ ] **Step 1: Convert generic activity queues**

Use Southern Machinery queues: inquiry qualification, source verification, RFQ/line proposal preparation, content review, demo/catalog follow-up, customer stage progression, and overdue confirmation items.

- [ ] **Step 2: Add safe decision frameworks**

Require every decision to identify evidence, unknowns, downside/risk, and next validation action. Separate internal recommendation from customer-facing promise.

- [ ] **Step 3: Validate operational batch**

Check all three files for `Southern Machinery`, `SMT`, `THT`, source/unknown handling, and no automatic send/publish/database mutation language.

### Task 7: Specialize Skill Evolution and Long-Term Memory

**Files:**
- Modify: `b2b-skill-generator/SKILL.md`
- Modify: `chat-memory/SKILL.md`

**Interfaces:**
- Consumes: A proposed new capability or a user request for prior confirmed context.
- Produces: Governed additions and privacy-safe contextual retrieval.

- [ ] **Step 1: Add inheritance requirements to the skill generator**

Require new skills to preserve non-overlap checks, current-name stability, Southern Machinery product source hierarchy, no-invention clauses, relevant CTA controls, privacy constraints, and approval gates. Do not register or restart a service unless explicitly requested.

- [ ] **Step 2: Add memory minimization**

Require `chat-memory` to retrieve only relevant historical context and never persist or expose credentials, browser session data, authorization codes, private customer details, or transient search results. Treat recalled commercial and technical claims as needing current-source verification.

- [ ] **Step 3: Validate continuity batch**

Check both files for product-source inheritance, explicit privacy exclusions, no external-action default, and unchanged frontmatter names.

### Task 8: Perform Whole-Library Structural and Behavior Validation

**Files:**
- Verify: `AGENTS.md`
- Verify: all 32 `*/SKILL.md` files

**Interfaces:**
- Consumes: Edited root governance and all preserved same-named skills.
- Produces: A validation report suitable for handoff.

- [ ] **Step 1: Verify file count and identities**

Run a PowerShell inventory of `SKILL.md` files and compare against the original 32 names. For each, read the YAML block and assert `name` matches the pre-edit value.

- [ ] **Step 2: Verify shared contract coverage**

Search all skills for Southern Machinery/SMT/THT context, source/verification language, `待确认`, and each category's required route. Manually inspect any file whose output lacks the expected keyword because a synonym may be valid.

- [ ] **Step 3: Verify hard safety gates**

Confirm `auto-smtp-email` still says disabled and requires preview/explicit confirmation. Confirm `auto-trade-customer-development` defaults to no sending. Confirm no changed file mentions using `chrome_profile_notebooklm` as an input or evidence source.

- [ ] **Step 4: Verify root governance and diff scope**

Read `AGENTS.md` in UTF-8, inspect its product-source hierarchy and brand URLs, then review the working-tree diff. Expected changes are exactly root governance, the 32 intended `SKILL.md` files, and the approved design/plan documents.

- [ ] **Step 5: Report results**

Report preserved skill count and names, changed paths, validation commands/results, any `待确认` boundaries added, and the NotebookLM authentication limitation. Do not claim product or commercial facts beyond cited source scope.
