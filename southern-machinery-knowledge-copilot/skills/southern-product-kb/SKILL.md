---
name: southern-product-kb
description: Southern Machinery 产品知识库建设工具集。提供产品分类体系、知识卡片模板、SEO/GEO 关键词库、产品线清单等参考资料，用于将原始产品资料编译为结构化 Wiki。
---

# Southern Machinery 产品知识库 Skill

本 Skill 为 Southern Machinery 产品知识 Copilot 提供结构化参考资料，包括：

- **产品分类体系**（`references/product-taxonomy.md`）：7 大产品类别的标准定义与归属规则
- **产品线清单**（`references/product-lineup.md`）：Southern Machinery 重点产品型号与基础信息
- **知识卡片模板**（`references/knowledge-card-template.md`）：13 章节标准知识卡片模板与填写规范
- **SEO/GEO 关键词库**（`references/seo-keyword-bank.md`）：按产品类别与工艺场景组织的关键词矩阵
- **FAQ 句式模板**（`references/faq-patterns.md`）：高频客户问题句式与回答框架
- **整线配置矩阵**（`references/production-line-matrix.md`）：SMT→THT→波峰焊→板处理的产线衔接参考

## 使用方式

- 当用户要求整理某个产品时，先读取 `references/product-taxonomy.md` 确认分类，再读取 `references/product-lineup.md` 核对型号，然后按 `references/knowledge-card-template.md` 输出知识卡片。
- 当用户要求生成 SEO/GEO 内容时，参考 `references/seo-keyword-bank.md` 匹配关键词。
- 当用户要求做整线方案时，参考 `references/production-line-matrix.md` 确认产线衔接。
- 模板文件位于 `templates/`，可直接复制使用：
  - `templates/product-card.md` — 单产品知识卡片空白模板
  - `templates/faq-page.md` — FAQ 页空白模板
  - `templates/comparison-page.md` — 产品对比页空白模板
