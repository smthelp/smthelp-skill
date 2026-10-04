# 07 · 资源管线：YouTube 视频板 + Product Catalog 板 + 图床

> 用途：单文件 HTML 落地页需要嵌入**真实机器素材**时，从三处公司资源站拉取，
> 而不是用 AI 生成或 Unsplash 抽象图。这份文档记录三处站点的结构、抓取模式、
> 以及本机网络下 `ph.smthelp.com` 不可达时的回退方案。

---

## 1. 三处资源站的职责

| 站点 | 内容 | 用途 | 抓取入口 |
|---|---|---|---|
| YouTube Video Board | 1248 张视频卡片，分类齐全（THT 插入、波峰焊、AOI、AGV、贴片…） | Hero 视频、Marquee 缩略图、Videos 区块网格 | `https://file.autoinsertion.com/public/Southern-Machinery-YouTube-Video-Board.html` |
| Product Catalog Board | 874 张文档卡（PDF + HTML 3D 浏览器图） | Specs 配套 PDF、3D 浏览器图下载、变体对照表辅助 | `https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html` |
| ph.smthelp.com | 公司图床，机器实拍图 | 替代 YouTube 缩略图做更"产品级"的图 | `https://ph.smthelp.com` |

**优先级**：真实设备图 > YouTube 视频缩略图 > 工程剖视示意图 > 槽位占位。
**底线**：绝不 AI 生成"看起来像机器"的图，等于替客户虚构产品。

---

## 2. YouTube Video Board 抓取模式

每张视频卡是一个 `<article class="doc-card video-card">`，关键 data 属性：

| 属性 | 用途 |
|---|---|
| `data-title` | 视频标题（搜索关键词用） |
| `data-model` | 关联机型（如 `[to be confirmed]` 表示未填） |
| `data-category` | 类别（Wave & Selective Soldering / THT Auto Insertion 等 14 类） |
| `data-duration` | 时长（秒） |
| `data-url` | YouTube 完整 URL |
| `data-embed` | `https://www.youtube-nocookie.com/embed/<ID>?rel=0` |
| `data-thumb` | `https://i.ytimg.com/vi/<ID>/hqdefault.jpg` |

**完整卡片结构**（用于解析）：每张 `<article>` 标签整体是元数据，下面的 `<img>` 是缩略图。

**抓取脚本**（30 行内搞定）：

```python
import re, html, json, requests
s = requests.get(YT_BOARD, timeout=60).text
cards = re.findall(r'<article class="doc-card video-card"[^>]*>', s)
def attr(t, n):
    m = re.search(r'data-' + n + r'="([^"]*)"', t)
    return html.unescape(m.group(1)) if m else ''
rows = [dict(title=attr(c, "title"), model=attr(c, "model"),
             cat=attr(c, "category"), dur=attr(c, "duration"),
             url=attr(c, "url"), embed=attr(c, "embed"),
             thumb=attr(c, "thumb")) for c in cards]
```

**选片规则**（落地页嵌入）：
- Hero 主力视频：精确匹配 `data-model == '<机型>'` 或 `data-title` 含机型号；
  优先选时长 1–3 分钟、标题用人类语言而非"to be confirmed"占位的。
- Marquee 12 张：从主类别挑 6 + 关联类别挑 6；优先同型号；时长差异化（30s / 60s / 2min 各几张）。
- Videos 网格 6 张：避开 Hero 主力，从 setup / process / QA 三类各挑 2 张。
- 缩略图：用 `hqdefault.jpg`（480×360，全 ID 必有）；Hero 优先用 `maxresdefault.jpg`
  （1280×720，约 60% 命中率，需 `onerror` 回退）。

---

## 3. Product Catalog Board 抓取模式

每张文档卡是 `<article class="doc-card">`，关键 data 属性：

| 属性 | 用途 |
|---|---|
| `data-category` | 类别（33 类，含 Marketing & ROI Tools） |
| `data-ext` | 后缀（pdf / html / xlsx） |
| `data-name` | 干净文件名（无扩展名） |
| `data-original` | 原始文件名（含扩展名） |
| `data-path` | 服务器相对路径 |
| `data-url` | 完整 URL |
| `data-size` | 字节数 |
| `data-mtime` | 修改时间 |

**选片规则**（落地页嵌入）：
- Specs 配套 PDF：`data-category == 'Wave & Selective Soldering'` 且 `data-name` 含主机型号；
  优先选 User Manual + 安装步骤 + 产品规格书各一份。
- 3D 浏览器图：`data-ext == 'html'`，优先 wave soldering machine / line / conveyor 三个布局图。
- 不抓 Marketing & ROI Tools 类（不直接放页面）。

---

## 4. ph.smthelp.com — 本机不可达时的回退方案

**实测（本机 2026-09-06）**：`ph.smthelp.com` 三个 DNS（8.8.8.8 / 1.1.1.1 / 223.5.5.5）
全部解析到 `198.18.0.80`（黑洞 IP），`curl` 与 WebFetch 均失败。

**这是本机网络环境的特殊情况**，海外用户访问正常。

页面端要做的两件事：
1. **图片优先源切换**：落地页里所有 `ph.smthelp.com` 路径作为**官方图床 URL**仍可写入
   （海外真实用户能看到），但**本机预览和构建脚本**需要备援。
2. **回退链**：
   - Hero 缩略图 → `i.ytimg.com/vi/<hero_id>/maxresdefault.jpg`，`onerror` 回退到 `hqdefault.jpg`
   - Marquee / Videos 缩略图 → `hqdefault.jpg`
   - Applications 卡片 → 同样 `hqdefault.jpg`（480×360 拉伸可接受）
   - Logo → `file.aismt.kdns.fr/raw/Southern%20Machinery%20logo.png`（实测 200，1020×283 PNG）

**一旦图床恢复**，把所有 `<img src="i.ytimg.com/...">` 替换为真实路径即可。
建议在每个 `<img>` 上保留 `data-ph-asset="<ph.smthelp.com 上的图 ID/路径>"`，
作为替换索引（落到公司知识库时按这个字段查）。

---

## 5. 与 Chatwoot 客服的接入

Chatwoot SDK 由公司 `chat.smthelp.com` 自托管，全局右下角。
集成到每个落地页 `<head>`：

```html
<script>
  window.chatwootSettings = {"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"};
  (function(d,t) {
    var BASE_URL="http://chat.smthelp.com";
    var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
    g.src=BASE_URL+"/packs/js/sdk.js";
    g.async = true;
    s.parentNode.insertBefore(g,s);
    g.onload=function(){
      window.chatwootSDK.run({
        websiteToken: 'saMcpgSupcmd1VQwytgPLfbK',
        baseUrl: BASE_URL
      })
    }
  })(document,"script");
</script>
```

**已知**：本机网络下 `chat.smthelp.com` 也可能被 DNS 屏蔽（同一个被黑洞的域 `smthelp.com`），
脚本静默失败。海外用户正常。**不要**做降级提示，否则正式版会误导。

---

## 6. SEO 命名规则

落地页文件名 + 标题模板：

| 字段 | 规则 | 示例 |
|---|---|---|
| 文件名 | `小写机型-主关键词-次关键词-修饰.html` | `s-ws450-wave-soldering-machine-450mm-pcb-lead-free-dual-wave.html` |
| `<title>` | `<机型> <主关键词> \| <次关键词 1>, <次关键词 2> \| <品牌>` | `S-WS450 Wave Soldering Machine \| 450 mm PCB, Dual Wave, Lead-Free \| Southern Machinery` |
| meta description | ≤ 155 字符，含主关键词 + 1–2 个数字 + 1 个差异化卖点 | `S-WS450 wave soldering machine: 50-450 mm PCB, 4 preheat zones, dual wave, 450-480 kg solder pot, lead-free. CE certified. Built in Shenzhen since 2011.` |
| meta keywords | 7–10 个，机型号 + 主词 + 工艺 + 区域 + 品牌 | `S-WS450, wave soldering machine, 450 mm PCB, dual wave, lead-free, THT line, Southern Machinery, SMThelp` |
| canonical | `https://www.SMThelp.com/products/<cat>/<slug>` | `https://www.SMThelp.com/products/wave-soldering/s-ws450` |
| OG image | 1280×720 静态图，落地页优先用 Hero 视频的 maxresdefault | `https://i.ytimg.com/vi/<hero_id>/maxresdefault.jpg` |

**Schema.org Product**：每页必写，包含 `name / brand / manufacturer / category / model / sku / offers`
（offers 用 0 + `priceCurrency: "USD"` + `availability: InStock`，明确不发具体价）。

**Open Graph + Twitter Card**：title / description / image / url 四件套，image 与 Schema 同源。

---

## 7. 落地页 Footer 的资源 + 社媒约定

固定四列结构：

| 列 | 内容 |
|---|---|
| 1. Brand | Logo + 一句话定位（"SMT and THT assembly equipment since 2011"） |
| 2. Social | LinkedIn Company / LinkedIn Profile / Twitter / Facebook / YouTube |
| 3. Resources | file.autoinsertion.com / ph.smthelp.com / 官网 / email / WhatsApp |
| 4. Meta | © 年份 · 工厂地址 · 认证（CE / CCC / UL / ISO 9001） |

**Footer 不写具体价格**，只写域名 + 联系方式。

**WhatsApp 入口**统一用 `https://wa.me/8613602562576`，电话格式 `+86 13602562576`。