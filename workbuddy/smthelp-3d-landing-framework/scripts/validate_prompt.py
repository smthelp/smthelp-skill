#!/usr/bin/env python3
"""
smthelp-3d-landing-framework / validate_prompt.py

对生成出来的落地页 Prompt 做合规自检。检查项直接对应品牌声纹的硬约束。

用法
    python3 validate_prompt.py --file generated.md
    cat generated.md | python3 validate_prompt.py
    python3 validate_prompt.py --file generated.md --strict   # WARN 也当失败

检查项
    E1 残留未替换占位符 [XXX]
    E2 强制 CTA 两行缺失或被改写
    E3 出现最终价格（USD 数字）
    E4 禁用空洞形容词（中英）
    W1 未出现 "On request" —— 所有参数都填了数字，需核对是否全部来自已确认锚点
    W2 CPH 与 UPH 同时出现 —— 需确认没有混用
    W3 缺少 WhatsApp / info@smthelp.com 联系入口
    W4 数值型卖点过少（无法判断是否"用数字说话"）
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CTA_LINE_1 = "Note: This configuration is a draft and must be finalized and reviewed by our senior Sales Engineer (Jason Wu)."
CTA_LINE_2 = "Action Required: Please provide your Gerber file or PCB drawings to info@smthelp.com for an accurate capacity simulation and nozzle engineering validation."

BANNED_EN = [
    "efficient", "intelligent", "excellent", "leading", "world-class", "world class",
    "perfect", "revolutionary", "game-changing", "game changing", "cutting-edge",
    "cutting edge", "state-of-the-art", "best-in-class", "unrivalled", "unmatched",
]
BANNED_CN = [
    "高效", "智能", "卓越", "领先", "一流", "完美", "革命性", "颠覆", "赋能",
    "在当今时代", "随着", "值得注意的是", "综上所述", "最好", "顶级", "唯一", "根治", "永不",
]

PRICE_RE = re.compile(r"(?:USD|US\$|\$)\s?\d{2,3}(?:,\d{3})+|\$\s?\d{4,}")
PLACEHOLDER_RE = re.compile(r"\[([A-Z0-9_]{2,})\]")
NUMERIC_CLAIM_RE = re.compile(r"\d[\d.,]*\s?(?:mm|kg|C\b|CPH|UPH|PPM|s\b|min|h\b|N\b|V\b|MPa|%)")
# 模板里会把禁用词列成负面清单，自检时必须先把那一行挖掉，否则永远误报
BANNED_LIST_RE = re.compile(r"^Banned filler words:.*$", re.M)
YAML_BLOCK_RE = re.compile(r"^```yaml\n(.*?)^```", re.M | re.S)
PREAMBLE_END = "---"


def parse_meta(text: str) -> dict:
    m = YAML_BLOCK_RE.search(text)
    if not m:
        return {}
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def check(text: str, strict: bool = False) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    meta = parse_meta(text)

    # E1 残留占位符
    leftover = sorted(set(PLACEHOLDER_RE.findall(text)))
    if leftover:
        errors.append(f"E1 残留未替换占位符：{', '.join(leftover)}")

    # E2 强制 CTA
    if CTA_LINE_1 not in text:
        errors.append("E2 强制 CTA 第 1 行缺失或被改写（必须是原文，逐字一致）")
    if CTA_LINE_2 not in text:
        errors.append("E2 强制 CTA 第 2 行缺失或被改写（必须是原文，逐字一致）")

    # E3 最终价格
    hits = PRICE_RE.findall(text)
    if hits:
        errors.append(f"E3 出现最终价格，违反报价熔断：{', '.join(sorted(set(hits))[:5])}")

    # E4 禁用词
    #   1) 先挖掉模板自身的负面清单行（否则永远误报）
    #   2) 用 (?<![-\w]) / (?![-\w]) 排除 CSS 工具类，如 leading-none / tracking-wide
    probe = BANNED_LIST_RE.sub("", text)
    low = probe.lower()
    bad_en = [
        w for w in BANNED_EN
        if re.search(r"(?<![-\w])" + re.escape(w) + r"(?![-\w])", low)
    ]
    bad_cn = [w for w in BANNED_CN if w in probe]
    if bad_en:
        errors.append(f"E4 英文禁用空洞形容词：{', '.join(bad_en)}")
    if bad_cn:
        errors.append(f"E4 中文禁用词：{', '.join(bad_cn)}")

    # E5 强制配套
    if meta.get("pairing_required") == "true":
        pairing_line = [l for l in text.splitlines() if "Recommended pairing:" in l]
        if not pairing_line:
            errors.append("E5 该机型有强制配套，但输出里没有 'Recommended pairing' 行（PAIRING 字段为空？）")

    # W1 参数溯源（基于机型元数据，而不是正文里搜 On request）
    if "spec_rows_withheld" in meta:
        n = int(meta["spec_rows_withheld"])
        if n == 0:
            warnings.append("W1 七行参数全部填了数字 —— 请逐条核对是否都来自已确认参数锚点")
        else:
            print(f"ℹ️  参数墙有 {n} 行写 On request（符合溯源要求）")

    # W2 CPH / UPH —— 只看参数墙区块，不看模板里的说明文字
    m = re.search(r"^Spec rows:\n(.*?)^Never invent a number", text, re.M | re.S)
    spec_block = m.group(1) if m else ""
    if re.search(r"\bCPH\b", spec_block) and re.search(r"\bUPH\b", spec_block):
        warnings.append("W2 参数墙里 CPH 与 UPH 同时出现 —— 确认没有混用（CPH 按点数，UPH 按板数）")

    # W3 联系入口
    if "WhatsApp +86 13602562576" not in text:
        warnings.append("W3 缺少 WhatsApp 联系入口（+86 13602562576）")
    if "info@smthelp.com" not in text:
        warnings.append("W3 缺少 info@smthelp.com")

    # W4 数字卖点密度
    nums = NUMERIC_CLAIM_RE.findall(text)
    if len(nums) < 6:
        warnings.append(f"W4 带单位的数字只有 {len(nums)} 处 —— B2B 页面应靠数字说话，建议 >= 6 处")

    print("=" * 62)
    if errors:
        print("❌ ERRORS（必须修）")
        for e in errors:
            print(f"   {e}")
    else:
        print("✅ 无 ERROR")

    if warnings:
        print("\n⚠️  WARNINGS（人工确认）")
        for w in warnings:
            print(f"   {w}")
    else:
        print("✅ 无 WARNING")
    print("=" * 62)

    if errors:
        return 1
    if strict and warnings:
        return 1
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="校验生成的落地页 Prompt 是否合规")
    ap.add_argument("--file", help="待校验文件路径；省略则从 stdin 读取")
    ap.add_argument("--strict", action="store_true", help="WARNING 也算失败")
    args = ap.parse_args()

    if args.file:
        text = Path(args.file).expanduser().read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    sys.exit(check(text, strict=args.strict))


if __name__ == "__main__":
    main()
