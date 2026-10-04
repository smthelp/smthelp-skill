# 04 · 参数溯源、报价熔断、CTA 与文案硬约束

> 这一节是**业务合规**，不是设计偏好。违反会让页面变成法律风险或信任事故。
> 权威来源：`~/.workbuddy/skills/smthelp-brand-voice/references/smt-term-bank.md`

## 一、参数溯源（最重要）

**只能引用术语库「二·B 已确认参数锚点」表内的数字。** 表外一律写：

- 英文页面 → `On request`
- 中文页面 → `以技术规格书为准`

禁止三种行为：
1. 凭印象补数字
2. 从竞品资料推算
3. 把相近机型的参数套用过来

### 高频踩坑

| 机型 | 坑 | 正确写法 |
|---|---|---|
| **S-WS450** | 链速（m/min）**不在**已确认清单 | `CONVEYOR SPEED · On request` |
| **S-3000** | `18,000 PCS/H` 是**轴向条件下的理论峰值** | 只用实测 `10,000–12,000 CPH (measured)` |
| **S-70LD** | `±0.5 mm` 是 **STF1003 供料精度**，不是插件头精度 | 参数名必须写 `FEEDING ACCURACY` |
| **精度** | 精度必须绑机型 | S-7900 `±0.05 mm`、S-7020T `±0.015 mm`、供料器 `±0.5 mm` |
| **0.4 mm pitch BGA** | 是 SMT 贴片机指标，也是**客户 PCB 的**属性 | 不能用来佐证 THT 插件机；描述客户现状时要写明归属 `your 0.4 mm pitch BGA` |

### 客户侧数据必须标明归属

下列数字是**要向客户问的**，不是我方设备规格：

`0.4 / 0.5 mm pitch BGA` · `0201 / 01005` · `300 mm 板长` · `30,000 CPH`

写法：`your 0.4 mm pitch BGA`、`if your SMT line runs at 30,000 CPH`。
**禁止**挪到我方设备上当卖点。

## 二、报价熔断

**全页禁止出现最终价格。** 只允许：

- 预算区间 + 说明 `Final quote depends on process options.`
- 内部参考锚点（35K CPH 整线 ≈ $163,888 / 25K CPH ≈ $138,800）**只能内部用，不得上页**

客户直接问价 → 先反问三项契约数据：

1. PCB 尺寸范围、是否双面元件、最小元件尺寸（0201 / 01005 / 0.4 mm pitch BGA）
2. 目标产能（CPH 或月产量）
3. 是否需兼容现有 Yamaha / JUKI / Panasonic 线体与 Feeders

客户拒绝提供 → 只给标准机型基础参数 + 预算区间，注明取决于工艺选配。

## 三、强制 CTA（逐字保留，不得改写、不得精简）

```
Note: This configuration is a draft and must be finalized and reviewed by our senior Sales Engineer (Jason Wu).
Action Required: Please provide your Gerber file or PCB drawings to info@smthelp.com for an accurate capacity simulation and nozzle engineering validation.
```

⚠️ 用 `smthelp-english-humanizer` 润色时必须**显式豁免**这两行——它不是套话，是业务合规项。

## 四、整线连带

| 主推机型 | 强制配套 | 依据 |
|---|---|---|
| **S-70LD**（odd-form insertion） | **STF1003** Tube Feeder | 防止插件机缺料停机 |
| **S-WS450**（wave soldering） | **SUL460** Magazine Unloader | 防止波峰焊出口堆料 |

在 `machines/*.json` 里用 `pairing_required: true` 标记，`validate_prompt.py` 会检查输出里是否有 `Recommended pairing` 行。

产线设计的固定动作：识别瓶颈工序 → 匹配上下料节拍（SUL460 料框切换约 30 秒）→ 补齐强制配套件 → **瓶颈工序留 20% 产能余量**。

## 五、价值锚定

给任何价格区间时必须同时给三条：

- **源头锚点**：Shenzhen-based manufacturer，深圳源头工厂直发
- **售后锚点**：Global Service & Support，全球现场与远程支持
- **ROI 陈述**：换算成客户当地人工成本的回本周期（2–3 年）

## 六、文案硬约束

### 术语不翻译

`Wave Soldering` / `Preheat` / `Solder Pot` / `Flux` / `Dross` / `Conveyor` / `PCB` / `THT` / `SMD` / `CPH` / `UPH` / `Odd-form` / `Magazine` / `Feeder` / `Nozzle` / `Pitch` / `Pick-and-place` / `Reflow` / `AOI` / `SPI` / `Gerber` / `BGA` / `QFP` / `EMS` / `Turnkey Line`

首次出现可加一次中文注释，之后不再重复。翻译失真会让海外工程师怀疑专业性。

### 禁用词（出现即删）

| 类别 | 词 |
|---|---|
| 空洞形容词 | 高效 / 智能 / 卓越 / 领先 / 一流 / 完美 / 革命性 / 颠覆 / 赋能 |
| AI 腔套话 | 在当今时代 / 随着…的发展 / 值得注意的是 / 综上所述 / 不仅仅是…更是… |
| 绝对化用语（违反广告法 + 平台规则） | 最好 / 第一 / 顶级 / 唯一 / 根治 / 永不 |
| 英文对应 | efficient / intelligent / excellent / leading / world-class / perfect / revolutionary / game-changing / cutting-edge / state-of-the-art / unmatched |

**替代规则**：删掉形容词，补一个**数字、工况或结果**。

```
✗ 这款设备效率极高，大幅提升产能。
✓ S-70LD 配 STF1003 tube feeder，供料节拍 0.8 s/件，替代人工插件工位。
```

### 单位与写法

- 供料节拍 `0.8 s/件`；产能 `4,000 CPH`；精度 `±0.05 mm`
- **`CPH`（点数）与 `UPH`（板数）不得混用**
- 温度用 `°C`，温区写 `top-side preheat`
- 尺寸用 `mm`
- **金额统一 USD**，不写 RMB

### 语气

- 读者是工艺工程师，不是冲动消费者
- **禁止**感叹号堆砌、emoji、"家人们"式口吻
- 公司背景（2011 年成立于深圳）放结尾信任段，一句话带过，**不要开场**
- 提及竞品写品牌原名，不贬损，只做参数/成本/交期/服务响应对比
  - ✓ `If you are running an existing Yamaha line, our feeder interface can be adapted — please send your feeder model list.`
  - ✗ `Our machine is better than Yamaha.`

## 七、自动自检

`scripts/validate_prompt.py` 覆盖下列检查：

| 码 | 级别 | 检查 |
|---|---|---|
| E1 | ❌ | 残留未替换占位符 |
| E2 | ❌ | 强制 CTA 两行缺失或被改写 |
| E3 | ❌ | 出现最终价格（USD 数字） |
| E4 | ❌ | 禁用空洞形容词（中英，自动排除 CSS 类名如 `leading-none`） |
| E5 | ❌ | `pairing_required: true` 但输出没有 `Recommended pairing` 行 |
| W1 | ⚠️ | 七行参数全填了数字 → 提醒逐条核对是否都来自已确认锚点 |
| W2 | ⚠️ | 参数墙里 CPH 与 UPH 同时出现 |
| W3 | ⚠️ | 缺少 WhatsApp / info@smthelp.com |
| W4 | ⚠️ | 带单位的数字少于 6 处 |

```bash
python3 scripts/validate_prompt.py --file generated.md            # WARNING 不阻断
python3 scripts/validate_prompt.py --file generated.md --strict   # WARNING 也当失败
```
