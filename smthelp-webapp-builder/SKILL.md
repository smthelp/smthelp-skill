---
name: smthelp-webapp-builder
description: 为 Southern Machinery 构建并部署零依赖、免构建的对外网页应用/落地页——多文件 hash 路由 SPA（部署成站）或单文件构建式 HTML（当邮件附件）。统一 SMThelp 品牌设计系统、GEO 结构化、Chatwoot 客服、明暗主题与 7 语言 i18n。当需要做产品落地页、设计指引站、DFM 工具页、内容型 Web App、把资料转成可分享网页，或客户要求「一个 .html 附件」时使用。
triggers:
  - 做一个网页应用
  - 创建落地页
  - 单HTML文件
  - 单个html
  - Web App
  - landing page
  - 静态站点
  - 推送到 GitHub
  - GitHub Pages
  - 设计指引站
  - DFM 工具页
  - 加 Chatwoot 客服
  - 品牌网页
  - 多语言落地页
  - 暗黑模式切换
category: 外贸营销 / 前端交付
version: 1.3.0
agent_created: true
author: Atlas
---

# SMThelp 对外 Web App 构建与部署

## 何时用

需要把 Southern Machinery 的**技术资料 / 产品线 / 工具**变成客户可直接访问的网页时。典型：设计指引站、产品落地页、DFM 自查工具、ROI 计算器、案例展示页、内容型站点。

**不适用**：需要后端/数据库/登录的应用（本 skill 只做静态站）；需要视频或 3D 生成的需求（产品不支持）。

---

## 一、架构决策（默认选择，不要推翻）

> **先选变体**：部署成站 → 本节的**多文件**架构；客户要「一个 .html 附件」→ 跳 **§十一 单文件变体**。
> 两者不通用，选错会导致返工（单文件塞不下多文件的分层，多文件也不需要构建脚本）。

**零依赖 + 免构建 + Hash 路由 SPA**。理由：

1. 目标宿主是 **GitHub Pages** —— 纯静态，无 Node 运行时
2. Jason 需要能**随时用文本编辑器改**，不能有构建链
3. Hash 路由（`#/route`）无需服务端 rewrite，Pages 直接可用
4. 产物控制在 4~5 个文件，便于审计与推送

**目录结构（固定）：**
```
<project>/
├── index.html              # 标记 + 静态路由内容 + meta/JSON-LD + Chatwoot
├── assets/
│   ├── css/style.css       # 品牌设计系统
│   └── js/
│       ├── data.js         # 内容层：IMG / VIDEOS / CATALOG / BLOGS …
│       └── app.js          # 行为层：路由 / 渲染 / 计算
├── .nojekyll               # 必须，避免 Pages 用 Jekyll 处理
└── README.md
```

**分层铁律：`data.js` 只放内容，`app.js` 只放行为。** 加内容只改 `data.js`，绝不碰路由逻辑。

**路由模式：**
```js
var ROUTES = ["guide","dfm","case","survey","blog","post","media","tools"];
window.addEventListener("hashchange", route);
function route(){ var n=(location.hash.replace(/^#\/?/,"")||"guide").split("/")[0];
  if(ROUTES.indexOf(n)===-1) n="guide"; /* show/hide sections + nav active */ }
```

---

## 二、品牌设计系统（token 固定，勿自创）

| Token | 值 | 用途 |
|---|---|---|
| 主色 | `#1C64F2` | 按钮、链接、强调 |
| 深海军蓝 | `#0b132b` | 页脚、深色区块 |
| 琥珀 | `#f59e0b` | 高亮、数据强调 |
| WhatsApp 绿 | `#25D366` | WhatsApp 按钮 |
| 字体 | `Inter` | 全局 |

- **Logo**：`https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`
  - 顶栏：`<header class="topbar">` → 左上角 `a.brand > img`
  - 页脚：同一 URL + `style="filter:brightness(0) invert(1)"` 转白
  - 同时用于 `og:image` 与 `rel="icon"`
- **页脚必备**：5 个社交链接 + 素材库文案 + 邮箱 + WhatsApp
  - LinkedIn 公司 `linkedin.com/company/smtmachine`
  - LinkedIn 个人 `linkedin.com/in/smtsupplier`
  - X `twitter.com/smtspecialist`
  - Facebook `facebook.com/autoinsertion`
  - YouTube `youtube.com/c/Smthelping`
  - 文案：`Browse our machine catalog at file.autoinsertion.com and find machine photos at ph.smthelp.com.`
  - `info@smthelp.com` · `https://wa.me/8613602562576`

参考实现（视觉基准）：`THT-Auto-Insertion-Machine-Solution-Landing.html`

---

## 三、可复用素材端点（直接取真实数据，不要编）

| 用途 | 端点 / 规律 |
|---|---|
| 图床检索 | `https://ph.smthelp.com/search/images?q=<关键词>`（Chevereto，返回真实图 URL） |
| YouTube 缩略图 | `https://i.ytimg.com/vi/{videoId}/hqdefault.jpg`（videoId **恒为 11 位**，务必断言） |
| 视频索引看板 | `https://file.autoinsertion.com/public/Southern-Machinery-YouTube-Video-Board.html` |
| 产品目录看板 | `https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html` |
| ROI 计算器 | `https://file.autoinsertion.com/public/Blog%20file/THT-Insertion-ROI-Calculator.xlsx` |
| 本地素材主库 | `F:\baidunetdiskworkspace\Through Hole Technology\`（见工作区 MEMORY.md §六 检索表） |

**验证图片 URL 可用性**：`curl --noproxy '*' -o f -w "%{http_code} %{content_type}" <url>` —— **必须带 `--noproxy '*'`**（见 §六 坑 1）。

---

## 四、Chatwoot 客服（固定片段）

放在 `index.html` **`</body>` 前**：

```html
<script>
window.chatwootSettings = {"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"};
(function(d,t) {
// Protocol-adaptive: 浏览器会拦截 https 页面上的 http:// 脚本（mixed content）。
var BASE_URL=(location.protocol==="https:"?"https://":"http://")+"chat.smthelp.com";
var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
g.src=BASE_URL+"/packs/js/sdk.js";
g.async = true;
s.parentNode.insertBefore(g,s);
g.onload=function(){ window.chatwootSDK.run({ websiteToken: 'saMcpgSupcmd1VQwytgPLfbK', baseUrl: BASE_URL }) }
})(document,"script");
</script>
```

**关键：BASE_URL 必须协议自适应。** Jason 习惯指定 `http://chat.smthelp.com`，但 GitHub Pages 是 HTTPS，硬编码 `http://` 会被浏览器作为 active mixed content **直接拦截**，客服静默失效。实测 `https://chat.smthelp.com/packs/js/sdk.js` → 200，`http://` → 301，故 https 可用。

再在 CSS 末尾加定位兜底：
```css
.woot-widget-holder, .woot--bubble-holder {
  position: fixed !important; bottom: 20px !important; right: 20px !important;
  left: auto !important; z-index: 2147483000 !important;
}
```
因为 hash 路由是单页，脚本只加载一次即覆盖所有"页面"。

---

## 五、GEO 与文案规范

> 完整方法见 `smthelp-geo-audit` 技能（六维评分卡 + 审计脚本 + 修复模板 + 13 条坑）。
> 这里只列**建站时就要做掉**的部分。

- **JSON-LD**：至少一个 `@graph`，含 `Organization`（`foundingDate` / `url` / `sameAs` / `address` / `contactPoint`）
  + `TechArticle`（`headline` / `about` / `inLanguage` / `datePublished` / `dateModified` / `mainEntityOfPage`）。
  只放一个裸 `TechArticle` 会让引擎无处挂靠事实，白丢实体分
- **`meta`**：`rel=canonical`（**必须指向真实已部署地址**）/ `og:title` / `og:description` / `og:image` /
  `og:url` / `og:site_name` / `twitter:card` 齐全
- **爬虫三件套**：`robots.txt`（显式放行 GPTBot / ClaudeBot / PerplexityBot / CCBot 等 + 声明 sitemap）、
  `sitemap.xml`、`llms.txt`（结构化事实清单，不是 slogan）
- **写作**：清晰断言 + 具体数字 + 结构化事实（可被引用）；用 ROI 语言
- **事实纪律**：所有参数必须可追溯到库内文件，**查不到就说"库里没有"，禁止用模型记忆填参数**
- **内容型文章**：可采用「钩子 → 问题 → 机制 → 载体 → 强化 → 行动」六段结构作为**内部写作纪律**，但**这些阶段名不得出现在对外标题中**（Jason 明确禁止标题含 hook / diagnosis / framework / vehicle / loop / CTA 等词）
- 对外发布前须 Jason 确认

### 5.1 内容型 SPA 必须做静态化（否则 GEO 直接腰斩）

Hash 路由 SPA 的内容默认只存在于 JS 里，而 **GPTBot / ClaudeBot / PerplexityBot / CCBot 基本不执行 JS**。
建站时就要把长文正文渲染成静态 HTML，别等审计时再返工。

**四条硬规则：**

1. **`<noscript>` 兜底是前提，不是可选项。** 路由容器默认 `display:none`，不执行 JS 时整页为空；
   把内容写进隐藏容器＝隐藏文本（cloaking），比不加更糟。必须补：
   `<noscript><style>.route{display:block !important}</style></noscript>`
2. **静态内容插在 JS 宿主元素的兄弟位置**，不要动 JS 渲染的那个容器（例：`#route-blog` 内
   `<div id="blog-grid">` 是 JS 宿主，静态文章插它之后）。这样**原渲染器与路由逻辑零改动**。
3. **转义策略逐字复刻原渲染器。** 数据层的段落/列表含 `<strong>` 等内联标记时，
   这些字段必须保持原样（原渲染器用 `innerHTML`），只有标题/代码/表格单元转义。
   「为了安全」全量转义会把 `&lt;strong&gt;` 字面量发给每个读者。
4. **加漂移断言。** 静态副本是构建时快照，数据源改了没重跑就会不一致。
   断言静态标题集合与 JS 已渲染 DOM 的标题集合完全相等（标题 + id 双重比对）。

**生成器**：独立脚本、幂等（先剥离旧注入再重新注入）、放构建目录不放仓库。
参考实现 `_build/tht-design-guide/inject-static-articles.js`。

### 5.2 标题层级

路由标题用 `h2`，列表项/文章标题用 `h3`，文章内章节用 `h4`；全站只保留一个 `h1`（首页主标题）。
不要在内容区用 `h1` 抢标题——层级跳级和重复 `h1` 都会被扣分。

### 5.3 ⚠️ 结构化数据必须有可见对应内容（否则是隐形标记 + 无效断言）

**规则：凡是写进 JSON-LD 的问答/评分/面包屑，页面上必须有用户可见的同一份内容。**

本次真实事故：S-7000 单文件页把 6 组 FAQ 问答**只**写进了 `FAQPage` 结构化数据，
页面正文里一个字都没有。后果：

- Google 的结构化数据政策要求 FAQ 标记与可见内容一致 → **不会展示，且可能被判为垃圾标记**
- AI 爬虫（GPTBot / ClaudeBot / PerplexityBot）会**交叉核对**结构化数据与渲染文本，不一致直接降低信任
- 等于**主动向生成式引擎提交了一份不可核实的声明**，与 GEO 目标背道而驰

**为什么没被拦住 —— 无效断言的典型形态：**

```python
# ❌ 只检查结构，不检查可见性。给了虚假的通过。
check("FAQPage has >= 5 questions", len(faq["mainEntity"]) >= 5)
```

这个断言永远为真，无论页面上有没有 FAQ。**断言必须能失败**——
写完立刻做反证测试（见下）。

**正确做法 —— 收敛为单一数据源：**

1. 正文新增 `#faq` 区块，用 `<details>/<summary>` 承载（可折叠、可被爬虫读取、无需 JS）
2. 问答文本**只存在一处**：词典的 `faq_q1..q6` / `faq_a1..a6`
3. `build.py` 的 JSON-LD **从同一份字典取值**（`en["faq_q%d" % i]`），不另写一份英文
4. 加断言：**每条 JSON-LD 问答都能在静态 HTML 中检索到**

```python
# ✅ 能失败，才叫断言
vis_text = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)   # 排除 JSON-LD 自身
vis_text = re.sub(r'<[^>]+>', ' ', vis_text)
vis_text = re.sub(r'\s+', ' ', vis_text)
q_missing = [q["name"] for q in faq["mainEntity"] if q["name"] not in vis_text]
check("every FAQPage question is visible in the static page", not q_missing, str(q_missing))
```

**反证测试（必做）**：把该区块从成品里正则删掉，断言应当**失败**；不失败说明断言是空的。

```python
broken = re.sub(r'<section class="alt" id="faq">.*?</section>', '', html, flags=re.S)
assert not all(q in visible(broken) for q in questions)   # 必须成立
```

**推论**：任何新增的结构化数据类型（HowTo / Review / BreadcrumbList / VideoObject）
都要先问一句「这份内容在页面上看得见吗」。看不见就不要写。

### 5.4 插入区块必须同步重排可见编号

页面 kicker 常写成 `01 — Why it matters` … `11 — Next step`。
新增区块后若忘记重排，会出现**重号**（本次 FAQ 插入后 CTA 仍是 `10 — Next step`）。
→ 加断言守住：编号连续 + DOM 顺序与编号一致。

```python
SECTION_ORDER = ["why","line","spec","hand","thr","roi","svc","vid","dl","faq","cta"]
SECTION_DOM_ID = {"spec":"s7000","hand":"handling","thr":"throughput",
                  "svc":"service","vid":"videos","dl":"downloads","cta":"contact"}
sec_nums = [int(re.match(r"^(\d\d)\s*—", dicts["en"]["%s_kick" % k]).group(1)) for k in SECTION_ORDER]
check("section numbers are 01..11 with no gap", sec_nums == list(range(1, 12)), str(sec_nums))
sec_pos = [html.find('id="%s"' % SECTION_DOM_ID[s]) for s in SECTION_ORDER]
check("sections in DOM order", all(p > 0 for p in sec_pos) and sec_pos == sorted(sec_pos))
```

⚠️ kicker 的键名**不等于** section 的 id（`spec`→`#s7000`、`cta`→`#contact`、`dl`→`#downloads`）。
直接拿键名去 `find` 会得到 `-1`，断言会因为错误的原因失败。

---

## 六、本机环境坑（踩过的，必读）

1. **`http_proxy` 拦截 loopback → 本地验证全部假失败。**
   本机 `http_proxy=http://127.0.0.1:54687`，curl 请求 `127.0.0.1:<port>` 会被代理返回 **502 / 94 字节错误页**，看起来像服务器坏了，其实是代理。
   → **一律加 `--noproxy '*'`**。

2. **后台 `python -m http.server` 会随父任务结束而死亡。**
   一次探测能通，下一批就 502 / connection refused。
   → **结论：优先做静态文件验证，不要为本地预览反复起服务。** 需要预览时用 `present_files` 直接打开 `index.html`（相对路径可正常加载，仅 Chatwoot 需 HTTP origin）。

3. **验证 JS 内容的作用域陷阱。**
   - 只想取数据（`BLOGS` 等）：用 `new Function(src + '\nreturn {BLOGS,VIDEOS,CATALOG,IMG};')()`。
   - 要跑**完整运行时**（jsdom 端到端）：**必须把所有脚本拼成一个字符串、只 `eval` 一次**。
     原因：站点是 classic `<script>`，顶层 `const` 落在**全局词法环境**，后续脚本可见；而 jsdom 的
     `window.eval()` 是**间接 eval**，每次调用都新建声明式环境 —— 逐个 `eval` 会让 `const BLOGS`
     对 `app.js` 不可见，报 `ReferenceError: BLOGS is not defined`。
     **这是测试脚手架假象，不是站点 bug**（浏览器里正常）。拼成一个 eval 即复现浏览器语义。
   - 反例教训：该错误在 `DOMContentLoaded` 监听器里抛出，会**中断 BOOT 后续所有语句**
     （`route()`、`addEventListener("sm:langchange", ...)` 全都没注册），表现为「切换语言后
     部分区块不翻译」——**看起来像功能 bug，其实是测试脚手架没跑完**。
     → 给 jsdom 挂 `VirtualConsole` 的 `jsdomError`，把未捕获异常计入失败，否则错误被静默吞掉。

3.1 **⚠️ 绝不要对同一个文件并行发多个 Edit 调用。**
   Edit 是「读-改-写」，并行时相互覆盖，**只有最后一个写入生效**，而且**每个调用都会返回成功**。
   本次实测：7 个并行 Edit 改同一文件，只有 1 个真正落盘。
   → 同一文件的多处替换，用**一个脚本一次读完-改完-写完**（见 `_build/.../patch-app-i18n.js`），
     或改为串行调用。改完必须 `grep` 复核实际落盘内容，不能只信工具返回的 success。

4. **禁词审查必须用 `\b` 词边界。**
   裸 grep `cta` 会误命中 `re`**`cta`**`ngular`；裸 grep `loop` 会误命中 `loopback`。
   → 用 `grep -oiE '\b(hook|diagnosis|framework|vehicle|loop|cta)\b'`。

5. **`.xls` 是 OLE 二进制，sheet-agent 打不开**（报 `UNOPENABLE_LOCAL_PATH`）。
   → 用 venv `C:\Users\Admin\.workbuddy-ai\binaries\python\envs\default` + `xlrd` 读。

6. **PDF 文本提取**：用 PyMuPDF（`fitz`），100 页约 100K 字符，足够做规则型站点。

7. **路径**：用 Windows 风格 + 双引号（目录名含空格：`Through Hole Technology`）。`/tmp` 在本环境不可用。

8. **⚠️ `curl -o /dev/null` 在 Windows 原生 curl 下会失败（exit 23）。**
   本机 `curl` 解析到 `C:\Windows\System32\curl.exe`，它打不开 `/dev/null`（那是 Git Bash 的模拟），
   于是**响应体写失败 → 非零退出**。
   → 后果：任何「探测线上是否可达」的脚本都会把成功误报为失败（`unreachable`），
     看起来像网络问题，实际是输出重定向。
   → 解法：**`-o` 指向真实临时文件**（`os.tmpdir()`）。
   → 另一个细节：curl 可能**在打印完状态码之后**才非零退出，所以 `execFileSync` 抛错时
     仍要读取异常对象上的 `stdout`，否则状态码被丢掉。
   完整封装见 `THT_design_Guideline/tools/geo-check.js` 的 `httpCode()`。

9. **⚠️ 本机 `nslookup` / 普通 DNS 查询返回假 IP，不能用来判断域名是否存在。**
   本机代理软件（Clash 类）以 fake-ip 模式拦截 DNS，对任意域名都返回 `198.18.x.x`
   （RFC 2544 保留段，公网不可路由），且不同子域返回**连续递增**的假 IP ——
   看起来像解析成功，实际是假的。曾因此误判一个 NXDOMAIN 的子域「已解析」。
   → **一律走 DoH**：
   ```bash
   curl -sS -H "accept: application/dns-json" \
     "https://cloudflare-dns.com/dns-query?name=<域名>&type=<A|CNAME|NS>"
   # Status: 0 = 有记录（看 Answer），Status: 3 = NXDOMAIN（不存在）
   ```
   查 NS 还能顺带确认域名是否托管在 Cloudflare（返回 `*.ns.cloudflare.com`）。

10. **⚠️ 外链实测必须带「预期噪声」白名单，否则真信号被淹没。**
    交付前把页面里所有 `href`/`src` 抽出来跑一遍 HTTP 检查，但**四类非 200 是正常的**，
    不做白名单会报出一堆假故障，反而让人忽略真问题：

    | 噪声 | 表现 | 原因 |
    |---|---|---|
    | `preconnect` 裸域名 | `fonts.googleapis.com` → 404 | 预连接提示，本就没有文档根 |
    | JS 模板字符串 | `i.ytimg.com/vi/'+v.id+'/...` → 404 | 正则抽到了拼接前的源码 |
    | canonical 指向的未部署路径 | 自家域名 → 404/URLError | 页面还没上线到该路径 |
    | Facebook / LinkedIn | 400 / 999 | 反爬，非浏览器客户端一律拒 |

    ```python
    IGNORE = ("https://fonts.googleapis.com", "https://fonts.gstatic.com", "'+v.id+'",
              "https://smthelp.com/", "https://www.facebook.com/")
    ```
    判据：**修掉白名单之外的全部非 200**。本次 51 条外链 → 12 条预期噪声 → **0 条真故障**。

11. **⚠️ 单次 `URLError` ≠ 死链，必须复测再判死。**
    实测：跳线供料器图片首轮报 `URLError`，单独 `curl` 复测为 **200** —— 是网络抖动。
    并发检查（`ThreadPoolExecutor`）更容易误报。
    → **可疑链接单独复测一次再下结论**，否则会白改一个本来正确的 URL。

12. **⚠️ 绝不「顺手修正」一个看起来可疑的 ID / URL —— 改完必须重测。**
    实测踩坑：视频 ID `o1WeoMJFo8E` 的缩略图能取到（200），我判断那个 `1` 是笔误，
    改成 `oWeoMJFo8E` → **404**，把本来正确的改坏了。
    **YouTube 的 11 位 ID 是不透明字符串，不能靠「看起来像笔误」推断。**
    → 任何 ID/URL 改动，改完立刻 `curl -o /dev/null -w '%{http_code}'` 复测；
      批量改则重跑 `checklinks.py`。

13. **⚠️ 响应式断点必须「实测」，不能「估算」；而且更宽不一定更宽松。**
    本次实测数据（导航 8 项，`navNeed=749px`）：

    | 视口 | 可用 | 余量 | 状态 |
    |---|---|---|---|
    | 1240 | 880 | 636 | 折叠为汉堡 |
    | 1260 | 1006 | 257 | 单行 |
    | 1281 | 1027 | 278 | 单行 |
    | 1320 | 1066 | 317 | 单行 |
    | 1400 | 897 | **148** | 单行（**余量反而变小**）|
    | 1600 | 897 | **148** | 单行 |

    原因：`.brand .bs`（品牌标语）在 **≥1400px 才显示**，一出现就吃掉 169px；
    同时 `.wrap.hd{max-width:1360px}` 封顶了头部宽度。
    → **结论：断点要取「实测余量最小」的那个宽度来验，而不是取最窄或最宽。**
    → 用 `probe2.js`（CDP）把 nav 临时设成 `width:max-content` 量出 `navNeed`，
      再和 `容器宽 - brand宽 - hctl宽 - gap` 比。**不要靠肉眼或按字符数猜。**

    **⚠️ 而且必须逐语言测 —— 只测英文会把最坏情况低估一个数量级。**
    本次（SF320AT 单文件页）同一段导航，7 门语言实测：

    | 语言 | `navNeed` | 说明 |
    |---|---|---|
    | **pt** | **777px** | 最宽 —— 断点要按它定 |
    | fr | 700px | |
    | es | 697px | |
    | ru | 694px | |
    | en | 646px | |
    | ar | 635px | |
    | zh | 586px | 最窄 |

    只测英文（646px）定的 1240px 断点，在葡语下标语一显示余量只剩 **26px** ——
    一次字体回退就换行，导航压到 topbar 上。
    → 修法是**压缩标语预算**（es 389→302px、pt 393→307px、fr 407→314px），
      最坏余量 26 → **112px**；**不是**把断点一味推高（推高会牺牲平板宽度）。
    → 度量口径：`room = 头部容器宽 − padding − brand宽 − 控件宽 − 2×gap`，
      `navNeed` 取**最宽那门语言**。
    → 改过任何一句标语、语言菜单项、或品牌副标题，**都要重跑一次逐语言实测**。

14. **⚠️ CDP 截图取景有两个必踩的坑。**
    - `deviceScaleFactor` 与 `clip.scale` **会相乘**：设 `deviceScaleFactor:2` 再给 `clip.scale:0.5`
      不是「缩略图」，而是把裁剪区域放大成 2 倍坐标系后取 0.5 → 图幅尺寸翻倍、内容极小。
      → **固定 `deviceScaleFactor:1`，只用 `clip.scale` 控缩放。**
    - `captureBeyondViewport:true` **不会触发** `loading="lazy"`：离屏图片全部渲染为空占位框。
      → 截图前先 `document.querySelectorAll('img[loading="lazy"]').forEach(i=>i.loading='eager')`，
        逐段 `scrollTo` 走一遍，再 `await Promise.all([...document.images].filter(i=>!i.complete)...)`。
      → 自检：打印 `N images, M loaded`，**M 必须等于 N**。
    - `chrome --print-to-pdf` 恒按约 1080px 排版，**无视 `@page size`** → 不能用来验证桌面布局。
    - **不要从缩放后的截图里读数字。** 本次在 0.66 倍截图上把 `1,249,000` 看成 `1,248,000`、
      把 `1028` 看成 `1000`，白跑了一轮核对。**数值一律回到源文件或 DOM 里核**
      （`grep -o` 源 PDF 文本 / 读 `i18n/*.json`），截图只用来判断版式与可见性。

15. **⚠️ `iframe.src = ""` 不是「清空」，是「导航到本页」。**
    空字符串按**文档 base URL** 解析 → iframe 载入**它自己**。
    本次实测：视频弹窗关闭后 `resolvedSrcAfterClose` 等于页面自身的 file URL，
    即在一个 1000px 高的框里**重载整份 670KB 单文件**。
    截图完全看不出异常（框里就是同一张页面），**只有断言抓得到**。
    → **必须写 `about:blank`**：`frame.src = "about:blank"`。
    → 断言：`'frame.src="about:blank"' in html`。

16. **⚠️ 自指断言（「页面里不含 X」）必须先剥注释再判断，而剥离顺序有硬约束。**
    模板注释里常常正好写着这个坑的反例（本次就是），于是断言假失败。

    ```python
    code_only = re.sub(r"data:image/webp;base64,[A-Za-z0-9+/=]+", " ", html)  # ① base64 最先
    code_only = re.sub(r"<!--.*?-->", " ", code_only, flags=re.S)             # ② 再 HTML 注释
    code_only = re.sub(r"/\*.*?\*/", " ", code_only, flags=re.S)             # ③ 最后 JS 注释
    ```

    **① 必须最先**：`/*` 是合法的 base64 字符对，内联图片里会随机出现。
    若先剥 JS 注释，base64 里的一个 `/*` 会开启一段「幽灵注释」，
    一路吞掉**真实代码**，断言于是对着残缺文本下结论。

17. **⚠️ Python `urllib` 报 TLS 失败 ≠ 死链，裸域名（apex）尤其如此。**
    实测：`https://smthelp.com` 在 Python 下间歇性 `SSLV3_ALERT_HANDSHAKE_FAILURE`，
    curl 在 200/200/000 之间跳（`curl: (23)`），**而 Chrome 稳定 200**
    （301 → `https://www.smthelp.com/`，标题正常）。链路是活的，是 Python 的 TLS 栈不兼容。
    → **别「顺手修 URL」**（尤其 JSON-LD 的 `@id`，一改实体标识就变）。
      先换 Chrome/CDP 复测；确认是工具链问题就**白名单 + 写明理由**，不是改链接。

18. **⚠️ 网格里的图注会「各自贴图」，长短不一会错位。**
    两列图（`.fig2`）里放高度不同的图（本次 853 vs 784px 的卡尺照、
    471 vs 408px 宽的面板照），网格项被拉伸到行高，但图注紧跟图片 →
    **两张图的图注不在同一水平线**，看起来像排版坏了。

    ```css
    .fig2 figure{display:flex;flex-direction:column}
    .fig2 figcaption{margin-top:auto;padding-top:9px}   /* 推到格子底部对齐 */
    ```

    **混长宽比的一行要「信箱化」**（本次 440×669 竖图配 460×320 横图，行高被撑到 1703px）：

    ```css
    .fig2.eq figure img{height:400px;object-fit:contain;padding:10px}   /* 1703 → 1400px */
    ```

    ⚠️ 但**不要全局套用** `object-fit:contain` —— 证据区的卡尺读数照需要满宽，
    信箱化会把数字缩到看不清。只给「设备外观 / 图纸」那类行加 `.eq`。

19. **⚠️ 二进制 `.ppt`（OLE2）也能读，不必装 Office。**
    `python-pptx` 只吃 `.pptx`（OOXML zip），对 OLE2 直接抛错。走 `olefile` 手撕两个流：

    ```python
    ole = olefile.OleFileIO(path)
    # ① 图片：Pictures 流按文件签名扫描
    #    逐偏移找 b"\x89PNG\r\n\x1a\n" / b"\xff\xd8\xff"，读到下一个签名或流尾
    # ② 文字：PowerPoint Document 流按 8 字节记录头遍历
    #    recVer:4 | recInstance:12 | recType:2 | recLen:4   （小端）
    #    recVer == 0xF  → 容器记录，递归进去
    #    TextCharsAtom = 0x0FA0 (UTF-16LE)
    #    TextBytesAtom = 0x0FA8 (cp1252)
    #    CString       = 0x0FBA (UTF-16LE)
    ```

    → 抽出的文字**顺序不可靠**（按记录流序，不等于页序），需按 slide 容器边界或人工重排。
    → **图片往往比文字更有信息量**：本次 4 页 PPT 抽出 9 张图，全是实测数据截图
      （卡尺读数、面板显示、CAD 剖视），正文反而只有几行标题。

---

## 七、验证清单（交付前逐项跑）

```bash
cd <project>
# 1. JS 语法
node --check assets/js/app.js && node --check assets/js/data.js
# 2. 数据层断言
node -e 'const s=require("fs").readFileSync("assets/js/data.js","utf8");
const m=new Function(s+"\nreturn {IMG,VIDEOS,CATALOG,BLOGS};")();
console.log("BLOGS",m.BLOGS.length,"VIDEOS",m.VIDEOS.length,"CATALOG",m.CATALOG.length);
console.log("videoIds ok:",m.VIDEOS.every(v=>v.id.length===11));'
# 3. 禁词审查（词边界！）
grep -oiE '\b(hook|diagnosis|framework|vehicle|loop|cta)\b' index.html assets/css/style.css assets/js/*.js | wc -l
# 4. 品牌/联系项
grep -c "Southern-Machinery-logo-300x83.png" index.html
for u in linkedin.com/company/smtmachine linkedin.com/in/smtsupplier twitter.com/smtspecialist \
         facebook.com/autoinsertion youtube.com/c/Smthelping info@smthelp.com wa.me/8613602562576; do
  printf "%-38s %s\n" "$u" "$(grep -c "$u" index.html)"; done
# 5. Chatwoot
grep -c "saMcpgSupcmd1VQwytgPLfbK" index.html
# 6. 端到端（jsdom 来自托管 Node 工作区，必须设 NODE_PATH）
NODE_PATH="C:/Users/Admin/.workbuddy-ai/binaries/node/workspace/node_modules" node tools/test-dom.js
node tools/qa-i18n.js
node tools/geo-check.js . https://<域名>
```

**⚠️ `test-dom.js` 报 `Cannot find module 'jsdom'` 不是测试坏了，是漏了 `NODE_PATH`。**
该依赖装在托管 Node 工作区（`~/.workbuddy-ai/binaries/node/workspace/node_modules`），
项目本身**零依赖、无 `node_modules`**（这是刻意设计，不要为了跑测试而 `npm install`）。
只有 `test-dom.js` 需要它，`qa-i18n.js` / `geo-check.js` 都是零依赖。

**HTML 结构**：确认 `<html>/<head>/<body>` 各一对，路由 href 与 `ROUTES` 数组一致。

---

## 八、部署到 GitHub Pages

```bash
git clone https://github.com/<org>/<repo>.git <dir>
cd <dir>
# 复制 index.html / assets/ / .nojekyll / README.md
git add -A
git commit -m "..."
GIT_TERMINAL_PROMPT=0 git push origin main
```

然后 **Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**。

**推送前必查权限（否则白做）：**
```bash
GIT_TERMINAL_PROMPT=0 git push --dry-run origin main
```
若返回 `remote: Permission to <org>/<repo>.git denied to <account>` + **403**：
→ 本机缓存凭据属于 **`smthelping`**，对 `smthelp111/*` 的权限**因仓库而异**（有的有 `push: true`，有的只有 `pull`）。
→ **不要反复重试**，用凭据查 API 一次定位根因：
```bash
TOKEN=$(printf "protocol=https\nhost=github.com\n\n" | git credential fill | sed -n 's/^password=//p')
curl -s --noproxy '*' -H "Authorization: Bearer $TOKEN" https://api.github.com/repos/<owner>/<repo> | grep -A6 '"permissions"'
curl -s --noproxy '*' -H "Authorization: Bearer $TOKEN" https://api.github.com/user/repository_invitations
```
→ **判据要点：公开仓库对任何账号都返回 `pull: true`，`pull: true` 不能证明是协作者**；
   必须交叉看 `push` 字段 + 待接受邀请列表 + `affiliation=collaborator` 列表。**token 不要回显到输出。**
→ 若 `push: false` 且待接受邀请为 0：**「已邀请」多半没生效**（可能发给了另一个同名易混账号，见下）。
→ 三条出路：① 让 Jason 在 **Settings → Collaborators** 把 `smthelping` 角色确认为 **Write**（不是 Read），
   并在 `smthelping` 账号**接受邀请**；② **推自己的 fork**（见 §8.2，立即可行）；③ 提供有写权限账号的 PAT
   —— **token 仅用于本次 push，用完立即从 remote 抹除，不写入任何文件。**

> **⚠️ 三个极易混淆的账号**：`smthelp111`（User，仓库 owner）、`smthelping`（User，本机凭据身份）、
> `smthelp`（**User，不是组织**）。邀请时选错账号是 403 的常见原因。
> **另：`Fork` ≠ 授予写权限** —— 用户以为「已邀请」时，往往只是把仓库 fork 到了自己名下。

**先克隆再提交**（不要 `git init` 强推），避免覆盖远端已有内容。

### 8.2 无写权限时的可行路径：推自己的 fork

**若 `smthelping` 名下有同名 fork**（`fork: true`，parent 指向目标仓库），smthelping 对该 fork 有完整
`admin/push` —— **这是即时可行的推送目标**，且不触碰任何人的仓库。

```bash
cd <repo>
git remote rename origin upstream                                        # 父仓库保留为 upstream
git remote add origin https://github.com/smthelping/<Repo>.git           # fork 作为推送目标
git push -u origin main
```

- 之后 `origin` = 自己的 fork，`upstream` = 父仓库（开 PR / 同步用）—— 标准 fork 工作流
- 推送后核验：`git/trees/main?recursive=1` 列文件 + `truncated: false`
- 需要合并回父仓库时，再向 `upstream` 开 PR（base 相同则可干净合并）
- **开 PR 属于对外动作，先经用户确认再执行**

**⚠️ 本机 `refs/remotes/` 写入不可靠**：改远端后 `git push -u` / `git fetch` 都报成功，
但 `refs/remotes/` 目录**始终为空**，`git status` 一直显示 `## main...origin/main [gone]`，
`git update-ref` 也返回成功却不落盘。**这不是推送失败**（用 GitHub API 核验远端提交即可确认）。

两个必要动作：
1. `mkdir -p .git/refs/remotes/<remote>` —— 目录不会自动创建，这是失败主因
2. **必须写完整 40 位 SHA** —— 短 SHA 会触发 `warning: ignoring broken ref`

```bash
mkdir -p .git/refs/remotes/origin
git rev-parse main | tr -d '\n' > .git/refs/remotes/origin/main   # 完整 SHA
git for-each-ref refs/remotes && git status -sb                   # 应恢复正常
```

### 8.3 fork 之上：开 PR + 启用 Pages（无需对方配合）

**推 fork 只是第一步。** 不依赖对方权限，还能再做两件事拿到完整结果：

**① 向父仓库开 PR**（开 PR 属对外动作，**先经用户确认**）
```bash
# 先查是否已有 PR，避免重复
curl -s --noproxy '*' -H "Authorization: Bearer $TOKEN" \
  "$API/repos/<owner>/<repo>/pulls?state=all"
# 先 compare，确认 ahead/behind，判断能否干净合并
curl -s --noproxy '*' -H "Authorization: Bearer $TOKEN" \
  "$API/repos/<owner>/<repo>/compare/main...<forkOwner>:main"
# 创建：head 必须写 "owner:branch"
curl -s --noproxy '*' -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"title":"...","head":"smthelping:main","base":"main","body":"..."}' \
  "$API/repos/<owner>/<repo>/pulls"
```
- 建完复查 `mergeable: true` / `mergeable_state: clean` 再向用户汇报

**② 启用 fork 的 GitHub Pages**（需对 fork 有 admin，通常满足）
```bash
curl -s --noproxy '*' -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"source":{"branch":"main","path":"/"}}' \
  "$API/repos/<forkOwner>/<repo>/pages"
# 返回 html_url，形如 https://<forkOwner>.github.io/<repo>/
```

**⭐ Pages 地址优于沙箱链接**（2026-09-17 实测对比）：

| 对比项 | GitHub Pages | 沙箱链接 |
|---|---|---|
| 文件字节数 | **与本地完全一致**（无任何注入） | `index.html` 大 ~575 B（注入 beacon） |
| 来源 | 仓库版本控制驱动，推即更新 | 手动触发发布 |
| 生命周期 | 长期稳定 | 预览性质 |

→ **正式交付用 Pages；沙箱链接只作快速预览。** 两者都要跑一遍
`tools/test-dom.js` + `tools/qa-i18n.js` 对**实际线上产物**验证（见 §八 末）。

**无写权限时的完整组合拳**：`推 fork` → `开 PR` → `启用 fork 的 Pages` ——
三件事都不依赖对方配合，即可同时拿到「代码进 GitHub」与「正式线上地址」。

### 8.4 绑定自定义域名（GitHub Pages + Cloudflare）

**DNS 记录**（子域名用 CNAME，apex 才需要 A 记录或 CNAME flattening）：

| Type | Name | Target | Proxy |
|---|---|---|---|
| `CNAME` | `<子域>` | `<账号>.github.io` | **DNS only（灰云）** |

目标只写 `<账号>.github.io`。

**⚠️ 最常见的错误：把仓库路径一起填进 Target。**
用户（和模型）的直觉是「要指向那个仓库」，于是把 `smthelping.github.io/THT_design_Guideline`
整个粘进 Target 字段。**Cloudflare 会原样接受并存储**，记录看起来"建好了"，
但 DNS 里根本不存在 `github.io/tht_design_guideline` 这个主机名 →
`dgl.smthelp.eu` 返回 **NXDOMAIN**（`Status: 3`），而**记录本身是存在的**，很容易误判为"已生效"。

> **CNAME target 是主机名，不是 URL，不能含 `/` 或 `:`。**
> GitHub Pages 把仓库挂在自定义域名的**根路径**上，仓库名整个丢掉 ——
> 所以 Target 必须**恰好**是 `smthelping.github.io`。

判定方法：查 CNAME 记录，看 `Answer[].data` 里有没有斜杠。
有斜杠 = 错，去面板把 Target 改成裸主机名即可（无需删记录重建）。

**⭐ 推送前先跑就绪检查**，它会一次性验证 DNS、HTTPS 与仓库侧一致性：
```bash
node _build/tht-design-guide/check-domain.js <site-dir>
# 全部 PASS 才推 CNAME；任何 FAIL 都不要推
```
关键断言：CNAME target 无斜杠/冒号、等于 `<账号>.github.io`、A 记录落在
`185.199.{108,109,110,111}.153`（GitHub Pages 段）、`https://<域名>/` 返回 200、
仓库 `CNAME` 文件与域名一致、canonical 一致、YouTube 频道链接未被误伤。

**⭐ 必须灰云，不要橙云。** 两个理由，第二个是硬伤：
1. 灰云才能让 GitHub Pages 自行签发/续期 Let's Encrypt 证书，`Enforce HTTPS` 才可用；
   橙云下 GitHub 无法完成域名验证，证书签不下来
2. **橙云会让 Cloudflare 的机器人防护挡在 AI 爬虫前面** —— `GPTBot` / `ClaudeBot` / `PerplexityBot`
   正是 GEO 优化的目标客户，一次 bot challenge 就把静态化的成果抵消掉。
   若确需 CDN/WAF，必须关闭 Bot Fight Mode 并放行已验证机器人

**仓库侧两件事：**

1. **`CNAME` 文件**（仓库根目录，内容为**裸主机名**，无 scheme、无路径、无末尾换行）：
   ```
   dgl.smthelp.eu
   ```
   这是 GitHub Pages 判断服务哪个主机的依据。
2. **站点自身 origin 全部改到新域名**：`rel=canonical`、`og:url`、
   JSON-LD 的 `@id` / `mainEntityOfPage`、`sitemap.xml`、`robots.txt`（含 Sitemap 行）、`llms.txt`。

**⚠️ CNAME 与 canonical 必须一致。** CNAME 决定 GitHub 服务哪个主机，canonical 系列决定爬虫认为
哪个主机权威。两者不一致 = 站点把自己 canonical 到一个它并不服务的主机。
→ 加断言：读 `CNAME` 内容，构造 `https://<cname>`，逐项校验 canonical / og:url / sitemap /
robots / llms / JSON-LD `@id` 都命中它。这样改域名变成一条命令的事。

**⚠️ 替换字符串要选完整 origin+路径，不要只替换用户名。**
`smthelping.github.io/THT_design_Guideline` 是无歧义的；而裸 `smthelping` 会误伤
`youtube.com/c/Smthelping`、仓库路径 `smthelping/THT_design_Guideline`、i18n 键 `smthelping-channel`。
→ 用**幂等脚本 + `--revert`** 一次改完，并在结尾统计「旧 origin 残留数」与
「YouTube 链接存活数」双向校验。参考 `_build/tht-design-guide/patch-custom-domain.js`。

**⚠️ 推送顺序：先建 DNS 并确认解析，再推 `CNAME`。**
一旦 Pages 配了自定义域名而 DNS 不解析，`*.github.io` URL 会 **301 到死掉的主机** →
**新旧两个地址都不可访问**。所以正确顺序是：
`建 DNS → DoH 确认解析 → 推 CNAME → 等 Let's Encrypt 签发 → 勾 Enforce HTTPS`。
在 DNS 就绪前，改动应**本地提交但不推送**，远端保持可用。

**⚠️ 一个自定义域名只能被一个仓库占用。** `CNAME` 一旦提交，若该分支被合并到父仓库，
父仓库也会带上它；若父仓库之后启用 Pages，两个仓库会争抢同一域名。
**合并前须明确由哪个仓库持有域名。**

**验证：三个闸门脚本，按顺序跑（均零依赖，失败非零退出，可用 `&&` 串）**

```bash
# 1. 推 CNAME 之前 —— DNS 记录是否正确
node _build/<proj>/check-domain.js <site-dir> <域名>

# 2. 推完 CNAME 之后 —— 等证书签发，然后强制断言 HTTPS
node _build/<proj>/wait-for-domain.js <域名> --minutes=15
node _build/<proj>/check-domain.js <site-dir> <域名> --require-https

# 3. 域名可用之后 —— 逐字节确认边缘发的就是这一版构建
node _build/<proj>/verify-deployed.js <site-dir> https://<域名>
```

**⚠️ `--require-https` 是标志不是参数，必须放最后。** 脚本签名是 `<site-dir> [domain]`，
写成 `check-domain.js <dir> --require-https` 会让脚本把标志当成域名 → 输出
`domain: --require-https` 并全线 FAIL，看起来像 DNS 崩了，其实只是参数位置错了。

**⚠️「返回 200」不等于「部署成功」。** GitHub Pages 可能返回 200 却发的是**旧构建或兜底页**。
逐字节比对才是唯一可靠的确认手段 —— 这就是 `verify-deployed.js` 存在的理由。
比对前必须把本地 CRLF 归一化为 LF（本机 `core.autocrlf=true`），否则六个文件全部误报不一致。

**⚠️ 如果「逐字节一致」和「内容标记检查」互相矛盾，先怀疑检查器。**
实测：`verify-deployed.js` 报 `all 10 static articles served 0/10`，而同一份 `index.html`
刚刚逐字节比对通过 —— 原因是正则锚定了 `class="static-article"`，实际标记是
`class="article static-article"`（两个类名）。**修工具，不要动交付物。**
（`tools/test-dom.js` 用 CSS 选择器 `querySelectorAll("#route-blog .static-article")`，没有此隐患。）

**⭐ Enforce HTTPS 是独立开关，证书 approved ≠ 已强制跳转。**
`https_enforced: false` 时 `http://<域名>/` 直接返回 200 不跳转，站点可被明文访问，
而 canonical 宣告的是 HTTPS 源。查证与开启（Pages API 需 token，本机凭据管理器里已有）：

```bash
TOKEN=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')

# 读当前状态 —— 先确认 https_certificate.state 是 "approved"
curl -sS -H "Accept: application/vnd.github+json" -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/<owner>/<repo>/pages

# 开启 —— 把现有配置原样回传，避免被清空
curl -sS -X PUT -H "Accept: application/vnd.github+json" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cname":"<域名>","build_type":"legacy","source":{"branch":"main","path":"/"},"https_enforced":true}' \
  https://api.github.com/repos/<owner>/<repo>/pages
```

**⚠️ `PUT /pages` 是替换而非合并。** 请求体必须同时带上 `cname` / `build_type` / `source`，
只发 `https_enforced` 有**清空自定义域名**的风险。返回 `204` 即成功。
（`GET /pages` 未认证时返回 404，别据此判断"没配 Pages"。）

**⚠️ Pages 设置改动不是即时的 —— 按分钟级轮询确认，别急着判失败。**
实测：`https_enforced` 置 `true` 且 API 已回读为 `true` 之后，`http://` 仍返回 200 约 **5 分钟**，
直到 14:25:20 才变成 301。边缘节点逐个更新，且响应带 `Cache-Control: max-age=600`，
用 `--noproxy '*'` 直连也一样会看到旧行为。→ 用 `for` 循环每 30s 探一次，
拿到 301/302/308 再下结论；期间不要重复 PUT。

**⚠️ 本机凭据可非交互读取，但别写进文件。** `git credential fill` 配合 printf 即可拿到 PAT
（`username=x-access-token`），足以调用 REST API —— 这解释了为什么 `git push` 能用而 `gh` 不能用。
token 只放 shell 变量，用完即弃，不要落盘、不要回显。

**⚠️ 证书签发前的失败长什么样**（不要误判为 DNS 问题）：
`schannel: failed to receive handshake`（curl 35）或 `Empty reply from server`（curl 52）——
两者都表示「边缘还没开始服务这个主机」，不是「DNS 错了」。证书签发通常几分钟，
但 GitHub 无回调，只能轮询；最坏情况可达 24h。

### 8.1 推送被 403 阻塞时的兜底：先发布在线链接

本机缓存凭据属于 `smthelping`，对 `smthelp111/*`、`smthelp/*` **均无写权限**，且机器上**不存在**任何可用 token（无 `GITHUB_TOKEN`/`GH_TOKEN` 环境变量、无 `~/.git-credentials`、无 `gh hosts.yml`、无 `~/.netrc`）—— 只有 Windows 凭据管理器里那份错误账号的缓存。

**不要卡在这里交付。** 用应用发布能力先给一个可访问链接（Jason 通常接受，但**必须先问**，不要静默发布）：

```
workbuddy_sites_deploy({
  directory: "<项目绝对路径>",
  language: "static",
  appName: "<简短中文名>",
  userAskedToPublish: true   // 仅当用户在本轮明确要求发布
})
```

- 纯静态站用 `language: "static"`，无需自建 Node 服务
- 重新发布会**覆盖同一链接**，且需用户在本轮再次明确要求
- 发布后必须告知管理入口：**「设置—数据管理—我发布的应用」**
- 验证线上资源：`curl --noproxy '*' -o f <url>` 后 `wc -c` 比对本地字节数（**不要信 `size_download`**，见 §六 坑 1）

**⚠️ `index.html` 线上会比本地大 ~575 字节，这是正常的。**
平台会在 `</head>` 前注入一段腾讯 beacon 埋点（`beacon.cdn.qq.com`）。注入位置在**自写预涂脚本之后**，
所以不影响首屏主题/语言。**其余资源（CSS/JS/i18n）均字节一致** —— 只有 `index.html` 会差。
→ 比对时**不要**因为 `index.html` 不一致就以为发布失败；用 `diff` 确认差异确实只是埋点。

**最强验证手法：把线上产物拉回来跑测试套件。**
```bash
BASE="<shareLink>"
mkdir -p live-verify/assets/js/i18n live-verify/assets/css
for f in index.html assets/css/style.css assets/js/ui.js assets/js/data.js assets/js/app.js \
         assets/js/i18n/app.js assets/js/i18n/{en,es,pt,fr,ar,ru,zh}.js; do
  curl -s --noproxy '*' "$BASE/$f" -o "live-verify/$f"; done
node <repo>/tools/test-dom.js live-verify      # 需 NODE_PATH 指向 jsdom
node <repo>/tools/qa-i18n.js  live-verify
rm -rf live-verify
```
这能证明**线上实际产物**（而不只是本地）功能完好，比只比字节数强得多。

GitHub 与在线发布**互不替代**：在线链接用于快速验证与分享，GitHub 仍是代码副本的正式归宿。

---

## 九、常见交付清单（按需）

- [ ] 顶栏左上角 Logo
- [ ] 页脚 5 社交 + 素材库文案 + 邮箱 + WhatsApp
- [ ] 产品图（真实 URL，来自 `ph.smthelp.com`）
- [ ] 视频（11 位 ID，来自 YouTube 看板）
- [ ] 产品目录（来自 Catalog Board）
- [ ] 内容型文章（标题禁词已审）
- [ ] Chatwoot 客服（协议自适应）
- [ ] JSON-LD + og meta
- [ ] `.nojekyll`
- [ ] README（架构 / 品牌 / 媒体来源 / 部署）
- [ ] 推送（或明确告知权限阻塞）

### 若含主题/多语言（见 §十）

- [ ] `<head>` 内联预涂脚本（防 FOUC）
- [ ] 语言下拉 7 项、主题按钮存在
- [ ] 刷新后偏好保持
- [ ] 切换语言后 **JS 渲染区块**同步更新（计算器/清单/卡片/画廊）
- [ ] 阿拉伯语 `dir="rtl"` + 拉丁度量双向隔离
- [ ] `tools/qa-i18n.js` 与 `tools/test-dom.js` 全绿

---

## 十、主题切换 + 多语言（i18n）实现范式

> 已在 `THT_design_Guideline` 落地并全量验证（79 项断言 + 静态质检全绿）。新站点直接套用。

### 10.1 架构：三个文件各管一件事

| 文件 | 职责 |
|---|---|
| `assets/js/ui.js` | **只管偏好**：主题 + 语言，读写 `localStorage`，设 `data-theme`/`lang`/`dir` |
| `assets/js/i18n/app.js` | `window.APP_I18N` —— **JS 动态生成的字符串**（计算器输出、清单、判定语），100 键 × 7 语 |
| `assets/js/i18n/<code>.js` | `window.I18N.<code>` —— **DOM 静态文本**，每语 ~456 条 |
| `assets/js/app.js` | 行为；渲染时通过 `T(key, vars)` 取词 |

**加载顺序（不可调换）**：`i18n/app.js` → 各语言 `i18n/<code>.js` → `ui.js` → `data.js` → `app.js`。
`ui.js` 必须先于 `app.js`，这样 `ui.js` 的 `sm:langchange` 监听先注册、先执行
（先把 DOM 翻好，`app.js` 再重建动态区块）。

### 10.2 防闪烁：`<head>` 内联预涂脚本

在 `<link rel="stylesheet">` 之后、任何渲染之前，用一个自包含 IIFE 读存储并写 `<html>` 属性。
**没有这一步，回访用户会先看到错误的主题/语言再跳变。**

```html
<script>
(function () {
  try {
    var LANGS = ["en","es","pt","fr","ar","ru","zh"];
    var t = localStorage.getItem("smthelp.theme");
    var l = localStorage.getItem("smthelp.lang");
    if (t !== "light" && t !== "dark") t = "light";
    if (LANGS.indexOf(l) === -1) l = "en";
    var d = document.documentElement;
    d.setAttribute("data-theme", t);
    d.setAttribute("lang", l);
    d.setAttribute("dir", l === "ar" ? "rtl" : "ltr");
  } catch (e) { /* 隐私模式存储不可用，走默认值 */ }
})();
</script>
```

- 存储键固定：`smthelp.theme` / `smthelp.lang`。**预涂脚本与 `ui.js` 里的键名必须逐字一致**（易错点）。
- 全部 `localStorage` 访问包 `try/catch`（隐私模式下会抛异常）。
- 默认语言 `en`；首次访问可回退 `navigator.language` 前缀匹配，再回退 `en`。

### 10.3 主题：只覆盖 token，不复制组件规则

- 把 `[data-theme="dark"]` 写在 CSS 里，**只覆盖 `:root` 的自定义属性**，组件规则一行不动。
- **关键坑：`--ink` 一个变量被当成两种用途**（正文前景色 + hero/footer/表头深色背景）。
  直接翻转它会把深色区块也翻成浅色。**必须先拆**：
  - `--text` / `--text-2`：**可随主题翻转**的前景文字色
  - `--surface` / `--surface-2`：面板背景
  - `--ink`：**保留**给 hero / 公式块 / 页脚 / 表头 —— 两种主题下都保持深色
- 顺手同步 `<meta name="theme-color">`（浅 `#ffffff` / 深 `#0b132b`），移动端地址栏才跟着变。
- 主题按钮用 `aria-pressed` 表达状态，图标在 ☀ / ☾ 之间切换。

### 10.4 语言：英文即源语言，原文缓存

- 可翻译元素挂 `data-i18n="slug"`，**英文文本留在标记里**（JS 挂了也能读）。
- `ui.js` 首次运行时 `cacheOriginals()` 把每个元素的英文 `textContent` 缓存一次；
  `applyI18n()` 用当前语言字典覆盖；**切回英文时还原缓存**，而不是再查一次表。
- 键名由英文文本 slug 化生成，**从标记反推键名**，杜绝键名漂移。
- **只替换「叶子文本」元素**（自身有文本节点、且无含文本的子元素）。
  否则 `textContent` 赋值会把嵌套标记整段抹掉。生成脚本用**栈式分词器**逐 `<tag>` 扫描，不要用正则匹配整段标签。
- 缺键自动回退英文 → **半成品翻译可以安全上线**。
- 数值规格、型号、位号、URL **一律不翻译**（翻公差是引入缺陷，不是本地化）；
  长文技术正文保持英文（工业资料惯例）。**这条要写进 README，否则会被当成漏翻**。

### 10.5 单位必须放在翻译里，不能放在数据里 ⚠️

**本次真实踩坑**：`data.js` 里写 `read: "7 min"`，于是「min」被带进了全部 6 个非英语语种，
中文模板退化成 `"{n}"`，界面直接显示一个光秃秃的 `7`。

→ **`data.js` 只存裸值（`read: 7`），措辞由各语言模板提供**：
`"{n} min read"` / `"阅读 {n} 分钟"` / `"{n} мин чтения"`。
**任何带单位的字段都适用这条。**

### 10.6 切换语言后，JS 渲染的区块必须重建

- 定义 `rerenderAll()`：重跑全部计算器 + 清单 + 卡片 + 画廊 + 目录。
- `document.addEventListener("sm:langchange", rerenderAll)`。
- **清单勾选状态要跨语言保持**：重建前 `checkedState()` 快照，重建后回填并重加 `.checked` 类。
- 事件绑定用 `dataset.bound` 守卫，避免重复绑定导致一次点击触发多次。
- 动态文本（如 `0 of 14 confirmed` 计分）**不要同时挂 `data-i18n`**，
  否则静态字典与动态赋值互相覆盖，结果取决于监听器注册顺序。二选一。

### 10.7 RTL（阿拉伯语）

- 布局用 **CSS 逻辑属性**：`margin-inline-start` / `border-inline-start` / `padding-inline-start` / `text-align: start`，
  这样 `dir="rtl"` 时自动镜像，不用写两套。
- **拉丁度量与型号必须双向隔离**，否则 `±0.07 mm` 在阿拉伯语里会显示成 `mm 0.07±`：
  ```css
  [dir="rtl"] .badge, [dir="rtl"] code, [dir="rtl"] .formula,
  [dir="rtl"] .ci-meta, [dir="rtl"] .r-val {
    direction: ltr; unicode-bidi: isolate;
  }
  ```

### 10.8 验证（两个脚本，放仓库 `tools/`）

| 脚本 | 作用 | 依赖 |
|---|---|---|
| `tools/qa-i18n.js` | 静态质检：占位符不匹配 / 空值 / **退化模板** / 缺目标文字 / 拉丁残留 | 无 |
| `tools/test-dom.js` | jsdom 端到端：默认态、懒加载路由、主题切换+持久化、语言切换、动态区块重建、勾选态保持、刷新恢复、7 语、未捕获异常 | `jsdom` |

```bash
cd <repo>
node tools/qa-i18n.js
NODE_PATH=<含 jsdom 的目录> node tools/test-dom.js
```

- 质检里**品牌名要白名单**（Panasonic / Yamaha / YouTube / pallet …），否则全被误报成「拉丁残留」。
- **「退化模板」检查必不可少**：只查占位符会漏掉 `en="{n} read"` → `zh="{n}"` 这种
  「占位符一致但措辞全丢」的情况（`{n}` 没有字母，其他检查也抓不到）。
- 详情与陷阱见 §六 坑 3 / 3.1。

---

## 十一、变体：单文件交付（客户要「一个 .html 附件」时）

> 2026-09-17 在 `tht-im-pcb-design-guideline-auto-insertion-dfm.html` 落地并全量验证。
> **当需求是「单 HTML 文件、可直接当附件发客户」时，§一 的多文件架构不适用** —— 走这一支。

### 11.1 何时选单文件而非多文件

| 判据 | 单文件 | 多文件（§一） |
|---|---|---|
| 交付形态 | 当邮件附件 / 客户本地打开 | 部署成站点 |
| 改内容的人 | 你（改 JSON 重跑构建） | Jason 直接编辑 |
| 路由 | 锚点滚动（`#section`） | hash 路由 SPA |
| 语言数 | ≤ 8（词典内联进 HTML） | 不限（每语一个文件） |

单文件的代价：**必须有构建脚本**。7 语言 × 300+ 键内联进 HTML 后手工维护必然漂移。

### 11.2 目录结构（构建源与成品分离）

```
<project>/
├── tht-im-...-dfm.html      # ← 成品，只此一个文件，交付物
└── _build-<name>/           # ← 构建源，不进交付
    ├── template.html        # 带 __PLACEHOLDER__ 的模板
    ├── build.py             # 注入词典 + 生成 JSON-LD + 预渲染英文
    ├── validate.py          # 静态断言（见 11.5 / 11.9）
    ├── falsify.py           # 反证测试：改坏成品，断言必须抓住（见 11.10）
    ├── eval.js              # 页面内运行时断言（见 11.8）
    ├── checklinks.py        # 外链实测（见 §六 坑 10）
    ├── probe2.js            # 头部导航逐宽度 / 逐语言实测（见 §六 坑 13）
    └── i18n/{en,es,pt,fr,ar,ru,zh}.json
```

**构建脚本必须幂等**：`template.html` 是唯一真源，`build.py` 每次从它重建成品。
**绝不手改成品** —— 下次构建就冲掉。

### 11.3 预渲染：把英文写进静态 HTML（GEO 的前提）

`data-i18n` 空节点 + JS 填充的方案，对**不执行 JS 的 AI 爬虫等于空页面**。
单文件页面必须在构建时就把英文正文注入静态标记：

```python
# 所有 data-i18n 元素都是空节点，直接把英文写进去
head = re.sub(r'(<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>)(</\2>)',
              lambda m: m.group(1) + esc(EN[m.group(3)]) + m.group(4), head)
```

- **`data-i18n` 元素必须全部是空节点**（`<h3 data-i18n="x"></h3>`），否则注入会叠在旧内容上
- **Blog / 视频卡 / 语言菜单也要预渲染**（容器 div 里塞好英文卡片），否则 JS 不跑时那几块是空的
- JS 的 `applyLang()` 在启动时整体覆盖 —— **静态是英文，切换语言才变**
- 代价：非英语访客会看到一瞬英文再翻。这是 GEO 的必付成本，别为此砍掉预渲染

**度量**：静态正文应 ≥ 3,000 词，且关键数值（型号 / 公差 / 公式）必须在 `<script>` **之前**的正文里出现。加断言。

### 11.4 词典规范（7 语 × 316 键）

- **一份 `en.json` 定键名，其余 6 份照抄键名**，值翻译。键数必须**严格相等**。
- 元信息放 `__meta`：`{"lang":"ar","dir":"rtl","label":"العربية","short":"AR"}` ——
  `dir` 驱动 RTL，`label`/`short` 驱动语言菜单，**不要另写一张语言表**。
- 单位写进词典，不写进数据（见 §10.5）。博客段落数**每篇不同**，用显式键列表：
  ```js
  const BLOGS = [
    {tag:"blog1_tag", title:"blog1_title", read:4, body:["blog1_b1","blog1_b2","blog1_b3","blog1_b4"]},
    {tag:"blog3_tag", title:"blog3_title", read:6,
     body:["blog3_b1","blog3_b2","blog3_b3","blog3_b4","blog3_b5","blog3_b6","blog3_b7","blog3_b8"]}
  ];
  ```
  **不要用 `[1,2,3,4].map()` 生成键名** —— 一旦某篇多一段就静默丢内容。

### 11.5 两条断言，缺一不可（本次真抓到 bug）

```python
# ① 键集一致性 + 非中文词典不得含 CJK 字符
cjk = re.compile(r'[\u4e00-\u9fff]')
for l in langs:
    assert set(D[l]) == set(D['en']), f"{l} 键集漂移"
    if l != 'zh':
        bad = [k for k,v in D[l].items() if isinstance(v,str) and cjk.search(v)]
        assert not bad, f"{l} 混入中文: {bad}"
```

**实测战果**：`ar.json` 的 `why1d` 里混进了 `成本` 两个汉字（`وينخفض成本 الإنتاج`），
键集检查、JSON 解析、页面渲染**全部正常**，只有这条断言抓得到。阿拉伯语读者会看到两个方块字。

```python
# ② 页面引用的每个键必须在 7 语中都有值
used = set(re.findall(r'data-i18n(?:-ph|-title)?="([^"]+)"', body))
used |= set(re.findall(r'"((?:blog[1-6]|video)_[a-z0-9_]+)"', src))
assert all(k in D[l] for l in langs for k in used)
```
反向也查：**未被页面引用的键 = 死键**，要么接上要么删掉。

### 11.6 `data-i18n-ph` / `data-i18n-title` 也要预渲染

`placeholder` 与 `title` 不会因为 `textContent` 被填充。必须单独处理：

```python
head = head.replace('data-i18n-ph="form_scope_ph"',
                    'placeholder="%s" data-i18n-ph="form_scope_ph"' % esc_attr(EN['form_scope_ph']))
```
JS 侧同步：
```js
document.querySelectorAll("[data-i18n-title]").forEach(function(el){
  el.setAttribute("title", T(lang, el.getAttribute("data-i18n-title")));
});
```

### 11.7 单文件的多语言 SEO

- **`?lang=xx` 深链**：`new URLSearchParams(location.search).get("lang")`，
  优先于 `localStorage`（这样链接可分享、可被 hreflang 指到）
- **`hreflang` 全量输出**：en 指干净 URL，其余 6 语指 `?lang=xx`，再补 `x-default`
- **`document.title` 与 `meta[name=description]` 也要随语言切换**（`applyLang()` 里改）
- **JSON-LD 只出英文**（`inLanguage: "en"`）—— 结构化数据不做多语言，避免实体冲突
- 主题**只预涂主题，不预涂语言**：静态内容是英文，提前设 `dir="rtl"` 会让英文段落先右对齐再跳回，
  比不设更糟。语言由启动脚本在翻译的同时设

### 11.8 验证套件（5 类 7 个脚本，CDP，零依赖，Node 22 原生 WebSocket）

单文件页「长得对」和「跑得对」是两件事，必须分开验。
**静态 → 外链 → 视觉 → 运行时 → 反证**，五类各管一件事，脚本全放构建源目录：

| 类 | 脚本 | 作用 | 关键点 |
|---|---|---|---|
| 静态 | `validate.py` | 断言（本次 **152 项**） | 纯字符串/正则，秒级，**先跑这个** |
| 外链 | `checklinks.py` | 全部外链实测 + **视频 ID 对板核对** | 见 §六 坑 10/12/17 |
| 视觉 | `shot.js` | 整页截图 | 强制 eager + 等 `image.complete`（§六 坑 14）|
| 视觉 | `shotsec.js` | 单区块截图，可指定 `light`/`dark` | `node shotsec.js <url> "#faq" out.png dark` |
| 视觉 | `probe2.js` | **头部导航实测**：逐宽度**逐语言**输出 `navNeed/avail/余量/是否换行` | §六 坑 13 |
| 运行时 | `eval.js` | **页面内功能断言**：在真实 DOM 里调 `calc()`、`applyLang()`、点 `#themeBtn` | 见下 |
| 反证 | `falsify.py` | **把成品故意改坏**，逐项确认断言抓得到 | §11.10 |

⚠️ 五类里**只有静态那类能秒级跑完**，所以它是主循环；其余四类是交付前的一次性关卡。
⚠️ `validate.py` 全绿**不等于**页面没问题 —— 只等于「当前这份文件没触发任何断言」。
   断言本身有没有判别力，要靠 §11.10 反证。

`eval.js` 是性价比最高的一件——它抓的是截图看不出来的东西：

```javascript
// 计算器：数值必须对得上，留空必须「要数字」而不是「编数字」
g("cPrice").value = 67000; g("cSal").value = 12000; calc();
out.m1Payback = txt("rPayback") + " " + txt("rPaybackU");     // 期望 2.8 years
g("cPrice").value = ""; calc();
out.blankPayback = txt("rPaybackU");                          // 期望 "Enter your machine investment…"

// 主题：读 key 要写对（本次 key 是 smth_theme，写错会误判为「没持久化」）
document.getElementById("themeBtn").click();
out.themeStored = localStorage.getItem("smth_theme");

// 预渲染自检：这两项为 0 就说明静态化漏了
out.emptyI18nNodes  = [...document.querySelectorAll("[data-i18n]")].filter(e => !e.textContent.trim()).length;
out.brokenImages    = [...document.images].filter(i => i.complete && i.naturalWidth === 0).length;
out.videoCards      = document.querySelectorAll("#vidGrid .vid").length;   // 选择器要照真实标记写
```

⚠️ **选择器写错会伪装成「功能缺失」**：本次 `#vgrid .vcard` 与 `details` 两个选择器都不存在
（真实是 `#vidGrid .vid`，FAQ 当时尚未建），一度看起来像「视频没预渲染、FAQ 没渲染」。
**探针返回 0 时，先 `grep` 真实标记确认选择器，再判断是不是 bug。**

### 11.9 单文件交付检查清单

- [ ] 无残留占位符（`__[A-Z_]{3,}__` 正则扫一遍）
- [ ] JSON-LD 可 `json.loads`，`@graph` 含 Organization / WebSite / WebPage / TechArticle / FAQPage / ItemList / BreadcrumbList
- [ ] 7 语键集相等 + 非中文词典无 CJK
- [ ] 页面引用的键 7 语全覆盖 + 无死键
- [ ] 静态正文词数 + 关键数值出现在 `<script>` 之前
- [ ] Blog / 视频卡 / 语言菜单已预渲染
- [ ] 禁词审查（`\b` 词边界，见 §六 坑 4）
- [ ] HTML 标签配对（HTMLParser 栈式扫描，`unclosed at EOF` 必须为空）
- [ ] `h1` 恰好 1 个
- [ ] 全部外链实测（见 §六 坑 10）
- [ ] **结构化数据的每条内容都能在静态 HTML 中检索到**（§5.3），且**做过反证测试**
- [ ] 可见区块编号连续、且与 DOM 顺序一致（§5.4）
- [ ] 页面内功能断言通过：计算器输入→输出、语言切换、主题持久化、无空 `data-i18n` 节点（§11.8）
- [ ] 导航在**逐语言实测余量最小的那门语言**（本次是 pt）下不换行（§六 坑 13）
- [ ] 网格图注底部对齐；混长宽比那一行已信箱化（§六 坑 18）
- [ ] 弹窗 / 嵌入框关闭后 `src` 是 `about:blank`，**不是空串**（§六 坑 15）
- [ ] **跑过 `falsify.py`：每个变异都被「预期的那条」断言抓住**（§11.10）
- [ ] 客户资料转公开页：黑名单断言 + **反向断言**（页面自己说明出处与不确定性，§11.11）
- [ ] 远端与本地**字节数相等**（`curl -sL <raw> | wc -c` vs `wc -c <local>`）

### 11.10 反证测试：不能失败的断言等于没有断言

`validate.py` 全绿只说明「这份文件没触发任何断言」，**不说明断言有判别力**。
一个恒真的断言会让 152 项全绿，同时放过所有 bug。

→ 交付前跑一次 `falsify.py`：**故意把成品改坏，逐项确认 `validate.py` 抓住，
  而且抓到的是「预期的那条」**（不是碰巧被别的断言拦下）。

本次 7 个变异，**7/7 被正确捕获**：

| 变异 | 应由哪条断言抓住 |
|---|---|
| 删掉可见 FAQ 区块 | `every FAQPage question is visible in the static page` |
| 改一个 JSON-LD 规格值 | `JSON-LD specifications match the visible table` |
| 把某个卡尺读数扰动 0.01mm | `2.28 mm = 25.00 - 22.72`（算式自洽） |
| 让两个区块用同一个可见编号 | `visible section numbers are 01..10` |
| 让两张内联图内容相同 | `no two inlined images are the same payload` |
| 把客户名重新写回页面 | `free of customer and quote artefacts` |
| 视频弹窗关闭改回空 `src` | `does not set an empty src` |

```python
# 每个变异：复制一份 → 改一处 → 跑 validate.py → 断言「失败」且「原因是预期那条」
for name, mutate, expect in MUTATIONS:
    shutil.copy2(BUILT, tmp)
    s = io.open(tmp, encoding="utf-8").read()
    io.open(tmp, "w", encoding="utf-8").write(mutate(s))
    rc, out = run([PY, VALIDATE, tmp, I18N])
    assert rc != 0, "%s 没被抓住" % name
    assert expect in out, "%s 被别的断言拦下了：%s" % (name, out[-300:])
```

⚠️ **本机 `shutil.rmtree` 会失败**（`OSError: SHFileOperationW 失败: 0x2`）——
环境的递归删除被改写到系统回收站，沙箱里不可用。
→ 用 `os.makedirs(exist_ok=True)` + 逐文件 `shutil.copy2`，**别用 rmtree 清临时目录**。

⚠️ **变异要贴着断言的设计意图改**。例如把两个区块编号改成同一个时，
必须确认它**没有先被「编号连续」那条拦下** —— 否则你以为验证了 A，实际验证的是 B。

⚠️ 新增任何断言后，**同步给 `falsify.py` 加一个对应变异**。否则新断言是没验过的。

### 11.11 客户资料转公开页：匿名化 + 证据分级（必做）

把**客户内部文件**（demo 报告 / 验收单 / 测试记录 / 报价）转成**公开落地页**时，
两个动作必须同时做，缺一个就是事故。

**① 匿名化 —— 写成断言，不是「我记得删了」**

客户名、联系人、地址、邮编、单号、金额、报价条款一律不得出现。
**扫全文**（含 JSON-LD、`alt`、`title`、`meta`），漏一个就是泄露商业信息：

```python
BANNED = ["absolute electronics", "jignesh", "jpatel", "menomonee", "53051",
          "AE22063001", "28,500", "26,605", "quotation"]
for b in BANNED:
    check("free of customer and quote artefacts: %s" % b, b not in html.lower())
```

**反向断言同样重要** —— 页面必须**自己说明**它引用了什么、不确定什么：

```python
check("states it cites a demo report", "demo report" in html.lower())
check("does not name the customer",  "the customer is not named" in html.lower())
check("spec must be reconfirmed",    "reconfirm" in html.lower())
```

**② 证据分级 —— 每个数字都要能追溯，且标注可信度**

页面里同时存在三种数据，**必须用标签区分**，否则读者会把示意当实测：

| 标签 | 含义 | 本次实例 |
|---|---|---|
| `已验证数据` | 客户文件里的原始实测读数 | 卡尺读数 25.00 / 22.72 / 23.62 mm |
| `概念示意` | 我方的解读、示意图、CAD 剖视 | 刀头 CAD 剖面图 |
| `待确认` | 需客户复测或我方复核的参数 | 适配机型的具体行程 |

→ **机型归属要显式声明是「标注」而非「确认」**：本次客户文件没写机型，
  按 Jason 指定标为 SF320AT，页面就写「按本页所属机型 SF320AT 标注，下单前需复核」。
  **不要默默写成一个确定事实。**

→ **任何「提升 N 倍 / 减少 N%」的结论，必须能在页面上就地复算**：
  本次把三组读数 + 算式一起放出来，读者自己减一遍就知道 70.5% 是怎么来的。
  这既是 GEO 的可引用性要求，也是不夸大的自证。
