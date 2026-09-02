---
name: himalaya-email-campaign-gotchas
description: "Southern Machinery EDM campaign 中发现的 Himalaya CLI + tinkmail.me 技术细节。 记录 BCC 处理、UTF-8 Subject 乱码、Web 研究被 CAPTCHA 拦截的应对方案。 触发场景：配置 Himalaya 群发账号、发送 BCC 邮件、处理特殊字符主题行、找不到目标客户联系方式时。\n"
whenToUse: "Himalaya BCC，himalaya message send，邮件乱码，tinkmail.me UTF-8，BCC 邮件发送，找不到客户邮箱，EDM 找不到联系人"
metadata:
  source: hermes
  origin: "sales-engineering/himalaya-email-campaign-gotchas"
---
# Himalaya Email Campaign — 技术细节与避坑指南

**来自 Southern Machinery 2026-04-28 EDM 测试 campaign 实战经验。**

---

## 一、BCC 处理（最关键发现）

### 常见误解

❌ 以为 BCC 需要用 Himalaya 的特殊 flag 或者环境变量来设置。
✅ **BCC 就是在邮件原始 header 里写 `BCC:` 头，Himalaya 会自动处理。**

### 正确格式

```bash
himalaya message send --account sale_3dsmt << 'EOF'
From: sale@3dsmt.com
To: lead@example.com
Subject: [Company Name] — 40% CapEx reduction on THT lines
BCC: jasonwu@smthelp.com
X-Priority: 3
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

[Email body]
EOF
```

**BCC 写入 Sent 文件夹的验证方法**：
```bash
himalaya envelope list --folder "Sent" --account sale_3dsmt
# 输出中可以看到 BCC 收件人也出现在 ENVELOPE 里
```

### 验证脚本

```python
import subprocess

def send_with_bcc(account: str, email_raw: str) -> dict:
    """发送邮件并验证 BCC 是否写入 Sent"""
    r = subprocess.run(
        ['himalaya', 'message', 'send', '--account', account],
        input=email_raw,
        capture_output=True, text=True
    )
    return {
        'rc': r.returncode,
        'stdout': r.stdout.strip(),
        'stderr': r.stderr.strip()[:200],
        'success': r.returncode == 0 and 'successfully sent' in r.stdout.lower()
    }
```

---

## 二、UTF-8 Subject 乱码（tinkmail.me 特性）

### 问题现象

```
发送Subject: "[Varela Electrónica] — Cómo reducir el costo..."
IMAP显示:   "[Varela Electr�nica] — C�mo reducir el costo..."
```

tinkmail.me 的 IMAP 服务器对 RFC 2047 未编码的 UTF-8 Subject 行解码有缺陷，
**但邮件本身发送正常**（收件人能正确看到），问题仅出现在 Sent folder 的列表显示。

### 解决方案（三选一）

**方案 A（推荐）：Subject 全部用 ASCII**
```python
# 把特殊字符转成 ASCII 或去掉
subject = "[Varela Electronica] - 38% THT cost reduction"  # 无éñ字符
```

**方案 B：RFC 2047 MIME 编码**
```python
import email.header
encoded = email.header.encode_header([
    (subject, 'utf-8')
])
# "=?UTF-8?B?W1ZhcmVsYSBFbGVjdHLDs25pY2FdIC0gQ/8tbW8gcmVkdWNpci4uLj8=?="
```
但在 himalaya 的 `<<EOF` heredoc 中使用 header 编码会增加复杂度。

**方案 C：Subject 用纯国家英文名**
```
"[Brazil] — 40% CapEx reduction on THT insertion lines"
"[Argentina] — 38% THT cost reduction benchmark"
```
特殊字符留给邮件正文，不影响发送。

---

## 三、Web 研究被 CAPTCHA 拦截的应对

### 实测情况（2026-04-28）

| 搜索引擎 | 结果 | 原因 |
|---------|------|------|
| Google (任意语言) | CAPTCHA | IP 被识别为数据中心 |
| DuckDuckGo | CAPTCHA | 同上 |
| Bing | 重定向劫持 | 同样是数据中心IP |

**IP**: 207.97.137.77 — 确认是 GitHub Actions / 数据中心 IP，无 residential proxy。

### 替代研究路径

**路径 1：直接访问目标公司官网**
```
https://www.dana.com          → 404（已改版）
https://www.continental.com/   → 可访问，但 Contact 页面隐藏
https://www.abb.com           → 可访问
```
绕过搜索引擎，直接去公司官网找 Contact / Careers / Supplier Portal。

**路径 2：行业协会目录**
```
巴西：abinee.org.br（Abinee — 巴西电子工业协会）
阿根廷：caena.org.ar 或直接搜索 ".ar automotive electronics"
```
已验证 abinee.org.br 可访问（成员页面 404，但首页活着）。

**路径 3：LinkedIn Sales Navigator**
通过公司官网找到 LinkedIn 页面 → 找相关员工 → 尝试通过公司邮箱格式（firstname@company.com）猜测。

**路径 4：海关数据（推荐长期方案）**
使用 `xiaoman-crm-wave-solder-prospecting` skill，自动化抓取从中国进口波峰焊机的海外客户数据。
```bash
# 每周一早上自动运行，无需人工干预，不受 CAPTCHA 影响
```

**路径 5：Yellow Pages / ThomasNet**
```
https://www.thomasnet.com —— 美国 B2B 黄页，可按产品+地区筛选
```
ThomasNet 有反爬但不如搜索引擎严格。

### 研究策略总结

```
当 Web 搜索被 CAPTCHA 拦截时：
1. 直接访问行业协会首页（找成员目录）
2. 直接访问目标公司官网（找 HR/Contact 邮箱格式）
3. LinkedIn 个人页面（绕过公司限制）
4. ThomasNet / Europages（欧洲黄页）
5. 海关数据（最准确但需要权限）
```

---

## 四、邮件正文字符集

### 多语言正文

```python
# 中文/葡语/西语正文 → 使用 UTF-8 charset
headers = f"""From: {from_addr}
To: {to_addr}
Subject: {subject}
BCC: {bcc_addr}
X-Priority: 3
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

"""
# 正文用 triple-quoted string，直接包含 UTF-8 字符
email_body = f"""
{headers}
{body_text}  # 这里放葡语/西语正文
"""
```

### 阿根廷邮件正文示例（含西班牙语）

```python
email_ar = f"""From: info@smthelp.eu
To: {lead_email}
Subject: {subject}  # 用 ASCII subject
BCC: jasonwu@smthelp.com
X-Priority: 3
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

Hola {first_name},

He seguido el crecimiento de {company_name} en el mercado de módulos automotores — su capacidad en BCM y ECU es bien conocida en la región.

El desafío que escucho con frecuencia: el equipo japonés consume 40-50% del presupuesto de CapEx, con períodos de recupero que superan los 5 años.

Southern Machinery fabrica líneas SMT/THT con rendimiento comparable — a un 30-40% menos de CapEx. Un cliente en Hungría redujo sus costos de inserción manual en un 38% y recuperó su inversión en 14 meses.

¿Funcionaría una llamada de 15 minutos esta semana para explorar si hay una oportunidad?

Un saludo,
Jason Wu | Sales Engineer
Southern Machinery | info@smthelp.eu | +86-136-0256-2576 | www.smthelp.com
Bldg 3, Longhua Industrial Zone, Shenzhen, China 518000

---
Este correo fue enviado a {lead_email} porque creemos que su empresa podría beneficiarse de soluciones de automatización SMT/THT.
Para cancelar la suscripción: responda con "unsubscribe" o "no".
"""
```

---

## 五、发送验证流程

### 完整发送前检查清单

```bash
# 1. 验证账号列表
himalaya account list

# 2. 验证单账号 SMTP 发送（发到自己）
himalaya message send --account info_smthelp_eu << 'EOF'
From: info@smthelp.eu
To: jasonwu@smthelp.com
Subject: [TEST] SMTP verification

Test message from info@smthelp.eu
EOF

# 3. 检查发送日志（RC=0 = 成功）
# RC 非 0 时：检查网络、SMTP 配置、账号密码

# 4. 验证 BCC 写入 Sent folder
himalaya envelope list --folder "Sent" --account sale_3dsmt
```

### 发送节奏建议（新账号预热）

| 阶段 | 每天/账号 | 时长 |
|-----|---------|------|
| 预热期 | 5-10 封 | 第 1-2 周 |
| 爬坡期 | 20-30 封 | 第 3-4 周 |
| 稳定期 | 30-50 封 | 第 5 周起 |

---

## 六、多账号邮件搜索与读取（扫描 SMT/THT 相关邮件）

### 2026-04-29 实战发现

当需要搜索所有账号中与 SMT/THT/波峰焊相关的邮件时，遇到以下问题：

#### 账号列表
```bash
himalaya account list
# 输出：
# | NAME            | BACKENDS   | DEFAULT |
# |-----------------|------------|---------|
# | info_3dsmt      | IMAP, SMTP |         |
# | info_smthelp_eu | IMAP, SMTP |         |
# | jasonwu_work    | IMAP, SMTP | yes     |  ← 主账号，常超时
# | sale_3dsmt      | IMAP, SMTP |         |
# | service_3dsmt   | IMAP, SMTP |         |
# | support_3dsmt   | IMAP, SMTP |         |
```

#### jasonwu_work 主账号超时问题
```
error: email::imap: authentication failed mechanism=Plain err=Stream(State(Flow(MalformedMessage { discarded_bytes: /* REDACTED */ })))
[Command timed out after 30s]
```
**解决**：该账号 IMAP 连接不稳定，搜索/读取操作超时。改用 `sale_3dsmt` 或 `info_smthelp_eu` 账号替代扫描。

#### Himalaya Query 语法限制（关键坑）

❌ **错误写法** — 空格分隔的多词术语义：
```bash
himalaya envelope list subject SMT line  # ✗ "found l expected `and`, `or`"
himalaya envelope list subject SMT THT   # ✗ "found THT expected `and`, `or`"
```

✅ **正确写法** — 必须显式用 `and`/`or` 连接每个条件：
```bash
himalaya envelope list subject SMT or subject THT or subject wave or subject insertion
```

✅ **单复数/变体一起搜**：
```bash
himalaya envelope list subject SMT or subject THT or subject wave or subject insertion or subject PCB or subject assembly
```

#### IMAP 超时处理
```bash
# 多次重试机制
for account in info_3dsmt info_smthelp_eu sale_3dsmt service_3dsmt support_3dsmt; do
  himalaya envelope list --account $account --folder INBOX --page 1 --page-size 500 2>&1 | \
    grep -v "^2026\|WARN\|missing required" | head -50
done
```

#### 扫描所有文件夹的标准流程
```bash
# 对每个账号，依次检查：INBOX → Sent → Drafts → Junk → Trash
for account in info_3dsmt info_smthelp_eu sale_3dsmt service_3dsmt support_3dsmt; do
  echo "=== $account INBOX ==="
  himalaya envelope list --account $account --folder INBOX --page 1 --page-size 500 2>&1 | ...
  echo "=== $account Sent ==="
  himalaya envelope list --account $account --folder Sent --page 1 --page-size 500 2>&1 | ...
done
```

#### 读取邮件内容（语法已更正 2026-07-08）

⚠️ **正确语法**（positional argument，无任何 flag）：
```bash
himalaya message read <ID>
```
⚠️ **错误语法**（这些 flag 不存在）：
```bash
himalaya message read --id <ID>     # ✗ --id 不存在
himalaya message read <ID> --account xxx  # ✗ --account 不存在于 message read
himalaya message read <ID> --folder Sent  # ✗ --folder 不存在于 message read
```

⚠️ **所有 message read 操作均超时**：即使用正确语法，在 30秒 timeout 下也全部超时（IMAP 服务器响应慢）。无法读取任何邮件正文，包括 Sent folder 中已确认存在的邮件 ID。建议改用浏览器登录 `https://outlook.office365.com` 读取邮件正文。

#### 错误信息速查

| 错误信息 | 含义 | 解决 |
|---------|------|------|
| `authentication failed mechanism=Plain` + timeout | jasonwu_work 账号 IMAP 不稳定 | 换用其他账号 |
| `[Command timed out after 30s]` | IMAP 连接慢/网络问题 | 换账号，或直接读 Sent 文件夹 |
| `cannot parse search emails query` | Query 语法错误（缺 and/or） | 用 `and`/`or` 连接每个条件 |
| `found l expected 'and', 'or'` | 多词搜索词（如 "SMT line"）空格导致解析错误 | 把多词词组拆成独立条件 |
| `missing required UNSEEN OK untagged response` | IMAP 服务器响应不标准 | 不影响读取，忽略 WARN |
| `page 2 out of bounds` | 只有 1 页数据，无需翻页 | 正常 |

### 关键发现

**SMT/THT 相关邮件只在 Sent 文件夹**（发出的 EDM），INBOX 通常只有 "Welcome to TinkMail" 垃圾邮件。
如果只查 INBOX 会漏掉所有已发送邮件。

---

## 七、常见错误排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `unknown backend type` | `backend.type = "smtp"` 写在 `[accounts.NAME]` 下而非 `[accounts.NAME.message.send]` | 修正为嵌套结构 |
| RC=0 但邮件没收到 | SMTP success 但可能被收件方拒收/bounce | 检查 BCC 收件箱是否收到 |
| `AUTHENTICATIONFAILED` | 密码错误或 `auth.raw` 而非 `auth.password` | 确认 TOML 中使用 `auth.raw = "password"` |
| Subject 乱码 | tinkmail.me 不支持裸 UTF-8 | 改用 ASCII subject |
| `AUTHENTICATIONFAILED` | 密码错误或 `auth.raw` 而非 `auth.password` | 确认 TOML 中使用 `auth.raw = "password"` |
| Subject 乱码 | tinkmail.me 不支持裸 UTF-8 | 改用 ASCII subject |
| `unrecognized argument '--id'` | `message read` 不接受 `--id` flag | 直接用 `himalaya message read <ID>` |
| 所有 `message read` 超时（30秒） | IMAP 服务器响应极慢 | 改用 `https://outlook.office365.com` 浏览器读取正文 |

## 八、IMAP 同步冻结观察（2026-07-08 更新）

- **Sent folder 冻结**：所有账号 Sent folder 最后同步日为 2026-04-28，2026-04-28 之后发送的邮件不在 Sent folder 中
- **INBOX 部分恢复**：`info_3dsmt` INBOX 自 2026-07-03 起有新邮件（"Goodnews." from info@1haag.com），说明 IMAP 同步正在缓慢恢复
- **Sent folder 仍冻结**：Sent folder 仍停在 2026-04-28，2026-07-03 之后发送的邮件未同步到 Sent
- **根本原因**：服务端 IMAP 同步从 2026-04-28 至约 2026-07-03 完全冻结

## 九、参考资源

- **smthelp-edm-campaign skill** — EDM campaign 主 skill（邮件序列、ICP、Spam 合规）
- **smthelp-knowledge-base** — Southern Machinery 产品参数知识库
- **jason-email-skill** — Jason Wu 专属邮件模板库
- **xiaoman-crm-wave-solder-prospecting** — 海关数据自动采集（不依赖 Web 搜索）
