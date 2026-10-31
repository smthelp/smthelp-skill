# 字段说明 / Field specification

## checklist.json 结构
```json
{
 "meta": {
  "model": "S-JVF02",                       // SM 型号，不翻译
  "product_name": {"zh": "SMT 振动（料管）飞达", "en": "SMT stick vibration feeder"},
  "compatible": "JUKI RS-1",                // 适配机型或配置；无则 ""
  "product_line": "feeder-vibration",       // product-lines/registry.json 的 id
  "doc_no": "SM-FQC-S-JVF02", "doc_rev": "A",
  "template_version": "1.0",
  "status": "draft",                        // draft | released（--release 自动写）
  "sources": [{"id": "MAN", "type": "manual", "title": "...", "url": "..."}]
 },
 "sections": [
  {"code": "A", "zh": "整机外观与结构", "en": "Appearance & Structure",
   "items": [{
     "id": "A02",                           // 分区字母 + 两位序号，唯一
     "grade": "MI",                         // CR 致命 | MA 主要 | MI 次要
     "status": "S",                         // C 已确认 | S 建议值 ★ | T 待确认 TBD
     "zh": {"item": "外形尺寸", "criterion": "...", "method": "钢直尺 / 游标卡尺 ...", "source": "产品页 §03 规格表 'Overall size'", "sampling": "每批抽 2 台"},
     "en": {"item": "Overall dimensions", "criterion": "...", "method": "...", "source": "Product page §03 spec table 'Overall size'", "sampling": "2 units per lot"},
     "spec": {"nominal": "365×66×125", "lsl": "-1", "usl": "+1", "unit": "mm"},
     "question": {"zh": "外形尺寸公差 ±1 mm 是否正确？", "en": "Is ±1 mm the right dimension tolerance?"}
   }]}
 ]
}
```

| 字段 | 必填 | 规则 |
|---|---|---|
| id | 是 | 与分区 code 同字母开头；不重复 |
| grade | 是 | 安全/电气默认 CR；功能、规格 MA；外观、清洁、标签 MI |
| status | 是 | C：数值和判定全部有来源；S：用了 G 编号建议值；T：资料缺失，判定写不出数值 |
| zh/en.item | 是 | 名词短语，≤ 10 字 / ≤ 5 words |
| zh/en.criterion | 是 | 可判定的句子；含数值时写单位与条件；T 项写需确认的内容，渲染时自动加「待确认 / TBD」 |
| zh/en.method | 是 | 动作 + 工具 + 次数/时长（“扭力螺丝刀抽检 ≥ 5 颗”） |
| zh/en.source | 是 | 见 extraction-rules.md 第 2 节写法；G 编号或 `Jason 确认 YYYY-MM-DD` |
| zh/en.sampling | 是 | `100%`、`每批抽 n 台`、`每批首台`、`—`（NA 项） |
| spec | 否 | nominal / lsl / usl / unit 均为字符串；T 项不得有数字 |
| question | S/T 必填 | 双语，一问一事，可直接发给 Jason 或客户 |

## 表格列（PDF 与 Excel 相同顺序）
| # | 中文 | English | 内容 |
|---|---|---|---|
| 1 | 编号 | No. | id |
| 2 | 等级 | Grade | CR / MA / MI |
| 3 | 检查项目 | Check item | item |
| 4 | 判定标准 | Acceptance criterion | criterion（S 橙色，T 红色加「待确认」） |
| 5 | 标准值 / 下限 ~ 上限 | Nominal / LSL ~ USL | 由 spec 生成；S 加 ★；T 显示 TBD |
| 6 | 检验方法 / 工具 | Method / tool | method |
| 7 | 抽样 | Sampling | sampling |
| 8 | 依据来源 | Source | source |
| 9 | 判定结果 | Result | PDF：☐ 合格 ☐ 不合格 ☐ NA；Excel：下拉 |
| 10 | 实测值 | Measured | 产线填写 |
| 11 | 结论 / 备注 | Conclusion / remark | 产线填写；NA 写原因 |
| 12 | 检验员 | Inspector | 产线填写 |
| 13 | 日期 | Date | 产线填写 |
