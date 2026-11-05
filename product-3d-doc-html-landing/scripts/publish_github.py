#!/usr/bin/env python3
"""Push files to GitHub in ONE commit with the Git Data API (no git binary needed).

usage: GITHUB_TOKEN=... python3 publish_github.py owner/repo branch "commit message" <local_path>=<repo_path> [...]
  <local_path> may be a file or a directory (uploaded recursively under <repo_path>/).
Large files are fine (blobs are posted base64). Existing files at the same paths are replaced; nothing else is touched.
For the landing-page repo, re-fetch README.md and patch it before passing it here - never overwrite blindly.
"""
import os, sys, json, base64, urllib.request

repo, branch, msg = sys.argv[1], sys.argv[2], sys.argv[3]
TOK = os.environ.get('GITHUB_TOKEN', 'x')
API = f'https://api.github.com/repos/{repo}'

def req(method, path, body=None):
    r = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                               headers={'Authorization': f'Bearer {TOK}', 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(r, timeout=120) as f: return json.loads(f.read() or b'{}')

files = []
for spec in sys.argv[4:]:
    loc, dst = spec.split('=', 1)
    if os.path.isdir(loc):
        for root, _, names in os.walk(loc):
            for n in names:
                if n in ('.DS_Store',) or '__pycache__' in root: continue
                p = os.path.join(root, n); files.append((p, dst.rstrip('/') + '/' + os.path.relpath(p, loc).replace(os.sep, '/')))
    else:
        files.append((loc, dst))
ref = req('GET', f'/git/ref/heads/{branch}'); base = ref['object']['sha']
base_tree = req('GET', f'/git/commits/{base}')['tree']['sha']
tree = []
for p, dst in files:
    b = req('POST', '/git/blobs', {'content': base64.b64encode(open(p, 'rb').read()).decode(), 'encoding': 'base64'})
    tree.append({'path': dst, 'mode': '100755' if os.access(p, os.X_OK) and p.endswith(('.py', '.sh')) else '100644', 'type': 'blob', 'sha': b['sha']})
    print('blob', dst)
nt = req('POST', '/git/trees', {'base_tree': base_tree, 'tree': tree})
c = req('POST', '/git/commits', {'message': msg, 'tree': nt['sha'], 'parents': [base]})
req('PATCH', f'/git/refs/heads/{branch}', {'sha': c['sha']})
print('commit', c['sha'], len(files), 'files')
