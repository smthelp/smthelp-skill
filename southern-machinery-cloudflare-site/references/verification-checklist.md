# Verification Checklist

## Repository and Build

- [ ] Project `AGENTS.md` was read and followed.
- [ ] Worktree changes were reviewed and unrelated edits preserved.
- [ ] No secrets, customer records, real passwords, or accidental resource IDs are tracked.
- [ ] Formatting, type checks, tests, and production build pass.
- [ ] Schema and migrations are reviewed.

## UI and Content

- [ ] All eight pages load and are independently navigable.
- [ ] Header, footer, CTAs, canonical/SEO metadata, and contact paths are consistent.
- [ ] Product specifications and quantified claims have sources.
- [ ] Desktop and mobile screenshots show no overlap, clipping, blank media, or unusable controls.
- [ ] Keyboard navigation, focus state, labels, contrast, and form errors are usable.
- [ ] Ad Studio covers empty, loading, success, copy/export, and upstream error states.

## Backend and Security

- [ ] RFQ accepts valid input, rejects malformed/oversized input, and persists correctly.
- [ ] Login rejects wrong credentials without leaking account state.
- [ ] Login page declares its shared API client before page-specific scripts and has no missing-global errors.
- [ ] Valid test login returns the expected role/session without exposing the token in logs.
- [ ] The issued session successfully calls one protected endpoint.
- [ ] Expired, altered, missing, and wrong-algorithm JWTs are rejected.
- [ ] Admin and super-admin permissions are enforced server-side.
- [ ] Inquiry, admin, upload, and webhook APIs reject unauthorized callers.
- [ ] CORS is same-origin or explicitly allowlisted.
- [ ] Upload type, size, filename, and object-key handling are validated.

## Cloudflare Production

- [ ] Authenticated Cloudflare account was confirmed.
- [ ] Binding names match code and resource identifiers match Cloudflare output.
- [ ] D1 tables exist and a controlled read/write check succeeds.
- [ ] R2 and KV bindings can perform their intended operations.
- [ ] Production secret bindings exist without exposing values.
- [ ] Public URL returns expected statuses and rendered content.
- [ ] Custom domain, canonical `pages.dev` domain, and latest deployment-specific URL were compared.
- [ ] The active production deployment source/commit is identified.
- [ ] Root Pages config, Worker bundling config, build command, and output directory agree.
- [ ] Browser console and network panel show no unexplained errors.
- [ ] Representative public and protected API requests behave correctly.
- [ ] Production mobile and desktop screenshots were inspected.

## Handoff

- [ ] Deployment target, URL, resource names, and verification results are reported.
- [ ] Git commit and branch are reported when pushed.
- [ ] The Git-triggered deployment matching the pushed commit was monitored and tested; manual deployment success was not used as a substitute.
- [ ] Remaining manual setup, DNS, secret rotation, or monitoring work is explicit.
- [ ] Temporary diagnostic deployments are removed when authorized.
