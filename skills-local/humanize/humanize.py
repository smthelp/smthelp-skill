from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path


def build_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text.strip()

    original = args.original
    if not original and args.baseline_text and not args.challenger_text:
        original = args.baseline_text

    # Auto-detect language from task/constraints/original to choose prompt language
    raw = " ".join(
        x for x in [args.task, args.constraints, original or ""] if x
    ).strip()
    import re as _re

    def _is_english(t: str) -> bool:
        if not t:
            return False
        latin = sum(1 for c in t if c.isascii() and c.isalpha())
        cjk = sum(1 for c in t if ord(c) > 0x2E7F)
        return latin > 10 and (latin > cjk * 1.2 or (latin > 15 and cjk <= 5))

    is_en = _is_english(raw)

    if is_en:
        lines = ["Use humanize to help generate and optimize an English communication message."]
        if args.task:
            lines.append(f"Task: {args.task.strip()}")
        if args.constraints:
            lines.append(f"Constraints: {args.constraints.strip()}")
        if args.must_include:
            lines.append(
                "Must include: " + ", ".join(f'"{item.strip()}"' for item in args.must_include if item.strip())
            )
        if args.banned_phrase:
            lines.append(
                "Avoid: " + ", ".join(f'"{item.strip()}"' for item in args.banned_phrase if item.strip())
            )
        if args.min_chars is not None:
            lines.append(f"At least {args.min_chars} characters")
        if args.max_chars is not None:
            lines.append(f"Within {args.max_chars} characters")
        if original:
            lines.append(f"Original: {original.strip()}")
    else:
        lines = ["用 humanize 帮我生成并优化一条中文沟通消息。"]
        if args.task:
            lines.append(f"任务：{args.task.strip()}")
        if args.constraints:
            constraint_parts = [args.constraints.strip()]
        else:
            constraint_parts = []
        if args.must_include:
            constraint_parts.append(
                "保留" + "、".join(f'"{item.strip()}"' for item in args.must_include if item.strip())
            )
        if args.banned_phrase:
            constraint_parts.append(
                "避免" + "、".join(f'"{item.strip()}"' for item in args.banned_phrase if item.strip())
            )
        if args.min_chars is not None:
            constraint_parts.append(f"不少于{args.min_chars}字")
        if args.max_chars is not None:
            constraint_parts.append(f"控制在{args.max_chars}字内")
        if constraint_parts:
            lines.append("约束：" + "，".join(constraint_parts))
        if original:
            lines.append(f"原文：{original.strip()}")

    return "\n".join(line for line in lines if line.strip())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Top-level wrapper for the humanize skill.",
    )
    parser.add_argument("--text", default=None)
    parser.add_argument("--task", default=None)
    parser.add_argument("--constraints", default=None)
    parser.add_argument("--must-include", action="append", default=[])
    parser.add_argument("--banned-phrase", action="append", default=[])
    parser.add_argument("--min-chars", type=int, default=None)
    parser.add_argument("--max-chars", type=int, default=None)
    parser.add_argument("--original", "--original-draft", dest="original", default=None)
    parser.add_argument("--baseline-text", default=None)
    parser.add_argument("--challenger-text", default=None)
    parser.add_argument("--run-dir", default=None)
    parser.add_argument("--output-root", default="./runs")
    parser.add_argument("--max-rounds", type=int, default=None)
    args = parser.parse_args()

    brief = build_text(args)
    if not brief.strip():
        raise ValueError("Provide --text or at least --task")

    script_path = Path(__file__).resolve().parent / "scripts" / "run_from_brief.py"
    sys.path.insert(0, str(script_path.parent))
    sys.argv = [
        str(script_path),
        "--text",
        brief,
        "--output-root",
        args.output_root,
    ]
    baseline_override = args.baseline_text if (args.original and args.baseline_text) else None
    if baseline_override:
        sys.argv.extend(["--baseline-text", args.baseline_text])
    if args.challenger_text:
        sys.argv.extend(["--challenger-text", args.challenger_text])
    if args.run_dir:
        sys.argv.extend(["--run-dir", args.run_dir])
    if args.max_rounds is not None:
        sys.argv.extend(["--max-rounds", str(args.max_rounds)])
    runpy.run_path(str(script_path), run_name="__main__")


if __name__ == "__main__":
    main()
