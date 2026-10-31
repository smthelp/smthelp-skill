# <MODEL> factory acceptance checklist kit. ZH and EN 1:1, one numbering for both files.
# basis: M = manual ; P = product document ; G = general SMT FAT practice (rendered as 【推测】/[Assumed]) ;
#        M+G / P+G = documented item with an assumed threshold or tolerance ; M+P = both documents
# Full worked example: ../../examples/s-jvf02/checklist.py ; section guide: ../../references/fat-checklist-guide.md

META_FAT = dict(
 model="<SM model>",
 title_zh="<SM 型号> <中文品名> 出厂验收检查表",
 title_en="<SM model> <product name> – Factory Acceptance Checklist",
 basis_doc_zh="说明书 = <manual name/rev>；产品资料 = <spec source>",
 basis_doc_en="Manual = <manual name/rev>; Product doc = <spec source>",
 info_zh=["序列号：", "订单号：", "测试工装 / 主机：", "环境温度：", "验收日期："],
 info_en=["Serial no.:", "Order no.:", "Test fixture / host:", "Ambient temp.:", "FAT date:"],
)

SECTIONS = [  # standard A–K; drop a section only if the product truly has nothing in it (then keep the item as NA)
 ("A", "文件与标识", "Documents and marking"),
 ("B", "外观与结构", "Appearance and structure"),
 ("C", "机构装配与螺丝紧固", "Mechanical assembly and fastening"),
 ("D", "安装与锁定", "Installation and locking"),
 ("E", "物料固定 / 上料", "Material fixing / loading"),
 ("F", "供料机构（振动 / 皮带 / 气动）", "Feeding mechanism (vibration / belt / pneumatic)"),
 ("G", "指示、传感器与光电检测", "Indicators, sensors and photoelectric detection"),
 ("H", "电气与安全", "Electrical and safety"),
 ("I", "规格参数核对", "Specification check"),
 ("J", "运行试验", "Running test"),
 ("K", "包装与出货", "Packing and shipping"),
]

# (section, item_zh, item_en, criterion_zh, criterion_en, method_zh, method_en, basis)
ITEMS = [
 ("A", "铭牌", "Nameplate", "<量化判定>", "<quantified criterion>", "<方法>", "<method>", "P+G"),
]
