# 版式模板 / Layout template (template_version 1.0)

## 页面
A4 横版，边距 10/8/12/8 mm；字体 Noto Sans SC（中英通用）；配色取 smt-brand-kit：Navy #003142 表头，Green #93AC3E 分隔线与分区左条，Light #EEF5F7 分区底色，★ 建议值 #9C5700，TBD #C0392B。

## 页面结构（自上而下）
1. 页眉：SM logo｜`<型号> <产品名> — 出厂检验 Checklist`｜副标题（适配机型 · 中文版/English）｜右侧公司全称、联系方式、文档号 Rev.、模板版本、smt-brand-kit。草稿状态加红字“草稿 – 含建议值或待确认项，不得用于正式放行”。
2. 表头信息（2 列 × 4 行）：型号、适配/配置、序列号、客户、订单/PI 号、目的地/电压、检验员、检验日期。
3. 检验表：13 列（见 field-spec.md），表头每页重复，分区行横跨整表。
4. 汇总：检验项数、合格、不合格、NA；总判定 ☐ 放行 ☐ 特采放行 ☐ 不放行/返工。
5. 签字：检验员 / QC 主管 / 客户见证（各含日期）。
6. 抽样与判定规则（来自 config）。
7. 图例：等级、★、TBD、来源写法、术语。
8. 页脚：Southern Machinery · 联系方式 · 文档号 Rev. · 页码 n / N。

## 标准分区（按产品线取用，代码固定，便于跨机型对比）
| 代码 | 中文 | English |
|---|---|---|
| A | 整机外观与结构 | Appearance & Structure |
| B | 机构装配与螺丝紧固 | Mechanical Assembly & Fastening |
| C | 功能 / 供料 / 运行测试（产品线命名，如“飞达供料与振动 / 皮带机构”） | Function / Feeding / Run Test |
| D | 传感器与光电检测 | Sensors & Photoelectric Detection |
| E | 电气与安全（接地、绝缘、急停） | Electrical & Safety |
| F | 规格参数核对 | Specification Verification |
| G | 软件与参数（有控制系统的设备） | Software & Parameters |
| H | 精度与产能（插件机、贴片机、印刷机、AOI） | Accuracy & Throughput |
| J | 随机文件、备件与包装 | Documents, Spares & Packing |
| K | 客户 / 目的地专项（NR-12、CE、电压） | Customer / Destination Requirements |

（不用 I，避免与数字 1 混淆。）小型配件可把 J 并入 F 的最后一项，如 S-JVF02 的 F08。
