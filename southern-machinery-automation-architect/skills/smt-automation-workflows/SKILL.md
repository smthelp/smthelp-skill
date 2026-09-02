---
name: smt-automation-workflows
description: "Southern Machinery automation workflow design toolkit. Provides the TAOC YAML schema reference, ready-to-use workflow templates for inquiry triage, competitor monitoring, LinkedIn lead capture, daily content generation and YouTube notes ingestion, plus a blank workflow template. Loaded by the Southern Machinery Automation Workflow Architect expert."
---

# SMT 自动化工作流设计工具包

本 Skill 为 Southern Machinery 自动化工作流架构师提供设计所需的参考资料与模板。

## 包含内容

| 文件 | 用途 |
|------|------|
| `references/workflow-yaml-schema.md` | TAOC 工作流 YAML schema 完整字段说明 |
| `references/workflow-examples.md` | 5 大场景的完整工作流示例（询盘分类/竞品监控/LinkedIn 抓取/每日内容/YouTube 入库） |
| `references/business-metric-map.md` | 业务指标映射表，用于工作流的业务价值标注 |
| `templates/workflow-template.yaml` | 空白工作流模板，可直接复制填充 |

## 使用方式

1. 设计新工作流时，先读 `references/workflow-yaml-schema.md` 确认字段规范
2. 对照 `references/workflow-examples.md` 中同类场景的示例
3. 用 `templates/workflow-template.yaml` 作为起点填充内容
4. 在"业务价值"段落引用 `references/business-metric-map.md` 中的指标定义
