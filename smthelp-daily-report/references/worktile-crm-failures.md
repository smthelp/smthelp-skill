# Worktile CRM 故障参考手册
> Last Updated: 2026-06-19

## 故障1: SSL 证书无效

**URL**: `https://v5.viwolf.cn/admin888`
**错误**: `net::ERR_CERT_AUTHORITY_INVALID`
**现象**: 浏览器拒绝访问，SSL 证书链不被信任

## 故障2: Demo 登录表单无效

**重定向目标**: `http://demo.v5.viwolf.cn/admin888/login.html`
**现象**: 
- 填写手机号 `13602562576` + 密码 `nbjxJY3-1806WJX` 后点击登录
- 表单提交后页面变空白，**不跳转至真实 CRM 控制台**
- demo 站点是展示页面，不是真实后端

## 症状识别

| 症状 | 意味着 |
|------|--------|
| 浏览器直接报 SSL 错误 | 证书过期或自签名，需联系 Worktile 技术支持 |
| SSL 通过但登录表单空提交 | demo 站点的认证流程未对接真实 CRM API |
| 登录后停留在同一页面 | Session 未建立，检查是否被重定向回 demo |

## 临时应对（当日日报生成时）

1. **立即放弃等待**，不要循环重试登录
2. 在日报模块2（客户矩阵）和模块3（营销线索）中标注：
   - `[CRM暂不可用 — SSL证书异常]`
   - `[数据待手动补充]`
3. 改用 Fallback Sources（Wiki + 本地文件扫描）
4. **不影响其他模块生成**：模块1/4/5/6 均可基于已知信息正常输出

## 长期解决建议

- 联系 Worktile（深圳）技术支持，要求：
  1. 修复 `v5.viwolf.cn` 的 SSL 证书（Let's Encrypt 或商业 CA）
  2. 确认 demo.viwolf.cn 与正式 CRM 的关系，避免认证逻辑混淆
- 备选方案：考虑导出 CRM 数据至 CSV，由日报 skill 改为读取本地文件作为数据源

## Credentials（供参考，请勿在报告中暴露）

- Phone: `13602562576`
- Password: `nbjxJY3-1806WJX`
- 保存于: Memory（`memory` 工具，`user` profile）
