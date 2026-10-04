---
name: foxmail-mailbox-mining
description: "直接从 Foxmail 7.2 本地邮件库（Storage/）离线挖掘客户/线索，无需打开客户端、无需 IMAP。邮件正文是加密的，但邮件头索引是明文可解析的：可提取发件人姓名+邮箱、收件人、主题、精确日期。适用于「从历史邮件整理客户清单 / 找沉睡客户 / 统计往来量 / 还原询盘主题」。触发词：Foxmail 邮件挖掘、邮件整理客户清单、邮箱数据导出、邮件线索、Foxmail 客户。"
agent_created: true
---

# Foxmail 7.2 本地邮件库离线挖掘

## 何时用

用户让你「从我和客户的邮件里整理客户清单」「挖历史询盘」「找沉睡客户」，且机器上存在
Foxmail 7.2 的数据目录（含 `FMStorage.list` + `Storage/<邮箱地址>/`）。

## 关键事实（逆向结论，已实测）

1. **邮件正文是加密的**。`Storage/<acct>/Mails/<a>/<b>/<id>` 每个文件都是密文，不要试图解码正文。
2. **邮件头索引是明文**：`Storage/<acct>/Mails/Index`（单个账户可达 200MB+）。
3. **日期索引也是明文**：`Storage/<acct>/Indexes/recvdate.ind` 与 `senddate.ind`。
4. 账户清单在 `FMStorage.list`（**UTF-16-LE** 编码，需 `decode('utf-16-le')`）。

### Index 文件结构（每账户）

- 头部 **51 字节**，之后是**定长 512 字节**的记录。
- 记录内的字段采用「长度前缀块 + 拼接字符串」：
  ```
  ... 00 00 | <len1> <len2> ... <lenN> | 00 | <str1><str2>...<strN>
  ```
  其中 `str1..strN` 依次是：发件人显示名、发件人邮箱、收件人1显示名、收件人1邮箱、
  （更多收件人成对出现）…、**最后一个字段是主题**。字段个数恒为奇数（`2 + 2*收件人数 + 1`）。
- 解析办法（见 `scripts/foxmail_extract.py`）：用正则 `rb'[\x20-\xff]{8,}'` 找到文本块
  起止 `(s, L)`，再向前找 `mm[s-1] == 0`，回溯到上一个 NUL 得到长度前缀段，
  从尾往前尝试 `k` 个字节使 `sum(seg[-k:]) == L`，命中即按长度切分字段。
  - 实测命中率 ≈ 96%；不命中的直接丢弃即可（多为二进制误报）。
  - ⚠️ **`k` 必须从大到小枚举**（`for k in range(len(seg), 0, -1)`）。
    反过来从小到大（`range(1, len(seg)+1)`）会优先命中 `k=1` 这类退化解，
    切分出一个字段 → `len(flds)<3` 被丢弃 → **全库静默返回 0 条，看起来像"查无此人"**。
    这个假阴性极难察觉（无报错、无异常，只是结果为空）。
  - ⚠️ **不要自己重写解析函数，直接复制 `scripts/foxmail_extract.py` 的 `fields_for` / `RUN` / `HDR` / `REC` 再改。**
    另外两个易错点：扫描是对**整个 mmap 做 `RUN.finditer`**（不是按 512 切片后各自 search，
    切片会切断跨记录的长度前缀块）；以及必须 `b'@' in g` 预筛。
  - 解码顺序：`utf-8` → `gbk` → `latin-1`。

### 日期索引结构（recvdate.ind / senddate.ind）

- 头部 32 字节；之后每条 **16 字节**：
  ```
  [4B 常量 a1 c2 3f ae][4B 大端 mail_id][4B 大端 日期序号][4B 大端 日内毫秒]
  ```
- **日期序号 = Python `datetime.date.fromordinal(n)` 的天数（纪元 0001-01-01）**。
  即 `datetime.date.fromordinal(day)` 直接就是收/发日期；`0` 表示无效。
- **mail_id 与 Index 的对应关系**：`mail_id = (文本块在 Index 中的偏移 - 51) // 512`。
- 无日期的条目（约 15%）多半是草稿/仅索引项，`recvdate` 取不到时回退 `senddate`。
- ⚠️ **必须过滤未来日期**：实测大账户会混进 `2040-03-19` 之类的脏序号（info@smthelp.com 命中 4 条）。
  解析后一律丢弃 `date > TODAY`，否则静默天数变负值、排序被污染。

### 账户层面的三件事（开工前先扫一遍，别默认每个账户都能挖）

1. **空壳账户**：只有 `Accounts/` 配置、没有 `Mails/Index` 的账户（实测 `jasonwuSMT@outlook.com`），
   直接跳过，不要当 0 记录账户参与统计。
2. **停更账户**：按 `recvdate/senddate` 的最大有效日期判定活跃度。
   实测 12 账户里只有 3 个是 2026 年主力（`info@smthelp.com` 占全库 69%），
   其余分别停在 2021 / 2022 / 2023。停更账户的历史往来仍可用，但**不能参与「近期静默」判断**。
3. **静默天数基准用「主库数据截止日」（实测 2026-05-06），不要用 `date.today()`**——
   会系统性叠加 100+ 天，把所有人风险等级抬高一档。

### 挖不出来的东西（别浪费时间）

- **邮件正文**：`Mails/<a>/<b>/<id>` 与 `Mime/Decode.rec0` 均为密文，无解。
- **地址簿**：`Global/Address/3.0/ContactCombination.rec0` 是 RECF 容器且加密
  （采样 200KB 命中 0 个明文邮箱）。联系人只能从邮件头的 from/to 反推。

### 其他目录（一般不需要）

- `Boxes/*.box`：收件箱/发件箱/垃圾箱等集合，二进制。
- `Indexes/msgBody`、`Indexes/email`：全文索引，未逆向。

## 执行步骤

1. 定位数据目录：`Storage/` 下每个子目录是一个邮箱账户。
2. 运行 `scripts/foxmail_extract.py`（改 `ROOT` / `OUT`），产出 JSONL：
   `account, sender_name, from, to, subject, date`。
3. 去重：按 `(account, from, to, subject)`。
4. 判定方向：
   - 己方域名集合（示例 `smthelp.com/.net`、`smtnozzle.org`）＋己方个人邮箱（qq/gmail/outlook）
   - `from` 属于己方 → 该记录是**发件**，外部方取 `to` 中的非己方地址
   - 否则若 `to` 中含己方 → **收件**，外部方取 `from`
5. 聚合：公司键 = 企业邮箱取**域名**，免费邮箱（gmail/hotmail/outlook/yahoo…）取**完整邮箱地址**。
   - ⚠️ **最大坑**：若先做域名归一化再聚合，写成 `comp[norm_dom(addr)]`，
     会把 `gmail.com` / `yahoo.com` 聚成「一家客户」（实测把 1.8 万封往来压成一行）。
     必须先判 FREE 再决定用地址还是域名：
     ```python
     def key_of(addr):
         d = norm_dom(dom(addr))
         return addr.lower() if d in FREE else (d or addr.lower())
     ```
   - **域名归并**（否则同一客户被拆成多条）：
     - 采购门户子域 → 主域：`jabil.coupahost.com → jabil.com`
       （PORTAL = coupa/coupahost/ariba/jaggaer/zycus/gep/ivalua/tradeshift/basware…）
     - 邮件系统子域 → 主域：去掉 `mail./email./service./noreply./smtp./mx./news.` 首段
       （**仅当 `len(parts)>=3`**，否则 `mail.ru` 这类会被打散）
   - 公司名推断要跳过地区/功能前缀，否则出现 `na.denso.com → "Na"`、
     `community.3ds.com → "Community"`：SKIP 集合需含
     na/eu/us/uk/cn/hk/tw/jp/kr/apac/emea/amer/global/mail/info/service/www/community/green/shop…
5b. **退信与自动回复必须按主题剔除**（否则占 C 级一大半）：
   `delivery status|undeliver|mail delivery fail|returned message|mailer-daemon|postmaster|
   auto-reply|automatic reply|out of office|未傳遞|退信|user unknown|mailbox full|blocked|rejected`
   命中即 `n_bounce+=1`，计分时 `eff_in = n_in - n_bounce`。
6. 去噪（必须做，否则一半是 EDM/物流/元器件推销）：按域名黑名单剔除
   社交平台、招聘、EDM/营销自动化、SEO 建站、SaaS 与开发运维工具、
   物流快递货代（dhl/ups/dsv/kuehne/expeditors/mainfreight/by56…）、
   元器件·PCB·化工推销方、行业媒体展会、明显无关行业的电商。
   - 实测黑名单必须**显式包含完整域名**而不只是关键词，否则漏网：
     `facebook.com fb.com instagram upwork kwork fiverr tradeindia indiamart
     sc.com(渣打银行通知) postmaster mailer-daemon messagelabs eigbox
     unisoft-cim mail-ascglobal elcina juliangoldie fastechpcb abiscircuits
     sourceability hardfind byethost netvigator da.direct serv00 mindautocloud
     gsma2017 adsale-marketing gismaexpo nepconchina efymag cbcinewsemail`
   - 只在 `n_out==0`（我方从未回复）时启用的**保守**推销关键词：
     seo/webdesign/hosting/vps/cpanel/sourcing/leads/outreach/coldmail…
7. 分级（A/B/C/D）时**必须加采购相关性门槛**，否则纯量大的新闻订阅会误判为 A：
   - `buylike = n_buy>=1 or n_po>=1 or n_inq>=3`；`replied = n_out>=1`
   - A：`score>=100 且 n_in>=10 且 n_out>=5 且 365天内有联系 且 (n_po>=1 or n_buy>=5)`
   - B：`score>=40 且 replied 且 730天内有联系 且 (n_buy>=1 or n_inq>=5)`
   - **C：`buylike 且 replied 且 静默<=730天`（原规则缺 `replied`，会把单向推销邮件全灌进 C 级）**
   - **D：`buylike 且 replied 且 静默>730天 且 n_total>=5`**
   - **E：`replied` 但无 buylike（供应商/货代/服务商/内部）**
   - **F：我方从未回复的单向来信 —— 单独一个 sheet，且只保留 `n_inq/n_buy/n_po>=1` 的，
     否则几千家营销订阅会淹没真正漏跟的询盘**
   - `score = n_out*5 + eff_in*1 + n_buy*8 + n_po*20 + 时效加权(90天+30/365天+15/730天+5)`
   - 其中 `n_out>=1`（我方真的回复过）是剔除订阅邮件的最有效单一条件。
8. 主题清洗：循环剥离 `Re:/Fwd:/答复:/回复:` 以及多语言自动回复前缀
   （`Automatic reply / Read: / Leído / Przeczytane / Прочтено / 已读`）；
   选「询盘产品」时优先**纯 ASCII 主题**，避免 GBK 误解码产生的乱码。

## 完整管线（一步到位）

`scripts/foxmail_extract.py`（改 `ROOT`/`OUT`）→ `scripts/build_contacts.py`（聚合+去噪+分级，
产出 `/tmp/contacts_rows.json` + `/tmp/people_rows.json`）→ 出 xlsx。
实测：12 账户 / 609,627 条记录，提取约 90 秒，聚合约 40 秒，出 3.5MB xlsx 约 40 秒。

**跑之前先把三个脚本里的 `TODAY` / `SRC` / `OUT` 改对**（`TODAY` 已改为 `datetime.date.today()`，
无需手动改日期）。建议把脚本复制到工作目录再改，保持技能内脚本为干净模板。

### 出表脚本二选一

| 脚本 | 用途 | 主表口径 |
|---|---|---|
| `scripts/make_xlsx.py` | **Mautic 导入**。用户给了 Mautic contacts 模板时必须用它 | Sheet1 严格 32 列模板 |
| `scripts/make_master_xlsx.py` | **通用 Master 客户库**。用户只是要「客户清单 / 再激活名单」时用这个 | 6 个 sheet，见下 |

`make_master_xlsx.py` 的 sheet 结构：
`01_Master客户库`（A-D 级，含「是否询盘」列）／`02_供应商与服务商`（E）／
`03_未跟进来信线索`（F）／`04_联系人明细`／`05_国别分布`／`06_说明与分级规则`。

## 交付建议

生成一个 xlsx，至少 5 个 sheet：
`01_Mautic导入_客户通讯录`（A-D 级，严格按用户给的模板列序）/ `02_往来统计与分级`（A-E）/
`03_联系人明细` / `04_未跟进来信线索`（F 级）/ `05_说明与分级规则`。
所有由域名推断的字段（公司名、国别、官网）必须显式标注 **待确认**，
国别只从 `.tr/.br/.mx/.vn` 等国别域推断，`.com/.net/.org` 一律留空（**不代表美国**）。

**若用户给了导入模板（如 Mautic contacts）**：主 sheet 必须严格沿用模板的列名、列序、列数
（含其拼写错误，如 Mautic 的 `discription` 不能改成 `description`），保证可直接导入；
额外的统计字段一律放其他 sheet，不要往主表加列。
Mautic 字段映射参考：`points=score`、`last_active=末次往来`、`attribution_date=首次往来`、
`attribution=来源`、`website=域名`、`subject=代表主题`、`discription=往来摘要+待确认说明`。

## 出表时的两个坑（实测）

1. **国别表里「静默>730 天的公司数」恒等于 D 级数量** —— 因为 A 要求 ≤365 天、B/C 要求 ≤730 天，
   A-D 中只有 D 可能 >730 天，这列是废列。改用**「户均往来封数」**，信息量大得多。
2. **「户均往来封数」是最有判别力的一列**，能一眼区分「深耕市场」和「撒网市场」。
   实测同一批数据：Slovakia 232 封/家、Mexico 113、Poland 83、Turkey 65（深耕，少量客户但往来极密）；
   UK 4.3、Russia 4.7（公司数虽多——UK 574 家、Russia 370 家——但几乎没有实质往来，多为一次性接触或冷开发）。
   **公司数多 ≠ 市场好，必须看户均往来量。**

## 交付时的口径提醒

- 「真正谈过话」的正确口径是 **`n_out >= 1`（我方回复过）**，不是「有邮件往来」。
  实测 22,420 个外部对象中，我方回复过的只有 18,345 个；其中进入客户库（A-D 级）的 11,101 家。
- E 级（供应商/货代/服务商）务必单独成表，否则会污染客户库。实测 E 级有 7,244 家，占比不小。
- 国别只能覆盖约 24% 的公司（实测 4,399 / 18,345），其余 `.com/.net/.org` 留空并在说明里讲清楚，
  不要猜成美国。

## 已知限制

- 拿不到电话、地址、职位、机型参数、正文内容——这些必须在交付物里标「待确认」。
- 二级国别域要按最长匹配处理（`com.br` 优先于 `br`）。
- 单账户 22 万条记录解析耗时约 15 秒（Python + mmap），写 12 万行 xlsx 约 2 分钟。
