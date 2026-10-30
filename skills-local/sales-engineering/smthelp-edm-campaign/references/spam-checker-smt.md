# Spam Word Checker — SMT Foreign Trade Extension

> 基于 ColdOutboundSkills `spam-word-checker` 规则，补充 SMT/THT 设备外贸专项禁止词库。

---

## 一、通用 Spam 词库（B2B 外贸通用）

### 禁止词

| 类别 | 禁止词 |
|-----|-------|
| 价格夸大 | "cheapest", "lowest price", "best price", "rock bottom", "unbeatable" |
| 绝对保证 | "100% guaranteed", "guaranteed ROI", "risk free", "no questions asked" |
| 催促压力 | "act now", "limited time", "don't miss out", "expires today", "hurry" |
| 免费陷阱 | "free machine", "free equipment", "free line" |
| 虚假获奖 | "award winning", "best in class", "world's best" |
| 攻击竞品 | "Fuji is overpriced", "Yamaha is garbage" |

---

## 二、SMT 设备外贸专项禁止词

### 技术夸大类

| 禁止表述 | 问题 | 替代说法 |
|---------|------|---------|
| "as accurate as Fuji" | 不能与日系直接等同 | "comparable placement accuracy" |
| "never breaks down" | 绝对化，违反广告法 | "18+ months zero major service calls" |
| "will definitely improve your yield" | 不能保证良率 | "our customers report [X]% average improvement" |
| "the best wave solder in China" | 绝对化表述 | "high-performance wave solder at competitive price" |
| "our machine is as good as [brand]" | 商标侵权风险 | "delivers comparable output at 60% of the cost" |

### 行业特殊禁止类

| 禁止表述 | 问题 | 替代说法 |
|---------|------|---------|
| "IATF certified"（未认证不得声称） | 认证资质滥用 | "CE certified, designed to meet IPC-610" |
| "replaces all your workers" | 夸大自动化程度 | "reduces insertion headcount by 6-8 workers per shift" |
| "no maintenance needed" | 误导性陈述 | "field-serviceable design with 24-48hr response" |
| "works perfectly forever" | 绝对化 | "proven in 18+ customer installations" |

### 过度承诺类

| 禁止表述 | 问题 | 替代说法 |
|---------|------|---------|
| "save 80% on labor" | 无法保证具体比例 | "customers report reducing insertion labor costs significantly" |
| "double your output" | 绝对化陈述 | "customers report throughput improvement up to X units/hour" |
| "investment pays back in 6 months" | 过度乐观 | "typical payback 12-18 months based on customer data" |
| "our quality is better than [日系]" | 直接对比风险 | "our specs meet or exceed comparable models" |

---

## 三、可安全使用的技术表述

### 精度与速度

```
✓ "±0.5mm placement accuracy"
✓ "4,000 CPH with 4-head configuration"
✓ "12,000 CPH for connector insertion"
✓ "0.8-second feed cycle"
✓ "AI vision correction for ±0.05mm accuracy"
✓ "Active Clinching: 98N insertion force"
```

### ROI 与成本

```
✓ "Customers report 14-18 month payback period"
✓ "Reducing manual insertion labor by 6-8 workers per shift"
✓ "37% OEE improvement reported by Hungary customer"
✓ "30-50% lower CapEx vs. comparable Japanese equipment"
✓ "$180K below budget for Thailand greenfield project"
```

### 认证与合规

```
✓ "CE certified"
✓ "Designed to meet IPC-610 Class 3"
✓ "Lead-free process compatible (SAC305)"
✓ "IATF 16949 compliant process documentation available"
```

---

## 四、邮件标题（Subject Lines）规则

### 安全的标题类型

**类型 A — 个性化问题**：
```
"question for {{first_name}} at {{company_name}}"
"{{company_name}} equipment upgrade"
"saw your expansion in {{city}}"
```

**类型 B — 数据驱动**：
```
"[Client] — 37% OEE improvement at Hungary plant"
"[Client] — THT labor cost benchmark for {{country}}"
"[Client] — {{country}} EMS CapEx benchmark"
```

**类型 C — 展会切入**：
```
"electronica this year?"
"NEPCON Thailand — personal tour available"
"productronica Munich — worth a detour?"
```

### 禁止的标题

```
❌ "Best regards from Southern Machinery" — 太正式/无价值
❌ "SMT equipment at good price" — 价格敏感词
❌ "Fuji quality at Chinese price" — 商标侵权风险
❌ "30% off for {{company_name}}" — 折扣在设备行业不适用
❌ "Urgent: equipment inquiry" — 制造紧迫感
❌ "Partnership opportunity" — 太泛
❌ "Free consultation" — 暗示免费服务
```

---

## 五、正文格式检查清单

```
□ 第一行：个性化情况识别（公司/城市/最近动态）
□ 无 "I hope this email finds you well"
□ 无 "I wanted to reach out"
□ 无 "Just following up"
□ 无 "Our company offers..." 开头的自我介绍
□ 数字具体：37% / 14 months / $180K（而非"很多"/"很快"）
□ 无超过2个连续句子介绍我们
□ CTA 是简单问句（"Would X work?" / "Is this relevant?"）
□ 签名：姓名 + 公司 + 邮箱 + 电话 + 网站 + 物理地址
□ 物理地址使用英文格式（如 "Bldg 3, Longhua District, Shenzhen, China"）
```

---

## 六、退订行合规（CAN-SPAM / GDPR）

所有邮件底部必须包含：

```
---
This email was sent to {{lead_email}} because [reason].
To unsubscribe: reply with "unsubscribe" or "no".
Southern Machinery | Bldg 3, Longhua Industrial Zone, Shenzhen, China 518000
{{from_email}} | www.smthelp.com | +86-136-0256-2576
```

> 注意：不能用 "we'll stop if you don't respond" 这种以沉默换停止的说法。
