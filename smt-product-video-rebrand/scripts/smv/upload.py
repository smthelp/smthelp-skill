"""Upload final/<batch> deliverables to Google Drive with the gws CLI (Hark: pass the google credential).
Usage: python3 upload.py <drive_folder_id> [slug ...]       -> mp4 + srt + thumbnail per slug (skips names already logged)
       python3 upload.py <drive_folder_id> --replace <slug> -> overwrite the logged file ids in place (same links)
       python3 upload.py <drive_folder_id> --doc            -> copy.html as a Google Doc
Log: final/<batch>/uploads.json (name -> file id)."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg

FOLDER = sys.argv[1]
LOG = os.path.join(cfg.OUT, 'uploads.json')
done = json.load(open(LOG)) if os.path.exists(LOG) else {}


def save():
    json.dump(done, open(LOG, 'w'), indent=1)


def gws(args):
    r = subprocess.run(['gws'] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-800:])
    return json.loads(r.stdout[r.stdout.index('{'):])


def up(path):
    name = os.path.basename(path)
    if name in done: return done[name]
    j = gws(['drive', '+upload', path, '--parent', FOLDER])
    done[name] = j['id']; save(); print('OK', name, j['id']); return j['id']


def replace(path):
    name = os.path.basename(path)
    j = gws(['drive', 'files', 'update', '--params', json.dumps({'fileId': done[name], 'fields': 'id,size'}), '--upload', path])
    print('REPLACED', name, j)


args = sys.argv[2:]
if args[:1] == ['--doc']:
    title = cfg.P.get('doc_title', f"{cfg.PRODUCT['model']} YouTube Video Copy - {cfg.BATCH}")
    j = gws(['drive', 'files', 'create', '--json', json.dumps({'name': title, 'mimeType': 'application/vnd.google-apps.document', 'parents': [FOLDER]}),
             '--params', '{"fields":"id,webViewLink"}', '--upload', os.path.join(cfg.OUT, 'copy.html')])
    done[title] = j['id']; save(); print('DOC', j.get('webViewLink'))
elif args[:1] == ['--replace']:
    for s in args[1:]:
        for k in ('mp4', 'srt', 'thumb'):
            replace(os.path.join(cfg.OUT, cfg.out_name(s, k)))
else:
    slugs = args or [v['slug'] for v in cfg.VIDEOS]
    for s in slugs:
        for k in ('mp4', 'srt', 'thumb'):
            p = os.path.join(cfg.OUT, cfg.out_name(s, k))
            up(p) if os.path.exists(p) else print('MISSING', p)
