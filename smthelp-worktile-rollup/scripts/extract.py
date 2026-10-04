#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract CRM-relevant rows from all 2026-05-21 export files into one JSON dataset."""
import os, glob, json, re, sys, warnings
from openpyxl import load_workbook

warnings.filterwarnings("ignore")
# usage: python extract.py <BASE_DIR> <OUT_DIR> [BATCH_TAG]
#   BATCH_TAG default 20260521094104 (最新一批 Worktile 导出)
BASE = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, ".workbuddy/tmp")
TAG = sys.argv[3] if len(sys.argv) > 3 else "20260521094104"
os.makedirs(OUT, exist_ok=True)
files = sorted(glob.glob(os.path.join(BASE, f"*{TAG}.xlsx")))

COLS = {
    0: "title", 1: "no", 2: "task_type", 3: "status", 4: "creator",
    5: "created_on", 6: "updated_on", 7: "desc", 8: "owner", 9: "due",
    10: "priority", 12: "follower", 13: "start_time",
    54: "contract_amt", 55: "cust_no", 58: "paid_amt", 64: "proj_amt",
    65: "customer", 67: "company", 71: "contact", 72: "tel", 73: "main_products",
    74: "industry", 76: "cust_cat", 78: "current_state", 79: "automation_level",
    90: "expect_sign_date", 91: "sales_owner", 115: "contract_no", 124: "payment_terms",
    125: "customer_name_a", 126: "customer_name_b", 128: "cust_grade", 129: "cust_type",
    137: "acct_manager", 149: "lost_reason", 174: "mobile", 175: "email",
    176: "job_title", 179: "region", 180: "deal_amt", 186: "website",
    187: "company_name2", 192: "tel2", 194: "source", 196: "company_size",
    207: "main_products_brand", 212: "company_header",
}

IMG_RE = re.compile(r"!\[image\.[a-zA-Z]+\]\([^)]*\)")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")

def clean(v):
    if v is None:
        return ""
    if not isinstance(v, str):
        return str(v)
    v = IMG_RE.sub(" ", v)
    v = LINK_RE.sub(r"\1", v)
    v = v.replace("\u00a0", " ")
    v = re.sub(r"[ \t]+", " ", v)
    return v.strip()

records = []
for fp in files:
    fname = os.path.basename(fp)
    proj = re.sub(r"^Worktile-Project-", "", fname)
    proj = re.sub(r"-" + TAG + r"\.xlsx$", "", proj)
    try:
        wb = load_workbook(fp, read_only=True, data_only=True)
        ws = wb[wb.sheetnames[0]]
        for ri, row in enumerate(ws.iter_rows(values_only=True)):
            if ri == 0:
                continue
            if row is None:
                continue
            rec = {"_project": proj, "_file": fname, "_row": ri + 1}
            empty = True
            for idx, key in COLS.items():
                val = row[idx] if idx < len(row) else None
                if key == "desc":
                    val = clean(val)[:3000]
                else:
                    val = clean(val)[:300]
                rec[key] = val
                if val and key != "desc":
                    empty = False
            if empty:
                continue
            records.append(rec)
        wb.close()
    except Exception as e:
        print("ERR", fname, e)

with open(os.path.join(OUT, "dataset.json"), "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False)
print("records:", len(records))
