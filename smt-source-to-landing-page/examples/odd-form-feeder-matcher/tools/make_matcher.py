#!/usr/bin/env python3
"""Build product/matcher.json for the odd-form feeder quick-match table.

Sources (all anonymised: no customer names, contacts, part numbers, supplier part numbers or prices):
  bomA  = "JM Checklist budgetary Ver.4.2.xlsx", sheet "Complete example" (12 radial/axial lines of a power-supply board)
  bomB  = "Odd Form component List with dimension.xlsx" (18 lines, body + overall dimensions; descriptions are photos only,
          component class identified by eye from the embedded photos) and its copy in "feeders_smt_help.xlsx" (JM_Study, 9 lines)
  bomC  = "feeders_smt_help.xlsx", sheet "Plan1" (35-line desktop board: description + packaging, no dimensions)
  bomD  = "Odd Form Insertion component list sample.xlsx" (6 lines: description, packaging, feeder type)
  mvf   = S-MVF01 reciprocating belt feeder qualification template (Components for MVF_SM.xlsx, 4 connectors, PW/PL/H/LH).
          S-MVF01 is a separate model from the Catalog V03 SBF2002 (Jason, 2026-10-23), so these rows name S-MVF01.
  cat   = Southern Machinery Customized Feeder Nozzle Catalog V03 (feeder envelopes, pages 2-12)
Dimensions: L >= W is the footprint (mm), H = body height, OH = overall height (body + leads above board where the source gives it).
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "matcher.json")
CAT = "https://file.autoinsertion.com/public/Southern%20Machinery%20Product/"

feeders = [
    dict(id="srf1001", model="SRF1001", page=3, pack=["radial_tape"], env={"L": [2, 15], "W": [2, 15], "H": [3, 30], "ld": [0.3, 1.0]},
         envtxt="2×2×3 – 15×15×30 mm · Ø 0.3–1.0 mm · 12.7 / 15 mm", image="https://ph.smthelp.com/images/2026/08/09/southern-machinery-radial-tape-feeder-image-0082.webp",
         url=CAT + "SRF1001%20Radial%20Tape%20Feeder%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="saf1001", model="SAF1001", page=2, pack=["axial_tape"], env={"L": [3, 20], "W": [3, 6], "H": [3, 6]},
         envtxt="3×3 – 6×20 mm · 35 / 64 / 92 mm",
         url=CAT + "SAF1001%20Axial%20Tape%20Feeder%20%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="stf1003", model="STF1003", page=4, pack=["tube"], env={"L": [3, 25], "W": [3, 25], "H": [3, 25]},
         envtxt="3×3×3 – 25×25×25 mm · 200–650 mm", image="https://ph.smthelp.com/images/2026/09/14/smthelp-feeder-tube-feeder-product-17.webp",
         url=CAT + "STF1003%20Tube%20Feeder%20%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="sbf1001", model="SBF1001", page=5, pack=["bulk"], env={"L": [3, 50], "W": [3, 50], "wt": [10, 300]},
         envtxt="3×3 – 50×50 mm · 10–300 g", image="https://ph.smthelp.com/images/2026/08/09/southern-machinery-bowl-feeder-img-1424-0163.webp",
         url=CAT + "SBF1001%20Vibration%20Bowl%20Feeder%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="sbf2002", model="SBF2002", page=6, pack=["bulk"], env={"L": [3, 20], "W": [3, 20], "H": [3, 20]},
         envtxt="3×3×3 – 20×20×20 mm",
         url=CAT + "SBF2002%20Reciprocating%20Belt%20Feeder%20%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="smvf01", model="S-MVF01", pack=["bulk"],
         url="https://file.autoinsertion.com/public/Product%20landing%20Page/s-mvf01-reciprocating-belt-feeder-smart-ems-pcb-assembly.html"),
    dict(id="stp1001", model="STP1001", page=9, pack=["tray"], env={"L": [3, 50], "W": [3, 50], "H": [3, 50]},
         envtxt="3×3×3 – 50×50×50 mm · 150×150 – 200×300 mm · ≤ 3 kg",
         url=CAT + "STP1001%20Tray%20Feeder%20%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="sjf1001", model="SJF1001", page=8, pack=["reel"], env={"ld": [0.5, 1.2]}, envtxt="Ø 0.5–1.2 mm · 6–40 mm · 3–5 mm",
         url=CAT + "SJF1001%20Jumper%20Wire%20Feeder%20%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="srt7001", model="SRT7001", page=11, pack=["reel"], env={}, envtxt="6.35 × 0.81 mm · 10.21 mm",
         url=CAT + "SRT7001%20Reel%20Terminal%20Feeder%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="sspc101", model="SSPC101", page=10, pack=["reel"], env={}, envtxt="1–16 mm × 0.1–1 mm",
         url=CAT + "SSPC101%20Solder%20Chip%20Feeder%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="slf1001", model="SLF1001", page=7, pack=["reel"], env={}, envtxt="< 60 / 80 / 100 mm · 0.05–0.08 mm",
         url=CAT + "SLF1001%20Label%20Feeder%20%20Southern%20Machinery%20Customized%20Feeder%20Nozzle%20Catalog%20V03.pdf"),
    dict(id="host_tape", model="", own=False, pack=["tape"], env={}, envtxt="32 mm"),
]

R = []


def row(id, type, cat, pack, feeder, src, status, spec="", L=None, W=None, H=None, OH=None, pitch=None, leads=None, ld=None,
        nozzle=None, alt=None, note=None):
    if L is not None and W is not None and W > L:
        L, W = W, L
    R.append({k: v for k, v in dict(id=id, type=type, spec=spec, cat=cat, pack=pack, L=L, W=W, H=H, OH=OH, pitch=pitch, leads=leads,
                                     ld=ld, feeder=feeder, alt=alt, nozzle=nozzle, status=status, note=note, src=src).items()
              if v not in (None, "")})


# ---- bomA: radial / axial ammo-pack lines (pitch from the description "P=" because the sheet's lead-width column disagrees on 3 lines)
row("A01", "y_cap", "capacitor", "radial_tape", "srf1001", "bomA", "custom", "Y1 2.2 nF, Ø11 × 5.5 mm", L=10, W=5, H=10, OH=14, pitch=10, leads=2, ld=0.55, nozzle="gripper")
row("A02", "surge", "protection", "axial_tape", "saf1001", "bomA", "tbc", "200 Vdc, Ø2.6 × 7.0 mm", L=7.0, W=2.6, H=2.6, OH=7.8, pitch=7, leads=2, ld=0.5, nozzle="axial", note="below_env")
row("A03", "mov", "protection", "radial_tape", "srf1001", "bomA", "custom", "10D, Ø12.5 × 5.9 mm, Y-kink", L=12.5, W=4.9, H=16.5, OH=20.5, pitch=7.5, leads=2, ld=0.8, nozzle="gripper")
row("A04", "ecap", "capacitor", "radial_tape", "srf1001", "bomA", "custom", "220 µF 35 V, Ø8 × 12 mm", L=8, W=8, H=11, OH=15, pitch=3.5, leads=2, ld=0.6, nozzle="vacuum")
row("A05", "x2_cap", "capacitor", "radial_tape", "srf1001", "bomA", "tbc", "X2 2.2 µF, 27 × 30 × 14.5 mm", L=26.5, W=13, H=22, OH=26, pitch=22.5, leads=2, ld=0.8, nozzle="vacuum", note="outside_env_pitch")
row("A06", "ntc", "protection", "radial_tape", "srf1001", "bomA", "custom", "NTC 10 kΩ, Ø4 × 3.5 mm", L=4, W=3, H=7, OH=11, pitch=2.54, leads=2, ld=0.5, nozzle="gripper", note="pitch_conflict")
row("A07", "ptc", "protection", "radial_tape", "srf1001", "bomA", "custom", "PTC 25 Ω 2 A, Ø13 × 6 mm", L=13, W=7, H=16.5, OH=19.5, pitch=5, leads=2, ld=0.6, nozzle="gripper", note="pitch_conflict")
row("A08", "ecap", "capacitor", "radial_tape", "srf1001", "bomA", "custom", "1 mF 50 V, Ø13 × 25 mm", L=13, W=13, H=25, OH=29, pitch=5, leads=2, ld=0.6, nozzle="vacuum")
row("A09", "x2_cap", "capacitor", "radial_tape", "srf1001", "bomA", "tbc", "X2 1 µF, 27 × 22.4 × 9 mm", L=26.5, W=8.5, H=17, OH=21, pitch=22.5, leads=2, ld=0.8, nozzle="vacuum", note="outside_env_pitch")
row("A10", "y_cap", "capacitor", "radial_tape", "srf1001", "bomA", "custom", "Y1 3.3 nF, Ø13 × 5.5 mm", L=12, W=5, H=12, OH=16, pitch=10, leads=2, ld=0.55, nozzle="gripper")
row("A11", "surge", "protection", "axial_tape", "saf1001", "bomA", "tbc", "3300 Vdc 5 kA, Ø8 × 6 mm", L=8, W=6, H=8, OH=12, pitch=12, leads=2, ld=0.8, nozzle="axial", note="outside_env")
row("A12", "ptc", "protection", "radial_tape", "srf1001", "bomA", "tbc", "PTC 50 Ω 10 A, Ø18 × 7 mm", L=18, W=7, H=21.5, OH=25.5, pitch=10, leads=2, ld=0.6, nozzle="gripper", note="outside_env")

# ---- bomB: connector-heavy board, dimensions in the source; class identified from the embedded photos
row("B01", "pin_header_dual", "connector", "bulk", "sbf2002", "bomB", "fit", "2-row, red housing", L=16, W=4, H=6, OH=8.5, nozzle="gripper", alt="sbf1001")
row("B02", "audio_jack", "io", "tape", "host_tape", "bomB", "conf", "3.5 mm, green", L=17.63, W=11.8, H=11, OH=14, nozzle="vacuum", note="host_tape")
row("B03", "pin_header_dual", "connector", "bulk", "sbf2002", "bomB", "fit", "2 × 3, black housing", L=6.55, W=5.65, H=5.65, OH=7.9, nozzle="gripper", alt="sbf1001")
row("B04", "inductor", "magnetic", "bulk", "sbf2002", "bomB", "fit", "box body, 2 leads", L=10.41, W=6.55, H=9.9, OH=13.05, leads=2, nozzle="vacuum", alt="sbf1001", note="photo_id")
row("B05", "pin_header", "connector", "bulk", "sbf2002", "bomB", "fit", "1-row, yellow housing", L=15.78, W=4, H=6.4, OH=7.9, nozzle="gripper", alt="sbf1001")
row("B06", "pin_header", "connector", "bulk", "sbf2002", "bomB", "fit", "1-row, black housing", L=10, W=4, H=5.85, OH=8.55, nozzle="gripper", alt="sbf1001")
row("B07", "buzzer", "electromech", "bulk", "sbf2002", "bomB", "fit", "Ø11.84 mm", L=11.84, W=11.84, H=9.43, OH=13.1, leads=2, nozzle="vacuum", alt="sbf1001", note="buzzer_pack")
row("B08", "pin_header", "connector", "bulk", "sbf2002", "bomB", "fit", "1-row, white housing", L=12, W=5.65, H=5.9, OH=8, nozzle="gripper", alt="sbf1001")
row("B09", "audio_jack", "io", "tape", "host_tape", "bomB", "conf", "3.5 mm, black", L=16, W=12.45, H=6.55, OH=8.71, nozzle="vacuum", note="host_tape")
row("B10", "led_indicator", "semiconductor", "tape", "host_tape", "bomB", "conf", "right-angle housing", L=12, W=4.26, H=9.26, OH=12, nozzle="gripper", note="host_tape")
row("B11", "sata", "io", "tray", "stp1001", "bomB", "custom", "7-pin vertical", L=16, W=6.4, H=8.9, OH=11.44, pitch=1.7, leads=7, nozzle="gripper", note="joined_desc")
row("B12", "usb_stack", "io", "tray", "stp1001", "bomB", "custom", "USB 3.0, dual stacked", L=17.5, W=14.8, H=14.8, OH=18.7, nozzle="vacuum")
row("B13", "wafer", "connector", "bulk", "sbf2002", "bomB", "fit", "4-pin, friction lock, red", L=10.24, W=5.78, H=9.6, OH=13.5, leads=4, nozzle="gripper", alt="sbf1001")
row("B14", "wafer", "connector", "bulk", "sbf2002", "bomB", "fit", "4-pin, white", L=10.2, W=5.85, H=10.45, OH=13.5, leads=4, nozzle="gripper", alt="sbf1001")
row("B15", "usb_a", "io", "tape", "host_tape", "bomB", "conf", "single port, low profile", L=14.5, W=14.4, H=5.8, OH=8.2, nozzle="vacuum", note="host_tape")
row("B16", "wafer", "connector", "bulk", "sbf2002", "bomB", "fit", "2-pin, white", L=5.86, W=5.13, H=10.2, OH=13.5, leads=2, nozzle="gripper", alt="sbf1001")
row("B17", "power_header", "connector", "bulk", "sbf2002", "bomB", "fit", "2 × 2, black", L=8.75, W=6.65, H=9.3, OH=12.56, leads=4, nozzle="gripper", alt="sbf1001")
row("B18", "power_header", "connector", "bulk", "sbf2002", "bomB", "tbc", "2 × 4, white", L=18.44, W=10.8, H=12.8, OH=16.22, leads=8, nozzle="gripper", alt="sbf1001", note="conditional")

# ---- bomC: desktop board, packaging list only (no dimensions in the source except where the description carries them)
row("C01", "jumper_shunt", "connector", "bulk", "sbf1001", "bomC", "fam", "2-position, 2.54 mm", pitch=2.54, leads=2, note="dims_needed")
row("C02", "audio_jack", "io", "tape", "host_tape", "bomC", "fam", "3.5 mm, 5-pin, on reel", leads=5, note="host_tape")
row("C03", "audio_jack", "io", "tape", "host_tape", "bomC", "fam", "3.5 mm, 6-pin, on reel", leads=6, note="host_tape")
row("C04", "pin_header", "connector", "bulk", "sbf1001", "bomC", "fam", "1 × 2, 2.54 mm", pitch=2.54, leads=2, alt="sbf2002", note="dims_needed")
row("C05", "buzzer", "electromech", "tray", "stp1001", "bomC", "fam", "5 V 40 mA", leads=2, note="buzzer_pack")
row("C06", "led", "semiconductor", "tray", "stp1001", "bomC", "fam", "THT LED", leads=2, note="dims_needed")
row("C07", "ecap", "capacitor", "radial_tape", "srf1001", "bomC", "fam", "Ø6.3 × 8 mm, 4 part numbers", L=6.3, W=6.3, H=8, leads=2, note="pitch_needed")
row("C08", "ecap", "capacitor", "radial_tape", "srf1001", "bomC", "fam", "33 µF 25 V, Ø5 × 11 mm", L=5, W=5, H=11, leads=2, note="pitch_needed")
row("C09", "ecap", "capacitor", "radial_tape", "srf1001", "bomC", "fam", "Ø6.3 × 11 mm, 2 part numbers", L=6.3, W=6.3, H=11, leads=2, note="pitch_needed")
row("C10", "pin_header", "connector", "bulk", "sbf1001", "bomC", "fam", "1 × 3, 2.54 mm", pitch=2.54, leads=3, alt="sbf2002", note="dims_needed")
row("C11", "power_header", "connector", "bulk", "sbf1001", "bomC", "fam", "2 × 2, 3.0 mm", pitch=3.0, leads=4, alt="sbf2002", note="dims_needed")
row("C12", "pin_header_dual", "connector", "bulk", "sbf1001", "bomC", "fam", "2 × 6 keyed (11 pins), 2.54 mm", pitch=2.54, leads=11, alt="sbf2002", note="dims_needed")
row("C13", "pin_header_dual", "connector", "bulk", "sbf1001", "bomC", "fam", "2 × 3 keyed (5 pins), 2.54 mm", pitch=2.54, leads=5, alt="sbf2002", note="dims_needed")
row("C14", "wafer", "connector", "bulk", "sbf1001", "bomC", "fam", "1 × 2, 2.5 mm", pitch=2.5, leads=2, alt="sbf2002", note="dims_needed")
row("C15", "usb_stack", "io", "tray", "stp1001", "bomC", "fam", "USB 3.0, 18-pin", leads=18, note="dims_needed")
row("C16", "pcie_slot", "socket", "tray", "stp1001", "bomC", "tbc", "PCIe x1, 36-pin, 1.0 mm", pitch=1.0, leads=36, note="dims_needed")
row("C17", "power_header", "connector", "bulk", "sbf1001", "bomC", "fam", "2 × 2, 4.2 mm", pitch=4.2, leads=4, alt="sbf2002", note="dims_needed")
row("C18", "power_header", "connector", "bulk", "sbf1001", "bomC", "fam", "2 × 3, 4.2 mm", pitch=4.2, leads=6, alt="sbf2002", note="dims_needed")
row("C19", "pin_header", "connector", "bulk", "sbf1001", "bomC", "fam", "1 × 4 fan header, 2.54 mm", pitch=2.54, leads=4, alt="sbf2002", note="dims_needed")
row("C20", "tact_switch", "electromech", "bulk", "sbf1001", "bomC", "fam", "DIP 4-pin", leads=4, alt="sbf2002", note="dims_needed")
row("C21", "battery_holder", "socket", "tray", "stp1001", "bomC", "fam", "CR2032, 2-pin", leads=2, note="dims_needed")
row("C22", "usb_stack", "io", "tray", "stp1001", "bomC", "fam", "USB 3.0 + USB 2.0, 27-pin", leads=27, note="dims_needed")
row("C23", "smd_transistor", "semiconductor", "bulk", "sbf1001", "bomC", "tbc", "3-pin, SMD body", leads=3, note="smd_bulk")
row("C24", "dimm", "socket", "tray", "stp1001", "bomC", "tbc", "DDR4, 288-pin", leads=288, note="dimm_size")
row("C25", "inductor", "magnetic", "tray", "stp1001", "bomC", "fam", "power choke, 2 part numbers", note="dims_needed")
row("C26", "dsub", "io", "tray", "stp1001", "bomC", "fam", "15-pin", leads=15, note="dims_needed")
row("C27", "pin_header_dual", "connector", "bulk", "sbf1001", "bomC", "tbc", "2 × 21, 2.54 mm", pitch=2.54, note="desc_conflict")

# ---- bomD: sample list with feeder type
row("D01", "transformer", "magnetic", "tray", "stp1001", "bomD", "fam", "single tray", note="dims_needed")
row("D02", "dip_ic", "semiconductor", "tube", "stf1003", "bomD", "fam", "PWM off-line switch, DIP-8", pitch=2.54, leads=8, note="dims_needed")
row("D03", "trimmer", "electromech", "bulk", "sbf1001", "bomD", "fam", "0.1 W, 2 part numbers", leads=3, alt="sbf2002", note="dims_needed")
row("D04", "pin_header", "connector", "bulk", "sbf1001", "bomD", "fam", "vertical, 4-pin, 2.5 mm", pitch=2.5, leads=4, alt="sbf2002", note="dims_needed")
row("D05", "wafer", "connector", "bulk", "sbf1001", "bomD", "fam", "2-pin, 1 row, right-angle shrouded, 2.5 mm", pitch=2.5, leads=2, alt="sbf2002", note="dims_needed")

# ---- mvf: S-MVF01 qualification template (Southern Machinery engineering judgment "OK"); H = overall incl. pins
row("M01", "wire_header", "connector", "bulk", "smvf01", "mvf", "conf", "4-circuit, 3.0 mm (.120 in)", L=12, W=6.6, OH=14.7, pitch=3.0, leads=4, nozzle="gripper", alt="sbf1001")
row("M02", "pin_header", "connector", "bulk", "smvf01", "mvf", "conf", "2-position, 2.54 mm (.1 in)", L=6.35, W=5, OH=14.22, pitch=2.54, leads=2, nozzle="gripper", alt="sbf1001")
row("M03", "pin_header", "connector", "bulk", "smvf01", "mvf", "conf", "3-pin, 3.96 mm (.156 in), vertical", L=7.62, W=6.35, OH=14.22, pitch=3.96, leads=3, nozzle="gripper", alt="sbf1001")
row("M04", "pin_header", "connector", "bulk", "smvf01", "mvf", "conf", "6-pin, 3.96 mm (.156 in), vertical", L=15, W=6.35, OH=14.22, pitch=3.96, leads=6, nozzle="gripper", alt="sbf1001")

# ---- cat: catalog reference examples (published material types; envelope only)
row("K01", "reel_terminal", "terminal", "reel", "srt7001", "cat", "fit", "tab 6.35 × 0.81 mm, 10.21 mm above PCB", W=0.81, note="catalog_example")
row("K02", "jumper_wire", "terminal", "reel", "sjf1001", "cat", "fit", "tinned copper Ø0.5–1.2 mm, span 6–40 mm", ld=1.2, note="catalog_example")
row("K03", "solder_preform", "terminal", "reel", "sspc101", "cat", "fit", "width 1–16 mm, thickness 0.1–1 mm", note="catalog_example")
row("K04", "label", "terminal", "reel", "slf1001", "cat", "fit", "liner < 60 / 80 / 100 mm, 0.05–0.08 mm", note="catalog_example")
row("K05", "relay", "electromech", "tube", "stf1003", "cat", "fam", "up to 25 × 25 × 25 mm", note="catalog_example")
row("K06", "network_port", "io", "bulk", "sbf2002", "cat", "fam", "up to 20 × 20 × 20 mm", alt="sbf1001", note="catalog_example")
row("K07", "spring", "terminal", "radial_tape", "srf1001", "cat", "fam", "up to 15 × 15 × 30 mm", note="catalog_example")
row("K08", "taped_resistor", "passive", "axial_tape", "saf1001", "cat", "fam", "3 × 3 – 6 × 20 mm, U-forming option", note="catalog_example")
row("K09", "memory_socket", "socket", "tray", "stp1001", "cat", "fam", "up to 50 × 50 × 50 mm", note="catalog_example")
row("K10", "hardware", "terminal", "bulk", "sbf1001", "cat", "fam", "3 × 3 – 50 × 50 mm, 10–300 g", note="catalog_example")

D = {
    "categories": ["connector", "io", "capacitor", "protection", "magnetic", "electromech", "semiconductor", "socket", "passive", "terminal"],
    "packaging": ["bulk", "tube", "tray", "radial_tape", "axial_tape", "tape", "reel"],
    "nozzles": ["gripper", "vacuum", "axial", "tbc"],
    "statuses": ["fit", "conf", "custom", "tbc", "fam"],
    "sources": ["bomA", "bomB", "bomC", "bomD", "mvf", "cat"],
    "bins": {
        "pitch": [[0, 2.0, "≤ 2.0 mm"], [2.0, 2.6, "2.0 – 2.6 mm"], [2.6, 5.0, "2.6 – 5.0 mm"], [5.0, 10.0, "5.0 – 10 mm"], [10.0, 999, "> 10 mm"]],
        "size": [[0, 5, "≤ 5 mm"], [5, 10, "5 – 10 mm"], [10, 15, "10 – 15 mm"], [15, 25, "15 – 25 mm"], [25, 50, "25 – 50 mm"], [50, 9999, "> 50 mm"]],
        "leads": [[0, 2, "1 – 2"], [2, 4, "3 – 4"], [4, 10, "5 – 10"], [10, 40, "11 – 40"], [40, 9999, "> 40"]],
        "ld": [[0, 0.5, "≤ 0.5 mm"], [0.5, 0.7, "0.5 – 0.7 mm"], [0.7, 9, "> 0.7 mm"]],
    },
    "feeders": feeders,
    "rows": R,
}
json.dump(D, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
types = sorted({r["type"] for r in R}); notes = sorted({r["note"] for r in R if r.get("note")})
print("rows", len(R), "feeders", len(feeders), "types", len(types), types, "notes", notes)
from collections import Counter
print(Counter(r["src"] for r in R), Counter(r["status"] for r in R), Counter(r["pack"] for r in R))
