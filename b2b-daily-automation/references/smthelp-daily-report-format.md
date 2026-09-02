# Southern Machinery 日报 — Excel 数据结构与报告格式规范
> **来源**：`/Users/jasonwu/Downloads/日报_SouthernMachinery_YYYYMMDD.xlsx`
> **适用对象**：Jason Wu / Southern Machinery SMT/THT 外贸销售工程师
> **适用场景**：生成日报、读入结构化数据、填充报告模板

---

## 文件读取流程

```bash
# 1. 安装依赖（首次）
pip3 install openpyxl -q

# 2. 写解析脚本到 ~/read_daily_report.py
python3 /Users/jasonwu/read_daily_report.py
```

**解析脚本模板**（`/Users/jasonwu/read_daily_report.py`）：
```python
import openpyxl
wb = openpyxl.load_workbook('/Users/jasonwu/Downloads/日报_SouthernMachinery_20260609.xlsx')
for sheet in wb.sheetnames:
    ws = wb[sheet]
    print(f'=== Sheet: {sheet} ===')
    for row in ws.iter_rows(values_only=True):
        if any(cell is not None for cell in row):
            print(row)
```

---

## Sheet 1: 今日战绩与合规复盘

### Section A — 多渠道营销动态盘点
表头：`['#', '渠道', '今日新增', '2h响应率', '累计本周', '状态', '操作建议']`
- 重点行：A1–A6（对应 B2B平台/官网/IMAP/LinkedIn/WhatsApp/展会）
- 状态值：✅ 已同步 / ⚠️ 无实时数据 / ⚠️ 待人工填报

### Section B — 核心在谈大单水位复盘
表头：`['#', '客户 / 国家', '目标设备', '项目瓶颈', '技术合规状态', '商务博弈水位', '下一步动作']`
- 重点行：B1–B5（当前活跃大单，最高水位）
- 颜色标签：🔴 高风险 / 🟡 中风险 / ✅ 合规完成

### Section C — 工业参数追问漏斗
表头：`['#', '客户 / 国家', '缺失参数类型', '影响设备范围', '发出日期', '逾期天数', '催收优先级']`
- 重点行：C1–C4（阻塞正式报价的技术参数缺失）

### Section D — Worktile CRM 任务状态
字段：`['指标', '数值', '说明']`
- 关键指标：全部任务总数 / 延期任务 / 今日任务 / 本周任务 / 月报状态 / Weekly Forecast 状态
- 延期任务目标：≤10 个（当前 25 个，需加速清理）

### Section E — 本地文件与 WhatsApp 动态
表头：`['类型', '文件名 / 来源', '时间戳', '大小', '关联客户', '后续动作']`
- 重点：WhatsApp 图片（需归因到客户） / ROI PDF（已生成待发送） / 营销简报 PDF

---

## Sheet 2: 明日工业硬核任务

### Top3 任务表
表头：`['#', '任务标签', '具体动作描述', '关联客户 / 项目', '交付物', '执行人', '截止时间']`
- 任务标签格式：`T1\n🔴 P1`（优先级颜色 + P级别）
- 每条任务包含：SPIN 驱动标签 / 具体动作 / 关联客户 / 交付物 / 截止时间

### 支撑数据表
字段：`['任务', '阻塞点', '根本原因', '解锁后路径']`

### KPI 跟踪表（周五填入实际值）
字段：`['KPI指标', '目标值', '本周实际', '达成率', '状态']`
- 周目标参考：新增有效询盘≥5/周 / 2h响应率≥90% / 发出报价/提案≥3/周 / 样品成交≥1/周

---

## 报告输出格式（日报 — 6 模块）

```
## 1. 今日核心工作成果
- 以动词开头（跟进/寄出/制作/发布），列出完成的客户开发、询盘分析、技术方案设计

## 2. 核心客户互动与询盘矩阵
| 客户名称/国家 | 产品类型 | 询盘设备需求 | 当前痛点/推进阶段 |

## 3. 营销引流与新增线索统计
| 来源渠道 | 今日新增 | 本周累计 | 状态 |

## 4. 待跟进技术/商务阻碍点
| # | 客户 | 缺失参数 | 影响设备 | 根本原因 | 解锁动作 |

## 5. 明日 Top 3 优先级安排
T1 🔴 P1 — [客户名] [动作]（截止时间）
Hook: ...
交付物: ...

## 6. 【周五特别复盘】（仅周五触发）
周 KPI 对比 / 下周大客攻坚计划 / 社媒排期
```

---

## 今日日期判断逻辑
- `datetime.now().weekday()`: Monday=0, Friday=4
- 周五触发 Section 6；周一至周四不触发
- 周六/周日：无日报，跳过

---

## 关键文件路径
| 文件 | 路径 |
|---|---|
| 日报 Excel | `/Users/jasonwu/Downloads/日报_SouthernMachinery_{YYYYMMDD}.xlsx` |
| 本周工作计划 | `/Users/jasonwu/Downloads/本周工作计划_SouthernMachinery.xlsx` |
| ROI PDF | `/Users/jasonwu/Downloads/S-70LD_ROI_*.pdf` |
| 解析脚本 | `/Users/jasonwu/read_daily_report.py` |
| CRM | https://smthelp.worktile.com |

---

## 注意事项
1. **禁止编造数据**：所有数字必须来自 Excel / CRM / 邮件 / 用户提供
2. **WhatsApp 图片归因**：今日 6 张图片（Jun5）尚未关联客户，需录入 CRM
3. **延期任务清理**：25 个延期任务需分摊到周中处理，目标周五前 ≤10 个
4. **周五触发 Section 6**：今日为周二，不触发周五复盘模块
