---
name: opencli-installation
description: "Install and configure OpenCLI (Make Any Website & Tool Your CLI) — browser automation, CLI hub, and AI agent primitives for Southern Machinery sales workflows."
whenToUse: "install opencli，opencli setup，browser bridge opencli，opencli skill install"
metadata:
  source: hermes
  origin: "sales-engineering/opencli-installation"
---
# OpenCLI Installation & Configuration

## What is OpenCLI

**OpenCLI** turns websites, browser sessions, Electron apps, and local tools into deterministic CLI interfaces.
- **18.4k GitHub stars**, npm: `@jackwener/opencli`
- Zero LLM cost at runtime — pure browser/API automation
- Built-in adapters: 100+ sites (Bilibili, Zhihu, Xiaohongshu, Twitter/X, Reddit, HackerNews, Amazon, 1688, etc.)
- Browser Bridge: reuse your logged-in Chrome session to operate any website
- CLI Hub: register local binaries (`gh`, `docker`, etc.) for unified discovery

---

## Installation

### Step 1: Install Node.js (if needed)

Requires **Node.js >= 21** (or Bun >= 1.0).

```bash
node --version   # Check — v22.13.0+ is fine
```

### Step 2: Install OpenCLI via npm

```bash
npm install -g @jackwener/opencli
opencli --version   # Verify → 1.7.8
```

### Step 3: Install Browser Bridge Extension (for browser commands)

**Method A — Chrome Web Store (recommended):**
Install **OpenCLI** from the [Chrome Web Store](https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk).

**Method B — Manual install:**
1. Download the latest `opencli-extension-v{version}.zip` from GitHub [Releases](https://github.com/jackwener/opencli/releases)
2. Unzip → open `chrome://extensions` → enable **Developer mode**
3. Click **Load unpacked** → select the unzipped folder

### Step 4: Verify

```bash
opencli doctor          # Check extension + daemon connectivity
opencli list            # List all commands
opencli --version      # Should return 1.7.8+
```

### Step 5 (Optional): Register OpenCLI skills for AI agents

```bash
npx skills add jackwener/opencli --skill opencli-adapter-author
npx skills add jackwener/opencli --skill opencli-browser
npx skills add jackwener/opencli --skill opencli-usage
npx skills add jackwener/opencli --skill opencli-autofix
npx skills add jackwener/opencli --skill smart-search
```

### Step 6 (Optional): Tab completion

```bash
# Zsh
echo 'eval "$(opencli completion zsh)"' >> ~/.zshrc

# Bash
echo 'eval "$(opencli completion bash)"' >> ~/.bashrc

# Fish
echo 'opencli completion fish | source' >> ~/.config/fish/config.fish
```

---

## Key Commands Quick Reference

| Command | Description |
|---------|-------------|
| `opencli list` | List all registered commands |
| `opencli <site> <cmd>` | Run a built-in adapter (e.g., `opencli bilibili hot`) |
| `opencli browser open <url>` | Open URL in logged-in Chrome |
| `opencli browser state` | Get current page DOM snapshot |
| `opencli browser click <selector>` | Click an element |
| `opencli browser type <selector> <text>` | Type into a field |
| `opencli browser extract <selector>` | Extract data from page |
| `opencli doctor` | Diagnose connectivity |
| `opencli profile list/rename/use` | Manage Chrome multi-profile routing |
| `opencli external register <name>` | Register a local CLI binary |

### Output formats (all built-in commands)

```bash
opencli <site> <cmd> -f json    # JSON
opencli <site> <cmd> -f table   # Rich table (default)
opencli <site> <cmd> -f yaml     # YAML
opencli <site> <cmd> -f csv     # CSV
opencli <site> <cmd> -f md      # Markdown
opencli <site> <cmd> -v         # Verbose (debug)
```

---

## Architecture

```
opencli (Node.js CLI)
    ↕ WebSocket localhost:19825
micro-daemon (auto-starts)
    ↕ Chrome DevTools Protocol
OpenCLI Browser Extension
    ↕
Chrome (logged-in session)
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLI_DAEMON_PORT` | `19825` | Daemon HTTP port |
| `OPENCLI_PROFILE` | — | Chrome profile alias to use |
| `OPENCLI_BROWSER_CONNECT_TIMEOUT` | `30` | Seconds to wait for browser |
| `OPENCLI_BROWSER_COMMAND_TIMEOUT` | `60` | Seconds per command |
| `OPENCLI_VERBOSE` | `false` | Verbose logging (`-v`) |
| `OPENCLI_LIVE` | `false` | Keep automation lease open after command |
| `OPENCLI_WINDOW_FOCUSED` | `false` | Open container in foreground (`--focus`) |
| `OPENCLI_CDP_ENDPOINT` | — | Remote browser / Electron CDP endpoint |

---

## Updating

```bash
npm install -g @jackwener/opencli@latest
npx skills add jackwener/opencli   # Refresh skills
```

---

## Troubleshooting

```bash
# Daemon not running?
opencli doctor

# Restart daemon
opencli daemon stop
opencli browser state   # auto-starts

# Check version
opencli --version

# Verbose debug
opencli -v <command>

# Clear browser target
opencli browser close
```

---

## For Southern Machinery (Southern Machinery context)

> **lark-cli (Feishu CLI) install/setup in Hermes**: see `references/lark-cli-hermes-setup.md`

OpenCLI is a browser + CLI automation layer. Key value for SMT sales engineering:

1. **Monitor competitor activity** — watch Amazon bestseller rankings, 1688 supplier prices
2. **Lead intelligence** — scrape LinkedIn, company websites through your logged-in Chrome
3. **Price monitoring** — track competitor equipment pricing across platforms
4. **Content aggregation** — pull tech news (HackerNews, 36kr) for market intelligence
5. **Automated outreach prep** — extract data from prospect websites before cold emails
6. **YouTube/ Bilibili research** — study competitor product videos and demos
7. **1688 sourcing** — monitor SMT equipment supplier prices on 1688.com
8. **Browser-based workflows** — operate any internal web tool through CLI
9. **GitHub monitoring** — track competitor open-source activity
10. **Multi-profile** — separate Chrome profiles for different business functions

> **Note**: Browser commands require you to be logged into the target site in Chrome first. OpenCLI reuses your existing session — no credentials stored in the CLI.
