# -*- coding: utf-8 -*-
"""English master strings for the odd-form feeder matcher page. Run: python3 tools/en_src.py -> product/i18n/en.json"""
import json, os

E = {}
E.update({
 "seo_title": "Odd-Form Feeder & Nozzle Matcher, Catalog V03 | Southern Machinery",
 "seo_desc": "Match odd-form THT components to the right feeder and nozzle: 76 real BOM lines, 10 Catalog V03 feeder models (tube, tray, bowl, belt, radial, axial, reel), filters by pitch and body size, free feasibility check.",
 "seo_keys": "odd form insertion feeder, odd-form component feeder, tube feeder, tray feeder, vibratory bowl feeder, belt feeder, radial tape feeder, axial tape feeder, gripper nozzle, customized feeder, THT feeder selection, NPI feeder, Southern Machinery",
 "og_title": "Which feeder fits this odd-form part? Southern Machinery quick-match table",
 "og_desc": "Filter 76 odd-form component examples by packaging, pitch, body size and lead count, see the Catalog V03 feeder and nozzle, and ask for a free feasibility check.",
 "topbar": "Shenzhen Southern Machinery · customized SMT and THT feeders and nozzles since 2011",
 "brand_sub": "Feeders · nozzles · odd-form insertion",
 "nav_matcher": "Quick match", "nav_npi": "NPI steps", "nav_fab": "Advantages", "nav_models": "Feeder models", "nav_spec": "Specs",
 "nav_videos": "Videos", "nav_blog": "Articles", "nav_docs": "Catalogs", "nav_faq": "FAQ", "nav_contact": "Feasibility check",
 "aria_theme": "Switch colour theme", "aria_lang": "Switch language", "aria_menu": "Menu", "aria_close": "Close",
 "aria_viewer": "Image viewer", "aria_wa": "Chat with Southern Machinery on WhatsApp", "aria_top": "Back to top", "lb_alt": "Enlarged product photo",
 "hero_badge": "Customized Feeder & Nozzle Catalog V03 · odd-form insertion",
 "hero_h1a": "Match every odd-form part",
 "hero_h1b": "to the right feeder and nozzle",
 "hero_sub": "Connectors in bulk, relays in tubes, transformers in trays, X2 capacitors on radial tape: look up how parts like yours were matched to Southern Machinery feeders and nozzles, then send your BOM for a free feasibility check.",
 "hero_cta1": "Ask for a feasibility check", "hero_cta2": "Open the quick-match table",
 "hero_note": "No price list on this page. Send the part, its packaging and your insertion machine model; we answer with the feeder and nozzle we would build and what we need to test.",
 "m1v": "10", "m1l": "feeder models in Catalog V03",
 "m2v": "76", "m2l": "component lines in the quick-match table",
 "m3v": "48 h", "m3l": "continuous ageing test on every catalog model",
 "m4v": "3–50 mm", "m4l": "component size range across tube, bowl and tray feeders",
 "trust1": "Shenzhen manufacturer, designing SMT/THT machines and feeders since 2011",
 "trust2": "IO hand-shake or stand-alone control through one 8-core 16 mm aviation plug",
 "trust3": "Samples or BOM tested free of charge before you commit",
 "sum_kick": "In one paragraph",
 "sum_h2": "What this page answers",
 "sum_p": "Southern Machinery (Shenzhen, founded 2011) builds customized feeders and nozzles that let odd-form insertion machines and SMT mounters pick parts standard feeders cannot present: SAF1001 axial tape, SRF1001 radial tape, STF1003 tube, SBF1001 vibratory bowl, SBF2002 belt, STP1001 tray, SJF1001 jumper wire, SRT7001 reel terminal, SSPC101 solder chip and SLF1001 label feeders, plus gripper and custom vacuum nozzles. The quick-match table maps 76 real component lines to those models by packaging, pitch and body size.",
 "sf1k": "Product", "sf1v": "Customized odd-form feeders and nozzles, Catalog V03",
 "sf2k": "Manufacturer", "sf2v": "Shenzhen Southern Machinery Sales and Service Co., Ltd., since 2011",
 "sf3k": "Packaging covered", "sf3v": "Bulk, tube, tray, radial tape, axial tape, reel (wire, terminal, solder, label)",
 "sf4k": "Component size", "sf4v": "3×3 mm to 50×50×50 mm, depending on feeder model",
 "sf5k": "Host machines", "sf5v": "Odd-form inserters and SMT mounters; IO communication or stand-alone",
 "sf6k": "Next step", "sf6v": "Free feasibility check on your samples or BOM",
 "why_kick": "Why odd-form parts stay manual",
 "why_h2": "The part is ready for automation. Its packaging is not.",
 "why_lead": "On most THT boards the radial and axial parts are already machine-inserted. What is left on the manual line is a list of odd shapes, each arriving in a different box.",
 "w1t": "Six packaging types on one board", "w1d": "Headers in bags, a relay in a tube, a transformer in a tray, Y-capacitors on ammo tape. A standard feeder bank expects one format, so the rest goes to hands.",
 "w2t": "Pitch that does not match the feeder", "w2d": "An X2 capacitor at 22.5 mm lead pitch is wider than a standard radial feeder's 15 mm body limit. The evaluation sheets mark exactly these lines as needing a custom feeder.",
 "w3t": "Grip, not suction", "w3d": "Open-frame headers, stacked USB and audio jacks have no flat top for a vacuum cup. Without a gripper nozzle shaped for the body, the head drops or tilts the part.",
 "w4t": "Missing data at NPI", "w4d": "Half the lines on a typical odd-form list carry a description and a packaging code but no dimensions. Feeder selection stalls until someone measures the sample.",
 "w5t": "Bulk parts with polarity", "w5d": "Trimmers, LEDs and buzzers in bulk must reach the pick point in one attitude. A bowl or belt feeder has to sort direction before the head arrives.",
 "w6t": "Every machine brand has its own rail", "w6d": "The feeder must mount, signal and stay at a repeatable pick position on your machine, not on a demo bench.",
 "mx_kick": "Core tool",
 "mx_h2": "Quick-match table: odd-form component to feeder",
 "mx_lead": "76 component lines taken from real odd-form evaluations and from Catalog V03, each mapped to a Southern Machinery feeder model and nozzle type. Filter by what you know about your part; click a row for the feeder description and a pre-filled feasibility request.",
 "mx_search": "Search", "mx_search_ph": "e.g. header, X2, USB, SRF1001",
 "mx_cat": "Component category", "mx_pack": "Packaging", "mx_feeder": "Feeder model", "mx_pitch": "Lead pitch",
 "mx_L": "Body length L", "mx_W": "Body width W", "mx_H": "Height H", "mx_leads": "Lead count", "mx_ld": "Lead diameter",
 "mx_any": "Any", "mx_unknown": "Include rows where this value is not in the source", "mx_unknown_v": "n/a",
 "mx_reset": "Reset filters", "mx_count": "{n} of {total} component lines", "mx_empty": "No line matches these filters. Widen a range or send us the part: an empty result is exactly the case for a feasibility check.",
 "mx_note": "Mapping rules: packaging decides the feeder family; body size, pitch and lead diameter are checked against the Catalog V03 envelope of that model. 'Fits catalog' means the source evaluation passed and the part is inside the published envelope; it is not a guarantee for your exact part. 'Confirmed mapping' is a confirmed pairing with a feeder outside Catalog V03: the host machine's own 32 mm tape feeder or the S-MVF01. Part numbers, customer names and suppliers are withheld.",
 "mx_col_comp": "Component", "mx_col_cat": "Category", "mx_col_pack": "Packaging", "mx_col_body": "Body L × W × H (mm)",
 "mx_col_pitch": "Pitch (mm)", "mx_col_leads": "Leads", "mx_col_ld": "Lead Ø (mm)", "mx_col_feeder": "Feeder", "mx_col_nozzle": "Nozzle / gripper", "mx_col_status": "Status",
 "mx_or": "or", "mx_d_title": "Component and feeder detail", "mx_d_spec": "Specification", "mx_d_body": "Body L × W × H (mm)", "mx_d_oh": "Overall height (mm)",
 "mx_d_feeder": "Suggested feeder", "mx_d_nozzle": "Nozzle / gripper", "mx_d_status": "Status", "mx_d_src": "Source", "mx_d_note": "Engineering note",
 "mx_d_env": "Catalog envelope", "mx_d_page": "Catalog V03, page",
 "mx_ask_wa": "Ask for a feasibility check (WhatsApp)", "mx_ask_mail": "Ask by email",
 "mx_ask_msg": "Hello Southern Machinery, please check feeder and nozzle feasibility for this odd-form component on our insertion machine (model: ____):",
 "mx_ask_subj": "Feasibility check",
 "mx_chk_h": "Check your own part against the catalog envelopes",
 "mx_chk_p": "Type what you know. Each feeder model is compared with the size, weight and lead-diameter range published in Catalog V03.",
 "mx_cL": "Length L (mm)", "mx_cW": "Width W (mm)", "mx_cH": "Height H (mm)", "mx_cWt": "Weight (g)", "mx_cLd": "Lead Ø (mm)",
 "mx_chk_fit": "Inside the published envelope of:", "mx_chk_none": "Outside every published envelope for this packaging. That is where a customized feeder starts: send a sample or drawing.",
 "mx_chk_out": "An envelope check is not a test. Orientation, lead stiffness and your machine's pick height decide the final answer.",
})
# categories, packaging, nozzles, statuses, sources
E.update({
 "mx_c_connector": "Connector / header", "mx_c_io": "I/O connector", "mx_c_capacitor": "Capacitor", "mx_c_protection": "Protection (MOV, NTC, PTC, surge)",
 "mx_c_magnetic": "Magnetics", "mx_c_electromech": "Electromechanical", "mx_c_semiconductor": "Semiconductor / LED", "mx_c_socket": "Socket / slot / holder",
 "mx_c_passive": "Resistor / passive", "mx_c_terminal": "Terminal, wire and hardware",
 "mx_p_bulk": "Bulk (loose)", "mx_p_tube": "Tube / stick", "mx_p_tray": "Tray", "mx_p_radial_tape": "Radial tape (ammo / reel)",
 "mx_p_axial_tape": "Axial tape", "mx_p_tape": "Embossed tape on reel", "mx_p_reel": "Coil / reel (wire, terminal, solder, label)",
 "mx_n_gripper": "Gripper nozzle", "mx_n_vacuum": "Vacuum nozzle (custom tip)", "mx_n_axial": "Axial lead handling", "mx_n_tbc": "Chosen at sample test",
 "mx_s_fit": "Fits catalog", "mx_s_conf": "Confirmed mapping", "mx_s_custom": "Customization", "mx_s_tbc": "To be confirmed", "mx_s_fam": "Family by packaging",
 "mx_src_bomA": "Odd-form evaluation A: power-supply board, 12 radial and axial lines (customer withheld)",
 "mx_src_bomB": "Odd-form evaluation B: connector board, 18 lines with measured dimensions (customer withheld)",
 "mx_src_bomC": "Odd-form list C: desktop board, 35 lines with packaging only (customer withheld)",
 "mx_src_bomD": "Odd-form sample list D: 6 lines with feeder type (customer withheld)",
 "mx_src_mvf": "S-MVF01 reciprocating belt feeder qualification template, 4 connectors",
 "mx_src_cat": "Southern Machinery Customized Feeder Nozzle Catalog V03",
})
# feeders: name, description, option label
F = {
 "srf1001": ("Radial Tape Feeder", "Feeds, forms, cuts and optionally bends (90°) radial parts from tape: electrolytic, Y- and square capacitors, terminals, springs, bent resistors. Outline 2×2×3 to 15×15×30 mm, lead core 0.3–1.0 mm, cut length 3–6 mm, tape hole pitch 12.7 or 15 mm (not interchangeable), ±0.2 mm, 1 s per cycle.", "SRF1001 radial tape"),
 "saf1001": ("Axial Tape Feeder", "Feeds taped resistors, triodes and jumper wires with U-shaping and lead trimming; material 3×3 to 6×20 mm, tape width 35, 64 or 92 mm (other widths built to order), ±0.3 mm, 0.8 s, optional paper tape return.", "SAF1001 axial tape"),
 "stf1003": ("Tube Feeder", "Feeds tube-packed relays, terminals, transformers, square and round capacitors, DIPs and transistors; 3×3×3 to 25×25×25 mm, PVC or aluminium tubes 200–650 mm, several tubes stacked, ±0.5 mm, 0.8 s, dual channel on request.", "STF1003 tube"),
 "sbf1001": ("Vibratory Bowl Feeder", "Sorts, orients and feeds bulk electronic components, hardware, plastic parts and connectors; 3×3 to 50×50 mm, 10–300 g, polarity sorting and lead cutting as options, single or front-and-rear bowls, ±0.5 mm, 0.8 s.", "SBF1001 vibratory bowl"),
 "sbf2002": ("Belt Feeder", "Compact, quiet bulk feeder with material selection and NG return for connectors, buzzers, network ports, terminals and square capacitors; 3×3×3 to 20×20×20 mm, ±1 mm, 1.5–2 s. Not for easily deformed pins.", "SBF2002 belt (bulk)"),
 "stp1001": ("Tray Feeder", "Supplies tray parts such as transformers, relays, hardware, memory sockets and large capacitors; 3×3×3 to 50×50×50 mm, PET blister trays 150×150 to 200×300 mm, up to 40 trays, ±1 mm, 3 s per part.", "STP1001 tray"),
 "sjf1001": ("Jumper Wire Feeder", "Straightens, cuts, forms and feeds tinned copper wire Ø0.5–1.2 mm from the roll; pin span 6–40 mm, pin length 3–5 mm, 5-minute mould change, ≤1.5 s per piece, no compressed air.", "SJF1001 jumper wire"),
 "srt7001": ("Reel Terminal Feeder", "Cuts and feeds reel terminals (tab 6.35 × 0.81 mm, 10.21 mm above the PCB) for SMT/THT machines and automated lines; ±0.5 mm, 0.8 s, empty-reel alarm after 3 misses.", "SRT7001 reel terminal"),
 "sspc101": ("Solder Chip Feeder", "Cuts and feeds solder sheet or wire from the coil, width 1–16 mm, thickness 0.1–1 mm; ±0.5 mm, 1.2 s, shortage alarm.", "SSPC101 solder chip"),
 "slf1001": ("Label Feeder", "Peels and presents labels, films, foam, adhesive, copper foil or steel sheet from the roll; liners under 60/80/100 mm, 0.05–0.08 mm thick, 3-inch core, ±0.2 mm X/Y.", "SLF1001 label"),
 "smvf01": ("Reciprocating Belt Feeder", "A separate model from the Catalog V03 SBF2002, with its own specification sheets, manual and videos, and its own component range. Bulk feeding: a motor-driven belt lifts loose parts to a selection track, rejected parts return on the belt, accepted parts reach the pick point by direct vibration, and a fibre-optic sensor confirms the part. IO communication or stand-alone. Component fit is confirmed per part with a sample.", "S-MVF01 reciprocating belt (bulk)"),
 "host_tape": ("32 mm tape feeder of the host machine", "Confirmed mapping for parts on 32 mm carrier tape: they run on the insertion machine's own 32 mm tape feeder, and Southern Machinery supplies the nozzle or gripper for the part.", "Host 32 mm tape feeder"),
}
for k, (n, d, o) in F.items():
    E["mx_f_%sn" % k], E["mx_f_%sd" % k], E["mx_fo_%s" % k] = n, d, o
T = {
 "audio_jack": "Audio jack", "battery_holder": "Battery holder", "buzzer": "Buzzer", "dimm": "DIMM memory socket", "dip_ic": "DIP IC",
 "dsub": "D-sub connector", "ecap": "Aluminium electrolytic capacitor", "hardware": "Hardware or plastic part", "inductor": "Inductor / choke",
 "jumper_shunt": "Jumper shunt", "jumper_wire": "Jumper wire", "label": "Label or film", "led": "LED", "led_indicator": "LED indicator",
 "memory_socket": "Memory module socket", "mov": "Varistor (MOV)", "network_port": "Network port (RJ45)", "ntc": "NTC thermistor",
 "pcie_slot": "PCIe slot", "pin_header": "Pin header", "pin_header_dual": "Dual-row pin header", "power_header": "Power connector header",
 "ptc": "PTC thermistor (inrush)", "reel_terminal": "Reel terminal", "relay": "Relay", "sata": "SATA connector", "smd_transistor": "SMD transistor",
 "solder_preform": "Solder preform", "spring": "Spring contact", "surge": "Surge absorber", "tact_switch": "Tact switch",
 "taped_resistor": "Axial resistor", "transformer": "Transformer", "trimmer": "Trimmer potentiometer", "usb_a": "USB-A connector",
 "usb_stack": "Stacked USB connector", "wafer": "Wafer / wire-to-board header", "wire_header": "Wire-to-board header", "x2_cap": "X2 safety capacitor",
 "y_cap": "Y1 safety capacitor",
}
for k, v in T.items():
    E["mx_t_" + k] = v
N = {
 "below_env": "Body diameter 2.6 mm is below the 3 mm minimum printed for SAF1001; confirm with a sample.",
 "buzzer_pack": "Buzzers arrive in bulk on one board and in trays on another: the packaging you receive decides the feeder.",
 "catalog_example": "Material type published in Catalog V03; envelope only, not a tested part.",
 "conditional": "Marked conditional in the source evaluation: samples or a packaging change are needed.",
 "desc_conflict": "The description gives 2×21 positions but a 3-pin count; the real pin count must be confirmed.",
 "dimm_size": "A DDR4 DIMM socket is far longer than the 50 mm published for STP1001: needs a customized tray solution.",
 "dims_needed": "Source gives description and packaging only; send dimensions or a sample to confirm the model.",
 "host_tape": "Confirmed mapping: runs on the host machine's own 32 mm tape feeder; Southern Machinery supplies the nozzle or gripper.",
 "joined_desc": "Pitch and pin count joined from a second list that carries the same part number.",
 "outside_env": "Body exceeds the published envelope of the standard model: customized feeder, confirm by sample test.",
 "outside_env_pitch": "22.5 mm pitch and a 26.5 mm body exceed the standard radial feeder; the source evaluation also flags a custom feeder.",
 "photo_id": "Component class identified from the photo in the source list.",
 "pitch_conflict": "The sheet's lead-width column disagrees with the pitch in the description; the description's P value is shown.",
 "pitch_needed": "Lead pitch is not in the source; it decides the SRF1001 forming mould.",
 "smd_bulk": "An SMD part in bulk is unusual for odd-form insertion; check whether it can be supplied on tape.",
}
for k, v in N.items():
    E["mx_note_" + k] = v
# NPI stepper
E.update({
 "npi_kick": "NPI feeder selection",
 "npi_h2": "Five steps from odd-form BOM to running feeder",
 "npi_lead": "The order an NPI engineer can follow for every odd-form line, so the feeder decision is made with data, not after the first failed trial.",
 "npi_prev": "Back", "npi_next": "Next step", "npi_cta": "Send samples or BOM", "npi_prog": "{d} of {n} checks done",
 "n1t": "Identify the packaging", "n1d": "Write down how each odd-form part actually arrives at your line, not how the datasheet says it can be ordered. Packaging decides the feeder family.",
 "n1c1": "Every odd-form line has a packaging code: bulk, tube, tray, radial tape, axial tape, embossed tape or coil.",
 "n1c2": "Lines with two possible packagings are flagged; ask purchasing which one is on the PO.",
 "n1c3": "For taped radial parts, the tape hole pitch (12.7 or 15 mm) is recorded.",
 "n2t": "Measure body, pitch and leads", "n2d": "Measure the real sample: body L × W × H, overall height above the board, lead pitch, lead count and lead diameter. These are the numbers the feeder envelope is checked against.",
 "n2c1": "Body L × W × H and overall height measured on the sample, in mm.",
 "n2c2": "Lead pitch, lead count and lead diameter recorded; any bent or kinked lead noted.",
 "n2c3": "Polarity mark and pick surface identified: flat top for vacuum, or a body that needs a gripper.",
 "n3t": "Match the feeder family", "n3d": "Use the quick-match table: packaging gives the family, dimensions check the envelope of the model. Parts outside the envelope go straight to the custom list.",
 "n3c1": "Each line mapped to a model (SRF1001, STF1003, SBF1001, SBF2002, STP1001 …) or to 'custom'.",
 "n3c2": "Nozzle type chosen per line: gripper or vacuum with a custom tip.",
 "n3c3": "Feeder slots counted against the space on your insertion machine.",
 "n4t": "Send samples or BOM for a free test", "n4d": "Send the list with photos, the dimensions and five to ten samples of every doubtful part, plus the exact insertion machine model and photos of its feeder rail.",
 "n4c1": "BOM with dimensions and packaging sent; part numbers may stay internal.",
 "n4c2": "Samples of every 'custom' or 'to be confirmed' line sent.",
 "n4c3": "Machine brand, model and feeder-rail photos sent.",
 "n5t": "Trial run and payback", "n5d": "Run the feeder on your machine with your parts, log feeding rate and stops, and compare the labour released with the cost of the feeder set.",
 "n5c1": "Trial run logged: parts fed, mis-picks, stops and their causes.",
 "n5c2": "Manual insertion hours released per month calculated (worksheet below).",
 "n5c3": "Spare parts, wear items and operator training agreed before the order.",
})
# FAB
E.update({
 "fab_kick": "What you get", "fab_h2": "Six technical advantages, each with a number behind it",
 "fab_lead": "Feature, what it does on the machine, and what it changes for your line.",
 "lab_f": "Feature", "lab_a": "Advantage", "lab_b": "Benefit",
 "fab1n": "Customized feeders", "fab1f": "Ten catalog feeder models covering axial, radial, tube, bowl, belt, tray, jumper wire, reel terminal, solder chip and label supply, each a base for customization.",
 "fab1a": "Track, mould or tray is adapted to your part instead of forcing the part into a standard format.", "fab1b": "Lines that stayed manual because no OEM feeder fits can move onto the machine.",
 "fab2n": "Customized nozzles and grippers", "fab2f": "Gripper nozzles with a fixed arm and a swing arm for odd shapes, special connectors and hybrid circuits; custom nozzles with interchangeable rubber tips for THT parts.",
 "fab2a": "The pick follows the body, so open headers, jacks and capacitors are held square through vision and insertion.", "fab2b": "Fewer drops and tilted inserts on exactly the parts that cause most manual rework.",
 "fab3n": "Works with your machine", "fab3f": "Every catalog model connects through an 8-core 16 mm aviation plug and runs with IO communication or on its own without communication.",
 "fab3a": "The feeder signals 'part ready' to the host, or runs stand-alone on a robot cell or non-standard machine.", "fab3b": "One feeder design serves odd-form inserters, SMT mounters and robot arms; the catalog lists installs on four machine brands.",
 "fab4n": "Tested before shipment", "fab4f": "Release records in Catalog V03: 48 hours continuous ageing on every model, plus 500 to 1,000 consecutive feeds without abnormality (2 hours continuous feeding for the bowl).",
 "fab4a": "Feeding faults show up on the bench, not during your first production week.", "fab4b": "Commissioning time goes into your parts and program, not into debugging the feeder.",
 "fab5n": "Precision by family", "fab5f": "Published feeding accuracy: ±0.2 mm radial and label, ±0.3 mm axial, ±0.5 mm tube, bowl, terminal and solder, ±1 mm tray and belt.",
 "fab5a": "You know which family can serve a tight pick position before you design the cell.", "fab5b": "Realistic expectations at NPI; tolerance questions are settled on paper.",
 "fab6n": "Free sample test", "fab6f": "Send samples or a BOM with dimensions; Southern Machinery engineering checks each line against feeder envelopes and your machine before quoting.",
 "fab6a": "Doubtful parts are tested on a feeder, not guessed from a datasheet.", "fab6b": "You commit to a feeder set with a written per-line result: fits, needs customization, or not possible.",
})
# models (10 cards) + fit table
MC = [
 ("SAF1001", "Axial tape", "Taped resistors, diodes and jumper wires; U-forming and lead trimming; 730×95×212 mm, 8 kg."),
 ("SRF1001", "Radial tape", "Capacitors, terminals, springs; cut, form and 90° bend; 12.7 or 15 mm tape; 720×92×165 mm, 10 kg."),
 ("STF1003", "Tube", "Relays, transformers, DIPs, capacitors from stacked tubes 200–650 mm; 1350×92×115 mm, 25 kg."),
 ("SBF1001", "Vibratory bowl", "Bulk connectors, hardware, plastic parts 3×3–50×50 mm, 10–300 g; single bowl 150 kg, double 190 kg."),
 ("SBF2002", "Belt (bulk)", "Connectors, buzzers, network ports up to 20×20×20 mm; NG return; 850×140×260 mm, 12 kg."),
 ("STP1001", "Tray", "Transformers, relays, sockets up to 50×50×50 mm; 40 trays under 10 mm; 1160×790×1530 mm, 75 kg."),
 ("SJF1001", "Jumper wire", "Tinned copper Ø0.5–1.2 mm, span 6–40 mm; no air supply; 580×50×180 mm."),
 ("SRT7001", "Reel terminal", "Tab 6.35 × 0.81 mm terminals cut from the reel; 550×130×110 mm, 10 kg."),
 ("SSPC101", "Solder chip", "Solder sheet or wire 1–16 mm wide, 0.1–1 mm thick; 540×115×230 mm, 7 kg."),
 ("SLF1001", "Label", "QR labels for MES, films, foam, copper foil, FPC stiffeners; 650×165×320 mm, 7.5 kg."),
]
E.update({"models_kick": "Catalog V03", "models_h2": "Ten feeder models, one per way a part can arrive",
          "models_lead": "Dimensions and weights as published in the Customized Feeder Nozzle Catalog V03."})
for i, (t, s, d) in enumerate(MC, 1):
    E["mc%dt" % i], E["mc%ds" % i], E["mc%dd" % i] = t, s, d
E.update({"fit_h": "Packaging → feeder family", "fit_c1": "Packaging at your line", "fit_c2": "Southern Machinery feeder", "fit_c3": "Check before choosing"})
FR = [
 ("Bulk connectors, headers, trimmers", "SBF1001 bowl or SBF2002 belt", "Belt up to 20×20×20 mm; bowl up to 50×50 mm and 300 g; deformable pins go to the bowl."),
 ("Tube / stick", "STF1003", "Tube length 200–650 mm, wall ≥ 0.6 mm, part up to 25 mm."),
 ("Tray", "STP1001", "Blister tray 150×150 to 200×300 mm, tray load ≤ 3 kg."),
 ("Radial tape (ammo or reel)", "SRF1001", "Tape hole pitch 12.7 or 15 mm; body up to 15×15×30 mm; lead core 0.3–1.0 mm."),
 ("Axial tape", "SAF1001", "Tape width 35, 64 or 92 mm; part 3×3 to 6×20 mm."),
 ("Wire, terminal or solder on a coil", "SJF1001, SRT7001, SSPC101", "Wire Ø0.5–1.2 mm; terminal tab 6.35 × 0.81 mm; solder 1–16 mm wide."),
 ("32 mm embossed carrier tape", "Host machine's own 32 mm tape feeder + Southern Machinery nozzle", "Confirmed mapping: the tape feeder is the host machine's; Southern Machinery supplies the nozzle or gripper."),
]
for i, (a, b, c_) in enumerate(FR, 1):
    E["fr%da" % i], E["fr%db" % i], E["fr%dc" % i] = a, b, c_
# spec table
SP = [
 ("Feeder models in the catalog", "SAF1001, SRF1001, STF1003, SBF1001, SBF2002, SLF1001, SJF1001, STP1001, SSPC101, SRT7001"),
 ("Host connection", "8-core 16 mm aviation plug; IO communication or self-control without communication"),
 ("Working voltage", "24 V (axial, radial, tube, label, terminal, solder, jumper); 220 V (bowl, belt, tray)"),
 ("Working air pressure", "0.4–0.6 MPa (jumper wire feeder needs no air)"),
 ("Feeding accuracy", "±0.2 mm radial and label · ±0.3 mm axial · ±0.5 mm tube, bowl, terminal, solder · ±1 mm tray, belt"),
 ("Feeding time", "0.8 s axial, tube, bowl, terminal · 1 s radial cycle · 1.2 s solder · ≤ 1.5 s jumper · 1.5–2 s belt · 3 s tray"),
 ("Component size", "3×3 to 6×20 mm axial · 2×2×3 to 15×15×30 mm radial · up to 25 mm tube · up to 20 mm belt · up to 50 mm bowl and tray"),
 ("Component weight", "10–300 g (bowl); tray load ≤ 3 kg (tray and label rolls)"),
 ("Lead / wire diameter", "Radial lead core 0.3–1.0 mm; jumper wire Ø0.5–1.2 mm"),
 ("Release tests", "48 h continuous ageing on every model; 500–1,000 consecutive feeds (bowl: 2 h continuous feeding)"),
 ("Nozzles", "Gripper nozzles (fixed + swing arm) for odd-form parts, special connectors, hybrid circuits; custom nozzles with interchangeable rubber tips"),
 ("Installed on", "Catalog success cases: Panasonic CM602, JUKI, YAMAHA and Mirae odd-form machines with tube, bowl and radial tape feeders"),
 ("Lead time", "Not stated in Catalog V03; quoted per project after the sample test"),
]
E.update({"spec_kick": "Catalog figures", "spec_h2": "Key specifications across the feeder range", "spec_lead": "Every value from the Customized Feeder Nozzle Catalog V03; the per-model PDF prevails.",
          "sp_c1": "Parameter", "sp_c2": "Value", "sp_c3": "Evidence", "ev_v": "Verified material", "ev_c": "Concept illustration", "ev_t": "To be confirmed",
          "spec_note": "Lead time is not a catalog figure: it is set in the quotation once the sample test shows how much customization each line needs."})
for i, (n, v) in enumerate(SP, 1):
    E["spr%dn" % i], E["spr%dv" % i] = n, v
# disclosure
DR = [
 ("Lead pitch on 3 radial lines (NTC, two PTCs)", "Description: P = 2.54, 5 and 10 mm", "Lead-width column of the same sheet: 4, 13 and 18 mm (the body width)", "Pitch taken from the description; the conflict is noted on each row."),
 ("Nozzle numbers for the same 9 bulk parts", "First copy of evaluation B: gripper series 2000/2001/2014", "Second copy: gripper 2070, vacuum 506/507/508", "Only the nozzle type (gripper or vacuum) is published; both copies agree on it."),
 ("Buzzer packaging", "Evaluation B: bulk, belt or bowl feeder", "List C: tray", "Different boards; both rows are kept and the packaging you receive decides."),
 ("Lead time", "Catalog V03: not stated", "SBF1001 parameter sheet: 1-month customized-solution commitment, 1-day spare parts", "Shown as to be confirmed; the quotation states it per project."),
 ("Company address", "Catalog V03: Room 1806, Block 3, Jinyun COFCO, Qianjin 2nd Road, Bao'an, Shenzhen 518102", "Brand profile: Xixiang, Bao'an District, Shenzhen", "Footer shows Bao'an District, Shenzhen until the current address is confirmed."),
]
E.update({"disc_kick": "Where sources disagree", "disc_h2": "Disclosure: five points printed side by side", "disc_lead": "Nothing averaged, nothing silently picked.",
          "dc_c1": "Topic", "dc_c2": "Source A", "dc_c3": "Source B", "dc_c4": "How we settle it"})
for i, (a, b, c_, d) in enumerate(DR, 1):
    E["dr%da" % i], E["dr%db" % i], E["dr%dc" % i], E["dr%dd" % i] = a, b, c_, d
# calc
E.update({"calc_kick": "Step 5 worksheet", "calc_h2": "How much manual insertion time a feeder set releases",
 "calc_lead": "Every figure is yours. The worksheet counts the operator hours that leave the manual insertion line; it does not price the feeders.",
 "calc_t": "Labour released per month", "calc_s": "Operators freed per shift × shifts × hours × working days.",
 "cf1": "Operators freed per shift", "cf2": "Shifts per day", "cf3": "Hours per shift", "cf4": "Working days per month",
 "cr1": "Operator hours released per month", "cr2": "Operator hours released per year",
 "calc_note": "Count only operators whose station disappears; loading feeders and refilling bowls still takes some operator time."})
# gallery
G = ["Odd-form feeder solution: tube, tray, bowl, belt and tape feeders by Southern Machinery",
 "S7900 odd-form insertion machines in a line (render)", "S7900 odd-form inserter with bowl feeders and conveyor (render)",
 "Gripper nozzle made by Southern Machinery for odd-form insertion", "Gripper nozzle for an odd-form insertion head",
 "Gripper nozzle base with fixed and swing arms", "Pair of gripper nozzles for odd-form parts",
 "Floor-standing tube feeder for odd-form insertion", "Tube feeders ready for shipment",
 "Vibratory bowl feeder on its stand", "Vibratory bowls with sorting tracks", "Double-bowl feeder for two bulk parts",
 "Radial tape feeders on the assembly bench", "Odd-form parts picked by Southern Machinery nozzles",
 "STP1001 tray feeder (Catalog V03, page 9)", "SBF2002 belt feeder (Catalog V03, page 6)",
 "SJF1001 jumper wire feeder (Catalog V03, page 8)", "SRT7001 reel terminal feeder (Catalog V03, page 11)"]
E.update({"gal_kick": "Photos and catalog pages", "gal_h2": "Feeders, nozzles and the S7900 they feed",
          "gal_lead": "Photos from ph.smthelp.com and crops from Catalog V03 pages, each labelled with what it shows."})
for i, v in enumerate(G, 1):
    E["g%d" % i] = v
# videos
E.update({"vid_kick": "Videos", "vid_h2": "Odd-form insertion, feeders and nozzles at work",
 "vid_lead": "23 videos from the Southern Machinery YouTube board, each checked live. Click a card to load the player.",
 "vf_all": "All", "vf_oddform": "Odd-form insertion", "vf_bulk": "Bowl and belt", "vf_tape": "Radial, axial, wire, terminal", "vf_tube": "Tube and tray", "vf_nozzle": "Nozzles and grippers",
 "vid_play": "Play video"})
# blog headings / summaries
B = [
 ("Why the last manual station is always odd-form", "The parts left by hand share one trait: their packaging, not their shape, keeps them off the machine."),
 ("Six packaging codes, six feeder families", "Bulk, tube, tray, radial tape, axial tape and coil each map to one feeder family. Start every NPI review there."),
 ("Pitch, body and lead: the three numbers to measure", "How lead pitch, body envelope and lead diameter decide whether a standard feeder works or a custom one is needed."),
 ("Gripper or vacuum: choosing the nozzle per part", "Open headers, jacks and capacitors need different pick tools. A practical rule set for the nozzle column of your BOM."),
 ("X2 capacitors and other parts that break the envelope", "What happens when a part is wider than the radial feeder allows, and how a customized feeder is specified."),
 ("Bulk parts: bowl or belt?", "Size, pin stiffness and polarity decide between a vibratory bowl and a belt feeder. The catalog numbers side by side."),
 ("A feasibility check that answers in writing", "What to send, what Southern Machinery tests, and what the per-line result looks like."),
 ("From first trial to a payback you can defend", "How to run the trial, log stops and turn released operator hours into a business case."),
]
E.update({"blog_kick": "Articles", "blog_h2": "Eight articles for NPI and process engineers",
 "blog_lead": "Short technical pieces on matching odd-form parts to feeders and nozzles.",
 "blog_note": "Article text is kept in English on every language version: these are technical pieces and a machine translation would blur the details.",
 "b_read": "Read the article", "b_min": "3 min read"})
for i, (t, s) in enumerate(B, 1):
    E["b%dt" % i], E["b%ds" % i] = t, s
# docs
DK = [("Customized Feeder Nozzle Catalog V03", "All ten feeder models and the special-application nozzles, 16 pages."),
 ("Innovative SMT/THT Odd Form Feeder Solution", "Odd-form feeder solution overview for EMS smart factories."),
 ("THT odd feeder configuration with SMT mounters (2024)", "How odd-form feeders are configured on SMT mounters."),
 ("S7900 Odd Form Machine Catalog 2025", "The odd-form insertion machine these feeders serve."),
 ("STF1003 Tube Feeder", "Catalog V03 sheet for the tube feeder."),
 ("STP1001 Tray Feeder", "Catalog V03 sheet for the tray feeder."),
 ("SBF1001 Vibration Bowl Feeder", "Catalog V03 sheet for the vibratory bowl feeder."),
 ("SBF2002 Reciprocating Belt Feeder", "Catalog V03 sheet for the belt feeder."),
 ("SRF1001 Radial Tape Feeder", "Catalog V03 sheet for the radial tape feeder."),
 ("Belt feeder vs bowl feeder", "Presentation comparing the two bulk-feeding approaches."),
 ("Customized gripper nozzle, 3D drawing", "Drawing of a customized SMT gripper nozzle."),
 ("Auto insertion PCB assembly requirements", "Board and component requirements for auto insertion.")]
E.update({"docs_kick": "Catalogs", "docs_h2": "Catalogs, sheets and drawings", "docs_lead": "Open the PDF in a new tab or preview it here.",
 "doc_open": "Open PDF", "doc_prev": "Preview", "dk_vb": "YouTube video board", "dk_vbd": "Every Southern Machinery video, searchable.",
 "dk_cb": "Product catalog board", "dk_cbd": "Every catalog, manual and drawing on the file server."})
for i, (t, d) in enumerate(DK, 1):
    E["dk%dt" % i], E["dk%dd" % i] = t, d
# service
E.update({"svc_kick": "How we work", "svc_h2": "From BOM to running feeder",
 "sv1t": "BOM review", "sv1d": "Each odd-form line mapped to a feeder family and nozzle type, gaps listed.",
 "sv2t": "Free sample test", "sv2d": "Doubtful parts run on a feeder; you get a per-line result in writing.",
 "sv3t": "Customization", "sv3d": "Track, mould, tray or gripper adapted to the part and to your machine's rail.",
 "sv4t": "Release test", "sv4d": "48-hour ageing and consecutive-feed test recorded before shipment.",
 "sv5t": "Commissioning support", "sv5d": "Pick position, IO hand-shake and operator training on your line, remote or on site."})
# FAQ
Q = [
 ("Which feeder do I need for an odd-form part?", "Start from the packaging: bulk goes to the SBF1001 bowl or SBF2002 belt, tubes to STF1003, trays to STP1001, radial tape to SRF1001, axial tape to SAF1001, coils to SJF1001, SRT7001 or SSPC101. Then check body size, pitch and lead diameter against that model's envelope in the quick-match table. The S-MVF01 reciprocating belt feeder is a separate model from SBF2002, with its own sheet; bulk parts are matched to it per part."),
 ("Do Southern Machinery feeders work with my insertion machine or SMT mounter?", "Every Catalog V03 model connects through an 8-core 16 mm aviation plug and runs with IO communication or stand-alone. The catalog shows installs on Panasonic CM602, JUKI, YAMAHA and Mirae odd-form machines; the exact mounting is confirmed from photos of your feeder rail."),
 ("What is the largest component a feeder can take?", "Up to 50×50×50 mm on the STP1001 tray feeder and 50×50 mm on the SBF1001 bowl (10–300 g). Tube parts go up to 25 mm, belt-fed parts up to 20 mm and radial taped parts up to 15×15×30 mm; anything larger is a customized feeder."),
 ("My X2 capacitor has a 22.5 mm pitch. Can it be fed?", "Not by the standard SRF1001, whose body envelope stops at 15 mm. Such lines are marked 'to be confirmed' in the table and handled as a customized radial feeder after a sample test."),
 ("When do I need a gripper nozzle instead of vacuum?", "When the part has no flat, sealed top: open pin headers, wafers, many connectors and Y-capacitors. Gripper nozzles with a fixed and a swing arm hold the body; parts with a flat top, such as jacks or electrolytic capacitors, usually take a vacuum nozzle with a custom tip."),
 ("How accurate is the feeding?", "As published in Catalog V03: ±0.2 mm radial and label feeders, ±0.3 mm axial, ±0.5 mm tube, bowl, terminal and solder, ±1 mm tray and belt."),
 ("Is the feasibility test really free?", "Yes. Send the BOM with dimensions and packaging, samples of doubtful parts and your machine model; you receive a written per-line result before any order."),
 ("What is the lead time?", "Catalog V03 does not state one. Lead time is quoted per project after the sample test, because it depends on how much customization each line needs."),
 ("Can bulk parts with polarity be fed in the right direction?", "Yes, when the polarity is physically recognizable. The SBF1001 bowl offers polarity sorting and lead cutting as options; the SBF2002 belt needs parts whose features can be told apart physically."),
 ("How are the feeders tested before shipment?", "Each catalog model carries a 48-hour continuous ageing test and 500 to 1,000 consecutive feeds without abnormality; the bowl feeder is run for 2 hours of continuous feeding."),
]
E.update({"faq_kick": "FAQ", "faq_h2": "Questions NPI engineers ask first"})
for i, (q, a) in enumerate(Q, 1):
    E["q%dt" % i], E["q%da" % i] = q, a
# family, contact, footer
E.update({
 "fam_kick": "Same family", "fam_h2": "Machines and feeders these parts run on",
 "fam1": "S7900 odd-form insertion machine", "fam2": "SBF1001 vibratory bowl feeder", "fam3": "S3000 radial insertion machine", "fam4": "S4000 axial insertion machine", "fam5": "FUJI NXT feeder calibration jig", "fam6": "S-MVF01 reciprocating belt feeder",
 "ct_kick": "Feasibility check", "ct_h2": "Send the odd-form lines that are still manual",
 "ct_lead": "BOM with packaging and dimensions, photos or samples, and your insertion machine model. You get a per-line answer: feeder, nozzle, and what needs testing.",
 "wa_btn": "WhatsApp an engineer", "mail_btn": "Email info@smthelp.com",
 "f_name": "Name", "f_company": "Company", "f_email": "Email", "f_machine": "Insertion machine brand and model", "f_parts": "Number of odd-form lines",
 "f_msg": "Parts, packaging and what you want to automate", "f_send": "Open my email with this request",
 "f_note": "This form opens your own email program. Nothing is sent from this page to any server.",
 "f_subject": "Feasibility check: odd-form feeders and nozzles",
 "foot_about": "Shenzhen Southern Machinery Sales and Service Co., Ltd. designs and manufactures SMT and THT machines, odd-form feeders and nozzles for PCB assembly automation. Founded in Shenzhen in 2011.",
 "foot_h1": "This page", "fl1": "Customized Feeder Nozzle Catalog V03 (PDF)", "fl2": "S7900 Odd Form Machine Catalog 2025 (PDF)", "fl3": "smthelp.com",
 "foot_h2": "Browse", "fl5": "Machine catalog: file.autoinsertion.com", "fl6": "Machine photos: ph.smthelp.com", "fl7": "YouTube video board", "fl8": "Product catalog board",
 "foot_h3": "Contact", "foot_wa": "WhatsApp +86 136 0256 2576", "foot_addr": "Bao'an District, Shenzhen, China",
 "foot_browse": "Browse our machine catalog at file.autoinsertion.com and find machine photos at ph.smthelp.com.",
 "foot_contact": "Contact us: info@smthelp.com",
 "foot_rights": "© 2026 Southern Machinery. Figures are quoted from Catalog V03 and the evaluations named on this page; the drawing confirmed with your order prevails.",
 "soc_lic": "LinkedIn Company Page", "soc_lip": "LinkedIn Profile", "soc_tw": "Twitter", "soc_fb": "Facebook", "soc_yt": "YouTube Channel",
})
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "i18n", "en.json")
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(E), "keys ->", out)
