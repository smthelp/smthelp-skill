# 问题库 · Issue Library

> **升级协议**：每次评估结束，发现的新问题类型追加到对应维度下。格式：
> `### [ID] 标题` + **症状** / **为什么扣分** / **检测方式** / **修复模板**。
> 若某问题反复出现（≥3 次），把它提升为 `config/scoring-rubric.json` 的正式 check 项并 bump `rubric_version`。

---

## A · 技术地基

### A-01 全站无 canonical
- **症状**：多个 URL 返回相同或高度相似内容（如 `/p` 与 `/p/`、带参数 URL、多域名）
- **为什么扣分**：引擎无法判断哪个是权威版本，权重分散
- **检测**：`canonical_coverage`（脚本自动）
- **修复模板**：每个页面 `<link rel="canonical" href="https://主域/当前路径" />`

### A-02 hreflang 缺协议前缀
- **症状**：`<link rel="alternate" hreflang="es" href="www.example.com/es/">` —— href 少了 `https://`
- **为什么扣分**：无效 URL，多语种声明全部作废，等于放弃对应语种市场
- **检测**：`hreflang_broken_hrefs`（脚本自动）
- **修复模板**：`href="https://www.example.com/es/"`，另加 `x-default` 指向主站

### A-03 soft-404
- **症状**：`/sitemap.xml` 返回 HTTP 200，但渲染的是 404 页面
- **为什么扣分**：抓取器消耗预算却拿到空内容，且产生"站点维护不佳"信号
- **检测**：`sitemap_soft404` / `soft404_pages`（脚本自动）
- **修复模板**：不存在的路径应返回真 404；已迁移的做 301；robots 里只声明真实存在的 sitemap

### A-04 导航死链
- **症状**：主导航里的入口（如 `/about-us-smthelp`、`/certificate`）实际返回 404 模板
- **为什么扣分**：同上，且用户与引擎都会遇到断头路
- **检测**：脚本抓取带 `about|contact|company` 的页面并检测 `is_soft404`
- **修复模板**：修复或移除入口；用 sitemap 与导航做交叉比对

### A-05 sitemap 批量 lastmod
- **症状**：2,864 条 URL 的 lastmod 同为某一天
- **为什么扣分**：时间戳失去新鲜度信号价值，引擎会忽略
- **检测**：`sitemaps[].lastmod_top` 分布（脚本自动）
- **修复模板**：只有内容真正变更时才更新 lastmod；批量重生成时保留原值

---

## B · 结构化数据

### B-01 全站零 JSON-LD ★最高频
- **症状**：`application/ld+json` 数量为 0，全站没有任何 schema
- **为什么扣分**：AI 无法机器确认实体身份，只能靠正文猜测；这是与同行的最大分差来源
- **检测**：`jsonld_total`（脚本自动）
- **修复模板**：见 `jsonld-templates.md`，首页至少注入 Organization + Person + FAQPage

### B-02 缺 Organization
- **症状**：没有公司名 / 地址 / 电话 / 成立年份的机器可读声明
- **为什么扣分**：NAP 不完整直接导致地图类与本地服务类问答失去引用资格
- **检测**：`has_organization`（脚本自动）
- **修复模板**：Organization 必填 `name / url / logo / address(streetAddress+addressLocality+addressCountry) / telephone / foundingDate / sameAs`

### B-03 产品页缺 Product schema
- **症状**：几百个产品 URL，没有一个带价格/型号/规格标记
- **为什么扣分**：无法被"某参数的产品选哪家"类问句召回
- **检测**：`has_product_schema`（脚本自动）
- **修复模板**：Product + `additionalProperty`（参数表逐项写入）+ `brand` + `offers`

### B-04 FAQ 有内容无 schema
- **症状**：`/faq` 页有真实问答，但没声明 `FAQPage`
- **为什么扣分**：等于把现成的 AI 速览卡弹药锁在抽屉里
- **检测**：`has_faq_content == true` 且 `has_faqpage == false`
- **修复模板**：见 `jsonld-templates.md` 的 FAQPage 段

### B-05 无 OG 标签
- **症状**：`og:*` 全为 0
- **为什么扣分**：社媒与 AI 抓取时无标题图与摘要卡，分享与引用形态不可控
- **检测**：`og_total`（脚本自动）

---

## C · 内容 AI 友好度

### C-01 首页无 H1 ★高频
- **症状**：全站最重要的页面 `h1_count = 0`
- **为什么扣分**：H1 是引擎抽取页面主题的权重最高信号
- **检测**：`homepage_h1`（脚本自动）
- **修复模板**：`品牌 + 品类 + 地域 + 年限` 四要素一句话，如
  `SMT & THT PCB Assembly Automation Equipment Manufacturer in Shenzhen, China Since 2011`

### C-02 数据化表达缺失
- **症状**：整页形容词堆砌（"professional / high quality / reliable"），无可量化参数
- **为什么扣分**：数字比形容词的 AI 采纳率高一个量级
- **检测**：`avg_data_density`（脚本自动，目标 ≥1.5/百词）
- **修复模板**：把每条承诺改写成可验证数字 —— "快速响应" → "2 小时内响应，当天出报价"

### C-03 产品页无参数表
- **症状**：`table_count = 0`，规格用图片呈现
- **为什么扣分**：图片里的参数引擎读不到，无法比对也无法引用
- **检测**：`has_spec_table`（脚本自动）
- **修复模板**：用 `<table>` 呈现核心参数（尺寸/产能/精度/功率/气源/重量），并同步进 Product schema

### C-04 内容时间衰减
- **症状**：博客最后更新停在 2–3 年前
- **为什么扣分**：生成引擎对新鲜度极敏感，旧内容几乎不被优先召回
- **检测**：`content_freshness_days`（脚本优先取博客真实发布日期，不信任 sitemap lastmod）
- **修复模板**：先复活 6 篇核心文章（改时间戳 + 补内容 + 加 Article schema），再稳定更新

### C-05 问句未用买家原话
- **症状**：FAQ 写的是"产品特点"，不是买家会问 AI 的话
- **为什么扣分**：匹配不上提问形态，进不了速览卡
- **检测**：`question_headings`（脚本）+ 人工判断
- **修复模板**：补上品牌/地域/场景限定词 ——
  "好操作吗？" → "Is Southern Machinery's SMT machine easy to operate for first-time users?"

### C-06 高价值证据只出现在一页
- **症状**：20 年经验 / 2 小时响应 / 100% 退款 只在 `/about-us`，首页与产品页都没有
- **为什么扣分**：单点证据难以被反复召回
- **修复模板**：把核心证据做成"证据块"，在首页、产品页、博客复用

---

## D · 站外信源生态

### D-01 全自证 ★最致命
- **症状**：检索品牌能找到的信源 100% 是自有资产（官网、自己的社媒、自己的公众号）
- **为什么扣分**：孤证不立。AI 提你的时候没有任何第三方能替你说话
- **检测**：Agent 检索后统计 `independent_source_count` / `independent_ratio`
- **修复模板**：第三方信源计划 —— 行业媒体投稿、协会档案、B2B 平台企业页、百科词条、客户案例署名

### D-02 场景词被竞品占位
- **症状**：核心场景词搜索结果前列全是竞品，自己缺席
- **为什么扣分**：买家问 AI 的时候，答案里根本没有你
- **检测**：按行业画像的 `scenario_queries` 逐条检索
- **修复模板**：围绕每个场景词写 1 篇决策型长文（How to choose / A vs B / Cost of…），一稿五改分发 ≥3 处

### D-03 无百科词条占位
- **症状**：品牌在百科类站点无条目
- **为什么扣分**：百科是引擎做实体消歧的首选参考源，缺位 = 把解释权交出去
- **修复模板**：创建企业词条，引用官网 + 社媒 + 第三方报道作来源

### D-04 视频/图纸未结构化
- **症状**：有 YouTube 实拍与图纸库，但无 VideoObject / ImageObject 声明
- **为什么扣分**：多模态证据的引用权重在上升，但引擎不知道这些资产属于你
- **修复模板**：Top 20 视频补 VideoObject（含 transcript），图纸补 ImageObject

---

## E · 实体一致性

### E-01 多域名同 title 镜像 ★高频
- **症状**：`com / net / org` 三个域名 title 完全相同、内容同源
- **为什么扣分**：引擎做实体归并时权重被切成三份，且无法判断哪个是权威主站
- **检测**：`mirror_domains`（脚本，仅统计 `same_title == true`）
- **修复模板**：确立唯一主站 → 其余 301 或 canonical 指向主站；确需保留的分站用 `parentOrganization` 明确层级

### E-02 NAP 双地址并存
- **症状**：联系页同时挂着两个不同地址
- **为什么扣分**：NAP 不一致让引擎在"某地有哪些厂家"类问题上犹豫，本地问答失去引用资格
- **检测**：`nap_conflicts`（脚本，已做同街道去重）
- **修复模板**：保留营业执照地址作为唯一 NAP；工厂地址可作为附加 `address` 节点或 `department`

### E-03 公司名多种写法
- **症状**：`Southern Machinery` / `... Co.,Ltd` / `... Co. Limited` / `Shenzhen ... Co., Ltd.` 并存
- **为什么扣分**：实体归并困难，品牌词召回分散
- **检测**：`name_variants`（脚本，已做 Ltd/Limited/标点归一化）
- **修复模板**：确定唯一法定名称，其余写入 `alternateName`

### E-04 品牌别名未声明
- **症状**："Southern Machinery" 与 "SMThelp" 两个叫法无关联声明
- **为什么扣分**：引擎可能当成两个公司
- **修复模板**：Organization 的 `alternateName` 数组

### E-05 多名销售联系方式并列
- **症状**：10 位销售各自邮箱手机平铺，无统一主 NAP
- **为什么扣分**：引擎提取联系方式时极易取错，且稀释主 NAP 信号
- **修复模板**：只展示 1 个主电话 + 1 个主邮箱；销售改按区域聚合展示

### E-06 同名公司干扰
- **症状**：存在同名或近名公司（参考案例：青玥 AI 撞上"北京青玥教育"）
- **为什么扣分**：实体消歧时品牌极可能被归错档案
- **修复模板**：全网统一用"品牌 + 地域"发表内容；title/description 强化地域限定
  ⚠️ 涉商标在先注册时，建议咨询专业代理机构，本 skill 不提供法律意见
