# PDF / xlsx 源材料提取回退链 (Extraction Fallback Chain)

实战场景：在混合格式、含图片型 PDF（尤其中文产品彩页）的物料库中抽证据时，标准视觉工具可能不可用。以下是已验证可用的回退链。

## 0. 可提取性探针（先判断文本型 vs 图片型）
```bash
pdftotext -layout "file.pdf" - | wc -w
# 词数为 0 → 图片型 PDF，走下方 OCR 链
```

## 1. 图片型 PDF → OCR（vision_analyze 不可用时的替代）
`vision_analyze` 在本机可能报 `No LLM provider configured for task=vision provider=auto. Run: hermes setup`。**不要反复重试**——直接 OCR：
```bash
pdftoppm -png -r 150 "file.pdf" /tmp/out            # 渲染每页 PNG：out-1.png, out-2.png ...
tesseract /tmp/out-1.png stdout --psm 6             # 整页块识别，中英文混合更稳
for pg in /tmp/out-*.png; do echo "== $pg =="; tesseract "$pg" stdout --psm 6 2>/dev/null; done
```
要点：
- `--psm 6`（统一块）在带表格/图注的产品页上比 `--psm 11/12` 更准。
- 渲染 dpi 150–180 兼顾速度与识别率；dpi 过低中文漏识严重。
- 依赖：`pdftoppm`（poppler）、`tesseract`（已装 5.5.2）。

## 2. xlsx 读取（execute_code 被拦截时）
若 `execute_code` 返回 `BLOCKED: cron_mode ... approve only if this cron profile is intentionally trusted`，改用终端 heredoc（同样被审批放行后可用）：
```bash
python3 - <<'PY'
import openpyxl
wb=openpyxl.load_workbook("file.xlsx", read_only=True, data_only=True)
for ws in wb.worksheets:
    print("--- Sheet:", ws.title, ws.max_row, "x", ws.max_column)
    for i, r in enumerate(list(ws.iter_rows(values_only=True))[:16]):
        vals=[str(c) for c in r if c is not None and str(c).strip()!=""]
        if vals: print(f"  R{i+1}:", " | ".join(vals)[:170])
PY
```

## 3. 多产品库归并策略（供上游 PPT/文档生成 skill 参考）
- 文件 > ~30 时先按产品线分族，再**先选 1 条做样板走完所有确认门**，用户满意后再批量。
- 跨型号速度/价格差异属正常（如 4,000 / 5,000 / 6,000 / 12,000 CPH），不是数据冲突，不要“静默修正”。

## 4. 已知坑（排查用，非约束）
- `python-pptx` 在 Hermes venv 曾因 lxml `etree` 导入失败；进入渲染前先 `python3 -c "import pptx"` 验证。
- 外部卷路径可能被系统提示标记为 "outside the allowed workspace"，但实际可读；遇权限提示按正常审批放行。
