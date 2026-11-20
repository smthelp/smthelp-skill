# SM stencil wiping paper rolls - SKU list (2026-11-19). Facts and sources: ../facts.md (listing ids A-J).
# Printer column keeps the ORIGINAL printer brand / model text as a compatibility identifier only.
# Size = core (tube) length x paper width x roll length (VERIFIED: listing drawings "管长 / 纸宽 / 纸长").
# SM code: SM-WP-<tube mm>-<paper width mm>-<length m>[-<opening>]
#   opening: X = cross slot, S = straight slot, G = 12 inner grooves, P = paper tube, R = plain round (no slot);
#   small cores add the core ID (S8 = straight slot, 8 mm core); no suffix = opening to be confirmed with the customer's old roll.
#   Sheets: SM-WP-SH-<w>x<h>-<pcs>;  width-only rolls (tube to order): SM-WP-W<width>-<length m>.
# cny = purchase / price basis, left None until Jason decides the basis.  USD = round(CNY x 2 / 6.6).
# status: "listed" = in >= 1 market size list; "table" = only in the reference size table (A i-028); "single" = one listing only.

GROUPS = {
    "A": "Rolls for GKG, Desen, Zhengshi and other 410 mm printers",
    "B": "Rolls for DEK printers (530 mm core)",
    "C": "Rolls for MPM printers (455 mm core)",
    "D": "Rolls for other printer brands",
    "E": "Large, width-only and sheet formats",
}

# group, printer brand, printer model / fit text (original), tube, width, length_m, core_id_mm, opening, status, sources, note
_RAW = [
    # --- A: 410 mm core ---
    ("A", "GKG / Desen", "GKG / Desen", 410, 140, 10, 20, "", "single", "A", "narrow width, one listing only"),
    ("A", "GKG / Desen / Zhengshi", "GKG G5 / Desen / Zhengshi", 410, 200, 10, 20, "X", "listed", "A C D F G H", ""),
    ("A", "GKG / Desen / Zhengshi", "GKG G5 / Desen / Zhengshi", 410, 250, 10, 20, "X", "listed", "A B C D F G H I", ""),
    ("A", "GKG / Desen / Zhengshi", "GKG / Desen / Zhengshi", 410, 275, 10, 20, "X", "single", "D", ""),
    ("A", "GKG / Desen / Zhengshi", "GKG G5 / Desen / Zhengshi", 410, 300, 10, 20, "X", "listed", "A B C D E F G H I J", ""),
    ("A", "GKG / Desen / Zhengshi", "GKG G5 / Desen / Zhengshi", 410, 350, 10, 20, "X", "listed", "A B C D E F G H I J", "data-sheet size (A i-023)"),
    ("A", "GKG / Desen / Zhengshi", "GKG G5 / Desen / Zhengshi", 410, 380, 10, 20, "X", "listed", "A B C D F G H I J", ""),
    ("A", "GKG / Desen / Zhengshi", "GKG / Desen / Zhengshi", 410, 395, 10, 20, "X", "single", "D", ""),
    ("A", "GKG / Desen / Zhengshi", "GKG G5 / Desen / Zhengshi", 410, 400, 10, 20, "X", "listed", "A B C E F G H I J", ""),
    ("A", "GKG", "GKG G9", 460, 300, 10, None, "", "listed", "A C F H", "opening TBC"),
    ("A", "GKG", "GKG G9", 460, 400, 10, None, "", "listed", "A C F H", "opening TBC"),
    ("A", "Nitto / Huancheng / Zhengshi", "Nitto / Huancheng / Zhengshi", 410, 350, 10, None, "", "listed", "A C", "opening TBC"),
    ("A", "Hetian Gude", "Hetian Gude", 410, 350, 10, None, "S", "single", "E", ""),
    ("A", "Hetian Gude", "Hetian Gude", 520, 350, 10, None, "S", "listed", "A C", ""),
    ("A", "Hetian Gude", "Hetian Gude", 520, 380, 10, None, "S", "single", "E", ""),
    # --- B: DEK ---
    ("B", "DEK", "DEK", 530, 200, 10, 20, "S", "single", "D", ""),
    ("B", "DEK", "DEK", 530, 250, 10, 20, "S", "listed", "D F I; table", ""),
    ("B", "DEK", "DEK", 530, 300, 10, 20, "S", "listed", "A B C D E F G H I J", ""),
    ("B", "DEK", "DEK", 530, 350, 10, 20, "S", "listed", "A B C D E F G H I J", ""),
    ("B", "DEK", "DEK", 530, 380, 10, 20, "S", "listed", "D G H J", ""),
    ("B", "DEK", "DEK", 530, 400, 10, 20, "S", "listed", "A B C E F G H I J; table", ""),
    ("B", "DEK", "DEK", 530, 450, 10, 20, "S", "listed", "A C D F G H I J", ""),
    ("B", "DEK", "DEK", 530, 490, 10, 20, "S", "single", "I; table", ""),
    ("B", "DEK", "DEK", 530, 500, 10, 20, "S", "listed", "A B C D E G H I J; table", ""),
    ("B", "DEK", "DEK", 530, 510, 10, 20, "S", "single", "G; table", ""),
    # --- C: MPM ---
    ("C", "MPM", "MPM", 455, 200, 10, 19.5, "G", "single", "D", ""),
    ("C", "MPM", "MPM", 455, 250, 10, 19.5, "G", "single", "D; table", ""),
    ("C", "MPM", "MPM", 455, 275, 10, 19.5, "G", "single", "D", ""),
    ("C", "MPM", "MPM", 455, 300, 10, 19.5, "G", "listed", "A C D E F G H J; table", ""),
    ("C", "MPM", "MPM", 455, 330, 10, 19.5, "G", "table", "table", ""),
    ("C", "MPM", "MPM", 455, 350, 10, 19.5, "G", "listed", "D E F G J; table", ""),
    ("C", "MPM", "MPM", 455, 380, 10, 19.5, "G", "single", "D", ""),
    ("C", "MPM", "MPM", 455, 400, 10, 19.5, "G", "listed", "A E F J; table", ""),
    ("C", "MPM", "MPM", 455, 445, 10, 19.5, "G", "single", "D", ""),
    ("C", "MPM", "MPM", 455, 450, 10, 19.5, "G", "listed", "A B C F H", ""),
    # --- D: other brands ---
    ("D", "EKRA", "EKRA", 450, 400, 10, None, "", "single", "C", "conflicts with table 400 x 300/400, core 13.5"),
    ("D", "EKRA", "EKRA (reference table)", 400, 300, 10, 13.5, "S", "table", "table", ""),
    ("D", "EKRA", "EKRA (reference table)", 400, 400, 10, 13.5, "S", "table", "table", ""),
    ("D", "Panasonic", "Panasonic", 350, 350, 10, 38, "P", "listed", "A B C E; table", ""),
    ("D", "Panasonic", "Panasonic SP28", 360, 350, 10, None, "", "single", "H", "opening TBC"),
    ("D", "Yamaha", "Yamaha", 360, 350, 10, 25.5, "P", "listed", "B C E; table", "A lists 350 x 350"),
    ("D", "Yamaha", "Yamaha (reference table)", 420, 400, 10, 25.5, "P", "table", "table", ""),
    ("D", "Hitachi", "Hitachi", 360, 300, 10, 30, "P", "single", "E; table", ""),
    ("D", "MINAMI", "MINAMI", 290, 270, 15, 8, "S", "listed", "C E", "15 m in C/E listings, 10 m in A/B/table - TBC"),
    ("D", "MINAMI", "MINAMI", 290, 270, 10, 8, "S", "listed", "A B; table", "see 15 m row"),
    ("D", "MINAMI", "MINAMI (reference table)", 410, 350, 10, 8, "S", "table", "table", ""),
    ("D", "JUKI", "JUKI (reference table)", 270, 260, 15, 38, "R", "table", "table", ""),
    ("D", "JUKI", "JUKI (reference table)", 353, 345, 15, 38, "R", "table", "table", ""),
    ("D", "JUKI", "JUKI (reference table)", 408, 400, 8, 38, "R", "table", "table", ""),
    ("D", "JUKI", "JUKI (reference table)", 535, 520, 12, 38, "R", "table", "table", ""),
    ("D", "FUJI", "FUJI (reference table)", 500, 500, 15, 26, "P", "table", "table", ""),
    ("D", "KME", "KME (reference table)", 480, 480, 20, 38, "P", "table", "table", ""),
    ("D", "SONY", "SONY (reference table)", 280, 260, 20, 20, "S", "table", "table", ""),
    # --- E: large / width-only / sheets ---
    ("E", "GKG / DEK / Desen", "Large-format printers", 620, 600, 10, 20, "", "listed", "A B C H", "opening TBC"),
]
_WIDTH_ONLY = [250, 300, 350, 380, 400, 450, 490, 500, 600, 680]   # J, 10 m, tube to order (850 also listed - TBC)


def code(tube, width, length, opening="", core=None):
    c = f"SM-WP-{tube}-{width}-{length}"
    if core and core < 19: opening += str(int(core))      # small cores (MINAMI 8, EKRA 13.5) get the core size
    return c + (f"-{opening}" if opening else "")


OPENING = {"X": "cross slot", "S": "straight slot", "G": "12 inner grooves", "P": "paper tube", "R": "plain round, no slot", "": "to be confirmed"}

ROWS = []
for g, brand, model, tube, width, length, core, op, status, src, note in _RAW:
    ROWS.append(dict(group=g, code=code(tube, width, length, op, core), brand=brand, model=model, tube=tube, width=width,
                     length_m=length, core_id=core, opening=OPENING[op], status=status, sources=src, note=note,
                     size=f"{tube} x {width} mm x {length} m", cny=None))
for w in _WIDTH_ONLY:
    ROWS.append(dict(group="E", code=f"SM-WP-W{w}-10", brand="Universal", model="Width-only roll, core to order", tube=None, width=w,
                     length_m=10, core_id=None, opening="to order", status="single", sources="J", note="state tube length and opening",
                     size=f"{w} mm x 10 m", cny=None))
ROWS.append(dict(group="E", code="SM-WP-SH-200x200-10", brand="Universal", model="Manual wiping sheets", tube=None, width=200,
                 length_m=None, core_id=None, opening="-", status="single", sources="G", note="200 x 200 mm, 10 sheets per pack",
                 size="200 x 200 mm, 10 sheets", cny=None))


def usd(cny):
    return None if cny is None else int(round(cny * 2 / 6.6))


if __name__ == "__main__":
    codes = [r["code"] for r in ROWS]
    dup = {c for c in codes if codes.count(c) > 1}
    for r in ROWS:
        print(f'{r["group"]} {r["code"]:24} {r["model"]:30} {r["size"]:24} core {r["core_id"]} {r["opening"]:18} {r["status"]:7} {r["sources"]}')
    print(len(ROWS), "rows; duplicate codes:", dup or "none")
