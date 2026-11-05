#!/usr/bin/env python3
"""smt-3d-animation-landing-kit command line.

  python3 scripts/smt3d.py <command> <job.json> [options]

Commands (run in this order; every step is idempotent and can be re-run):
  init <dir> [--example stf1003-tube-feeder]  scaffold a new job folder from an example
  validate <job>        check job.json/content.json against the contract (languages, blogs, formats, files)
  fetch <job>           download inputs (3D drawing, pages, docs) into <work>/src
  analyze <job>         dump structure + selling points of the pages/docs to <work>/build/analysis.md
  mesh <job>            3D drawing -> lightweight model (extract_mesh + pack_mesh) at job.model
  lp <job>              build the single-file landing page            -> <work>/out/<slug>.html
  verify <job>          automated checklist on the built page          -> <work>/out/verify/verify_report.json
  i18n-todo <job> <lang> write the untranslated keys for a language     -> <work>/build/i18n_todo_<lang>.json
  stage <job>           copy video/thumb stages + duel.js + assets into <work>/build
  tts <job> | timeline <job> | audio <job>   narration, subtitles, music mix
  render <job> <169|916> [--budget 1000]     render missing segments until the time budget (s) is used
  finish <job> <169|916>                     concat segments + audio -> final 4K MP4
  thumbs <job>          thumbnails + Shorts cover
  seo <job>             YouTube title / description / chapters / tags   -> <work>/out/youtube-seo-<slug>.txt
  drive <job>           create the Drive folder and upload <work>/out deliverables (needs `gws` + Google connector)
  all <job>             validate fetch analyze mesh lp verify stage tts timeline audio thumbs seo (render/finish separately)
"""
import os, sys, json, re, glob, shutil, subprocess, time, html, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from common import load_job, W, SKILL

HERE = os.path.dirname(os.path.abspath(__file__))
def py(script, *args):
    r = subprocess.run([sys.executable, os.path.join(HERE, script), *map(str, args)])
    if r.returncode: sys.exit(f'{script} failed ({r.returncode})')

def cmd_init(d, example='stf1003-tube-feeder'):
    src = os.path.join(SKILL, 'examples', example)
    if os.path.exists(d) and os.listdir(d): sys.exit(f'{d} is not empty')
    shutil.copytree(src, d, ignore=shutil.ignore_patterns('_work'))
    print(f'new job at {d}: edit job.json, content.json, script.json, duel.js, video.html, thumb.html, i18n/*.json')

def cmd_validate(job):
    cfg = job['_cfg']; P = job['_P']; errs, warns = [], []
    for k in ['name', 'slug', 'content']:
        if not job.get(k): errs.append(f'job.{k} missing')
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', job.get('slug', '')): errs.append('slug must be kebab-case ascii')
    C = json.load(open(P(job['content']), encoding='utf8')) if job.get('content') and os.path.exists(P(job['content'])) else None
    if C is None: errs.append('content file not found')
    else:
        for k in ['meta', 'hero', 'contact']:
            if k not in C: errs.append(f'content.{k} missing')
        n = len(C.get('blogs', {}).get('items', []))
        if n != cfg['blog_count']: errs.append(f'content.blogs.items = {n}, config.blog_count = {cfg["blog_count"]}')
        if 'roi' not in (job.get('sections') or cfg['sections']): warns.append('roi section not in sections list')
        for s in C.get('gallery', {}).get('items', []) + C.get('hero', {}).get('images', []):
            if '://' not in s['src'] and not os.path.exists(P(s['src'])): errs.append('missing image ' + s['src'])
    if cfg['default_language'] not in cfg['languages']: errs.append('default_language not in languages')
    if len(cfg['languages']) != 7: warns.append(f'{len(cfg["languages"])} languages configured (spec default is 7)')
    fmt = cfg['model']['preferred_format']
    if fmt not in cfg['model']['accepted_formats']: errs.append(f'model.preferred_format {fmt} not accepted')
    d3 = job.get('inputs', {}).get('drawing_3d', '')
    ext = 'edrawings-html' if d3.lower().endswith(('.html', '.htm')) else d3.lower().rsplit('.', 1)[-1]
    if d3 and ext not in cfg['model']['accepted_formats']: errs.append(f'3D input format {ext} not in model.accepted_formats')
    if job.get('duel'):
        if not os.path.exists(P(job['duel']['script'])): errs.append('duel script missing')
        if C and len(C.get('duel', {}).get('chapters', [])) == 0: errs.append('content.duel.chapters empty')
    if job.get('video') and not os.path.exists(P(job['video']['script'])): errs.append('video.script missing')
    for e in errs: print('ERROR', e)
    for w in warns: print('WARN ', w)
    print('valid' if not errs else f'{len(errs)} error(s)'); return not errs

def _get(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 0: return dst
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    open(dst, 'wb').write(urllib.request.urlopen(req, timeout=180).read()); return dst

def _src_name(url, i, kind):
    base = urllib.request.unquote(url.split('?')[0].rstrip('/').split('/')[-1]) or f'{kind}{i}'
    return re.sub(r'[^A-Za-z0-9._-]+', '_', base)[-90:]

def cmd_fetch(job):
    I = job.get('inputs', {}); P = job['_P']; got = {}
    items = ([('drawing', I['drawing_3d'])] if I.get('drawing_3d') else []) + [('page', u) for u in I.get('pages', [])] + [('doc', u) for u in I.get('docs', [])]
    for i, (kind, u) in enumerate(items):
        dst = W(job, 'src', f'{kind}_{_src_name(u, i, kind)}')
        if '://' in u: _get(u, dst)
        else: shutil.copy(P(u), dst)
        got.setdefault(kind, []).append(dst); print(kind, os.path.getsize(dst), dst)
    json.dump(got, open(W(job, 'src', 'manifest.json'), 'w'), indent=1)

def cmd_analyze(job):
    man = json.load(open(W(job, 'src', 'manifest.json'))); out = ['# Source analysis — ' + job['name'], '']
    for f in man.get('page', []):
        s = open(f, encoding='utf8', errors='ignore').read()
        t = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
        out += [f'## Page: {os.path.basename(f)}', 'Title: ' + ' '.join(re.findall(r'<title>(.*?)</title>', s, re.S))[:200],
                'Sections: ' + ', '.join(re.findall(r'<section[^>]*id="([^"]+)"', s)),
                'Headings: ' + ' | '.join(html.unescape(re.sub('<[^>]+>', '', h)).strip() for h in re.findall(r'<h[12][^>]*>(.*?)</h[12]>', t, re.S))[:1500],
                'Images: ' + ', '.join(sorted(set(re.findall(r'https://ph\.smthelp\.com/images/[^"\' )]+', s)))[:20]),
                'YouTube: ' + ', '.join(sorted(set(re.findall(r'(?:embed/|watch\?v=|youtu\.be/|vi/)([A-Za-z0-9_-]{11})', s)))),
                'Docs: ' + ', '.join(sorted(set(u for u in re.findall(r'https?://[^"\' ]+\.pdf', s)))[:10]),
                'Contacts: ' + ', '.join(sorted(set(re.findall(r'mailto:[^"?]+|wa\.me/\d+|tel:[+\d ]+', s)))), '']
    for f in man.get('doc', []):
        if f.lower().endswith('.pdf') and shutil.which('pdftotext'):
            txt = subprocess.run(['pdftotext', '-layout', f, '-'], capture_output=True, text=True).stdout
            open(W(job, 'build', os.path.basename(f) + '.txt'), 'w').write(txt)
            out += [f'## Document: {os.path.basename(f)}', '```', txt[:6000], '```', '']
            if shutil.which('pdfimages'):
                d = W(job, 'assets', 'pdf'); os.makedirs(d, exist_ok=True); subprocess.run(['pdfimages', '-png', f, os.path.join(d, 'i')])
    out += ['## Selling-point worksheet (fill in content.json from this)', '- Pain (customer words) → Feature (spec + source) → Advantage → Benefit',
            '- Every number must come from a spec sheet / manual / PDF; record conflicts and which source wins.', '']
    open(W(job, 'build', 'analysis.md'), 'w', encoding='utf8').write('\n'.join(out)); print('analysis ->', W(job, 'build', 'analysis.md'))

def cmd_mesh(job):
    man = json.load(open(W(job, 'src', 'manifest.json'))); src = (man.get('drawing') or [None])[0]
    if not src: sys.exit('no inputs.drawing_3d')
    mc = job['_cfg']['model']; dst = job['_P'](job.get('model', 'assets/model.b64')); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if src.lower().endswith(('.html', '.htm')):
        py('extract_mesh.py', src, W(job, 'build', 'mesh'), '--wait', 25); mj = W(job, 'build', 'mesh', 'mesh.json')
    else: mj = src
    args = [mj, dst, '--budget', mc['triangle_budget']]
    if job.get('model_groups'): args += ['--groups', job['_P'](job['model_groups'])]
    py('pack_mesh.py', *args)

def cmd_stage(job):
    P = job['_P']; V = job.get('video', {})
    for name, key in [('video.html', 'stage'), ('thumb.html', 'thumb')]:
        src = P(V[key]) if V.get(key) else (P(name) if os.path.exists(P(name)) else os.path.join(SKILL, 'templates', 'video', name))
        shutil.copy(src, W(job, 'build', name))
    if job.get('duel'): shutil.copy(P(job['duel']['script']), W(job, 'build', 'duel.js'))
    for f in glob.glob(os.path.join(job['_root'], 'assets', '*')):
        dst = W(job, 'assets', os.path.basename(f))
        if os.path.abspath(f) != os.path.abspath(dst) and not os.path.exists(dst): shutil.copy(f, dst)
    print('stage ready in', W(job, 'build'))

def cmd_render(job, fmt, budget=1000):
    TL = json.load(open(W(job, 'video', 'timeline.json'))); seg = job['_cfg']['video']['segment_seconds']; t0 = time.time()
    starts = [round(x * seg, 2) for x in range(int(TL['total'] // seg) + 1) if x * seg < TL['total']]
    for s in starts:
        out = W(job, 'out', f'seg_{fmt}_{s:g}.mp4')
        if os.path.exists(out + '.done'): continue
        est = seg * job['_cfg']['video']['fps'] * 0.5
        if time.time() - t0 + est > budget: print('budget used; run render again to continue'); return
        py('render.py', job['_jobfile'], fmt, f'{s:g}', f'{min(s + seg, TL["total"]):g}')
    print('all segments rendered for', fmt)

def cmd_seo(job):
    S = job.get('seo', {}); TL = json.load(open(W(job, 'video', 'timeline.json'))); B = job['_cfg']['brand']
    def mmss(t): return f'{int(t // 60)}:{int(t % 60):02d}'
    ch = S.get('chapters', {}); lines = []
    for sc in TL['scenes']:
        if sc['id'] in ch: lines.append(f"{'0:00' if not lines else mmss(sc['start'])} {ch[sc['id']]}")
    lp = S.get('landing_url', '')
    desc = '\n'.join([S.get('intro', ''), '', 'What you will see:', *['• ' + b for b in S.get('bullets', [])], '', 'Chapters', *lines, '',
                      *(['Interactive page (3D model, animation, ROI, 7 languages):', lp] if lp else []), *S.get('links', []), '',
                      f'WhatsApp: https://wa.me/{B["whatsapp"]} ({B["phone"]})', f'Email: {B["email"]}', f'Website: {B["website"]}', '',
                      *[f'{k.capitalize()}: {v}' for k, v in B['social'].items()], '', ' '.join(S.get('hashtags', []))])
    tags = ', '.join(S.get('tags', []))
    warn = [w for w, c in [('title > 100 chars', len(S.get('title', '')) > 100), ('tags > 500 chars', len(tags) > 500), ('shorts title > 100', len(S.get('short_title', '')) > 100)] if c]
    txt = f"""YOUTUBE PUBLISHING KIT — {job['name']}\n\n1) LONG-FORM 16:9 4K\nTITLE ({len(S.get('title',''))} chars)\n{S.get('title','')}\n\nALTERNATIVE TITLES\n""" + \
          '\n'.join('- ' + t for t in S.get('alt_titles', [])) + f"\n\nDESCRIPTION\n{desc}\n\nTAGS ({len(tags)} chars)\n{tags}\n\n2) SHORTS 9:16 4K\nTITLE\n{S.get('short_title','')}\n\nDESCRIPTION\n{S.get('short_desc','')}\n"
    out = W(job, 'out', f"youtube-seo-{job['slug']}.txt"); open(out, 'w', encoding='utf8').write(txt)
    print('seo ->', out, ('WARN ' + ', '.join(warn)) if warn else '')

def cmd_drive(job):
    if not shutil.which('gws'): sys.exit('gws CLI not found: upload <work>/out manually or run inside Hark with the Google connector')
    D = job['_cfg']['drive']; name = job.get('drive', {}).get('folder_name', job['name']) + time.strftime(' (%Y-%m-%d)')
    r = subprocess.run(['gws', 'drive', 'files', 'create', '--params', '{"fields":"id,name"}', '--json',
                        json.dumps({'name': name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [D['parent_folder_id']]})], capture_output=True, text=True)
    fid = json.loads(r.stdout)['id']; print('folder', fid)
    for f in sorted(glob.glob(W(job, 'out', '*'))):
        if re.search(r'seg_|\.done$|\.txt\.tmp$', f) or os.path.isdir(f): continue
        subprocess.run(['gws', 'drive', '+upload', f, '--parent', fid], capture_output=True); print('uploaded', os.path.basename(f))
    json.dump({'folder_id': fid, 'name': name}, open(W(job, 'out', 'drive.json'), 'w'))

def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(0)
    c = sys.argv[1]
    if c == 'init': return cmd_init(sys.argv[2], *(sys.argv[4:5] if '--example' in sys.argv else []))
    jf = sys.argv[2]; job = load_job(jf); job['_jobfile'] = jf
    if c == 'validate': sys.exit(0 if cmd_validate(job) else 1)
    elif c == 'fetch': cmd_fetch(job)
    elif c == 'analyze': cmd_analyze(job)
    elif c == 'mesh': cmd_mesh(job)
    elif c == 'lp': py('build_lp.py', jf)
    elif c == 'verify': py('verify_lp.py', W(job, 'out', job['slug'] + '.html'), '--job', jf, '--shots', W(job, 'out', 'verify'))
    elif c == 'i18n-todo':
        en = json.load(open(W(job, 'build', 'i18n_en_keys.json'), encoding='utf8')); l = sys.argv[3]
        have = {}
        if job.get('i18n_dir') and os.path.exists(os.path.join(job['_P'](job['i18n_dir']), l + '.json')): have = json.load(open(os.path.join(job['_P'](job['i18n_dir']), l + '.json'), encoding='utf8'))
        todo = {k: v for k, v in en.items() if k not in have}; out = W(job, 'build', f'i18n_todo_{l}.json')
        json.dump(todo, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=0); print(len(todo), 'keys to translate ->', out)
    elif c == 'stage': cmd_stage(job)
    elif c == 'tts': py('tts.py', jf)
    elif c == 'timeline': py('timeline.py', jf)
    elif c == 'audio': py('audio_mix.py', jf)
    elif c == 'render': cmd_render(job, sys.argv[3], int(sys.argv[sys.argv.index('--budget') + 1]) if '--budget' in sys.argv else 1000)
    elif c == 'finish': py('finish_video.py', jf, sys.argv[3])
    elif c == 'thumbs': py('thumbs.py', jf)
    elif c == 'seo': cmd_seo(job)
    elif c == 'drive': cmd_drive(job)
    elif c == 'all':
        if not cmd_validate(job): sys.exit(1)
        for step in [cmd_fetch, cmd_analyze, cmd_mesh]: step(job)
        py('build_lp.py', jf); py('verify_lp.py', W(job, 'out', job['slug'] + '.html'), '--job', jf, '--shots', W(job, 'out', 'verify'))
        cmd_stage(job); py('tts.py', jf); py('timeline.py', jf); py('audio_mix.py', jf); py('thumbs.py', jf); cmd_seo(job)
        print('next: smt3d.py render <job> 169 ; finish <job> 169 ; render <job> 916 ; finish <job> 916 ; drive <job>')
    else: print(__doc__); sys.exit(2)

if __name__ == '__main__': main()
