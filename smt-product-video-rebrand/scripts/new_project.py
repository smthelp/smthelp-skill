#!/usr/bin/env python3
"""Scaffold a new product video project.
Usage: python3 new_project.py <project_dir> --model "X3100" --name "X-ray SMD component counter" --prefix x3100-x-ray-smd-counter
Then: copy source clips into <project_dir>/source/, catalog them (catalog.sh), fill content/shots.py,
content/facts.md and content/batch1.py (see references/method.md)."""
import argparse, json, os, shutil
SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('dir'); ap.add_argument('--model', required=True); ap.add_argument('--name', required=True)
ap.add_argument('--prefix', required=True); ap.add_argument('--series', default='SMART EMS')
a = ap.parse_args()
os.makedirs(a.dir + '/source', exist_ok=True); os.makedirs(a.dir + '/content', exist_ok=True)
pj = json.load(open(SK + '/config/project.example.json'))
pj['product'].update(model=a.model, name=a.name, chip=f'{a.series} {a.model}'.strip(),
                     tag=f'{a.series} {a.model}  ·  {a.name.upper()}'.strip())
pj['product']['outro_line'] = f"{a.series} {a.model} {a.name}  ·  Shenzhen Southern Machinery, since 2011".strip()
pj['file_prefix'] = a.prefix
pj['utm_prefix'] = a.model.lower()
pj.update(primary_keyword=a.name.lower(), landing_page='TODO: product landing page URL',
          landing_label=f'{a.model} specifications, FAQ and quotation request', default_intro_shot=['A1', 1.0],
          desc_disclaimer='Specifications follow the product brochure. Price and lead time are quoted per order.',
          pronunciations=[], example_only_patterns=['\\d+(\\.\\d+)? ?%'], drive_folder_id='',
          doc_title=f'{a.model} YouTube Video Copy - Batch 1')
pj.pop('_doc', None)
json.dump(pj, open(a.dir + '/project.json', 'w'), indent=2, ensure_ascii=False)
for f in ('shots.py', 'batch1.py', 'facts.md'):
    shutil.copy(f'{SK}/templates/{f}', f'{a.dir}/content/{f}')
print('created', a.dir)
