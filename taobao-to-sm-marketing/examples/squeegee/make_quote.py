# SM printer squeegee price list (Jason 2026-11-19): USD = round(Taobao CNY x 2 / 6.6); CNY = supplier shop card price (lowest variant).
import sys, os, datetime
D = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(D); sys.path.insert(0, K)
from models import ROWS, GROUPS, DEK_SQA, usd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as XImg

QNO = "SM-Q-SQ-" + datetime.date.today().strftime("%Y%m%d"); DATE = datetime.date.today().isoformat()
GREEN, TEAL, DARK = "90C641", "0AA5A5", "003141"
TITLE = "SMT Printer Squeegees, Blades & Storage - all major printer brands"
TERMS = [
 "Prices are starting prices (shortest standard length / basic version). The final price depends on length (150-750 mm), blade thickness and end-dam type - please send printer brand, model and squeegee length.",
 "Squeegee assembly = aluminium holder + blade, fixing screws included. Can be ordered as a full pair (2 holders + 2 blades); MOQ 2 pieces.",
 "Stainless blade thickness 0.3 mm standard; 0.2 / 0.25 / 0.4 / 0.5 mm and 0.15 mm step-stencil blades on request.",
 "End dams: fixed rubber, fixed stainless or elastic (movable) rubber.",
 "DEK SQA part numbers: SQA300 170 mm, SQA301 200, SQA302 250, SQA303 300, SQA304 350, SQA305 400, SQA306 440, SQA307 483, SQA308 510, SQA309 535, SQA489 580, SQA478 610 mm.",
 "Price basis: EXW Shenzhen, packing included; freight quoted on request.",
 "Payment terms, lead time and validity: [to be confirmed by Southern Machinery].",
]
def items():
    out = []
    for g,brand,model,prod,conf,cny,_ in ROWS: out.append(dict(g=g,brand=brand,model=model,prod=prod,conf=conf,cny=cny,usd=usd(cny)))
    return out

def xlsx(path):
    it = items(); wb = Workbook(); ws = wb.active; ws.title = "Price list"
    thin = Side(style="thin", color="BBBBBB"); B = Border(left=thin,right=thin,top=thin,bottom=thin)
    for i,w in enumerate([6,20,30,34,46,14,8,14]): ws.column_dimensions[chr(65+i)].width = w
    ws.row_dimensions[1].height = 48; ws.add_image(XImg(os.path.join(K,"sm-logo.png")), "A1")
    ws.merge_cells("D1:H1"); ws["D1"] = "PRICE LIST / QUOTATION"; ws["D1"].font = Font(bold=True,size=20,color=DARK); ws["D1"].alignment = Alignment(horizontal="right",vertical="center")
    r = 3
    for k,v in [("Product",TITLE),("Quotation No.",QNO),("Date",DATE),("To","[Customer name / company]"),("Currency","USD, starting unit price"),("From","Southern Machinery | info@smthelp.com | WhatsApp +86 136 0256 2576 | www.smthelp.com")]:
        ws.cell(r,2,k).font = Font(bold=True,color=DARK); ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=8); ws.cell(r,3,v); r += 1
    r += 1
    hdr = ["No.","Printer brand","Model / fits","Product","Configuration","From (USD)","Qty","Amount (USD)"]
    first = None; n = 1
    for g in "ABC":
        ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=8)
        c = ws.cell(r,1,f"{g}. {GROUPS[g]}"); c.font = Font(bold=True,color="FFFFFF",size=12); c.fill = PatternFill("solid",fgColor=GREEN); r += 1
        for i,h in enumerate(hdr,1):
            c = ws.cell(r,i,h); c.font = Font(bold=True,color="FFFFFF"); c.fill = PatternFill("solid",fgColor=TEAL); c.alignment = Alignment(horizontal="center",vertical="center",wrap_text=True); c.border = B
        r += 1
        for x in [x for x in it if x['g']==g]:
            first = first or r
            for i,v in enumerate([n,x['brand'],x['model'],x['prod'],x['conf'],x['usd'],0,f"=F{r}*G{r}"],1):
                c = ws.cell(r,i,v); c.border = B; c.alignment = Alignment(vertical="center",wrap_text=True,horizontal="center" if i in (1,6,7,8) else "left")
                if i in (6,8): c.number_format = '"$"#,##0'
            ws.cell(r,7).fill = PatternFill("solid",fgColor="FFF8DC"); r += 1; n += 1
    last = r-1
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=7)
    c = ws.cell(r,1,"TOTAL (USD) - enter quantities in the yellow Qty column"); c.font = Font(bold=True); c.alignment = Alignment(horizontal="right")
    t = ws.cell(r,8,f"=SUM(H{first}:H{last})"); t.font = Font(bold=True,color=DARK); t.number_format = '"$"#,##0'; t.border = B
    r += 2; ws.cell(r,1,"Notes").font = Font(bold=True,color=DARK,size=12); r += 1
    for i,tx in enumerate(TERMS,1):
        ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=8)
        c = ws.cell(r,1,f"{i}. {tx}"); c.alignment = Alignment(wrap_text=True,vertical="top"); ws.row_dimensions[r].height = 30; r += 1
    ws.page_setup.orientation = "landscape"; ws.sheet_properties.pageSetUpPr.fitToPage = True; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    wb.save(path); return it

def pdf(path, it):
    from weasyprint import HTML
    th = "<tr><th>No.</th><th>Printer brand</th><th>Model / fits</th><th>Product</th><th>Configuration</th><th>From (USD)</th></tr>"
    body = ""; n = 1
    for g in "ABC":
        rows = ""
        for x in [x for x in it if x['g']==g]:
            rows += f"<tr><td>{n}</td><td><b>{x['brand']}</b></td><td>{x['model']}</td><td>{x['prod']}</td><td>{x['conf']}</td><td class=p>${x['usd']:,}</td></tr>"; n += 1
        body += f"<h2>{g}. {GROUPS[g]}</h2><table class=q>{th}{rows}</table>"
    html = f"""<html><head><style>
@page{{size:A4 landscape;margin:12mm 12mm 14mm;@bottom-center{{content:"Southern Machinery  |  www.smthelp.com  |  info@smthelp.com  |  WhatsApp +86 136 0256 2576   -   page " counter(page);font:8pt DejaVu Sans;color:#0AA5A5}}}}
body{{font-family:'DejaVu Sans';font-size:8.6pt;color:#222}}
.top{{display:flex;justify-content:space-between;align-items:center;border-bottom:4px solid #90C641;padding-bottom:6px}}
h1{{color:#003141;font-size:22pt;margin:0}} .meta td{{padding:1px 8px 1px 0}} .meta b{{color:#003141}}
table.q{{width:100%;border-collapse:collapse;margin-top:4px}} .q th{{background:#0AA5A5;color:#fff;padding:5px;font-size:8.4pt}}
.q td{{border:1px solid #ccc;padding:3.5px 5px}} .q tr:nth-child(even) td{{background:#f4f9ec}} td.p{{text-align:right;font-weight:bold;color:#003141;white-space:nowrap}}
h2{{background:#90C641;color:#fff;font-size:10.5pt;padding:4px 8px;margin:10px 0 0;page-break-after:avoid}}
.hero{{display:flex;gap:10px;align-items:center;margin:8px 0}} .hero img{{height:105px;border:1px solid #ddd}}
ol{{margin:4px 0 0 16px;padding:0}} li{{margin-bottom:3px}}
</style></head><body>
<div class=top><img src="file://{K}/sm-logo.png" style="height:44px"><h1>PRICE LIST / QUOTATION</h1></div>
<div class=hero><img src="file://{K}/assets/01-holder.jpg"><img src="file://{K}/assets/02-pair.jpg">
<table class=meta><tr><td><b>Product</b></td><td>{TITLE}</td></tr><tr><td><b>Quotation No.</b></td><td>{QNO}</td></tr><tr><td><b>Date</b></td><td>{DATE}</td></tr>
<tr><td><b>To</b></td><td>[Customer name / company]</td></tr><tr><td><b>Currency</b></td><td>USD, starting unit price (see note 1)</td></tr></table></div>
{body}<h2>Notes</h2><ol>{''.join(f'<li>{t}</li>' for t in TERMS)}</ol></body></html>"""
    HTML(string=html).write_pdf(path)

if __name__ == "__main__":
    o = os.path.join(K,"out","quote"); os.makedirs(o,exist_ok=True)
    base = os.path.join(o,"Southern-Machinery-Price-List-SMT-Printer-Squeegee-Blades-USD")
    it = xlsx(base+".xlsx"); pdf(base+".pdf", it)
    for x in it: print(x['g'], x['model'], x['prod'], x['cny'], x['usd'])
