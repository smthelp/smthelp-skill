---
name: inquiry-to-proposal
description: Turn a new customer's inquiry email into a four-part B2B sales pack for Southern Machinery - (1) company background check with sources and confidence, (2) contact persona, (3) product-solution match against the Southern Machinery SMT/THT catalogue with honest fit limits, (4) staged follow-up plan plus a ready-to-send English reply email. Use when Jason pastes or forwards a customer inquiry / RFI / RFQ and says 背调, 客户分析, 询盘分析, 联系人画像, 匹配方案, 跟进计划, 回复邮件, or just "按询盘项目处理".
metadata:
  version: 1.0.0
  updated: 2026-10-15
  owner: Jason Wu (Southern Machinery)
  first_case: examples/hirschmann-automotive-2026-10.md
---

# Inquiry → Proposal（新客户询盘四件套）

输入：客户的初始询盘邮件（可含催复邮件链、附件、签名档）。
输出：中文结构化分析（四节）+ 一封英文回复邮件（可直接复制发送）。不确定信息一律标 **待确认**。

## Workflow

1. **拆邮件（5 分钟内完成）**
   - 列出：发件人、职位、公司实体与地址、抄送人、首发日期、催复次数、我方是否已回复、是否群发（"Dear Sir or Madam"、无我司名称 = 群发 RFI）。
   - 判定询盘性质：RFI（市场摸底）/ RFQ（要报价）/ 具体订单 / 备件询价。决定回复深度与紧迫度。
   - 把客户的需求逐条抄成"需求清单"（明确需求 + 隐含需求，例如"标准化"背后是降本、降风险）。
   - 找"一票否决点"：客户明确排除的东西（如"connector stitching, not PCB stitching"）。这一点决定后面整个匹配的诚实度。

2. **客户背调**（web_search / web_fetch，最多 6–8 次检索；方法见 `references/research-sources.md`）
   - 集团 + 发件工厂分开查：成立时间、股权、行业、员工、工厂、营收趋势、利润、终端客户。
   - 每个事实带：来源 + 可信度（高 = 官网/年报/工商；中 = 第三方数据库/新闻；低 = 推测）。
   - 推断采购规模、预算窗口、经营压力，必须标"推测"。
   - 列"信息缺口"。

3. **决策链与联系人画像**
   - 用 LinkedIn / XING / FinalScout 检索每个收件人、抄送人的职位，排出：经济决策人、技术评估人、发起人、执行人。
   - 主联系人画像：职权范围、沟通风格（从措辞、催复频率判断）、痛点、关注点、潜在异议、性格与采购意向（标"推测"）、对应打法。

4. **匹配方案**（产品库见 `references/product-library.md`，先读它）
   - 先写"关键判断"：我司产品与客户需求的真实匹配程度，包括不合适的部分。
   - 推荐清单表：产品 / 已公开规格 / 适配点 / 局限。只引用官网或手册中的规格。
   - 逐条需求对应：✓ 满足 / 部分满足 / ✗ 不满足 / 待确认。
   - 涉及产能分档时，运行 `python3 scripts/capacity_calc.py --cph <CPH> --pins <..> --volumes <..>`，结果标"估算"。
   - 差异化卖点（最多 4 条，必须真实）+ 风险提示。

5. **跟进计划**：按 `references/report-template.md` 第 4 节的四阶段表（首次回复 → 资料/样品或报价 → 确认/演示 → 促单），写明具体日期（用北京时间，并换算客户当地时间）、目标、待确认事项，以及"无回音时怎么办"。

6. **英文回复邮件**：按 `references/email-template.md` 写。价格、交期、认证、本地服务等 Jason 才知道的内容留 `[ ]` 占位，绝不编造。

7. **交付与归档**
   - 回复 Jason：一句话关键判断 + 四节分析 + 邮件模板。
   - 分析存为 `<客户>-<YYYY-MM>.md`（Hark 项目里放在 `work/`），并在项目记录里加一行。
   - 新的经验教训（新的数据源、产品边界、常见异议）写回本 skill（见 Upgrading）。

## Fixed requirements (do not drop)

- 四节顺序固定：客户背调 → 联系人画像 → 匹配方案 → 跟进计划与邮件。
- 不确定 = **待确认**；推断 = **推测**；计算 = **估算**。
- 绝不编造价格、交期、认证（CE/UL/IATF）、客户案例名称、良率/CPK、本地服务网点。
- 必须写出产品"不匹配/局限"的部分；不适合的产能档或功能要在邮件里如实说明。
- 邮件：主题行沿用客户原线程 `RE:` 并追加我方价值短语；延误先简短致歉；结构化逐条回应客户清单；行动号召只给 1 个主动作（通常是用客户样品做免费在线演示 + 一页评估报告/ROI）+ 索取资料清单。
- 收件人保持原线程：To 主联系人，CC 保留客户方全部抄送人。
- 客户机密信息只存私有仓库 `smthelp/smthelp-skill`，不推送到公开仓库。

## Upgrading this skill

- 产品规格、价格区间、交期、认证有更新 → 改 `references/product-library.md`（Jason 提供的价格写在"内部价格区间"表，标日期）。
- 新的背调数据源（如某国工商查询网站）→ 加到 `references/research-sources.md`。
- 新的常见异议与回应 → 加到 `references/report-template.md` 的异议库。
- 每处理完一个客户，可把脱敏后的分析放进 `examples/`，作为下次的参照。
- Bump `metadata.version`（major：四节结构变化；minor：新增章节/数据源/脚本；patch：措辞修正），并在 Version history 加一行。
- Sync：本地 `/workspace/smthelp-skill/inquiry-to-proposal/` → GitHub `smthelp/smthelp-skill`（私有）：`python3 scripts/push_github.py smthelp/smthelp-skill <local file> inquiry-to-proposal/<path>`（shell 调用需带 github credentials）。

## Version history

- 1.0.0 (2026-10-15) - 从 Hirschmann Automotive 连接器插针 RFI 案例提炼：四节流程、背调数据源、产品库与适配边界、产能估算脚本、英文邮件模板。
