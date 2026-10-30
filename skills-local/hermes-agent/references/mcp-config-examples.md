# MCP server config examples

Drop into `~/.hermes/config.yaml` under a top-level `mcp_servers:` key. Restart the Hermes session after editing — `/reload-mcp` only re-reads existing definitions.

## Filesystem (read/write scoped to a path)

```yaml
mcp_servers:
  filesystem:
    transport: stdio
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/jasonwu/projects"]
```

Tools exposed: `mcp__filesystem__read_file`, `mcp__filesystem__write_file`, `mcp__filesystem__list_directory`, etc.

## GitHub (needs PAT with repo scope)

```yaml
mcp_servers:
  github:
    transport: stdio
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."
```

Tools exposed: `mcp__github__create_issue`, `mcp__github__search_repositories`, `mcp__github__get_file_contents`, etc.

## Postgres

```yaml
mcp_servers:
  postgres:
    transport: stdio
    command: npx
    args: ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost:5432/dbname"]
```

## Playwright (browser automation)

```yaml
mcp_servers:
  playwright:
    transport: stdio
    command: npx
    args: ["-y", "@playwright/mcp@latest"]
```

Tools exposed: `mcp__playwright__browser_navigate`, `mcp__playwright__browser_snapshot`, etc. May collide with the built-in `browser` toolset — disable one or the other via `hermes tools`.

## Remote (HTTP/SSE transport)

```yaml
mcp_servers:
  remote_example:
    transport: sse
    url: "https://mcp.example.com/sse"
    headers:
      Authorization: "Bearer ${MCP_REMOTE_TOKEN}"
```

## Common gotchas

- **Env var expansion:** Hermes expands `${VAR}` from `~/.hermes/.env` and process env at tool-call time, not at config-load time. Use it for secrets.
- **stdio vs sse:** stdio = `command` + `args` (server launched per-session). sse = `url` + `headers` (server is a remote service). Don't mix fields between the two.
- **Server name → tool prefix:** the key under `mcp_servers:` (e.g. `github`) becomes the prefix. `mcp__github__<tool_name>`.
- **Tool selection:** even after a server is configured, individual tools can be toggled via `hermes mcp configure <name>`. `/reload-mcp` re-applies the toggle.
- **No config → no tools.** Installing the `mcp` Python client package does *not* auto-discover servers. You must add `mcp_servers:` for any tools to appear.
