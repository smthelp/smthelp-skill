---
name: github
description: "Complete GitHub workflow: auth, repo management, PRs, code review, and issues. Use when working with GitHub repositories, PRs, issues, or CI/CD."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Git, gh-cli, Repositories, Pull-Requests, Code-Review, Issues, CI/CD, Authentication]
    related_skills: []
---

# GitHub Complete Workflow

Complete guide for all GitHub operations: authentication, repository management, pull requests, code review, issues, and CI/CD. Each section shows `gh` first, then `git` + `curl` fallback.

---

## 1. Authentication

> Absorbed from `github-auth` skill.

GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. See `references/github-auth.md` for the full auth reference.

### Detection Flow

```bash
# Check what's available
git --version
gh --version 2>/dev/null || echo "gh not installed"

# Check if already authenticated
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**Decision tree:**
1. If `gh auth status` shows authenticated → use `gh` for everything
2. If `gh` is installed but not authenticated → use gh auth method
3. If `gh` is not installed → use git-only method (no sudo needed)

### Quick Setup Reference

| Method | When to Use | Key Command |
|--------|-------------|-------------|
| HTTPS + PAT | Most portable, works everywhere | `git config --global credential.helper store` |
| SSH key | Already have keys or prefer SSH | `ssh-keygen -t ed25519` + add to GitHub |
| gh CLI | gh installed, want richer API | `gh auth login` |

For full details (token scopes, SSH config, gh token login, troubleshooting), see `references/github-auth.md`.

---

## 2. Repository Management

> Absorbed from `github-repo-management` skill.

Create, clone, fork, configure, and manage GitHub repositories.

### Setup

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

# Get your GitHub username
if [ "$AUTH" = "gh" ]; then
  GH_USER=$(gh api user --jq '.login')
else
  GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")
fi
```

### Cloning

```bash
# Pure git — works identically with gh or curl
git clone https://github.com/owner/repo-name.git
git clone --depth 1 https://github.com/owner/repo-name.git
git clone --branch develop https://github.com/owner/repo-name.git

# gh shortcut
gh repo clone owner/repo-name
```

### Creating Repositories

```bash
# With gh
gh repo create my-project --public --clone
gh repo create my-org/my-project --private --description "A tool" --license MIT --clone

# With curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user/repos \
  -d '{"name": "my-project", "private": false, "auto_init": true}'
```

### Forking

```bash
# With gh
gh repo fork owner/repo-name --clone

# With curl + git
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/owner/repo-name/forks
sleep 3 && git clone https://github.com/$GH_USER/repo-name.git
git remote add upstream https://github.com/owner/repo-name.git
```

### Repository Settings

```bash
# Branch protection (curl)
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{"required_status_checks": {"strict": true, "contexts": ["ci/test"]}, "enforce_admins": false, "required_pull_request_reviews": {"required_approving_review_count": 1}}'

# Secrets (gh is dramatically simpler)
gh secret set API_KEY --body "value"
gh secret list
```

### Releases

```bash
# With gh
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release list

# With curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d '{"tag_name": "v1.0.0", "name": "v1.0.0", "body": "Changelog", "draft": false}'
```

### GitHub Actions

```bash
# gh
gh workflow list
gh run list --limit 10
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID>

# curl
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10
```

### Gists

```bash
gh gist create script.py --public --desc "Useful script"
gh gist list
```

---

## 3. Pull Request Workflow

> Absorbed from `github-pr-workflow` skill.

Full PR lifecycle: branch, commit, open, CI monitoring, merge.

### Branch Creation

```bash
git fetch origin && git checkout main && git pull origin main
git checkout -b feat/add-user-authentication
```

Branch naming: `feat/`, `fix/`, `refactor/`, `docs/`, `ci/`

### Making Commits

```bash
git add src/auth.py tests/test_auth.py
git commit -m "feat: add JWT-based user authentication"
```

Use [Conventional Commits](references/conventional-commits.md): `type(scope): description`

### Push and Create PR

```bash
git push -u origin HEAD
```

**With gh:**
```bash
gh pr create --title "feat: add user authentication" \
  --body "## Summary\n- Adds login/register endpoints\n\nCloses #42" \
  --label enhancement
```

**With curl:**
```bash
BRANCH=$(git branch --show-current)
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{\"title\": \"feat: add user authentication\", \"head\": \"$BRANCH\", \"base\": \"main\"}"
```

### Monitor CI

```bash
# gh
gh pr checks
gh pr checks --watch

# curl
SHA=$(git rev-parse HEAD)
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status
```

For CI troubleshooting patterns, see `references/ci-troubleshooting.md`.

### Auto-Fix CI Failures

```bash
# Get failure logs
gh run view <RUN_ID> --log-failed

# Fix and push
git add <fixed_files> && git commit -m "fix: resolve CI failure" && git push
```

### Merging

```bash
# gh
gh pr merge --squash --delete-branch
gh pr merge --auto --squash --delete-branch

# curl
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d '{"merge_method": "squash", "commit_title": "feat: add auth (#PR)" }'
```

For PR body templates, see `templates/pr-body-bugfix.md` and `templates/pr-body-feature.md`.

---

## 4. Code Review

> Absorbed from `github-code-review` skill.

Review local changes before pushing, or review open PRs on GitHub.

### Reviewing Local Changes (Pre-Push)

```bash
# Get the diff
git diff main...HEAD --stat
git diff main...HEAD

# Check for common issues
git diff main...HEAD | grep -n "print\|console\.log\|TODO\|FIXME\|HACK"
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*="
git diff main...HEAD | grep -n "<<<<<<\|>>>>>>\|======"
```

**Review output format:**
```
## Code Review Summary

### Critical
- **src/auth.py:45** — SQL injection: user input passed directly to query.

### Warnings
- **src/models/user.py:23** — Password stored in plaintext.

### Suggestions
- **src/utils/helpers.py:8** — Duplicates logic in src/core/utils.py:34.
```

### Reviewing a PR

```bash
# gh
gh pr view 123
gh pr diff 123

# curl
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/123

# Checkout locally for full review
git fetch origin pull/123/head:pr-123 && git checkout pr-123
gh pr checkout 123
```

### Leave Comments on a PR

```bash
# gh
gh pr comment 123 --body "Overall looks good."

# curl — general comment
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/123/comments \
  -d '{"body": "Overall looks good."}'

# curl — inline comment
HEAD_SHA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/123 \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/123/comments \
  -d "{\"body\": \"Simplify with list comprehension.\", \"path\": \"src/auth.py\", \"commit_id\": \"$HEAD_SHA\", \"line\": 45, \"side\": \"RIGHT\"}"
```

### Submit Formal Review

```bash
# gh
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."

# curl — atomic multi-comment review
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/123/reviews \
  -d '{"commit_id": "'$HEAD_SHA'", "event": "REQUEST_CHANGES", "body": "Found issues.", "comments": [{"path": "src/auth.py", "line": 45, "body": "SQL injection risk."}]}'
```

### Review Checklist

- **Correctness**: Does it do what it claims? Edge cases?
- **Security**: No hardcoded secrets? Input validation?
- **Code Quality**: Clear naming? No unnecessary complexity?
- **Testing**: New code tested? Error paths covered?
- **Performance**: No N+1 queries? Appropriate caching?
- **Documentation**: Public APIs documented?

For the structured review output template, see `references/review-output-template.md`.

---

## 5. Issues Management

> Absorbed from `github-issues` skill.

Create, search, triage, label, assign, and manage GitHub issues.

### View Issues

```bash
# gh
gh issue list
gh issue list --state open --label bug
gh issue view 42

# curl
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=open" \
  | python3 -c "import sys,json; [print(f\"#{i['number']} {i['title']}\") for i in json.load(sys.stdin) if 'pull_request' not in i]"
```

### Create Issues

```bash
# gh
gh issue create \
  --title "Login redirect ignores ?next= parameter" \
  --body "## Description\nSteps to reproduce..." \
  --label bug,backend \
  --assignee username

# curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues \
  -d '{"title": "Login redirect ignores ?next= parameter", "body": "Description", "labels": ["bug"]}'
```

### Bug Report Template

```
## Bug Description
<What's happening>

## Steps to Reproduce
1. <step>

## Expected Behavior
<What should happen>

## Actual Behavior
<What happens instead>

## Environment
- OS: <os>
- Version: <version>
```

For feature request and bug report templates, see `templates/`.

### Manage Labels and Assignment

```bash
# gh
gh issue edit 42 --add-label "priority:high" --remove-label "needs-triage"
gh issue edit 42 --add-assignee username

# curl labels
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels \
  -d '{"labels": ["priority:high"]}'
```

### Issue Triage Workflow

1. `gh issue list --label "needs-triage"`
2. Read and categorize each issue
3. Apply labels and priority
4. Assign if owner is clear
5. Comment with triage notes

---

## Quick Reference

| Action | gh | curl |
|--------|-----|------|
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create name --public` | `curl POST /user/repos` |
| Create PR | `gh pr create ...` | `curl POST /pulls` |
| View PR | `gh pr view N` | `curl GET /pulls/N` |
| Review PR | `gh pr review N --approve` | `curl POST /pulls/N/reviews` |
| CI status | `gh pr checks` | `curl GET /commits/$SHA/status` |
| Merge | `gh pr merge --squash` | `curl PUT /pulls/N/merge` |
| List issues | `gh issue list` | `curl GET /repos/o/r/issues` |
| Create issue | `gh issue create ...` | `curl POST /repos/o/r/issues` |
| Secrets | `gh secret set KEY` | `curl PUT /actions/secrets/KEY` (+ encryption) |
| Releases | `gh release create v1.0` | `curl POST /repos/o/r/releases` |

---

## References

- `references/github-auth.md` — Full authentication reference (SSH, HTTPS, gh CLI, troubleshooting)
- `references/review-output-template.md` — Structured review output format
- `references/conventional-commits.md` — Commit message format reference
- `references/ci-troubleshooting.md` — CI failure diagnosis patterns
- `templates/bug-report.md` — Bug report issue template
- `templates/feature-request.md` — Feature request issue template
- `templates/pr-body-bugfix.md` — PR body template for bug fixes
- `templates/pr-body-feature.md` — PR body template for features
- `scripts/gh-env.sh` — Auth detection helper script
