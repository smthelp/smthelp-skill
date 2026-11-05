# page.py - product data consumed by scripts/build.py (executed with helpers in scope).
# Helpers: ph('2026/09/22/name.md.png') -> (thumb, full) on ph.smthelp.com; emb('key') -> inline image from emb.json;
#          V('i18n_key') -> table/spec cell rendered from i18n; EM (emb.json dict); en (English strings); CFG (merged config).
HERO = EM['hero'][0]; HERO_SIZE = tuple(EM['hero'][1])          # or a ph.smthelp.com URL and its size
STATION_IMG = {1: ph('2026/..../step1.md.webp')[0]}              # missing numbers fall back to STATION_ICON
STATION_ICON = {2: 'fa-lightbulb'}
TABLE_ROWS = [('MODEL-A', V('t_type_a'), '50 x 50 - 330 x 250', '1330 x 765 x 1250, 140 kg')]   # first cell bold
SPECS = [('sp_card_title', [('k_size', '1330 x 765 x 1250 mm', 'src_sheet'), ('k_power', V('v_power'), 'src_sheet')])]
DISC_COUNT = 3; DISC_TBC = [1]                                    # d1t/d1a/d1b/d1n ... ; rows flagged To be confirmed
GALLERY = [ph('2026/..../photo.md.png'), emb('photo2')]          # captions g1..gN
VIDEOS = ['YouTubeID1']                                           # titles v1t..vNt
CLIPS = ['GoogleDriveFileID']                                     # titles c1t..cNt (folder must be public)
DOWNLOADS = [('Product sheet', 'https://file.autoinsertion.com/public/...pdf', 'dl_pdf')]   # dl_pdf | dl_man | dl_3d
N_MODES = 1                                                       # procedural mode: number of md<n>_* keys
BLOG_ABOUT = 'product family'; CRUMB_SECTION = 'PCB Handling'; CRUMB_NAME = 'Product name'
PRODUCT_LD = {"@type": "Product", "name": "Product name", "brand": {"@type": "Brand", "name": "Southern Machinery"}}
TOOL_HTML = ''   # optional card under the 3D stage (selector, configurator)
TOOL_JS = ''     # its script; set window.__toolRefresh = fn to re-run on language change
