# 输入规范（input-spec）

## 1. 必需输入

| 项 | 说明 | 例 |
|---|---|---|
| 产品源素材 | 至少一种：PDF（淘宝/1688 详情页打印件、规格书、目录）、1688/淘宝/smthelp.com 产品 URL、产品图片 | 6 份淘宝 PDF + 2 个 smthelp.com 产品页 |
| 主题 | 一句话的页面主题（英文或中文均可），决定 H1、SEO 文件名和文案角度 | "Auto Insertion Radial components splicing tape made by Southern Machinery" |

## 2. 可选输入（不给就用默认值）

| 项 | 默认 |
|---|---|
| 品牌偏好：Logo、主色、联系方式、社媒链接 | `templates/brand-southern-machinery.json`（见下表） |
| 参考模板 URL | 现有骨架（S-300B / S-MVF01 系设计）即可，不必再给 |
| 目标仓库/路径 | 本地 `work/<slug>/` + GitHub `smthelping/smt-product-landing-html/<product-line>/` |
| 语言 | en（默认）、es、pt、fr、ar（RTL）、ru、zh |
| 博客数量 | 8 篇（`blog_count`） |
| Chatwoot 配置 | 品牌默认（下表） |
| 产品线文件夹 | 按产品归类：`materials-consumables` / `tht-auto-insertion` / `feeders-nozzles` / `board-handling` / `nozzle-and-gripper` |
| 是否发布 WebDAV | 不发布；用户明确要求才发，密码每次现问 |

## 3. Southern Machinery 默认值（brand-southern-machinery.json）

- Logo：`https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`（页眉左上角）
- WhatsApp：`https://wa.me/8613602562576`；电话 `+86 136 0256 2576`
- 邮箱：`info@smthelp.com`
- 社媒五件套：LinkedIn 公司页 `https://www.linkedin.com/company/smtmachine`、LinkedIn 个人 `https://cn.linkedin.com/in/smtsupplier`、Twitter `https://twitter.com/smtspecialist`、Facebook `https://www.facebook.com/autoinsertion`、YouTube `https://www.youtube.com/c/Smthelping`
- 机器目录：`https://file.autoinsertion.com`；机器图片：`https://ph.smthelp.com`
- YouTube Video Board：`https://file.autoinsertion.com/public/Southern-Machinery-YouTube-Video-Board.html`
- Product Catalog Board：`https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html`
- Chatwoot：`BASE_URL=https://chat.smthelp.com`（用户原稿写 http，一律改 https），`websiteToken: saMcpgSupcmd1VQwytgPLfbK`，`chatwootSettings={"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"}`
- 领域知识：`smthelp/smthelp-skill/learn-SMT-in-3-hours`（私有仓库，Jason 的 SMT 三小时课程）

## 4. Intake 检查清单

开工前逐项打勾，缺的先自己找（URL 抓取、图床搜索、视频墙、目录墙），找不到才问：

- [ ] 源素材可读（PDF 有文字层？没有就读页面渲染图）
- [ ] 主题明确（能写出 H1 和 SEO 文件名）
- [ ] 产品线文件夹确定（可从主题推断）
- [ ] 有没有和已有页面同名/同主题（查 smt-product-landing-html README，避免重复）
- [ ] 价格、供应商店名、他牌水印已识别并准备剔除
- [ ] 是否要求 WebDAV 发布

## 5. 缺信息时怎么问（最多 2 个问题）

只问真正改变产出的，一次问完，给出默认选项让用户一个字回答：

1. 「主题就按 *<从素材推断的主题>* 做，归到 `<product-line>/`，可以吗？」
2. 「需要同时发布到 file.autoinsertion.com 吗？（需要的话发布时我再问密码）」

其余一律用默认值，不要问 Logo、语言、博客数量、Chatwoot。

## 6. 源素材处理红线

- **价格永不出现**（淘宝/1688 的 ¥ 价格是内贸参考），页面引导询盘
- **供应商名、店铺名、他牌水印永不出现**（如 DHR、ESOCOO、Southern Electronics、GIANNG 水印）；用图前逐张目检
- alicdn / 淘宝图片不外链（防盗链 403 且暴露货源）：裁切避开水印后 base64 内嵌或上传自有图床
- 来源之间数字冲突 → 进 disclosure 表，各自标来源，不擅自取舍；拿不准的标 `To be confirmed`


## 7. 可选：快速匹配表的数据来源（1.1.0 起）

matcher 的行来自用户给的 Excel/BOM/评估表 + 目录。先用 `scripts/extract_sources.py` 或 openpyxl 把每张表导成文本，再写一个小脚本（放 `work/<slug>/tools/`）生成 `product/matcher.json`：
- 一张来源表一个匿名代号（bomA、bomB…），代号的说明写进 `mx_src_<code>`，不写客户名
- 包装代码统一（granel/bandeja/fitado/rolo → bulk/tray/radial_tape/tape 等）
- 只录来源里有的数字；描述里的 P= 值与表格列冲突时取描述，并在 disclosure 与 `mx_note_*` 里说明
- 目录给的每个供料器 envelope 写进 `feeders[].env`，超出即标 `tbc`
