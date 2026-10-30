# -*- coding: utf-8 -*-
"""2026-10-23 revision: S-MVF01 is a separate model from SBF2002; 32 mm carrier tape -> host 32 mm tape feeder + SM nozzle is confirmed.
Applies the changed keys to the six translated i18n files (en.json comes from en_src.py). Idempotent."""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "i18n")
T = {
 "es": {
  "mx_src_mvf": "Plantilla de cualificación del alimentador de banda alternativa S-MVF01, 4 conectores",
  "mx_f_smvf01n": "Alimentador de banda alternativa",
  "mx_f_smvf01d": "Modelo distinto del SBF2002 del catálogo V03, con sus propias fichas técnicas, manual y vídeos, y su propia gama de componentes. Alimentación a granel: una banda motorizada eleva las piezas sueltas hasta una pista de selección, las rechazadas vuelven por la banda, las aceptadas llegan al punto de recogida por vibración directa y un sensor de fibra óptica confirma la pieza. Comunicación IO o funcionamiento autónomo. La compatibilidad se confirma pieza a pieza con una muestra.",
  "mx_fo_smvf01": "S-MVF01 banda alternativa (granel)",
  "mx_f_host_taped": "Correspondencia confirmada para piezas en cinta portadora de 32 mm: funcionan en el alimentador de cinta de 32 mm propio de la insertadora, y Southern Machinery suministra la boquilla o la pinza para la pieza.",
  "mx_note_host_tape": "Correspondencia confirmada: usa el alimentador de cinta de 32 mm propio de la máquina; Southern Machinery aporta la boquilla o la pinza.",
  "fr7a": "Cinta portadora embutida de 32 mm",
  "fr7b": "Alimentador de cinta de 32 mm de la propia máquina + boquilla Southern Machinery",
  "fr7c": "Correspondencia confirmada: el alimentador de cinta es el de la máquina; Southern Machinery aporta la boquilla o la pinza.",
  "disc_h2": "Transparencia: cinco puntos lado a lado",
  "q1a_add": " El alimentador de banda alternativa S-MVF01 es un modelo distinto del SBF2002, con su propia ficha; las piezas a granel se asignan a él pieza a pieza.",
  "fam6": "Alimentador de banda alternativa S-MVF01"},
 "pt": {
  "mx_src_mvf": "Modelo de qualificação do alimentador de esteira alternativa S-MVF01, 4 conectores",
  "mx_f_smvf01n": "Alimentador de esteira alternativa",
  "mx_f_smvf01d": "Modelo distinto do SBF2002 do catálogo V03, com fichas técnicas, manual e vídeos próprios e a sua própria gama de componentes. Alimentação a granel: uma esteira motorizada eleva as peças soltas até uma pista de seleção, as rejeitadas voltam pela esteira, as aceitas chegam ao ponto de coleta por vibração direta e um sensor de fibra óptica confirma a peça. Comunicação IO ou operação autônoma. A compatibilidade é confirmada peça a peça com uma amostra.",
  "mx_fo_smvf01": "S-MVF01 esteira alternativa (granel)",
  "mx_f_host_taped": "Mapeamento confirmado para peças em fita portadora de 32 mm: rodam no alimentador de fita de 32 mm da própria máquina de inserção, e a Southern Machinery fornece o bico ou a garra para a peça.",
  "mx_note_host_tape": "Mapeamento confirmado: roda no alimentador de fita de 32 mm da própria máquina; a Southern Machinery fornece o bico ou a garra.",
  "fr7a": "Fita portadora embutida de 32 mm",
  "fr7b": "Alimentador de fita de 32 mm da própria máquina + bico Southern Machinery",
  "fr7c": "Mapeamento confirmado: o alimentador de fita é o da máquina; a Southern Machinery fornece o bico ou a garra.",
  "disc_h2": "Transparência: cinco pontos lado a lado",
  "q1a_add": " O alimentador de esteira alternativa S-MVF01 é um modelo distinto do SBF2002, com ficha própria; as peças a granel são associadas a ele peça a peça.",
  "fam6": "Alimentador de esteira alternativa S-MVF01"},
 "fr": {
  "mx_src_mvf": "Modèle de qualification du chargeur à bande alternative S-MVF01, 4 connecteurs",
  "mx_f_smvf01n": "Chargeur à bande alternative",
  "mx_f_smvf01d": "Modèle distinct du SBF2002 du catalogue V03, avec ses propres fiches techniques, manuel et vidéos, et sa propre gamme de composants. Alimentation en vrac : une bande motorisée monte les pièces en vrac vers une piste de sélection, les pièces refusées retournent par la bande, les pièces acceptées rejoignent le point de prise par vibration directe et un capteur à fibre optique confirme la pièce. Communication IO ou fonctionnement autonome. L'adéquation se confirme pièce par pièce avec un échantillon.",
  "mx_fo_smvf01": "S-MVF01 bande alternative (vrac)",
  "mx_f_host_taped": "Correspondance confirmée pour les pièces en bande porteuse de 32 mm : elles passent sur le chargeur bande 32 mm propre à l'insertionneuse, et Southern Machinery fournit la buse ou la pince adaptée à la pièce.",
  "mx_note_host_tape": "Correspondance confirmée : passe sur le chargeur bande 32 mm propre à la machine ; Southern Machinery fournit la buse ou la pince.",
  "fr7a": "Bande porteuse alvéolée de 32 mm",
  "fr7b": "Chargeur bande 32 mm propre à la machine + buse Southern Machinery",
  "fr7c": "Correspondance confirmée : le chargeur bande est celui de la machine ; Southern Machinery fournit la buse ou la pince.",
  "disc_h2": "Transparence : cinq points côte à côte",
  "q1a_add": " Le chargeur à bande alternative S-MVF01 est un modèle distinct du SBF2002, avec sa propre fiche ; les pièces en vrac lui sont attribuées pièce par pièce.",
  "fam6": "Chargeur à bande alternative S-MVF01"},
 "ar": {
  "mx_src_mvf": "نموذج تأهيل مغذي الحزام الترددي S-MVF01، 4 موصلات",
  "mx_f_smvf01n": "مغذي الحزام الترددي",
  "mx_f_smvf01d": "طراز مستقل عن SBF2002 الوارد في الكتالوج V03، وله أوراق مواصفات ودليل ومقاطع فيديو خاصة به ونطاق مكونات خاص به. تغذية المواد السائبة: يرفع حزام يعمل بمحرك القطع السائبة إلى مسار انتقاء، وتعود القطع المرفوضة على الحزام، وتصل القطع المقبولة إلى نقطة الالتقاط بالاهتزاز المباشر، ويؤكد حساس ألياف ضوئية وجود القطعة. اتصال IO أو تشغيل مستقل. تُؤكَّد ملاءمة كل مكوّن بعينة.",
  "mx_fo_smvf01": "S-MVF01 حزام ترددي (سائب)",
  "mx_f_host_taped": "مطابقة مؤكدة للمكونات على شريط حامل 32 مم: تعمل على مغذي الشريط 32 مم الخاص بآلة الإدخال نفسها، وتوفر Southern Machinery الفوهة أو الملقط المناسب للمكوّن.",
  "mx_note_host_tape": "مطابقة مؤكدة: يعمل على مغذي الشريط 32 مم الخاص بالآلة نفسها؛ وتوفر Southern Machinery الفوهة أو الملقط.",
  "fr7a": "شريط حامل مُشكَّل 32 مم",
  "fr7b": "مغذي الشريط 32 مم الخاص بالآلة + فوهة Southern Machinery",
  "fr7c": "مطابقة مؤكدة: مغذي الشريط هو مغذي الآلة؛ وتوفر Southern Machinery الفوهة أو الملقط.",
  "disc_h2": "إفصاح: خمس نقاط جنبًا إلى جنب",
  "q1a_add": " مغذي الحزام الترددي S-MVF01 طراز مستقل عن SBF2002 وله ورقة مواصفات خاصة؛ وتُطابَق المكونات السائبة معه مكوّنًا مكوّنًا.",
  "fam6": "مغذي الحزام الترددي S-MVF01"},
 "ru": {
  "mx_src_mvf": "Шаблон квалификации возвратно-поступательного ленточного питателя S-MVF01, 4 разъёма",
  "mx_f_smvf01n": "Возвратно-поступательный ленточный питатель",
  "mx_f_smvf01d": "Отдельная модель, не SBF2002 из каталога V03: собственные спецификации, руководство и видео, собственный диапазон компонентов. Подача россыпи: лента с приводом поднимает детали к дорожке отбора, отбракованные возвращаются по ленте, принятые доходят до точки захвата прямой вибрацией, оптоволоконный датчик подтверждает наличие детали. Обмен по IO или автономная работа. Пригодность подтверждается для каждой детали на образце.",
  "mx_fo_smvf01": "S-MVF01 возвратно-поступательный (россыпь)",
  "mx_f_host_taped": "Подтверждённое соответствие для деталей в несущей ленте 32 мм: они работают на штатном ленточном питателе 32 мм установочной машины, а Southern Machinery поставляет насадку или захват под деталь.",
  "mx_note_host_tape": "Подтверждённое соответствие: работает со штатным ленточным питателем 32 мм; Southern Machinery поставляет насадку или захват.",
  "fr7a": "Тиснёная несущая лента 32 мм",
  "fr7b": "Штатный ленточный питатель 32 мм + насадка Southern Machinery",
  "fr7c": "Подтверждённое соответствие: ленточный питатель штатный; Southern Machinery поставляет насадку или захват.",
  "disc_h2": "Раскрытие: пять пунктов рядом",
  "q1a_add": " Возвратно-поступательный ленточный питатель S-MVF01 — отдельная модель, не SBF2002, со своей спецификацией; детали россыпью подбираются к нему поштучно.",
  "fam6": "Возвратно-поступательный ленточный питатель S-MVF01"},
 "zh": {
  "mx_src_mvf": "S-MVF01 往复式皮带供料器评估模板，4 个连接器",
  "mx_f_smvf01n": "往复式皮带供料器",
  "mx_f_smvf01d": "与目录 V03 的 SBF2002 是不同型号，有自己的规格书、说明书和视频，适用的元件范围也不同。散料供料：电机驱动的皮带把散料提升到选料轨道，不合格料随皮带回流，合格料经直振送到取料位，光纤传感器确认到料。支持 IO 通讯或独立运行。元件是否适用需逐个用样品确认。",
  "mx_fo_smvf01": "S-MVF01 往复式皮带（散料）",
  "mx_f_host_taped": "32 mm 载带元件的已确认匹配：使用插件机自带的 32 mm 载带供料器，Southern Machinery 提供适配该元件的吸嘴或夹爪。",
  "mx_note_host_tape": "已确认匹配：使用主机自带的 32 mm 载带供料器；Southern Machinery 提供吸嘴或夹爪。",
  "fr7a": "32 mm 压纹载带",
  "fr7b": "主机自带 32 mm 载带供料器 + Southern Machinery 吸嘴",
  "fr7c": "已确认匹配：载带供料器为主机自带；Southern Machinery 提供吸嘴或夹爪。",
  "disc_h2": "信息披露：五处并列说明",
  "q1a_add": "S-MVF01 往复式皮带供料器与 SBF2002 是不同型号，有自己的规格书；散料元件需逐个评估是否适用。",
  "fam6": "S-MVF01 往复式皮带供料器"},
}
for lang, kv in T.items():
    p = os.path.join(D, lang + ".json"); d = json.load(open(p, encoding="utf-8"))
    # disclosure: drop the old row 1 (SBF2002 vs S-MVF01) once, shift rows 2..6 to 1..5
    if "dr6a" in d:
        for i in range(1, 6):
            for s in "abcd":
                d["dr%d%s" % (i, s)] = d["dr%d%s" % (i + 1, s)]
        for s in "abcd":
            del d["dr6" + s]
    add = kv.pop("q1a_add")
    if "S-MVF01" not in d["q1a"]:
        d["q1a"] = d["q1a"].rstrip() + add
    d.update(kv)
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(lang, len(d))

# status "conf" (confirmed mapping with a feeder outside Catalog V03) + sentence in the mapping-rules note
S = {
 "es": ("Correspondencia confirmada", " 'Correspondencia confirmada' es una asignación confirmada a un alimentador fuera del catálogo V03: el alimentador de cinta de 32 mm de la propia máquina o el S-MVF01."),
 "pt": ("Mapeamento confirmado", " 'Mapeamento confirmado' é uma associação confirmada a um alimentador fora do catálogo V03: o alimentador de fita de 32 mm da própria máquina ou o S-MVF01."),
 "fr": ("Correspondance confirmée", " « Correspondance confirmée » désigne une association confirmée avec un chargeur hors catalogue V03 : le chargeur bande 32 mm propre à la machine ou le S-MVF01."),
 "ar": ("مطابقة مؤكدة", " «مطابقة مؤكدة» تعني ربطًا مؤكدًا بمغذٍّ من خارج الكتالوج V03: مغذي الشريط 32 مم الخاص بالآلة نفسها أو S-MVF01."),
 "ru": ("Подтверждённое соответствие", " «Подтверждённое соответствие» — подтверждённая привязка к питателю вне каталога V03: штатному ленточному питателю 32 мм или S-MVF01."),
 "zh": ("已确认匹配", "「已确认匹配」表示与目录 V03 之外的供料器的已确认配对：主机自带的 32 mm 载带供料器或 S-MVF01。"),
}
for lang, (lab, add) in S.items():
    p = os.path.join(D, lang + ".json"); d = json.load(open(p, encoding="utf-8"))
    d["mx_s_conf"] = lab
    if "S-MVF01" not in d["mx_note"]:
        d["mx_note"] = d["mx_note"].rstrip() + add
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
