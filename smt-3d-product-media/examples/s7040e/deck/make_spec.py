#!/usr/bin/env python3
"""S7040E Eyelet Insertion Machine (4 heads, 4 vibration bowls, bulk eyelets) - standard product presentation, EN + ZH.
Facts: AGENTS.md v2 (all S70xx = S7020T base spec, S7040E 4 heads/4 feeders, eyelet range 1.3-4.0 mm sec 4.3, clinch 'pressing to blossom' sec 3.3,
bowl feeding flow sec feeders); S7020T manual; Jason PDF 'S-7000 Eyelet Pin Insertion Machine Solution' (bottom-die blossoming, UPS option not used).
Video slide uses {video}/{poster} placeholders filled by smt-3d-product-media."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "AGENTS.md v2 sec 4.2 (Jason, 2026-11-07); S7020 Series 202303; S7020T manual"

def spec(L):
    en = L == "en"; t = lambda e, z: e if en else z
    S = []
    S.append({"type": "overview", "title": t("S7040E at a Glance", "S7040E 产品概览"),
      "lead": t("A dedicated eyelet insertion machine: 4 insertion heads and 4 vibration bowls insert bulk eyelets and flare them from below, with vision correction and insertion check on every point.",
                "专用铆钉插件机：4 个插件头、4 个振动盘，插入散装铆钉并从底部铆压开花，每个点都有视觉校正和插入检测。"),
      "apps": [[t("Parts", "元件"), t("Eyelets, hollow rivets and rivet pins, Ø1.3–4.0 mm, up to 4 sizes per board", "铆钉、空心铆钉、铆柱，Ø1.3–4.0 mm，每板最多 4 种规格")],
               [t("Industries", "行业"), t("Appliance and power boards, single-sided boards needing reinforced holes", "家电与电源板、需要孔位加强的单面板")],
               [t("Feeding", "供料"), t("4 vibration bowls for bulk eyelets (reel feeder optional)", "4 个振动盘供散装铆钉（可选 Reel 料盘）")]],
      "image": "eyelet_pcb_top.jpg", "caption": t("Board with inserted eyelets", "已插铆钉的电路板"),
      "notes": "Eyelet range Ø1.3–4.0 mm: AGENTS 4.3 (S7040E, S-7000E Upgrade). Photo: Jason upload 'Eyelet Insertion PCB'."})
    S.append({"type": "pains", "title": t("Why Manual Eyelet Insertion Holds Lines Back", "人工插铆钉的瓶颈"),
      "lead": t("Eyelets are tiny and must be flared evenly. Hand insertion and hand riveting cap output and quality.",
                "铆钉细小且需均匀开花。人工插钉、人工铆压限制了产量和质量。"),
      "items": [[t("Slow, two steps", "慢，两道工序"), t("Insert by hand, then rivet at a press", "人工插钉，再到压机上铆压")],
                [t("Uneven flaring", "开花不均"), t("Cracked or loose eyelets fail at soldering", "开裂或松动，焊接时出问题")],
                [t("Missing eyelets", "漏插"), t("Found only after soldering, then reworked", "焊后才发现，只能返工")],
                [t("Many sizes", "规格多"), t("Mixing diameters by hand causes errors", "人工混用不同直径易出错")],
                [t("Labour dependence", "依赖人工"), t("Output follows headcount and turnover", "产量随人数和流失率波动")],
                [t("No traceability", "无法追溯"), t("No record of what was inserted and when", "无法记录插了什么、何时插")]],
      "notes": "Qualitative customer pains. No figures claimed."})
    S.append({"type": "metrics", "title": t("Key Figures", "关键参数"),
      "lead": t("S7040E = S7020T platform with 4 insertion heads and 4 feeders, dedicated to eyelets.", "S7040E = S7020T 平台 + 4 个插件头 + 4 个供料器，专用于铆钉。"),
      "items": [["4 + 4", t("Heads + bowls", "插件头 + 振动盘"), t("Up to 4 eyelet sizes, no changeover", "最多 4 种铆钉，无需换型")],
                ["0.5 s", t("Per part", "每件"), t("7,200 parts/h net insertion", "净插件 7,200 件/小时")],
                ["Ø1.3–4.0", t("Eyelet diameter (mm)", "铆钉直径 (mm)"), t("Gripper and die per size", "每种规格配夹爪与底模")],
                ["0.015 mm", t("Vision correction", "视觉校正"), t("Automatic hole / Mark correction", "自动孔位 / Mark 校正")]],
      "footer": t("7,200 parts/h = 3,600 s ÷ 0.5 s, insertion only; PCB in/out and Mark reading are added per board.",
                  "7,200 件/小时 = 3,600 秒 ÷ 0.5 秒，仅计插件；每块板另计进出板与 Mark 识别时间。"),
      "notes": SRC + ". 0.5 s/part unified figure (Jason)."})
    S.append({"type": "fab", "title": t("FAB 1 · Four Heads, Four Bowls", "FAB 1 · 4 头 4 振动盘"),
      "rows": [[[t("4 insertion heads", "4 个插件头"), t("Gripper sized per eyelet", "按铆钉规格设计夹爪")], [t("4 sizes, one pass", "一次 4 种规格"), t("No changeover between them", "规格之间无需换型")], [t("More output", "产量更高"), t("Replaces several hand stations", "替代多个人工工位")]],
               [[t("4 vibration bowls", "4 个振动盘"), t("Bulk eyelets oriented flange-up", "散装铆钉自动排向，帽沿朝上")], [t("Track and slider", "轨道与滑块"), t("One eyelet at a time to the head", "逐个送到插件头")], [t("Less handling", "减少人工"), t("Operators only refill", "操作员只需补料")]],
               [[t("Bottom clinch die", "底部铆压模"), t("Splits and flares each eyelet", "切开并压开每个铆钉")], [t("Insert and rivet in one", "插铆一体"), t("No separate press step", "无需另设压机工序")], [t("Even flaring", "开花均匀"), t("Firm eyelets before soldering", "焊前铆钉牢固")]]],
      "notes": "Bowl flow (sort -> linear track -> slider -> air to gripper): AGENTS feeder section (S-7000E). Bottom die splits and flares ('pressing to blossom'): AGENTS 3.3."})
    S.append({"type": "fab", "title": t("FAB 2 · Accuracy, Checks and Data", "FAB 2 · 精度、检测与数据"),
      "rows": [[[t("Vision correction", "视觉校正"), t("Hole and Mark correction 0.015 mm", "孔位与 Mark 校正 0.015 mm")], [t("Hits every hole", "精准对孔"), t("Corrects board tolerance", "补偿电路板公差")], [t("Fewer misses", "减少漏插"), t("Less rework before soldering", "焊前返工更少")]],
               [[t("Insertion detection", "插入检测"), t("Base supports and checks each eyelet", "底座支撑并检测每个铆钉")], [t("Stops and alarms", "停机报警"), t("Missing parts caught at once", "漏插即时发现")], [t("No missing eyelets", "杜绝漏插"), t("Caught before soldering", "焊接前即拦截")]],
               [[t("Excel / USB programming", "Excel / USB 编程"), t("Online visual teaching", "在线视觉示教")], [t("Fast new programs", "新程序快"), t("Import coordinates, no retyping", "导入坐标，无需重输")], [t("RS-232C to MES", "RS-232C 接 MES"), t("Production data for traceability", "生产数据可追溯")]]],
      "notes": "Correction 0.015 mm, insertion detection: S7020T manual. Programming/communication: AGENTS 4.2."})
    S.append({"type": "video", "title": t("How It Works", "工作原理"),
      "lead": t("3D working principle (4 heads, 4 bowls, bulk eyelets) plus real 4-head bulk insertion footage.", "3D 工作原理（4 头 4 振动盘、散装铆钉），含 4 头散装插件实机视频。"),
      "items": [{"video": "{video}", "poster": "{poster}", "head": t("3D + real machine video", "3D 动画 + 实机视频"),
                 "body": [t("PCB in, feed, insert, flare, out", "进板、供料、插件、铆压、出板"), t("Voiceover, EN and ZH versions", "带配音，中英两版")]}],
      "notes": "Video by smt-3d-product-media from 'Pin Eyelet Inserter.STEP' with 4-head copies. Real clips (Drive): 5 插件头散装供料 r1, bowl r2, 马来西亚插片+铆柱.mp4, 插针机.mp4. No pure-eyelet clip found in Drive."})
    S.append({"type": "process", "title": t("Insertion Cycle in Six Steps", "插件流程"),
      "steps": [[t("Load", "进板"), t("Loader feeds PCB, clamp", "上板机送板并夹紧")], [t("Feed", "供料"), t("Bowl to track to head", "振动盘经轨道送到插件头")], [t("Correct", "校正"), t("Camera reads Mark / hole", "相机识别 Mark / 孔位")],
                [t("Insert", "插件"), t("Head presses eyelet in", "插件头压入铆钉")], [t("Flare", "铆压"), t("Bottom die splits and flares", "底模切开并压成开花")], [t("Unload", "出板"), t("Into magazine", "送入料框")]],
      "images": [["s7040e_insert.jpg", t("4 heads over the board (3D)", "4 个插件头作业（3D）")], ["real_rivet_posts.jpg", t("Bottom clinch dies", "底部铆压模")], ["eyelet_pcb_bottom.jpg", t("Flared eyelets, solder side", "焊接面铆钉开花")]],
      "notes": "Flow per S7020T manual sec 2.2 + AGENTS 3.3. real_rivet_posts.jpg: frame of Drive '马来西亚插片+铆柱.mp4'. eyelet_pcb_bottom.jpg: Jason upload P31012-094046."})
    S.append({"type": "gallery", "title": t("Design Details", "设计细节"),
      "items": [{"image": "real_4heads.jpg", "head": t("4 insertion heads", "4 个插件头"), "body": [t("Gripper per eyelet size", "每种规格专用夹爪"), t("Servo-driven X/Y table", "伺服驱动 X/Y 工作台")]},
                {"image": "bowls_inside.png", "head": t("4 vibration bowls", "4 个振动盘"), "body": [t("Bulk eyelets, no tape cost", "散装铆钉，无编带成本"), t("Reel feeder optional", "可选 Reel 料盘")]},
                {"image": "eyelet_heads.jpg", "head": t("Eyelet insertion heads", "铆钉插件头"), "body": [t("Holds eyelet until seated", "夹持至铆钉到位"), t("Element spacing ≥ 2 mm", "元件间距 ≥ 2 mm")]},
                {"image": "eyelet_pcb_bottom.jpg", "head": t("Flared on the solder side", "焊接面开花"), "body": [t("Even, firm flaring", "开花均匀牢固"), t("Vertical error ≤ 0.8°", "垂直误差 ≤ 0.8°")]}],
      "notes": "Element spacing ≥ 2 mm, vertical error ≤ 0.8°: AGENTS 4.2 (S7020 Series 202303). eyelet_heads.jpg: Jason PDF p5 (2-head eyelet unit, S-7000)."})
    S.append({"type": "gallery", "title": t("Complete Line, Magazine to Magazine", "完整产线：料框进，料框出"),
      "items": [{"image": "s7040e_3d_hero.jpg", "fit": True, "head": t("Loader + S7040E + unloader", "上板机 + S7040E + 下板机"), "body": [t("SLD250 loader, SULD250 unloader", "SLD250 上板机，SULD250 下板机"), t("SMEMA linked", "SMEMA 连线")]},
                {"image": "site_S7040E.jpg", "head": t("S70xx platform outline", "S70xx 平台外形"), "body": [t("Left-to-right PCB flow", "PCB 左进右出"), "1700 × 1300 × 1600 mm"]}],
      "imgh": 3.3,
      "notes": "Loader/unloader default SLD250 + SULD250 (AGENTS). site_S7040E.jpg = real S7020T installation with label changed to S7040E (same outline) - pending Jason OK for external use; do not caption as S7040E customer site."})
    S.append({"type": "specs", "title": t("S7040E Specifications", "S7040E 技术参数"),
      "rows": [[t("Insertion heads / feeders", "插件头 / 供料器"), "4 / 4"],
               [t("Feeding", "供料方式"), t("4 vibration bowls, bulk eyelets (reel optional)", "4 个振动盘，散装铆钉（可选 Reel）")],
               [t("Eyelets", "适用铆钉"), t("Diameter 1.3–4.0 mm; eyelets, hollow rivets, rivet pins", "直径 1.3–4.0 mm；铆钉、空心铆钉、铆柱")],
               [t("Clinch", "铆压"), t("Bottom die splits and flares the eyelet", "底模切开铆钉并压成开花")],
               [t("Speed", "速度"), t("0.5 s per part", "0.5 秒/件")],
               [t("PCB size", "PCB 尺寸"), t("80 × 80 to 380 × 280 mm (larger customizable)", "80 × 80 至 380 × 280 mm（可定制加大）")],
               [t("Insertion angle", "插件角度"), t("360°, 1° increment", "360°，1° 步进")],
               [t("Vision correction", "视觉校正"), "0.015 mm"],
               [t("Programming", "编程"), t("Online visual, Excel, USB import", "在线视觉示教、Excel、USB 导入")],
               [t("Communication", "通讯"), t("RS-232C, MES connection", "RS-232C，可接 MES")],
               [t("Power / air", "电源 / 气源"), t("Single 220 V AC, 50/60 Hz, 1.6 KVA; 5–6 kgf/cm²", "单相 220 V AC，50/60 Hz，1.6 KVA；5–6 kgf/cm²")],
               [t("Dimensions", "外形尺寸"), "1700 × 1300 × 1600 mm"],
               [t("Weight", "重量"), "1500 kg"]],
      "footer": t("Dimensions without loader and unloader. Other voltages on request.", "尺寸不含上下板机。其他电压可按需定制。"),
      "notes": SRC + ". All S70xx incl. S7040E use S7020T base specs (Jason 2026-11-07); old S7040E PDF figures and the S-7000 PDF (8000 CPH, 2300 x 1340 x 1860) retired."})
    S.append({"type": "table", "title": t("S70xx Series Model Guide", "S70xx 系列选型"),
      "columns": [t("Model", "型号"), t("Dedicated parts", "专用元件"), t("Heads / feeders", "插件头 / 供料器"), t("Feeding", "供料方式"), t("Speed", "速度")],
      "widths": [1.6, 3, 2, 2.6, 1.6],
      "rows": [[m, p, hf, t("Bowl or reel", "振动盘或料带"), t("0.5 s / part", "0.5 秒/件")] for m, p, hf in [
               ("S7020T", t("Terminal", "端子"), "2 / 2"), ("S7040T", t("Terminal", "端子"), "4 / 4"), ("S7020P", "PIN", "2 / 2"), ("S7040P", "PIN", "4 / 4"),
               ("S7020E", t("Eyelet", "铆钉"), "2 / 2"), ("S7040E", t("Eyelet", "铆钉"), "4 / 4"), ("S7020S", t("Tact switch", "轻触开关"), "2 / 2")]],
      "lead": t("One platform, one footprint: choose the part type and 2 or 4 heads.", "同一平台、同一占地：按元件类型选择 2 头或 4 头。"),
      "footer": t("All models: 1700 × 1300 × 1600 mm, 1500 kg, 1.6 KVA, PCB 380 × 280 mm (customizable).", "全系列：1700 × 1300 × 1600 mm，1500 kg，1.6 KVA，PCB 380 × 280 mm（可定制）。"),
      "notes": "Naming S70<heads>0<letter>; all models S7020T base spec (Jason 2026-11-07)."})
    S.append({"type": "table", "title": t("Capacity Example", "产能示例"),
      "columns": [t("Eyelets per board", "每板铆钉数"), t("Insertion (s)", "插件 (秒)"), t("+ PCB in/out & Mark (s)", "+ 进出板与 Mark (秒)"), t("s / board", "秒/板"), t("Boards / h", "板/小时")],
      "widths": [2, 1.8, 2.8, 1.6, 1.6],
      "rows": [["10", "5", "5", "10", "360"], ["20", "10", "5", "15", "240"], ["28", "14", "5", "19", "189"], ["40", "20", "5", "25", "144"]],
      "lead": t("0.5 s per eyelet, plus 4 s PCB in/out and 1 s Mark reading per board.", "每个铆钉 0.5 秒，每块板另加 4 秒进出板和 1 秒 Mark 识别。"),
      "footer": t("Boards/h = 3,600 ÷ s/board, rounded down, before efficiency factor. Confirm with your board in a sample run.",
                  "板/小时 = 3,600 ÷ 秒/板，向下取整，未计效率系数。以客户电路板试插结果为准。"),
      "notes": "28 eyelets = 20 + 8 example board in Jason's S-7000 PDF (p3/p4). PCB in/out 4 s + Mark 1 s: same assumption as S7040P/S7020T decks."})
    S.append({"type": "summary", "title": t("Summary & Next Step", "总结与下一步"),
      "lead": t("S7040E inserts and flares up to four eyelet sizes per pass at 0.5 s per part, with vision correction and insertion check.",
                "S7040E 一次插入并铆压最多 4 种规格铆钉，0.5 秒/件，配视觉校正和插入检测。"),
      "items": [[t("4 heads, 4 bowls", "4 头 4 振动盘"), t("Bulk eyelets, no changeover", "散装铆钉，无需换型")],
                [t("Insert and flare", "插铆一体"), t("Bottom die flares every eyelet", "底模逐个铆压开花")],
                [t("Complete line", "完整产线"), t("SLD250 loader, SULD250 unloader, SMEMA", "SLD250 上板机，SULD250 下板机，SMEMA")],
                [t("Local support", "本地支持"), t("On-site installation and operator training", "现场安装与操作培训")]],
      "cta": t("Send your PCB file and eyelet samples to info@smthelp.com for a free evaluation", "请将 PCB 文件和铆钉样品发送至 info@smthelp.com，免费评估"),
      "notes": "Brand Book CTA."})
    return {
      "meta": {"lang": L, "title": t("S7040E Eyelet Insertion Machine – 4 Heads 4 Bowl Feeders – Southern Machinery", "S7040E 铆钉插件机 – 4 头 4 振动盘 – Southern Machinery"),
               "subject": t("4-head eyelet insertion machine with 4 vibration bowls for bulk eyelets, 0.5 s per part", "4 头铆钉插件机，4 个振动盘散装供料，0.5 秒/件"),
               "keywords": "eyelet insertion machine, S7040E, eyelet inserter, hollow rivet insertion, PCB eyelet machine, vibratory bowl feeder, THT automation, Southern Machinery"},
      "labels": {"deck_label": "Product Presentation"} if en else {"contents": "目录", "deck_label": "产品介绍", "app_head": "项目", "app_sub": "内容",
                "fab": [["特点", "具备什么"], ["优势", "能做什么"], ["收益", "带来什么"]], "specs": ["参数", "规格", "参数", "规格"]},
      "title": {"eyebrow": t("EYELET INSERTION", "铆钉自动化"), "name": t("Eyelet Insertion Machine — S7040E", "铆钉插件机 — S7040E"),
                "subtitle": t("4 insertion heads and 4 vibration bowls insert and flare bulk eyelets", "4 个插件头、4 个振动盘，散装铆钉插入即铆压"),
                "tagline": t("4 heads · 4 bowl feeders · 0.5 s per part", "4 头 · 4 振动盘 · 0.5 秒/件"), "date": t("November 2026", "2026 年 11 月"), "image": "studio_S7040E.jpg",
                "notes": "Studio cutout of real S7020T photo relabeled S7040E (same outline) - pending Jason OK."},
      "contents": [[t("Overview", "产品概览"), t("What S7040E is and where it fits", "S7040E 是什么、用在哪里")], [t("Key Figures & FAB", "关键参数与 FAB"), t("Heads, bowls, speed, accuracy", "插件头、振动盘、速度、精度")],
                   [t("How It Works", "工作原理"), t("3D animation, real footage, cycle", "3D 动画、实机视频、流程")], [t("Design & Line", "设计与产线"), t("Details, clinch, loader and unloader", "细节、铆压、上下板机")],
                   [t("Specifications", "技术参数"), t("S7040E data and S70xx guide", "S7040E 参数与 S70xx 选型")], [t("Capacity", "产能"), t("Boards per hour example", "每小时产能示例")]],
      "slides": S}

for L in ("en", "zh"):
    json.dump(spec(L), open(os.path.join(HERE, f"spec-{L}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
