#!/usr/bin/env python3
"""Turn case.json + calc.json into a slide spec (deck-<lang>.json) for render16.py (or the
smt-brand-kit A4 make_deck.py - same spec format).

usage: make_spec.py <case_dir> <lang> [--calc out/calc.json] [--out out/deck-<lang>.json]
Wording lives in assets/i18n/<lang>.json; product facts in assets/machines/<id>.json; case facts in case.json.
Every number is formatted here from calc.json, so slides never hand-type a figure."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calc import load_case, compute, SKILL


class Fmt:
    def __init__(self, loc): self.t, self.d = loc["thousands"], loc["decimal"]
    def __call__(self, v, dec=0):
        s = f"{v:,.{dec}f}"
        return s.replace(",", "\0").replace(".", self.d).replace("\0", self.t)


def L(x, lang):
    """Pick the language from a {en:..., pt:...} dict (falls back to en)."""
    return x.get(lang, x.get("en", "")) if isinstance(x, dict) else x


def values(case, c, m, T, lang):
    F = Fmt(T["_locale"]); proc = m.get("process", "radial")
    sp = [F(s, 1) for s in c["spans_used"]]
    and_ = T["_locale"].get("and", "and" if lang == "en" else "e")
    v = {
        "customer": case["customer"], "board": case["board"], "board_variant": case.get("board_variant", case["board"]),
        "machine": m["name"], "process_word": T["process_word"][proc], "process_pl": T["process_pl"][proc],
        "bpp": c["bpp"], "cycle": F(c["cycle"], 0 if float(c["cycle"]).is_integer() else 1), "ppb": c["ppb"], "ppp": c["ppp"],
        "fit_count": c["fit_count"], "prog_pts": c["prog_pts"], "panels_h": F(c["panels_h"]), "boards_h": F(c["boards_h"]),
        "cph": F(c["cph"]), "per_ins": F(c["per_ins"], 2), "eff_pct": F(c["eff"] * 100), "boards_h_eff": F(c["boards_h_eff"]),
        "boards_shift": F(c["boards_shift"]), "boards_day2": F(c["boards_day2"]), "boards_month": F(c["boards_month"]),
        "days": c["days"], "shift_h": c["shift_h"], "dpw": c["dpw"], "parts_h": F(c["parts_h"]), "ops_manual": c["ops_manual"],
        "ops_machine": c["ops_machine"], "cur": c["cur"], "wage": F(c["wage"]), "factor": F(c["factor"], 1),
        "cost_op": F(c["cost_op"]), "run_cost": F(c["run_cost"]), "manual_total": F(c["manual_total"]), "auto_total": F(c["auto_total"]),
        "saving_m": F(c["saving_m"]), "saving_y": F(c["saving_y"]), "released": c["released"], "ratio": F(c["ratio"], 1) + "×",
        "manual_bph": F(c["manual_bph"]), "manual_rate": F(c["manual_rate"]), "ins_month_m": F(c["ins_month"] / 1e6, 2),
        "million": T["_locale"]["million"], "defects": F(c["defects_avoided"]), "manual_ppm": F(c["manual_ppm"]),
        "machine_ppm": F(c["machine_ppm"]), "pn_count": c["pn_count"], "pol_count": c["pol_count"],
        "feeder_stations": c["feeder_stations"], "max_lead": F(c["max_lead"], 1) if c["max_lead"] else "-",
        "lead_min": F(c["lead_min"], 1) if c["lead_min"] else "-", "lead_max": F(c["lead_max"], 1) if c["lead_max"] else "-",
        "spans_used": (", ".join(sp[:-1]) + f" {and_} " + sp[-1]) if len(sp) > 1 else (sp[0] if sp else "-"),
        "spans_slash": " / ".join(sp), "ramp_weeks": len(c["ramp"]),
        "pb_list": f" {and_} ".join(str(x) for x in c["payback_months"]),
        "pb2": F(c["pb2_months"]) if c.get("pb2_months") else "-",
    }
    return v, F


def load_lang(lang):
    """Language file merged over English, so a key not yet translated falls back to EN (qa.py warns W3)."""
    en = json.load(open(os.path.join(SKILL, "assets", "i18n", "en.json"), encoding="utf-8"))
    if lang != "en": en.update(json.load(open(os.path.join(SKILL, "assets", "i18n", lang + ".json"), encoding="utf-8")))
    return en


def build(case_dir, lang, c=None):
    case, p, m = load_case(case_dir)
    c = c or compute(case, p, m)
    if case.get("type") == "line_evaluation": return build_line(case_dir, lang, case, p, m, c)
    T = load_lang(lang)
    V, F = values(case, c, m, T, lang)
    t = lambda k: T[k].format_map(V) if isinstance(T[k], str) else [x.format_map(V) for x in T[k]]
    fm = lambda s: L(s, lang).format_map(V)
    ph = case.get("photos", {})
    pic = lambda k: os.path.join(os.path.abspath(case_dir), ph[k]["src"]) if ph.get(k) else None
    cap = lambda k: L(ph[k].get("cap", ""), lang) if ph.get(k) else ""
    money = lambda x: f"{c['cur']} {F(x)}"
    src = f"Sources: {case['test'].get('source', '')}; {case.get('bom_source', '')}; {m.get('source', '')}; {case['labour'].get('wage_source', '')}."
    S = []
    S.append({"type": "cover", "kicker": t("cover_kicker"), "title": t("cover_title"), "subtitle": t("cover_sub"),
              "image": pic("cover"), "focus": ph.get("cover", {}).get("focus", [0.5, 0.5]),
              "metrics": [{"v": f"{V['cycle']} s", "l": t("m_cycle")}, {"v": str(c["ppp"]), "l": t("m_ppp")},
                          {"v": V["boards_h_eff"], "l": t("m_bheff")}, {"v": str(c["released"]), "l": t("m_released")}],
              "notes": src + " [Measured: cycle. Planning assumption: efficiency, labour.]"})
    why = [{"h": t("why1_h"), "b": t("why1_b")}]
    if c["pol_count"]: why.append({"h": t("why2_h"), "b": t("why2_b")})
    why.append({"h": t("why3_h"), "b": fm(case["labour"]["wage_card"]) if case["labour"].get("wage_card") else t("why3_b")})
    S.append({"type": "cards", "kicker": t("why_kicker"), "title": t("why_title"), "cols": 1, "cards": why,
              "image": pic("why"), "caption": cap("why"), "notes": "Polarised parts from BOM; wage: " + case["labour"].get("wage_source", "")})
    S.append({"type": "steps", "kicker": t("test_kicker"), "title": t("test_title"),
              "steps": [{"h": t(f"t{i}_h"), "b": t(f"t{i}_b")} for i in range(1, 5)],
              "image": pic("test"), "caption": cap("test"),
              "notes": f"[Measured] {case['test'].get('source', '')}. Program points per board in test: {c['prog_pts']}; BOM: {c['ppb']}."})
    cols = t("bom_cols")
    rows = [cols] + [[b["refs"], L(b["desc"], lang), b["value"], str(b["qty"]), F(b["span_mm"], 1) if b.get("span_mm") else "-",
                      "✓" if b.get("fit", True) else "—"] for b in case["bom"]]
    rows.append(["", t("bom_total"), "", str(c["ppb"]), "", ""])
    S.append({"type": "table", "kicker": t("bom_kicker"), "title": t("bom_title") if c["fit_count"] == c["bom_total"] else t("bom_title_partial"),
              "lead": t("bom_lead"), "colw": [0.16, 0.28, 0.2, 0.1, 0.14, 0.12], "rows": rows,
              "note": L(case.get("out_of_scope", ""), lang), "notes": case.get("bom_source", "")})
    S.append({"type": "metrics", "kicker": t("cap_kicker"), "title": t("cap_title"),
              "metrics": [{"v": V["panels_h"], "l": t("c_panels_h")}, {"v": V["boards_h"], "l": t("c_boards_h")},
                          {"v": V["cph"], "l": t("c_cph")}, {"v": f"{V['per_ins']} s", "l": t("c_per_ins")},
                          {"v": V["boards_h_eff"], "l": t("c_bheff")}, {"v": V["boards_shift"], "l": t("c_shift")},
                          {"v": V["boards_day2"], "l": t("c_day2")}, {"v": V["boards_month"], "l": t("c_month")}],
              "text": t("cap_text"), "image": pic("capacity"), "notes": src})
    wk = T["ramp_weeks"]; rr = [t("ramp_cols")]; n = len(c["ramp"])
    for r in c["ramp"]:
        i = r["week"]
        lab = wk[i - 1] if i <= 3 and i < n else (wk[3] if i == n else wk[4])
        rr.append([lab.format(n=i), F(r["rate"] * 100) + " %", F(r["boards"]), F(r["cum"])])
    S.append({"type": "table", "kicker": t("ramp_kicker"), "title": t("ramp_title"), "lead": t("ramp_lead"),
              "colw": [0.46, 0.16, 0.19, 0.19], "rows": rr, "note": t("ramp_note"), "notes": "[Concept view] week output = planned boards/h x hours x days x rate."})
    rl = t("roi_rows")
    S.append({"type": "table", "kicker": t("roi_kicker"), "title": t("roi_title"), "lead": t("roi_lead"), "colw": [0.44, 0.28, 0.28],
              "rows": [t("roi_cols"), [rl[0], str(c["ops_manual"]), str(c["ops_machine"])],
                       [rl[1], money(c["cost_op"]), money(c["cost_op"])], [rl[2], "—", money(c["run_cost"])],
                       [rl[3], money(c["manual_total"]), money(c["auto_total"])], [rl[4], "", money(c["saving_m"])],
                       [rl[5], "", money(c["saving_y"])]],
              "note": t("roi_note"), "notes": src + " Operators = ceil(parts/h / manual rate)."})
    pc = T["pb_cols"]; hdr = [pc[0], pc[1]] + [pc[2].format(m=mm) for mm in c["payback_months"]]
    prow = [[k, money(v["saving"])] + [money(v["saving"] * mm) for mm in c["payback_months"]] for k, v in c["shifts"].items()]
    S.append({"type": "table", "kicker": t("pb_kicker"), "title": t("pb_title"), "lead": t("pb_lead"),
              "colw": [1 / len(hdr)] * len(hdr), "rows": [hdr] + prow, "note": t("pb_note"),
              "notes": "Payback months = customer quote / monthly net saving. Price never shown."})
    S.append({"type": "cards", "kicker": t("sp_kicker"), "title": t("sp_title"), "cols": 2, "numbered": True,
              "cards": [{"h": fm(x["h"]), "b": fm(x["b"])} for x in m["selling_points"]], "notes": m.get("source", "")})
    S.append({"type": "metrics", "kicker": t("ben_kicker"), "title": t("ben_title"),
              "metrics": [{"v": str(c["released"]), "l": t("b_released")}, {"v": V["ratio"], "l": t("b_ratio")},
                          {"v": V["defects"], "l": t("b_defects")}, {"v": f"{V['cycle']} s", "l": t("b_cycle")}],
              "text": t("ben_text"), "image": pic("benefits"), "notes": src})
    if ph.get("gallery"):
        S.append({"type": "gallery", "kicker": t("gal_kicker"), "title": t("gal_title"),
                  "images": [{"src": os.path.join(os.path.abspath(case_dir), g["src"]), "cap": L(g["cap"], lang)} for g in ph["gallery"][:6]]})
    S.append({"type": "table", "kicker": t("spec_kicker"), "title": t("spec_title"), "colw": [0.42, 0.58],
              "rows": [t("spec_cols")] + [[L(a, lang), L(b, lang)] for a, b in m["specs"]], "notes": m.get("source", "")})
    bl = [t("a_measured"), t("a_bom"), t("a_params")]
    if c["prog_pts"] and c["prog_pts"] != c["ppb"]: bl.append(t("a_prog"))
    bl += [L(x, lang) for x in case.get("open_points", [])] + [t("a_price"), t("a_disclaimer")]
    S.append({"type": "bullets", "kicker": t("ass_kicker"), "title": t("ass_title"), "bullets": bl,
              "image": pic("assumptions"), "caption": cap("assumptions")})
    S.append({"type": "cta", "kicker": t("cta_kicker"), "title": t("cta_title"),
              "facts": [{"h": t(f"n{i}_h"), "b": t(f"n{i}_b")} for i in range(1, 4)], "text": t("cta_bar")})
    return {"title": t("deck_title"), "lang": lang, "slides": S, "template_text": T.get("template_text", {})}


def build_line(case_dir, lang, case, p, M, c):
    """Line evaluation (several boards, one machine group per process, e.g. radial + odd-form)."""
    from mark_board import mark
    T = load_lang(lang); F = Fmt(T["_locale"]); PN = T["process_name"]
    out = os.path.join(case_dir, "out"); os.makedirs(out, exist_ok=True)
    A = lambda r: os.path.join(os.path.abspath(case_dir), r)
    ph = case.get("photos", {})
    grp = {g["process"]: g for g in c["line"]}
    rad, odd = grp.get("radial"), grp.get("oddform")
    line_desc = " + ".join(f"{g['qty']} × {g['name']} {PN[g['process']]}" for g in c["line"])
    V = {"customer": case["customer"], "board_count": c["board_count"], "line_desc": line_desc[0].upper() + line_desc[1:],
         "radial_name": rad["name"] if rad else "-", "odd_name": odd["name"] if odd else "-",
         "odd_stations": len(odd["stations"]) if odd and odd["stations"] else (odd["qty"] if odd else 0),
         "rate_min": F(c["rate_min"]), "rate_max": F(c["rate_max"]), "eff_pct": F(c["eff"] * 100),
         "plan_min": F(c["rate_min"] * c["eff"]), "plan_max": F(c["rate_max"] * c["eff"]), "shift_h": c["shift_h"], "days": c["days"],
         "rates_list": "; ".join(f"{g['name']} ~{F(g['cph'])} CPH ({M[g['machine']].get('eval_cph_note', '')})" for g in c["line"])}
    t = lambda k, **kw: (T[k].format_map({**V, **kw}) if isinstance(T[k], str) else [x.format_map({**V, **kw}) for x in T[k]])
    cap = lambda k: L(ph[k].get("cap", ""), lang) if ph.get(k) else ""
    pic = lambda k: A(ph[k]["src"]) if ph.get(k) else None
    acc = L(case.get("accuracy_note", ""), lang)
    src = f"Sources: {case.get('source', '')}; " + "; ".join(M[g['machine']].get("source", "") for g in c["line"])
    S = []
    S.append({"type": "cover", "kicker": t("L_cover_kicker"), "title": t("L_cover_title"), "subtitle": t("L_cover_sub"),
              "image": pic("cover"), "focus": ph.get("cover", {}).get("focus", [0.5, 0.5]),
              "metrics": [{"v": str(c["board_count"]), "l": t("L_m_boards")}, {"v": str(sum(g["qty"] for g in c["line"])), "l": t("L_m_line")},
                          {"v": f"{V['rate_min']}–{V['rate_max']}", "l": t("L_m_rate")}, {"v": "±5 %" if case.get("evidence") == "photo" else "—", "l": t("L_m_acc")}],
              "notes": src + " [Estimate from photos]"})
    S.append({"type": "steps", "kicker": t("L_method_kicker"), "title": t("L_method_title"),
              "steps": [{"h": t(f"L_s{i}_h"), "b": t(f"L_s{i}_b")} for i in range(1, 5)], "image": pic("method"), "caption": cap("method"), "notes": acc})
    cards = []
    for g in c["line"]:
        cards.append({"h": t("L_grp_h", name=g["name"], proc=PN[g["process"]]),
                      "b": t("L_grp_b_" + g["process"], qty=g["qty"], name=g["name"], cph=F(g["cph"]), stations=" / ".join(g["stations"]))})
    S.append({"type": "cards", "kicker": t("L_line_kicker"), "title": t("L_line_title"), "cols": 1, "cards": cards,
              "image": pic("line"), "caption": cap("line"), "notes": src})
    gcol = lambda b, proc: next((x for x in b["groups"] if x["process"] == proc), None)
    rows = [t("L_sum_cols")]
    for b in c["boards"]:
        r, o = gcol(b, "radial"), gcol(b, "oddform")
        rows.append([f"{b['id']} · {b['pcb']}", str(b["bpp"]), str(b["parts_board"]), F(r["cycle"], 1) if r else "—", F(o["cycle"], 1) if o else "—", F(b["line_boards_h"])])
    S.append({"type": "table", "kicker": t("L_sum_kicker"), "title": t("L_sum_title") if c["board_count"] == 4 else t("L_sum_title_n"),
              "colw": [0.26, 0.13, 0.13, 0.16, 0.16, 0.16], "rows": rows, "note": t("L_sum_note"), "notes": src})
    cb = {x["id"]: x for x in case["boards"]}
    for b in c["boards"]:
        cbd = cb[b["id"]]; img = A(cbd["photo"])
        if cbd.get("markers"): img = mark(img, cbd["markers"], os.path.join(os.path.abspath(out), f"marked-{b['id']}.jpg"))
        mets = []
        for g in b["groups"]:
            mets.append({"v": str(g["ppp"]), "l": t("L_b_m_parts", proc=PN[g["process"]])})
            mets.append({"v": F(g["cycle"], 1), "l": t("L_b_m_cycle", qty=g["qty"], name=g["name"])})
        mets += [{"v": F(b["line_boards_h"]), "l": t("L_b_m_line")}, {"v": F(b["planned_boards_h"]), "l": t("L_b_m_plan")}]
        parts_list = ", ".join(f"{g['per_board']} {PN[g['process']]}" for g in b["groups"])
        S.append({"type": "board", "kicker": t("L_b_kicker", id=b["id"], pcb=b["pcb"], model=b["model"]),
                  "title": t("L_b_title", id=b["id"], line_boards_h=F(b["line_boards_h"]), bottleneck=b["bottleneck_name"]),
                  "image": img, "metrics": mets, "text": t("L_b_text", bpp=b["bpp"], parts_list=parts_list) + (" " + L(cbd["note"], lang) if cbd.get("note") else ""),
                  "notes": "Cycle = parts per panel / (CPH x machines) x 3600. " + (L(cbd.get("note", ""), lang))})
    if odd and any(x.get("feeders") for x in case["boards"]):
        st = odd["stations"] or sorted({k for x in case["boards"] for k in x.get("feeders", {})})
        rows = [[T["L_feed_cols0"]] + [x["id"] for x in case["boards"]]]
        for s_ in st: rows.append([s_] + [x.get("feeders", {}).get(s_, "—") for x in case["boards"]])
        n = len(case["boards"])
        S.append({"type": "table", "kicker": t("L_feed_kicker"), "title": t("L_feed_title"), "colw": [0.12] + [0.88 / n] * n,
                  "rows": rows, "note": t("L_feed_note"), "size": 13})
    bn = {b["bottleneck_name"] for b in c["boards"]}
    rows = [t("L_bal_cols", alt=(list(bn)[0] if len(bn) == 1 else "machine"))]
    for b in c["boards"]:
        o = gcol(b, "oddform")
        rows.append([b["id"], b["bottleneck_name"], F(o["util"] * 100) + " %" if o else "—", F(b["line_boards_h"]), F(b["alt_boards_h"]), "+" + F(b["alt_gain"] * 100) + " %"])
    S.append({"type": "table", "kicker": t("L_bal_kicker"), "title": t("L_bal_title", bott_main=list(bn)[0]) if len(bn) == 1 else t("L_bal_title_mixed"),
              "colw": [0.12, 0.18, 0.17, 0.17, 0.2, 0.16], "rows": rows, "note": t("L_bal_note"), "notes": "[Concept view]"})
    S.append({"type": "bullets", "kicker": t("L_ready_kicker"), "title": t("L_ready_title"), "bullets": t("L_ready"),
              "image": pic("readiness"), "caption": cap("readiness")})
    rows = [t("L_spec_cols")]
    for g in c["line"]:
        for a, b in M[g["machine"]]["specs"]: rows.append([f"{g['name']} · {L(a, lang)}", L(b, lang)])
    S.append({"type": "table", "kicker": t("L_spec_kicker"), "title": t("L_spec_title"), "colw": [0.36, 0.64], "rows": rows,
              "size": 12 if len(rows) > 10 else 13, "notes": src})
    if ph.get("gallery"):
        S.append({"type": "gallery", "kicker": t("L_gal_kicker"), "title": t("L_gal_title"),
                  "images": [{"src": A(g["src"]), "cap": L(g["cap"], lang)} for g in ph["gallery"][:6]]})
    bl = ([acc] if acc else []) + [t("L_a_rates"), t("L_a_eff")]
    bl += [f"{x['id']}: {L(x['note'], lang)}" for x in case["boards"] if x.get("note")]
    bl += [L(x, lang) for x in case.get("open_points", [])] + [t("a_price")]
    S.append({"type": "bullets", "kicker": t("L_ass_kicker"), "title": t("L_ass_title"), "bullets": bl, "size": 13})
    S.append({"type": "cta", "kicker": t("cta_kicker"), "title": t("cta_title"),
              "facts": [{"h": t(f"L_n{i}_h"), "b": t(f"L_n{i}_b")} for i in range(1, 4)], "text": t("cta_bar")})
    return {"title": t("L_deck_title"), "lang": lang, "slides": S, "template_text": T.get("template_text", {}) if lang != "en" else {}}


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    case_dir, lang = a[0], a[1]
    calc = json.load(open(a[a.index("--calc") + 1])) if "--calc" in a else None
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(case_dir, "out", f"deck-{lang}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(build(case_dir, lang, calc), open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("spec", out)
