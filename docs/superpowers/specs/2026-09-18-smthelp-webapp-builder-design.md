# smthelp-webapp-builder Design

## Purpose

Create one reusable skill for building Southern Machinery's outward-facing web assets — either a multi-file hash-routed SPA deployed as a site, or a single-file build-based HTML deliverable attached to a customer email. The skill carries the brand design system, the GEO requirements, the Chatwoot widget, the dark/light theme and the 7-language i18n pattern, and the verification discipline that proves a page is correct rather than merely plausible.

## Architecture

`SKILL.md` is deliberately self-contained: routing, brand tokens, asset endpoints, both delivery variants, and the verification suite all live in one file, so an invocation never needs a second read before work can start.

```text
SKILL.md
  §一     architecture decision (SPA vs single file)
  §二     brand design tokens
  §三     reusable asset endpoints
  §四     Chatwoot widget (fixed snippet)
  §五     GEO and copy rules, structured-data visibility
  §六     local-environment pitfalls, 19 entries, all measured
  §七     pre-delivery verification checklist
  §八     GitHub Pages deployment and custom domain
  §九     delivery checklists
  §十     theme switching + i18n pattern
  §十一   single-file variant: build pipeline and its verification suite
```

## Requirements

- Directory display name `smthelp-webapp-builder`; two delivery variants chosen by an explicit judgement table, not by preference.
- The single-file variant keeps build sources separate from the artefact and rebuilds idempotently from `template.html`; the artefact is never hand-edited.
- English body text is pre-rendered into static markup, because a `data-i18n`-empty page is an empty page to a crawler that does not run JavaScript.
- Structured data has visible on-page counterparts. FAQ answers come from one dictionary shared by the JSON-LD and the visible `#faq` section, so the two cannot drift.
- Verification is five classes: static assertions, external links, visual, in-page runtime, and falsification. An assertion that cannot fail is not an assertion.
- Every local-environment pitfall is recorded together with the measurement that established it, never as folklore. Where a previous belief was later falsified, the correction replaces the belief.

## Validation

- The reference build passes `validate.py`, and `falsify.py` confirms each deliberate mutation is caught by the expected assertion rather than by an unrelated one.
- `checklinks.py` reports no dead link outside the documented whitelist, and every embedded video ID matches the published board.
- Responsive breakpoints are verified by measurement in the widest language, not estimated from English.

## Known Deviation

`quick_validate.py` reports `Unexpected key(s) in SKILL.md frontmatter: agent_created, author, category, triggers, version`, because the official schema allows only `allowed-tools, description, license, metadata, name`. These legacy flat keys are shared by the other `smthelp-*` skills in this repository, and the skill is in active use.

Decision: the frontmatter is left as authored. Rewriting working keys to satisfy a validator that most sibling skills also fail would risk breaking skill matching for no functional gain. A future repository-wide migration of the `smthelp-*` skills to `metadata:` should move all of them together, not just this one.
