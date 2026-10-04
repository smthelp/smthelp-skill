# lark-cli (Feishu/Lark CLI) — Hermes Agent Setup Reference

## Installation

```bash
# Install globally via npx
npx @larksuite/cli@latest install
```

- Installs to: `~/.npm-global/bin/lark-cli`
- Global npm prefix: `~/.npm-global/` (per `npm root -g`)
- **Requires** `~/.npm-global/bin` on PATH (typically pre-added in `~/.zshrc` line 8: `export PATH="$HOME/.npm-global/bin:$PATH"`)

## Verify

```bash
~/.npm-global/bin/lark-cli --version
# → lark-cli version X.X.X
```

## Hermes Context: Do NOT run `config init`

`lark-cli config init` refuses inside Hermes with:
```
"config init is refused inside hermes context (would create a parallel app and shadow the existing hermes binding)"
```

**Correct approach: use `config bind`**

```bash
# Bot-only identity (safer — no impersonation, no personal resource access)
lark-cli config bind --source hermes --identity bot-only

# User-default identity (needed for personal calendar/mail/drive access)
lark-cli config bind --source hermes --identity user-default
```

Successful output:
```json
{
  "ok": true,
  "app_id": "cli_a95716fd7df9dbda",
  "config_path": "/Users/jasonwu/.lark-cli/hermes/config.json",
  "identity": "bot-only",
  "workspace": "hermes"
}
```

## Post-Bind Verification

```bash
lark-cli auth status
```

Expected: bot identity `ready: true`, user identity `missing` (normal for bot-only).

## Key Distinction

| Command | When to use |
|---------|-------------|
| `config init --new` | Standalone terminal use (outside Hermes) |
| `config bind --source hermes` | Inside Hermes Agent session |
| `auth login --recommend` | Add user identity (personal resources) |

## Notes

- Binding is a **one-time sync** — subsequent Hermes config changes do NOT auto-propagate to lark-cli. Re-run `config bind` if the app credential changes.
- Bot identity allows tenant-level API calls (send messages as app, read/write group chats, etc.).
- User identity is required for personal calendar, mail, and drive access.
