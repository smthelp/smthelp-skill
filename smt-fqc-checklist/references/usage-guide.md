# 使用说明 / Usage guide

## 给 Jason / 销售：怎么让 Hark 出一份新表
发一句话 + 资料即可，例如：
> 用 smt-fqc-checklist 给 S3010A 径向插件机做出厂检验表，资料：<说明书链接> <参数表> <视频链接>；客户巴西，220 V 60 Hz，要 NR-12。

Hark 会：读资料 → 归类 → 生成中文 PDF、英文 PDF、Excel、待澄清问题清单 → 发你确认。你只需回答问题清单（如“扭矩用 0.6 N·m”、“没有光电传感器”），Hark 改为已确认后出正式版（Rev. A，正式放行版不再有 ★ 和 TBD）。

## 给产线 / QC：怎么填表
1. 表头：填序列号、客户、订单/PI 号、目的地/电压、检验员、日期（型号和适配机型已预填）。
2. 逐项按“检验方法 / 工具”操作，对照“判定标准”和“标准值 / 下限 ~ 上限”。
3. 判定结果：PDF 勾 ☐ 合格 / ☐ 不合格 / ☐ NA；Excel 用下拉选择，底部自动统计。
4. 实测值：凡有数值的项必须写实测数字和单位（如 24.3 V、0.05 Ω、62 dB(A)）。
5. NA：在“结论 / 备注”写原因（如“本机无皮带机构”）。
6. 不合格：备注写现象与处置（返工 / 更换零件），复检后另起一行或在备注写复检结果与日期。
7. 总判定按页底“抽样与判定规则”：任一 CR 不合格 → 不放行；MA 不合格 → 返工复检；仅 MI 且 ≤ 2 项 → QC 主管可特采。
8. 签字：检验员、QC 主管；客户见证验收时客户签字。拍照编号写在备注。
9. 草稿版（页眉红字“草稿”）只用于试检和确认阈值，不能用于正式放行。

## 符号
- ★ 建议值：资料未给出，按通用标准建议，待确认。
- 待确认 / TBD：资料缺失，没有填数字，需要工程或 Jason 提供。
- 等级 CR 致命 / MA 主要 / MI 次要。
- 依据来源：`手册 §5.1 p.9` = 操作手册第 5.1 节第 9 页；`产品页 §03` = 产品页第 03 节规格表；`视频 01:25` = 视频时间点；`通用标准 G-ELE-04` = 本 skill 通用条目库编号。

## 命令速查（Hark / 工程师）
```bash
pip install openpyxl weasyprint
python3 scripts/validate_checklist.py examples/s-jvf02/output/checklist.json
python3 scripts/build_checklist.py examples/s-jvf02/output/checklist.json --out /tmp/out           # 草稿
python3 scripts/build_checklist.py <checklist.json> --out <dir> --release                          # 正式版（无 S/T 才能通过）
python3 scripts/build_checklist.py <checklist.json> --out <dir> --config config/brazil-nr12.json    # 客户 / 目的地专用配置
```
