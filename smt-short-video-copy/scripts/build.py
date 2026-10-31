#!/usr/bin/env python3
"""smt-short-video-copy renderer.

usage: python3 build.py <kit_dir> [--out <dir>]
<kit_dir> holds videos.py (META, V, PLAT, CTA_EN, CTA_ZH, DISCLAIM_EN, DISCLAIM_ZH)
and checklist.py (META_FAT, SECTIONS, ITEMS); formats in ../templates/kit/.
Writes to <out> (default <kit_dir>/out):
  <MODEL>_短视频文案包_<n>主题_CN-EN.docx, <MODEL>_出厂验收检查表_中文.xlsx,
  <MODEL>_Factory_Acceptance_Checklist_EN.xlsx, srt/<Vxx>_EN|ZH.srt, <MODEL>_SRT_字幕.zip
"""
import sys, os, re, zipfile, argparse
ap = argparse.ArgumentParser(); ap.add_argument("kit"); ap.add_argument("--out")
ARGS = ap.parse_args()
sys.path.insert(0, os.path.abspath(ARGS.kit))
from videos import META, V, PLAT, CTA_EN, CTA_ZH, DISCLAIM_EN, DISCLAIM_ZH
from checklist import META_FAT, SECTIONS, ITEMS
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.abspath(ARGS.out or os.path.join(ARGS.kit, "out")); os.makedirs(OUT, exist_ok=True)
MODEL = META["model"]
NAVY, GREEN, TEAL, LIGHT = "003142", "93AC3E", "0097B2", "EEF5F7"

# ---------------- checklist XLSX ----------------
BASIS = {"zh": {"M": "说明书", "P": "产品资料", "G": "推测", "M+G": "说明书｜阈值推测", "P+G": "产品资料｜公差推测", "M+P": "说明书+产品资料"},
         "en": {"M": "Manual", "P": "Product doc", "G": "Assumed", "M+G": "Manual | threshold assumed", "P+G": "Product doc | tolerance assumed", "M+P": "Manual + product doc"}}

def checklist(lang):
    zh = lang == "zh"
    wb = Workbook(); ws = wb.active
    ws.title = "出厂验收" if zh else "FAT"
    thin = Side(style="thin", color="7F8C8D"); B = Border(left=thin, right=thin, top=thin, bottom=thin)
    hdr = ["编号", "检查项目", "验收标准 / 判定依据", "检查方法", "合格", "不合格", "NA", "实测值", "结论", "检验员", "日期", "依据标注"] if zh else \
          ["No.", "Check item", "Acceptance criterion / basis", "Method", "Pass", "Fail", "NA", "Measured value", "Conclusion", "Inspector", "Date", "Basis"]
    widths = [7, 18, 46, 26, 6, 7, 6, 14, 12, 10, 11, 16]
    ncol = len(hdr)
    title = META_FAT["title_zh"] if zh else META_FAT["title_en"]
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncol)
    c = ws.cell(1, 1, title); c.font = Font(bold=True, size=15, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal="center", vertical="center"); ws.row_dimensions[1].height = 30
    info = META_FAT["info_zh"] if zh else META_FAT["info_en"]
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncol)
    c = ws.cell(2, 1, "      ".join(x + " ________" for x in info)); c.font = Font(size=10); ws.row_dimensions[2].height = 22
    note = ("勾选：在「合格 / 不合格 / NA」列下拉选 ☑。「推测」= 资料未给出、按通用 SMT 设备出厂验收惯例拟定的阈值，正式下发前请技术部确认。依据：" + META_FAT["basis_doc_zh"] + "。"
            if zh else
            "Tick: choose ☑ from the drop-down under Pass / Fail / NA. 'Assumed' = threshold not given in the source documents, drafted from general SMT equipment FAT practice; confirm with engineering before release. Basis: " + META_FAT["basis_doc_en"] + ".")
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=ncol)
    c = ws.cell(3, 1, note); c.font = Font(size=9, italic=True, color="4A5A63"); c.alignment = Alignment(wrap_text=True, vertical="top"); ws.row_dimensions[3].height = 34
    r = 4
    for i, h in enumerate(hdr, 1):
        c = ws.cell(r, i, h); c.font = Font(bold=True, color="FFFFFF", size=10); c.fill = PatternFill("solid", fgColor=TEAL)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = B
    ws.row_dimensions[r].height = 24
    dv = DataValidation(type="list", formula1='"☐,☑"', allow_blank=True); ws.add_data_validation(dv)
    dvc = DataValidation(type="list", formula1='"合格,不合格,NA"' if zh else '"Pass,Fail,NA"', allow_blank=True); ws.add_data_validation(dvc)
    n = 0
    for sec, szh, sen in SECTIONS:
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncol)
        c = ws.cell(r, 1, f"{sec}  {szh if zh else sen}"); c.font = Font(bold=True, color=NAVY, size=11)
        c.fill = PatternFill("solid", fgColor=LIGHT)
        for k in range(1, ncol + 1): ws.cell(r, k).border = B
        for it in [x for x in ITEMS if x[0] == sec]:
            n += 1; r += 1
            _, izh, ien, stzh, sten, mzh, men, basis = it
            std = stzh if zh else sten
            if "G" in basis: std = ("【推测】" if zh else "[Assumed] ") + std
            row = [f"{n:02d}", izh if zh else ien, std, mzh if zh else men, "☐", "☐", "☐", "", "", "", "", BASIS[lang][basis]]
            for k, v in enumerate(row, 1):
                c = ws.cell(r, k, v); c.border = B; c.font = Font(size=10, color=("B03A2E" if k == 12 and "G" in basis else "222222"))
                c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if k in (1, 5, 6, 7) else "left")
            for k in (5, 6, 7): ws.cell(r, k).font = Font(size=14); dv.add(ws.cell(r, k))
            dvc.add(ws.cell(r, 9))
            ws.row_dimensions[r].height = max(30, 15 * (len(std) // (24 if zh else 44) + 1))
    r += 2
    sign = (["总判定：☐ 合格放行   ☐ 不合格返工", "检验员签字：__________  日期：________", "质量主管签字：__________  日期：________"] if zh else
            ["Overall: ☐ Pass – release   ☐ Fail – rework", "Inspector: __________  Date: ________", "QA supervisor: __________  Date: ________"])
    for s in sign:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncol)
        ws.cell(r, 1, s).font = Font(bold=True, size=11); ws.row_dimensions[r].height = 24; r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncol)
    ws.cell(r, 1, "Shenzhen Southern Machinery Sales and Service Co., Ltd · smthelp.com · info@smthelp.com · WhatsApp +86 136 0256 2576").font = Font(size=9, color="4A5A63")
    for i, w in enumerate(widths, 1): ws.column_dimensions[chr(64 + i)].width = w
    ws.freeze_panes = "C5"
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"; ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = ws.page_margins.right = 0.3; ws.page_margins.top = ws.page_margins.bottom = 0.5
    ws.oddFooter.center.text = ("第 &P 页 / 共 &N 页" if zh else "Page &P of &N")
    fn = os.path.join(OUT, f"{MODEL}_出厂验收检查表_中文.xlsx" if zh else f"{MODEL}_Factory_Acceptance_Checklist_EN.xlsx")
    wb.save(fn); return fn, n

# ---------------- SRT ----------------
def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def split_lines(text, zh):
    parts = re.split(r"(?<=[。，；！？])" if zh else r"(?<=[.,:;!?])\s+", text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    lim = 16 if zh else 42
    out, cur = [], ""
    for p in parts:
        if cur and len(cur) + len(p) > lim: out.append(cur); cur = p
        else: cur = (cur + ("" if zh else " ") + p).strip()
    if cur: out.append(cur)
    return out

def srt_cues(v, zh):
    cues, t = [], 0.0
    for sh in v["shots"]:
        d = sh[0]; vo = sh[7] if zh else sh[8]
        lines = split_lines(vo, zh); total = sum(len(x) for x in lines) or 1
        st = t + 0.1; span = d - 0.3
        for ln in lines:
            dd = span * len(ln) / total
            cues.append((st, st + dd, ln)); st += dd
        t += d
    return cues

def write_srt(v, zh):
    fn = os.path.join(OUT, "srt", f"{v['id']}_{'ZH' if zh else 'EN'}.srt"); os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, "w", encoding="utf-8") as f:
        for i, (a, b, ln) in enumerate(srt_cues(v, zh), 1): f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{ln}\n\n")
    return fn

# ---------------- DOCX copy pack ----------------
def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr(); s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hexc); tcPr.append(s)

def para(doc, text, bold=False, size=10, color=None, italic=False):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    if color: r.font.color.rgb = RGBColor.from_string(color)
    p.paragraph_format.space_after = Pt(3); return p

def table(doc, hdr, rows, widths=None, fs=8.5):
    t = doc.add_table(rows=1, cols=len(hdr)); t.style = "Table Grid"
    for i, h in enumerate(hdr):
        c = t.rows[0].cells[i]; c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(fs); r.font.color.rgb = RGBColor(255, 255, 255); shade(c, NAVY)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""; r = cells[i].paragraphs[0].add_run(str(v)); r.font.size = Pt(fs)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths): row.cells[i].width = Cm(w)
    doc.add_paragraph(); return t

def mmss(t): return f"{int(t)//60}:{int(t)%60:02d}"

def docx_pack():
    doc = Document()
    st = doc.styles["Normal"]; st.font.name = "Noto Sans SC"; st.element.rPr.rFonts.set(qn("w:eastAsia"), "Noto Sans SC"); st.font.size = Pt(10)
    sec = doc.sections[0]; sec.orientation = WD_ORIENT.LANDSCAPE; sec.page_width, sec.page_height = sec.page_height, sec.page_width
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(sec, m, Cm(1.5))
    para(doc, META["title_en"], True, 20, NAVY)
    para(doc, f"短视频文案包 · Short-Video Copy Pack（{len(V)} 个主题 · YouTube Shorts / LinkedIn / TikTok）", True, 13, TEAL)
    para(doc, f"Southern Machinery · 草稿 {META['draft']} · {META['date']} · 发布前须 Jason 审核", False, 9, "4A5A63", True)

    doc.add_heading("0. 资料来源与可访问性 / Sources and access", level=2)
    table(doc, ["资料 / Source", "状态 / Status", "用途 / Used for"], META["sources"], [8, 6, 12])
    if META.get("conflict_note"): para(doc, META["conflict_note"], False, 9, "B03A2E")

    doc.add_heading("1. 用到的仓库 skill / Repo skills applied", level=2)
    para(doc, META["skills_applied"], size=9.5)

    doc.add_heading("2. 平台调性建议 / Platform tone", level=2)
    table(doc, ["平台", "调性 / Tone", "格式", "标题 / 文案要点"], [
        ["YouTube Shorts", "工程师口吻、参数前置、可搜索 / Engineer voice, spec-first, searchable", "9:16，≤60 s，烧录字幕 + 上传 SRT", "标题 ≤70 字符含核心关键词 + #Shorts；描述前两行放关键词；附非隶属声明"],
        ["LinkedIn", "专业、问题先行、方法论 / Problem-first, method, professional", "9:16 或裁 4:5；静音自动播放 → 必须烧录字幕", "正文 3 段：痛点 → 方法 → 产品；结尾一个问题引导评论；3–5 个标签"],
        ["TikTok / Reels", "快节奏、口语、一个看点 / Fast, casual, one payoff", "9:16，15–30 s 最佳，前 1 s 出画面动作", "标题一句话 + 1 个 emoji；标签 5–7 个，混合大词与长尾词"],
    ], [3.5, 7, 6, 9.5])
    para(doc, "统一结尾联系方式（片尾 + 描述）：" + CTA_EN + "  ｜  " + CTA_ZH, size=9)
    para(doc, "非隶属声明（YouTube / LinkedIn 描述末尾）：" + DISCLAIM_EN + "  ｜  " + DISCLAIM_ZH, size=9)

    doc.add_heading("3. 10 个主题总览 / Overview", level=2)
    cover = META["coverage"]
    table(doc, ["#", "主题 / Theme", "时长", "覆盖要求项", "类型"], [[v["id"], v["zh"] + "\n" + v["en"], f"{v['dur']} s", cover[v["id"]], v["type_zh"] + " / " + v["type_en"]] for v in V], [1.3, 11, 1.5, 6, 6])

    for v in V:
        doc.add_page_break()
        p = PLAT[v["id"]]
        para(doc, f"{v['id']} · {v['zh']}", True, 15, NAVY)
        para(doc, v["en"], True, 11.5, TEAL)
        para(doc, f"时长 Duration：{v['dur']} s ｜ 画幅 9:16 ｜ 类型：{v['type_zh']} / {v['type_en']}", size=9.5)
        para(doc, f"目标观众：{v['aud_zh']} ｜ Audience: {v['aud_en']}", size=9.5)
        para(doc, f"开场画面：{v['hook_zh']}", size=9.5); para(doc, f"Opening shot: {v['hook_en']}", size=9.5)
        if v.get("note_zh"):
            para(doc, "⚠ " + v["note_zh"], size=9, color="B03A2E"); para(doc, "⚠ " + v["note_en"], size=9, color="B03A2E")

        doc.add_heading("A. 分镜脚本 / Storyboard", level=3)
        rows, t = [], 0
        for i, s in enumerate(v["shots"], 1):
            d, szz, sze, vz, ve, oz, oe, voz, voe, src = s
            rows.append([f"{i:02d}", f"{mmss(t)}–{mmss(t+d)}\n{d}s", f"{szz}\n{sze}", vz + "\n" + ve, oz + "\n" + oe, voz + "\n" + voe, src]); t += d
        table(doc, ["镜号\nShot", "时间/时长\nTime", "景别\nSize", "画面内容 / Visual", "字幕提示（上屏）/ On-screen text", "口播要点 / VO", "素材来源 / Source"], rows, [1.2, 1.8, 1.4, 6, 5, 6.3, 3])

        doc.add_heading("B. 口播稿 / Voice-over", level=3)
        para(doc, "English：" + " ".join(s[8] for s in v["shots"]), size=9.5)
        para(doc, "中文：" + "".join(s[7] for s in v["shots"]), size=9.5)

        doc.add_heading("C. 字幕（时间轴）/ Subtitles (timeline)", level=3)
        ce, cz = srt_cues(v, False), srt_cues(v, True)
        rows = [[f"{ts(a)[3:]} → {ts(b)[3:]}", ln] for a, b, ln in ce]
        rowsz = [[f"{ts(a)[3:]} → {ts(b)[3:]}", ln] for a, b, ln in cz]
        n = max(len(rows), len(rowsz)); rows += [["", ""]] * (n - len(rows)); rowsz += [["", ""]] * (n - len(rowsz))
        table(doc, ["EN 时间", "EN 字幕", "ZH 时间", "ZH 字幕"], [a + b for a, b in zip(rows, rowsz)], [3.4, 9.4, 3.4, 9.4], 8)
        para(doc, f"另附 SRT 文件：{v['id']}_EN.srt / {v['id']}_ZH.srt", size=8.5, color="4A5A63", italic=True)

        doc.add_heading("D. 标题与标签 / Titles & tags", level=3)
        tags = " ".join(p["tags"])
        table(doc, ["平台 Platform", "标题 / 文案 (EN)", "中文对照", "标签 / Hashtags"], [
            ["YouTube Shorts", p["yt"] + "\n\n" + p["desc"] + "\n\n" + CTA_EN + "\n" + DISCLAIM_EN, p["yt_zh"], tags + " #Shorts"],
            ["LinkedIn", p["li"] + "\n\n" + CTA_EN, p["li_zh"] + "\n\n" + CTA_ZH, " ".join(p["tags"][:5])],
            ["TikTok / Reels", p["tt"], "（同 YouTube 标题意思，口语化）", tags + " #fyp"],
        ], [2.6, 10, 8, 5])
        para(doc, "SEO 关键词：" + " · ".join(p["seo"]), size=9)

    doc.add_page_break()
    doc.add_heading("4. 待拍素材清单 / Shots to film", level=2)
    need = []
    for v in V:
        for i, s in enumerate(v["shots"], 1):
            if "NEW" in s[9]: need.append([f"{v['id']}-{i:02d}", s[3], s[2], s[9]])
    table(doc, ["镜号", "画面", "景别", "备注"], need, [2.5, 13, 2, 7])
    para(doc, META["existing_media"], size=9)

    doc.add_heading("5. 发布前待确认 / To confirm before publishing", level=2)
    for s in META["to_confirm"]:
        para(doc, "• " + s, size=9.5)
    fn = os.path.join(OUT, f"{MODEL}_短视频文案包_{len(V)}主题_CN-EN.docx"); doc.save(fn); return fn

if __name__ == "__main__":
    a, n1 = checklist("zh"); b, n2 = checklist("en"); print(a, n1, b, n2)
    for v in V: write_srt(v, False); write_srt(v, True)
    print(docx_pack())
    z = os.path.join(OUT, f"{MODEL}_SRT_字幕.zip")
    with zipfile.ZipFile(z, "w") as zf:
        for f in sorted(os.listdir(os.path.join(OUT, "srt"))): zf.write(os.path.join(OUT, "srt", f), f)
    print(z)
