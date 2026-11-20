#!/usr/bin/env python3
"""Create a new kit folder from templates/kit.
usage: new_kit.py <work_dir>/<product>-kit --name "SMT Printer Squeegee" --slug SM-Printer-Squeegee --prefix SM-SQ
Creates: facts.md, models.py, kit.yaml, sources/ assets/ img/raw/ out/ quote/ landing-src/ + example spec/video json."""
import os, sys, shutil, argparse, datetime
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
ap = argparse.ArgumentParser(); ap.add_argument("kit"); ap.add_argument("--name", required=True); ap.add_argument("--slug", required=True); ap.add_argument("--prefix", default="SM-XX")
a = ap.parse_args(); k = a.kit
if os.path.exists(k) and os.listdir(k): sys.exit(f"STOP: {k} exists and is not empty")
shutil.copytree(os.path.join(root, "templates", "kit"), k, dirs_exist_ok=True)
for d in ("sources", "extract", "assets", "img/raw", "out/video", "out/quote", "landing/i18n", "landing/photos", "landing-src/tr"): os.makedirs(os.path.join(k, d), exist_ok=True)
y = open(os.path.join(root, "config", "config.example.yaml"), encoding="utf-8").read()
y = y.replace('"SMT Stencil Wiping Paper Rolls"', f'"{a.name}"').replace('"SM-Stencil-Wiping-Paper"', f'"{a.slug}"').replace('"SM-WP"', f'"{a.prefix}"')
open(os.path.join(k, "kit.yaml"), "w", encoding="utf-8").write(y)
today = datetime.date.today().isoformat()
open(os.path.join(k, "facts.md"), "w", encoding="utf-8").write(f"""# {a.name} - facts ({today})
Internal only. Every fact has a source tag; conflicts stay "to be confirmed".

## Sources
| tag | file / listing | shop (internal) | card price CNY | notes |
|---|---|---|---|---|

## Product facts
| fact | value | source | status |
|---|---|---|---|

## Printer / machine fit (original models kept)
| brand | model text | size / part no. | source |
|---|---|---|---|

## Conflicts and open points
1.
""")
open(os.path.join(k, "models.py"), "w", encoding="utf-8").write(f'''# {a.name} - SKU list ({today}). Facts: facts.md. Original machine models kept as compatibility text.
# cny = price basis (shop named in kit.yaml), None until confirmed. USD rule in usd().
GROUPS = {{"A": "Group A"}}
ROWS = [
    # dict(group="A", code="{a.prefix}-001", brand="DEK", model="Horizon / Galaxy", size="", opening="", cny=None, status="listed", src="A"),
]
def usd(cny, markup=2.0, fx=6.6):
    return None if cny is None else int(round(cny * markup / fx))
''')
print("kit created:", k); print("next: put Taobao PDFs in sources/, fill facts.md, then follow SKILL.md step 2")
