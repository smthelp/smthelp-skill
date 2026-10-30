---
name: foxmail-archive-mining
description: >
  从 Foxmail 客户端的数据目录（Storage/）里离线提取全部历史邮件与客户线索，不需要 Foxmail
  客户端、不需要 Windows 机器。用于把企业多年的邮件归档变成结构化客户名单（A/B/C 分档）、
  联系人库、话题统计；也用于把邮件归档 + LinkedIn 导出 + 展会名单等多源数据缝合成一张
  客户 CRM 表（去重、补公司/国家/行业、加跟进看板）。
  当用户说"挖掘邮件归档""导出 Foxmail 邮件""从老邮件里找客户""沉睡客户唤醒""邮件考古"
  "建 CRM""客户表合并去重""多源联系人合并"时使用。
agent_created: true
---

# foxmail-archive-mining

把 Foxmail 7.x 的本地归档目录，直接解析成结构化邮件数据与客户名单。

## 核心事实（先读，能省你几小时）

| 项 | 值 |
|---|---|
| 正文在哪 | `<账号>/Indexes/msgBody/{,1..N}/bodytxt_txt.rec0` |
| 正文编码 | **UTF-16LE 明文**，文件头 `RECF` 魔数 + 128 字节头 |
| 记录格式 | `[id:4B][len:4B][UTF-16LE 文本]`（但记录**不连续**，别按此顺序读） |
| `Mails/NN/NN/*` | 高熵密文，`strings` 捞不到东西 —— **那是附件/MIME 缓存，不是正文，别去解** |
| 邮箱明文 | `Indexes/email/emailid_org.rec0`、`Address/3.0/1/AddrEmail_org.rec0` |
| Message-ID | `Indexes/msgid/msgid_id_org.rec0`（内含时间戳，如 `<20170116122632…@domain>`） |
| `Indexes/*.map` | `KVLS` 键值索引，16 字节/条 `[tag:4][id:4][值A:4][值B:4]`，**大端序**；值 A 非单调，不是简单偏移，**别逆它** |
| `msgExt/*/exttxt_txt.rec0` | 实测 **0 条邮件头**，跳过 |
| 通讯录 | `Address/3.0/1/AddrEmail_org.rec0`（明文邮箱）；`Global/Address/3.0/ContactCombination.rec0` 是 ASCII 字符串但**不含邮箱** |

**一句话：正文是明文，扫文本流即可，不要试图逆容器格式。**

## 用法

```bash
PY=/Users/mac/.workbuddy-ai/binaries/python/envs/default/bin/python

# 第 1 步：提取邮件 -> messages.jsonl（实测 1.48 GB / 52 文件 约 5 分钟）
$PY scripts/extract_messages.py <Foxmail数据目录> <输出目录>

# 第 2 步：整合成分档客户名单 -> contacts.json
$PY scripts/consolidate_contacts.py <Foxmail数据目录> <输出目录>

# 第 3 步（可选）：多源缝合成 CRM 表 -> SMThelp-CRM.xlsx
$PY scripts/build_crm.py
```

前两个脚本顶部的 `BASE` 常量按实际路径改；输出写到 `<输出目录>/messages.jsonl` 与 `contacts.json`。
`build_crm.py` 顶部有 `BASE` / `LI` / `OUT` 三个路径常量，按实际改；依赖第 2 步的 `contacts.json`。

## 提取算法（脚本已实现，改前先读）

```python
UNIT = rb"(?:[\x09\x0a\x0d\x20-\x7e]\x00|[\x00-\xff][\x4e-\x9f]|[\x00-\xff][\x30-\x33])"
RUN = re.compile(UNIT + rb"{12,}")

def extract_text(path):
    parts = []
    with open(path, "rb") as fh:
        while chunk := fh.read(16 * 1024 * 1024):     # 16 MB 是偶数，码元不被切断
            parts += [m.group().decode("utf-16-le", "replace") for m in RUN.finditer(chunk)]
    return "".join(parts)
```

`UNIT` 覆盖三类码元：ASCII+CRLF、CJK（U+4E00–9FFF）、CJK 标点（U+3000–33FF）。
分块边界落在偶数字节上，跨块的 run 拼接后文本仍完整 —— **不需要 overlap**。

切分邮件靠邮件头块：

```python
HDR = re.compile(
    r"(?:^|[\r\n])[ \t]*(?:From|发件人)[ \t]*:[ \t]*(?P<frm>[^\r\n]{1,180})[\r\n]+"
    r"[ \t]*(?:Date|日期|时间)[ \t]*:[ \t]*(?P<date>[^\r\n]{1,90})[\r\n]+"
    r"[ \t]*(?:To|收件人)[ \t]*:[ \t]*(?P<to>[^\r\n]{1,400})[\r\n]+"
    r"[ \t]*(?:Subject|主题)[ \t]*:[ \t]*(?P<subj>[^\r\n]{0,400})", re.M)
```

## 踩过的坑（都真实踩过）

1. **日期有三种格式，必须都覆盖**：
   - `2020-01-16 10:52`
   - `Mon, Apr 20, 2020 09:02 PM` ← 漏这个会丢一半日期
   - `1/15/22 9:36 PM (GMT-05:00)`
2. **同一消息在后续回复里被反复引用**，同一个头块会重复出现几十次 —— 按 `(from, to, date, subject[:120])` 去重。
3. **签名污染**：老板自己的签名（含 `+86 手机号`、公司域名）被引用在几乎每封邮件里。
   做**任何**电话区号/国家推断前，必须**逐行剥离自有签名**，否则所有客户都被判成"中国"。
   且 `+86` 命中要**无条件丢弃**。
4. **显示名不可信**：可能是邮箱前缀（`lgarcia`）、职能词（`info`、`sales`、`ventas`、`compras`）、
   公司名（`GR SYS`）、或 `姓, 名` 倒序。判断"名"时要用邮箱本地部分做交叉校验。
5. **邮箱列表要过滤**：`do_not_reply@`、`coupahost`、纯数字本地部分（QQ 号）、16 位以上十六进制（哈希）。
6. **NAS/网络盘**：`find` 全盘遍历会超时（几十万文件），**限定路径**再搜；删除操作可能被文件系统拒绝。
7. `msgBody` 可能有多个分片目录（`1..15`），**全都要扫**，漏一个就丢一批邮件。

## 交付物模板

提取完通常产出：

1. `客户复活名单.xlsx` —— 分档表 + 发送排期（按时区归组，每批同一时区）
2. `客户复活邮件模板.md/html` —— 3 套英文模板 + 已个性化的现成草稿
3. `SMThelp-CRM.xlsx` —— 多源合并客户主表（见下节）

**分档启发式**（可调）：

| 档 | 判据 |
|---|---|
| A 成交过 | 正文前 600 字出现 proforma invoice / payment / shipment / B/L / contract / warranty / spare part |
| B 报过价 | 出现 quotation / price / offer / FOB / lead time，无成交信号 |
| C 仅询盘 | 只有 inquiry / requirement / catalog / RFQ |

**只看正文前 600 字** —— 再往后就是引用历史，会把整条线程的每个消息都染成同一档。

## 多源客户表缝合（CRM）

脚本：`scripts/build_crm.py`（顶部 `BASE` / `LI` / `OUT` 按实际改）。

### 先判断各层是不是互补的

把每个数据源的**字段填充率**算出来，不要假设它们重复：

| 层 | 邮箱 | 公司 | 职位 | 国家 |
|---|---|---|---|---|
| LinkedIn 连接（Connections.csv） | 1.8% | 97.3% | 98.0% | ~0% |
| LinkedIn 通讯录（Contacts.csv） | 100% | 0.9% | 3.2% | 13.8% |
| Foxmail 归档 | 100% | 0.1% | 0.4% | 64.8% |

有公司没邮箱 + 有邮箱没公司 → **缝合能凭空造出可用记录**，这不是去重，是补全。

### 三个提升手段（按收益排序）

1. **企业邮箱域名推公司** —— `juki.com → Juki`、`sanmina.com → Sanmina`。
   必须排除免费邮箱（品牌词表 `FREEMAIL_HEAD`）与泛化词（`DOM_STOP`：smt/info/sales/mail…）。
   这一招把成交客户的公司覆盖从 **6.5% 提到 88.9%**，收益最大。
2. **按姓名缝合** —— 归一化键：NFKD 去重音 → 去括号 → 只留 ≥2 字母的词。
   精确全名优先；`姓+首字母` 只在**唯一命中**时用。缝合后必须 `consumed` 标记，
   否则一个人被多条 LinkedIn 记录重复认领。过滤 <3 字符的公司名（`H`/`G`）和自家公司名。
3. **通讯录 `Addresses` 字段抠国家** —— `Shenzhen,Guangdong,China` / `Singapore` / `CA 94010`。
   长国名优先匹配（否则 `china` 命中 `chinatown`）；美国靠 `州缩写+5位邮编`。

### 这个数据源的硬限制（别硬编）

- `linkedin_connections_export_microsoft_outlook.csv` 的 `Business Country` 列**填充率 0%**。
- 旧通讯录（`JasonwuWu Contacts2016.csv`）的国家值是 **GBK 乱码**（`�й�` = 中国），不是 UTF-8。
- 结论：**国家覆盖 17% 就是上限**。硬编 = 造假数据。正确做法是**加一列「国家依据」**
  （邮箱域名 / 通讯录地址 / 正文提及×N / 电话区号×N），让推断来源可追溯，把「待确认」显式呈现。

### 修过的脏数据（都会再遇到）

| 症状 | 样例 | 修法 |
|---|---|---|
| OCR 垃圾邮箱（手机通讯录导入） | `1h361@163.com`、`4xi3ngcn@wd.sbga`、`ht@lwww.` | TLD 白名单 + 单 `@` + 禁字符 + **数字占比 >40% 拒绝** |
| 姓名含缩写/公司词/自家痕迹 | `T N GANESH`、`Rogrio GR SYS`、`Sara from Southern Machinery` | 去单字母 token、剥尾部公司词表、`NAME_BAD` 过滤自家品牌 |
| 全小写姓名 | `liebig fritz` | `islower()` → Title Case；`isupper()` 且长度>3 同理 |
| 电话字段脏 | `257131203, +1 333-468-7782`、`+5592994622098,8718`、同号重复三遍 | 按 `,;/|` 切段 → 取数字位数 7–15 且**最长**的那个 |
| 姓名重复 | `李少良李少良` | 检测整串是否由子串重复构成 |

### 行业分类：加知名厂商映射

纯关键词规则会留下 **74% 待分类**，因为 `Flextronics`/`Sanmina`/`Philips`/`Indium`
这些公司名里没有 "electronic"/"smt" 等词。加一层 `KNOWN_CO` 映射（公开信息，非猜测）
+ 多语种「生产/制造现场」规则（tecnico/engenheiro/manutenção/calidad，外贸客户职位多为葡/西语），
待分类降到 61%。**厂商映射要放在关键词规则之前**（精度优先）。

### 表结构建议

阶段用真实业务阶梯（`新线索 → 已联系 → 已报价 → 样品试机 → 成交 → 搁置`），
但**允许增设真实存在的中间态**（如「已连接」= LinkedIn 已连接但无邮件往来）。
推断出来的字段（公司/国家/行业）**都配一列「依据」**，否则半年后没人敢用这张表。

## 合规红线

- 邮件归档含客户隐私。**内部整理可以，外泄不行**；对外发送前必须由负责人确认。
- 欧盟客户注意 GDPR；发出前留退订/止损语。
- 不要编造参数、价格、交期。拿不准标 `[待确认]`。
