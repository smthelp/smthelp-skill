---
name: southern-machinery-cloudflare-site
description: Build, redesign, secure, deploy, troubleshoot, or reproduce a Southern Machinery SMT/THT marketing website on Cloudflare Workers or Pages. Use for an eight-page product site, verified product content, RFQ/admin backends, Ad Studio with an n8n webhook, D1/R2/KV provisioning, custom-domain or login incidents, production hardening, Pages Git deployment verification, or GitHub synchronization.
---

# Southern Machinery Cloudflare Site

Build and ship a production-ready Southern Machinery website while preserving verified product facts, brand positioning, backend security, and repeatable Cloudflare deployment.

## Operating Rules

- Read the repository-level `AGENTS.md` before planning or editing.
- Inspect the repository, current framework, git status, existing Cloudflare files, schemas, and tests before choosing an implementation.
- For substantial work, present a short plan and obtain confirmation when the active project instructions require it.
- Preserve unrelated user changes. Never reset, overwrite, or commit them without authorization.
- Treat product catalogs and repository product data as the source of truth. Do not invent CPH, labor savings, ROI, price, delivery time, certifications, or customer results.
- Never store passwords, password hashes, JWT secrets, API tokens, customer data, Cloudflare account IDs, or deployment-specific UUIDs in this skill or committed configuration.
- Do not deploy, provision cloud resources, initialize a production database, or push Git changes unless the user requested that external change.

## Select the Workflow

1. **Build or redesign only:** follow Discovery, Content, UX, Implementation, and Local Verification.
2. **Secure an existing app:** inspect auth, authorization, CORS, uploads, secrets, and database access; then follow `references/architecture-and-security.md`.
3. **Deploy only:** verify the build and bindings, then follow `references/cloudflare-deployment.md`.
4. **Full delivery:** execute all phases in order and finish with production verification and GitHub synchronization.

## Phase 1: Discover

1. Read `AGENTS.md`, package scripts, source routes, schema, Wrangler configs, README files, and design assets.
2. Identify the stack and reuse local patterns. Do not replace a working framework merely to match an example.
3. Inventory authoritative product facts and flag unsupported claims.
4. Determine whether Cloudflare resources already exist before creating anything.
5. Check git status and remote configuration. Keep cloud deployment and GitHub push as separately authorized actions.

Read `references/brand-and-content-rules.md` before creating public-facing copy or visual design.

## Phase 2: Define the Site

For the standard Southern Machinery THT site, provide eight distinct navigable pages:

1. Home
2. Products
3. Turnkey Solutions
4. Industries
5. About
6. Support
7. Contact / RFQ
8. Ad Studio

The Ad Studio is an operational page, not a marketing teaser. Include inputs, generated-output states, errors, loading feedback, and a configurable n8n webhook placeholder. Never hardcode a production webhook or credential.

Maintain shared navigation, footer, contact details, SEO metadata, responsive behavior, and visible calls to action across the site. Use real product imagery when available. Ensure all page links and forms work without client-side dead ends.

## Phase 3: Implement

- Keep shared brand data, navigation, product facts, and layout primitives centralized.
- When multiple pages call the backend from browser scripts, define one shared same-origin API client before page-specific scripts execute. Verify its declaration order in rendered HTML; a successful backend does not prevent browser errors such as `API is not defined`.
- Validate RFQ payloads on the server and store only necessary fields.
- Keep admin and inquiry management routes server-protected.
- Use D1 for relational records, R2 for product/media objects, and KV for lightweight site settings or cached configuration.
- Separate public assets from privileged APIs.
- Add schema migrations or an idempotent initialization path; do not silently mutate production data.
- Use environment bindings and secrets instead of committed credentials.

For backend rules and security acceptance criteria, read `references/architecture-and-security.md`.

## Phase 4: Verify Locally

Run the repository's formatter, type checks, unit tests, build, and focused integration tests. Then verify:

- all eight routes and navigation states;
- desktop and mobile layouts;
- RFQ success, validation failure, and server failure;
- authentication, role restrictions, logout, and expired/invalid tokens;
- uploads, object access, and unsupported file rejection;
- Ad Studio loading, success, empty, and webhook failure states;
- no secrets or real deployment IDs in tracked files.

Use `scripts/validate_project.sh <project-dir>` as a portable preflight helper. It supplements rather than replaces repository tests.

## Phase 5: Provision and Deploy

Read `references/cloudflare-deployment.md` completely before changing Cloudflare state.

1. Confirm the authenticated Cloudflare account matches the user's intended account.
2. Create or reuse D1, R2, and KV resources.
3. Record generated UUIDs from command output. A requested name is not a valid D1 or KV ID.
4. Render a local deployment config from `assets/templates/wrangler.worker.toml` or `assets/templates/wrangler.pages.toml`.
5. Store JWT and external-service secrets with Cloudflare secret management.
6. Initialize D1 using the reviewed schema and the actual database name or generated ID.
7. Build, deploy, and capture the production URL.
8. If the Worker preview succeeds but `workers.dev` repeatedly returns platform errors, diagnose first, then use the documented Pages Advanced Mode fallback when compatible.
9. For Git-connected Pages projects, keep the root Pages configuration separate from the Worker bundling configuration and verify the dashboard build command/output directory before pushing a production commit.

For Pages Advanced Mode, adapt `scripts/prepare_pages.mjs` to the repository build output. It creates `_worker.js`, `_routes.json`, and a Pages deployment config without embedding resource IDs.

## Phase 6: Production Acceptance

Follow `references/verification-checklist.md`. Test the public URL rather than assuming a successful deployment command means the site works. Inspect response status, rendered UI, console errors, API behavior, persistence, authorization boundaries, and mobile screenshots.

Delete temporary diagnostic deployments only when they were created during the current task and deletion is authorized. Do not delete pre-existing resources.

## Incident Workflow

For an inaccessible custom domain or broken admin login:

1. Compare the custom domain, canonical `pages.dev` domain, latest deployment-specific URL, and one known-good deployment URL.
2. Separate DNS/TLS failures from application `404`, `5xx`, or blank-response failures.
3. List Pages projects and deployments; match the production deployment to its Git commit or manual source.
4. If both custom and canonical domains fail while an older deployment works, rebuild and manually deploy the reviewed artifact to restore service before changing DNS.
5. For browser errors, inspect rendered script order and console evidence before testing passwords or changing backend auth.
6. Test invalid credentials, valid credentials, token issuance, role, and one protected API without printing or committing the token.
7. After pushing, monitor the Git-triggered deployment. A successful manual deployment does not prove Git integration is configured correctly.
8. If automatic deployment fails, confirm the working manual deployment still serves production; never replace it with an unverified rollback.

## Phase 7: GitHub Synchronization

1. Review the final diff and exclude generated output, local caches, secrets, and deployment-only files unless intentionally tracked.
2. Re-run relevant tests.
3. Commit only task-related changes with a precise message.
4. Push to the confirmed branch and remote.
5. Report the commit, branch, production URL, created/reused resources, verification results, and any remaining manual steps.

## Resource Map

- `references/brand-and-content-rules.md`: company identity, information hierarchy, copy and visual constraints.
- `references/architecture-and-security.md`: Cloudflare architecture, authentication, RBAC, CORS, upload and secret rules.
- `references/cloudflare-deployment.md`: provisioning, IDs, Workers/Pages workflows, database setup, fallback logic.
- `references/verification-checklist.md`: local and production acceptance checklist.
- `assets/templates/`: placeholder-only Wrangler templates.
- `assets/templates/wrangler.pages-root.toml`: root config for Git-connected Pages builds whose output is generated into a separate directory.
- `scripts/prepare_pages.mjs`: generic Pages Advanced Mode packager.
- `scripts/validate_project.sh`: non-destructive project preflight.
