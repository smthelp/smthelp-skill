#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Foxmail RECF 正文文件中提取全部邮件（From/Date/To/Subject + 正文首段）。
输出 JSONL 到 .workbuddy-ai/work/messages.jsonl
"""
import json
import re
import sys
import time
from pathlib import Path

if len(sys.argv) < 3:
    sys.exit("用法: extract_messages.py <Foxmail数据目录> <输出目录>")
BASE = Path(sys.argv[1]).expanduser().resolve()
WORK = Path(sys.argv[2]).expanduser().resolve()
WORK.mkdir(parents=True, exist_ok=True)
OUT = WORK / "messages.jsonl"

CHUNK = 16 * 1024 * 1024

UNIT = rb"(?:[\x09\x0a\x0d\x20-\x7e]\x00|[\x00-\xff][\x4e-\x9f]|[\x00-\xff][\x30-\x33])"
RUN = re.compile(UNIT + rb"{12,}")

HDR = re.compile(
    r"(?:^|[\r\n])[ \t]*(?:From|发件人)[ \t]*:[ \t]*(?P<frm>[^\r\n]{1,180})[\r\n]+"
    r"[ \t]*(?:Date|日期|时间)[ \t]*:[ \t]*(?P<date>[^\r\n]{1,90})[\r\n]+"
    r"[ \t]*(?:To|收件人)[ \t]*:[ \t]*(?P<to>[^\r\n]{1,400})[\r\n]+"
    r"[ \t]*(?:Subject|主题)[ \t]*:[ \t]*(?P<subj>[^\r\n]{0,400})",
    re.M,
)

EMAIL_RE = re.compile(r"[\w.\-+]+@[\w\-]+(?:\.[\w\-]+)+")

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def parse_date(s: str) -> str:
    """返回 YYYY-MM-DD，失败返回 ''。"""
    s = s.strip()
    m = re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1990 <= y <= 2030 and 1 <= mo <= 12 and 1 <= d <= 31:
            return f"{y:04d}-{mo:02d}-{d:02d}"
    m = re.search(r"(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})", s)
    if m:
        mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y < 100:
            y += 2000 if y < 70 else 1900
        if 1990 <= y <= 2030 and 1 <= mo <= 12 and 1 <= d <= 31:
            return f"{y:04d}-{mo:02d}-{d:02d}"
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})", s)
    if m:
        mo = MONTHS.get(m.group(2).lower())
        if mo:
            return f"{int(m.group(3)):04d}-{mo:02d}-{int(m.group(1)):02d}"
    return ""


def extract_text(path: Path) -> str:
    parts = []
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(CHUNK)
            if not chunk:
                break
            for m in RUN.finditer(chunk):
                parts.append(m.group().decode("utf-16-le", errors="replace"))
    return "".join(parts)


def main():
    targets = []
    # 自动发现 Storage/ 下的所有账号目录
    st = BASE / "Storage"
    accounts = sorted(d.name for d in st.iterdir() if d.is_dir()) if st.is_dir() else []
    print(f"发现 {len(accounts)} 个账号: {accounts}", flush=True)
    for acc in accounts:
        for sub in ["msgBody", "msgExt"]:
            d = BASE / "Storage" / acc / "Indexes" / sub
            if not d.is_dir():
                continue
            subs = [x for x in d.iterdir() if x.is_dir()]
            subs.sort(key=lambda x: (not x.name.isdigit(), int(x.name) if x.name.isdigit() else 0))
            for sub2 in [d] + subs:
                f = sub2 / ("bodytxt_txt.rec0" if sub == "msgBody" else "exttxt_txt.rec0")
                if f.is_file():
                    targets.append((acc, f))

    print(f"待处理 {len(targets)} 个文件", flush=True)
    total_msgs = 0
    seen = set()

    with OUT.open("w", encoding="utf-8") as out:
        for i, (acc, f) in enumerate(targets, 1):
            t0 = time.time()
            size = f.stat().st_size
            try:
                txt = extract_text(f)
            except Exception as e:
                print(f"  [{i}/{len(targets)}] 失败 {f}: {e}", flush=True)
                continue

            n = 0
            hits = list(HDR.finditer(txt))
            for j, m in enumerate(hits):
                end = hits[j + 1].start() if j + 1 < len(hits) else len(txt)
                body = txt[m.end():min(end, m.end() + 4000)]
                rec = {
                    "acc": acc,
                    "frm": m.group("frm").strip(),
                    "to": m.group("to").strip(),
                    "date": m.group("date").strip(),
                    "iso": parse_date(m.group("date")),
                    "subj": m.group("subj").strip(),
                    "body": body[:2500],
                }
                key = (rec["frm"], rec["to"], rec["date"], rec["subj"][:120])
                if key in seen:
                    continue
                seen.add(key)
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
            total_msgs += n
            print(f"  [{i}/{len(targets)}] {acc} {f.parent.name}/{f.name} "
                  f"{size/1e6:.0f}MB -> {len(hits)} 头 / 新增 {n}  (累计 {total_msgs}) "
                  f"{time.time()-t0:.1f}s", flush=True)

    print(f"\n完成：{total_msgs} 条唯一邮件 -> {OUT}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
