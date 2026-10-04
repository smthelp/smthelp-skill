# 08 · Dan Koe 六步法博客块（嵌入落地页）

> 用途：把外部导流来的访问者转化为"读过 → 信了 → 询价"，
> 用 3 篇按 Hook → Diagnosis → Framework → Vehicle → Loop → CTA 结构的短博客
> 直接嵌在产品落地页里（`<details>` 可折叠，SEO 友好，正文始终在 DOM 里）。

---

## 1. 为什么直接嵌，不另开 `/blog`

- B2B 决策周期短：买家查一个产品页，看完参数 5 分钟内决定是否询价。把博客
  嵌在页面内能把"看完规格 → 看懂工艺 → 联系我们"压在同一次滚动里。
- 离站：外链到 `/blog` 会丢 30–60% 跳出，站内嵌入可降到 5%。
- SEO：内容进 DOM（即使折叠）也能被 Google 抓取，关键词密度自然提升。

---

## 2. 六步法 → 段落映射

每篇博客 5 个段落（CTA 由全页统一 CTA 区负责，不在博客内重复）：

| 步骤 | 段落职责 | 写法提示 | 字数 |
|---|---|---|---|
| **Hook** | 三秒抓注意力：抛一个反常识观察或画面 | "The line is running, but the joints say otherwise." | 30–50 词 |
| **Diagnosis** | 说痛、让对方觉得"这说的就是我" | 拆 2–4 个真实原因，避免抽象 | 80–120 词 |
| **Framework** | 给可复用的解决法（**不是**情绪） | 编号 / 步骤 / 比例 / "rule of thumb" | 80–120 词 |
| **Vehicle** | 把框架装进具体产品 | 列 2–3 个该机型实测参数 + 视频链接 | 80–120 词 |
| **Loop** | 老用户怎么回来 | 订阅 / 季度复盘 / 下次再访理由 | 30–50 词 |
| **CTA** | 明确下一步 | "Email X to info@smthelp.com" | 1 行 |

总字数 350–550 词一篇，过长会压垮其它区块，过短缺乏说服力。

---

## 3. 标题硬约束（写完必检）

**标题里禁止出现这 6 个词**：hook / diagnosis / framework / vehicle / loop / CTA。

要避开的原因：标签会破坏叙事张力、读者会觉得是模板填充、
、和真实工程师语言的距离拉远。

替代写法：
- Hook → "It's rarely the alloy" / "Why a 450 kg pot changes everything" / "Add THT in 3 answers"
- Diagnosis → 用 "the actual cause is..." "what's really happening...""
- Framework → 用 "rule of thumb" "4-knob inspection" "3 answers"
- Vehicle → 用品牌词 + 数字 + 工艺词
- Loop → 用 "next time" "each quarter" "next contract"
- CTA → 直接行动 "Email X" "Reply with Y"

落地页发布前必跑：
```bash
grep -wE "hook|diagnosis|framework|vehicle|loop|cta" blogs.html
```
期待无命中。

---

## 4. 折叠实现（无 JS 也可读）

用原生 `<details>`/`<summary>`：

```html
<details class="ins-card">
  <summary>
    <span class="ins-kicker">Insight 01 · Joint quality</span>
    <span class="ins-title">Grey, dull joints after the wave? It's rarely the alloy</span>
  </summary>
  <div class="ins-body">
    <p><span class="pull">The stop-the-line moment.</span> ...</p>
    <p>...</p>
  </div>
</details>
```

要点：
- 标题在 `<summary>` 里，搜索引擎可见，读者第一眼能扫。
- 折叠默认收起；点开看长文。LCP 友好。
- 想 SEO 抓取也无所谓——内容始终在 DOM，CSS 控制可见性。

JS 增强（可选）：点击 summary 时改 `data-open` 属性，CSS 据此显示"收起"按钮文案。
不写 JS 也能正常工作。

---

## 5. 与强制 CTA 的边界

每篇博客最后一段的 CTA 必须引导到**全页 CTA 区**（quote 区块），而不是另开一个
"立即购买"按钮——避免一个页面出现 5 个询价入口，转化反而下降。

**Blog 内部可写动作引导**（"Email X" / "Send the trace"），
但**按钮只在 quote 区块**出现一次；强制 CTA 两行文字（Jason Wu / Gerber 文件）也
只在 quote 区块出现一次。

---

## 6. 选题矩阵（落到 S-WS450 上）

每篇博客主关键词各不相同，避免互抢：

| 博客 | 主关键词 | 目标痛点 |
|---|---|---|
| 01 | Joint quality / grey solder joints | 工艺缺陷归因 |
| 02 | Heavy board / solder pot capacity | 选型失误 |
| 03 | SMT + THT line integration | 加线规划 |

**选题三指标**（取自 `smthelp-hook-angle-lab`）：
- 覆盖面：这个痛点覆盖目标客户多广？— 用工艺词命中搜索流量
- 决策相关性：买家在哪个阶段会读这篇？— 选型阶段（不是售后阶段）
- 可验证性：内容能不能引用真实数据？— 必须能，否则不写

---

## 7. 发布前自检清单

- [ ] 标题不含 hook/diagnosis/framework/vehicle/loop/cta（grep 必 0 命中）
- [ ] 6 段顺序正确（Hook→Diagnosis→Framework→Vehicle→Loop→CTA）
- [ ] Vehicle 段引用了至少 2 个该机型的**已确认参数**（不引用 `On request`）
- [ ] 段落字数 30–120 词，总字数 350–550
- [ ] 全篇没有禁用词（efficient / intelligent / excellent / leading / world-class / perfect / revolutionary / game-changing / cutting-edge）
- [ ] 正文 0 感叹号
- [ ] CTA 指向 quote 区块，不在本博客卡片内重复
- [ ] Loop 段给出具体回访动作（订阅 / 季度复盘 / 下个合同）
- [ ] 移动端 <details> 仍可点击展开（不要用 `display:none` 隐藏 summary）