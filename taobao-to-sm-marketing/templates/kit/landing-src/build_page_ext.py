#!/usr/bin/env python3
"""Product-local extension of smt-product-landing-page/scripts/build_page.py (v1.2.0) for the
SMT stencil wiping paper roll page (copied from squeegee-kit/landing-src/build_sq.py). Runs the skill
builder unchanged and adds, guarded by keys/flags:
* a Size selector section (mod_* / bh_* / op_* / sz_* keys): printer brand -> core length x paper widths,
  roll length and core opening (SIZE rows below, from models.py / facts.md)
* calc_mode "rolls": the payback calculator becomes a wiping-roll consumption planner
* videos with "embed": true are inlined once as base64 (window.__VE) and played through a Blob URL
usage: build_wp.py <product_dir> --out <dir>
"""
import sys, os, re, json as _json
SKILL = "/workspace/smthelp-skills-business/smt-product-landing-page/scripts/build_page.py"
# brand (literal, or i18n key when it starts with "@"), core mm, paper widths mm, roll, opening key
SIZE = [("GKG / Desen / Zhengshi", "410", "200 · 250 · 275 · 300 · 350 · 380 · 395 · 400", "10 m", "op_xc"),
        ("GKG G9", "460", "300 · 400", "10 m", "op_c"),
        ("Nitto / Huancheng / Zhengshi", "410", "350", "10 m", "op_c"),
        ("Hetian Gude", "520 / 410", "350 · 380 / 350", "10 m", "op_s"),
        ("DEK", "530", "200 · 250 · 300 · 350 · 380 · 400 · 450 · 490 · 500 · 510", "10 m", "op_sc"),
        ("MPM", "455", "200 · 250 · 275 · 300 · 330 · 350 · 380 · 400 · 445 · 450", "10 m", "op_g"),
        ("Panasonic", "350", "350", "10 m", "op_p38"),
        ("Panasonic SP28", "360", "350", "10 m", "op_c"),
        ("Yamaha", "360 / 420", "350 / 400", "10 m", "op_p25"),
        ("Hitachi", "360", "300", "10 m", "op_p30"),
        ("MINAMI", "290", "270", "15 / 10 m", "op_s8"),
        ("EKRA", "450 / 400", "400 / 300 · 400", "10 m", "op_e"),
        ("JUKI", "270 · 353 · 408 · 535", "260 · 345 · 400 · 520", "8 - 15 m", "op_r"),
        ("FUJI · KME · SONY", "500 · 480 · 280", "500 · 480 · 260", "15 · 20 · 20 m", "op_t"),
        ("@sz_large", "620", "600", "10 m", "op_c"),
        ("@sz_sheet", "-", "200 x 200 mm", "@sz_pack", "op_none")]
src = open(SKILL, encoding="utf-8").read()
EXT = r'''
import base64 as _b64
# ---- brands & models section ----
if "mod_h2" in EN:
    def _c(v): return f'<span data-i18n="{v[1:]}">{t(v[1:])}</span>' if v.startswith("@") else H.escape(v)
    _hdr = "".join(f'<th data-i18n="{k}">{t(k)}</th>' for k in ["bh_b", "bh_c", "bh_w", "bh_r", "bh_o"])
    _rows = "".join(f'<tr><th>{_c(b)}</th><td dir="ltr">{c}</td><td dir="ltr">{w}</td><td>{_c(r)}</td><td data-i18n="{o}">{t(o)}</td></tr>' for b, c, w, r, o in _SIZE)
    MODELS_HTML = f"""<section id="models"><div class="wrap">
  {el("span","mod_kick",'class="kick"')}
  {el("h2","mod_h2",'class="sec"')}
  {el("p","mod_lead",'class="lead"')}
  <div class="tw"><table class="t-wide btab"><thead><tr>{_hdr}</tr></thead><tbody>{_rows}</tbody></table></div>
  <div class="codebox"><h3 data-i18n="sz_h">{t("sz_h")}</h3>
  <p data-i18n="sz_p1">{t("sz_p1")}</p><p data-i18n="sz_p2">{t("sz_p2")}</p>
  <p class="mnote" data-i18n="sz_foot">{t("sz_foot")}</p></div>
</div></section>
"""
    page = page.replace('<section id="disclosure"', MODELS_HTML + '<section id="disclosure"', 1)
    page = page.replace('<a href="#disclosure" data-i18n="nav_disc">', f'<a href="#models" data-i18n="nav_models">{t("nav_models")}</a>\n      <a href="#disclosure" data-i18n="nav_disc">', 1)
    page = page.replace("</style>", """.codebox{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:20px 22px;margin-top:22px;box-shadow:var(--shadow)}
.codebox h3{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--gold2);margin-bottom:12px}
.btab td[dir=ltr]{font-variant-numeric:tabular-nums}
.codebox p{font-size:14px;color:var(--fg2)}
.btab tbody th{color:var(--brand);white-space:nowrap}
.mnote{font-size:13px;color:var(--fg3);margin-top:12px}
</style>""", 1)
# ---- blade-change planner (HTML swapped at source level, JS here) ----
if P.get("calc_mode") == "rolls":
    _js = r"""function calc(){
  var lang=document.documentElement.lang||"en";
  var p=num("cPrints"), ev=num("cEvery"), adv=num("cAdv"), days=num("cDays"), rl=num("cRoll")||10;
  var set=function(id,txt){ var e=document.getElementById(id); if(e) e.textContent=txt; };
  var w=(p>0&&ev>0)?p/ev:0;
  set("rWipes", w>0 ? fmt(w,lang) : "—");
  var md=w*adv/1000;
  set("rMday", md>0 ? fmt(md,lang) : "—");
  var mm=md*days;
  set("rMmonth", mm>0 ? fmt(mm,lang) : "—");
  var r=document.getElementById("rRolls"), u=document.getElementById("rRollsU");
  if(!r) return;
  if(!(mm>0)){ r.textContent="—"; u.textContent=T(lang,"calc_needinput"); return; }
  r.textContent=fmt(mm/rl,lang); u.textContent=T(lang,"unit_rolls");
}
"""
    page, _n = re.subn(r'function calc\(\)\{.*?\n\}\n', lambda m: _js, page, count=1, flags=re.S)
    assert _n == 1, "calc js not found"
    page = page.replace('["cFeeders","cShare","cMin","cRate","cTech","cTechRate","cPrice"]', '["cPrints","cEvery","cAdv","cDays","cRoll"]')
# ---- embedded videos ----
_ve = []
for _v in P["videos"]:
    if _v.get("embed") and _v.get("src"):
        _tok = f"embed:{len(_ve)}"
        _ve.append("data:video/mp4;base64," + _b64.b64encode(open(os.path.join(PD, _v["src"]), "rb").read()).decode())
        page = page.replace(f'data-src="{_v["src"]}"', f'data-src="{_tok}"').replace(f'"src": "{_v["src"]}"', f'"src": "{_tok}"')
if _ve:
    page = page.replace("player.src=src;", "player.src=vsrc(src);", 1)
    _vjs = ('<script>window.__VE=' + json.dumps(_ve) + ';function vsrc(s){if(String(s).indexOf("embed:")!==0)return s;var i=+s.slice(6);window.__VB=window.__VB||{};'
            'if(!window.__VB[i]){try{var d=atob(window.__VE[i].split(",")[1]),a=new Uint8Array(d.length);for(var j=0;j<d.length;j++)a[j]=d.charCodeAt(j);'
            'window.__VB[i]=URL.createObjectURL(new Blob([a],{type:"video/mp4"}));}catch(e){return window.__VE[i];}}return window.__VB[i];}</script>\n')
    page = page.replace("<script>const I18N", _vjs + "<script>const I18N", 1) if "<script>const I18N" in page else page.replace("<script>/* Runtime", _vjs + "<script>/* Runtime", 1)
    assert "window.__VE" in page and "vsrc(src)" in page, "video embed hook failed"
'''
PRE = """
if P.get("calc_mode") == "rolls":
    _cd = [str(x) for x in P.get("calc_defaults", ["", "", "", "", "10"])]
    CALC_HTML = (f'<div class="calc">\\n    <div class="ch"><h3 data-i18n="calc_h">{t("calc_h")}</h3><p data-i18n="calc_sub">{t("calc_sub")}</p></div>\\n'
             f'    <div class="cb">\\n      <div>{fld("cPrints","c_prints",_cd[0])}{fld("cEvery","c_every",_cd[1],"c_hint_every")}{fld("cAdv","c_adv",_cd[2],"c_hint_adv")}{fld("cDays","c_days",_cd[3])}{fld("cRoll","c_roll",_cd[4],"c_hint_roll")}</div>\\n'
             f'      <div class="cres">{rrow("r_wipes","rWipes")}{rrow("r_mday","rMday")}{rrow("r_mmonth","rMmonth")}\\n'
             f'        <div class="big"><div class="k" data-i18n="r_rolls">{t("r_rolls")}</div><div class="v" id="rRolls">—</div><div class="u" id="rRollsU"></div></div></div>\\n    </div>\\n'
             f'    <div class="cf" data-i18n="calc_foot">{t("calc_foot")}</div>\\n  </div>')
"""
_PJ = _json.load(open(os.path.join([x for x in sys.argv[1:] if not x.startswith("--")][0], "product.json"), encoding="utf-8"))
if _PJ.get("calc_mode") == "rolls":
    _A = '  <div class="calc">\n    <div class="ch"><h3 data-i18n="calc_h">'
    _B = '<div class="cf" data-i18n="calc_foot">{t("calc_foot")}</div>\n  </div>'
    _a = src.index(_A); _b = src.index(_B, _a) + len(_B)
    src = src[:_a] + "  {CALC_HTML}" + src[_b:]
else:
    PRE = ""
marker = "os.makedirs(OUTDIR, exist_ok=True)"
assert marker in src
src = src.replace(marker, EXT + "\n" + marker, 1)
src = src.replace('page = f"""', PRE + '\npage = f"""', 1)
g = {"__file__": SKILL, "__name__": "__main__", "_SIZE": SIZE}
sys.argv = [SKILL] + sys.argv[1:]
exec(compile(src, SKILL, "exec"), g)
