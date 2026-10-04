#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
geo_score.py — Phase 3 六维评分（自动基线 + 硬上限规则 + Agent 待判项）

用法:
  python3 geo_score.py --scan /tmp/scan.json --out /tmp/score.json
  python3 geo_score.py --scan scan.json --rubric ../config/scoring-rubric.json \
      --manual d_manual.json --out score.json

设计:
  * mode=auto  维度: 完全由脚本按 rubric checks 打分
  * mode=semi  维度: 脚本打可量化部分，输出 needs_agent 清单
  * mode=agent 维度: 脚本只输出清单与 rubric 提示，分数留空待 Agent 填
  * cap_rules: 命中即封顶，不因其他项高分抵消
  * --manual: 传入 Agent 判定值（JSON），例如
      {"independent_source_count": 1, "independent_ratio": 0.1,
       "scenario_word_presence": 0.0, "founding_year_consistent": true}
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RUBRIC = os.path.join(HERE, "..", "config", "scoring-rubric.json")


# ----------------------------- value resolvers -----------------------------
def resolve(scan, key):
    v = scan.get(key)
    if v is None:
        # a few derived keys live under different names
        alt = {
            "canonical": "canonical_coverage",
            "has_faq_content": "has_faq_content",
            "content_depth": "avg_words",
            "data_density": "avg_data_density",
            "mirror_domains": "mirror_domains",
        }.get(key)
        if alt:
            v = scan.get(alt)
    return v


def pts_threshold(v, th):
    """th: [[min_value, points], ...] descending. First match wins."""
    if v is None:
        return 0
    for m, p in th:
        if v >= m:
            return p
    return 0


def pts_inverse_threshold(v, th):
    """Lower is better: [[max_value, points], ...] ascending."""
    if v is None:
        return 0
    for m, p in th:
        if v <= m:
            return p
    return 0


def pts_inverse_count(v, th):
    """Count of problems; 1 means 'only one, clean'."""
    if v is None:
        return 0
    v = v if isinstance(v, int) else len(v)
    for m, p in th:
        if v <= m:
            return p
    return 0


def score_check(scan, check, manual):
    key = check["key"]
    kind = check["type"]
    raw = manual.get(key, resolve(scan, key))

    if kind == "bool":
        got = check["points"] if bool(raw) else 0
    elif kind == "ratio":
        got = round((raw or 0) * check["points"], 1)
    elif kind == "threshold":
        got = pts_threshold(raw, check["thresholds"])
    elif kind == "inverse_threshold":
        got = pts_inverse_threshold(raw, check["thresholds"])
    elif kind == "inverse_count":
        got = pts_inverse_count(raw, check["thresholds"])
    else:
        got = 0
    return got, raw


# ----------------------------- cap rules -----------------------------
def eval_caps(rubric, ctx):
    """ctx: flat dict of all resolved values."""
    hits = []
    for r in rubric.get("cap_rules", []):
        try:
            if eval(r["when"], {"__builtins__": {}}, dict(ctx)):
                hits.append(r)
        except Exception:
            pass
    return hits


# ----------------------------- main -----------------------------
def main():
    ap = argparse.ArgumentParser(description="GEO audit — Phase 3 scoring")
    ap.add_argument("--scan", required=True)
    ap.add_argument("--rubric", default=DEFAULT_RUBRIC)
    ap.add_argument("--manual", help="JSON file with agent-judged values")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    scan = json.load(open(args.scan, encoding="utf-8"))
    rubric = json.load(open(args.rubric, encoding="utf-8"))
    manual = json.load(open(args.manual, encoding="utf-8")) if args.manual else {}

    # --- resolve every key once, for cap-rule evaluation ---
    ctx = {}
    for d in rubric["dimensions"]:
        for c in d.get("checks", []):
            _, raw = score_check(scan, c, manual)
            v = raw
            if isinstance(v, (list, dict)):
                v = len(v)
            ctx[c["key"]] = v if v is not None else 0
    for k, v in scan.items():
        if isinstance(v, (int, float, bool)) or v is None:
            ctx.setdefault(k, v if v is not None else 0)
        elif isinstance(v, list):
            ctx.setdefault(k, len(v))

    caps = eval_caps(rubric, ctx)

    out = {
        "rubric_version": rubric["rubric_version"],
        "scanned_at": scan.get("scanned_at"),
        "url": scan.get("url"),
        "profile": scan.get("profile"),
        "cap_rules_hit": caps,
        "dimensions": [],
        "needs_agent": [],
    }

    for d in rubric["dimensions"]:
        dim = {"id": d["id"], "name": d["name"], "en": d["en"],
               "mode": d["mode"], "weight": d["weight"],
               "counted_in_overall": d.get("counted_in_overall", True),
               "checks": []}
        total = 0.0
        for c in d.get("checks", []):
            got, raw = score_check(scan, c, manual)
            total += got
            if isinstance(raw, (list, dict)):
                raw = len(raw)
            dim["checks"].append({
                "key": c["key"], "label": c["label"],
                "value": raw, "points": got, "max": c["points"],
                "missed": c["points"] - got,
            })
        dim["baseline"] = round(total, 1)

        # apply caps
        applied = [c for c in caps if c["dimension"] == d["id"]]
        if applied:
            dim["capped_at"] = min(c["cap"] for c in applied)
            dim["cap_reasons"] = [c["reason"] for c in applied]
            dim["score_candidate"] = min(dim["baseline"], dim["capped_at"])
        else:
            dim["score_candidate"] = dim["baseline"]
        dim["score"] = round(dim["score_candidate"], 1)

        dim["missed_points"] = round(100 - dim["baseline"], 1)
        top_missed = sorted(dim["checks"], key=lambda x: -x["missed"])[:5]
        dim["top_gaps"] = [
            {"label": t["label"], "missed": t["missed"], "value": t["value"]}
            for t in top_missed if t["missed"] > 0
        ]

        if d.get("needs_agent"):
            dim["needs_agent"] = d["needs_agent"]
            out["needs_agent"].append({
                "dimension": d["id"], "name": d["name"],
                "mode": d["mode"], "items": d["needs_agent"],
            })
        out["dimensions"].append(dim)

    counted = [d for d in out["dimensions"] if d["counted_in_overall"]]
    if counted:
        out["overall_baseline"] = round(
            sum(d["score"] for d in counted) / len(counted), 1)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # --- console report ---
    print(f"\n{'='*66}")
    print(f"GEO 评分  {scan.get('url')}   (rubric v{rubric['rubric_version']})")
    print("=" * 66)
    for d in out["dimensions"]:
        flag = "" if d["counted_in_overall"] else "  [不计入综合分]"
        cap = f"  ⛔封顶{d['capped_at']}" if d.get("capped_at") is not None else ""
        print(f"  {d['id']} {d['name']:<8} baseline={d['baseline']:>5}  "
              f"→ {d['score']:>5}{cap}{flag}")
        for g in d.get("top_gaps", [])[:3]:
            print(f"        · 扣分 {g['missed']:>4.0f}  {g['label']}  (实测 {g['value']})")
    if out.get("overall_baseline") is not None:
        print("-" * 66)
        print(f"  综合基线分: {out['overall_baseline']} / 100")
    if out["needs_agent"]:
        print("-" * 66)
        print("  待 Agent 判定（脚本无法自动量化）:")
        for n in out["needs_agent"]:
            print(f"    [{n['dimension']}] {n['name']}")
            for it in n["items"]:
                print(f"        - {it}")
    print("=" * 66)
    print(f"written -> {args.out}")


if __name__ == "__main__":
    main()
