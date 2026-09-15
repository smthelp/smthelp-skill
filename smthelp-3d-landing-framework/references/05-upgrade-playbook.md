# 05 · 升级手册

> 这个 skill 的设计前提是**模板与数据分离**。
> 绝大多数需求属于"加数据"，不需要改模板，更不需要改脚本。

## 升级决策树

```
需求是什么？
│
├─ 新增一个机型的落地页
│   └─ 加 machines/<MODEL>.json          ← 只加数据，零代码（见 §1）
│
├─ 改某个机型的参数 / 文案
│   └─ 改 machines/<MODEL>.json 的 fields
│
├─ 改版式：区块顺序、配色、字号、动效时长
│   └─ 改 templates/prompt-master-EN.md  ← 会影响所有机型（见 §2）
│
├─ 新增一种页面类型（整线页 / 索引页 / 案例页）
│   └─ 加 templates/<type>-EN.md + 机型 JSON 里 page_type 改掉（见 §3）
│
├─ 新增一条合规检查项
│   └─ 改 scripts/validate_prompt.py（见 §4）
│
└─ 品牌声纹变了（颜色/CTA/话术口径）
    └─ 改 smthelp-brand-voice，再同步本 skill 的 SKILL.md 与模板
```

每一次改动都要：更新 `CHANGELOG.md` + 升 `SKILL.md` 的 `version` 字段。

---

## §1 加一个机型（最常见）

### 步骤

1. 从术语库取参数。**只取「二·B 已确认参数锚点」表内的数字**：
   ```
   ~/.workbuddy/skills/smthelp-brand-voice/references/smt-term-bank.md
   ```
   不在表内的一律写 `On request`，并把这一项记进 `params_withheld`。

2. 复制最接近的现有机型：
   ```bash
   cp machines/S-7900.json machines/<MODEL>.json
   ```

3. 改这些字段：

   | 字段 | 说明 |
   |---|---|
   | `model` | 机型号，与文件名一致 |
   | `fields.MODEL` … `fields.MARQUEE_MEDIA` | 26 个占位符的值（见下表） |
   | `params_confirmed` | 列出每个数字来自哪个锚点，便于日后审计 |
   | `params_withheld` | 未确认项 + 原因；会打印到生成文件的"生成前请确认"区 |
   | `pairing_required` | S-WS450 / S-70LD 为 `true`，其余 `false` |
   | `notes` | 给自己的提醒（易错点、口径提醒） |
   | `updated` | 今天日期 |

4. 跑一遍：
   ```bash
   python3 scripts/build_prompt.py --model <MODEL> --validate
   ```
   出现 W1（七行参数全填了数字）时要逐条核对参数来源。

### 26 个字段速查

| 字段 | 含义 | 写作要点 |
|---|---|---|
| `MODEL` | Hero 大字机型 | 7 字符以内最佳，太长会让 13vw 标题溢出 |
| `PROCESS` | 工艺名 | 页面主叙事标题，如 `Wave Soldering` |
| `CATEGORY` | 产线段 | `THT LINE` / `SMT FEEDING` / `BOARD HANDLING` / `CLEANING` |
| `ONE_LINER` | Hero 左下定位句 | **机型 + 2 个关键参数 + 一个工况词**，≤ 20 词 |
| `NARRATIVE` | 工艺叙事 | **2 句，不含数字**；讲动作序列，不讲卖点 |
| `HOTSPOT_1..3` | 设备图标注 | 短标签，≤ 6 词 |
| `CORNER_1..4` | 四角技术卡 | 格式 `标签 / 数值`，数值用 `#90C641` |
| `SPEC_01..07` | 参数墙 7 行 | 格式 `NN  参数名(左对齐)  数值+单位` |
| `PAIRING` | 推荐/强制配套 | 空字符串 → 脚本自动删掉整行 |
| `APP_01..03` | 应用场景 | 垂直行业 + 板卡类型，不是抽象能力词 |
| `HERO_MEDIA` | Hero 素材描述 | 明确到视角与格式（3/4 去背 / MP4 / 渲染） |
| `MARQUEE_MEDIA` | 跑马灯素材清单 | 6–8 个具体镜头，`/` 分隔 |

### 参数墙写作规范

- 必须 **7 行**（模板里写死 7 个 `[SPEC_NN]`）。参数不够时，用 `On request` 占位行补齐。
- 参数名左对齐到同一列，方便生成后被 LLM 稳定解析。
- 数值一律带单位（`450 mm` / `280 C` / `0.8 s per component` / `< 500 PPM`）。
- 组合值写清楚归属，如 `FEEDING ACCURACY  +-0.5 mm`（不是 `ACCURACY`）。

---

## §2 改版式（影响所有机型）

改 `templates/prompt-master-EN.md` 里 `<!-- BEGIN PROMPT -->` 与 `<!-- END PROMPT -->` 之间的内容。

### 改之前先问三个问题

1. **是否违反硬约束？** 对照 `references/04-compliance-and-copy.md`
2. **是否破坏了占位符契约？** 删掉某个 `[SPEC_05]` 会让所有机型的脚本报错（缺字段/残留占位符）
3. **是否需要所有机型重新生成？** 改版式后建议：
   ```bash
   python3 scripts/build_prompt.py --all --out-dir /tmp/regression --validate
   ```
   全部通过再提交。

### 常见版式改动

| 想改什么 | 改哪里 |
|---|---|
| 配色 | `GLOBAL STYLES` 段的 6 个色值 |
| 字号节奏 | 各段 `clamp()` 与 `text-[Nvw]` |
| 区块顺序 | `SECTION ORDER` + 对应的 `N. XXX SECTION` 编号 |
| 增减区块 | 加/删整段，同步更新 `SECTION ORDER` |
| 动效时长 | `FadeIn` 的 `duration` 与各处 `delay` |
| 滚动灵敏度 | `2. TRUST MARQUEE` 的 `* 0.25` |

### 加一个新的占位符

1. 模板里写 `[NEW_FIELD]`
2. `scripts/build_prompt.py` 的 `REQUIRED` 或 `OPTIONAL` 列表里加上
3. **所有现有机型 JSON 都要补这个字段**（放 `REQUIRED` 时会强制报错提醒你）
4. 更新本文件 §1 的字段速查表

---

## §3 加一种页面类型

当前只有 `single-machine`。加新类型：

1. 新建 `templates/<type>-EN.md`，沿用 `<!-- BEGIN PROMPT -->` / `<!-- END PROMPT -->` 标记
2. 机型 JSON 里 `page_type` 改成新类型，`fields` 按新模板的占位符给
3. `scripts/build_prompt.py` 增加 `--template` 参数（或按 `page_type` 自动选模板）

### 已规划但未实现的类型

| 类型 | 与单机型的差异 |
|---|---|
| **整线方案页** `turnkey-line` | Specs → 产线布局图 + 工序链 + 节拍平衡表；新增瓶颈工序分析段；ROI 段更重（整线 CapEx、投资回收）；FAQ 增加"分期实施" |
| **全产品索引页** `catalog` | Hero → 多机型卡片 + 分类筛选；去掉 Hotspot 与四角卡；Application 叠卡换成产品族 |
| **客户案例页** `case-study` | Hero → 客户行业 + 结果数字；新增 Before/After 对比段；Specs 换成"部署清单" |

实现任一种时，先复制 `prompt-master-EN.md` 改名，再按差异改，最后补 `--template` 路由。

---

## §4 加一条合规检查

改 `scripts/validate_prompt.py`：

- **硬错误** → 加进 `errors`（前缀 `E`），会让 CI 与 `--validate` 失败
- **提醒** → 加进 `warnings`（前缀 `W`），只在 `--strict` 下失败

两个必须注意的陷阱：

1. **模板自列举造成的误报**
   模板里的 `COPY RULES` 会把禁用词列成负面清单，自检时必须先挖掉那一行（已用 `BANNED_LIST_RE` 处理）。新增同类规则时照做。

2. **CSS 类名造成的误报**
   `leading-none` / `tracking-wide` 这类 Tailwind 类名会命中禁用词。英文词检查必须用
   `(?<![-\w])word(?![-\w])` 的词边界，不能用 `in` 子串判断。

新增检查后跑一遍全量回归：

```bash
python3 scripts/build_prompt.py --all --out-dir /tmp/regression --validate
```

---

## §5 版本号规则

`MAJOR.MINOR.PATCH`

| 变更 | 段 |
|---|---|
| 加机型 / 改某个机型数据 | PATCH |
| 加页面类型 / 加自检项 / 改版式（不破坏字段契约） | MINOR |
| 改占位符契约 / 重构目录结构 / 换底层框架 | MAJOR |

改完同步：`SKILL.md` 的 `version` 字段 + `CHANGELOG.md`。
