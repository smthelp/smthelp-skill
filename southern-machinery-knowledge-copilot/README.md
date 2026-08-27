# Southern Machinery 产品知识 Copilot

Southern Machinery SMT/THT 产品知识库架构师，将原始产品资料编译为结构化 Markdown Wiki，生成知识卡片、FAQ、SEO/GEO 内容与销售话术，支持官网与内容营销复用。

## 类型

Agent 型（单个 AI 专家）· 行业分类：05-MarketingGrowth（营销增长）

## 核心能力

1. **产品资料结构化编译** — 将手册/规格书/PPT/网页内容提炼为统一结构知识卡片，建立产品分类体系与参数标准化字段
2. **GEO/SEO/AEO 内容生成** — 输出可直接进入官网/WordPress/Notion/CRM/PPT 的结构化内容块（关键词、FAQ、卖点、内容页建议）
3. **整线知识图谱构建** — 围绕 SMT → THT → 波峰焊 → 板处理 建立产品关联、工艺衔接、选型逻辑
4. **销售与内容营销赋能** — 提炼适用场景、参数、优势、限制、兼容性，生成销售跟进话术
5. **矛盾标注与索引维护** — 多资料参数冲突时标注来源，维护产品/参数/场景/关键词索引

## 知识库 Skill（southern-product-kb）

预加载的结构化参考资料：

- `references/product-taxonomy.md` — 7 大产品类别标准定义与归属规则
- `references/product-lineup.md` — Southern Machinery 重点产品型号清单
- `references/knowledge-card-template.md` — 13 章节标准知识卡片模板与填写规范
- `references/seo-keyword-bank.md` — 按类别与场景组织的 SEO/GEO 关键词矩阵
- `references/faq-patterns.md` — 高频客户问题句式与回答框架
- `references/production-line-matrix.md` — 整线配置与产线衔接参考
- `templates/` — 知识卡片/FAQ 页/对比页空白模板

## 使用示例

- 帮我整理一份 S-70LD 自动插件机的产品知识卡片，按标准结构输出
- 把这份波峰焊产品手册编译成结构化 Wiki，建立交叉引用和索引
- 为 Southern Machinery SMT 产线生成一篇 SEO 文章大纲

## 头像

头像已通过 ImageGen 自动生成在 `avatars/expert.png`（1024×1024，红橙色调，对应营销增长分类）。如需替换为自定义头像：
- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 安装

专家包已位于专家目录：

```
~/.workbuddy/plugins/marketplaces/my-experts/plugins/southern-machinery-knowledge-copilot/
```

已通过 register_expert.py 注册到 marketplace.json，在 WorkBuddy 中可见可用。

## 打包分享

```bash
python3 scripts/package_expert.py ~/.workbuddy/plugins/marketplaces/my-experts/plugins/southern-machinery-knowledge-copilot/
```
