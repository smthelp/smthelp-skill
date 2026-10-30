---
name: github-skills-sync
description: Sync local AI agent skills to a GitHub repository. Use when asked to back up, upload, mirror, or sync skills/plugins to GitHub, or when a skills library repo must stay in sync with a local ~/.workbuddy/skills directory. Handles large repos via blobless sparse-checkout, secret scanning, and metadata-preserving diff.
---

# GitHub Skills Sync

Sync a local skills directory to a GitHub repo without destroying remote content.

## When to Use

- "Sync my skills to GitHub" / "back up my skills" / "upload skills to <repo>"
- Keeping a large skills-library repo in sync with a local install directory

## Critical: Do NOT Full-Clone Large Repos

A skills library repo with hundreds of skills can be 100MB+. A plain
`git clone --depth 1` may download the pack then hang in checkout for 15+ minutes.

Use **blobless sparse-checkout** instead — it fetches only the trees you name:

```bash
mkdir -p /tmp/skill-sync && cd /tmp/skill-sync
git init -q
git sparse-checkout init --cone
git sparse-checkout set <dir1> <dir2> ...        # only paths you need to diff
git remote add origin https://github.com/<owner>/<repo>.git
git fetch --depth 1 --filter=blob:none origin main
git checkout -q -b main FETCH_HEAD
```

This completes in seconds (3.5M instead of 96M). Pushing is also fast (seconds)
because only new objects are sent.

**To add NEW directories later, you must extend the sparse scope first:**

```bash
git sparse-checkout add <newdir1> <newdir2>
```

Otherwise new files sit outside the sparse cone and `git add` silently ignores them.

## Workflow

### 1. Inventory local skills

```bash
ls -la ~/.workbuddy/skills/            # user-level
ls -la .workbuddy/skills/              # project-level (may not exist)
```

Note symlinked skills (e.g. `ego-browser -> /path/to/real`); compare with `ls -laL`.

### 2. Secret scan BEFORE any push (mandatory)

```bash
cd ~/.workbuddy/skills/
# keys/certs
find . \( -name "*.pem" -o -name "*.key" -o -name "*.p12" -o -name "id_rsa*" \) 2>/dev/null
# API tokens in file contents
grep -rInE "(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)" .
# hardcoded personal paths
grep -rIn "/Users/<username>" --include="*.md" --include="*.py" --include="*.sh" --include="*.js" .
```

Abort and report if anything sensitive is found.

### 3. Check remote repo state and .gitignore

```bash
gh repo view <owner>/<repo> --json name,visibility,defaultBranchRef
gh api repos/<owner>/<repo>/contents/.gitignore --jq '.content' | base64 -d
```

- Confirm visibility (public vs private) and tell the user before pushing.
- Verify `.gitignore` won't silently drop needed files (`node_modules/`, `dist/`,
  `build/`, `**/.git/` are common gotchas). Check locally:
  `find . \( -name node_modules -o -name dist -o -name build \)`

### 4. Classify: new vs existing vs divergent

```bash
gh api repos/<owner>/<repo>/git/trees/main --jq '.tree[] | select(.type=="tree") | .path' > remote.txt
```

Then per local skill: **new** / **exists**.

### 5. Diff existing skills — distinguish real changes from metadata noise

`diff -rq` alone is misleading. Differences confined to frontmatter are often
just provenance metadata (e.g. upstream `metadata: {source: hermes, origin: ...}`)
plus a trailing blank line. Compare **body content** with frontmatter stripped:

```python
def split_fm(p):
    t = open(p, encoding='utf-8').read()
    if not t.startswith('---'): return t
    end = t.find('\n---', 3)
    return t[end+4:] if end != -1 else t

# strip() to ignore leading/trailing blank-line differences
body_same = split_fm(local).strip() == split_fm(remote).strip()
```

**Rule: if bodies match, do NOT overwrite.** Upstream may carry provenance
metadata that a naive overwrite would destroy. Only push skills whose body
content genuinely differs or that don't exist upstream.

### 6. Copy and stage

**Use Python `shutil.copytree`, not a shell loop with `rsync`.** A shell glob like
`smthelp-*/` carries a trailing slash, and `rsync -a src/ dst/` means "copy the
*contents* of src", not the directory. In a loop over several skills this
silently dumps every `SKILL.md` on top of each other at the destination root and
flattens `references/` subdirs into it. No error is raised.

```python
import os, shutil
for n in os.listdir(SRC):                     # no glob, no trailing slash
    if not os.path.isdir(os.path.join(SRC, n)): continue
    d = os.path.join(DST, n)
    if os.path.exists(d): shutil.rmtree(d)
    shutil.copytree(os.path.join(SRC, n), d,
                    ignore=shutil.ignore_patterns('.DS_Store'))
```

If you do use rsync, write `rsync -a "$d" "$dst/"` where `$d` has **no** trailing
slash — and verify with `ls dst/<dirname>/SKILL.md` afterwards, not just the
command's exit code.

```bash
cd /tmp/skill-sync && git add <dir1> <dir2> README.md
```

**Safety check before committing — deletions must be 0:**

```bash
git status --porcelain | grep -c '^ D'     # must print 0
git diff --cached --name-status | awk '{print $1}' | sort | uniq -c
```

sparse-checkout marks un-fetched paths `skip-worktree`, so the other hundreds of
remote skills show as neither deleted nor modified. If deletions are non-zero,
STOP — investigate before committing.

### 7. Update index/README if the repo maintains one

Many skill libraries keep a categorized index with counts, e.g.:
`# Library — skill index（357 skills / 14 categories）` and
`## Category · English（96）` followed by a comma-separated, alphabetized list.

Insert new entries in sorted order and bump both the per-category count and the
total. Verify alphabetical placement afterwards.

### 8. Commit and push

```bash
git commit -F - <<'MSG'
add N skills: <names>

- new: ...
- N skills verified content-identical, left untouched to preserve provenance
- index updated: 357 -> 361
MSG
git push origin main
```

### 9. Verify

```bash
gh api repos/<owner>/<repo>/commits/main --jq '{sha:.sha[0:7], files:.files|length}'
gh api repos/<owner>/<repo>/git/trees/main --jq '[.tree[]|select(.type=="tree")]|length'
gh api "repos/<owner>/<repo>/git/trees/main:<biggest-skill>?recursive=1" \
  --jq '[.tree[]|select(.type=="blob")]|length'   # compare to local file count
```

## Verify the push actually landed

**Never trust `git push ... | tail` — the exit code comes from `tail`, which is
always 0**, so a failed push prints "success". Verify against the remote instead:

```bash
git push origin main; echo "exit=${PIPESTATUS[0]}"   # zsh: $pipestatus[1]
gh api repos/<owner>/<repo>/commits/main --jq '{sha:.sha[0:7]}'
```

The remote SHA must match your local HEAD. If it doesn't, the push failed.

### Fallback when git push keeps failing

Network issues (HTTP2 framing, "Empty reply from server", 502 tunnel) can make
`git push` fail repeatedly. For text files, bypass git entirely with the
Contents API — it is far more reliable:

```bash
# 1) get the file's current SHA (required for updates)
gh api repos/<owner>/<repo>/contents/<path> --jq '{sha:.sha, size:.size}'

# 2) build a JSON payload, then PUT it (--input avoids huge command-line args)
gh api -X PUT repos/<owner>/<repo>/contents/<path> --input payload.json
```

```python
import base64, json
json.dump({
  "message": "...",
  "content": base64.b64encode(open(path,"rb").read()).decode(),
  "sha": "<current sha from step 1>",
  "branch": "main",
}, open("/tmp/payload.json","w"), ensure_ascii=False)
```

Afterwards reconcile the local clone:

```bash
git fetch origin main && git reset --hard origin/main   # ONLY after fetch succeeds
```

**Never `reset --hard` if the fetch failed** — it silently rewinds the working
tree to the stale remote ref and discards your edits.

`git config http.version HTTP/1.1` works around some HTTP2 framing errors, but
is not a guaranteed fix.

## Detecting and repairing index drift

A skills-library README often contains a hand-maintained index that silently
drifts from the actual directories. Always diff both directions:

```python
missing_in_index = sorted(remote_dirs - index_entries)   # repo has, index lacks
ghost_in_index   = sorted(index_entries - remote_dirs)   # index lists, repo lacks
```

Before classifying, read each missing directory's real `SKILL.md` description —
never guess from the directory name:

```bash
gh api repos/<o>/<r>/contents/<dir>/SKILL.md --jq '.content' | base64 -d
```

Expect legitimate `ghost_in_index` entries: repos often ignore nested git repos
(e.g. `.gitignore` lists `humanize/`, `self-improvement/`) while the README still
lists them under a "kept locally" note. Leave those alone.

Also expect non-skill directories (e.g. `docs/` holding only subfolders, no
`SKILL.md`) — exclude them from the index rather than forcing them in.

When adding a batch of skills, prefer a **new category** over stuffing an
unrelated suite into an existing one, and keep categories sorted by size.

## Repo-wide secret scan (when the remote is bigger than your local copy)

Local-only scanning is not enough when the remote repo already contains hundreds
of skills you didn't write. To audit the **remote** content:

**GitHub Code Search does not work on private repos** — searching for a string
you know exists returns 0 results. Verify this once (search for a phrase from the
README); if it returns 0 while a global search returns hits, code search is
unusable and you must download and scan locally.

Download every text file with the GraphQL API (batch many blobs per query):

```graphql
repository(owner:"<o>", name:"<r>") {
  object(expression: "main:<path>") { ... on Blob { text } }
}
```

Build one query per batch (40 paths works well) using aliases `f0, f1, ...`,
run 4 workers, retry 3 times. 2600 files took ~165s this way. Then regex-scan
the downloaded files locally.

Classify hits before alarming the user — most are false positives:

| Pattern | Verdict |
| --- | --- |
| `process.env.X` / `os.environ["X"]` | Safe — a reference, not a value |
| `xxx`, `abc123...`, `<YOUR_KEY>`, `EXAMPLE` | Safe — placeholder |
| `AKIAIOSFODNN7EXAMPLE`, `sk-abc...` in `test/`, `sanitize.test.js` | Safe — test fixtures |
| Cloudflare Turnstile `1x0000...AA` | Safe — public test key |
| `AIza...`, `GOCSPX-`, `AKIA`, real JWT | **Real credential** |

Report **locations and credential types only, never the values** — restating a
secret in chat or a memory file is a second leak.

### Known-prefix regexes alone miss most credentials

A first pass keyed on well-known prefixes (`AIza`, `sk-`, `AKIA`, `ghp_`, `eyJ`)
finds only the minority. In a real 400-skill repo it surfaced 5 secrets; a second
aggressive pass surfaced **13 more**. The missed ones had no recognizable prefix
at all — they were just values sitting next to a label:

- 5 SMTP app passwords listed as `` `AAAA`, `BBBB`, `CCCC` `` after "**Passwords**"
- a 4-char admin password in a markdown table row `| 密码 | xxxx |`
- an incoming-webhook URL whose last path segment *is* the secret
- an admin panel path that doubles as the password (`/admin888` + password `admin888`)

So scan for the **label**, not just the token shape. Two complementary passes:

```python
# pass 1 — known prefixes (high precision, low recall)
r"AIza[0-9A-Za-z_\-]{30,}|GOCSPX-[A-Za-z0-9_\-]+|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"

# pass 2 — label followed by a value (catches everything else)
r"(?i)\b(passwords?|secret|api[_\- ]?key|access[_\- ]?token|bearer|"
r"credential|密码|密钥|口令|令牌)\b\s*[:=：]?\s*[`\"']?([^\s`\"'|,;)\n]{4,})"
# plus markdown table rows:  ^\s*\|\s*(password|密码|api[_\- ]?key)\s*\|\s*([^|]+)\|
```

Then **narrow by directory ownership**: secrets cluster in the user's own
first-party skills (`smthelp-*`, company/CRM/marketing stack), while the bulk of
hits in vendored/doc skills (`cloudflare/references/**`, `lark-base/references/**`)
are documentation noise where `token` is just a field name. Filter to first-party
paths before triaging, or you will drown in false positives.

Also expect the *same* secret repeated across several files (docs + SKILL.md +
a references file). Always finish with a per-value residual grep over the whole
tree — fixing the file where you first spotted it is not enough.

## Redacting leaked credentials

Replace plaintext with **environment-variable references, not inert
placeholders**. A skill containing `<YOUR_API_KEY>` is dead documentation;
`${SMTHELP_IMAGE_HOST_API_KEY}` still tells the agent what to fetch and from
where. In code blocks go one step further and read it properly:

| Context | Replace with |
| --- | --- |
| curl / shell | `-H "X-API-Key: ${VAR}"` |
| Python | `os.environ["VAR"]` (add `import os`) |
| n8n header | `{{ $env.VAR }}` |
| markdown table | `` `${VAR}`（环境变量） `` |

Then add a short warning block above the credential section naming every
variable required and where to rotate it.

**Do not redact indiscriminately** — it destroys usability and wastes the user's
time. Verify each hit is actually secret:

- **OAuth Client ID** is public by design (it appears in the auth URL users see).
  Only the Client Secret requires rotation.
- **Business contact details** (email signature, WhatsApp link in `AGENTS.md`)
  are intentionally published — leave them. They only became dangerous because
  they doubled as a login username alongside a leaked password; fix the password.
- **Resource tokens** in vendor docs are usually just examples; swap them for an
  obviously-fake value rather than deleting the example.

**Redacting HEAD is not the same as removing the secret.** Git history still
contains every value, and any clone or fork keeps it. Say this explicitly and
offer `git filter-repo` as a separate, destructive follow-up that requires its
own confirmation (it rewrites every commit SHA and forces all clones to re-clone).

If the repo has an `AGENTS.md`-style rules file, check it for constraints before
editing — a common one is *"Keep the original skill count, directories, and YAML
`name` values."* Verify afterwards that frontmatter `name` is byte-identical:

```bash
for f in $(git diff --name-only); do
  diff <(git show HEAD:"$f" | sed -n '1,/^---$/p' | grep -m1 '^name:') \
       <(sed -n '1,/^---$/p' "$f" | grep -m1 '^name:') || echo "NAME CHANGED: $f"
done
```

## Writing business-domain skills: parameter traceability

When adapting generic skills for a specific company's products, **invented
parameters are more dangerous than placeholders**. A placeholder gets noticed; a
plausible-looking number survives all the way into a customer proposal.

Build one **single source of truth** reference file and make every skill point at it:

```
<skill>/references/<domain>-term-bank.md
  §2    Confirmed parameter anchors   ← the ONLY quotable numbers
  §2·C  Customer-side inputs          ← specs you ASK for, not specs you sell
```

Rules that earned their keep:

1. **Nothing outside the table gets written.** "Not in the anchor table" means
   write `per process confirmation`, not a guess.
2. **Precision figures bind to a model.** ±0.05 mm vs ±0.015 mm vs ±0.5 mm differ
   10–30×; a bare `±0.05 mm` will be copied onto the wrong machine.
3. **Separate measured from derived.** `0.8 s per component` is measured;
   `10 parts × 0.8 s = 8 s` is derived and must be labelled `theoretical cycle`.
4. **Customer-side inputs get their own section.** `0.4 mm pitch BGA`, `0201`,
   `30,000 CPH` describe the *customer's* board/line. They must never be
   repositioned as the vendor's own capability.
5. **Every output template ends with a `parameter traceability` block** listing each
   number, its model, and its source.

**Audit pass after writing** — grep every number with a unit across all skills and
diff against the anchor table. Anything unmatched is either a customer-side input
(→ move it to §2·C) or an invention (→ delete it):

```python
nums = set(re.findall(r"\d[\d,\.]*\s*(?:mm|°C|kg|CPH|s/件|PPM|N|V|Ah|m/s|L|kW|MPa)", anchor_table))
# then for each skill file, report findall(...) - nums
```

Watch for list-numbering false positives (`1. LinkedIn` → `1. L`) — filter them.

Also: **grep your own memory files after correcting a parameter.** A wrong figure
written into `MEMORY.md` or a daily log will keep resurfacing in later sessions
even after the skills themselves are fixed.

## Structural health check

A missing `SKILL.md` means an agent can never load that skill, even if the
README indexes it. Check every directory:

```bash
gh api repos/<o>/<r>/git/trees/main --jq '.tree[]|select(.type=="tree")|.path' > dirs.txt
# for each dir, check whether SKILL.md exists
```

Legitimate non-`SKILL.md` layouts:

- `docs/`-style folders holding only subfolders — not a skill, exclude from index
- CodeBuddy/Claude **expert packages**: `.codebuddy-plugin/plugin.json` +
  `agents/` + `skills/`. Validate by checking `plugin.json` has
  `name`/`version`/`description`/`author`/`agents`/`skills`. Their skill file
  lives at `skills/<name>/SKILL.md`, so a missing top-level file is normal.
- A directory with only `references/` and no `SKILL.md` is a **real defect** —
  report it, but changing it may violate the repo's own rules (e.g. an
  `AGENTS.md` saying "Keep the original skill count, directories, and YAML
  `name` values"). Read the repo's `AGENTS.md` before touching structure.

## Pitfalls

- **macOS has no `timeout`** command — don't wrap commands in it.
- **Stale lock files are not always `index.lock`.** A killed `git sparse-checkout`
  leaves `.git/info/sparse-checkout.lock` behind and every later command fails
  with "Another git process seems to be running". Confirm no git process is
  alive, then clear both:
  `rm -f .git/index.lock .git/info/sparse-checkout.lock`
- **zsh has no `$PIPESTATUS`.** Use `$pipestatus[1]` after a pipe, and plain `$?`
  when there is no pipe — `${PIPESTATUS[0]}` silently expands to empty and you
  lose the exit code you were trying to check.
- **`grep -c` exits 1 when it counts 0 matches**, which breaks `&&` chains in
  verification one-liners. Use `grep -c ... || true`, or capture then test.
- **Symlinked skills** need `ls -laL` / `rsync -a` (follows links) or you'll copy
  a dangling link instead of content.
- **Binary assets** (fonts, images) inflate the repo; confirm they uploaded by
  checking a sampled file's size via the contents API.
- **Never `git add -A`** in a sparse checkout without checking for deletions first.
- Partial (blobless) clones push fine — only new objects are transmitted.
- **A trailing slash on a glob turns into "copy contents".** `for d in X-*/` yields
  `X-foo/`, and `rsync -a X-foo/ dst/` copies the *contents*, so looping over
  several skills dumps every `SKILL.md` on top of each other at the destination
  root and flattens `references/` into it. No error is raised. Prefer
  `shutil.copytree` (see step 6). After any bulk copy, check `ls dst/` for stray
  `SKILL.md` / `references/` before you trust the exit code.

## Bidirectional version arbitration (read before any "local → remote" push)

The default assumption "local is newer, push it" is wrong for two common setups,
and acting on it silently destroys content:

1. **The local dir is a cloud-sync folder** (Baidu Netdisk / iCloud / Dropbox /
   Syncthing). Files can be silently **reverted to an older version** by the sync
   client. `mtime` is the only signal, and it is easy to miss.
2. **Another agent session, machine, or CI pushes to the same branch.** The remote
   can contain a *regression* someone else committed.

Both happened on one repo in a single day: a netdisk revert left a local skill at
v1.3.4 while the remote held v1.6.0, and a concurrent session then pushed the
local v1.3.4 **over** the remote v1.6.0, deleting a 622-line script.

### Arbitration procedure

Never push a bulk `rsync --delete` result straight to the remote. Do this first:

```bash
git fetch origin main

# 1) Does the remote have files you lack? If yes, do NOT use -s ours blindly.
comm -23 <(git ls-tree -r --name-only origin/main | sort) <(git ls-files | sort)

# 2) Separate "file mode only" noise from real content divergence.
git diff --numstat HEAD origin/main | awk '$1==0 && $2==0 {m++} $1!=0||$2!=0 {c++}
  END {print "mode-only:", m+0, "content-differs:", c+0}'

# 3) For every content-differs file, decide direction explicitly
#    (compare mtime, version: field, and the diffs themselves).
```

Mode-only churn is usually huge and meaningless (hundreds of files). Normalize it
before committing instead of letting it pollute the diff:

```bash
# strip the exec bit from everything except shell scripts
git ls-files -s | awk '$1=="100755"{print $4}' | grep -v '\.sh$' > /tmp/to644.txt
xargs -a /tmp/to644.txt -d '\n' git update-index --chmod=-x
```

`chmod` on disk is not always enough — `git update-index --chmod=-x` writes the
index directly and always works.

### Recovering the authoritative version

If the remote regressed but you have a good commit locally (or in the reflog):

```bash
git checkout <GOOD_COMMIT> -- <path>            # restore content, keep history
git merge -s ours origin/main --no-edit -m "…"  # keep your tree, record the merge
git push origin main
```

`-s ours` is only safe after step 1 confirms the remote has **zero** files you do
not have. If the remote *does* hold unique files, resolve per-file instead.

### Then fix the local copy too

After establishing which side is authoritative, **write that version back to the
local working directory**. Otherwise the cloud-sync client hands you the stale copy
again next session and the conflict recurs.

### Reporting

When arbitration changes what gets pushed, say so explicitly in the commit message
and to the user: which paths were kept from which side, and what a naive push would
have destroyed.
