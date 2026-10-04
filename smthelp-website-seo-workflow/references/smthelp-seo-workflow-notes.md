---
name: smthelp-seo-workflow
description: Southern Machinery 网站后台 SEO 优化工作流 — smthelp.v5.viwolf.cn THT 产品系列（35个产品）
archived: 2026-06-14
absorbed_into: sales-engineering/smthelp-website-seo-workflow (as §2)
---

# Southern Machinery 网站后台 SEO 优化工作流

## 后台登录信息

> ⚠️ **凭证从环境变量读取，禁止硬编码。** 需要 `SMTHELP_WEB_ADMIN_PATH`、
> `SMTHELP_WEB_ADMIN_USER`、`SMTHELP_WEB_ADMIN_PASSWORD`。

- URL: `http://smthelp.v5.viwolf.cn/${SMTHELP_WEB_ADMIN_PATH}`
- 用户名: `${SMTHELP_WEB_ADMIN_USER}`
- 密码: `${SMTHELP_WEB_ADMIN_PASSWORD}`
- 语言参数: lang=en

## 核心 URL Pattern
- 产品列表: `http://smthelp.v5.viwolf.cn/${SMTHELP_WEB_ADMIN_PATH}/manage.shop.php?listid=18407&modelid=8&lang=en`
- 产品编辑: `http://smthelp.v5.viwolf.cn/${SMTHELP_WEB_ADMIN_PATH}/manage.shop.php?action=edt&listid=18407&modelid=8&pid=1&productid={PID}&lang=en`
- 产品保存: `http://smthelp.v5.viwolf.cn/${SMTHELP_WEB_ADMIN_PATH}/manage.shop.php?action=edt&listid=18407&modelid=8&pid=1&productid={PID}&submit=1&lang=en`

## 产品分类结构
- THT machine (listid=18407, modelid=8): 35个产品，分2页
- Wave soldering (listid=19282)
- Blog (listid=19280, modelid=6): 当前为空

## 完整产品清单（THT系列）

### 第1页
| productid | 产品名称 | 状态 |
|---|---|---|
| 136440 | S-7000D Tact Switch Inserter | ✅ 已完成 |
| 135444 | S7020 Series PIN Eyelet Terminal Insertion Machine | ⏳ 下一个 |
| 135614 | S4000 Axial Auto Insertion Machine | 待处理 |
| 135493 | S-3000 PCB DIP Assembly Radial Insertion Machine | 待处理 |
| 137614 | S-4000 Axial Inserter Machine | 待处理 |
| 137600 | S-4000 Axial Inserter Machine | 待处理 |
| 135427 | S-4000H Jumper Wire Inserter Machine | 待处理 |
| 135426 | S-3000 Radial Insertion Machine | 待处理 |
| 135425 | S-3010B Radial Insertion Machine (Offline) | 待处理 |
| 135425 | S-70LD Odd Form Insertion Machine | 待处理（旗舰款） |
| 135443 | S-7000I Fuse Holder Insertion Machine | 待处理 |
| 137636 | S-7000T Terminal Insertion Machine | 待处理 |
| 135618 | S-7000T Terminal Insertion Machine | 待处理 |
| 135440 | S-7000 Pin Insertion Machine | 待处理 |
| 137665 | Auto Lead Cutter Machine for THT PCB Assembly | 待处理 |
| 137657 | S7900 ODD FORM INSERT MACHINE | 待处理 |
| 135616 | S-WS450 Wave Soldering Machine | 待处理 |
| 135442 | S-7000T Terminal Insertion Machine | 待处理 |
| 135441 | S-7000E Eyelet Pin Inserter | 待处理 |
| 135384 | S-680 Automatic Scrap Tape Cutting Machine | 待处理 |

### 第2页（需重新提取productid）
访问 http://smthelp.v5.viwolf.cn/${SMTHELP_WEB_ADMIN_PATH}/manage.shop.php?listid=18407&modelid=8&page=2&lang=en 用JS提取

## SEO 优化步骤

1. **登录后台** — navigate to admin URL, type credentials, click login
2. **进入产品列表** — navigate to manage.shop.php with listid=18407
3. **定位产品** — 用 `browser_console` 提取所有产品行，找到目标 productid
4. **进入编辑页** — navigate to edit URL with productid
5. **清空现有SEO字段** — 用 browser_console 清空原有内容
6. **写入SEO标题** — 格式: `产品型号 | 产品名称 | 核心卖点 - Southern Machinery`
7. **写入SEO关键词** — 逗号分隔，8-15个精准长尾词
8. **写入SEO描述** — 150-180字符，精准描述功能、应用、优势
9. **保存** — 点击保存按钮

## 已知问题
- Session 会话约30分钟过期，操作间隔长时需重新登录
- 产品编辑页需用 lang=en 保证英文界面
- 翻页用 JS click，而非 navigate（因为是动态加载）
