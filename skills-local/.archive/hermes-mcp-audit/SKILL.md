---
name: hermes-mcp-audit
description: Audit and (re)establish MCP server availability in a Hermes Agent install — covers the 3-step diagnostic (config, venv, install), the `uv pip install` + venv auto-detection gotcha, and a re-runnable audit script. Use when the user asks "what MCP tools are available", "is MCP set up", "add MCP", or fan-out diagnostics land in your session.
version: 1.0.0
author: MiniMax
license: MIT
metadata:
  hermes:
    tags: [hermes, mcp, audit, diagnostic, setup, multi-agent]
    related_skills: [hermes-agent, native-mcp, mcporter]
---

# Hermes MCP Audit

Diagnostic + remediation recipe for "what MCP-backed tools does this Hermes install actually have right now, and how do I get more?" Use it when a user (or a sibling M-agent in a fan-out) asks about MCP availability, or before recommending an MCP-backed integration.

For the *configuration schema* and *usage* of MCP servers, defer to the bundled `native-mcp` skill (protected) and `mcporter` (protected). This skill is the **availability** layer: it answers "is the runtime ready, what servers are wired up, and what's missing?".

## When to load

- User asks: "what MCP tools are available right now", "is MCP set up", "do I have filesystem/github/etc MCP", "audit my MCP"
- A fan-out query from jason hits you and other M-variants about MCP setup
- User wants to add an MCP server and you need to confirm the `[mcp]` extra is installed first
- A cron job or subagent needs MCP tools and you must verify before dispatching

## The 3-step audit (run all three, in order)

### 1. Check config — what servers are declared?

```bash
grep -B 1 -A 50 "^  mcp_servers:" ~/.hermes/config.yaml
# OR for the whole tree:
grep -A 50 "mcp_servers" ~/.hermes/config.yaml
```

- If `mcp_servers:` is absent → **0 MCP-backed tools are available**, regardless of what packages are installed.
- If present → list the server names; each becomes a `mcp__<server>__<tool>` tool at runtime.

### 2. Check venv — is the `mcp` client library installed?

```bash
ls ~/.hermes/hermes-agent/venv/lib/python*/site-packages/ | grep -E "^mcp(-[0-9]|\.dist-info)?$"
```

- If `mcp` and `mcp-<version>.dist-info` are both present → client lib is ready.
- The `mcp` package often arrives as a transitive dependency of other extras (e.g. `computer-use`), so it's frequently installed even when the `[mcp]` extra was never explicitly requested. Don't be surprised by a no-op `pip install`.

### 3. Check installed extras — what *could* be loaded?

```bash
cd ~/.hermes/hermes-agent && grep -A 1 "^mcp = " pyproject.toml
```

The `[mcp]` extra is just `mcp==1.26.0` + a pinned `starlette==1.0.1` (CVE-2026-48710 patch). It is *necessary* but **not sufficient** — you still need `mcp_servers:` config for any tools to appear.

## The `uv pip install` + venv gotcha (PITFALL)

`uv pip install -e ".[mcp]"` from inside `~/.hermes/hermes-agent` will fail with `error: No virtual environment found` if you don't tell `uv` which venv to use. Unlike `pip` and `python -m venv`, `uv` does **not** auto-detect an active venv from `cwd`. Two fixes:

```bash
# Option A — explicit VIRTUAL_ENV prefix (works without `source venv/bin/activate`):
VIRTUAL_ENV=/Users/jasonwu/.hermes/hermes-agent/venv \
  uv pip install -e "/Users/jasonwu/.hermes/hermes-agent[mcp]"

# Option B — point uv at the venv's python directly:
uv pip install --python /Users/jasonwu/.hermes/hermes-agent/venv/bin/python \
  -e "/Users/jasonwu/.hermes/hermes-agent[mcp]"
```

**Don't** use `--system` here — it would install into the macOS system Python, bypassing the venv entirely. That's the wrong fix.

Expected output for a stock install: `Resolved N packages`, `mcp` shows as already satisfied (no-op), and hermes-agent gets an editable reinstall. No breakage.

## Adding a server (the actual unlock)

The install is rarely the blocker. The real unlock is `mcp_servers:` config. Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  filesystem:
    transport: stdio
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/jasonwu"]
  github:
    transport: stdio
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."
```

Then **restart the Hermes session** (not `/reload-mcp` — that toggles tool selection, not server definitions). Tool names appear as `mcp__<server>__<tool>`.

See `references/mcp-config-examples.md` for a fuller template (Postgres, Playwright, etc.).

## Re-runnable audit

A one-shot script lives at `scripts/audit-mcp.sh` — copies the 3-step audit + gotcha-fix into a single command. Useful for cron, subagent self-checks, and M-fleet fan-outs.

```bash
bash ~/.hermes/skills/hermes-mcp-audit/scripts/audit-mcp.sh
```

## Pitfalls

- **0 tools ≠ 0 installed.** Config can be empty even when `mcp` package is present. Always check both.
- **`--system` is the wrong fix.** If `uv pip install` complains about venv, prefix with `VIRTUAL_ENV=...` — never `--system`.
- **Don't re-run `hermes update` expecting it to add MCP.** `update` refreshes the code; it does not touch `mcp_servers:` config.
- **`/reload-mcp` doesn't add servers.** It re-reads *existing* server definitions. For new servers, full session restart.
- **Stale transitive `mcp`.** The package may be installed but at an older version. To upgrade explicitly: `VIRTUAL_ENV=~/.hermes/hermes-agent/venv uv pip install -e "~/.hermes/hermes-agent[mcp] --upgrade-package mcp"`.
- **Profile isolation.** If running under a non-default profile, audit `~/.hermes/profiles/<name>/config.yaml` and `~/.hermes/profiles/<name>/hermes-agent/venv/`, not the root.

## What to tell the user

When asked "what MCP tools are available right now?", structure the answer as:

1. **Number** — explicit count of configured servers and expected tool namespaces
2. **Config status** — present or absent in `~/.hermes/config.yaml`
3. **Client status** — `mcp` package present in venv at version X
4. **Install result** — what `uv pip install -e ".[mcp]"` actually did (usually: no-op)
5. **Next step** — concrete `mcp_servers:` block template for the integration they want

Avoid the trap of saying "MCP is installed" when 0 servers are configured — those are different things.
