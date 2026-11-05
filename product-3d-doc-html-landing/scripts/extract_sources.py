#!/usr/bin/env python3
"""Extract text, tables, images and videos from product documents into <workdir>/sources/.

usage: python3 extract_sources.py <workdir> <file-or-dir> [...]
Supports: .pdf (pdftotext -layout, pdfimages -png), .pptx (slide text in order, ppt/media/* incl. mp4/glb),
          .docx (paragraphs + tables), .xlsx/.csv (rows), .md/.txt, images (copied), .mp4/.mov (copied + ffprobe).
Writes:   sources/<stem>/text.md, sources/<stem>/media/*, sources/inventory.json (every file, type, size, slide/page).
Then run contact_sheet.py to look at the pictures before choosing any.
"""
import sys, os, re, json, zipfile, subprocess, shutil, html, glob
W = os.path.abspath(sys.argv[1]); OUT = os.path.join(W, 'sources'); os.makedirs(OUT, exist_ok=True)
files = []
for a in sys.argv[2:]:
    files += sorted(glob.glob(os.path.join(a, '*'))) if os.path.isdir(a) else [a]
inv = []
def slug(s): return re.sub(r'[^A-Za-z0-9]+', '-', os.path.splitext(os.path.basename(s))[0]).strip('-')[:60]
for f in files:
    ext = f.rsplit('.', 1)[-1].lower(); d = os.path.join(OUT, slug(f)); md = os.path.join(d, 'media'); os.makedirs(md, exist_ok=True)
    rec = {'file': os.path.basename(f), 'type': ext, 'bytes': os.path.getsize(f), 'media': []}
    txt = ''
    if ext == 'pdf':
        txt = subprocess.run(['pdftotext', '-layout', f, '-'], capture_output=True, text=True).stdout
        subprocess.run(['pdfimages', '-png', '-p', f, os.path.join(md, 'p')])
    elif ext == 'pptx':
        z = zipfile.ZipFile(f)
        sl = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)], key=lambda n: int(re.findall(r'\d+', n)[-1]))
        for n in sl:
            x = z.read(n).decode('utf8', 'ignore')
            t = ' '.join(html.unescape(s) for s in re.findall(r'<a:t>([^<]*)</a:t>', x)).strip()
            txt += f'\n## {os.path.basename(n)}\n{t}\n'
        for i in z.infolist():
            if i.filename.startswith('ppt/media/') and i.file_size > 20000:
                open(os.path.join(md, os.path.basename(i.filename)), 'wb').write(z.read(i.filename))
    elif ext == 'docx':
        z = zipfile.ZipFile(f); x = z.read('word/document.xml').decode('utf8', 'ignore')
        for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
            t = ''.join(html.unescape(s) for s in re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
            if t.strip(): txt += t + '\n'
        for i in z.infolist():
            if i.filename.startswith('word/media/'): open(os.path.join(md, os.path.basename(i.filename)), 'wb').write(z.read(i.filename))
    elif ext in ('xlsx', 'csv'):
        if ext == 'csv': txt = open(f, encoding='utf8', errors='ignore').read()
        else:
            try:
                import openpyxl
                wb = openpyxl.load_workbook(f, data_only=True)
                for ws in wb: txt += f'\n## {ws.title}\n' + '\n'.join(' | '.join('' if c is None else str(c) for c in r) for r in ws.iter_rows(values_only=True))
            except ImportError: txt = '(install openpyxl to read xlsx)'
    elif ext in ('md', 'txt'): txt = open(f, encoding='utf8', errors='ignore').read()
    elif ext in ('png', 'jpg', 'jpeg', 'webp', 'gif'): shutil.copy(f, md)
    elif ext in ('mp4', 'mov', 'webm', 'm4v'): shutil.copy(f, md)
    elif ext in ('glb', 'gltf', 'stl', 'obj', 'step', 'stp', 'fbx'): shutil.copy(f, md); rec['model'] = True
    open(os.path.join(d, 'text.md'), 'w').write(f'# {rec["file"]}\n{txt}')
    for m in sorted(os.listdir(md)):
        p = os.path.join(md, m); r = {'name': m, 'bytes': os.path.getsize(p)}
        if m.lower().endswith(('.mp4', '.mov', '.webm', '.m4v')) and shutil.which('ffprobe'):
            r['probe'] = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=width,height', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.split()
        if m.lower().endswith(('.glb', '.gltf')): rec['model'] = True
        rec['media'].append(r)
    rec['chars'] = len(txt); inv.append(rec); print(rec['file'], rec['chars'], 'chars', len(rec['media']), 'media')
json.dump(inv, open(os.path.join(OUT, 'inventory.json'), 'w'), ensure_ascii=False, indent=1)
