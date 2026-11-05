# 文案结构（i18n 键）

所有可见文字都是 i18n 键；`en_ui.py` 定义 `EN = {...}`，`en_blog.py` 定义 `B = [dict(...), ...]`。

| 区块 | 键 |
|---|---|
| Meta | meta_title, meta_desc |
| 导航 | skip, nav_line, nav_stations, nav_bom, nav_spec, nav_videos, nav_blog, nav_contact, aria_theme, aria_lang |
| Hero | hero_badge, hero_h1, hero_sub, hero_cta1, hero_cta2, hero_note, hero_img_alt, m1v..m4v, m1l..m4l, trust |
| 3D | l3d_kicker, l3d_h2, l3d_p, l3d_play, l3d_resume, l3d_rotate, l3d_reset, l3d_fed, l3d_cycle, l3d_fallback, l3d_concept, l3d_full, l3d_mat, l3d_light, mat_orig, mat_metal, mat_clay, mat_xray, mat_wire, light_studio, light_warm, light_night |
| 模式 | md{n}_n（名称）, md{n}_d（说明）, md{n}_f（关键数字），n = 1..模式数 |
| 工具卡 | 自定义（例：fd_*、fr*） |
| How it works | st_kicker, st_h2, st_p, st{n}_n/_d/_f，n = 1..station_count |
| 型号表 | bom_kicker, bom_h2, bom_p, bom_c1..c4, bom_note, t_*（类型名） |
| 规格 | spec_kicker, spec_h2, spec_p, ev_ver, ev_con, ev_tbc, sp_*（卡片标题）, k_*（参数名）, v_*（文字值）, src_*（来源） |
| 披露表 | disc_kicker, disc_h2, disc_p, disc_c1..c4, d{n}t/a/b/n |
| 图库 | gal_kicker, gal_h2, gal_p, gal_more, g1..gN |
| 视频 | vid_kicker, vid_h2, vid_p, vid_more, vid_clips, vid_clips_p, v{n}t, c{n}t |
| 下载 | dl_kicker, dl_h2, dl_p, dl_pdf, dl_man, dl_3d, dl_more |
| ROI | roi_kicker, roi_h2, roi_p, roi_ops, roi_freed, roi_wage, roi_shifts, roi_price, roi_r1, roi_r2, roi_months, roi_need, roi_note |
| 博客 | blog_kicker, blog_h2, blog_p, blog_read, blog_close；每篇 b{i}_t 标题, _c 分类, _m 阅读时长, _x 摘要, _h1.._h6 小标题, _p1.._p6 段落 |
| FAQ | faq_kicker, faq_h2, fq{n}, fa{n} |
| 询盘/页脚 | cta_h2, cta_p, cta_mail, cta_wa, ft_* |

## 博客六步（不在可见文本里出现方法名）
1 一个具体场景（工厂里真实发生的问题）→ 2 为什么会这样（根因）→ 3 怎么判断/怎么做（方法）→ 4 我们的产品怎么解决（带型号和数字）→ 5 读者今天就能做的一步 → 6 联系方式。小标题用普通业务语言，例如 "The loader that did not fit the flow"。

## 写作规则
- 面向工厂经理、工艺工程师；英文为源语言，句子短，数字精确，带单位。
- 不写价格（报价页除外的 ROI 投资基数）、不写客户名。
- 不确定的数字标 To be confirmed，并进披露表。
