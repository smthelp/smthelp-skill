# 验证清单

## validate.py（硬性，失败退出码 1）
1. 体积 ≤ `page.size_budget_kb`
2. 所有 `<script>` 通过 `node --check`
3. JSON-LD 可解析，含 Organization、WebPage、FAQPage、BlogPosting
4. 无残留 `%%占位符%%`
5. 每个 data-i18n 键在每种语言都存在
6. 语言集合 = 配置
7. 可见文本、全部译文、class 名无禁用词
8. 无隐私词（客户名、报价号、单价…）
9. 博客篇数 = `blog_count`
10. FAQ 条数 = `faq_count`
11. 每种语言有 hreflang，且有 x-default
12. Chatwoot token 存在
13. Logo、5 个社媒、WhatsApp、目录站、图床链接齐全
14. 3D 画布与 `__mode3d` 存在
15. ROI 字段存在（启用时）
警告：http:// 链接、非图床外链图片、过多大尺寸内嵌图。

## render_test.py（浏览器）
- 无页面 JS 报错（407 / 隧道失败 是沙箱代理问题，可忽略）
- 每个模式按钮可切换并截图
- 材质、光照按钮能循环
- zh、ar（dir=rtl）、390 px 手机无横向溢出

## 人工必看
- 打开所有截图：hero 图不要信息海报、3D 不黑屏、文字不溢出、卡片不遮挡主体
- 披露表覆盖所有文档矛盾
- 规格数字与来源一致（抽查 5 条）
- 片段视频文件夹为"知道链接的任何人可查看"
- 交付时向用户列出：未逐条校对的翻译、待确认数字、未使用的资料
