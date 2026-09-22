---
name: smthelp-admin-blog-publishing
description: Southern Machinery 网站后台（smthelp.v5.viwolf.cn/admin888）发布 GEO 博客文章的标准流程与关键技术细节。覆盖登录、博客入口、富文本编辑器（UEDITOR）内容注入、表单提交验证。
triggers:
  - "发布博客文章"
  - "网站后台写文章"
  - "smthelp blog GEO article"
  - "UEDITOR 内容写入"
  - "admin888 blog article"
---

# Southern Machinery 网站后台博客发布流程

## 后台登录
- URL: http://smthelp.v5.viwolf.cn/admin888
- 用户名: admin / 密码: admin888
- 语言参数: lang=en

## 博客入口
- URL pattern: `manage.shop.php?listid=19280&modelid=6&lang=en`
- 当前状态: Blog (listid=19280) 目前为空文章列表
- 添加新文章: `manage.shop.php?action=add&listid=19280&lang=en`

## 表单字段映射（博客文章）

| 表单字段 | HTML name 属性 | 说明 |
|---|---|---|
| 文章标题 | `ktitle` | 同时也是 SEO title 和 URL 别名来源 |
| SEO 标题 | `ktitle` | 复用同一字段 |
| SEO 关键词 | `kkeywords` | 逗号分隔，8-15 个长尾词 |
| SEO 描述 | `kdescription` | 150-180 字符 |
| 简短描述 | UEDITOR 实例 `ueditorInstant0` | 对应 `kdesc1` |
| 简短描述2 | UEDITOR 实例 `ueditorInstant1` | 对应 `kdesc1`（备用） |
| 文章正文 | UEDITOR 实例 `ueditorInstant2` | 对应 `kcontent` |

## 关键技术：UEDITOR 富文本编辑器

**重要发现：** 网站后台使用 **百度 UEDITOR**（不是 CKEDITOR/Summernote），编辑器实例嵌入在 iframes 中，通过 `UE.instants` 全局对象访问。

### 识别 UEDITOR 实例
在浏览器 console 中执行：
```javascript
Object.keys(UE.instants).map(function(k) {
  return k + ':' + UE.instants[k].getContent().substring(0, 50);
})
// 输出: ueditorInstant0:..., ueditorInstant1:..., ueditorInstant2:...
```

### 写入内容到 UEDITOR
```javascript
var html = '<h2>Your Article Content Here</h2><p>...</p>';
UE.instants.ueditorInstant0.setContent(html);  // 简短描述
UE.instants.ueditorInstant2.setContent(html); // 文章正文
```

### 获取 UEDITOR 内容
```javascript
UE.instants.ueditorInstant0.getContent()
```

## 验证表单数据
在 console 中查看所有已提交的表单字段：
```javascript
var fields = [];
document.querySelectorAll('input, textarea').forEach(function(el) {
  var info = el.tagName + ' name=' + el.name + ' value=' + (el.value || '').substring(0, 80);
  fields.push(info);
});
fields.join('\n')
```

## 文章发布后验证
1. 检查返回的文章列表，文章 ID（如 137666）出现在列表中
2. 访问前台 URL 验证渲染：`http://smthelp.v5.viwolf.cn/{url-alias}.html`
3. 确认 H1 标题、description、规格表、CTA 联系信息均正确显示

## 已知注意事项
- Session 会话约 30 分钟过期，操作间隔长时需重新登录
- 产品编辑页用 `lang=en` 保证英文界面
- 保存按钮 ref 通常为 `@e33`（需结合实际 snapshot 确认）
- UEDITOR 实例数量可能因页面不同而变化，通过 `Object.keys(UE.instants)` 确认
