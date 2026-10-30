---
name: smt-machine-marketing-image-prompts
description: Southern Machinery SMT/THT/波峰焊设备营销图片生成专用 Prompt — 基于 EvoLinkAI/awesome-gpt-image-2-prompts 规范结构，结合 Southern Machinery 全产品线参数。用于生成：产品主图、E-commerce详情页、展会海报、社交媒体Banner、工厂场景图、整线信息图。
triggers:
  - "生成SMT设备营销图"
  - "THT插件机产品图"
  - "波峰焊设备广告图"
  - "SMT产品主图"
  - "Southern Machinery营销素材"
  - "S-70LD S-7900产品图片"
  - "SMThelp广告图"
  - "SMT整线信息图"
  - "工厂场景营销图"
---

# SMT Machine Marketing Image Prompts
# Southern Machinery 专用 / For Southern Machinery Only

> **基于**: EvoLinkAI/awesome-gpt-image-2-prompts prompt patterns
> **产品线覆盖**: S-70LD / S-7900 / S-7020T / S-WS450 / SUL460 / SFY03 / SMT整线
> **适用场景**: 产品主图 / E-commerce详情页 / 展会海报 / LinkedIn Banner / 工厂场景 / 整线信息图

---

## 核心结构说明

每个 Prompt 遵循以下层级：

```
1. Core Subject       → 主体：机器外观、主体视角
2. Layout & Composition → 构图：多图格/单图/信息图布局
3. Scene Elements     → 场景元素：环境、背景、道具
4. Color Palette      → 色调：品牌色+产品色
5. Lighting           → 光影：戏剧光/工作室光/自然光
6. Text Treatment     → 文字处理：标签、型号、技术参数
7. Quality Tags       → 质量标签：4K、超写实、商业级
```

---

## 🚀 Prompt #1: S-70LD 异形插件机 — 产品主图

**场景**: 电商平台产品主图 / 展会单产品海报

```
{"type":"industrial equipment product photography","product":{"brand":"Southern Machinery","model":"S-70LD","category":"odd-form insertion machine (THT auto-placement)","function":"automated insertion of 3-25mm odd-form components: relays, terminals, connectors","key_specs":{"component_range":"3-25mm","feeder":"STF1003 tube feeder (0.8s feed cycle, ±0.5mm accuracy)","spring_lifespan":"4 million cycles","drive":"stepper motor 57-type (max 600 rpm)","power":"24V, avg/peak 4A/6A","air_pressure":"0.4-0.6 MPa"},"visual_identity":{"body_color":"industrial orange and dark gray metal chassis","control_panel":"7-inch touchscreen HMI on upper right","feeder_zone":"tube feeder mounted on left side","insertion_head":"centered high-precision head with camera vision","brand_label":"Southern Machinery logo + S-70LD model text on body","color_scheme":["industrial orange #FF6B00","dark gray #2D2D2D","matte black #1A1A1A","accent gold #C0A060"]}},"style":{"overall":"premium industrial equipment catalog photography","mood":"powerful, precise, reliable, professional manufacturing","lighting":"dramatic three-point studio lighting with orange rim light, cool fill light, dark background gradient","camera_angle":"three-quarter front view angled from lower-left toward upper-right, slight tilt showing insertion head and feeder","depth_of_field":"shallow focus on machine front, softer background with subtle depth","background":"dark charcoal seamless studio backdrop with subtle hexagonal grid pattern","environment":"clean SMT factory floor suggestion, no clutter, no workers"}},"scene_elements":{"machine":{"body":"S-70LD odd-form inserter in full view, industrial orange chassis with dark metal panels, visible insertion head at center, STF1003 tube feeder on left, 7-inch color touchscreen HMI on upper right","details":["brand text 'S-70LD' on front panel in bold white","brand text 'Southern Machinery' in smaller font below","model number sticker near control panel","LED status indicators green/amber on panel","visible vision camera above insertion zone","steel frame base with level adjustment feet"]},"supporting_elements":["clean dark reflective studio floor surface","floating material specification labels nearby","no human figures, no cables, no debris"]},"text_treatment":{"model_label":"S-70LD — Odd-Form Inserter","brand_label":"Southern Machinery","spec_lines":["Component: 3-25mm | Feeder: STF1003 | Accuracy: ±0.5mm | Feed: 0.8s"],"tagline_font":"bold condensed sans-serif in white/gold","accent":"thin orange divider line above tagline"},"aspect_ratio":"4:5 (portrait e-commerce key visual)","quality":"ultra-detailed commercial product photography, crisp focus across machine, realistic metal reflections, premium industrial aesthetic, 4K, no watermark"
```

---

## 🚀 Prompt #2: S-7900 4头AI视觉插件机 — 旗舰产品信息图

**场景**: E-commerce详情页 / 产品对比页 / LinkedIn帖子图

```
{"type":"e-commerce product marketing board","product":{"brand":"Southern Machinery","model":"S-7900","category":"high-speed odd-form insertion machine with AI vision","function":"automated insertion of 3-25mm components with Active Clinching for automotive-grade reliability","key_specs":{"heads":"4 insertion heads (quad-head)","speed":"4,000 CPH","accuracy":"±0.05mm","insertion_force":"98N","vision":"AI artificial intelligence vision correction system","technology":"Active Clinching (mechanical lead clinching before solder fillet)","highlight":"automotive-grade joint reliability, IPC-610 compliant"},"visual_identity":{"body_color":"matte black chassis with carbon fiber texture panels","accent_color":"electric cyan blue LED strips on edges and head mounts","control_panel":"15-inch industrial touchscreen HMI, graphical UI showing real-time CPH","brand_label":"Southern Machinery logo + S-7900 in chrome silver on black","color_scheme":["matte black #111111","carbon gray #2A2A2A","electric cyan #00D4FF","chrome silver #C0C0C0","warning amber #FF9500"]}},"style":{"overall":"premium tech product marketing composite board","mood":"intelligent, high-precision, future-forward, automotive-grade reliability","lighting":"dramatic dark studio lighting, cyan accent rim lights, high-contrast key light from upper left","camera_angle":"hero shot: front three-quarter view from lower left showing all 4 heads, exploded annotation callouts","background":"dark studio void with subtle circuit board trace pattern in background, blue glow emanating from machine base"},"layout":{"format":"tall composite board (portrait 9:16) divided into 6 sections","sections":[{"title":"Hero Product Shot","position":"top-left","count":1,"labels":["S-7900 front three-quarter view","4-head insertion system visible","AI vision camera above heads","cyan LED accent strips glowing"]},{"title":"Active Clinching Technology","position":"top-right","count":2,"labels":["Active Clinching: leads mechanically clinched during insertion","Secondary mechanical interlock + solder fillet = dual protection","Automotive-grade thermal cycling reliability"]},{"title":"AI Vision System","position":"mid-left","count":2,"labels":["AI vision correction for each component"," ±0.05mm placement accuracy","Real-time error detection and correction"]},{"title":"Key Specifications","position":"mid-right","count":4,"labels":["4 Heads | 4,000 CPH | ±0.05mm | 98N","Active Clinching Technology","15-inch HMI Touchscreen","CE Certified"]},{"title":"Application Scenarios","position":"lower-left","count":3,"labels":["Automotive BCM & ECU modules","Power Battery Management System (BMS)","Industrial control boards with relays & connectors"]},{"title":"vs. Japanese Equipment","position":"lower-right","count":3,"labels":["CapEx 30-50% lower than Fuji/Yamaha","14-month average payback period","37% OEE improvement at customer site"]}]},"text_treatment":{"headline_font":"bold tech display type in electric cyan","model_font":"chrome silver bold on matte black","spec_font":"clean monospaced type for numbers, sans-serif for labels","accent":"cyan thin divider lines, blueprint-style annotation arrows"},"camera_and_composition":{"hero_shot":"three-quarter front view from lower left, dramatic low-angle emphasizing power","annotation_shots":"close-up macro of insertion head, AI camera module, clinching mechanism detail","aspect_ratio":"portrait 9:16"},"quality":"ultra-detailed commercial product infographic, blueprint-style annotations, premium automotive tech aesthetic, 4K"
```

---

## 🚀 Prompt #3: S-WS450 波峰焊机 — 产品主图

**场景**: 设备电商主图 / 展会设备展示

```
{"type":"industrial equipment product photography","product":{"brand":"Southern Machinery","model":"S-WS450","category":"wave soldering machine (dual-wave lead-free)","function":"DIP production line wave soldering for PCB assemblies, ideal for power supply and communication boards","key_specs":{"pcb_width":"450mm","preheat_temp":"up to 280°C","solder_temp":"up to 300°C","solder_pot":"460KG large capacity lead-free solder bath","wave_system":"dual-wave system (first turbulent wave + second smooth laminar wave)","process":"lead-free compatible (SAC305 standard)","energy_feature":"4-zone preheat with independent temperature control"},"visual_identity":{"body_color":"industrial blue-gray steel chassis with orange safety trim","panel_color":"light gray control cabinet with large touchscreen HMI","brand_label":"Southern Machinery logo + S-WS450 on front panel in white on orange","color_scheme":["industrial blue-gray #4A5568","safety orange #FF6B00","dark steel #1E2024","HMI green #00C853","solder silver #B0BEC5"]}},"style":{"overall":"industrial equipment catalog photography","mood":"powerful, high-temperature precision, robust manufacturing","lighting":"dramatic workshop lighting with orange rim highlights, showing solder wave in subtle warm glow","camera_angle":"front view with slight elevation (15°) showing conveyor entry, solder bath area, and control panel","depth_of_field":"medium depth, sharp on machine front and solder zone, softer on background","background":"dark workshop backdrop with subtle heat shimmer effect near solder zone"},"scene_elements":{"machine":{"full_view":"S-WS450 wave solderer in full front view, industrial blue-gray chassis, visible conveyor belt entry at bottom, solder bath chamber in center, preheat zone at top, control cabinet on right side","details":["brand 'Southern Machinery' on front header panel","model 'S-WS450' in bold white on orange stripe","large 10-inch touchscreen HMI showing temperature curves","visible solder wave when chamber door is slightly open","orange safety handrails along conveyor entry","stainless steel solder bath with shiny surface","flux spray nozzle visible above preheat zone","nitrogen inlet pipe (optional nitrogen protection)"]},"supporting_elements":["golden solder wave shimmer effect","dark workshop floor with oil stain texture","floating spec labels for temperature zones","no workers in shot"]},"text_treatment":{"model_label":"S-WS450 — Dual-Wave Soldering System","brand_label":"Southern Machinery | CE Certified","spec_lines":["PCB Width: 450mm | Solder Temp: 300°C Max | Bath: 460KG | Lead-Free"],"tagline":"Dual Wave. Zero Compromises.","tagline_font":"bold condensed white on dark panel","accent":"orange horizontal stripe across top of frame"},"aspect_ratio":"4:3 (e-commerce product gallery) or 16:9 (exhibition banner)","quality":"ultra-detailed industrial product photography, realistic solder wave glow, premium manufacturing equipment aesthetic, 4K, no watermark"
```

---

## 🚀 Prompt #4: SMT整线鸟瞰图 — 信息图

**场景**: 公司官网首页大图 / LinkedIn封面 / 展会主视觉背景

```
{"type":"full production line infographic visualization","product":{"brand":"Southern Machinery","line_type":"SMT+THT full automation line (complete turnkey solution)","line_config":{"stage_1":"SMT Placement Line","stage_2":"THT Insertion Line","stage_3":"Wave Soldering","stage_4":"PCB Handling & AGV Circulation"},"included_machines":[{"name":"Auto Loader (上板机)","model":"S-UL350","function":"PCB auto loading from magazine to line"},{"name":"Solder Paste Printer (锡膏印刷机)","function":"precision solder paste deposition"},{"name":"High-Speed Pick & Place (高速贴片机)","speed":"25,000-35,000 CPH","function":"SMT component placement"},{"name":"Reflow Oven (回流焊)","function":"SMT solder reflow process"},{"name":"AOI Inspection (AOI光学检测)","function":"automated optical inspection post-reflow"},{"name":"S-70LD Odd-Form Inserter (异形插件机)","function":"THT component insertion for non-standard parts"},{"name":"S-WS450 Wave Soldering Machine (波峰焊机)","function":"DIP through-hole soldering"},{"name":"SUL460 Auto Unloader (自动下板机)","function":"PCB unloading to magazine with ±30s changeover"},{"name":"SFY03 Magnetic AGV (磁导航AGV)","function":"magazines/materials automated transport between stations"}],"visual_identity":{"brand_color":"Southern Machinery orange #FF6B00","tech_color":"dark industrial blue-gray #2D3748","data_color":"electric cyan #00D4FF for data flows","bg_color":"very dark charcoal #0D0D0D to black gradient"},"style":{"overall":"futuristic smart factory visualization with blueprint/circuit aesthetic","mood":"automated, intelligent, seamless, Industry 4.0","lighting":"dramatic overhead factory lighting, blue-cyan data flow lines glowing between machines","camera_angle":"aerial top-down view (45° bird's eye) showing full line from left to right","depth_of_field":"full depth of field, all machines in sharp focus","background":"dark factory floor with subtle hex grid pattern, glowing cyan conveyor flow lines connecting machines"},"layout":{"format":"wide panoramic infographic board (16:9)","sections":[{"title":"SMT Zone","position":"far left","count":4,"machines":["Auto Loader","Solder Paste Printer","Pick & Place","Reflow Oven"]},{"title":"AOI Zone","position":"left-center","count":1,"machines":["AOI Inspection System"]},{"title":"THT Zone","position":"center","count":2,"machines":["S-70LD Odd-Form Inserter","S-7020T Terminal Inserter"]},{"title":"Wave Soldering","position":"right-center","count":1,"machines":["S-WS450 Wave Soldering Machine"]},{"title":"PCB Handling","position":"far right","count":2,"machines":["SUL460 Auto Unloader","SFY03 AGV circulating"]}],"flow_indicators":["cyan glowing arrows showing PCB flow direction","dashed lines showing AGV circulation routes","color-coded zone backgrounds (orange=SMT, blue=THT, amber=Wave, green=PCB Handling)"]},"scene_elements":{"factory_floor":{"machines":"all 9 machines shown in clean isometric top-down silhouette with key identifying features","conveyor":"glowing cyan conveyor belts connecting machines in sequence","AGV":"SFY03 AGV shown as small vehicle with magnetic track line circulating between SUL460 and loader","data_flow":"faint digital data particles flowing along conveyor direction","environment":"dark factory floor, clean and organized, no workers visible, ceiling-mounted overhead lights"}],"supporting_elements":["legend box bottom-left showing line capacity and CapEx savings vs. Japanese equipment","stats_panel":["Line Speed: up to 35,000 CPH (SMT)","Footprint: ~25m linear","CapEx Savings: 30-50% vs Fuji/Yamaha","CE Certified | 4-8 Week Delivery"]},"text_treatment":{"title":"FULL SMT+THT AUTOMATION LINE","title_font":"bold condensed white/orange on dark background","subtitle":"From Loader to Unloader — One Partner, One Solution","subtitle_font":"clean sans-serif in electric cyan","machine_labels":"clean white text below each machine block","stats_font":"monospaced bold numbers in cyan/orange","accent":"glowing orange divider line under title"},"aspect_ratio":"16:9 (presentation, website hero, LinkedIn cover)","quality":"ultra-detailed industrial infographic, blueprint-style schematic, futuristic smart factory aesthetic, 4K, no watermark"
```

---

## 🚀 Prompt #5: SUL460 自动下板机 + SFY03 AGV — 协同工作场景图

**场景**: 产品详情页场景图 / 展会 Booth 背景 / 社交媒体

```
{"type":"industrial equipment lifestyle scene photography","product":{"brand":"Southern Machinery","models":["SUL460 Auto Unloader","SFY03 Magnetic AGV"],"category":"PCB handling and automated material transport system","functions":{"SUL460":"automatic PCB unloading to magazine, ±30s magazine changeover, 10-40mm step pitch, integrates with SFY03 AGV for ±5mm precise docking","SFY03":"magnetic navigation AGV, 50KG load capacity, 6-8hr battery life, rapid swap battery design, single-point laser obstacle detection, 0.7M/S speed"},"visual_identity":{"SUL460_color":"industrial yellow #FFD600 and dark gray #2D2D2D","SFY03_color":"safety orange #FF6B00 and black #111111","brand_label":"Southern Machinery logos on both machines","color_scheme":["industrial yellow #FFD600","safety orange #FF6B00","dark gray #2D2D2D","cyan data lights #00D4FF"]}},"style":{"overall":"clean factory floor lifestyle shot with equipment in operational context","mood":"automated, smooth, efficient, modern manufacturing","lighting":"bright factory ambient light from above (overhead metal halide), slight lens flare from ceiling lights, realistic workshop atmosphere","camera_angle":"eye-level side view showing SUL460 and SFY03 in working alignment, slight low angle to emphasize scale","depth_of_field":"medium-shallow, SUL460 and AGV in sharp focus, softer background showing factory environment","background":"modern clean SMT factory floor, organized cable management, ceiling-mounted overhead lights, no clutter, no workers in shot"},"scene_elements":{"equipment":{"SUL460_auto_unloader":"industrial yellow and dark gray auto unloader in side view, visible magazine clamp mechanism, LED status panel, SUL460 label on body","SFY03_AGV":"compact safety orange AGV vehicle docked precisely beneath SUL460 output conveyor, visible magnetic sensing tape on floor, battery indicator LEDs green","magazines":"2 empty PCB magazines on AGV platform, clean and organized","conveyor":"short output conveyor connecting SUL460 to AGV transfer zone","details":["'SUL460' model label in bold on machine side panel","'SFY03' label on AGV body","green LEDs on both machines indicating operational status","magnetic navigation tape visible on factory floor in cyan-blue","orange safety bumper visible on AGV front"]},"supporting_elements":["clean smooth factory floor with faint yellow safety line","organized cable tray on ceiling","overhead sensor bar on ceiling above equipment","no human figures, no cables on floor"]},"text_treatment":{"title":"SUL460 + SFY03 — Seamless PCB Handling System","subtitle":"Auto Unloader + AGV Circulation | ±30s Changeover | ±5mm AGV Precision Docking","stats":"50KG AGV Load | 6-8hr Battery | 0.7M/S Speed | 24hr Operation","font_style":"bold white on dark overlay panel at bottom","accent":"thin yellow divider line"},"aspect_ratio":"16:9 (social media / exhibition) or 4:3 (product page)","quality":"ultra-detailed commercial industrial photography, realistic factory atmosphere, warm overhead lighting, premium manufacturing aesthetic, 4K"
```

---

## 🚀 Prompt #6: 波峰焊+治具清洗组合方案 — 信息图

**场景**: 波峰焊选型页 / 清洗设备关联销售图

```
{"type":"industrial equipment composite marketing board","product":{"brand":"Southern Machinery","models":["S-WS450 Wave Soldering Machine","SME5200 Full-Auto Fixture Cleaning Machine"],"category":"DIP production line + post-soldering cleaning solution","combo_value":"complete DIP line from soldering to clean fixture — Southern Machinery one-stop solution","S-WS450_specs":"450mm PCB | 300°C max | 460KG solder pot | dual wave | lead-free","SME5200_specs":"Φ1000mm×H200mm basket | 80L+80L tanks | 3-stage filtration | 30-40min cycle | 33KW total power"},"visual_identity":{"color_palette":["safety orange #FF6B00 (for wave solder machine)","industrial blue-gray #4A5568 (for cleaning machine)","clean white #F5F5F5 (for background)","data cyan #00D4FF (for flow arrows)","matte black #1A1A1A (for text panels)"]},"style":{"overall":"clean e-commerce composite board with warm industrial tones","mood":"complete solution, turnkey, professional, organized","lighting":"bright studio light, clean white background for cleaning machine, warm ambient for wave solderer","camera_angle":"two hero shots side by side, S-WS450 left (warm workshop feel), SME5200 right (clinical clean studio)","background":"split background: left half dark workshop, right half bright clinical white"},"layout":{"format":"wide composite board (16:9) split into 5 sections","sections":[{"title":"Wave Soldering + Fixture Cleaning — Full DIP Line Solution","position":"top full width","count":1,"labels":["S-WS450 + SME5200 Complete Solution","No more manual fixture cleaning | No more alcohol-based fire hazards | 30-40min automated cycle"]},{"title":"S-WS450 Wave Soldering Machine","position":"left-mid","count":3,"labels":["450mm PCB | 300°C | 460KG Solder Pot","Dual Wave + Lead-Free (SAC305)","4-Zone Preheat Independent Control"]},{"title":"SME5200 Fixture Cleaner","position":"right-mid","count":3,"labels":["Φ1000×H200mm Basket | 3-Stage Filtration","Water-Based Cleaning (No Alcohol Fire Hazard)","Cools, Cleans, Rinses, Dries in 30-40min"]},{"title":"Workflow Diagram","position":"lower-center","count":5,"labels":["Wave Solder Complete → Remove Fixtures → Load SME5200 → 30min Cycle → Ready for Next Shift"]},{"title":"Key Benefits","position":"bottom","count":4,"labels":["Fire Hazard Eliminated (water-based vs alcohol)","Fixture Life Extended (proper filtration)","Labor Cost Saved (automated vs manual scrub)","Production Uptime Improved (faster changeover)"]}]},"text_treatment":{"title_font":"bold orange/white on dark panel","machine_labels":"bold dark text on light panels","spec_font":"monospaced for numbers","flow_labels":"cyan arrows with white text","accent":"orange/cyan color coding distinguishing two machines"},"aspect_ratio":"16:9 (presentation / website)","quality":"ultra-detailed commercial marketing board, clean e-commerce aesthetic, professional industrial layout, 4K"
```

---

## 🚀 Prompt #7: THT整线方案（3机种组合）— E-commerce详情页

**场景**: THT整线方案页面 / 客户选型对比页

```
{"type":"THT production line e-commerce marketing board","product":{"brand":"Southern Machinery","line_type":"THT Full Automation Line (3-machine combo)","line_config":{"machine_1":"S-4000 Axial Inserter (axial components: resistors, diodes, capacitors)","machine_2":"S-3000 Radial Inserter (radial components)","machine_3":"S-70LD Odd-Form Inserter (relays, terminals, connectors, 3-25mm)"},"combined_benefit":"full THT coverage: axial + radial + odd-form = complete through-hole automation","visual_identity":{"brand_color":"Southern Machinery orange #FF6B00","machine_colors":{"S-4000":"orange #FF6B00 with dark gray panels","S-3000":"industrial green #2D8B57 with gray chassis","S-70LD":"industrial orange #FF6B00 with dark metal"},"color_scheme":["orange #FF6B00","dark gray #1E2024","industrial green #2D8B57","chrome label silver #B0BEC5","data blue #00D4FF"]}},"style":{"overall":"premium THT line catalog composite board","mood":"complete, professional, high-throughput, cost-effective","lighting":"bright factory ambient, each machine with dedicated key light, clean studio feel","camera_angle":"3 machine hero shots in landscape row, each machine with distinct personality shot (S-4000: front view with axial tape reels, S-3000: side view with radial component presentation, S-70LD: three-quarter view with feeder)","background":"dark charcoal seamless with subtle hex grid, orange accent lines connecting machines"},"layout":{"format":"tall portrait composite board (9:16) split into 8 sections","sections":[{"title":"Complete THT Automation Line","position":"top full width","count":1,"labels":["3 Machines. 100% Through-Hole Coverage. One Partner."]},{"title":"S-4000 Axial Inserter","position":"upper-left","count":3,"labels":["Axial Components Only","High Speed + Stable","Easy Material Changeover"]},{"title":"S-3000 Radial Inserter","position":"upper-right","count":3,"labels":["Radial Components Only","Preventive Maintenance Guide","High Throughput Design"]},{"title":"S-70LD Odd-Form Inserter","position":"mid-center (wide)","count":4,"labels":["Relays, Terminals, Connectors","3-25mm Component Range","STF1003 Feeder (0.8s | ±0.5mm)","Active Clinching Option (S-7900)"]},{"title":"Combined Speed","position":"lower-left","count":2,"labels":["Total THT Line: up to 18,000 CPH combined","Axial + Radial + Odd-Form = Zero Manual Insertion"]},{"title":"Cost Savings","position":"lower-center","count":3,"labels":["Replace 8-12 workers per shift","14-Month Average Payback","30-50% Lower CapEx than Japanese Lines"]},{"title":"CE Certification","position":"lower-right","count":2,"labels":["All Machines CE Certified","EU Safety Standards Compliant"]}]},"text_treatment":{"title_font":"bold condensed white/orange on dark panel at top","machine_headers":"bold orange/green/white on machine color cards","spec_font":"monospaced for all numbers","stats_font":"bold cyan for key numbers (18K CPH, 14-month payback, 8-12 workers)","accent":"colored divider lines matching each machine's brand color"},"aspect_ratio":"portrait 9:16 (mobile e-commerce)","quality":"ultra-detailed e-commerce marketing board, professional industrial catalog aesthetic, color-coded machine sections, 4K"
```

---

## 🚀 Prompt #8: LinkedIn Banner / Social Media Ad — 单产品版

**场景**: LinkedIn帖子封面 / Facebook广告图 / Instagram方形帖

```
{"type":"social media advertisement banner","product":{"brand":"Southern Machinery","model":"S-70LD (or S-7900 / S-WS450 / SUL460+SFY03 — swap model name)","category":"THT automation equipment for EMS factories","core_message":"Cut your THT labor costs by 38% | 30-50% lower CapEx than Fuji/Yamaha | CE Certified"},"visual_identity":{"brand_color":"Southern Machinery orange #FF6B00","text_color":"white #FFFFFF and orange #FF6B00 on dark background","color_palette":["dark charcoal #0D0D0D (background)","Southern orange #FF6B00 (brand accent)","white #FFFFFF (primary text)","electric cyan #00D4FF (data highlights)","gold #C0A060 (premium accents)"]},"style":{"overall":"bold social media ad with dramatic industrial backdrop","mood":"bold, direct, ROI-focused, professional","lighting":"dark dramatic with orange rim light on machine silhouette, subtle depth","camera_angle":"machine silhouette or sharp product shot as hero, text overlay at bottom third","background":"dark gradient with subtle factory grid pattern, orange light bloom from machine base"},"text_treatment":{"headline":"[Model Name] — Cut THT CapEx by 30-50%","subheadline":"Same throughput as Fuji/Yamaha. 14-month payback. 38% labor cost reduction.","cta":"Contact: jasonwu@smthelp.com | +86-136-0256-2576","brand":"Southern Machinery | www.smthelp.com","font":"bold condensed sans-serif, high contrast white/orange","accent":"thin orange divider line above brand line"},"layout":{"format":"square or portrait social media (1:1 or 4:5)","zones":[{"zone":"upper 60%","content":"hero machine shot or dramatic factory scene"},{"zone":"lower 40%","content":"dark panel with white headline + subheadline + brand line"}]},"aspect_ratio":"1:1 (Instagram square) or 4:5 (Instagram portrait) or 16:9 (LinkedIn banner)","quality":"bold social media advertisement, high contrast text, dramatic industrial aesthetic, 4K, optimized for social feed"
```

---

## 🚀 Prompt #9: 展会 Booth 背景 — 整线全景

**场景**: 展会展位背景墙 / 会议中心大屏 / 产品发布会舞台背景

```
{"type":"exhibition booth backdrop / event stage background","product":{"brand":"Southern Machinery","line_type":"Full SMT+THT+Wave Soldering+PCB Handling Production Line","display_mode":"dramatic full-line silhouette with key machine highlights"},"visual_identity":{"brand_color":"Southern Machinery orange #FF6B00","tech_colors":"dark industrial #0D0D0D background, electric cyan #00D4FF data flow lines","machines_color_coded":{"SMT_zone":"orange #FF6B00","THT_zone":"green #2ECC71","Wave_zone":"amber #F39C12","PCB_Handling_zone":"blue #3498DB"}},"style":{"overall":"massive dramatic exhibition backdrop with full production line visualization","mood":"impressive, futuristic, comprehensive, Industry 4.0","lighting":"dramatic stage lighting with orange and cyan accents, subtle volumetric light beams from above","camera_angle":"cinematic wide shot of entire line, bird's eye elevated 30° showing full 20-meter line in perspective","background":"very dark void with subtle circuit board trace pattern, glowing conveyor flow lines connecting all machines, holographic-style zone labels floating above each machine"},"scene_elements":{"machines_illustrated":{"SMT_Loder":"auto loader silhouette with orange LED","Printer":"solder paste printer with green status","Placer":"high-speed pick & place with 4 heads visible","Reflow":"reflow oven with thermal glow effect","AOI":"inspection system with blue scan lines","S-70LD":"odd-form inserter with orange accent, feeder visible","S-WS450":"wave solderer with amber solder glow","SUL460":"auto unloader with yellow chassis","SFY03":"AGV with cyan magnetic tape on floor"},"effects":["glowing orange conveyor lines connecting all machines","holographic zone labels floating above each machine","subtle particle effects suggesting PCB flow","ambient orange/cyan light bloom from machines","ceiling spotlight beams at 15° angles"]},"text_treatment":{"main_title":"FULL SMT + THT + WAVE SOLDERING LINE","main_title_font":"bold condensed white, massive scale (occupying top 15% of frame)","subtitle":"From Single Component to Complete Assembly — One Partner","subtitle_font":"clean sans-serif in electric cyan","machines_labels":"floating holographic labels above each machine zone","stats_panel":"bottom of frame: orange/gold text on dark transparent panel","stats_content":"35,000 CPH SMT | 4,000 CPH THT | 450mm Wave | 30-50% CapEx Savings | CE Certified | 4-8 Week Delivery","brand_tagline":"Southern Machinery — Precision at Scale"},"aspect_ratio":"16:9 (presentation / event backdrop / exhibition wall)","quality":"cinematic exhibition backdrop, ultra-detailed futuristic factory visualization, volumetric lighting, dramatic stage aesthetic, 8K resolution"
```

---

## 使用说明

### 快速替换模板

1. **换产品型号**: 将 `"S-70LD"` 替换为 `S-7900` / `S-7020T` / `S-WS450` / `SUL460` / `SFY03`
2. **换场景**: `product photography` → `lifestyle scene` / `infographic` / `social media ad`
3. **换比例**: `4:5` (电商) / `16:9` (展会/Banner) / `1:1` (社交媒体)
4. **换色调**: 工业橙 → 品牌橙色 `#FF6B00`；科技蓝 → 电蓝 `#00D4FF`

### 组合规则

| 目标用途 | 推荐 Prompt # | 组合产品 |
|---------|-------------|---------|
| 电商产品主图 | #1 / #3 | S-70LD / S-WS450 |
| 详情页信息图 | #2 / #7 | S-7900 / THT整线 |
| LinkedIn帖子 | #8 | 单产品 |
| 展会大屏 | #9 | 全线 |
| 工厂场景 | #5 | SUL460+SFY03 |
| 关联销售 | #6 | S-WS450+SME5200 |

### 质量优化技巧

- 加入 `no text, no watermark, no human figures` 获得纯产品图
- 加入 `blueprint-style annotations` 获得技术图解风格
- 加入 `shallow depth of field, bokeh background` 获得电影感
- 加入 `golden hour factory lighting` 获得暖调工业场景
- 将 `4K` 替换为 `8K` 用于大尺寸打印用途

### 禁止事项

- ❌ 不可在 prompt 中引用竞争品牌（Fuji/Yamaha/Panasonic）外观
- ❌ 不可生成包含真实工厂员工面孔的图片
- ❌ 不可使用非 Southern Machinery 品牌颜色（除标准工业色）
- ❌ 不可用于非 Southern Machinery 产品的营销场景
