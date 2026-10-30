"""Build YouTube SRT captions from the caption chunks the renderer computed (timeline_l.json / timeline_p.json,
written by preview.py on setupVideo). Usage: python make_srt.py <product-code>  (run in build/)"""
import json, sys, os
code = sys.argv[1] if len(sys.argv) > 1 else 'PRODUCT'

def ts(x):
    ms = int(round(x * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"

os.makedirs('../deliverables', exist_ok=True)
for k, f in (('16x9', 'timeline_l.json'), ('9x16', 'timeline_p.json')):
    if not os.path.exists(f):
        continue
    ch = json.load(open(f))['chunks']; out = []
    for i, c in enumerate(ch, 1):
        b = min(c['b'], ch[i]['a'] - 0.01) if i < len(ch) else c['b']
        out.append(f"{i}\n{ts(c['a'])} --> {ts(b)}\n{c['text']}\n")
    open(f'../deliverables/{code}_{k}_EN.srt', 'w').write('\n'.join(out))
    print(k, len(ch), 'cues')
