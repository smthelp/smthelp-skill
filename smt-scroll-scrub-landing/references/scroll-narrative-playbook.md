# 滚动叙事分镜模板（按设备类型）

用法：选定机型 → 抄对应模板 → 填入 `S4 · 4A` prompt 的「分镜」占位处。
每一格 = 约 1 屏滚动（100 vh）。**每格必须有一个真实工艺动作 + 一个已核实参数**。

通用字段：

| 字段 | 说明 |
| --- | --- |
| 工序 | 真实工艺动作名，用英文术语 |
| 画面 | 生成/拍摄什么内容。优先 `ph.smthelp.com` 真实机器图，生成图仅用于氛围与剖切示意 |
| 上屏参数 | 只能来自 `verified-params.md`，否则写 `待确认` |
| 上屏文案 | 真 HTML 文字，≤ 12 词，删形容词保留结果 |
| 滚动作用 | 该格用什么手法推进（推近 / 平移 / 剖切 / 参数浮现） |

---

## 模板 A · 异形插件机 S-7900（4 头，4,000 CPH，±0.05 mm，98 N，AI vision，Active Clinching）

| # | 工序 | 画面 | 上屏参数 | 上屏文案 | 滚动作用 |
| --- | --- | --- | --- | --- | --- |
| 0 | Idle / whole machine | 车间光线下整机静态，机器在动 | `4 heads · 4,000 CPH` | Odd-form insertion, automated | 静止 Hero |
| 1 | Feeding | 推近送料区，管装料管上料 | `3–25 mm component range` | Handles relays, terminals, connectors | 推近 |
| 2 | Tube feeding detail | STF1003 供料器特写 | `0.8 s per component`（STF1003） | Continuous tube feeding | 剖切外壳 |
| 3 | Vision alignment | AI 视觉对位抓元件特写 | `±0.05 mm placement accuracy` | Vision-guided pick & place | 参数浮现 |
| 4 | Insertion | 插入瞬间，引脚穿板 | `98 N insertion force` | Stable insertion, no board lift | 慢放 |
| 5 | Clinching | Active Clinching 折弯机构 | `Active Clinching` | Clinched in-line, no second station | 剖切机构 |
| 6 | Board out | 出板，与下游交接 | `SMEMA interface` | Hands off to the next station | 平移出画 |
| 7 | CTA | 参数总览 + 单一 CTA | 全部已核实参数 | Talk to an engineer → | 定格 |

> ⚠️ S-7900 的 **适用板尺寸、换线时间、功率、气源要求** 不在已核实清单内 → 一律 `待确认`。

---

## 模板 B · 高速插件机 S-7020T（双头，12,000 CPH，±0.015 mm，vision correction）

| # | 工序 | 画面 | 上屏参数 | 上屏文案 | 滚动作用 |
| --- | --- | --- | --- | --- | --- |
| 0 | Whole machine | 整机 + 高速运动轨迹光轨 | `Dual head · 12,000 CPH` | High-speed radial insertion | 静止 Hero |
| 1 | Sequencing | 料站排序区 | `12,000 CPH` | Throughput for high-volume runs | 推近 |
| 2 | Vision correction | 视觉校正抓取瞬间 | `±0.015 mm accuracy` | Vision correction standard | 参数浮现 |
| 3 | Insertion | 端子/继电器座插入 | `Terminal & relay socket ready` | Connectors seated first time | 慢放 |
| 4 | Board out | 出板节拍 | `待确认`（换线与板尺寸） | Line-ready output | 平移 |
| 5 | CTA | 参数总览 + CTA | 已核实参数 | Get the spec sheet → | 定格 |

---

## 模板 C · 波峰焊 S-WS450（PCB 宽 450 mm，预热 ≤280 °C，锡炉 ≤300 °C，460 kg，双波峰，无铅）

| # | 工序 | 画面 | 上屏参数 | 上屏文案 | 滚动作用 |
| --- | --- | --- | --- | --- | --- |
| 0 | Whole machine | 整机 + 锡炉蒸汽 | `450 mm PCB width` | Lead-free wave soldering | 静止 Hero |
| 1 | Fluxing | 助焊剂喷涂区 | `Dual wave system` | Flux, preheat, solder in one pass | 推近 |
| 2 | Preheating | 预热区温度分层可视化 | `Preheat up to 280 °C` | Controlled thermal ramp | 热力图浮现 |
| 3 | Wave 1 (turbulent) | 第一波（湍流波）透视图 | `Solder pot capacity 460 kg` | Turbulent wave wets shadowed joints | 剖切锡炉 |
| 4 | Wave 2 (laminar) | 第二波（层流波） | `Solder up to 300 °C` | Laminar wave removes bridges | 剖切 |
| 5 | Cooling / out | 冷却出板 | `Lead-free process compatible` | RoHS-compliant joints | 平移 |
| 6 | Downstream | 与 SUL460 下板机交接 | `SUL460 · ~30 s magazine change` | No stacking at the exit | 推远 |
| 7 | CTA | 参数 + CTA | 已核实参数 | Request a process review → | 定格 |

> ⚠️ S-WS450 **链速（m/min）未核实**，涉及节拍计算时必须标 `待确认`。

---

## 模板 D · 管装供料器 STF1003（3×3×3–25×25×25 mm，0.8 s/件，±0.5 mm，弹簧寿命 400 万次）

| # | 工序 | 画面 | 上屏参数 | 上屏文案 | 滚动作用 |
| --- | --- | --- | --- | --- | --- |
| 0 | Unit on machine | 供料器装在插件机上 | `0.8 s per component` | Keeps the inserter fed | 静止 Hero |
| 1 | Tube load | 料管上料（PVC / 铝管） | `Tube length 200–650 mm` | PVC and aluminium tubes | 推近 |
| 2 | Component range | 不同尺寸元件排列 | `3×3×3 – 25×25×25 mm` | One feeder, wide component range | 网格浮现 |
| 3 | Feeding action | 步进推送元件 | `Stepper 57 · ≤600 rpm` | Four-speed adjustable feed | 剖切轨道 |
| 4 | Precision | 定位精度特写 | `±0.5 mm` | Repeatable pick position | 参数浮现 |
| 5 | Endurance | 老化测试 / 连续供料 | `1,000 cycles no fault · 48 h burn-in` | Tested before it ships | 定格 |
| 6 | Specs + CTA | 电气与气源 | `24 V · 0.4–0.6 MPa` | Get the datasheet → | 定格 |

---

## 模板 E · 整线方案（SMT line / THT line）

整线最多 7 屏，一屏一道工序。用**产线俯视推进**手法：镜头沿产线水平平移，滚动=沿产线走。

SMT 线：Loader → Printer → SPI（有需要才加）→ Pick & Place → Reflow → AOI → Buffer/Unloader
THT 线：Manual/Assisted insertion → Lead forming & cutting → Automatic insertion → Selective or wave soldering → Inspection → Test → Unloader/AGV

每格统一三段式：**这道工序做什么 → 为什么必须有（不做会怎样）→ 上下游怎么接**。

| # | 工序 | 上屏文案骨架 | 滚动作用 |
| --- | --- | --- | --- |
| 1 | Loader / conveyor | Board in, hands off the operator | 沿产线平移 |
| 2 | Printer | Paste deposition sets the yield ceiling | 推近钢网 |
| 3 | SPI（按需） | Catch paste defects before placement | 剖面示意，标注"justify by volume" |
| 4 | Pick & place | Placement accuracy drives first-pass yield | 俯视吸取动作 |
| 5 | Reflow | Thermal profile, not oven temperature | 温区曲线浮现 |
| 6 | AOI | Detect before it ships, not at the customer | 扫描线扫过 |
| 7 | Buffer / unloader / AGV | Buffer absorbs the mismatch between stations | 推远到全产线 |

> 整线页**不写总 CPH**，除非客户给了各站实际配置。改用：「Give me your target boards/hour and I'll size the line.」

---

## 通用手法库

| 手法 | 适用 | 说明 |
| --- | --- | --- |
| 推近（dolly in） | 从整机到某个工位 | 最安全，成本最低 |
| 剖切（cutaway / X-ray） | 展示机构原理 | 工业设备的"拆解"，工程师最爱看 |
| 参数浮现（spec reveal） | 每格落一个数字 | 必须配真 HTML 文字，字体层级统一 |
| 慢放（speed ramp） | 关键动作瞬间（插入、焊接、折弯） | 一页最多用 2 次，多了变炫技 |
| 沿产线平移（line dolly） | 整线方案 | 滚动距离 = 产线长度，直觉最强 |
| 热力/曲线浮现（data overlay） | 温度曲线、温区、节拍 | 用 SVG/CSS 做，不要烘进视频 |

**禁止**：零件炸开飞散（消费品类手法，工业设备显得不专业）、无工艺含义的旋转、超过 2 次的速度突变。
