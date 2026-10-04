---
name: smthelp-3d-landing-framework
description: "SMT/THT 单机型产品 3D 落地页生成器：把 3D Creator 风格作品集页框架改造为 B2B 工业设备页。机型数据 + 主模板 → 一键生成可直接粘进 open-design / DSH / Cursor / v0 的英文 Prompt，并跑合规自检。内置 10 个机型（S-WS450 / S-70LD / S-7900 / S-7020T / S-3000 / STF1003 / BF-2002D / SUL460 / SME5200 / SFY03）。触发词：3D 落地页、产品落地页、landing page prompt、机型页、S-WS450 落地页、S-70LD 落地页。"
version: 1.4.0
agent_created: true
---

# Southern Machinery 3D 落地页框架（单机型产品页）

从 Azou《DeepSeek Harness 工具包》第 5 节的 "3D Creator-style portfolio landing page" Prompt Spec 改造而来的**工业 B2B 版本**。

原框架服务个人 IP 作品集（抽象 3D 肖像 + 抽象动效 GIF + 课程/项目列表）。
本框架服务海外 EMS / ODM 工厂的采购经理与工艺工程师。

**改造主线**：把"炫技的 3D 装饰"换成"可信的设备证据"，把"人格叙事"换成"参数与 ROI"。

---

## 标准工作流（先走这条）

```bash
PY=/Users/mac/.workbuddy/binaries/python/versions/3.13.12/bin/python3
cd ~/.workbuddy/skills/smthelp-3d-landing-framework

$PY scripts/build_prompt.py --list                                  # 1. 看有哪些机型
$PY scripts/build_prompt.py --model S-WS450 --validate              # 2. 生成 + 自检
$PY scripts/build_prompt.py --model S-WS450 --out ~/Desktop/x.md    # 3. 落盘
$PY scripts/build_prompt.py --all --out-dir ~/Desktop/sm-lp         #    或批量
```

生成的 Prompt 整段粘进 open-design / DSH / Cursor / v0 / Bolt 即可。

**新机型不要改模板**，复制一份 `machines/S-7900.json` 改字段即可（见 `references/05-upgrade-playbook.md`）。

---

## 硬约束（随时可能忘，写在这里）

1. **参数溯源**：只取 `smthelp-brand-voice` 术语库「已确认参数锚点」。表外一律 `On request`。
   - **S-WS450 的 Conveyor Speed（m/min）未确认 → 必须写 `On request`**
   - **S-3000 的 18,000 PCS/H 是轴向理论峰值 → 禁止当 headline，只用实测 10,000–12,000 CPH**
   - **S-70LD 的 ±0.5 mm 是 STF1003 供料精度，不是插件头精度 → 必须标注 `FEEDING ACCURACY`**
2. **报价熔断**：页面无最终价，只有预算区间 + 三问（PCB 尺寸 / 目标产能 / 现有线体品牌与 feeder 型号）。
3. **整线连带**：S-WS450 页必带 SUL460；S-70LD 页必带 STF1003（见 JSON 的 `pairing_required`）。
4. **强制 CTA 两行原文**必须逐字保留：
   ```
   Note: This configuration is a draft and must be finalized and reviewed by our senior Sales Engineer (Jason Wu).
   Action Required: Please provide your Gerber file or PCB drawings to info@smthelp.com for an accurate capacity simulation and nozzle engineering validation.
   ```
5. **术语不翻译**：Wave Soldering / Preheat / Solder Pot / Flux / Dross / Conveyor / PCB / THT / SMD / CPH / UPH / Odd-form / Magazine / Feeder / Nozzle / Pitch。
6. **Hero 必须是设备本体**（3/4 视角渲染 / 实拍去背 / 运行 MP4），禁止抽象 3D 卡通形象与装饰粒子。
7. **首屏高度用 `100svh`**，不用 `100vh`（移动端 LinkedIn / 微信内置浏览器地址栏会跳动）。

---

## 品牌色板

| 变量 | 色值 | 用途 |
|---|---|---|
| `--ink` | `#0B0E0F` | 页面底色、深色区块 |
| `--steel-dark` | `#5C6E73` | 标题渐变起点 |
| `--steel-light` | `#D9E4EA` | 标题渐变终点 |
| `--text` | `#D7E2EA` | 正文 |
| `--teal` | `#0AA5A5` | 链接、参数数值、焦点色 |
| `--green` | `#90C641` | 数值强调、Hotspot 点、CTA 高光 |

字体 `'Archivo'` 300–900。CTA 渐变 `linear-gradient(123deg, #06282A 7%, #0AA5A5 37%, #6FA832 72%, #90C641 100%)`。

## 区块顺序（单机型页 8 段）

```
1 HeroSection       深色  机型大字 + 设备主视觉(Magnet+Hotspot) + CTA
2 TrustMarquee      深色  真实动作素材双向滚动 + 资质跑马灯
3 ProcessSection    深色  工艺原理(字符渐显) + 四角技术标注卡
4 SpecsSection      浅色  编号参数墙(溯源标注)
5 RoiSection        深色  CapEx/回本/服务 + 报价熔断条
6 ApplicationStack  深色  3 张粘性叠卡(垂直行业工况)
7 FaqSection        浅色  6 问手风琴
8 QuoteSection      深色  询盘表单 + 强制 CTA + Footer
```

## 关键改造点（相对原框架）

| 原框架 | 改为 | 原因 |
|---|---|---|
| 抽象 3D 肖像 + Magnet | 设备主视觉 + Magnet + Hotspot 参数标注 | 工程师要看到机器本体 |
| 21 张抽象动效 GIF | 6–12 条真实设备动作素材 | 前 3 秒必须是机器在动 |
| 滚动系数 `0.3` | **`0.25`** | 工业实拍比抽象图更晃眼 |
| 字符渐显长段落 | 只用于 2–3 句工艺叙事 | 参数必须一次性可读、可截图 |
| Tracks 编号列表 | Specs 编号参数墙 + 溯源标注 | 采购第一动作是扫参数 |
| Projects 叠卡 | 应用场景叠卡（真实产线照片） | 禁 Unsplash 抽象图 |
| 紫橙渐变 JoinButton | Teal→Green QuoteButton | 品牌色 |
| — | 新增 Trust / ROI / 报价熔断 / FAQ / sticky WhatsApp | B2B 决策必需 |

---

## 目录

| 路径 | 内容 |
|---|---|
| `templates/prompt-master-EN.md` | **唯一真源**占位符模板。只在这里改版式/区块/动效 |
| `machines/*.json` | 机型数据（10 个）。新增机型只加文件，不改代码 |
| `scripts/build_prompt.py` | 模板 + 数据 → 可执行 Prompt |
| `scripts/validate_prompt.py` | 合规自检（E1–E5 硬错误 / W1–W4 提醒） |
| `references/01-block-mapping.md` | 原框架 → B2B 的完整映射与改造原理 |
| `references/02-section-specs.md` | 8 段区块的详细规格（含具体 class 与 clamp 值） |
| `references/03-components-and-tech.md` | 组件、性能、降级、SEO |
| `references/04-compliance-and-copy.md` | 参数溯源、报价熔断、CTA、禁用词表 |
| `references/05-upgrade-playbook.md` | **如何升级**：加机型 / 改版式 / 加页面类型 |
| `references/06-html-render-spec.md` | Prompt → 单文件 HTML 的原生实现、素材槽位约定、交付校验 |
| `references/07-resource-pipeline.md` | YouTube 视频板 + Product Catalog 板抓取、ph.smthelp.com 回退、Chatwoot 接入、SEO 命名规则 |
| `references/08-dan-koe-blog.md` | 六步法段落映射、标题硬约束（6 词禁列）、折叠实现、选题矩阵、发布自检 |
| `references/09-deploy-github-pages.md` | **发布**：PAT 授权、仓库结构、Pages 源分支陷阱、空提交触发重建、上线核验清单 |
| `CHANGELOG.md` | 版本记录 |

## 相关 skill

- `smthelp-brand-voice` — 参数锚点、报价熔断、强制 CTA（硬约束的来源，改参数必查）
- `smthelp-product-copywriting` — 落地页文案结构与字段
- `smthelp-english-humanizer` — 英文去 AI 味（**注意：不要让它砍掉强制 CTA 与三问**）
