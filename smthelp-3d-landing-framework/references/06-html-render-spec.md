# 06 · 单文件 HTML 落地页渲染规格（Prompt → HTML）

> 用途：把 `templates/prompt-master-EN.md` 生成的英文 Prompt 落地成**可直接在浏览器打开 /
> 可直接部署的单文件 HTML**，不依赖 React / Vite / Tailwind 构建链。
> 适用场景：官方站产品页、社媒引流页、展会二维码落地页、邮件签名页。

---

## 1. 为什么不用 React 原样实现

Prompt 里写的是 React + Tailwind + Framer Motion（因为那是对代码生成工具最友好的描述）。
交付给用户的是**独立 HTML 文件**时，换成原生实现更稳：

| Prompt 描述 | HTML 实现 | 说明 |
|---|---|---|
| `framer-motion` FadeIn | `IntersectionObserver` + `.fade/.in` | `rootMargin:'50px', threshold:0`，命中后 `unobserve`（等价 `once:true`） |
| `framer-motion` Magnet | `mousemove` + `translate3d(dx/strength, dy/strength, 0)` | 进入范围 `transition .3s ease-out`，离开 `.6s ease-in-out`；`strength 3`、`padding 150` |
| 字符级渐显 `AnimatedText` | 拆 `<span class="char">`，滚动进度算 `upto = floor(p * len)` | `p` 由 `getBoundingClientRect().top` 在视口 80%→20% 区间映射 |
| 粘性叠卡 `useScroll + useTransform` | `position:sticky` + 手写 `scale` | `targetScale = 1 - (total - 1 - index) * 0.03` |
| 双向跑马灯 | 两个 `requestAnimationFrame` 节流的 passive scroll 监听 | 系数 `0.25`；每行先 clone 到 **3 倍**再位移 |
| Tailwind class | 直接写 CSS 变量 + clamp | 见 §2 |

Framer Motion 的 `motion.create()` 等动态标签在原生实现里不需要。

---

## 2. 设计令牌（直接抄）

```css
:root{
  --bg:#0B0E0F; --text:#D7E2EA; --teal:#0AA5A5; --green:#90C641;
  --line:rgba(217,228,234,.15); --line-strong:rgba(217,228,234,.18); --ink:#0B0E0F;
  --grad:linear-gradient(180deg,#5C6E73 0%,#D9E4EA 100%);
  --cta:linear-gradient(123deg,#06282A 7%,#0AA5A5 37%,#6FA832 72%,#90C641 100%);
}
```
- 字体 Archivo 300–900（Google Fonts），fallback 系统 sans
- 主标题 `.hero-heading`：`background:var(--grad)` + `background-clip:text` + `text-fill-color:transparent`
- 首屏高度用 `100svh`，**不用** `100vh`
- `html,body,#root` 全部铺 `--bg`，横向 `overflow-x:clip`
- 大段圆角：`40px / 50px / 60px` 三档（对应 sm / md 断点），区块之间用负 margin 叠压

---

## 3. 素材槽位约定（重要）

没有真实设备素材时**不要**用 Unsplash 抽象图，也不要 AI 生成"看起来像机器"的图——
那等于替客户虚构产品。做法是留**可读的素材槽位**：

```html
<div class="media-slot" data-asset="Solder wave close-up"> … </div>
```

- 槽位样式：暗色网格底 + 1px 虚线边 + mono 小字标注所需镜头
- 文件顶部用 HTML 注释写明 `ASSET SLOTS` 清单与建议尺寸
- 全站搜 `data-asset` 即可定位全部待补素材
- Hero 视觉若暂无渲染图：用**工程剖视示意图 SVG**（按真实结构画：喷雾 → 预热 → 双波峰 → 冷却），
  这是真实的工程信息，不是虚构照片

---

## 4. 区块落位顺序（与 Prompt 一致）

1. Hero（nav / eyebrow / 巨型标题 / one-liner + 报价按钮 / 主视觉 + Hotspot ×3）
2. Trust Marquee（双行反向 + mono 信任条）
3. Process（四角参数卡 + 巨型标题 + 字符渐显叙事 + 3 张 StatCard + 按钮）
4. Specs（**白底** + 7 行编号参数 + 脚注 + 配套条 + 变体对照表）
5. ROI（暗底 + 3 卡 + 数据条 + 资格审查三问）
6. Application Stack（3 张 sticky 叠卡）
7. FAQ（白底 + `<details>` 手风琴 6 问）
8. Quote（表单 + 联系方式 + 强制 CTA 块 + Footer）+ 移动端 sticky WhatsApp 底栏

移动端：`@media(max-width:767px){body{padding-bottom:3.2rem}}` 给底栏留位。

---

## 5. 降级与无障碍

- `@media(prefers-reduced-motion:reduce)`：关 Magnet、跑马灯位移、字符动画（`.char{opacity:1}`）、hotspot pulse
- `details/summary` 原生手风琴 → 无 JS 时 FAQ 依然可读
- 所有 scroll 监听 `{ passive:true }`，`will-change:transform` 只加在动画元素
- 移动端四角参数卡改为 2×2 网格，避免遮挡标题

---

## 6. 交付前必跑的校验脚本

```python
# 把 HTML 转成纯文本再查，避免被 <a href="mailto:..."> 打断导致"逐字一致"误判
import re, html
s = open("page.html", encoding="utf-8").read()
body = s.split("<body", 1)[1]
body = re.sub(r"<script[\s\S]*?</script>", "", body)
body = re.sub(r"<!--[\s\S]*?-->", "", body)
txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
```

然后查 6 项：

| 检查 | 期望 |
|---|---|
| 强制 CTA 两行 | 纯文本里逐字命中（各 ≥1 次） |
| Footer 行 | `www.SMThelp.com \| info@smthelp.com \| WhatsApp +86 13602562576 \| Shenzhen, China · Since 2011 \| CE` |
| 强制配套机型 | `pairing_required:true` 的机型，型号必须出现 |
| 禁用词 | `efficient / intelligent / excellent / leading / world-class / perfect / revolutionary / game-changing / cutting-edge` 全部 0 命中 |
| 最终价格 | `(USD\|US$\|$)\s?\d+` 0 命中 |
| 感叹号 | 正文 0（DOCTYPE 与注释里的 `!` 不算） |

**坑**：CTA 里的邮箱如果包成 `<a href="mailto:…">`，`grep` 整串会失败。
要么保持纯文本，要么先剥标签再比对——二者选一，不要靠肉眼。

---

## 7. 已知实现坑

- **跑马灯 clone 次数**：`foreach 原数组 { foreach 原数组 { clone } }` 会变成 N² 份（6→42）。
  正确写法是 `for pass in 0..1 { 原数组.forEach(clone) }` → 3 倍。
- **Hero 主视觉层级**：`.hero-visual` 是 `position:absolute z-index:10`，
  标题与底部按钮必须显式加 `position:relative; z-index:20`，否则移动端被机器图盖住。
- **字符渐显**只在叙事句上用，参数一律一次性可读、可截图转发。
- **变体对照表**：同一系列多个型号（如 S-WS450 A/C/M）不要塞进 7 行 Specs，
  单独做一张横向滚动表，`min-width:640px` 保证手机上可滑。
