---
name: apple-icloud-cli
description: "Manage Apple Notes, Reminders, FindMy, iMessage, and other Apple iCloud services from the terminal via third-party CLIs (memo, remindctl, etc.). Class-level umbrella for macOS-only Apple productivity tools that sync via iCloud. Use when the user says 'add a reminder', 'save to Notes', 'create a reminder on my phone', or wants terminal access to any Apple iCloud service."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Apple, macOS, iCloud, Notes, Reminders, memo, remindctl]
    related_skills: [macos-computer-use, obsidian]
---

# Apple iCloud CLI Tools (macOS)

Class-level umbrella for the third-party CLIs that expose Apple iCloud services (Notes, Reminders, FindMy, iMessage) to the terminal. Every section below covers a different Apple service. The full content of each section lives in `references/<service>.md`.

## When to Use

- User wants to add / view / complete a Reminder
- User wants to create / search / edit a Note
- User wants to track a device or AirTag via FindMy
- User wants to send an iMessage from the terminal
- User wants to control the macOS UI (open apps, type into fields, take screenshots)

## Common Prerequisites

- **macOS only.** None of these CLIs work on Linux/Windows.
- **Grant Automation access** when prompted (System Settings → Privacy & Security → Automation → enable the CLI for Notes/Reminders/Calendar)
- **iCloud sign-in** required in System Settings for cross-device sync
- Use `pty=true` for interactive prompts (most CLIs support both flag-driven and interactive modes)

## Services

| Service | CLI | Reference |
|---|---|---|
| Apple Notes | `memo` (via `brew tap antoniorodr/memo`) | `references/apple-notes.md` |
| Apple Reminders | `remindctl` (via `brew install steipete/tap/remindctl`) | `references/apple-reminders.md` |
| FindMy devices / AirTags | macOS FindMy.app + `peekaboo` (AppleScript + screenshot) | `references/findmy.md` |
| iMessage | `imsg` (via `brew install steipete/tap/imsg`) | `references/imessage.md` |
| macOS UI control | cua-driver / `computer_use` tool | (see `macos-computer-use` skill in `apple/macos-computer-use/`) |

For all four covered services, load the per-service reference file. The macOS UI control skill is kept standalone because it has substantial session-specific content (cursor routing, Space-aware screenshots, AX tree capture, etc.) that doesn't fit a thin reference.

## Decision Tree: "remind me…" / "save this to Notes…"

When the user says one of these ambiguous phrases:

- **"remind me to X"** → ask: Apple Reminders (syncs to your iPhone) or agent cronjob alert (in-session only)?
- **"save this to my notes"** → Apple Notes (iCloud sync) or Obsidian vault (Markdown-native) or in-agent `memory` tool (private to the session)?
- **"send a message"** → iMessage (Apple-to-Apple) or another channel (Telegram, email)?

The per-service references cover these disambiguation questions in detail.

## Output Formats

Most Apple iCloud CLIs support `--json` / `--plain` / `--quiet` for scripting. Default to `--json` when you need to parse the output programmatically (e.g. for an "if overdue then notify" loop).

## Common Pitfalls Across All Apple iCloud CLIs

- **macOS only** — there's no Linux equivalent. Don't suggest these on a non-Mac host.
- **Automation permission** — first run will pop a System Settings dialog. If the user is in a headless SSH session, they may need to grant permission on the actual desktop.
- **iCloud sign-in required** — if the user is signed out of iCloud, none of these will work even with the CLIs installed.
- **Sync delays** — iCloud sync is not instant. Operations appear on the iPhone within ~5-30 seconds typically, but can lag up to a minute.

## References

| File | Covers |
|---|---|
| `references/apple-notes.md` | `memo` CLI: list, create, search, edit, delete, move, export Notes. Limitations (no image editing). Related to Obsidian for Markdown-native notes. |
| `references/apple-reminders.md` | `remindctl` CLI: list today/tomorrow/week, manage lists, create with due/alarm fields, complete/delete, output formats, date formats. Includes the `--due` vs `--alarm` distinction that's easy to get wrong. |
