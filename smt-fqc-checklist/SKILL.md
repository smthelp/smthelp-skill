---
name: smt-fqc-checklist
description: 把 Southern Machinery SMT/THT 产品资料（说明书、彩页、参数表、产品页、图片、视频）转成中英双语、品牌版、可勾选可签字的出厂检验 Checklist（FQC/OQC/FAT）：PDF（中文、英文各一份，A4 横版）+ Excel（中文版/English/待确认/抽样判定 4 个工作表）+ 待澄清问题清单。每项带检验方法/工具、标准值与上下限、抽样、依据来源（页码/章节/视频时间点），资料没有的数值一律标「待确认 / TBD」，绝不臆造。Use when Jason asks for 出厂检验表、出厂验收 checklist、FQC/OQC/FAT checklist、pre-shipment inspection list, or a new model/product line for one.
version: 1.0.0
metadata:
  updated: 2026-10-31
  first_product: S-JVF02 vibration stick feeder for JUKI RS-1
  depends_on: smt-brand-kit (brand tokens, never-publish rules)
  template_version: "1.0"
---

# smt-fqc-checklist — 产品资料 → 双语出厂检验 Checklist

一个产品 = 一份 `checklist.json`（唯一事实源）。脚本只负责渲染和把关；质量取决于提取与归类。

```
资料 sources/ → 解析提取 (extraction-rules.md) → facts 归类 → checklist.json (field-spec.md)
   → validate_checklist.py（闸门）→ build_checklist.py → CN.pdf / EN.pdf / CN-EN.xlsx / TBD-Questions.md
   → Jason 确认 ★/TBD → 改 status=C → build --release 正式版
```

## 触发条件
- Jason 说：出厂检验表 / 出厂验收 Checklist / FQC / OQC / FAT / 发货前检验 / pre-shipment inspection，并给出某机型或其资料链接。
- 新增机型、新增产品线、客户提出特殊验收要求（如巴西 NR-12 葡语标识、CE、目的地电压）需要改表时。
- 不适用：营销物料（用 smt-brand-kit）、报价/PI（smt-quotation / smt-proforma-invoice）。

## 适用场景
插件机（径向/轴向/异形）、贴片机、印刷机、回流焊/波峰焊、AOI/SPI、传送/上下板机、飞达及配件、分板机等 Southern Machinery 出口设备的出厂检验、客户见证验收（FAT）、发货前自检。

## 输入项清单（先收齐，缺的问 Jason，一次最多问 2 件）
| 输入 | 必需 | 说明 |
|---|---|---|
| 型号 + 产品名 | 是 | SM 型号（如 S-JVF02），不用供应商型号 |
| 产品资料 | 是，≥1 份 | 说明书 PDF、彩页、参数表、产品页 HTML、3D 页、图片、视频/音频链接或文件 |
| 产品线 | 是 | 选 `product-lines/registry.json` 中的一条；没有就按“新增产品线”流程加 |
| 适配机型 / 配置 | 视产品 | 如 JUKI RS-1、电压版本、选配 |
| 客户 / 目的地要求 | 否 | 目的地电压频率、语言、CE / NR-12 / UL 等 |
| 现有检验表 | 否 | 有则作为结构基础，条目并入并标来源 |
| 文档号 / 版本 | 否 | 默认 `SM-FQC-<MODEL>`、Rev. A |

## 输出物定义
1. `<MODEL>-FQC-Checklist-CN.pdf`、`<MODEL>-FQC-Checklist-EN.pdf`：A4 横版，品牌页眉（SM logo、公司、联系方式），表头（型号/适配/序列号/客户/订单 PI/目的地电压/检验员/日期），13 列表格，☐ 合格 ☐ 不合格 ☐ NA 可勾选，汇总、总判定、三方签字，抽样与判定规则，图例。中英两份一一对应，各自独立成表。
2. `<MODEL>-FQC-Checklist-CN-EN.xlsx`：工作表「中文版」「English」（判定下拉 + COUNTIF 统计 + 打印设置）、「待确认 TBD」、「抽样与判定 Sampling」。
3. `<MODEL>-TBD-Questions.md`：双语待澄清问题清单（发 Jason 确认）。
4. `checklist.json`：存档，下次改版直接改它。
列定义见 `references/field-spec.md`；版式见 `references/checklist-template.md`。

## 使用步骤
1. **建目录**：`<work>/<model>/sources/`，把资料下载进去（PDF、HTML、图片、视频）。
2. **解析提取**：按 `references/extraction-rules.md`：PDF 逐页取文本（无文字层的页转图片看）；HTML 取规格表；视频/音频取字幕或转写并记时间点；图片看铭牌/标签。每条事实记 值+单位+条件+来源（文件、章节、页码或 mm:ss）。
3. **归类**：把事实归入 8 类（功能项、技术参数、外观要求、尺寸公差、电气/性能指标、装配与包装、安全与合规、附件备件），再映射到产品线的检验分区（registry.json）。
4. **写 checklist.json**：从 `references/item-library.md` 取该产品线的通用条目，用产品事实填具体值；每项给 grade（CR/MA/MI）、status（C/S/T）、抽样、方法/工具、双语文字、来源；S/T 必须带双语问题。术语按 `references/glossary.csv`；品牌与型号（JUKI、RS-1、S-JVF02、Southern Machinery、smt-brand-kit）不翻译。
5. **闸门**：`python3 scripts/validate_checklist.py <checklist.json>` → 0 ERROR；WARN 逐条看（多为术语不一致）。
6. **渲染**：`python3 scripts/build_checklist.py <checklist.json> --out <dir>`；用 `pdftoppm -r 80 -png` 看 1–2 页，确认无溢出、颜色正确。
7. **交付 Jason**：PDF×2 + xlsx + 待澄清问题（一句话说明 ★ 与 TBD 数量）。
8. **定稿**：Jason 回答后把对应项改为 status C 并写来源 `Jason 确认 YYYY-MM-DD`，`--release` 渲染正式版（有 S/T 会被拒绝），Rev. 递增。
9. **沉淀**：Jason 的新规则写入对应 reference，并按“升级流程”改版本号。

## 约束与注意事项
- **不臆造**：产品参数只来自资料或 Jason；资料没有 → status T，判定标准写「待确认 / TBD」，不填数字（闸门会拦截）。
- **建议值**：仅可使用 `item-library.md` 中带编号的通用标准（G-xxx-nn）作建议，status S，显示 ★，进入问题清单，不能正式放行。
- 每项必须有来源：`手册 §9 p.12`、`产品页 §03 规格表 'Weight'`、`视频 01:25`、`通用标准 G-ELE-04`、`Jason 确认 2026-11-02`。资料内部冲突时 status T 并在问题里写出两个值。
- 不出现：供应商名称/标识/型号、价格、交期、质保、付款条款、客户名称（表头留空由产线填）、无证书的认证。
- 一台设备 100 % 全检；同型号批量小件按 config 的抽样规则。CR 项永远 100 %。
- 安全/电气项默认 CR；功能与规格 MA；外观、清洁、标签 MI（可按客户要求上调）。
- Chinese 回复 Jason；表格双语。不在表内写营销语言。
- 字体：需要 CJK 字体（Noto Sans SC）；缺失时下载 `https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf` 到 `~/.fonts` 并 `fc-cache -f`。依赖：`pip install openpyxl weasyprint`。

## 可扩展：参数化配置
- `config/default.json`：品牌（来自 smt-brand-kit brand.json）、语言、纸张、等级与状态定义、抽样（AQL、特采上限）、判定规则。客户或目的地专用规则：复制为 `config/<customer-or-country>.json`，用 `--config` 指定。
- `product-lines/registry.json`：产品线 → 分区模块、必检条目、关键参数提示。
- `references/item-library.md`：分区通用条目与 G 编号建议值。

### 新增产品线
1. 在 `registry.json` 加一条（id、中英名、sections、key_params、must_items）。
2. 在 `item-library.md` 加该产品线专有条目（如回流焊温区曲线、AOI 误报率），建议值给新的 G 编号。
3. 用一台真实机型跑完整流程，产出放 `examples/<model>/`，minor 版本 +1。

### 模板版本与 skill 版本
- skill 版本 `MAJOR.MINOR.PATCH`（frontmatter `version`）：MAJOR = checklist.json 格式不兼容；MINOR = 新产品线/新输出/新校验；PATCH = 文字、版式、bug。
- 模板版本 `template_version`（config 与每份 checklist.json 的 meta）：表格列或版式变化时 +0.1；旧 checklist.json 用旧模板版本号也能渲染时不改 MAJOR。
- 文档 Rev.（每份表）：A、B、C…，任何条目或数值变化 +1，放行后不得改同一 Rev.。
- 每次升级：改文件 → 跑示例 `examples/s-jvf02` 的 validate + build → 在下方历史加一行 → 同步 GitHub smthelp/smthelp-skill（先给 Jason 看）。

## 文件
- `references/usage-guide.md` 使用说明（给产线 / QC / 销售）
- `references/extraction-rules.md` 资料解析、提取、归类、来源标注规则
- `references/field-spec.md` checklist.json 字段说明 + 表格列说明
- `references/checklist-template.md` 版式模板（分区、表头、签字、图例）
- `references/item-library.md` 通用条目库与 G 编号建议值
- `references/glossary.csv` 中英术语对照（check=yes 的由闸门校验）
- `product-lines/registry.json` 产品线注册表
- `config/default.json` 参数化配置
- `scripts/validate_checklist.py`、`scripts/build_checklist.py`
- `examples/s-jvf02/` 完整示例：input（资料清单 + 提取归类结果）→ output（checklist.json + PDF/xlsx/问题清单）

## 版本历史
- 1.0.0 (2026-10-31) 首版：由 S-JVF02（JUKI RS-1 振动料管飞达）验收表沉淀；双语 PDF/xlsx/TBD 输出，C/S/T 状态、CR/MA/MI 等级、抽样判定规则、validate 闸门、产品线注册表。
