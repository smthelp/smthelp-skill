#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
geo_report.py — Phase 5 生成单文件 GEO 评估报告（无外链，可直接浏览器打开）

用法:
  python3 geo_report.py --data data.json --out output.html
  python3 geo_report.py --data data.json --template ../templates/report.html --out output.html

输入 data.json 结构见 templates/data-schema.md（与本 skill 的 data.json 一致）。
所有 CSS/JS 内联，系统字体栈，响应式，适配 prefers-reduced-motion。
"""
import argparse
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TPL = os.path.join(HERE, "..", "templates", "report.html")

E = lambda s: html.escape(str(s if s is not None else ""), quote=True)


def dcolor(s):
    if s is None:
        return "#64748b"
    if s >= 80:
        return "#22c55e"
    if s >= 60:
        return "#82bf32"
    if s >= 40:
        return "#eab308"
    if s >= 25:
        return "#f97316"
    return "#ef4444"


def ring(score, color, r=34, sw=7, size=80):
    c = 2 * 3.14159 * r
    off = c * (1 - (score or 0) / 100)
    return (f'<svg viewBox="0 0 {size} {size}" class="ring" role="img" '
            f'aria-label="{score} 分">'
            f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" '
            f'stroke="rgba(255,255,255,.08)" stroke-width="{sw}"/>'
            f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-dasharray="{c:.1f}" '
            f'stroke-dashoffset="{off:.1f}" transform="rotate(-90 {size/2} {size/2})"/></svg>')


def bar(score, color):
    return f'<div class="bar"><i style="width:{score or 0}%;background:{color}"></i></div>'


LVL = {"P0": ("致命级", "#ef4444"), "P1": ("重要级", "#f97316"), "P2": ("改进级", "#eab308")}


def build(data, tpl_path=None):
    global DEFAULT_TPL
    tpl_path = tpl_path or DEFAULT_TPL
    M = data["meta"]
    overall = M["overall"]
    oc = dcolor(overall)
    logo = M.get("logo", "")

    # ---- dimensions ----
    dims = ""
    for d in data["dimensions"]:
        s = d["score"]
        col = dcolor(s)
        score_html = ring(s, col, r=52, sw=9, size=120) if s is not None \
            else '<div class="ring-tbd">待测</div>'
        num = f"{s:g}" if s is not None else "—"
        ev = "".join(f'<li><b class="ok">✓</b>{E(x)}</li>' for x in d.get("evidence", []))
        gp = "".join(f'<li><b class="no">✕</b>{E(x)}</li>' for x in d.get("gaps", []))
        cap = ""
        if d.get("capped_at") is not None:
            cap = (f'<span class="cap" title="{E(d.get("cap_reason",""))}">'
                   f'⛔ 命中硬上限 {d["capped_at"]}</span>')
        dims += f'''
    <article class="dim">
      <div class="dim-head">
        <div class="dim-score">{score_html}<span class="dim-num" style="color:{col}">{num}</span></div>
        <div class="dim-meta">
          <h3><em>{E(d['id'])}</em> · {E(d['name'])} <span class="dim-en">{E(d.get('en',''))}</span></h3>
          <p class="dim-scope">{E(d.get('scope',''))}</p>
          {bar(s if s is not None else 0, col)}
          <span class="verdict" style="--vc:{col}">{E(d.get('verdict',''))}</span>
          {cap}
        </div>
      </div>
      <div class="dim-body">
        <div class="plist"><h4>抓取到的正面证据</h4><ul>{ev}</ul></div>
        <div class="plist"><h4>扣分缺口</h4><ul>{gp}</ul></div>
      </div>
    </article>'''

    # ---- strengths / opportunities ----
    strengths = "".join(f'''
    <div class="card s-card">
      <div class="s-no">亮点 {E(s["no"])}</div>
      <h3>{E(s["title"])}<span class="tag">{E(s.get("tag",""))}</span></h3>
      <p>{E(s["body"])}</p>
    </div>''' for s in data.get("strengths", []))

    opps = "".join(f'''
    <div class="card o-card">
      <div class="o-no">机会 {E(o["no"])}</div>
      <h3>{E(o["title"])}</h3>
      <p>{E(o["body"])}</p>
    </div>''' for o in data.get("opportunities", []))

    # ---- issues ----
    issues = ""
    for i in data.get("issues", []):
        lbl, col = LVL.get(i["level"], ("改进级", "#eab308"))
        issues += f'''
    <article class="issue" style="--lc:{col}">
      <div class="issue-head">
        <span class="lvl">{E(i["level"])}<em>{lbl}</em></span>
        <h3>{E(i["title"])}</h3>
      </div>
      <p class="issue-body">{E(i["body"])}</p>
      <div class="fix"><b>🛠 修复</b><span>{E(i["fix"])}</span></div>
    </article>'''

    # ---- roadmap ----
    road = ""
    for w in data.get("roadmap", []):
        lis = "".join(f"<li>{E(t)}</li>" for t in w["tasks"])
        road += f'''
    <div class="week">
      <div class="week-head"><span class="wk">{E(w["week"])}</span>
        <b>{E(w["theme"])}</b><em>{E(w.get("sub",""))}</em></div>
      <ul>{lis}</ul>
      <div class="wk-out">📦 产出：{E(w["output"])}</div>
    </div>'''

    tests = "".join(f'''
      <tr><td><b>{E(t["id"])}</b></td><td><span class="tt">{E(t["type"])}</span></td>
      <td class="tq">{E(t["q"])}</td><td>{E(t["watch"])}</td></tr>'''
        for t in data.get("blind_tests", []))

    scan = data.get("scan", {})
    facts = "".join(
        f'<div class="fact {k}"><span>{E(a)}</span><i>{b}</i></div>'
        for a, b, k in data.get("facts", []))

    social = data.get("social", {})

    tpl = open(tpl_path, encoding="utf-8").read() if os.path.exists(tpl_path) else FALLBACK
    rep = {
        "__TITLE__": E(M.get("report", "GEO 评估报告")),
        "__DATE__": E(M.get("date", "")),
        "__ENTITY__": E(M.get("entity", "")),
        "__FRAMEWORK__": E(M.get("framework", "")),
        "__METHOD__": E(M.get("method", "")),
        "__TARGET__": E(M.get("target", "")),
        "__DESC__": E(M.get("meta_description", "GEO 生成式引擎优化评估报告")),
        "__LOGO__": E(logo),
        "__OVERALL__": str(overall),
        "__OCOLOR__": oc,
        "__RING__": ring(overall, oc, r=94, sw=13, size=220),
        "__DIAGNOSIS__": E(M.get("diagnosis", "")),
        "__SUMMARY__": M.get("summary_html", ""),
        "__CHIPS__": "".join(
            f'<span class="chip"><b>{E(c["n"])}</b>{E(c["label"])}</span>'
            for c in data.get("chips", [])),
        "__FACTS__": facts,
        "__DIMS__": dims,
        "__DIMNOTE__": data.get("dimension_note_html", ""),
        "__STRENGTHS__": strengths,
        "__ISSUES__": issues,
        "__OPPS__": opps,
        "__ROAD__": road,
        "__ROADNOTE__": data.get("roadmap_note_html", ""),
        "__TESTS__": tests,
        "__TESTNOTE__": data.get("test_note_html", ""),
        "__CODE__": E(data.get("jsonld_sample", "")),
        "__CODENOTE__": data.get("code_note_html", ""),
        "__CTA_H2__": data.get("cta_html", "让 AI 在下一次被询盘前，先认识你的品牌。"),
        "__CTA_P__": data.get("cta_sub_html", ""),
        "__LI__": E(social.get("linkedin_company", "#")),
        "__LIP__": E(social.get("linkedin_profile", "#")),
        "__TW__": E(social.get("twitter", "#")),
        "__FB__": E(social.get("facebook", "#")),
        "__YT__": E(social.get("youtube", "#")),
        "__CAT__": E(social.get("catalog", "#")),
        "__CATNAME__": E((social.get("catalog", "") or "").replace("https://", "")),
        "__PH__": E(social.get("photos", "#")),
        "__PHNAME__": E((social.get("photos", "") or "").replace("https://", "")),
        "__FOOTNOTE__": E(M.get("footer_note", "")),
    }
    for k, v in rep.items():
        tpl = tpl.replace(k, v)
    return tpl


FALLBACK = "<!DOCTYPE html><html><body><h1>template missing</h1></body></html>"


def main():
    ap = argparse.ArgumentParser(description="GEO audit — Phase 5 report rendering")
    ap.add_argument("--data", required=True)
    ap.add_argument("--template", default=DEFAULT_TPL)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    data = json.load(open(args.data, encoding="utf-8"))
    out = build(data, args.template)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"written {args.out}  bytes={len(out)}  overall={data['meta']['overall']}")


if __name__ == "__main__":
    main()
