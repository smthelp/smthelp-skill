"""CLI: python -m dyh <stage> -c config.json [--run-name X] ...
Stages: scrape rank filter download frames dedupe select-template select verify upload | auto (scrape..dedupe)."""
import argparse, json, sys
from . import config, log, __version__
from . import scrape, rank, filter as flt, download, frames, dedupe, select, verify, deliver, sinks
from .errors import DyhError

def main(argv=None):
    ap = argparse.ArgumentParser(prog="dyh", description="Douyin profile video harvester")
    ap.add_argument("stage", choices=["scrape", "rank", "filter", "list", "download", "frames", "dedupe",
                                      "select-template", "select", "verify", "upload", "auto", "version"])
    ap.add_argument("-c", "--config"); ap.add_argument("--run-name"); ap.add_argument("--profile",
                    help="profile URL or sec_uid (scrape/auto)")
    ap.add_argument("--ids", nargs="*", help="limit download to these aweme_ids or ranks")
    ap.add_argument("--manifest-copy", help="also write manifest CSV here (upload)")
    ap.add_argument("--set", action="append", default=[], help='override, e.g. --set select.count=10')
    a = ap.parse_args(argv)
    if a.stage == "version": print(__version__); return 0
    ov = {}
    if a.run_name: ov["run_name"] = a.run_name
    for kv in a.set:
        k, v = kv.split("=", 1); cur = ov; ks = k.split(".")
        for x in ks[:-1]: cur = cur.setdefault(x, {})
        try: cur[ks[-1]] = json.loads(v)
        except json.JSONDecodeError: cur[ks[-1]] = v
    try:
        cfg = config.load(a.config, ov)
        log.setup(cfg["run_dir"], cfg["log_level"]); log.event("cli", "start", command=a.stage, version=__version__)
        prof = a.profile or cfg.get("profile")
        if a.stage in ("scrape", "auto"):
            if not prof: raise DyhError("E_CONFIG", "--profile or config.profile required")
            scrape.run(cfg, prof)
        if a.stage in ("rank", "auto"): rank.run(cfg)
        if a.stage in ("filter", "auto"): flt.run(cfg)
        if a.stage in ("list",): flt.print_table(cfg)
        if a.stage in ("download", "auto"): download.run(cfg, a.ids)
        if a.stage in ("frames", "auto"): frames.run(cfg)
        if a.stage in ("dedupe", "auto"): dedupe.run(cfg)
        if a.stage == "select-template": print(select.template(cfg))
        if a.stage == "select": select.run(cfg, sinks.make(cfg).existing_names())
        if a.stage == "verify": verify.run(cfg)
        if a.stage == "upload": deliver.run(cfg, a.manifest_copy)
        return 0
    except DyhError as e:
        log.get("cli").error(str(e)); return e.exit

if __name__ == "__main__":
    sys.exit(main())
