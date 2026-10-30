#!/usr/bin/env python3
"""
Hermes 7-Agent Profile Provisioning Script
Location: /Users/mac/.trade/fix_profiles.py
Run this after: hermes profile install (to register profiles)
                 OR after adding a new profile
Purpose: Ensures all profiles have complete config.yaml + data subdirs + state files
"""
import os, yaml, json

BASE_HOME = "/Users/mac/.hermes"
PROFILES_DIR = os.path.join(BASE_HOME, "profiles")
SALES_HOME = "/Users/mac/Documents/SouthernMachinerySales"

PROFILES = [
    "orchestrator", "leadhunter", "inboxsorter",
    "solutionarchitect", "negotiator", "postsales", "contentrepurposer"
]

SUBDIRS = [
    "sessions", "logs", "skills", "memories", "cron", "hooks", "sandboxes",
    "cache", "audio_cache", "image_cache", "backups", "migration", "pairing",
    "state-snapshots", "webui", "kanban"
]

DBFILES = [
    "state.db", "kanban.db", "response_cache.db",
    "models_dev_cache.json", "provider_models_cache.json",
    "ollama_cloud_models_cache.json"
]

TOOLSETS = {
    "orchestrator":      ["hermes-cli", "web", "terminal", "file", "skills", "delegation"],
    "leadhunter":       ["hermes-cli", "web", "terminal", "file", "skills", "delegation"],
    "inboxsorter":      ["hermes-cli", "web", "terminal", "file", "skills"],
    "solutionarchitect":["hermes-cli", "web", "terminal", "file", "skills"],
    "negotiator":       ["hermes-cli", "web", "terminal", "file", "skills"],
    "postsales":        ["hermes-cli", "web", "terminal", "file", "skills"],
    "contentrepurposer":["hermes-cli", "web", "terminal", "file", "skills"],
}

def main():
    with open(os.path.join(BASE_HOME, "config.yaml")) as f:
        main_cfg = yaml.safe_load(f)

    model_cfg = main_cfg["model"]
    agent_cfg = main_cfg.get("agent", {})
    terminal_cfg = main_cfg.get("terminal", {})

    for prof in PROFILES:
        pdir = os.path.join(PROFILES_DIR, prof)
        print(f"[PROVISION] {prof}")

        # Fix 1: Create all data subdirectories
        for sub in SUBDIRS:
            os.makedirs(os.path.join(pdir, sub), exist_ok=True)
        for db in DBFILES:
            open(os.path.join(pdir, db), "a").close()
        print(f"  [OK] Data dirs + state files created")

        # Fix 2: Write complete config.yaml (with real API credentials)
        profile_cfg = {
            "model": {
                "default": model_cfg["default"],
                "provider": model_cfg["provider"],
                "base_url": model_cfg["base_url"],
                "api_key": model_cfg["api_key"],
            },
            "providers": {},
            "fallback_providers": [],
            "credential_pool_strategies": {"gemini": "fill_first"},
            "toolsets": TOOLSETS[prof],
            "agent": agent_cfg,
            "terminal": terminal_cfg,
        }
        config_path = os.path.join(pdir, "config.yaml")
        with open(config_path, "w") as f:
            yaml.dump(profile_cfg, f, default_flow_style=False, allow_unicode=True)
        print(f"  [OK] config.yaml written (model={model_cfg['default']})")

        # Update hermes.json
        with open(os.path.join(pdir, "hermes.json"), "w") as f:
            json.dump({
                "model": {"default": model_cfg["default"], "provider": model_cfg["provider"]},
                "toolsets": TOOLSETS[prof],
                "agent": agent_cfg,
            }, f, indent=2)

    print("\n=== Provisioning Complete ===")
    for prof in PROFILES:
        pdir = os.path.join(PROFILES_DIR, prof)
        cfg = os.path.exists(os.path.join(pdir, "config.yaml"))
        dirs_ok = all(os.path.exists(os.path.join(pdir, s)) for s in SUBDIRS)
        print(f"  {prof}: config.yaml={cfg}, all_dirs={dirs_ok}")

if __name__ == "__main__":
    main()
