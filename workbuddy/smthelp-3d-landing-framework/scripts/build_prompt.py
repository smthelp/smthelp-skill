#!/usr/bin/env python3
"""
smthelp-3d-landing-framework / build_prompt.py

把「主模板」+「机型数据」合成为一段可直接粘贴进 open-design / DSH / Cursor / v0 的英文 Prompt。

用法
    python3 build_prompt.py --list
    python3 build_prompt.py --model S-WS450
    python3 build_prompt.py --model S-WS450 --out ~/Desktop/S-WS450-prompt.md
    python3 build_prompt.py --all --out-dir ~/Desktop/sm-lp-prompts
    python3 build_prompt.py --model S-WS450 --validate     # 生成后自动跑合规自检

设计约定
- 模板与数据分离：新版式改 templates/，新机型只加 machines/*.json
- PAIRING 为空时，脚本自动删除整行 "Bottom grey note bar"
- 未填的必填字段直接报错退出，绝不静默留下 [占位符]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "templates" / "prompt-master-EN.md"
MACHINES = SKILL_DIR / "machines"
VALIDATOR = SKILL_DIR / "scripts" / "validate_prompt.py"

BEGIN = "<!-- BEGIN PROMPT -->"
END = "<!-- END PROMPT -->"

REQUIRED = [
    "MODEL", "PROCESS", "CATEGORY", "ONE_LINER", "NARRATIVE",
    "HOTSPOT_1", "HOTSPOT_2", "HOTSPOT_3",
    "CORNER_1", "CORNER_2", "CORNER_3", "CORNER_4",
    "SPEC_01", "SPEC_02", "SPEC_03", "SPEC_04", "SPEC_05", "SPEC_06", "SPEC_07",
    "HERO_MEDIA", "MARQUEE_MEDIA",
]
OPTIONAL = ["PAIRING"]

# PAIRING 为空时要整行删掉的句子（模板中的原句）
PAIRING_LINE_RE = re.compile(r'^Bottom grey note bar: "Recommended pairing: \[PAIRING\]"\s*$', re.M)

PLACEHOLDER_RE = re.compile(r"\[([A-Z0-9_]+)\]")


def load_template() -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        sys.exit(f"[ERROR] 模板缺少 {BEGIN} / {END} 标记：{TEMPLATE}")
    body = text.split(BEGIN, 1)[1].split(END, 1)[0]
    return body.strip() + "\n"


def list_machines() -> list[Path]:
    return sorted(MACHINES.glob("*.json"))


def load_machine(model: str) -> dict:
    path = MACHINES / f"{model}.json"
    if not path.exists():
        available = ", ".join(p.stem for p in list_machines())
        sys.exit(f"[ERROR] 找不到机型 {model}。可用机型：{available}")
    return json.loads(path.read_text(encoding="utf-8"))


def render(body: str, machine: dict) -> str:
    fields = machine.get("fields", {})

    # 1. 完整性检查
    missing = [k for k in REQUIRED if not str(fields.get(k, "")).strip()]
    if missing:
        sys.exit(f"[ERROR] {machine['model']} 缺少必填字段：{', '.join(missing)}")

    # 2. PAIRING 空值 → 删整行
    if not str(fields.get("PAIRING", "")).strip():
        body = PAIRING_LINE_RE.sub("", body)
        fields = dict(fields)
        fields["PAIRING"] = ""

    # 3. 替换
    out = body
    for key, value in fields.items():
        out = out.replace(f"[{key}]", str(value))

    # 4. 残留检查
    leftover = sorted(set(m.group(1) for m in PLACEHOLDER_RE.finditer(out)))
    if leftover:
        sys.exit(f"[ERROR] {machine['model']} 生成后仍有未替换占位符：{', '.join(leftover)}")

    return out


def header(machine: dict) -> str:
    fields = machine.get("fields", {})
    withheld_specs = sum(
        1 for k in fields if k.startswith("SPEC_") and "on request" in str(fields[k]).lower()
    )
    lines = [
        f"# {machine['model']} — {fields.get('PROCESS')} 落地页 Prompt",
        "",
        "```yaml",
        f"model: {machine['model']}",
        f"page_type: {machine.get('page_type', 'single-machine')}",
        f"machine_data_updated: {machine.get('updated', 'n/a')}",
        f"pairing_required: {str(bool(machine.get('pairing_required'))).lower()}",
        f"spec_rows_withheld: {withheld_specs}",
        "```",
        "",
        f"- 机型：`{machine['model']}`　页面类型：`{machine.get('page_type', 'single-machine')}`",
        f"- 机型数据版本：{machine.get('updated', 'n/a')}（框架版本见 skill CHANGELOG.md）",
    ]
    if machine.get("pairing_required"):
        lines.append(f"- **强制配套（页面上必须出现）**：{fields.get('PAIRING') or '见 machines/*.json'}")
    if machine.get("params_withheld"):
        lines.append("")
        lines.append("## ⚠️ 生成前请确认（这些参数未确认，已在内容中写 On request）")
        lines += [f"- {w}" for w in machine["params_withheld"]]
    lines += ["", "---", ""]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="生成 Southern Machinery 单机型 3D 落地页 Prompt")
    ap.add_argument("--list", action="store_true", help="列出所有可用机型")
    ap.add_argument("--model", help="机型名，如 S-WS450")
    ap.add_argument("--all", action="store_true", help="生成所有机型")
    ap.add_argument("--out", help="输出到指定文件（单机型）")
    ap.add_argument("--out-dir", help="批量输出目录（配合 --all）")
    ap.add_argument("--validate", action="store_true", help="生成后自动运行合规自检")
    args = ap.parse_args()

    if args.list:
        print(f"{'MODEL':<12} {'PROCESS':<26} {'UPDATED':<12} PAIRING*")
        print("-" * 70)
        for p in list_machines():
            m = json.loads(p.read_text(encoding="utf-8"))
            star = "*" if m.get("pairing_required") else " "
            print(f"{m['model']:<12} {m['fields']['PROCESS']:<26} {m.get('updated','n/a'):<12} {star}")
        print("\n* = 强制配套，页面上必须出现")
        return

    if not args.model and not args.all:
        ap.print_help()
        return

    body = load_template()
    targets = [args.model] if args.model else [p.stem for p in list_machines()]

    for model in targets:
        machine = load_machine(model)
        prompt = header(machine) + render(body, machine)

        if args.out_dir:
            outdir = Path(args.out_dir).expanduser()
            outdir.mkdir(parents=True, exist_ok=True)
            dest = outdir / f"{model}-landing-prompt.md"
            dest.write_text(prompt, encoding="utf-8")
            print(f"[OK] {dest}")
        elif args.out:
            dest = Path(args.out).expanduser()
            dest.write_text(prompt, encoding="utf-8")
            print(f"[OK] {dest}")
        else:
            print(prompt)

        if args.validate:
            tmp = Path("/tmp") / f"_lp_{model}.md"
            tmp.write_text(prompt, encoding="utf-8")
            r = subprocess.run([sys.executable, str(VALIDATOR), "--file", str(tmp)])
            if r.returncode:
                sys.exit(r.returncode)


if __name__ == "__main__":
    main()
