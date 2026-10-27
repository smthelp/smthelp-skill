# Southern Machinery 报价单审核清单 v1.0.0 (2026-10-27)

来源：smt-brand-kit 1.0.0（brand-guide.md, brand.json, feedback-log.md）+ 外贸报价惯例。
注意：品牌包"never publish 价格/交期/付款/质保"只适用于营销物料；报价单里这些条款必须有，检查完整与一致。

严重度：🔴 高 = 会造成损失/纠纷/泄露供应商（必须改）；🟠 中 = 不专业或易误解（应改）；🟢 低 = 风格润色（建议）。
输出格式：每份报价单一张问题表：# | 严重度 | 位置(页/单元格/段落) | 现文 | 问题 | 建议改法。

## A. 品牌一致性
1. 公司全称：Shenzhen Southern Machinery Sales and Service Co., Ltd.（brand.json 写法，"and" 小写，结尾带句点）；正文简称 Southern Machinery。全文统一，不混用 SM / 南方机械 / 其他拼写。
2. Logo：sm-logo.png 原色、原比例，不拉伸、不改色；深色底时放白色圆角卡。
3. 颜色：Navy #003142（标题、表头）、Green #93AC3E（强调线）、Teal #0097B2、Grey #4A5A63（正文）、Light #EEF5F7（底纹）。不出现其他主色。
4. 字体：英文报价单用 Arial（客户 Mac/Windows 都有，profile.json style.font 可改为 Microsoft YaHei）；同一文档字号层级统一。
5. 联系方式块（固定顺序）：smthelp.com · info@smthelp.com · WhatsApp +86 136 0256 2576；可加地址 Xixiang, Bao'an, Shenzhen, China 及销售人邮箱 jasonwu@smthelp.com。
6. 型号命名：首次 "Smart EMS <SM型号> <通用品名>"，之后用 SM 型号；供应商型号只在 Jason 要求时出现。
7. 供应商痕迹清零：供应商公司名、品牌、logo、网址、电话、邮箱、地址、二维码、原厂型号、文件属性(作者/公司)、图片水印、页眉页脚、隐藏工作表/批注。
8. 第三方设备品牌（如 FUJI、Panasonic）只用于说明兼容，附非关联说明，不暗示 OEM 关系。
9. 不出现夸张词（revolutionary, world-leading, best-in-class），不写无证书支撑的认证，不写产能/良率/ROI 承诺百分比（除非合同性指标且有依据）。

## B. 必备内容 / 条款
10. 报价编号（建议 SMQ-YYYYMMDD-xx）、报价日期、有效期（例：Valid for 30 days from issue date）。
11. 买方信息：公司名、联系人、地址/国家、邮箱电话；与询盘一致、拼写正确。
12. 卖方信息：全称、地址、联系人、联系方式（同 A1/A5）。
13. 产品：SM 型号、品名、配置/选配、关键参数、电压/频率（按买方国家，如 220V/50Hz, 110V/60Hz）、气源、软件语言。
14. 单价 × 数量 = 小计；合计、折扣、运费、保险、税；货币单位(USD/EUR/CNY)全篇一致，大写金额与小写一致（如有）。
15. 贸易术语：Incoterms® 2020 + 指定港/地点（如 FOB Shenzhen, CIF Ho Chi Minh Port, EXW Shenzhen），与运费/保险是否计入一致。
16. 付款条件：比例与节点清晰（如 30% T/T deposit, 70% T/T before shipment / L/C at sight），比例合计 100%。
17. 交期：从何时起算（收到定金后 X working days），与付款节点衔接。
18. 质保：期限、起算点（自装运/安装验收）、范围与除外（易损件、人为损坏）、远程/现场支持。
19. 安装调试与培训：是否包含、远程或上门、差旅费由谁承担、人天数。
20. 包装：出口木箱/真空包装、熏蒸（IPPC）、毛重/尺寸（如有）。
21. 银行信息：开户名与公司全称一致、银行名、账号、SWIFT、银行地址；提醒"账户变更以书面确认为准"防诈骗。
22. 签字盖章栏：卖方签字/公司章，买方确认栏。
23. 备注：价格不含进口关税/当地税费、图片仅供参考等免责条款。

## C. 一致性与质量
24. 算术：逐行重算单价×数量、小计、合计、百分比定金金额。
25. 跨页/跨表一致：型号、数量、金额、交期、条款在正文、汇总、PI、邮件之间一致。
26. 日期格式统一（建议 27 Oct 2026 / 2026-10-27），有效期未过期。
27. 英文质量：拼写、语法、术语（Incoterms、T/T、L/C、Proforma Invoice）、单位空格（430 mm）、数字格式（1,250.00）。
28. 版式：分页、表格不截断、打印 A4 适配、PDF 可搜索文本。

## D. 旧报价单常见问题（2025-2026 三份样板实测，qa_quote.py 已自动检查）
- Date 用 =NOW()：每次打开都变成当天，客户和自己都无法确认报价日期 → 写固定日期。
- 公司名三种写法（Sales And Service Co Limited / Sales and  Service Co.,Ltd）且缺 Shenzhen → 统一为注册全称。
- "T0:"（数字 0）、"Ex-work SZ"、"receipt deposit"、"to be cover"、"responsibled"、"1 years"、"no mentioned"、"Payment terms：Payment terms"、全角标点、"KG/c ㎡"、"Ralay"、"Signa/Plugl"、"Parament"。
- 总表型号与明细表不一致（SLD250 vs SLD-250）。
- 只写 "free installation and training"，不说远程还是上门、差旅谁付。
- EXW 出货却 "50% after installation"：货走了钱没收到。
- 质保无起算点或干脆没有（Storage Rack 那份）。
- 无银行信息、无签字栏、联系方式缺 info@ / WhatsApp，仍有 FAX。
- 打印跨页：J 列单独掉到第二页（列宽超 A4）。
- 规格自相矛盾：S350C 名称 0.5 m 但规格写 Rail length 1 m；输送高度 900 mm 与上下板机 950 mm 不一致。
