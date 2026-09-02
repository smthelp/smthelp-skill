# 搜索与调研策略参考

## 公司背景调研最优搜索组合

### 标准制造企业背调
```
# 并行启动（无依赖关系）
WebSearch: "[公司名] revenue employees manufacturing [行业]"
WebFetch:   https://www.[公司域名]/about
WebFetch:   https://www.[公司域名]/products
WebSearch: "[公司名] SMT PCB assembly factory production"
```

### 科技/初创公司背调
```
WebSearch: "[公司名] funding valuation series investors 2024 2025"
WebFetch:   https://craft.co/[公司slug]
WebFetch:   https://getlatka.com/companies/[公司slug]
WebSearch: "[公司名] hardware team manufacturing engineer job"
```

### 联系人身份确认
```
WebSearch: "[姓名] [公司名] [职位关键词] LinkedIn"
WebFetch:   https://linkedin.com/in/[姓名slug]
# 通过邮箱域名确认归属：@company.com 说明是内部员工
```

### CES/认证密集型客户
```
WebSearch: "[公司名] ISO AS9100 IATF certification"
WebFetch:   https://www.[公司域名]/quality
```

## 产品型号匹配最优搜索组合

### 客户指定了具体型号
```
WebFetch:  https://www.smthelp.com/[产品slug]
IMA KB1:   "[型号] [规格关键词]"
IMA KB2:   "[型号] [规格关键词]"
WebSearch: "smthelp.com [型号] specifications"
```

### 客户描述需求但未指定型号
```
WebSearch: "site:smthelp.com [功能关键词]"
WebFetch:  https://www.smthelp.com/product-category/[分类slug]/
IMA KB1:   "[功能描述] [应用场景]"
```

### 配件/备件匹配
```
WebSearch: "\"[设备型号]\" belt OR spare OR replacement"
IMA KB1:   "[设备型号] 配件 备件 皮带 规格"
WebFetch:  https://file.autoinsertion.com/Southern Machinery Manual/[设备名] Manual.pdf
```

## 竞品对标最优搜索组合

```
WebSearch: "[竞品型号] specifications CPH datasheet price"
WebSearch: "[竞品型号] vs comparison alternatives"
WebSearch: "[竞品品牌] [竞品型号] LED display SMT performance"
```

## 物流/关税参考搜索

```
WebSearch: "shipping electronics from China to [国家] costs customs import 2024 2025"
WebSearch: "[国家] import duty electronics SMT equipment HS code"
```

## 搜索优先级规则

1. **先搜公司身份**：公司官网 > craft.co/latka > LinkedIn > D&B
2. **再搜产品匹配**：smthelp.com 官网 > IMA KB1 > IMA KB2 > 行业网站
3. **后搜竞品对标**：竞品官网 > SMTnet > 行业论坛
4. **最后搜物流关税**：货代网站 > 海关官网

## 典型调研时间分配

| 客户类型 | 背调时间 | 产品匹配时间 | 总耗时 |
|---------|---------|------------|--------|
| 配件询盘（小） | 3-5 min | 2-3 min | ~8 min |
| 单品询价（中） | 5-8 min | 5-8 min | ~15 min |
| 整线RFQ（大） | 10-15 min | 8-12 min | ~25 min |
| 客户已指定竞品（复杂） | 8-10 min | 10-15 min | ~25 min |
