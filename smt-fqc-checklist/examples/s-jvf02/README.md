# 示例：S-JVF02 振动料管飞达（JUKI RS-1）

输入 → `input/request-and-sources.md`：Jason 的请求、4 份资料及读取结果、事实提取表、归类映射。
输出 → `output/`：
- `checklist.json` 唯一事实源（48 项，6 个分区 A–F；26 项已确认 C，19 项建议值 S ★，3 项待确认 T）
- `S-JVF02-FQC-Checklist-CN.pdf` / `-EN.pdf` 中英文独立表（草稿）
- `S-JVF02-FQC-Checklist-CN-EN.xlsx` 中文版 / English / 待确认 TBD / 抽样与判定
- `S-JVF02-TBD-Questions.md` 22 个待澄清问题

对照阅读：输入事实表每一行都能在 checklist.json 的 source 字段找到；资料缺失的 3 项（D04 光电传感器、E08 安全标签、F05 振动频率范围）没有数值，只有问题。

复现：
```bash
python3 scripts/validate_checklist.py examples/s-jvf02/output/checklist.json
python3 scripts/build_checklist.py examples/s-jvf02/output/checklist.json --out examples/s-jvf02/output
```
