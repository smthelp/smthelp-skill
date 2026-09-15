---
name: hostinger-mcp-deploy
description: Inspect the current workspace for generated static webpages, landing pages, frontend build output, or WordPress plugin code, then deploy the best candidate to a Hostinger staging/test directory through the connected hostinger-hosting MCP server and return a public preview URL. Use when the user invokes $hostinger-mcp-deploy, Hostinger_MCP_Deploy, asks to deploy a generated page/plugin to Hostinger, publish a temporary overseas customer preview link, sync code to Hostinger testing space, or produce a standalone public URL for review.
---

# Hostinger MCP Deploy

## Goal

Deploy the latest relevant web artifact from the current workspace to a safe Hostinger test location and return a public URL that an overseas customer can click directly.

## Required Tooling

Use the connected `hostinger-hosting` MCP server when available. If the Hostinger MCP tools are not visible, search/load tools for `hostinger hosting mcp deploy upload file list directory` before proceeding.

If the Hostinger MCP server is unavailable, stop and explain that deployment cannot be completed until the `hostinger-hosting` MCP connection is available. Do not fake a URL.

## Workflow

1. Inspect the current workspace to identify deployable output.
2. Decide whether the artifact is a static webpage/frontend build or a WordPress plugin.
3. Run lightweight validation before upload.
4. Use Hostinger MCP to list candidate domains and web roots.
5. Choose the safest matching test/staging subdirectory.
6. Upload/sync only the selected artifact files.
7. Verify the public URL loads if tooling allows.
8. Return the final customer-preview URL and a short deployment summary.

## Artifact Detection

Prefer the newest or user-requested artifact. Inspect timestamps and likely paths.

Static webpage candidates:

- `index.html` in the current directory or a recent subdirectory
- `html/`, `dist/`, `build/`, `out/`, `public/`, `site/`, `landing/`, `preview/`
- Single-file landing pages generated for Southern Machinery content
- Assets referenced by the HTML, such as CSS, JS, images, fonts, videos, and PDFs

WordPress plugin candidates:

- A directory containing a PHP file with a WordPress plugin header
- `wp-content/plugins/<plugin-name>/`
- A generated plugin zip or plugin source folder

Do not deploy unrelated WordPress core files, database dumps, `.wpress` backups, `.sql`, `.sql.gz`, `.env`, credentials, cache folders, `node_modules`, `.git`, or local scratch files.

## Pre-Deploy Checks

For static pages:

- Confirm an entry file exists, usually `index.html`.
- Check referenced local assets are included.
- Prefer built output over source code when a framework has a build directory.
- Avoid deploying development-only files such as package manifests unless required by a static host.

For WordPress plugins:

- Confirm a valid plugin header exists.
- Check PHP files for obvious syntax issues when PHP is available.
- Upload to a staging plugin directory, not directly to a live production plugin path, unless the user explicitly requests production deployment.
- Never activate, deactivate, delete, or overwrite a production plugin without explicit user approval.

## Choosing the Hostinger Target

Use Hostinger MCP to list available domains, file managers, web roots, and directories. Select in this order:

1. Existing test/staging directory clearly matching the artifact name or product slug.
2. Existing safe preview directory such as `/public_html/test/`, `/public_html/demo/`, `/public_html/preview/`, `/public_html/staging/`, `/public_html/codex/`, or `/public_html/tmp/`.
3. A new slugged subdirectory under a safe preview parent, such as `/public_html/test/<artifact-slug>/`.
4. For WordPress plugins, a staging WordPress install plugin path only if clearly identified as staging/test.

Avoid uploading into the domain root `/public_html/` or a live production WordPress path unless the user explicitly requested it.

Use clean lowercase slugs from the artifact, product model, page title, or plugin name. Include a short date suffix when useful to avoid overwriting a previous preview.

## Sync Rules

- Preserve relative paths needed by the page or plugin.
- Overwrite files inside the selected test subdirectory only.
- Delete remote files only when necessary and only inside the selected test subdirectory.
- Keep uploads minimal and deterministic.
- If a remote file conflict is found outside the selected test subdirectory, choose a new test subdirectory instead.

## URL Construction

After upload, construct the public URL from the Hostinger domain and deployed path.

For static pages:

- Directory deploy: `https://<domain>/<test-path>/`
- Single HTML not named `index.html`: `https://<domain>/<test-path>/<file>.html`

For WordPress plugins:

- Return the staging WordPress site URL where the plugin can be previewed.
- If activation or page setup is required and not completed, clearly state that upload is complete but preview needs activation/configuration.

Verify the URL with an HTTP request or browser check when available. If verification fails, report the deployment path and the failure honestly.

## Final Response

Return concise results in this shape:

```text
Deployment complete.

Preview URL: https://example.com/test/product-page/

Deployed: static landing page from /path/to/artifact
Target: Hostinger /public_html/test/product-page/
Notes: Verified page loads successfully.
```

Never invent a successful deployment or public URL. If Hostinger MCP is missing, credentials fail, upload is blocked, or verification fails, explain the exact blocker and what is needed next.
