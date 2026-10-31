#!/usr/bin/env python3
"""Render a Southern Machinery bilingual factory (FQC/OQC) inspection checklist.

Usage:
  python3 scripts/build_checklist.py <checklist.json> --out <dir> [--config config/default.json] [--release]

Input : checklist.json (format: references/field-spec.md)
Output: <MODEL>-FQC-Checklist-CN.pdf, <MODEL>-FQC-Checklist-EN.pdf (A4 landscape, tick boxes),
        <MODEL>-FQC-Checklist-CN-EN.xlsx (sheets: 中文版 / English / 待确认 TBD / 抽样与判定 Sampling),
        <MODEL>-TBD-Questions.md (bilingual clarification list)
--release refuses to render while any item is S (suggested) or T (TBD).
Needs: pip install openpyxl weasyprint ; a CJK font (Noto Sans SC) installed.
"""
import argparse, base64, json, os, sys

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.drawing.image import Image as XLImage

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

T = {
 "zh": dict(sheet="中文版", sub="中文版", title="出厂检验 Checklist",
   head=[("型号", "{model}"), ("适配 / 配置", "{compatible}"), ("序列号", ""), ("客户", ""), ("订单 / PI 号", ""), ("目的地 / 电压", ""), ("检验员", ""), ("检验日期", "")],
   cols=["编号", "等级", "检查项目", "判定标准", "标准值 / 下限 ~ 上限", "检验方法 / 工具", "抽样", "依据来源", "判定结果", "实测值", "结论 / 备注", "检验员", "日期"],
   res=["合格", "不合格", "NA"], boxes="☐ 合格<br>☐ 不合格<br>☐ NA",
   summary=["检验项数", "合格", "不合格", "NA", "总判定  ☐ 放行   ☐ 特采放行   ☐ 不放行 / 返工"],
   sign=["检验员签字 / 日期", "QC 主管签字 / 日期", "客户见证签字 / 日期"],
   legend="等级：CR 致命 / MA 主要 / MI 次要。★ = 建议值（资料未给出，按通用标准建议，待确认）；“待确认 / TBD” = 资料缺失，未填数值。依据来源：手册章节与页码 / 产品页章节 / 视频时间点 / 通用标准编号。术语见 glossary。",
   tbd="待确认 / TBD", draft="草稿 – 含建议值或待确认项，不得用于正式放行", rules="抽样与判定规则"),
 "en": dict(sheet="English", sub="English", title="Factory Inspection Checklist",
   head=[("Model", "{model}"), ("Machine / config", "{compatible}"), ("Serial No.", ""), ("Customer", ""), ("Order / PI No.", ""), ("Destination / voltage", ""), ("Inspector", ""), ("Date", "")],
   cols=["No.", "Grade", "Check item", "Acceptance criterion", "Nominal / LSL ~ USL", "Method / tool", "Sampling", "Source", "Result", "Measured", "Conclusion / remark", "Inspector", "Date"],
   res=["Pass", "Fail", "NA"], boxes="☐ Pass<br>☐ Fail<br>☐ NA",
   summary=["Items", "Pass", "Fail", "NA", "Overall  ☐ Release   ☐ Concession   ☐ Hold / rework"],
   sign=["Inspector signature / date", "QC manager signature / date", "Customer witness signature / date"],
   legend="Grade: CR critical / MA major / MI minor. ★ = suggested value (not in the sources, proposed from general practice, to be confirmed); 'TBD' = data missing, no value entered. Source: manual section and page / product page section / video time / general-practice code. Terms per glossary.",
   tbd="TBD", draft="DRAFT – contains suggested or TBD items, not for formal release", rules="Sampling & judgement rules"),
}


def spec_text(spec, status, lang, cfg):
    if status == "T":
        return T[lang]["tbd"]
    if not spec:
        return "—"
    s = spec.get("nominal", "")
    lo, hi = spec.get("lsl"), spec.get("usl")
    if lo or hi:
        rng = f"{lo or '—'} ~ {hi or '—'}"
        s = f"{s} / {rng}" if s else rng
    if spec.get("unit"):
        s += " " + spec["unit"]
    if status == "S":
        s += " ★"
    return s


def items(data, lang):
    for sec in data["sections"]:
        yield "sec", f"{sec['code']}  {sec[lang]}"
        for it in sec["items"]:
            L = it[lang]
            crit = L["criterion"]
            if it["status"] == "T":
                crit = f"{T[lang]['tbd']}：{crit}" if lang == "zh" else f"{T[lang]['tbd']}: {crit}"
            yield "item", it, [it["id"], it["grade"], L["item"], crit, spec_text(it.get("spec"), it["status"], lang, None),
                               L["method"], L["sampling"], L["source"]]


def build_xlsx(data, cfg, path):
    c = cfg["brand"]["colors"]; m = data["meta"]
    thin = Side(style="thin", color=c["muted"]); B = Border(left=thin, right=thin, top=thin, bottom=thin)
    wb = Workbook(); wb.remove(wb.active)
    widths = [6, 6, 14, 36, 15, 24, 9, 18, 9, 11, 15, 9, 9]
    for lang in ("zh", "en"):
        t = T[lang]; ws = wb.create_sheet(t["sheet"])
        for k, w in enumerate(widths): ws.column_dimensions[chr(65 + k)].width = w
        img = XLImage(os.path.join(HERE, cfg["brand"]["logo"])); img.width, img.height = 150, 42; ws.add_image(img, "A1")
        ws.row_dimensions[1].height = 34
        ws.merge_cells("D1:M1"); ws["D1"] = f"{m['model']} {m['product_name'][lang]} — {t['title']}"; ws["D1"].font = Font(bold=True, size=15, color=c["navy"])
        ws.merge_cells("D2:M2"); ws["D2"] = f"{cfg['brand']['short']} · {cfg['brand']['contact']} · {m['doc_no']} Rev. {m['doc_rev']} · template {cfg['template_version']}"; ws["D2"].font = Font(size=8, color=c["grey"])
        if m.get("status") != "released":
            ws.merge_cells("D3:M3"); ws["D3"] = t["draft"]; ws["D3"].font = Font(bold=True, size=9, color=c["tbd"])
        r = 4
        for col in "ABCDEFGHIJKLM": ws[f"{col}{r}"].fill = PatternFill("solid", fgColor=c["green"])
        ws.row_dimensions[r].height = 4
        hd = [(a, b.format(**m)) for a, b in t["head"]]
        for k in range(0, 8, 2):
            r += 1
            for j, (col1, col2, col3) in enumerate(((1, 2, 5), (6, 7, 11))):
                a, b = hd[k + j]
                x = ws.cell(r, col1, a); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=c["navy"])
                ws.merge_cells(start_row=r, start_column=col2, end_row=r, end_column=col3); ws.cell(r, col2, b)
            for cc in range(1, 14): ws.cell(r, cc).border = B
            ws.row_dimensions[r].height = 18
        r += 2; hdr = r
        for cc, v in enumerate(t["cols"], 1):
            x = ws.cell(r, cc, v); x.font = Font(bold=True, color="FFFFFF", size=9); x.fill = PatternFill("solid", fgColor=c["navy"])
            x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); x.border = B
        ws.row_dimensions[r].height = 30
        dv = DataValidation(type="list", formula1='"%s"' % ",".join(t["res"]), allow_blank=True); ws.add_data_validation(dv)
        first = r + 1; nsec = 0
        for row in items(data, lang):
            r += 1
            if row[0] == "sec":
                nsec += 1
                ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=13)
                x = ws.cell(r, 1, row[1]); x.font = Font(bold=True, color=c["navy"]); x.fill = PatternFill("solid", fgColor=c["light"])
                continue
            it, vals = row[1], row[2]
            for cc, v in enumerate(vals, 1):
                x = ws.cell(r, cc, v); x.alignment = Alignment(wrap_text=True, vertical="top")
                color = c["navy"] if cc == 1 else ("000000")
                if cc in (4, 5) and it["status"] == "S": color = c["suggest"]
                if cc in (4, 5) and it["status"] == "T": color = c["tbd"]
                x.font = Font(size=9, bold=(cc == 1), color=color)
            for cc in range(1, 14): ws.cell(r, cc).border = B
            dv.add(ws.cell(r, 9)); ws.cell(r, 9).alignment = Alignment(horizontal="center", vertical="center")
            ln = max(len(vals[3]) / (19 if lang == "zh" else 34), len(vals[5]) / (13 if lang == "zh" else 23), len(vals[7]) / (10 if lang == "zh" else 17), 1)
            ws.row_dimensions[r].height = max(28, 13 * (int(ln) + 1))
        last = r
        ws.freeze_panes = ws.cell(hdr + 1, 1)
        r += 2; s = t["summary"]
        ws.cell(r, 1, s[0]).font = Font(bold=True); ws.cell(r, 3, f"=COUNTA(A{first}:A{last})-{nsec}")
        for j, (lab, val) in enumerate(((s[1], t["res"][0]), (s[2], t["res"][1]), (s[3], t["res"][2]))):
            ws.cell(r, 4 + j * 2, lab).font = Font(bold=True); ws.cell(r, 5 + j * 2, f'=COUNTIF(I{first}:I{last},"{val}")')
        r += 1; ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=13); ws.cell(r, 1, s[4]).font = Font(bold=True, color=c["navy"])
        r += 2
        for k, sg in enumerate(t["sign"]):
            col = (1, 5, 10)[k]; ws.cell(r, col, sg).font = Font(bold=True, size=9); ws.cell(r + 1, col, "______________________")
        r += 3; ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=13)
        x = ws.cell(r, 1, t["legend"]); x.alignment = Alignment(wrap_text=True, vertical="top"); x.font = Font(size=8, color=c["grey"]); ws.row_dimensions[r].height = 36
        ws.page_setup.orientation = "landscape"; ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_title_rows = f"{hdr}:{hdr}"; ws.page_margins.left = ws.page_margins.right = 0.3
        ws.oddFooter.center.text = f"{cfg['brand']['short']} · {cfg['brand']['contact']} · &P / &N"; ws.oddFooter.center.size = 7
    # TBD sheet
    ws = wb.create_sheet("待确认 TBD")
    for k, w in enumerate([7, 8, 22, 50, 50, 28]): ws.column_dimensions[chr(65 + k)].width = w
    hdr = ["编号 No.", "状态 Status", "检查项目 Item", "待澄清问题（中文）", "Question (English)", "依据来源 Source"]
    for cc, v in enumerate(hdr, 1):
        x = ws.cell(1, cc, v); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=c["navy"])
    r = 1
    for sec in data["sections"]:
        for it in sec["items"]:
            if it["status"] in ("S", "T"):
                r += 1
                q = it.get("question", {})
                for cc, v in enumerate([it["id"], cfg["status"][it["status"]]["zh"] + " " + it["status"], it["zh"]["item"] + " / " + it["en"]["item"], q.get("zh", ""), q.get("en", ""), it["zh"]["source"]], 1):
                    x = ws.cell(r, cc, v); x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = B
    # Sampling sheet
    ws = wb.create_sheet("抽样与判定 Sampling")
    ws.column_dimensions["A"].width = 90; ws.column_dimensions["B"].width = 90
    sp = cfg["sampling"]; jd = cfg["judgement"]
    rows = [("抽样规则", "Sampling rules"), (sp["unit_rule"]["zh"], sp["unit_rule"]["en"]), (sp["lot_rule"]["zh"], sp["lot_rule"]["en"]), ("判定规则", "Judgement rules")] + list(zip(jd["zh"], jd["en"]))
    for i, (a, b) in enumerate(rows, 1):
        for cc, v in ((1, a), (2, b)):
            x = ws.cell(i, cc, v); x.alignment = Alignment(wrap_text=True, vertical="top")
            x.font = Font(bold=a in ("抽样规则", "判定规则"), color=c["navy"] if a in ("抽样规则", "判定规则") else "000000")
        ws.row_dimensions[i].height = 32
    wb.save(path)


def build_pdf(data, cfg, lang, path):
    import weasyprint
    c = cfg["brand"]["colors"]; m = data["meta"]; t = T[lang]; b = cfg["brand"]
    logo = base64.b64encode(open(os.path.join(HERE, b["logo"]), "rb").read()).decode()
    font = cfg["page"]["font"]
    css = f"""
@page {{ size: A4 landscape; margin: 10mm 8mm 12mm 8mm;
  @bottom-center {{ content: "{b['short']} · {b['contact']} · {m['doc_no']} Rev. {m['doc_rev']} · " counter(page) " / " counter(pages); font-family: '{font}'; font-size: 6.8pt; color: #{c['grey']}; }} }}
body {{ font-family: '{font}', sans-serif; font-size: 7.1pt; color: #222; }}
.top {{ display:flex; align-items:center; border-bottom: 3px solid #{c['green']}; padding-bottom:4px; }}
.top img {{ height: 32px; margin-right: 12px; }} .top h1 {{ font-size: 13.5pt; color:#{c['navy']}; margin:0; }}
.top .s {{ color:#{c['grey']}; font-size:7.5pt; }} .top .r {{ margin-left:auto; text-align:right; font-size:6.8pt; color:#{c['grey']}; }}
.draft {{ color:#{c['tbd']}; font-weight:700; font-size:7.5pt; margin-top:2px; }}
table {{ width:100%; border-collapse: collapse; }} td, th {{ border: 0.6pt solid #{c['muted']}; padding: 2px 3px; vertical-align: top; }}
.hd td {{ height: 14px; }} .hd td.k {{ background:#{c['navy']}; color:#fff; font-weight:700; width:10%; }}
thead th {{ background:#{c['navy']}; color:#fff; font-weight:700; font-size:7pt; }} thead {{ display: table-header-group; }}
tr {{ page-break-inside: avoid; }} tr.sec td {{ background:#{c['light']}; color:#{c['navy']}; font-weight:700; border-left: 3pt solid #{c['green']}; font-size:8pt; }}
td.id {{ color:#{c['navy']}; font-weight:700; }} .S {{ color:#{c['suggest']}; }} .T {{ color:#{c['tbd']}; font-weight:700; }}
td.res {{ white-space: nowrap; font-size: 6.9pt; line-height: 1.35; }} .src {{ font-size: 6.5pt; color:#{c['grey']}; }}
.sum td {{ height: 16px; }} .sig td {{ height: 32px; width:33%; font-weight:700; }}
.rules {{ font-size: 6.8pt; margin-top: 5px; }} .rules b {{ color:#{c['navy']}; }} .leg {{ font-size: 6.5pt; color:#{c['grey']}; margin-top:4px; }}
"""
    hd = [(a, v.format(**m)) for a, v in t["head"]]
    hdh = "".join("<tr>" + "".join(f"<td class='k'>{hd[k + j][0]}</td><td>{hd[k + j][1]}</td>" for j in (0, 1)) + "</tr>" for k in range(0, 8, 2))
    w = [3.2, 3.2, 8.5, 20, 9.5, 13, 5.5, 9.5, 6.3, 6, 7.3, 4.2, 3.8]
    th = "".join(f"<th style='width:{w[i]}%'>{x}</th>" for i, x in enumerate(t["cols"]))
    body = ""
    for row in items(data, lang):
        if row[0] == "sec":
            body += f"<tr class='sec'><td colspan='13'>{row[1]}</td></tr>"; continue
        it, v = row[1], row[2]; cls = it["status"] if it["status"] in ("S", "T") else ""
        body += (f"<tr><td class='id'>{v[0]}</td><td>{v[1]}</td><td>{v[2]}</td><td class='{cls}'>{v[3]}</td><td class='{cls}'>{v[4]}</td>"
                 f"<td>{v[5]}</td><td>{v[6]}</td><td class='src'>{v[7]}</td><td class='res'>{t['boxes']}</td><td></td><td></td><td></td><td></td></tr>")
    s = t["summary"]; sp = cfg["sampling"]; jd = cfg["judgement"][lang]
    rules = f"<div class='rules'><b>{t['rules']}：</b> {sp['unit_rule'][lang]} {sp['lot_rule'][lang]} " + " ".join(f"{i + 1}) {x}" for i, x in enumerate(jd)) + "</div>"
    draft = f"<div class='draft'>{t['draft']}</div>" if m.get("status") != "released" else ""
    html = f"""<html><head><meta charset='utf-8'><style>{css}</style></head><body>
<div class='top'><img src='data:image/png;base64,{logo}'><div><h1>{m['model']} {m['product_name'][lang]} — {t['title']}</h1><div class='s'>{m.get('compatible', '')} · {t['sub']}</div>{draft}</div>
<div class='r'>{b['company']}<br>{b['contact']}<br>{m['doc_no']} · Rev. {m['doc_rev']} · template {cfg['template_version']} · {b['brand_kit']}</div></div>
<table class='hd' style='margin:5px 0'>{hdh}</table>
<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>
<table class='sum' style='margin-top:6px'><tr><td><b>{s[0]}</b></td><td></td><td><b>{s[1]}</b></td><td></td><td><b>{s[2]}</b></td><td></td><td><b>{s[3]}</b></td><td></td><td colspan='2'><b>{s[4]}</b></td></tr></table>
<table class='sig' style='margin-top:6px'><tr>{''.join(f'<td>{x}</td>' for x in t['sign'])}</tr></table>
{rules}<div class='leg'>{t['legend']}</div></body></html>"""
    weasyprint.HTML(string=html).write_pdf(path)


def build_tbd(data, path):
    m = data["meta"]; out = [f"# {m['model']} 待澄清问题清单 / Open questions", "", "| No. | 状态 Status | 项目 Item | 问题 | Question | 来源 Source |", "|---|---|---|---|---|---|"]
    n = 0
    for sec in data["sections"]:
        for it in sec["items"]:
            if it["status"] in ("S", "T"):
                n += 1; q = it.get("question", {})
                out.append(f"| {it['id']} | {it['status']} | {it['zh']['item']} / {it['en']['item']} | {q.get('zh', '')} | {q.get('en', '')} | {it['zh']['source']} |")
    out += ["", f"共 {n} 项。S = 建议值待确认；T = 资料缺失待提供。/ {n} items. S = suggested value to confirm; T = missing data to supply."]
    open(path, "w").write("\n".join(out) + "\n")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checklist"); ap.add_argument("--out", required=True)
    ap.add_argument("--config", default=os.path.join(HERE, "config", "default.json"))
    ap.add_argument("--release", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.checklist)); cfg = json.load(open(a.config))
    open_items = [it["id"] for s in data["sections"] for it in s["items"] if it["status"] in ("S", "T")]
    if a.release:
        if open_items:
            sys.exit(f"--release refused: {len(open_items)} items still S/T: {', '.join(open_items)}")
        data["meta"]["status"] = "released"
    os.makedirs(a.out, exist_ok=True); mdl = data["meta"]["model"]
    build_xlsx(data, cfg, os.path.join(a.out, f"{mdl}-FQC-Checklist-CN-EN.xlsx"))
    build_pdf(data, cfg, "zh", os.path.join(a.out, f"{mdl}-FQC-Checklist-CN.pdf"))
    build_pdf(data, cfg, "en", os.path.join(a.out, f"{mdl}-FQC-Checklist-EN.pdf"))
    n = build_tbd(data, os.path.join(a.out, f"{mdl}-TBD-Questions.md"))
    total = sum(len(s["items"]) for s in data["sections"])
    print(f"OK {mdl}: {total} items, {n} open (S/T) -> {a.out}")


if __name__ == "__main__":
    main()
