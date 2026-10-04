# Cloudflare Deployment

## Preconditions

Confirm the intended Cloudflare account, repository branch, deployment target, resource region/jurisdiction requirements, and whether resources should be created or reused. Deployment mutates external state and requires user authorization.

## Resource Identity

Cloudflare resource names and IDs are different:

- D1 `database_name` is human-readable; `database_id` is a Cloudflare-generated UUID.
- KV namespace title is human-readable; `id` and optional `preview_id` are Cloudflare-generated identifiers.
- R2 bindings normally use the bucket name.

Never place a requested friendly name in an ID field. Capture actual identifiers after provisioning and render them into the project deployment config. Examples in this skill use placeholders only.

## Provisioning Sequence

1. Authenticate and confirm account identity.
2. List existing D1 databases, R2 buckets, KV namespaces, Pages projects, and Workers before creating duplicates.
3. Create only missing resources using user-approved names.
4. Save returned IDs in the deployment config, not in reusable skill files.
5. Set secrets through Cloudflare's secret mechanism.
6. Review the schema, then initialize the intended D1 database explicitly.
7. Build and deploy.

Typical commands vary by Wrangler version; inspect `wrangler --help` before relying on flags. Common forms are:

```sh
npx wrangler whoami
npx wrangler d1 list
npx wrangler d1 create <database-name>
npx wrangler r2 bucket create <bucket-name>
npx wrangler kv namespace create <namespace-title>
npx wrangler secret put JWT_SECRET
npx wrangler d1 execute <database-name> --file=./schema/schema.sql --remote
```

Do not initialize a similarly named database by assumption. Inspect the target binding and returned ID.

## Workers Path

Use `assets/templates/wrangler.worker.toml` as a starting point. Replace every placeholder, verify the entry point, build, run a local/remote preview as appropriate, deploy, and request the health route and representative pages/APIs from the assigned URL.

## Pages Advanced Mode Path

Use Pages Advanced Mode when the application is compatible with `_worker.js`, or as a diagnosed fallback when Worker preview works but the assigned `workers.dev` route repeatedly produces Cloudflare platform errors.

1. Build the Worker bundle into a clean output directory.
2. Rename/copy the entry bundle to `_worker.js`.
3. Write `_routes.json` so required routes pass through the Worker.
4. place a Pages-compatible `wrangler.toml` beside the output.
5. Deploy the directory to the intended Pages project.

Adapt `scripts/prepare_pages.mjs` or the repository's equivalent. Use `assets/templates/wrangler.pages.toml`. Pages projects may not accept all Worker-specific configuration fields.

Do not immediately change architecture after one transient error. Capture error codes, compare local preview and remote preview, test a minimal health handler if authorized, and confirm whether failure is application code, binding configuration, routing, or platform behavior.

## Git-Connected Pages Configuration

Pages Git builds and Worker bundling need different configuration semantics. For an Advanced Mode repository, use this split:

- Root `wrangler.toml`: Pages project config with `pages_build_output_dir = ".pages-dist"` (or the chosen generated directory).
- `wrangler.worker.toml`: Worker entry point and bindings used only to generate the `_worker.js` bundle.
- Output `.pages-dist/wrangler.toml`: Pages deployment config with `pages_build_output_dir = "."` because it lives inside the artifact.

Make build scripts explicit:

```json
{
  "scripts": {
    "dev": "wrangler dev --config wrangler.worker.toml",
    "build:pages": "wrangler deploy --dry-run --config wrangler.worker.toml --outdir=.pages-dist && node scripts/prepare-pages.mjs"
  }
}
```

Configure the Pages dashboard Git build settings consistently:

```text
Framework preset: None
Build command: npm run build:pages
Build output directory: .pages-dist
Root directory: /
```

Use `assets/templates/wrangler.pages-root.toml` for the repository root, `assets/templates/wrangler.worker.toml` for bundling, and `assets/templates/wrangler.pages.toml` inside the artifact.

After every production push, list deployments and locate the row whose source commit matches the push. Test its deployment-specific URL before treating Git synchronization as complete. A manual deployment can be healthy while a newer Git deployment is empty, failed, or points at the wrong output directory. A failed Git deployment normally should not replace the last successful production deployment; verify rather than assume.

## Custom Domain Incident Triage

Check in this order:

1. DNS answer and TLS handshake for the custom domain.
2. HTTP status/body for the custom domain and canonical `pages.dev` domain.
3. Latest deployment-specific URL and one previously successful deployment URL.
4. Pages project custom-domain list and deployment history.

Interpret common evidence:

- Custom domain fails, canonical works: inspect custom-domain binding, DNS, proxy status, and certificate.
- Both domains return the same application `404`: inspect the active deployment and output artifact before changing DNS.
- Latest commit URL fails, older URL works: rebuild/redeploy a known-good artifact, then correct Git build settings.
- Remote preview works but `workers.dev` fails with repeatable platform codes: preserve evidence and consider Pages Advanced Mode after isolating application code and bindings.

## Database Initialization

- Review schema for destructive statements and embedded credentials.
- Use migrations for existing production databases.
- For a new empty database, execute the reviewed schema remotely and query table metadata afterward.
- Bootstrap administrators using secure runtime input. Do not ship known default passwords.

## Cleanup

Remove only temporary diagnostic Workers/Pages projects created during the current task, and only with authorization. Preserve D1/R2/KV resources and existing deployments unless deletion was explicitly requested.
