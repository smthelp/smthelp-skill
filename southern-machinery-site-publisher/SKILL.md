---
name: southern-machinery-site-publisher
description: "Build, refine, troubleshoot, and publish Southern Machinery B2B SMT/THT equipment websites from an existing frontend project. Use when the user asks to create or update a Southern Machinery website, add SMT/THT/wave soldering navigation or footer sections, follow the jilles.dev Codex design/deploy guides, deploy an Astro/static frontend to Cloudflare Workers with Assets, repair Cloudflare Workers deployment issues, or recover from workers.dev 1101 errors by using an existing custom domain."
metadata:
  source: codex
  origin: "southern-machinery-site-publisher"
---
# Southern Machinery Site Publisher

## Overview

Use this skill to turn the current website project into a polished Southern Machinery B2B website and publish it with Cloudflare Workers with Assets. Work in the folder the user opened; do not scaffold a new project unless the user explicitly asks.

## Core Rules

- Treat the current working directory as the website project. Confirm it contains `package.json`, `src/`, an Astro config, and `wrangler.jsonc`/`wrangler.toml` before editing.
- Prefer the existing stack and file structure. For Astro projects, keep changes in `src/pages`, `src/layouts`, `public`, and `wrangler.jsonc` unless the codebase indicates otherwise.
- Speak simply to non-technical users. Say “我正在检查/发布网站”, not “请运行命令” or “去找 API token”.
- Never deploy to Cloudflare Pages for this workflow. Use Cloudflare Workers with Assets.
- Do not ask the user for Cloudflare account IDs or API tokens. Use the active Wrangler login and `wrangler whoami`.
- Do not delete existing Workers, routes, domains, DNS records, or user files unless the user explicitly approves that exact action.

## Source Guides

When the user mentions these guides, fetch and follow them before acting:

- Design guide: `https://jilles.dev/llm/codex/design.md`
- Deploy guide: `https://jilles.dev/llm/codex/deploy.md`

If network access needs permission, ask in plain language: “请点击允许，我需要读取你指定的设计/部署指南。”

## Website Design Workflow

1. Inspect the project:
   - Read `package.json`, `astro.config.*`, `wrangler.*`, `src/pages`, `src/layouts`, and existing CSS/components.
   - Use `rg`/`rg --files` before slower search tools.
2. Build the actual usable website, not a marketing placeholder.
3. Use a professional B2B industrial style:
   - Clear fixed top navigation.
   - Restrained corporate layout with dense but readable sections.
   - Industrial blue as the main action color.
   - Avoid decorative gradient-only hero art, one-note palettes, nested cards, and oversized landing-page fluff.
4. Include Southern Machinery positioning:
   - Shenzhen manufacturer, founded 2011.
   - High-efficiency, cost-effective SMT/THT equipment.
   - Complete line capability: SMT, THT insertion, wave soldering, board handling, inspection options.
   - Overseas installation guidance, training, spare parts, and remote support.
5. Use this exact logo URL when requested or when branding is needed:
   - `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`
   - Keep header logo around `max-height: 45px`; include fallback text if the remote image fails.
6. For the standard header, include:
   - Left logo.
   - Links: `Home`, `SMT Lines`, `THT Insertion`, `Wave Soldering`.
   - CTA: `Get a Quote`.
7. For the standard footer, include four columns:
   - About: logo and 10+ years Shenzhen manufacturing experience.
   - Products: `SMT Lines`, `Auto Insertion`, `Wave Soldering`.
   - Resources: `Machine Catalog` to `https://file.autoinsertion.com`, `Machine Photos` to `https://ph.smthelp.com`.
   - Connect: social icons opening in a new tab:
     - LinkedIn Company: `https://www.linkedin.com/company/smtmachine`
     - LinkedIn Profile: `https://cn.linkedin.com/in/smtsupplier`
     - Twitter: `https://twitter.com/smtspecialist`
     - Facebook: `https://www.facebook.com/autoinsertion`
     - YouTube: `https://www.youtube.com/c/Smthelping`

## Local Validation

Run the project’s existing build command, usually `npm run build`. If the user has the in-app browser open, use the existing local dev server when possible; otherwise start the project’s dev server and provide the URL.

Before finalizing UI work, verify:

- The header is fixed/responsive and does not overlap content.
- The logo scales cleanly.
- Footer columns stack cleanly on mobile.
- CTA links and external links work.
- Text fits in buttons, cards, and narrow viewports.

## Cloudflare Workers Deployment

Use Cloudflare Workers with Assets.

1. Confirm Wrangler is available and authenticated:
   - `./node_modules/.bin/wrangler --version`
   - `./node_modules/.bin/wrangler whoami`
2. If not logged in, start Wrangler login and tell the user only: “请在浏览器里完成 Cloudflare 登录。”
3. Build the website.
4. Ensure `wrangler.jsonc` is a Workers-with-Assets config. For a static Astro site, prefer:

```jsonc
{
	"$schema": "./node_modules/wrangler/config-schema.json",
	"compatibility_date": "YYYY-MM-DD",
	"name": "project-name",
	"workers_dev": true,
	"assets": {
		"directory": "./dist"
	},
	"observability": {
		"enabled": true
	}
}
```

5. Run `./node_modules/.bin/wrangler types` after config changes.
6. Deploy with `./node_modules/.bin/wrangler deploy`.
7. Verify the public URL with both headers and content. A successful deploy message is not enough.

## Handling `workers.dev` 1101

If the `*.workers.dev` URL returns `error code: 1101`:

1. Do not assume the website code is broken.
2. Check whether the Worker receives the request:
   - Run `wrangler tail <worker-name>`.
   - Request the public URL.
   - If no logs appear, the request is failing before it reaches the Worker.
3. Test a Cloudflare remote preview. If preview serves the site but public `workers.dev` does not, suspect routing/subdomain state.
4. Check whether other Workers under the same account subdomain also fail. If several existing `*.pcba.workers.dev` URLs return `1101`, treat it as an account `workers.dev` issue.
5. Inspect existing Worker custom domains before creating anything new. Use Wrangler/API through the active token, but never print the token. Example pattern:

```bash
./node_modules/.bin/wrangler auth token --json
```

Use the token only inside a one-off command/process. Query:

- `/accounts/{account_id}/workers/subdomain`
- `/accounts/{account_id}/workers/scripts/{script_name}/subdomain`
- `/accounts/{account_id}/workers/domains`

6. If an existing custom domain is already bound to the Worker and returns `HTTP 200`, update `wrangler.jsonc` to make it the source of truth:

```jsonc
{
	"workers_dev": false,
	"routes": [
		{
			"pattern": "pcba.smthelp.eu",
			"custom_domain": true
		}
	]
}
```

7. Redeploy and verify the custom domain. Report the working domain as the website URL.

## Southern Machinery Known Deployment

For this project/history, the reliable public URL is:

- `https://pcba.smthelp.eu`

The `pcb-assembly-automation.pcba.workers.dev` URL may return `1101` because the account-level `pcba.workers.dev` subdomain has shown failures across multiple Workers. Prefer `pcba.smthelp.eu` for final user-facing delivery unless the user specifically asks to repair `workers.dev`.

## Final Response Pattern

Use a concise status format:

```markdown
Status: Green / Yellow / Red

网站:
- [URL]

我做了:
- ...

验证:
- Build passed
- Public URL returned HTTP 200

需要注意:
- ...
```

Use Chinese when the user writes in Chinese.
