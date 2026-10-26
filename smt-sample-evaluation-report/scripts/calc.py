#!/usr/bin/env python3
"""Capacity / ramp-up / ROI / payback / benefit model for a sample (trial) run.

usage: calc.py <case_dir> [--out calc.json]
Reads <case_dir>/case.json + assets/config/defaults.json (+ assets/machines/<id>.json) and writes raw
numbers (no rounding) to calc.json. All formulas are in references/method.md; change them
there and here together, then bump the skill version."""
import json, math, os, sys

SKILL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def load_case(case_dir):
    case = json.load(open(os.path.join(case_dir, "case.json"), encoding="utf-8"))
    p = json.load(open(os.path.join(SKILL, "assets", "config", "defaults.json"), encoding="utf-8"))
    p.update(case.get("params", {}))
    mach = lambda i: json.load(open(os.path.join(SKILL, "assets", "machines", i + ".json"), encoding="utf-8"))
    if case.get("type") == "line_evaluation":
        return case, p, {g["machine"]: mach(g["machine"]) for g in case["line"]}
    return case, p, mach(case["machine"])


def compute(case, p, m):
    if case.get("type") == "line_evaluation": return compute_line(case, p, m)
    t, lab, bom = case["test"], case["labour"], case["bom"]
    ppb = sum(b["qty"] for b in bom if b.get("fit", True))          # insertions per board on this machine
    bpp = t["boards_per_panel"]; cyc = t["cycle_s_per_panel"]
    ppp = ppb * bpp
    panels_h = 3600 / cyc
    boards_h = panels_h * bpp
    bh = boards_h * p["efficiency"]                                     # planned boards / h
    shift = bh * p["hours_per_shift"]
    month1 = shift * p["working_days_month"]
    parts_h = bh * ppb
    ops_manual = math.ceil(parts_h / p["manual_parts_per_operator_hour"] - 1e-9)
    cost_op = lab["monthly_wage"] * p["employer_factor"]
    ops_m = p["machine_operators_per_shift"]; run = p["machine_running_cost_month"]

    def saving(n):  # n shifts; running cost is per machine-month
        manual = n * ops_manual * cost_op
        auto = n * ops_m * cost_op + run
        return manual, auto, manual - auto

    man1, auto1, sav1 = saving(1)
    shifts = {str(n): dict(zip(("manual", "auto", "saving"), saving(n))) for n in p["shifts_compare"]}
    week_full = bh * p["hours_per_shift"] * p["days_per_week"]
    ramp, cum = [], 0
    for i, r in enumerate(p["ramp"]):
        w = week_full * r; cum += w; ramp.append({"week": i + 1, "rate": r, "boards": w, "cum": cum})
    manual_bph = p["manual_parts_per_operator_hour"] / ppb
    ins_month = month1 * ppb
    mppm = m.get("machine_ppm", 500)
    leads = [b["lead_mm"] for b in bom if b.get("lead_mm")] or case.get("lead_range_mm", [])
    spans = sorted({b["span_mm"] for b in bom if b.get("span_mm")})
    return {
        "ppb": ppb, "bom_total": sum(b["qty"] for b in bom), "fit_count": ppb, "bpp": bpp, "ppp": ppp, "cycle": cyc,
        "prog_pts": t.get("program_points_per_board"),
        "panels_h": panels_h, "boards_h": boards_h, "cph": boards_h * ppb, "per_ins": cyc / ppp,
        "eff": p["efficiency"], "boards_h_eff": bh, "boards_shift": shift, "boards_day2": shift * 2, "boards_month": month1,
        "parts_h": parts_h, "ops_manual": ops_manual, "ops_machine": ops_m, "cost_op": cost_op, "run_cost": run,
        "manual_total": man1, "auto_total": auto1, "saving_m": sav1, "saving_y": sav1 * 12, "shifts": shifts,
        "payback_months": p["payback_months"], "pb2_months": 12 * sav1 / shifts["2"]["saving"] if "2" in shifts else None,
        "ramp": ramp, "released": ops_manual - ops_m, "manual_bph": manual_bph, "ratio": bh / manual_bph,
        "ins_month": ins_month, "defects_avoided": ins_month * (p["manual_ppm"] - mppm) / 1e6,
        "manual_ppm": p["manual_ppm"], "machine_ppm": mppm, "pn_count": len([b for b in bom if b.get("fit", True)]),
        "pol_count": sum(b["qty"] for b in bom if b.get("polarised") and b.get("fit", True)),
        "feeder_stations": m.get("feeder_stations"), "max_lead": m.get("max_lead_mm"),
        "lead_min": min(leads) if leads else None, "lead_max": max(leads) if leads else None, "spans_used": spans,
        "lead_over_limit": [b["refs"] for b in bom if b.get("lead_mm") and m.get("max_lead_mm") and b["lead_mm"] > m["max_lead_mm"]],
        "span_unsupported": [b["refs"] for b in bom if b.get("span_mm") and m.get("spans_mm") and b["span_mm"] not in m["spans_mm"]],
        "manual_rate": p["manual_parts_per_operator_hour"], "wage": lab["monthly_wage"], "factor": p["employer_factor"],
        "cur": lab["currency"], "days": p["working_days_month"], "shift_h": p["hours_per_shift"], "dpw": p["days_per_week"],
        "params": p,
    }


def compute_line(case, p, M):
    """Multi-board, multi-machine line estimate (e.g. from PCBA photos): one machine group per process.
    group cycle = parts per panel / (eval CPH x machines) x 3600; line cycle = slowest group (bottleneck)."""
    eff = p["efficiency"]; boards = []
    for b in case["boards"]:
        bpp = b["boards_per_panel"]; groups = []
        for g in case["line"]:
            mm = M[g["machine"]]; proc = mm["process"]; qty = b.get("qty", {}).get(g["machine"], g["qty"])
            cph = g.get("cph", mm["eval_cph"]); per_board = b["parts"].get(proc, 0)
            ppp = per_board * bpp; cyc = ppp / (cph * qty) * 3600 if ppp else 0
            groups.append({"machine": g["machine"], "name": mm["name"], "process": proc, "qty": qty, "cph": cph,
                           "per_board": per_board, "ppp": ppp, "cycle": cyc,
                           "panels_h": 3600 / cyc if cyc else None, "boards_h": 3600 / cyc * bpp if cyc else None})
        cyc = max(x["cycle"] for x in groups); bott = max(groups, key=lambda x: x["cycle"])
        for x in groups: x["util"] = x["cycle"] / cyc if cyc else 0
        # balance option: one more machine on the bottleneck group
        alt = [x["cycle"] * (x["qty"] / (x["qty"] + 1) if x is bott else 1) for x in groups]
        cyc2 = max(alt)
        lb = 3600 / cyc * bpp
        boards.append({"id": b["id"], "pcb": b.get("pcb", ""), "model": b.get("model", ""), "bpp": bpp, "groups": groups,
                       "line_cycle": cyc, "bottleneck": bott["machine"], "bottleneck_name": bott["name"],
                       "line_panels_h": 3600 / cyc, "line_boards_h": lb, "planned_boards_h": lb * eff,
                       "boards_shift": lb * eff * p["hours_per_shift"], "boards_month": lb * eff * p["hours_per_shift"] * p["working_days_month"],
                       "parts_board": sum(b["parts"].values()),
                       "alt_add": bott["name"], "alt_cycle": cyc2, "alt_boards_h": 3600 / cyc2 * bpp, "alt_gain": cyc / cyc2 - 1})
    rates = [x["line_boards_h"] for x in boards]
    return {"type": "line_evaluation", "boards": boards, "board_count": len(boards), "eff": eff,
            "shift_h": p["hours_per_shift"], "days": p["working_days_month"],
            "line": [{"machine": g["machine"], "name": M[g["machine"]]["name"], "process": M[g["machine"]]["process"],
                      "qty": g["qty"], "cph": g.get("cph", M[g["machine"]]["eval_cph"]), "stations": g.get("stations", [])} for g in case["line"]],
            "rate_min": min(rates), "rate_max": max(rates), "params": p}


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(a[0], "out", "calc.json")
    case, p, m = load_case(a[0])
    c = compute(case, p, m)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(c, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    keys = ("rate_min", "rate_max") if c.get("type") == "line_evaluation" else ("boards_h_eff", "boards_month", "ops_manual", "saving_m", "saving_y", "defects_avoided")
    print(json.dumps({k: c[k] for k in keys}, indent=1))
