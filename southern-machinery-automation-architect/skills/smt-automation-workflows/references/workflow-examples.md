# 5 大场景完整工作流示例

以下为 Southern Machinery 最高频的 5 个自动化场景的完整 TAOC 工作流示例，可直接复制修改使用。

---

## 示例 1：询盘自动分类与分级（Sales · Inquiry Triage）

```yaml
workflow:
  name: "询盘自动分类与分级 / Inquiry Auto-Triage"
  category: "sales"
  business_goal: "A 类询盘 24h 内个性化回复，C 类自动发目录，减少人工分级耗时"
  target_metric: "Response Time"
  owner: "Jason Wu"
  schedule: "实时（邮件到达即触发）"

trigger:
  type: "email"
  condition: "subject contains 'inquiry|quote|price|SMT|THT|wave solder' AND from != @smthelp.com"
  source: "Gmail 询盘收件箱"

steps:
  - name: "解析邮件内容"
    tool: "gmail.read"
    input: "新邮件的 subject + body + attachments"
    output: "结构化字段：sender_email, company_name, country, product_interest, pcb_params, quantity"
  - name: "匹配客户分级规则"
    tool: "rule_engine.classify"
    input: "结构化字段 + Southern Machinery 分级规则库"
    output: "tier: A | B | C，附分级理由"
    note: "A=明确产品+数量+公司背景；B=有产品意向缺细节；C=泛泛问价"
  - name: "生成回复草稿"
    tool: "llm.generate_email"
    input: "tier + 客户信息 + 产品知识库"
    output: "A类=个性化回复草稿；B类=模板+追问清单；C类=目录PDF附件"
  - name: "写入询盘台账"
    tool: "sheets.append"
    input: "客户信息 + 分级 + 草稿链接"
    output: "Google Sheets 新增一行记录"
    note: "台账列：日期/公司/国家/产品/分级/状态/负责人"

output:
  format: "email_draft"
  location: "email://jason@smthelp.com (草稿) + sheets://inquiry_log"
  fields: ["日期", "公司名", "国家", "产品意向", "PCB参数", "分级", "回复草稿链接", "台账行号"]

cta:
  action: "推送 Telegram 通知 Jason 有新询盘待处理"
  target: "telegram://@jason_wu"
  auto: true
```

```markdown
## 业务价值
- **提升指标**：Response Time（A 类询盘从平均 2 天缩短到 <24h）
- **预估节省**：每周节省 4 小时人工分级时间
- **业务影响**：A 类询盘响应速度提升直接提高成单概率；C 类自动发目录释放销售精力聚焦高价值客户
```

---

## 示例 2：竞品价格监控（Intelligence · Competitor Watch）

```yaml
workflow:
  name: "竞品价格与规格周报 / Competitor Price & Spec Weekly"
  category: "intelligence"
  business_goal: "每周掌握 JUKI/Yamaha/Universal/Neoden/新益昌 价格与规格变动"
  target_metric: "Knowledge Reuse"
  owner: "Jason Wu"
  schedule: "每周一 09:00"

trigger:
  type: "schedule"
  condition: "cron: '0 9 * * 1'"
  source: "竞品官网产品页 + 行业新闻源"

steps:
  - name: "抓取竞品产品页"
    tool: "web_scraper.extract"
    input: "竞品 URL 列表（JUKI/Yamaha IM/Universal/Neoden/新益昌）"
    output: "各竞品产品名/型号/价格/规格/促销信息"
    note: "价格变动需人工审核后采信"
  - name: "与上周数据对比"
    tool: "diff.compare"
    input: "本周抓取数据 + Obsidian://Competitors/last_week.json"
    output: "变动项清单：涨价/降价/新增型号/规格更新/促销活动"
  - name: "生成竞品变动周报"
    tool: "llm.generate_report"
    input: "变动项清单 + Southern Machinery 对应产品对比"
    output: "Markdown 周报，含变动表格 + Southern Machinery 应对建议"
  - name: "存档本周数据"
    tool: "obsidian.write"
    input: "本周抓取的完整数据"
    output: "Obsidian://Competitors/YYYY-MM-DD.json"

output:
  format: "markdown + pdf"
  location: "obsidian://Competitors/Weekly/ + telegram://@jason_wu"
  fields: ["竞品名", "产品型号", "上周价格", "本周价格", "变动幅度", "规格变化", "应对建议"]

cta:
  action: "推送周报摘要到 Telegram 并生成 PDF 存档"
  target: "telegram://@jason_wu + obsidian://Competitors/Reports/"
  auto: true
```

```markdown
## 业务价值
- **提升指标**：Knowledge Reuse（竞品情报从散落网页变为结构化可检索知识库）
- **预估节省**：每周节省 3 小时人工搜集竞品信息时间
- **业务影响**：及时掌握竞品价格变动，支撑 Southern Machinery 报价策略与差异化定位
```

---

## 示例 3：LinkedIn 线索抓取与触达（Marketing · Lead Capture）

```yaml
workflow:
  name: "LinkedIn 目标线索抓取 / LinkedIn Lead Capture"
  category: "marketing"
  business_goal: "从东南亚/中东/墨西哥/东欧 EMS/ODM 工厂提取决策者线索"
  target_metric: "Leads"
  owner: "Jason Wu"
  schedule: "每日 08:30"

trigger:
  type: "schedule"
  condition: "cron: '30 8 * * *'"
  source: "LinkedIn 搜索 + 目标公司列表"

steps:
  - name: "搜索目标公司决策者"
    tool: "linkedin.search"
    input: "目标区域 EMS/ODM 公司名 + 职位关键词（CEO/CTO/Production Manager/Sourcing）"
    output: "决策者清单：姓名/职位/公司/区域/LinkedIn URL"
  - name: "匹配采购意向信号"
    tool: "llm.score_intent"
    input: "决策者近期动态 + 公司规模 + 行业匹配度"
    output: "意向评分 1-5 + 信号说明（如：近期发帖提到产线扩建/SMT 采购）"
  - name: "生成触达话术草稿"
    tool: "llm.generate_outreach"
    input: "高意向决策者信息 + Southern Machinery 价值主张"
    output: "LinkedIn 连接请求话草稿（≤300 字符）+ 跟进消息草稿（150-300 词）"
    note: "话术必须含具体 ROI 数据点，禁止模板感"
  - name: "写入线索台账"
    tool: "sheets.append"
    input: "线索信息 + 评分 + 话术草稿链接"
    output: "Google Sheets 新增线索行"

output:
  format: "table"
  location: "sheets://linkedin_leads + email://jason@smthelp.com (话术草稿)"
  fields: ["姓名", "职位", "公司", "区域", "LinkedIn URL", "意向评分", "信号说明", "话术草稿"]

cta:
  action: "推送当日高意向线索清单到 Jason 待审队列"
  target: "telegram://@jason_wu"
  auto: true
```

```markdown
## 业务价值
- **提升指标**：Leads（每日新增结构化线索，替代手动搜索）
- **预估节省**：每周节省 6 小时人工搜索 LinkedIn 时间
- **业务影响**：线索触达从"想起来才做"变为每日稳定产出，扩大目标区域覆盖
```

---

## 示例 4：每日营销内容生成（Marketing · Daily Content）

```yaml
workflow:
  name: "每日营销内容包 / Daily Marketing Content Pack"
  category: "marketing"
  business_goal: "每日产出 LinkedIn 帖子 + EDM 邮件 + 产品短文，保持内容节奏"
  target_metric: "Content Output"
  owner: "Jason Wu"
  schedule: "每日 09:00"

trigger:
  type: "schedule"
  condition: "cron: '0 9 * * *'"
  source: "产品知识库 + 内容日历 + 行业新闻"

steps:
  - name: "读取今日内容主题"
    tool: "calendar.read"
    input: "内容日历今日条目（产品/案例/行业洞察轮换）"
    output: "主题 + 对应产品知识卡路径"
  - name: "生成多平台文案"
    tool: "llm.generate_content"
    input: "主题 + 产品知识卡 + Southern Machinery 价值主张"
    output: "LinkedIn 帖子（150-300 词+3标签）/ EDM 邮件（≤300 词+CTA）/ 产品短文（200-400 词）"
    note: "文案必须含硬数据（产能/CPH/ROI），禁止废话和模板感"
  - name: "标注关键词与 CTA"
    tool: "llm.tag_content"
    input: "生成的文案"
    output: "SEO 关键词建议 + CTA 链接（官网产品页/询盘表单/WhatsApp）"
  - name: "存档至内容库"
    tool: "obsidian.write"
    input: "完整内容包"
    output: "Obsidian://Marketing/Daily/YYYY-MM-DD.md"

output:
  format: "markdown"
  location: "obsidian://Marketing/Daily/ + telegram://@jason_wu"
  fields: ["日期", "主题", "LinkedIn帖子", "EDM邮件", "产品短文", "关键词", "CTA链接"]

cta:
  action: "推送内容包到 Jason 待发布队列"
  target: "telegram://@jason_wu"
  auto: true
```

```markdown
## 业务价值
- **提升指标**：Content Output（从每周手动写 1-2 篇变为每日稳定产出 3 篇）
- **预估节省**：每周节省 5 小时内容创作时间
- **业务影响**：保持 LinkedIn 和 EDM 内容节奏，持续触达目标客户，提升品牌曝光与询盘转化
```

---

## 示例 5：YouTube 视频笔记入库（Knowledge · Notes Ingestion）

```yaml
workflow:
  name: "YouTube 视频笔记自动入库 / YouTube Notes Ingestion"
  category: "knowledge"
  business_goal: "把 SMT 行业 YouTube 视频自动转为结构化 Cornell 笔记入库"
  target_metric: "Knowledge Reuse"
  owner: "Jason Wu"
  schedule: "手动触发（输入视频 URL）"

trigger:
  type: "manual"
  condition: "on_demand（用户提供 YouTube URL）"
  source: "YouTube 视频字幕/转录"

steps:
  - name: "获取视频字幕"
    tool: "youtube.transcript"
    input: "YouTube 视频 URL"
    output: "完整字幕文本 + 时间戳"
  - name: "提取关键知识点"
    tool: "llm.extract_keypoints"
    input: "字幕文本 + SMT 领域知识库"
    output: "关键知识点清单（技术要点/产品提及/行业洞察）"
  - name: "生成 Cornell 笔记"
    tool: "llm.generate_cornell"
    input: "关键知识点 + 视频元信息（标题/频道/时长）"
    output: "Cornell 笔记：线索栏（关键词）/ 笔记栏（详细内容）/ 总结栏（3-5 句摘要）"
  - name: "匹配产品分类"
    tool: "rule_engine.classify"
    input: "笔记内容 + Southern Machinery 产品分类体系"
    output: "关联产品标签（S-70LD/S-WS450/SUL460/S3000/通用）"
  - name: "写入知识库"
    tool: "obsidian.write"
    input: "Cornell 笔记 + 产品标签 + 视频元信息"
    output: "Obsidian://Knowledge/YouTube/YYYY-MM-DD-video-title.md"

output:
  format: "markdown"
  location: "obsidian://Knowledge/YouTube/ + telegram://@jason_wu (摘要)"
  fields: ["视频标题", "频道", "时长", "Cornell笔记", "关键知识点", "关联产品", "摘要"]

cta:
  action: "推送笔记摘要到 Telegram 并更新知识索引"
  target: "telegram://@jason_wu + obsidian://Knowledge/Index.md"
  auto: true
```

```markdown
## 业务价值
- **提升指标**：Knowledge Reuse（视频知识从看过即忘变为可检索结构化笔记）
- **预估节省**：每个视频节省 30 分钟手动整理笔记时间
- **业务影响**：行业知识持续沉淀，支撑销售话术和内容创作的素材储备
```
