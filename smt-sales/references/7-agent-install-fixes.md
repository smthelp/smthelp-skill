# 7-Agent Installation Fixes (June 2026)

**Skill:** `smt-sales`
**Applies to:** All 7 Hermes profile installations for Southern Machinery
**Provisoning script:** `/Users/mac/.trade/fix_profiles.py`

## The 4 Must-Apply Fixes

These fixes were discovered through repeated installation attempts. Always apply when reinstalling or adding a new profile.

---

### Fix 1: Data Directories Missing

**Problem:** Individual profile dirs (`profiles/orchestrator/`, etc.) only contain AGENT.md/SOUL.md + hermes.json. Hermes requires standard data subdirectories — without them, the profile cannot run sessions, store memories, or execute cron jobs.

**Required subdirectories per profile:**
```
sessions/  logs/  skills/  memories/  cron/  hooks/  sandboxes/
cache/  audio_cache/  image_cache/  backups/  migration/  pairing/
state-snapshots/  webui/  kanban/
```

**Required state files per profile:**
```
state.db  state.db-shm  state.db-wal
kanban.db  response_store.db
models_dev_cache.json  provider_models_cache.json
ollama_cloud_models_cache.json
```

**Fix:** Run `/Users/mac/.trade/fix_profiles.py` (Python script that creates all dirs + files for all 7 profiles).

**Verification:**
```bash
for p in orchestrator leadhunter inboxsorter solutionarchitect negotiator postsales contentrepurposer; do
  dirs=$(ls /Users/mac/.hermes/profiles/$p/ | grep -v "\.md\|\.json\|\.db" | wc -l | tr -d ' ')
  echo "$p: $dirs data subdirs"
done
# Expected: 16-19 per profile (not 2-3)
```

---

### Fix 2: Model Not Configured (config.yaml Required)

**Problem:** Setting only `hermes.json` is insufficient for API calls. `hermes.json` lacks `base_url` and `api_key` — Hermes reads the full config from `config.yaml` for the active profile. Without it, `hermes profile list` shows `--` for the model and the profile cannot make API calls.

**Fix:** Run `/Users/mac/.trade/fix_profiles.py` — it copies the model/provider/base_url/api_key from the default profile's `config.yaml` into each specialist profile's `config.yaml`.

**Verification:**
```bash
hermes profile list
# All 7 profiles should show MiniMax-M2.7-highspeed, NOT --

grep "default:" /Users/mac/.hermes/profiles/orchestrator/config.yaml
# Expected: default: MiniMax-M2.7-highspeed

grep "base_url:" /Users/mac/.hermes/profiles/leadhunter/config.yaml
# Expected: base_url: https://v1.aicodee.com/v1
```

---

### Fix 3: Distribution Install Creates Duplicate/Wrong Layout

**Problem:** Running `hermes profile install /path/to/distribution/` creates a new profile at `profiles/southern-machinery-7-agent/` with its own `home/`, `logs/`, `sessions/` etc. This is the **bundle profile**, not the 7 individual agent profiles. The actual profile dirs (`profiles/orchestrator/`, etc.) remain empty shells.

**Correct 2-step process:**

**Step 1** — Run distribution install (registers all profiles via `distribution.yaml`):
```bash
hermes profile install --name southern-machinery-7-agent --force -y \
  /Users/mac/.hermes/agents/_shared
```

**Step 2** — Provision individual profile dirs with SOUL.md + hermes.json + config.yaml + data subdirs:
```bash
python3 /Users/mac/.trade/fix_profiles.py
```

**Verification:**
```bash
hermes profile list
# Should show 8 entries: default + 7 agent profiles (all with model configured)
# southern-machinery-7-agent bundle profile may also appear (harmless)
```

---

### Fix 4: Shell Aliases Fail with Wrong Argument Order

**Symptom:** `hermes profile alias leadhunter` printed usage help instead of creating the alias.

**Root cause:** The positional argument order is `alias <profile_name>`, not `alias --name <profile_name>`. The `--name` flag is for providing a **custom** alias name, not for specifying the profile.

**Fix — correct syntax:**
```bash
hermes profile alias <profile_name> --force
# Examples:
hermes profile alias orchestrator --force
hermes profile alias leadhunter --force
hermes profile alias inboxsorter --force
hermes profile alias solutionarchitect --force
hermes profile alias negotiator --force
hermes profile alias postsales --force
hermes profile alias contentrepurposer --force
```

This creates shell wrappers at `/Users/mac/.local/bin/<name>` enabling short commands like `orchestrator chat`.

**Verification:**
```bash
ls -la /Users/mac/.local/bin/orchestrator
# Expected: -rwxr-xr-x ... orchestrator
```

---

## The Provisioning Script

Location: `/Users/mac/.trade/fix_profiles.py`

This script reads the default profile config, then provisions all 7 profiles with:
1. All 16 data subdirectories
2. All 7 state/database files
3. Complete `config.yaml` (with real API credentials)
4. Updated `hermes.json` with correct model + toolsets

**To re-run after adding a new profile:**
```bash
python3 /Users/mac/.trade/fix_profiles.py
```

---

## Known Limitation

`ls /Users/mac/Documents/SouthernMachinerySales/` may hang/timeout. Use `read_file` or `search_files` with glob pattern instead:
```bash
read_file: path="/Users/mac/Documents/SouthernMachinerySales/leads/README.md"
search_files: path="/Users/mac/Documents/SouthernMachinerySales", pattern="*.md"
```
