# S-JVF02 short-video copy pack: 10 concepts. EN is the source; ZH mirrors it 1:1.
# Shot tuple: (dur_s, size_zh, size_en, visual_zh, visual_en, osd_zh, osd_en, vo_zh, vo_en, source)
# Sources: M=Operation Manual Rev.2025 (figure no.), P=product document via landing page,
# 3D=eDrawings 3D HTML viewer (screen-record), YT=Southern Machinery YouTube clip, PH=photo library, NEW=待拍 / to shoot


META = dict(
 model="S-JVF02",
 title_en="S-JVF02 Vibration Stick Feeder for JUKI RS-1",
 title_zh="S-JVF02 振动料管飞达（JUKI RS-1 用）",
 date="2026-10-31", draft="v1",
 # every number allowed on screen, with its source (M = manual, P = product document)
 facts=["S-JVF02 (M,P)", "JUKI RS-1 (P)", "4 lanes (P)", "3 × 3 – 30 × 10 mm (P)", "66 mm sticks (P)", "365 × 66 × 125 mm (P)",
        "6.5 kg (P)", "24 V DC (P)", "15 W (P)", "14 numbered parts S-JVF02-052801…052814 (M)", "4-step install (M §4.1)",
        "5-step set-up (M §5.1)", "3-point tube fixing (M §5.1)", "+86 136 0256 2576 (SM contact)", "5 checks (count of V09 items)"],
 skills_applied="smt-brand-kit（品牌口吻、禁发清单、命名、9:16 Shorts 分镜格式、反馈日志）· smthelp-video-script（前 3 秒机器在动、参数上屏 ≥2 s、不确定数字不上屏、待拍素材清单）· b2b-short-video（一支视频一个核心点、竖屏 9:16）· smt-short-video-copy（本方法）",
 sources=[
  ["S-JVF02 Operation Manual Rev.2025 (PDF, 14 p.)", "可访问，已读全文 / Read in full", "结构、安装 4 步、料管 3 点固定、振动调节、故障表、14 项零件表、安全条款"],
  ["Product landing page (s-jvf02-vibration-stick-feeder-juki-rs-1.html)", "可访问，已读全文 / Read in full", "4 通道、3×3–30×10 mm、66 mm 料管、365×66×125 mm、6.5 kg、24 V DC、15 W；6 段 YouTube 运行视频"],
  ["4 × 3D Drawing HTML (eDrawings viewer)", "可打开，为 3D 模型查看器，无文字参数 / 3D viewer only, no text specs", "分镜中的 3D 旋转、爆炸图镜头（屏幕录制）"],
  ["Audio .wav (17 min 28 s)", "可访问，已转写 / Transcribed", "英文播客式讲解，主要是竞品与搜索意图分析 → 用于 SEO 关键词；不含新参数；竞品名称不入文案"],
 ],
 conflict_note="参数冲突提示：说明书第 3 章注明「源文件未给出电气参数、尺寸、重量」；24 V DC / 15 W / 365×66×125 mm / 6.5 kg / 4 通道 / 3×3–30×10 mm 均来自产品资料。文案已按产品资料使用，发布前请确认。",
 coverage={"V01": "整机外观与结构", "V02": "飞达供料（四通道）", "V03": "安装锁定", "V04": "机构装配与螺丝紧固", "V05": "料管固定 / 供料",
           "V06": "振动 / 皮带机构", "V07": "传感器与光电检测（指示灯）", "V08": "电气与安全：接地、绝缘、急停", "V09": "规格参数核对：型号、电压、频率、元件范围", "V10": "出厂验收汇总"},
 existing_media="已有素材：说明书插图（Fig. 2-1/2-2/4-1～4-5/9-1）、产品页实拍照片（台面整机、后视、整套出货件）、4 个 3D 查看器（录屏）、YouTube 运行视频 6 段。全部镜头不露人脸（FB-003）。",
 to_confirm=["24 V DC / 15 W、尺寸、重量、4 通道：说明书称未载，数据来自产品资料 → 请技术部确认后再上屏（V01、V02、V08、V09）。",
  "V04、V08、V10 展示的扭力检查、防松标记、接地/绝缘/急停测试、30 min 连续运行，是按通用出厂验收惯例拟定的流程（推测）；须与实际出厂流程一致后才能发布。",
  "资料未记载光电 / 料位传感器；V07 只讲指示灯与开关。如有传感器配置，请告知，补一镜。",
  "振动频率 Hz 范围未公开，V09 不上屏数字。",
  "片尾 CTA 未写「免费」评估；如需加「Free sample feeding test」，请确认后加。"],
)

CTA_EN = "Send your part list + a photo of the sticks. info@smthelp.com · WhatsApp +86 136 0256 2576"
CTA_ZH = "发料号清单和料管照片给我们：info@smthelp.com · WhatsApp +86 136 0256 2576"
DISCLAIM_EN = "JUKI and RS-1 are trademarks of their owner. Southern Machinery is an independent supplier and is not affiliated with JUKI."
DISCLAIM_ZH = "JUKI 和 RS-1 为其所有者的商标。Southern Machinery 为独立供应商，与 JUKI 无隶属关系。"

OUTRO = (3, "特写", "CU", "片尾：SM Logo 白底卡片 + 联系方式，海军蓝底", "Outro: SM logo on white card + contacts, navy background",
         "smthelp.com · WhatsApp +86 136 0256 2576", "smthelp.com · WhatsApp +86 136 0256 2576",
         "发来料号，我们帮您评估供料。", "Send your part list. We'll check the feeding.", "SM brand assets")

V = []

V.append(dict(
 id="V01", zh="整机外观与结构：30 秒看懂 S-JVF02", en="S-JVF02 anatomy in 30 seconds", dur=30,
 cover="整机外观与结构", type_zh="机型介绍（短版）", type_en="Product anatomy",
 aud_zh="EMS 工艺/设备工程师，JUKI RS-1 产线", aud_en="EMS process & equipment engineers running JUKI RS-1 lines",
 hook_zh="画面：料管里元件被振动推向吸取位；字幕「料管元件，像编带一样供料」",
 hook_en="Visual: parts vibrating forward in the stick to the pick point; text 'Stick parts. Fed like tape.'",
 shots=[
  (3,"特写","CU","料管内元件随振动前移到吸取位","Parts vibrating forward in the stick to the pick point","料管元件，像编带一样供料","Stick parts. Fed like tape.","料管元件，也能像编带一样自动供料。","Stick-packed parts, fed like tape.","YT S-JVF02 on RS-1 clip"),
  (5,"全景","WS","3D 模型 360° 旋转，整机外形","3D model, 360° turn of the whole feeder","S-JVF02 · JUKI RS-1 飞达座","S-JVF02 · for the JUKI RS-1 feeder bank","这是适配 JUKI RS-1 飞达座的 S-JVF02 振动料管飞达。","This is the S-JVF02 vibration stick feeder for the JUKI RS-1 bank.","3D viewer (any of 4)"),
  (6,"中景","MS","3D 爆炸图：主体、顶板、导轨、支撑架依次高亮","3D exploded view: main body, top plate, guide rail, support frame highlighted in turn","主体 · 顶板 · 导轨 · 支撑架","Main body · Top plate · Guide rail · Support frame","主体、顶板和导轨承载料管，支撑架托住料管尾端。","Main body, top plate and guide rail carry the sticks. The support frame holds the rear.","3D viewer exploded / M Fig. 9-1"),
  (5,"特写","CU","控制单元：两只旋钮、指示灯、开关","Control unit: two dials, pilot lamp, switch","功率旋钮 · 频率旋钮 · 指示灯 · 开关","Power dial · Frequency dial · Pilot lamp · Switch","一个控制单元：功率、频率两只旋钮，加指示灯和开关。","One control unit: power dial, frequency dial, pilot lamp and switch.","M Fig. 2-2 / PH bench photo"),
  (4,"近景","MCU","后视：手柄与飞达座连接器","Rear view: handlebar and bank connector","手柄锁紧 · 飞达座连接器","Handlebar lock · Bank connector","手柄加连接器，免工具锁进飞达座。","Handlebar and connector lock it into the bank. No tools.","PH rear-view photo"),
  (4,"中景","MS","整套出货件平铺，尺寸重量大字上屏","Full shipped set laid out, size and weight in large text","365 × 66 × 125 mm · 6.5 kg","365 × 66 × 125 mm · 6.5 kg","整机 365×66×125 毫米，6.5 公斤。","365 by 66 by 125 millimetres. 6.5 kilograms.","PH full-set photo · P spec"),
  OUTRO]))

V.append(dict(
 id="V02", zh="手工挑料是隐形瓶颈：四通道振动供料", en="The hand-picking bench is your hidden bottleneck", dur=30,
 cover="四通道供料", type_zh="改造对比（无 ROI 数字）", type_en="Before / after (method, no ROI figures)",
 aud_zh="高混线生产经理、EMS 厂长", aud_en="Production managers on high-mix EMS lines",
 hook_zh="画面：操作员手指从料管里一颗颗挑件；字幕「瓶颈不在贴片机，在这张桌子」",
 hook_en="Visual: operator picking parts out of a tube by hand; text 'Your bottleneck is this bench.'",
 shots=[
  (3,"近景","MCU","操作员从料管手工挑件放板（不露脸，仅手部）","Operator's hands picking parts from a tube (hands only, no face)","瓶颈不在贴片机，在这张桌子","Your bottleneck is this bench.","瓶颈往往不在贴片机，而在旁边这张手工挑料桌。","The bottleneck isn't the mounter. It's this bench.","NEW 待拍 (hands only)"),
  (5,"特写","CU","手工放件：极性反、混料的风险示意","Hand placement close-up: reversed-polarity / mixed-part risk","极性反 · 混料 · 疲劳","Reversed polarity · Mixed parts · Fatigue","手工挑料慢，还容易极性放反、混料。","Hand-picking is slow, and it reverses polarity and mixes parts.","NEW 待拍"),
  (6,"中景","MS","S-JVF02 四条料道同时振动供料","S-JVF02 with four lanes feeding at once","4 条独立料道","4 independent lanes","S-JVF02 有四条独立料道，四个料号，或一个料号四倍库存。","S-JVF02 runs four independent lanes: four part numbers, or four sticks of one.","YT clip / P spec"),
  (5,"特写","CU","吸嘴在开口吸取位取件","Nozzle picking at the opened pick area","一颗一颗，固定高度与姿态","One part at a time. Fixed height and attitude.","元件一颗一颗送到固定高度和姿态，吸嘴直接取。","Parts arrive one at a time, at a fixed height and attitude.","YT S-JVF02 on RS-1 clip"),
  (4,"特写","CU","一条料道空了，换上新料管，其他三道仍在振动","One lane empties, a new stick slides in, the other three keep feeding","换一条，其余三条照跑","Swap one lane. Three keep feeding.","一条料道空了就换管，其余三条不停。","When one lane empties, swap the stick. The other three keep feeding.","NEW 待拍 / YT clip"),
  (4,"中景","MS","元件尺寸窗口大字上屏 + 料管宽度","Size window in large text + stick width","元件 3×3 – 30×10 mm · 料管 66 mm","Parts 3×3 – 30×10 mm · 66 mm sticks","适用元件 3×3 到 30×10 毫米，料管宽 66 毫米。","Parts from 3 by 3 up to 30 by 10 millimetres, on 66 millimetre sticks.","P spec"),
  OUTRO]))

V.append(dict(
 id="V03", zh="四步上机：手柄抬起、对孔、对插头、松开锁紧", en="Four moves onto the RS-1 bank. No tools.", dur=15,
 cover="四步上机", type_zh="运行实况（超短）", type_en="How-to (ultra short)",
 aud_zh="产线操作员、设备技术员", aud_en="Line operators and maintenance techs",
 hook_zh="画面：手柄抬起的特写；字幕「4 步，免工具」",
 hook_en="Visual: handlebar lifting close-up; text '4 moves. No tools.'",
 shots=[
  (3,"特写","CU","抬起手柄","Raise the handlebar","① 抬起手柄","① Raise the handlebar","第一步，抬起手柄。","One: raise the handlebar.","M Fig. 4-2"),
  (3,"特写","CU","对准飞达座定位孔","Align with the bank alignment hole","② 对准定位孔","② Align the alignment hole","第二步，对准定位孔。","Two: align with the alignment hole.","M Fig. 4-3"),
  (3,"特写","CU","对准连接器推入","Align with the connector and push in","③ 对准连接器推入","③ Align the connector, push in","第三步，对准连接器推入。","Three: align the connector and push in.","M Fig. 4-4"),
  (3,"近景","MCU","松开手柄，锁定；指示灯亮","Release handlebar, locked; pilot lamp on","④ 松开手柄 = 锁定","④ Release = locked","第四步，松开手柄，锁定。","Four: release. It's locked.","M Fig. 4-5 · NEW lamp shot"),
  OUTRO]))

V.append(dict(
 id="V04", zh="机构装配与螺丝紧固：出厂前每颗螺丝都过一遍", en="Assembly and fastening: every screw checked before it ships", dur=45,
 cover="装配与紧固", type_zh="工厂实拍", type_en="Factory floor",
 aud_zh="采购工程师、质量工程师（SQE）", aud_en="Buyers and supplier-quality engineers",
 hook_zh="画面：扭力螺丝刀拧到位「咔」一声；字幕「出厂前，每颗螺丝都过一遍」",
 hook_en="Visual: torque screwdriver clicking off; text 'Every screw. Before it ships.'",
 shots=[
  (3,"特写","CU","扭力螺丝刀拧紧顶板螺丝，听到打滑声","Torque driver clicks off on a top-plate screw","每颗螺丝，出厂前都过一遍","Every screw. Before it ships.","出厂前，每一颗螺丝我们都过一遍。","Every screw gets checked before it ships.","NEW 待拍"),
  (7,"中景","MS","3D 爆炸图按装配顺序合拢：主体→导轨→顶板→前盖","3D exploded view closing in assembly order: main body → guide rail → top plate → front cover","14 个零件 · 全部有料号","14 parts · every one numbered","S-JVF02 由 14 个编号零件组成，从主体到连接器。","The S-JVF02 is built from 14 numbered parts, main body to connector.","3D viewer / M Fig. 9-1"),
  (7,"特写","CU","振动器、弹簧、板簧装配特写","Close-ups: vibrator, spring and leaf spring being fitted","振动器 · 弹簧 · 板簧","Vibrator · Spring · Leaf spring","振动器和弹簧决定振动传递，装配要到位不松动。","The vibrator and springs carry the vibration. They must sit tight.","NEW 待拍 / M parts list"),
  (6,"特写","CU","螺丝紧固后画防松标记线","Anti-loosening paint mark drawn after tightening","紧固 + 防松标记","Torqued + paint-marked","拧紧后画防松标记，运输和振动后一眼能看出有没有松。","After torque, a paint mark. Any loosening shows at a glance.","NEW 待拍"),
  (6,"近景","MCU","手柄、定位销、导轨的手动行程检查","Hand check of handlebar, locating pin and guide-rail travel","手柄回弹 · 定位销 · 导轨平行","Handlebar return · Locating pin · Rail alignment","手柄回弹、定位销、导轨平行，逐项手检。","Handlebar return, locating pin, rail alignment: each checked by hand.","NEW 待拍"),
  (6,"中景","MS","振动运行时靠近听：无异响","Running feeder, ear close: no rattle","运行无异响","No rattle under vibration","通电振动，听一遍。螺丝松了，会先在声音里暴露。","Then we run it and listen. A loose screw shows up as noise first.","NEW 待拍"),
  (7,"中景","MS","检验员在验收表上勾选合格（只拍表与手）","Inspector ticks the acceptance sheet (sheet and hands only)","出厂验收表 · 逐项签字","Factory acceptance sheet · signed line by line","每台都按出厂验收表逐项签字。","Every unit is signed off line by line on the acceptance sheet.","NEW 待拍"),
  OUTRO]))

V.append(dict(
 id="V05", zh="料管三点固定：定位环、板簧、定位块", en="Three points that fix the pick height", dur=30,
 cover="三点固定", type_zh="操作教学", type_en="Set-up how-to",
 aud_zh="操作员、工艺工程师", aud_en="Operators and process engineers",
 hook_zh="画面：元件在吸取位跳起歪斜；字幕「吸不到件？先看这三个点」",
 hook_en="Visual: a part tilting at the pick area; text 'Mis-picks? Check these three points.'",
 shots=[
  (3,"特写","CU","吸取位元件歪斜跳动","Part tilting and jumping at the pick area","吸不到件？先看这三个点","Mis-picks? Check these three points.","吸不到件，先看料管这三个固定点。","Mis-picks? Check these three points first.","NEW 待拍"),
  (6,"特写","CU","料管尾端放在支撑架上方，用定位环固定","Rear of the tube over the support frame, fixed by the locating ring","① 尾端：定位环","① Rear: locating ring","尾端放在支撑架上方，用定位环固定。","Rear end over the support frame, fixed by the locating ring.","M Fig. 2-2 · NEW"),
  (6,"特写","CU","料管中段压在板簧下","Middle of the tube under the leaf spring","② 中段：板簧压住","② Middle: under the leaf spring","中段压进板簧下面，让板簧压住料管。","The middle goes under the leaf spring, pressed down.","M Fig. 2-2 · NEW"),
  (6,"特写","CU","前端用定位块固定，剪掉吸取位的料管顶面","Front fixed by the locating piece; top face of the tube cut at the pick area","③ 前端：定位块 + 剪开顶面","③ Front: locating piece + cut the top face","前端用定位块固定，再把吸取位的料管顶面剪掉。","Front fixed by the locating piece, then cut the top face at the pick area.","M §5.1 · NEW"),
  (6,"中景","MS","开机，元件平稳前移到吸取位","Switch on: parts flow smoothly to the pick point","三点固定 = 吸取高度不漂","Three points = a pick height that holds","三点固定，吸取高度就不会漂。","Three fixed points. The pick height stays put.","YT clip"),
  OUTRO]))

V.append(dict(
 id="V06", zh="振动供料怎么调：频率、功率两只旋钮", en="Two dials that stop feeder jams", dur=45,
 cover="振动调节", type_zh="原理 + 调机", type_en="Mechanism + tuning",
 aud_zh="工艺工程师、设备技术员", aud_en="Process engineers and maintenance techs",
 hook_zh="画面：元件卡住不动 vs 元件乱跳，分屏；字幕「不动，还是乱跳？」",
 hook_en="Visual: split screen, stalled parts vs bouncing parts; text 'Stalling or bouncing?'",
 shots=[
  (3,"中景","MS","分屏：左元件停滞，右元件乱跳","Split screen: left stalled, right bouncing","不动，还是乱跳？","Stalling or bouncing?","供料卡住，只有两种情况：不动，或乱跳。","Every feeding jam is one of two: it stalls, or it bounces.","NEW 待拍"),
  (7,"特写","CU","3D 剖视：振动器 + 弹簧把振动传到导轨","3D cutaway: vibrator and springs passing vibration to the guide rail","振动器 → 弹簧 → 导轨 → 料管","Vibrator → springs → guide rail → stick","振动器加弹簧，把振动传给导轨和料管。零件表里没有皮带。","A vibrator and springs drive the rail and the stick. There's no belt in the parts list.","3D viewer / M Fig. 9-1"),
  (8,"特写","CU","转动功率旋钮：元件由慢变快","Turning the power dial: parts speed up","功率：太慢加，乱跳减","Power: up if slow, down if jumping","功率旋钮管力度：走得慢就加，乱跳就减。","The power dial sets strength. Too slow, turn it up. Jumping, turn it down.","M §5.2 · NEW"),
  (8,"特写","CU","转动频率旋钮，找到最顺的一点","Turning the frequency dial to the smoothest point","频率：找最顺的一点","Frequency: find the smoothest point","频率旋钮找最顺的那个点。","The frequency dial finds where parts move most smoothly.","M §5.2 · NEW"),
  (8,"近景","MCU","一次只动一只旋钮，观察几秒","One dial at a time, watch a few seconds","一次只调一只，看几秒再动","One dial at a time. Watch, then adjust.","一次只调一只，观察几秒再调下一步。","Adjust one dial at a time. Watch the flow for a few seconds.","M §5.2 TIP"),
  (8,"中景","MS","记录每个料号的旋钮位置卡片贴在飞达座旁","Dial-setting card per part number taped by the bank","每个料号记下旋钮位置","Log both dial positions per part number","把每个料号的两只旋钮位置记下来，下次换线直接调到位。","Log both dial positions per part number. Next changeover starts there.","P landing set-up tip · NEW"),
  OUTRO]))

V.append(dict(
 id="V07", zh="状态指示与检测：指示灯、开关和机器取件确认", en="Read the feeder's status from the aisle", dur=30,
 cover="指示灯与检测", type_zh="操作 + 故障判断", type_en="Status & checks",
 aud_zh="操作员、设备技术员", aud_en="Operators and maintenance techs",
 hook_zh="画面：一排飞达中一盏指示灯熄灭；字幕「灯不亮？两个原因」",
 hook_en="Visual: one pilot lamp off in a row of feeders; text 'Lamp off? Two causes.'",
 note_zh="说明书和产品资料均未记载独立的光电传感器。本片只讲已记载的指示灯/开关/连接器，不宣称光电检测。若 Jason 确认有料位光电传感器，再加一镜。",
 note_en="Neither the manual nor the product document lists a photoelectric sensor. This video only shows the documented lamp, switch and connector; no photoelectric claim.",
 shots=[
  (3,"中景","MS","飞达座一排，其中一台指示灯不亮","Row of feeders, one pilot lamp off","灯不亮？两个原因","Lamp off? Two causes.","指示灯不亮，只有两个原因。","Pilot lamp off? There are two causes.","NEW 待拍"),
  (6,"特写","CU","开关拨到 ON，灯亮","Switch flipped on, lamp lights","① 开关没开","① Switch is off","一，开关没开。打开就亮。","One: the switch is off. Turn it on.","M §8"),
  (6,"特写","CU","抬手柄、重新插入、松开锁定，灯亮","Raise handlebar, reseat, release to lock, lamp lights","② 没锁进飞达座","② Not locked in the bank","二，没锁到位。重新插入，松开手柄锁紧。","Two: not locked. Reseat it and release the handlebar.","M §8 / Fig. 4-5"),
  (6,"特写","CU","吸嘴在开口吸取位取件，取件确认由贴片机完成","Nozzle picks at the opened pick area; pick check is done by the mounter","剪开顶面，吸嘴才能取件","Cut the top face, or the nozzle can't pick","吸嘴取不到件？检查吸取位的料管顶面剪开没有。","Nozzle can't pick? Check the tube's top face is cut at the pick area.","M §8"),
  (6,"近景","MCU","连接器特写：电源与信号经飞达座接入","Connector close-up: power and signal via the bank","电源与通讯走飞达座连接器","Power and communication via the bank connector","电源和通讯都经飞达座连接器，锁紧即上电。","Power and communication come through the bank connector the moment it locks.","P landing · PH rear photo"),
  OUTRO]))

V.append(dict(
 id="V08", zh="电气与安全：24 V DC、接地、绝缘、急停", en="24 V DC, grounding, insulation, E-stop: what we test", dur=45,
 cover="电气与安全", type_zh="质量背书", type_en="Quality proof",
 aud_zh="设备经理、EHS 安全工程师", aud_en="Equipment managers and EHS engineers",
 hook_zh="画面：万用表表笔接触连接器，读数 24 V；字幕「24 V DC · 15 W」",
 hook_en="Visual: meter probes on the connector reading 24 V; text '24 V DC · 15 W'",
 note_zh="24 V DC / 15 W 来自产品资料；说明书注明未载电气参数，发布前请 Jason 确认。接地、绝缘、急停的数值为通用出厂验收方法（推测），口播不念具体阈值。",
 note_en="24 V DC / 15 W are from the product document; the manual itself says electrical ratings are not stated. Confirm before publishing. Ground/insulation/E-stop thresholds are generic FAT practice (assumed); VO does not quote them.",
 shots=[
  (3,"特写","CU","万用表测连接器供电，读数约 24 V","Meter on the connector supply reading about 24 V","24 V DC · 15 W","24 V DC · 15 W","S-JVF02 用 24 伏直流，功率 15 瓦。","The S-JVF02 runs on 24 volts DC, 15 watts.","NEW 待拍 · P spec"),
  (8,"特写","CU","接地电阻测试仪：机身金属件到连接器接地端","Bonding tester: feeder body to the connector ground pin","接地连续性","Ground continuity","出厂前测接地：机身到连接器接地端，必须导通。","Before shipping we test ground continuity, body to connector ground.","NEW 待拍"),
  (8,"特写","CU","兆欧表测 24 V 回路对机身绝缘","Insulation tester: 24 V circuit to frame","绝缘电阻","Insulation resistance","再测绝缘：24 伏回路对机身。","Then insulation, from the 24 volt circuit to the frame.","NEW 待拍"),
  (8,"中景","MS","贴片机急停按下，飞达振动停止","Machine E-stop pressed; feeder vibration stops","急停 → 振动停止","E-stop → vibration stops","装上贴片机按急停，确认飞达振动随之停止。","On the machine, we press E-stop and check the vibration stops.","NEW 待拍 (on RS-1)"),
  (7,"特写","CU","关开关后再拔出飞达","Switch off before pulling the feeder","先关开关，再拔飞达或换管","Switch off before removing or changing sticks","拔飞达、换料管之前，先关开关。","Switch off before removing the feeder or changing a stick.","M §1 Safety"),
  (8,"近景","MCU","吸取区运行中，手远离（警示图标）","Pick area running; hands clear (warning icon)","运行时手远离吸取区","Hands clear of the pick area while running","运行时，手远离吸嘴取件区。","Keep hands clear of the pick area while the machine runs.","M §1 Safety"),
  OUTRO]))

V.append(dict(
 id="V09", zh="规格参数核对：型号、电压、频率、适用元件", en="Spec check before you order: model, voltage, frequency, parts", dur=30,
 cover="参数核对", type_zh="参数清单（上屏为主）", type_en="Spec checklist",
 aud_zh="采购、设备工程师", aud_en="Buyers and equipment engineers",
 hook_zh="画面：铭牌特写；字幕「下单前核对这 5 项」",
 hook_en="Visual: nameplate close-up; text 'Check these 5 before you order.'",
 note_zh="「频率」：供电为 24 V DC，无工频 Hz 要求；振动频率可调，但资料未给出 Hz 范围，不上屏数字。",
 note_en="'Frequency': supply is 24 V DC, so there is no mains-frequency rating; vibration frequency is adjustable but no Hz range is published, so no number on screen.",
 shots=[
  (3,"特写","CU","飞达铭牌特写","Feeder nameplate close-up","下单前核对这 5 项","Check these 5 before you order.","下单前，核对这五项。","Before you order, check these five.","NEW 待拍 nameplate"),
  (5,"中景","MS","飞达插在 RS-1 飞达座上","Feeder in an RS-1 bank","① 型号：S-JVF02 · JUKI RS-1","① Model: S-JVF02 · JUKI RS-1","一，型号 S-JVF02，用于 JUKI RS-1 飞达座。","One: model S-JVF02, for the JUKI RS-1 feeder bank.","YT clip"),
  (5,"特写","CU","连接器 + 电压大字","Connector + voltage in large text","② 电压：24 V DC · 15 W","② Voltage: 24 V DC · 15 W","二，电压 24 伏直流，15 瓦。","Two: 24 volts DC, 15 watts.","P spec"),
  (5,"特写","CU","频率旋钮转动","Frequency dial turning","③ 频率：直流供电 · 振动频率可调","③ Frequency: DC supply · vibration frequency adjustable","三，频率：直流供电不涉及工频，振动频率旋钮可调。","Three: frequency. DC supply, and the vibration frequency is adjustable.","M §5.2"),
  (5,"中景","MS","卡尺量元件 + 料管宽度","Caliper on a part + stick width","④ 元件 3×3 – 30×10 mm · ⑤ 料管 66 mm","④ Parts 3×3 – 30×10 mm · ⑤ 66 mm sticks","四，元件 3×3 到 30×10 毫米。五，料管宽 66 毫米。","Four: parts 3 by 3 to 30 by 10 millimetres. Five: 66 millimetre sticks.","P spec · NEW caliper"),
  (4,"中景","MS","四项参数汇总卡","Summary card of the specs","超出范围？可做定制料道","Outside the window? Custom lanes available","超出范围的元件，可以做定制料道。","Outside the window? We design custom lanes.","P options"),
  OUTRO]))

V.append(dict(
 id="V10", zh="出厂验收 60 秒：一台飞达出货前要过的关", en="60 seconds of factory acceptance on one feeder", dur=60,
 cover="出厂验收", type_zh="工厂实拍（汇总）", type_en="Factory acceptance walk-through",
 aud_zh="SQE、采购、海外经销商", aud_en="SQEs, buyers and overseas distributors",
 hook_zh="画面：检验员撕下验收表，飞达入箱；字幕「出货前，它过了这些关」",
 hook_en="Visual: feeder going into its box with the signed sheet; text 'Before it ships, it passes all this.'",
 shots=[
  (3,"中景","MS","飞达连同签好的验收表装箱","Feeder boxed with the signed acceptance sheet","出货前，它过了这些关","Before it ships, it passes all this.","出货之前，每台 S-JVF02 都要过这些关。","Before it ships, every S-JVF02 passes these checks.","NEW 待拍"),
  (7,"中景","MS","外观与尺寸：卡尺量 66 mm 宽度，称重","Appearance and size: caliper on the 66 mm width, weighing","外观 · 尺寸 · 重量","Appearance · Size · Weight","先看外观，量宽度和外形尺寸，称重。","First, appearance, the 66 millimetre width, overall size and weight.","NEW 待拍 · P spec"),
  (8,"特写","CU","14 个零件对照零件表、螺丝防松标记","14 parts against the parts list; screw paint marks","14 项零件 · 紧固","14 parts · Fastening","对照零件表核 14 个零件，螺丝紧固加防松标记。","Fourteen parts against the list. Every screw torqued and marked.","M Fig. 9-1 · NEW"),
  (8,"特写","CU","测试座上手柄四步装拆三次","Handlebar install/remove on a test bank, three times","手柄锁紧 · 装拆顺畅","Handlebar lock · smooth in and out","在测试飞达座上反复装拆，手柄锁得住、拔得出。","On a test bank, in and out repeatedly. It locks and it releases.","NEW 待拍"),
  (8,"特写","CU","万用表、接地、绝缘测试","Meter, ground and insulation tests","24 V DC · 接地 · 绝缘","24 V DC · Ground · Insulation","电气：24 伏供电、接地导通、绝缘。","Electrical: 24 volt supply, ground continuity, insulation.","NEW 待拍"),
  (8,"中景","MS","两只旋钮全行程转动，指示灯、开关测试","Both dials through full travel; lamp and switch test","旋钮全行程 · 指示灯 · 开关","Dials full travel · Lamp · Switch","两只旋钮全行程，指示灯和开关逐一确认。","Both dials through full travel. Lamp and switch, one by one.","NEW 待拍"),
  (10,"中景","MS","四条料道装样品料管连续振动运行","All four lanes with sample sticks, continuous run","4 道连续供料试运行","4-lane continuous feeding run","四条料道装上样品料管，连续供料，看有没有卡料和异响。","Four lanes loaded with sample sticks. Continuous run, no stalls, no rattle.","NEW 待拍 / YT clip"),
  (5,"近景","MCU","检验员签字（只拍手）","Inspector signs (hands only)","逐项签字 · 才能出货","Signed line by line, then shipped","逐项签字，才能出货。","Signed line by line. Only then does it ship.","NEW 待拍"),
  OUTRO]))

# Platform copy: (yt_title, yt_title_zh, yt_desc, li_post, li_post_zh, tt_caption, seo, tags)
PLAT = {
"V01": dict(
 yt="S-JVF02 Stick Feeder for JUKI RS-1: Anatomy in 30s #Shorts",
 yt_zh="S-JVF02 料管飞达（JUKI RS-1 用）：30 秒看懂结构",
 desc="Main body, guide rail, support frame, a two-dial control unit and a tool-less handlebar lock: the S-JVF02 vibration stick feeder for the JUKI RS-1 feeder bank, 365 × 66 × 125 mm, 6.5 kg.",
 li="Stick-packed parts can feed like tape.\n\nThe S-JVF02 vibration stick feeder sits in the JUKI RS-1 feeder bank next to your tape feeders. One control unit (power dial, frequency dial, pilot lamp, switch), a guide rail and support frame for the sticks, and a handlebar that locks it in without tools.\n\nWhich stick-packed parts still go through a hand-picking bench on your line?",
 li_zh="料管元件，也能像编带一样供料。\n\nS-JVF02 振动料管飞达装在 JUKI RS-1 飞达座上，和编带飞达并排。一个控制单元（功率旋钮、频率旋钮、指示灯、开关），导轨和支撑架承载料管，手柄免工具锁紧。\n\n您的产线上，还有哪些料管元件在靠手工挑料？",
 tt="Stick parts, fed like tape 👀 S-JVF02 for JUKI RS-1",
 seo=["JUKI RS-1 vibration stick feeder","stick feeder","tube feeder","SMT feeder","pick and place feeder"],
 tags=["#SMT","#SMTFeeder","#StickFeeder","#JUKI","#RS1","#PCBAssembly","#ElectronicsManufacturing"]),
"V02": dict(
 yt="Hand-picking tube parts? Feed them with 4 vibration lanes #Shorts",
 yt_zh="还在手工挑料管元件？用 4 条振动料道自动供料",
 desc="Tube-packaged resistors, diodes and connectors are often hand-picked beside the mounter. The S-JVF02 runs 4 independent lanes for parts 3×3 – 30×10 mm on 66 mm sticks, for the JUKI RS-1.",
 li="The bottleneck on many high-mix lines isn't the mounter. It's the small table beside it, where someone picks tube-packed parts by hand.\n\nA five-minute audit: take your three highest-volume stick parts, time one hand pick, count them for one shift. That number prices the bench.\n\nThe S-JVF02 runs four independent lanes on the JUKI RS-1: four part numbers, or four sticks of one high-runner. Parts 3×3 to 30×10 mm, 66 mm sticks.",
 li_zh="很多高混线的瓶颈不在贴片机，而在旁边那张手工挑料桌。\n\n五分钟自查：取用量最大的三个料管元件，计时一次手工取放，统计一个班次的数量。这个数字就是这张桌子的成本。\n\nS-JVF02 在 JUKI RS-1 上有四条独立料道：四个料号，或一个高用量料号的四根料管。元件 3×3 到 30×10 mm，料管宽 66 mm。",
 tt="Your bottleneck isn't the mounter. It's this bench 😬",
 seo=["stick feeder for JUKI","tube component feeding","automate tube packaged components","vibration feeder SMT","high mix SMT line"],
 tags=["#SMT","#LeanManufacturing","#EMS","#StickFeeder","#JUKI","#Automation","#PCBA"]),
"V03": dict(
 yt="Install a JUKI RS-1 stick feeder in 4 moves, no tools #Shorts",
 yt_zh="4 步免工具装上 JUKI RS-1 料管飞达",
 desc="Raise the handlebar, align the alignment hole, align the connector, release to lock. Installation steps from the S-JVF02 operation manual.",
 li="Four moves, no tools: raise the handlebar, align the alignment hole, align the connector, release to lock. That's the whole S-JVF02 install on a JUKI RS-1 bank, straight from the manual.",
 li_zh="四步，免工具：抬起手柄、对准定位孔、对准连接器、松开锁紧。这就是 S-JVF02 装上 JUKI RS-1 飞达座的全部步骤，摘自说明书。",
 tt="4 moves. No tools. ✅ #JUKI RS-1 stick feeder",
 seo=["how to install JUKI RS-1 feeder","stick feeder installation","RS-1 feeder bank","SMT feeder setup"],
 tags=["#SMT","#HowTo","#JUKI","#RS1","#Feeder","#Maintenance","#SMTTips"]),
"V04": dict(
 yt="How we assemble and torque-check a stick feeder #Shorts",
 yt_zh="料管飞达的装配与螺丝紧固检查",
 desc="14 numbered parts, torque-checked screws with paint marks, a hand check of handlebar, locating pin and rail, and a listen-test under vibration before every S-JVF02 ships.",
 li="A vibration feeder shakes itself all day. That's why loose screws are the first thing we look for.\n\nEvery S-JVF02 is built from 14 numbered parts. Before shipping: torque check and paint mark on each screw, hand check of handlebar return, locating pin and guide rail, then a run with the ear close to it. A loose screw shows up as noise first.",
 li_zh="振动飞达整天都在自己振动，所以螺丝松动是我们第一个查的。\n\n每台 S-JVF02 由 14 个编号零件组成。出货前：每颗螺丝扭力检查并画防松标记，手检手柄回弹、定位销和导轨，再通电振动贴近听。螺丝松了，会先在声音里暴露。",
 tt="Every screw. Before it ships. 🔧",
 seo=["SMT feeder assembly","feeder quality inspection","vibration feeder maintenance","stick feeder spare parts"],
 tags=["#Manufacturing","#QualityControl","#SMT","#Feeder","#FactoryTour","#Engineering"]),
"V05": dict(
 yt="Stick feeder mis-picks? Check these 3 points #Shorts",
 yt_zh="料管飞达吸不到件？先查这三个点",
 desc="Locating ring at the rear, leaf spring in the middle, locating piece at the front, and the tube's top face cut at the pick area. Set-up steps from the S-JVF02 manual.",
 li="Most stick-feeder mis-picks come from the tube, not the machine.\n\nThe S-JVF02 fixes each tube at three points: locating ring at the rear on the support frame, leaf spring pressing the middle, locating piece at the front. Then the top face is cut at the pick area. Three fixed points keep the pick height where the nozzle expects it.",
 li_zh="料管飞达吸不到件，多半是料管的问题，不是机器。\n\nS-JVF02 用三个点固定料管：尾端在支撑架上用定位环，中段由板簧压住，前端用定位块。再把吸取位的料管顶面剪开。三点固定，吸取高度才稳定在吸嘴预期的位置。",
 tt="Mis-picks? It's usually the tube 👇",
 seo=["stick feeder mispick","tube feeder setup","leaf spring feeder","SMT pick up error"],
 tags=["#SMT","#Troubleshooting","#SMTTips","#Feeder","#JUKI","#ProcessEngineering"]),
"V06": dict(
 yt="Vibration feeder jams: tune power and frequency like this #Shorts",
 yt_zh="振动飞达卡料：这样调功率和频率",
 desc="Too slow: more power. Jumping: less power. Frequency: find the smoothest point. One dial at a time. Vibration is driven by a vibrator and springs; there is no belt in the S-JVF02 parts list.",
 li="Every vibration-feeding jam is one of two sentences: the part stopped, or the part moved too much.\n\nOn the S-JVF02 the fix is two dials. Power sets the strength: up if parts crawl, down if they jump. Frequency finds the point where they move most smoothly. One dial at a time, watch a few seconds, then log both positions per part number so the next changeover starts from a known setting.",
 li_zh="振动供料卡料只有两种：元件不动，或者动得太厉害。\n\nS-JVF02 用两只旋钮解决。功率管力度：走得慢就加，乱跳就减。频率找元件走得最顺的那一点。一次只调一只，看几秒，再把每个料号的两只旋钮位置记下来，下次换线直接从已知设定开始。",
 tt="Stalling or bouncing? Two dials fix both 🎛️",
 seo=["vibration feeder adjustment","stick feeder jam","feeder frequency power setting","SMT vibration feeder"],
 tags=["#SMT","#SMTTips","#Feeder","#Troubleshooting","#Manufacturing","#JUKI"]),
"V07": dict(
 yt="Feeder pilot lamp off? Two causes, 30-second fix #Shorts",
 yt_zh="飞达指示灯不亮？两个原因，30 秒排查",
 desc="Switch off, or not locked in the bank. Plus: if the nozzle can't pick, check the tube's top face is cut. From the S-JVF02 troubleshooting table.",
 li="Pilot lamp off on a stick feeder? The S-JVF02 manual lists two causes: the switch is off, or the feeder isn't locked in the bank. Reseat it and release the handlebar.\n\nNozzle can't pick? Check the tube's top face is cut at the pick area. Power and communication come through the bank connector the moment it locks.",
 li_zh="料管飞达指示灯不亮？S-JVF02 说明书列了两个原因：开关没开，或者没锁进飞达座。重新插入，松开手柄锁紧。\n\n吸嘴取不到件？检查吸取位的料管顶面剪开没有。电源和通讯都经飞达座连接器，锁紧即上电。",
 tt="Lamp off? It's one of these two 💡",
 seo=["SMT feeder not working","feeder pilot lamp","stick feeder troubleshooting","JUKI feeder error"],
 tags=["#SMT","#Troubleshooting","#Maintenance","#Feeder","#JUKI","#SMTTips"]),
"V08": dict(
 yt="24 V DC stick feeder: ground, insulation and E-stop checks #Shorts",
 yt_zh="24 V DC 料管飞达：接地、绝缘、急停检查",
 desc="The S-JVF02 runs on 24 V DC, 15 W. Before shipping: supply voltage, ground continuity, insulation resistance, and vibration stopping on machine E-stop. Safety rules from the operation manual.",
 li="A small feeder still gets a full electrical check.\n\nThe S-JVF02 runs on 24 V DC, 15 W. Before it ships we check the supply at the connector, ground continuity from body to connector, insulation of the 24 V circuit to the frame, and that vibration stops when the machine's E-stop is pressed. On the line: switch off before removing the feeder or changing a stick, and keep hands clear of the pick area.",
 li_zh="小飞达也要过完整的电气检查。\n\nS-JVF02 使用 24 V DC，15 W。出货前我们检查连接器供电、机身到连接器的接地导通、24 V 回路对机身的绝缘，以及按下贴片机急停后振动是否停止。产线上：拔飞达或换料管前先关开关，运行时手远离吸取区。",
 tt="Small feeder. Full electrical check ⚡",
 seo=["SMT feeder electrical safety","24V DC feeder","equipment grounding test","insulation resistance test"],
 tags=["#SMT","#ElectricalSafety","#QualityControl","#Feeder","#Manufacturing","#EHS"]),
"V09": dict(
 yt="Before you order a JUKI RS-1 stick feeder, check these 5 #Shorts",
 yt_zh="订购 JUKI RS-1 料管飞达前，核对这 5 项",
 desc="Model S-JVF02 for the JUKI RS-1 bank · 24 V DC, 15 W · DC supply, adjustable vibration frequency · parts 3×3 – 30×10 mm · 66 mm sticks. Outside the window? Custom lanes.",
 li="Five checks before you order a stick feeder for a JUKI RS-1:\n1. Model: S-JVF02, for the RS-1 feeder bank\n2. Voltage: 24 V DC, 15 W\n3. Frequency: DC supply; vibration frequency adjustable on the control unit\n4. Parts: 3×3 to 30×10 mm\n5. Sticks: 66 mm wide\n\nParts outside the window go to custom lane design.",
 li_zh="订购 JUKI RS-1 料管飞达前，核对五项：\n1. 型号：S-JVF02，用于 RS-1 飞达座\n2. 电压：24 V DC，15 W\n3. 频率：直流供电；振动频率可在控制单元上调\n4. 元件：3×3 到 30×10 mm\n5. 料管：宽 66 mm\n\n超出范围的元件，可做定制料道。",
 tt="5 specs to check before you buy ✅",
 seo=["JUKI RS-1 stick feeder specifications","S-JVF02","stick feeder 66mm","tube feeder component size"],
 tags=["#SMT","#Procurement","#JUKI","#RS1","#StickFeeder","#SMTFeeder"]),
"V10": dict(
 yt="60 seconds of factory acceptance on one SMT stick feeder",
 yt_zh="60 秒看一台 SMT 料管飞达的出厂验收",
 desc="Appearance, size and weight, 14 parts and fastening, handlebar lock, 24 V DC electrical checks, dials, lamp and switch, then a 4-lane continuous feeding run. Signed line by line before shipping.",
 li="What does a stick feeder go through before it ships?\n\nAt Southern Machinery each S-JVF02 is checked line by line: appearance, 66 mm width, size and weight; 14 parts and screw fastening; handlebar lock in and out on a test bank; 24 V DC supply, ground and insulation; both dials, lamp and switch; then a continuous run on all four lanes with sample sticks. Signed, then boxed.",
 li_zh="一台料管飞达出货前要过哪些关？\n\n在 Southern Machinery，每台 S-JVF02 逐项检查：外观、66 mm 宽度、尺寸和重量；14 个零件与螺丝紧固；在测试飞达座上反复装拆手柄锁紧；24 V DC 供电、接地、绝缘；两只旋钮、指示灯和开关；最后四条料道装样品料管连续运行。签字后才装箱。",
 tt="Before it ships, it passes all this 📋",
 seo=["SMT feeder factory acceptance test","FAT checklist SMT","feeder quality inspection","stick feeder supplier China"],
 tags=["#SMT","#QualityControl","#FactoryAcceptance","#Manufacturing","#Feeder","#MadeInShenzhen"]),
}
