---
name: github-workflows
description: "GitHub operations via gh CLI or REST: auth, issues, PRs, code review, repos, actions, releases. Class-level umbrella for all GitHub operations the agent performs — search this skill when the user says 'open a PR', 'triage issues', 'review this PR', 'create a repo', or 'fix CI'."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, gh-cli, Pull-Requests, Issues, Code-Review, Repositories, CI/CD, Authentication]
    related_skills: [github-pr-workflow, github-issues, github-code-review, github-repo-management, github-auth]
---

# GitHub Workflows

Class-level umbrella for GitHub operations. Every section below shows the `gh` way first, then the `git` + `curl` fallback for machines without `gh`. For full detail on any one section, load the corresponding `references/<topic>.md` file via `skill_view(name="github-workflows", file_path="references/<topic>.md")`.

## When to Use

- User says "open a PR", "triage issues", "review PR", "create a repo", "set up a secret", "fix CI", "cut a release", "fork the repo"
- The agent needs to talk to the GitHub API for any operation
- You need to know whether to use `gh` or fall back to `curl` with a personal access token

## Topics

| Topic | When | Reference |
|---|---|---|
| Authentication | First time: pick `gh`, HTTPS token, or SSH | `references/auth.md` |
| Issues | Triage, label, assign, comment, close | `references/issues.md` |
| Pull requests | Branch, commit, open PR, watch CI, merge | `references/pr-workflow.md` |
| Code review | Pre-push self-review, review a PR, post comments | `references/code-review.md` |
| Repository mgmt | Clone, create, fork, settings, secrets, releases, Actions, gists | `references/repo-management.md` |
| Templates | PR bodies, bug reports, feature requests | `templates/` |
| Helpers | `gh-env.sh` auth detection script | `scripts/gh-env.sh` |

## Shared Setup (used by every topic)

Before running any GitHub operation, source the env helper (or run the inline block):

```bash
# Source the helper — exports GITHUB_TOKEN, GH_OWNER, GH_REPO, AUTH as needed
source "${HERMES_HOME:-$HOME/.hermes}/skills/github/github-workflows/scripts/gh-env.sh"
```

The helper covers four cases, in priority order:
1. `gh auth status` returns success → use `gh` (best UX, handles auth transparently)
2. `$GITHUB_TOKEN` is set in the env → use `curl` with the header
3. `~/.hermes/.env` has `GITHUB_TOKEN=` → export it and use `curl`
4. `~/.git-credentials` has a github.com entry → extract the token and use `curl`

If none of the four succeed, the helper prints `AUTH=none` and the agent should ask the user to set up auth (see `references/auth.md`).

### Extract owner/repo from the git remote

Many `curl` commands need `owner/repo`. The helper also exports:

```bash
GH_OWNER=acme        # e.g. acme
GH_REPO=widget-api    # e.g. widget-api
```

…extracted from the current directory's `git remote get-url origin`. Works for both HTTPS and SSH URLs.

## One-gh-fits-most decision

For 90% of GitHub operations, the `gh` command is dramatically simpler than raw `curl`. Install it with `brew install gh` (macOS) or see <https://cli.github.com/manual/installation>. If `gh` is unavailable and the operation is rare (e.g. set a secret, fork a repo), fall back to `curl` per the reference; if it's frequent, prompt the user to install `gh`.

## Common patterns across all topics

- **First action in any script:** `source scripts/gh-env.sh` (or run the inline block)
- **Owner/repo variables:** prefer `$GH_OWNER/$GH_REPO` from the helper over re-deriving per-command
- **JSON parsing:** the `curl` recipes inline `python3 -c "import sys,json; ..."` rather than requiring `jq` (some sandboxes lack it)
- **Idempotency:** most `gh` commands and many `curl` PATCH/POST endpoints are idempotent for the operations you'll want to retry (label add, comment post, branch protect, etc.)
- **Auth failures:** `gh` will print a clear "not authenticated" error; `curl` returns HTTP 401. Both signal "run the auth setup in `references/auth.md`."

## Verification checklist

- [ ] `source scripts/gh-env.sh` succeeded (no `AUTH=none` printed)
- [ ] `gh auth status` (if `gh` is in use) returns "Logged in to github.com as <user>"
- [ ] The operation that was just attempted is visible in the GitHub UI or via `gh <verb> list`

## References

| File | Covers |
|---|---|
| `references/auth.md` | All three auth methods: `gh` CLI, HTTPS PAT, SSH keys. Includes the `gh-env.sh` script source and troubleshooting. |
| `references/issues.md` | View, create, label, assign, comment, close, search, bulk operations. Includes bug report / feature request templates. |
| `references/pr-workflow.md` | Branch → commit → push → open PR → watch CI → fix failures → merge. CI troubleshooting, conventional commits, PR body templates. |
| `references/code-review.md` | Pre-push self-review checklist, reviewing a PR end-to-end, leaving inline comments, submitting a formal review (approve / request changes / comment). |
| `references/repo-management.md` | Clone, create, fork, settings, branch protection, secrets, releases, Actions workflows, gists, GitHub API cheatsheet. |
