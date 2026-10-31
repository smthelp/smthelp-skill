#!/usr/bin/env python3
"""Quality gate for a kit before build/delivery. Exit 1 on any ERROR.

usage: python3 qa_copy.py <kit_dir>
Checks
  structure  every video has id/zh/en/dur/shots; shot tuples have 10 fields; durations add up to dur;
             dur in {15, 30, 45, 60}; first shot <= 3 s; last shot is the SM outro (contains smthelp.com)
  pairing    every ZH field has its EN twin and vice versa (no empty side)
  platform   PLAT entry per video: yt <= 70 chars, tags 5-8, seo >= 3
  never-pub  price / lead time / stock / warranty / payment terms / discount / certificates /
             saving-yield-ROI % in VO, on-screen text and platform copy
  headings   banned words (hook, diagnosis, framework, vehicle, loop, CTA, 钩子 ...) in titles
  numbers    every number shown on screen must appear in META["facts"] (if provided) -> WARN otherwise
  checklist  numbering continuous; each item has ZH+EN; items with basis containing G carry 推测/Assumed via build
"""
import os, re, sys
kit = sys.argv[1]; sys.path.insert(0, os.path.abspath(kit))
from videos import META, V, PLAT
from checklist import SECTIONS, ITEMS
E_, W_ = [], []
NEVER = re.compile(r"\$\s?\d|\bUSD\b|\bRMB\b|price\s*[:=]?\s*\d|lead[ -]?time|in stock|warrant|payment terms|discount|"
                   r"certified|certificate|sav(?:e|es|ing|ings)\s+(?:up to\s+)?\d+\s?%|\bROI\b\s*\d|yield\s*\d+\s?%|"
                   r"价格|报价\s*\d|交期|现货|有库存|库存充足|质保|保修|付款方式|折扣|认证|节省\s*\d+\s?%|良率\s*\d", re.I)
BANNED = re.compile(r"\b(hook|diagnosis|framework|vehicle|loop|CTA)\b|钩子|诊断|框架|载体|循环|行动号召", re.I)
facts = [str(f) for f in META.get("facts", [])]
for v in V:
    vid = v.get("id", "?")
    for k in ("id", "zh", "en", "dur", "shots"):
        if k not in v: E_.append(f"{vid}: missing {k}")
    sh = v["shots"]
    if any(len(s) != 10 for s in sh): E_.append(f"{vid}: shot tuple must have 10 fields")
    tot = sum(s[0] for s in sh)
    if tot != v["dur"]: E_.append(f"{vid}: shots add to {tot}s, dur says {v['dur']}s")
    if v["dur"] not in (15, 30, 45, 60): W_.append(f"{vid}: duration {v['dur']}s outside 15/30/45/60")
    if sh[0][0] > 3: E_.append(f"{vid}: first shot {sh[0][0]}s > 3s (opening must show the machine moving)")
    if "smthelp.com" not in (sh[-1][5] + sh[-1][6]): E_.append(f"{vid}: last shot is not the SM outro")
    for i, s in enumerate(sh, 1):
        for a, b, n in ((1, 2, "size"), (3, 4, "visual"), (5, 6, "osd"), (7, 8, "vo")):
            if bool(str(s[a]).strip()) != bool(str(s[b]).strip()): E_.append(f"{vid}-{i:02d}: {n} ZH/EN not paired")
        for t in (s[5], s[6], s[7], s[8]):
            if NEVER.search(t): E_.append(f"{vid}-{i:02d}: never-publish term in '{t}'")
        if facts:
            for num in re.findall(r"\d+(?:\.\d+)?", s[6]):
                if not any(num in f for f in facts): W_.append(f"{vid}-{i:02d}: on-screen number {num} not in META['facts']")
    for t in (v["zh"], v["en"]):
        if BANNED.search(t): E_.append(f"{vid}: banned word in title '{t}'")
    p = PLAT.get(vid)
    if not p: E_.append(f"{vid}: no PLAT entry"); continue
    if len(p["yt"]) > 70: E_.append(f"{vid}: YouTube title {len(p['yt'])} > 70 chars")
    if not 5 <= len(p["tags"]) <= 8: W_.append(f"{vid}: {len(p['tags'])} tags (want 5-8)")
    if len(p["seo"]) < 3: W_.append(f"{vid}: fewer than 3 SEO keywords")
    for k in ("yt", "desc", "li", "li_zh", "tt", "yt_zh"):
        if NEVER.search(p.get(k, "")): E_.append(f"{vid}: never-publish term in PLAT.{k}")
        if k in ("yt", "yt_zh") and BANNED.search(p.get(k, "")): E_.append(f"{vid}: banned word in PLAT.{k}")
secs = [s[0] for s in SECTIONS]
for it in ITEMS:
    if it[0] not in secs: E_.append(f"checklist: unknown section {it[0]}")
    if not all(str(x).strip() for x in it[1:7]): E_.append(f"checklist: empty ZH/EN field in '{it[1]}'")
    if it[7] not in ("M", "P", "G", "M+G", "P+G", "M+P"): E_.append(f"checklist: bad basis {it[7]} in '{it[1]}'")
for e in E_: print("ERROR", e)
for w in W_: print("WARN ", w)
print(f"{len(V)} videos, {len(ITEMS)} checklist items -> {len(E_)} errors, {len(W_)} warnings")
sys.exit(1 if E_ else 0)
