# 滚动驱动实现骨架、性能预算与降级

## 一、三种实现，按场景选

| 方案 | 适用场景 | 优点 | 风险 |
| --- | --- | --- | --- |
| **A. `<video>` + `currentTime` scrub** | Hero 主影片（默认推荐） | 一个文件、天然双向可逆、成本最低 | 必须 `preload="auto"`，否则拖动会卡；体积敏感 |
| **B. 图像序列（帧序列）** | 剖切示意、逐帧精确控制的段落 | 每一帧可控、可换单帧 | 请求数多，需预加载；体积大 |
| **C. 纯 CSS/JS 分层位移** | 参数浮现、文字节奏、轻量动效 | 零媒体体积、最稳 | 做不了真实机器运动 |

**默认组合**：Hero 用 A，剖切段用 B，文字/参数段用 C。不要混合在同一滚动段里。

---

## 二、方案 A 骨架（video scrub）

```html
<section class="scrub-hero" id="hero">
  <div class="scrub-sticky">
    <video id="heroVideo" muted playsinline preload="auto"
           poster="poster.webp" src="hero-1080p.mp4"></video>
    <!-- 参数/文案层：真 HTML，可复制可搜索 -->
    <div class="scrub-caption" data-at="0.15">
      <p class="kicker">Tube feeding</p>
      <p class="spec">0.8 s per component <span class="unit">STF1003</span></p>
    </div>
    <!-- 其余 data-at 节点按分镜表追加 -->
  </div>
</section>
```

```css
.scrub-hero { height: 400vh; }            /* 单 Hero ≤ 4 屏 */
.scrub-sticky { position: sticky; top: 0; height: 100vh; overflow: hidden; }
#heroVideo { width: 100%; height: 100%; object-fit: cover; display: block; }
.scrub-caption { position: absolute; opacity: 0; transition: opacity .25s ease; }
.scrub-caption.is-on { opacity: 1; }
```

```js
const v = document.getElementById('heroVideo');
const hero = document.getElementById('hero');
const caps = [...document.querySelectorAll('.scrub-caption')];

// 视频元数据就绪后再绑定，否则 duration 是 NaN
let ready = false;
v.addEventListener('loadedmetadata', () => { ready = true; v.currentTime = 0; });

let raf = null;
function onScroll() {
  if (raf) return;
  raf = requestAnimationFrame(() => {
    raf = null;
    if (!ready) return;
    const r = hero.getBoundingClientRect();
    const total = hero.offsetHeight - window.innerHeight;
    const p = Math.min(1, Math.max(0, -r.top / total));   // 0..1，双向
    if (Number.isFinite(v.duration)) {
      v.currentTime = v.duration * p;                      // 回滚即还原
    }
    for (const c of caps) {
      const at = parseFloat(c.dataset.at);
      c.classList.toggle('is-on', p >= at && p < at + 0.18);
    }
  });
}
addEventListener('scroll', onScroll, { passive: true });
addEventListener('resize', onScroll);
```

**关键点**
- `preload="auto"` 是硬要求。lazy 会让 scrub 卡成幻灯片。
- `muted` + `playsinline` 必须有，否则 iOS Safari 会全屏接管。
- 用 `duration` 映射而非硬编码帧数，换文件不用改代码。
- 不要在 scroll 回调里直接操作 DOM，用 `requestAnimationFrame` 节流。

---

## 三、方案 B 骨架（帧序列，用于剖切段）

```js
const frames = 48;                       // 分镜格数 × 每格帧数
const img = document.getElementById('seq');
const pre = [];
for (let i = 0; i < frames; i++) {
  const im = new Image();
  im.src = `frames/seq_${String(i).padStart(3,'0')}.webp`;
  pre.push(im);
}
// 滚动时：const idx = Math.min(frames - 1, Math.floor(p * frames));
// img.src = pre[idx].src;  （已进缓存，切换无网络等待）
```

帧数控制在 **48 帧以内**，WebP，单帧 ≤ 60 KB。超过就改用方案 A。

---

## 四、移动端降级（必做）

```css
@media (max-width: 768px), (prefers-reduced-motion: reduce) {
  .scrub-hero { height: auto; }
  .scrub-sticky { position: static; height: auto; }
  #heroVideo { display: none; }          /* 不加载影片 */
  .scrub-hero { background: url('poster.webp') center/cover no-repeat; }
  .scrub-caption { position: static; opacity: 1; }   /* 改为常规图文流 */
}
```

JS 侧同时跳过视频加载：

```js
const isMobile = matchMedia('(max-width: 768px), (prefers-reduced-motion: reduce)').matches;
if (!isMobile) { /* 才绑定 scroll scrub 与 video 加载 */ }
```

`prefers-reduced-motion` 必须尊重——部分企业 IT 策略强制开启。

---

## 五、性能预算（硬上限）

海外 EMS 工厂网络与展会 wifi 是真实约束，按最坏情况（约 5 Mbps）设计。

| 资源 | 上限 |
| --- | --- |
| Hero 视频 | ≤ 6 MB（1080p / H.264 mp4 + WebM 备源，≤ 12 s） |
| Poster 图 | ≤ 200 KB（WebP） |
| 帧序列总量 | ≤ 3 MB（≤48 帧 × ≤60 KB） |
| 首屏 JS + CSS | ≤ 150 KB（未压缩） |
| 首屏可交互 | 展会 wifi 下 ≤ 3 s |
| Lighthouse 移动端 | Performance ≥ 80 |

优化动作：视频去掉音轨、CRF 26–28、关键帧间隔 1 s（scrub 更顺）；图片全部 WebP + `width/height` 属性防抖动；字体 `font-display: swap`，中英混排只加载用到的字重。

---

## 六、SEO 与可访问性（外贸站不能省）

- 标题/参数/CTA **全部真 HTML**，`<h1>` 唯一，型号名进 `<title>` 与 `<h1>`
- 视频加 `aria-label`，滚动段外层给 `<section>` 加语义化标题（可用 `.sr-only` 隐藏）
- 每个产品页加 `Product` 结构化数据（JSON-LD）：`name` / `brand` / `model` / `description`
- 图片 `alt` 写实："S-7900 odd-form insertion machine on an EMS line"，不要 "image1"
- 中英双版本用 `hreflang` 标注，不要靠 JS 切语言

---

## 七、截图比对规范（每步必做）

```bash
# 无头浏览器截图，与 reference/ 下的参考图并排比对
npx playwright screenshot --viewport-size=1920,1080 \
  --full-page=false http://localhost:PORT hero.png
```

规则：
- **1920×1080 只用于比对截图，绝不是页面尺寸**
- 滚动段至少截 3 个位置：0% / 50% / 100%
- 页面用相对单位（`rem` / `vw` / `%`），无固定像素宽高，无横向滚动条
- 没亲自看过两张图，不许说"匹配了"

---

## 八、备份规范

每次改动**前**：

```bash
mkdir -p backups/$(date +%Y%m%d-%H%M%S)
cp -r index.html assets/ backups/$(date +%Y%m%d-%H%M%S)/
```

`backups/` 加入 `.gitignore`（不进仓库）。
