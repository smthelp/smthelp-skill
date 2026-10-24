"""Configuration loader shared by every smv script.

Environment:
  SMV_PROJECT  project directory (required) - contains project.json, content/, source/
  SMV_BATCH    content module name in <project>/content (default: project.json default_batch)
Layout created under the project: tts/, build/<slug>/<tag>/, final/<batch>/
"""
import json, os, sys, importlib

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJ = os.path.abspath(os.environ.get('SMV_PROJECT', '.'))
if not os.path.exists(os.path.join(PROJ, 'project.json')):
    sys.exit(f'E01 project.json not found in SMV_PROJECT={PROJ}')


def _merge(a, b):
    for k, v in (b or {}).items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            _merge(a[k], v)
        else:
            a[k] = v
    return a


P = json.load(open(os.path.join(PROJ, 'project.json')))
B = _merge(json.load(open(os.path.join(SKILL, 'config', 'brand.json'))), P.get('brand_overrides'))
BATCH = os.environ.get('SMV_BATCH', P.get('default_batch', 'batch1'))

SRC = os.path.join(PROJ, P.get('source_dir', 'source')) + '/'
BUILD = os.path.join(PROJ, 'build')
TTS = os.path.join(PROJ, 'tts')
OUT = os.path.join(PROJ, 'final', BATCH)
for d in (BUILD, TTS, OUT):
    os.makedirs(d, exist_ok=True)

LOGO = os.path.join(PROJ, P['logo']) if P.get('logo') else os.path.join(SKILL, B['logo'])
FONT_DIR = os.path.join(SKILL, 'assets', 'fonts') + '/'
FPS = B['video']['fps']
W4, H4 = B['video']['width'], B['video']['height']
CONTACT = B['contact']

PRODUCT = P['product']            # dict: model, chip, tag, kicker_prefix, ...
PREFIX = P['file_prefix']        # e.g. x3100-x-ray-smd-counter


def fmt(s):
    """fill {placeholders} from contact / brand / product"""
    vals = dict(B); vals.update(CONTACT); vals.update(PRODUCT)
    return s.format(**{k: v for k, v in vals.items() if isinstance(v, (str, int, float))})


sys.path.insert(0, os.path.join(PROJ, 'content'))
content = importlib.import_module(BATCH)
VIDEOS = content.VIDEOS
SEO = content.SEO
OUTRO_TEXT = getattr(content, 'OUTRO_TEXT', fmt(P.get('outro_text', '')))
SLIDES = getattr(content, 'SLIDES', {})
shots_mod = importlib.import_module('shots')
SHOTS = shots_mod.SHOTS
HAS_CUSTOM_SLIDES = os.path.exists(os.path.join(PROJ, 'content', 'slides.py'))


def custom_slides():
    """content/slides.py, imported lazily (it imports gfx, which imports cfg)"""
    return importlib.import_module('slides') if HAS_CUSTOM_SLIDES else None


def out_name(slug, kind):
    """kind: mp4 | srt | thumb"""
    return {'mp4': f'{PREFIX}-{slug}-4k.mp4', 'srt': f'{PREFIX}-{slug}-4k.srt', 'thumb': f'{PREFIX}-{slug}-thumbnail.png'}[kind]
