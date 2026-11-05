# 输入约定

## 文件类型
| 类型 | 扩展名 | 处理 |
|---|---|---|
| 介绍文档 | .pdf | `pdftotext -layout` 文字，`pdfimages -png -p` 图片（按页编号） |
| 演示文稿 | .pptx | 按幻灯片顺序取文字；`ppt/media/` 下 >20 KB 的图片、mp4、glb 全部取出 |
| Word | .docx | 段落文字 + `word/media/` |
| 表格 | .xlsx .csv | 逐行文字（xlsx 需 openpyxl） |
| 3D | .glb .gltf .stl .obj .ply .step .stp .fbx；pptx 内嵌 glb | `model_prep.py` 统一转 GLB |
| 视频 | .mp4 .mov .webm | 取时长/分辨率；上传公开 Drive 文件夹后作为"片段"嵌入 |
| 图片 | .png .jpg .webp | 先查图床有无同款，没有才内嵌 |

## 命名与来源规则
- 页面文件名、title 来自用户给的原始文件名（SEO 化），例如 "SMT PCB Loader solution" → `smt-pcb-loader-solution-...-smart-ems-factory.html`。
- 型号、数字只能来自文档、目录板、视频板标题或用户；每条规格写明来源（`src_*` 键）。
- 两份文档数字不同：都列进披露表（Document A / Document B / What to rely on），不要自己挑一个。
- 报价单：隐去单价、总价、客户名、国家、报价号、销售人员；`privacy_terms` 写入这些字符串，validate 会拦截。
- 联系方式以品牌标准为准：info@smthelp.com、wa.me/8613602562576；文档里出现的其他电话（如 frank@、wendy@）不上页面。

## 最少要有
产品名称、至少一个型号及尺寸/能力参数、至少 4 张图（图床或资料内）。缺少时先问用户，不编造。
