---
name: smthelp-case-study-html
description: "客户项目复盘数据 → 脱敏英文项目案例 → 单文件 HTML 页面（索引导航 + 统一模板 + 官网配图）。当用户要求『把客户项目做成案例报告/案例页』『生成可公开发布的项目案例』『做客户背书/选型参考页面』『输出单文件 HTML 案例集』时触发。"
agent_created: true
---

# 脱敏案例页生成（SMT 外贸）

## 核心定位

把**内部真实的客户跟进数据**改写成**可以公开发给新客户的英文案例集**。

难点不在写作文案，在三件事：

1. **脱敏**——客户名、域名、价格、合同金额一个都不能漏，且不能让人反推。
2. **诚实**——内部数据里绝大多数是询价/报价阶段，不是已交付产线。不能把「报价了」写成「产能提升 40%」。
3. **可交付**——单文件 HTML，内联样式脚本，能直接丢给客户或挂到官网。

本 skill 的输出是一份**能立刻发出去的 HTML**，不是草稿。

---

## 一、脱敏规则（硬约束）

### 必须抹掉

| 类型 | 处理 |
|---|---|
| 客户公司名、域名、邮箱后缀 | 全部删除 |
| 终端客户名（客户的客户） | 全部删除 |
| 价格、报价金额、合同金额、PI 金额 | 全部删除，且不要写「约 XX 万」这类可反推的表述 |
| 供应商名、内部工具名（NotebookLM / Gemini / 1688 等） | 全部删除或泛化 |
| 第三方设备品牌名（JUKI / Panasonic / ERSA 等） | 泛化为 "an installed placement platform" / "their Japanese placement platform" / "the installed wave soldering platform" |

### 客户画像写法（统一模板）

> 「{国家/地区} 的一家生产 {产品类别} 的公司」+ 行业、规模、产线特征

例：
- `a manufacturer of smart bathroom mirror controllers in Canada`
- `an EMS provider in France running wave soldering lines`
- `a distributor in Mexico supplying six categories of SMT and THT consumables`

### 高频泄漏点（每次都要单独查）

- 案例标题里塞了设备品牌名 → 改用设备类别
- **配图的 URL slug 里带品牌名**（如 `Juki-Nozzle.jpg`）→ 换成通用图（`Nozzle.jpg`）
- 官网产品页 URL 的 slug 带品牌 → 换源页面
- 「与日本 XXX 签订合作协议」→ 「the Japanese headquarters」

### 校验（必做，程序化）

渲染完成后对成品 HTML 全文跑黑名单匹配：客户名/域名/终端客户/品牌/工具名。
注意排除误报：自有官网产品页 slug 里的型号（如 `s1688-smt-stencil-cleaning-machine`）是**公司自己的产品**，不是客户名。

---

## 二、证据分级（本 skill 最重要的机制）

内部数据里「已交付 + 有实测数据」的案例通常只占 20%。**不要把报价阶段写成产线收益**。

每个量化数字打三级标签之一：

| 标签 | 含义 | 用法 |
|---|---|---|
| `Measured` | 产线实测 | 只有在客户现场真正测到的才用 |
| `Delivery record` | 交付/流程记录 | 日期、数量、天数、批次数 —— 这类最安全，也最有说服力 |
| `Specification` | 公开规格 | 设备标称参数，明确标注不是该客户的实测 |

没有实测数据的案例，**直接写明**「No production measurements exist at this stage」，然后交付记录撑场面（询价→出货天数、供货批次、品类数）。

例：
> Evidence basis. Quotation and supplier registration record. Board size is the customer's stated maximum. No production measurements exist; no machine has been installed.

---

## 三、统一案例模板

每节固定六块：

1. **Project background** — 客户是谁（脱敏画像）、产线是什么、为什么找过来
2. **The challenge** — 具体的技术/商务卡点（要具体到板子尺寸、器件形态、包装方式、认证要求）
3. **Our solution** — 我方做了什么，**谁做的**（真实姓名）
4. **Implementation and results** — 带日期的落地过程 + 指标卡
5. **Customer benefits** — 3–5 条 `<li>`，每条是客户拿到的具体好处
6. **Evidence basis** — 证据分级声明

指标卡用 `<div class="mx-grid">`，每张卡带 `mx-v`（值）/ `mx-l`（标签）/ `mx-t`（证据等级）。

时间轴用 `<details>` 折叠，每行 `日期 + 事件`，日期来自项目系统的真实记录。

---

## 四、配图管线（ph.smthelp.com 已死，走官网）

### 图床不可用（已确认，别再排查）

`ph.smthelp.com`（Chevereto v4）**服务端 HTTPS 故障**：TLS 握手成功但服务端返回 0 字节 / record-layer 失败。
已用 curl（HTTP/1.1、TLS1.2、TLS1.3）、自写裸 TLS 客户端、真实 Chromium（`ERR_HTTP2_PROTOCOL_ERROR`）、两个第三方代理交叉验证。
真实 IP `103.153.101.182`（需用 DoH 解析，本地 `dig` 被污染成 `198.18.0.50`）。**不是本地网络问题，别浪费时间重试。**

### 官网图片管线

- sitemap 真身是 **`/sitemap_en.xml`**（2,920 条）。`/sitemap.xml` 返回 404 HTML 页面，别用它。
- 图片托管在腾讯 COS：`hk03-1251009151.file.myqcloud.com/smthelp.com/{desc,shop_imgs,ueditor}/...`
- 支持缩略图参数：`?imageMogr2/thumbnail/{W}x{H}/format/webp`
- URL 常带 `-WxH` 尺寸后缀（如 `foo-800x600.jpg`），**必须先剥离**再请求原图
- 归一化时过滤 chrome 图：logo / icon / social / certificate- / iso-9001 / ce-mark

### 爬虫要点

扫描 `<img>` 的 `src` / `data-src` / `data-original` / `data-lazy`，外加 `<a href>` 的大图链接。
**不要只匹配灯箱结构**（`<a href><img alt>`）——实测只能覆盖 204/858 页；通用 `<img>` 扫描能到 1,222 页 / 11,136 图。
12 线程，`requests` 需装进隔离 venv：`/Users/mac/.workbuddy/binaries/python/envs/default/bin/python -m pip install requests`

### 取图尺寸（用来消除 CLS）

COS 支持 `?imageInfo`，返回原图宽高 —— **值是字符串，必须 `int()` 转换**，否则会被误判失败。

```
https://<cdn>/smthelp.com/desc/2015/09/Nozzle.jpg?imageInfo
→ {"format":"jpeg","width":"800","height":"800", ...}
```

拿到后写进 `<img width height>`，配合 CSS `.fig img{width:100%;height:auto}` 预留空间。

### 找不到图就留空

用户规则：**不要用无关占位图，不要外链失效图片**。渲染一个说明块：

```html
<div class="fig-empty"><p>No matching image was found in the Southern Machinery
product library for this project. It is left blank deliberately rather than
filled with an unrelated picture.</p></div>
```

同时给每个 `<img>` 加 `onerror="this.closest('figure').style.display='none'"`，做双保险。

---

## 五、单文件 HTML 的三个已知坑（每次都会踩）

长文档 + 顶部 sticky 索引导航的组合，必出这三个问题：

### 坑 1：移动端导航条撑爆屏幕

chips 换行后导航能到 **350px**，占 844px 视口的 41%。
**修**：`max-width:760px` 下把 chips 改成单行横向滚动条 ——

```css
.chips{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.chip{flex:0 0 auto}
```

导航降到 ~74px。再加一段 JS 让激活项自动滚进可视区（只动容器的 `scrollLeft`，不要 `scrollIntoView`，那会连带滚动整页）。

### 坑 2：图片撑开布局 → CLS → 锚点跳不准

用 `?imageInfo` 写 `width`/`height`（见上）。CLS 归零。

### 坑 3：锚点偏移量 & 长跳转动画

- 不要同时设 `scroll-margin-top` 和 `scroll-padding-top`，两者会**叠加**（132+132=264px 的空洞）。
- 导航条高度随 chips 换行变化，硬编码必错。**用 JS 实测**：

```js
var nav = document.querySelector('nav');
function syncPad(){
  document.documentElement.style.scrollPaddingTop =
    Math.round(nav.getBoundingClientRect().height + 16) + 'px';
}
syncPad();
window.addEventListener('resize', syncPad, {passive:true});
if('ResizeObserver' in window) new ResizeObserver(syncPad).observe(nav);
```

- chip 点击改为 `preventDefault` + 自己滚，**超过 3 屏用 `instant`、3 屏内用 `smooth`**：

```js
el.scrollIntoView({behavior: dist > window.innerHeight*3 ? 'instant' : 'smooth', block:'start'});
if(history.replaceState) history.replaceState(null, '', '#' + el.id);
```

**关键陷阱：`behavior:'auto'` 会回退到 CSS 的 `scroll-behavior:smooth`**，想要真瞬时必须用 `'instant'`。
否则 70,000px 的移动版页面跨页跳转会动画好几秒。

---

## 六、写作文风

按 `smthelp-english-humanizer` 的 **A 档**（正式、零人格化、工程师写的）：短句、主动语态、给确切参数。
SMT 术语保留英文（nozzle / feeder / depanelizer / wave soldering finger / odd-form insertion），数字、强制 CTA 不做改写。

`smthelp-brand-voice` 的强制 CTA 两行必须原文照抄，放在页面末尾 CTA 块里。

---

## 七、验收清单

渲染完必须全部跑一遍：

- [ ] 黑名单扫描（客户/域名/终端客户/品牌/工具名）→ 0 泄漏
- [ ] 禁用词扫描（AI 腔 + 绝对化形容词）→ 0
- [ ] `$` / `USD` / 任何金额 → 0
- [ ] 标签配平（section / figure / details / table / div / ul / li / p）
- [ ] 外部 CSS/JS 引用 → 0（`<style>` 和 `<script>` 各 1 个，均内联）
- [ ] 所有 `<img src>` 和源页面 `<a href>` → HTTP 200
- [ ] 浏览器冒烟（ego-browser）：逐个点 20 个导航 chip，验证落点在导航条下方
- [ ] 桌面 1283px + 移动 390px 双断点，各跑一次完整流程
- [ ] CLS = 0，JS 错误 = 0，无横向溢出

### ego-browser 冒烟要点

`js(expr)` **只接受一个字符串参数**，不能传 `{awaitPromise:true}` 之类的 options，否则报 `Invalid parameters`。
顶层对象字面量要写成 `(() => ({...}))()`，直接 `({...})` 会被当成代码块报 "is not a function"。
每个 heredoc 开头要 `await useOrCreateTaskSpace(name)`，否则 `listTabs: Task space not selected`。

---

## 八、相关 skill

- `smthelp-worktile-rollup` —— 上游：从 Worktile xlsx 归并出 Top N 客户与证据时间线
- `smthelp-brand-voice` —— 品牌色、术语保留、禁用词、强制 CTA
- `smthelp-english-humanizer` —— A/B/C/D 语域分级
- `smthelp-technical-article` —— 不许编造工况的硬规则
