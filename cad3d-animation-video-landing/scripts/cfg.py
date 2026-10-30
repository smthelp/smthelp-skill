"""Read PROJ/product.json and print shell `export` lines for the pipeline.
Usage: eval "$(python3 scripts/cfg.py /path/to/product.json)" """
import json, sys, shlex
c = json.load(open(sys.argv[1]))
g = lambda *k, d=None: (lambda v: v)(__import__('functools').reduce(lambda a, b: (a or {}).get(b), k, c) or d)
env = {
  'CODE': g('product', 'code', d='PRODUCT'),
  'DRAWING_URL': g('inputs', 'drawing', d=''), 'LANDING_URL': g('inputs', 'landing', d=''),
  'VOICE': g('voice', 'voice', d='en-US-AndrewMultilingualNeural'), 'VOICE_RATE': g('voice', 'rate', d='+2%'),
  'FPS': g('video', 'fps', d=24), 'R3D': g('video', 'render_scale_3d', d=0.6), 'R3D_L': g('video', 'render_scale_3d_landscape', d=0.6), 'R3D_P': g('video', 'render_scale_3d_portrait', d=0.5),
  'AA': g('video', 'antialias', d=0), 'SHARDS': g('video', 'shards', d=1),
  'CHUNK': g('video', 'chunk_seconds', d=1150), 'NSEG': g('video', 'segments', d=8),
  'ASPECTS': ' '.join(g('video', 'aspects', d=['l', 'p'])),
  'DRIVE_FOLDER': g('delivery', 'drive_folder_id', d=''), 'DRIVE_SUBFOLDER': g('delivery', 'subfolder', d=''),
}
for k, v in env.items(): print(f'export {k}={shlex.quote(str(v))}')
