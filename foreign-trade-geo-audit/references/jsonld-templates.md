# JSON-LD 模板集

> 每个模板都可直接粘贴。占位符用 `{{...}}` 标记，上线前替换并**核对 NAP 归一结果**。
> 新增模板时同步更新本文件顶部目录。

## 目录
1. [首页四实体 @graph](#1-首页四实体-graph) — Organization + Person + ItemList + FAQPage
2. [产品页 Product](#2-产品页-product)
3. [面包屑 BreadcrumbList](#3-面包屑-breadcrumblist)
4. [文章 Article / BlogPosting](#4-文章-article--blogposting)
5. [视频 VideoObject](#5-视频-videoobject)
6. [OG + canonical 全站通用](#6-og--canonical-全站通用)
7. [校验方式](#7-校验方式)

---

## 1. 首页四实体 @graph

**用途**：一次解决 B 维度最大欠账。放在首页 `</head>` 前。

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://{{主域}}/#organization",
      "name": "{{法定全称}}",
      "alternateName": ["{{品牌简称}}", "{{品牌别名}}"],
      "url": "https://{{主域}}/",
      "logo": "{{Logo 绝对地址}}",
      "foundingDate": "{{YYYY-MM}}",
      "description": "{{一句话：品类 + 地域 + 年限 + 服务对象}}",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "{{街道详细地址}}",
        "addressLocality": "{{城市}}",
        "addressRegion": "{{省/州}}",
        "addressCountry": "{{CN}}"
      },
      "telephone": "{{+86-xxx-xxxx-xxxx}}",
      "email": "{{主邮箱}}",
      "sameAs": [
        "{{LinkedIn 公司页}}",
        "{{Facebook}}",
        "{{Twitter/X}}",
        "{{YouTube 频道}}"
      ],
      "knowsAbout": ["{{品类1}}", "{{品类2}}", "{{品类3}}", "{{品类4}}"],
      "makesOffer": {
        "@type": "Offer",
        "itemOffered": {"@type": "Product", "name": "{{主力产品}}" }
      }
    },
    {
      "@type": "Person",
      "@id": "https://{{主域}}/#{{人物 slug}}",
      "name": "{{姓名}}",
      "jobTitle": "{{CEO}}",
      "worksFor": {"@id": "https://{{主域}}/#organization"},
      "email": "{{邮箱}}",
      "sameAs": ["{{LinkedIn 个人档案}}"]
    },
    {
      "@type": "ItemList",
      "name": "{{产品线总称}}",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "{{产品线1}}", "url": "https://{{主域}}/{{路径1}}"},
        {"@type": "ListItem", "position": 2, "name": "{{产品线2}}", "url": "https://{{主域}}/{{路径2}}"}
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "{{买家原话问句，含品牌/地域/场景限定词}}",
          "acceptedAnswer": {"@type": "Answer", "text": "{{答案，务必含可量化数字}}"}
        }
      ]
    }
  ]
}
</script>
```

**写作要点**
- `description` 用「品类 + 地域 + 年限 + 服务对象」四要素，这是引擎生成摘要最爱抓的句式
- `alternateName` 解决品牌别名归一（E-03/E-04）
- `sameAs` 把社媒资产接进实体（现成素材，多数站忘了写）
- FAQ 的 `name` 必须是**买家会问 AI 的原话**，不是产品特点标题
- FAQ 的 `text` 里塞数字：年限 / 响应时效 / 赔付承诺 / 服务天数

---

## 2. 产品页 Product

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{型号 + 品名}}",
  "sku": "{{型号}}",
  "brand": {"@type": "Brand", "name": "{{品牌}}"},
  "manufacturer": {"@id": "https://{{主域}}/#organization"},
  "description": "{{一句话用途 + 适用场景}}",
  "image": ["{{主图绝对地址}}"],
  "additionalProperty": [
    {"@type": "PropertyValue", "name": "PCB Width", "value": "{{值}}", "unitText": "mm"},
    {"@type": "PropertyValue", "name": "Capacity", "value": "{{值}}", "unitText": "CPH"},
    {"@type": "PropertyValue", "name": "Temperature Accuracy", "value": "±{{值}}", "unitText": "°C"},
    {"@type": "PropertyValue", "name": "Power", "value": "{{值}}", "unitText": "kW"}
  ],
  "offers": {
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "priceCurrency": "USD",
    "priceSpecification": {"@type": "PriceSpecification", "price": "{{可填询价则不填 price}}"},
    "seller": {"@id": "https://{{主域}}/#organization"}
  }
}
</script>
```

> ⚠️ `additionalProperty` 是"参数型问句"能否召回的关键。没有它，产品页在引擎眼里就是一堆形容词。
> 页面正文**必须同时有 `<table>` 参数表**——schema 与可见内容要互相印证，否则可信度打折。

---

## 3. 面包屑 BreadcrumbList

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"Home","item":"https://{{主域}}/"},
    {"@type":"ListItem","position":2,"name":"{{一级分类}}","item":"https://{{主域}}/{{一级路径}}"},
    {"@type":"ListItem","position":3,"name":"{{二级分类}}","item":"https://{{主域}}/{{二级路径}}"},
    {"@type":"ListItem","position":4,"name":"{{当前产品}}"}
  ]
}
</script>
```

---

## 4. 文章 Article / BlogPosting

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{标题 ≤110 字符}}",
  "description": "{{摘要}}",
  "image": "{{主图}}",
  "datePublished": "{{YYYY-MM-DD}}",
  "dateModified": "{{YYYY-MM-DD}}",
  "author":    {"@id": "https://{{主域}}/#{{人物 slug}}"},
  "publisher": {"@id": "https://{{主域}}/#organization"},
  "mainEntityOfPage": {"@type":"WebPage","@id":"https://{{主域}}/{{文章路径}}"}
}
</script>
```

> `dateModified` 会显著影响新鲜度信号。**只有内容真的改了才更新**——批量刷时间戳会被识破。

---

## 5. 视频 VideoObject

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "{{视频标题}}",
  "description": "{{说明，尽量含可量化信息}}",
  "thumbnailUrl": ["{{缩略图}}"],
  "uploadDate": "{{YYYY-MM-DD}}",
  "duration": "PT{{M}}M{{S}}S",
  "contentUrl": "https://www.youtube.com/watch?v={{ID}}",
  "embedUrl": "https://www.youtube.com/embed/{{ID}}",
  "transcript": "{{文字稿 —— 强烈建议填，这是被引用的主力文本}}",
  "publisher": {"@id": "https://{{主域}}/#organization"}
}
</script>
```

---

## 6. OG + canonical 全站通用

```html
<!-- 每个页面都要有 -->
<link rel="canonical" href="https://{{主域}}{{当前路径}}" />

<!-- 多语种：注意 href 必须带完整协议 -->
<link rel="alternate" hreflang="en" href="https://{{主域}}/" />
<link rel="alternate" hreflang="es" href="https://{{主域}}/es/" />
<link rel="alternate" hreflang="x-default" href="https://{{主域}}/" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="{{品牌}}" />
<meta property="og:title" content="{{页面标题}}" />
<meta property="og:description" content="{{页面摘要}}" />
<meta property="og:image" content="{{1200×630 绝对地址}}" />
<meta property="og:url" content="https://{{主域}}{{当前路径}}" />
<meta name="twitter:card" content="summary_large_image" />
```

---

## 7. 校验方式

上线后自查，任一环节失败都会让 schema 白写：

```bash
# 1. 语法必须是合法 JSON（提取 ld+json 内容后解析）
python3 - <<'PY'
import re, json
h = open('page.html', encoding='utf-8').read()
for i, b in enumerate(re.findall(
        r'application/ld\+json[^>]*>(.*?)</script>', h, re.S)):
    try:
        d = json.loads(b)
        print(f"  block {i}: OK  @type={d.get('@type') or [x.get('@type') for x in d.get('@graph',[])]}")
    except Exception as e:
        print(f"  block {i}: JSON 语法错误 -> {e}")
PY

# 2. 官方校验（联网）
#    https://validator.schema.org/
#    https://search.google.com/test/rich-results

# 3. 复扫：重新跑 geo_scan.py，确认 jsonld_total > 0 且类型齐全
python3 scripts/geo_scan.py --url https://{{主域}} --out after.json
```

**升级记录**：新增模板时在本文件顶部目录追加一行，并在 `CHANGELOG.md` 记一笔。
