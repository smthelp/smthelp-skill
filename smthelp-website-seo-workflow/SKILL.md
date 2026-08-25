---
name: smthelp-website-seo-workflow
description: "Southern Machinery (smthelp.v5.viwolf.cn) 后台SEO产品优化工作流 — 从登录到完成单个产品SEO字段更新的完整流程，含分页、字段定位、session管理、SEO内容规范。"
whenToUse: "smthelp SEO优化，网站后台产品编辑，THT产品SEO，smthelp.v5.viwolf.cn admin"
metadata:
  source: hermes
  origin: "sales-engineering/smthelp-website-seo-workflow"
---
# smthelp.v5.viwolf.cn SEO优化工作流

## 站点信息
- **域名**: smthelp.v5.viwolf.cn
- **后台入口**: http://smthelp.v5.viwolf.cn/admin888
- **登录凭证**: admin / admin888
- **语言模式**: `lang=en`（英文后台）

---

## 一、登录与Session管理

### 登录流程
1. 导航到 `http://smthelp.v5.viwolf.cn/admin888/login.html`
2. 填入用户名 `admin`，密码 `admin888`
3. 点击登录按钮
4. 登录后重定向到管理首页

### Session有效期
- Session会过期（大约几分钟后无操作）
- 过期后直接导航到产品编辑URL会跳转到 `login.html`
- **处理方式**: 每次进入编辑页面时检查URL是否为login页面，如果是则重新登录

---

## 二、产品列表与分页

### THT产品分类
- **URL**: `http://smthelp.v5.viwolf.cn/admin888/manage.shop.php?action=def&listid=18407&lang=en`
- 共35个产品，分2页展示（每页20/15）

### 分页参数
- 第1页: 默认URL
- 第2页: `http://smthelp.v5.viwolf.cn/admin888/manage.shop.php?pid=2&modelid=8&lang=en&rn=20&listid=18407`
- **注意**: 分页通过JS实现，在console中执行以下JS可找到分页链接：
  ```javascript
  const links = document.querySelectorAll('a');
  const pageLinks = [];
  links.forEach(a => {
    const t = a.innerText?.trim();
    if (t === '2' || t === 'Next' || t === '»') pageLinks.push({text: t, href: a.href});
  });
  JSON.stringify(pageLinks);
  ```

---

## 三、产品编辑页面

### 编辑页面URL格式
```
http://smthelp.v5.viwolf.cn/admin888/manage.shop.php?action=edt&listid=18407&modelid=8&pid=1&productid={PRODUCT_ID}&lang=en
```

参数说明：
- `listid=18407` — THT machine分类
- `modelid=8` — 产品模型ID
- `pid=1` — 第1页（pid=2为第2页产品）
- `productid` — 产品ID

### SEO字段定位（编辑页面Tab: 文本）
表单字段顺序（第1次快照后确认）：
| 字段 | Element Ref | 说明 |
|---|---|---|
| 产品名称 | e24 (textbox nth=1) | 产品URL标识 |
| **SEO标题** | e25 (textbox nth=2) | 需优化 |
| **SEO关键词** | e26 (textbox nth=3) | 需优化 |
| **SEO描述** | e27 (textbox nth=4) | 需优化 |

**重要**: refs在每次页面加载后都会变化，**必须先执行 `browser_snapshot` 获取当前refs**，再进行 `browser_click` 和 `browser_type` 操作。

### 表单填写步骤
1. `browser_click` 点击目标字段（聚焦）
2. `browser_press` 按 `Meta+a` 全选
3. `browser_type` 输入新内容

### 保存
- 找到"保存"按钮（通常为 `e33`）并点击
- 保存成功后页面跳转回产品列表

---

## 四、SEO内容规范

### 标题（SEO Title）
格式: `产品型号 + 产品类型 + | 补充说明 - Southern Machinery`
示例: `S-7000D Tact Switch Inserter | High-Speed THT Pushbutton Insertion Machine - Southern Machinery`

要求:
- 60字符以内
- 包含产品型号（S-7000D）和产品类型（tact switch inserter）
- 包含品牌标识（Southern Machinery）
- 包含差异化关键词（high-speed, precision等）

### 关键词（SEO Keywords）
格式: 逗号分隔的关键词列表
要求:
- 第1个关键词必须是产品核心词（tact switch inserter）
- 必须包含产品型号（S-7000D）
- 包含长尾词（through-hole switch insertion machine）
- 包含行业词（THT insertion equipment, electronic manufacturing automation）
- 包含应用词（pushbutton switch, panel switch）
- 避免泛泛的"machine"或"auto insertion machine"

### 描述（SEO Description）
格式: 2-3句话，150-200字符
内容要求:
1. 第1句: 产品名称 + 功能（automates...）
2. 第2句: 目标市场和应用场景（Designed for EMS factories producing...）
3. 第3句: 核心优势和品牌背书（Southern Machinery, CE certified, Get a quote）
必须避免:
- 泛泛的"high quality, competitive price"
- 产品类型错误（如把tact switch写成odd-form insertion）
- 与实际产品无关的描述

---

## 五、THT产品分类清单（listid=18407）

### 第1页产品（20个）
| 产品ID | 产品名称 | 优先级 |
|---|---|---|
| 136440 | S-7000D Tact Switch Inserter | ✅ 已完成 |
| 135444 | S7020 Series PIN Eyelet Terminal Insertion Machine | 待处理 |
| 135614 | S4000 Axial Auto Insertion Machine | 待处理 |
| 135493 | S-3000 PCB DIP Assembly Radial Insertion Machine | 待处理 |
| 137614 | S-4000 Axial Inserter Machine | 待处理 |
| 137600 | S-4000 Axial Inserter Machine | 待处理 |
| 135427 | S-4000H Jumper Wire Inserter Machine | 待处理 |
| 135426 | S-3000 Radial Insertion Machine | 待处理 |
| 135425 | S-3010B Radial Insertion Machine (Offline) | 待处理 |
| 135425 | S-70LD Odd Form Insertion Machine | ⭐ 旗舰款 |
| 135443 | S-7000I Fuse Holder Insertion Machine | 待处理 |
| 137636 | S-7000T Terminal Insertion Machine | 待处理 |
| 135618 | S-7000T Terminal Insertion Machine | 待处理 |
| 135440 | S-7000 Pin Insertion Machine | 待处理 |
| 137665 | Auto Lead Cutter Machine for THT PCB Assembly | 待处理 |
| 137657 | S7900 ODD FORM INSERT MACHINE | 待处理 |
| 135616 | S-WS450 Wave Soldering Machine | 待处理 |
| 135442 | S-7000T Terminal Insertion Machine | 待处理 |
| 135441 | S-7000E Eyelet Pin Inserter | 待处理 |
| 135384 | S-680 Automatic Scrap Tape Cutting Machine | 待处理 |

### 第2页产品（15个）
| 产品ID | 产品名称 |
|---|---|
| 134747 | THT Component Cutting&Bending Machine |
| 134727 | S-WS350B Lead-free Dual Wave Soldering Machine |
| 134724 | 30 Years THT Field Experience (Service) |
| 134707 | Auto Lead Cutter Machine for THT PCB Assembly |
| 134705 | S-WS450 Wave Soldering Machine |
| 134691 | S-1000 Sequencer Machine |
| 134600 | PAC SCI Servo Amplifiers (Service) |
| 134596 | S-7000 Full Automatic Pin Insertion Machine |
| 134579 | S-7000 Odd Form Inserter |
| 134541 | Odd Form Component Eyelet Pin Auto Insertion Machine S-7000E |
| 134538 | S-WS250 Wave Soldering Machine |
| 134537 | S7000 Odd Form Insertion Machine |
| 134536 | PCB Design Guideline (Service) |
| 134535 | S-3000 Radial Auto Insertion Machine |
| 134528 | S4000 Axial Auto Insertion Machine |

---

## 六、其他分类

| 分类 | listid | 说明 |
|---|---|---|
| Wave soldering machine | 19282 | 波峰焊产品 |
| Blog (THT Chatbots) | 19280 | ⚠️ 后台显示"THT Chatbots"但实际为博客文章区，已有1篇发布（S-7000D Tact Switch Inserter, productid=137666） |

---

## 七、已知问题

1. **产品名称包含 "_presentation"**: 部分产品URL后缀有 `_presentation`，SEO标题应去除此后缀
2. **关键词错误**: 原SEO关键词经常使用"odd form component insertion machine"等错误产品类型词，需根据实际产品类型更正
3. **产品内容描述错误**: 描述中经常出现张冠李戴（如S7020的描述中出现tact switch）
4. **Blog分类名称**: listid=19280 后台显示"THT Chatbots"，但实际为博客文章，不是聊天机器人，不要被误导

---

## 八、B2B SEO内容输出模板（定期执行cron任务时使用）

> 触发词: "SEO content generator" / "B2B blog outline" / "每周SEO报告"

### 标准输出结构
每个Outline包含以下章节：
1. **Primary Target Keyword** + secondary keywords
2. **Publication:** 目标平台 (SMThelp.com Blog → LinkedIn → Alibaba)
3. **Linked Equipment:** Southern Machinery具体型号
4. **I–VI 结构:** HOOK → PROBLEM → TECHNICAL DEEP-DIVE → ROI CALCULATION → BRIDGE TO SM → CTA
5. **IMAGE REQUIREMENTS (MINIMUM 4):** 3D工厂布局（MANDATORY）+ 机器照片 + 图表 + 信息图
6. **ROI公式块:** 包含计算示例和 payback period
7. **INTERNAL LINKS:** 各Equipment Page + Homepage CTA

### 格式要求
- B2B, SMT, THT, ROI, MIC, EMS, ODM **全部大写**
- 数字精确（CPH, 投资金额, 回本周期）
- Homepage CTA统一: `[www.SMThelp.com](http://www.SMThelp.com)`
- 每篇目标字数: ≥2,000 words
- 每篇必须包含: 3D产线布局图（MANDATORY）、ROI计算公式、Lead-generation CTA

### 历史输出记录
| 周次 | Outline主题 | 状态 |
|------|------------|------|
| Week 26 (Jun 12) | Odd-Form Insertion ROI | 输出完成 |
| Week 27 (Jun 26) | Active Clinching / AGV Board Handling / Line Commissioning | 输出完成 |

---

*工作流版本: 2026-06-26 | 更新: blog分类状态纠正 + B2B SEO内容输出模板*

## §2 — smthelp-seo-workflow (Legacy Notes)

> This section consolidated from `smthelp-seo-workflow` skill. Full reference at `references/smthelp-seo-workflow-notes.md`.

The `smthelp-seo-workflow` skill covered the same workflow as §1 above. Key additions from that skill:

### Alternative URL Patterns (from smthelp-seo-workflow)
- Product list: `http://smthelp.v5.viwolf.cn/admin888/manage.shop.php?listid=18407&modelid=8&lang=en`
- Product edit: `http://smthelp.v5.viwolf.cn/admin888/manage.shop.php?action=edt&listid=18407&modelid=8&pid=1&productid={PID}&lang=en`
- Product save: `http://smthelp.v5.viwolf.cn/admin888/manage.shop.php?action=edt&listid=18407&modelid=8&pid=1&productid={PID}&submit=1&lang=en`

### SEO Optimization Steps (condensed from smthelp-seo-workflow)
1. **Login** — navigate to admin URL, type credentials, click login
2. **Enter product list** — navigate to manage.shop.php with listid=18407
3. **Locate product** — use `browser_console` to extract all product rows, find target productid
4. **Enter edit page** — navigate to edit URL with productid
5. **Clear existing SEO fields** — use browser_console to clear
6. **Write SEO title** — format: `产品型号 | 产品名称 | 核心卖点 - Southern Machinery`
7. **Write SEO keywords** — comma-separated, 8-15 precise long-tail keywords
8. **Write SEO description** — 150-180 chars
9. **Save** — click save button

### Known Issues (from smthelp-seo-workflow)
- Session expires ~30 min; re-login if navigating to edit page redirects to login
- Product edit page requires `lang=en` for English interface
- Pagination uses JS click, not navigate (dynamic load)
- 2nd page productids need re-extraction via JS

For complete product list with productids and current status, see §1 above.
