#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""smt-source-to-landing-page: build one self-contained landing page from a product folder.

Usage:
    python3 scripts/build.py <product-dir> [--out <dir>] [--check]

<product-dir> holds:
    product.json        structure: sections, counts, images, videos, docs, JSON-LD, calc ...
    i18n/<lang>.json    flat key -> plain-text strings (en is the master; others may omit keys)
    blogs.json          {"en": [post, ...], "<lang>": [...optional translations]}
                        post = [{"h": heading, "p": [paragraph, ...]}, ...]
    *.css / *.svg       optional product CSS and an inline illustration
    assets/             optional local images, referenced as "asset:<file>" and inlined as base64

No product-specific code lives here: a new product needs only a new product folder.
--check only validates the config and strings (missing keys, banned words) and writes nothing.
"""
import argparse, base64, html, json, mimetypes, os, re, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(SKILL, "templates")

LANG_META = {
    "en": ("ltr", "English", "EN", "en_US"), "es": ("ltr", "Español", "ES", "es_ES"),
    "pt": ("ltr", "Português", "PT", "pt_BR"), "fr": ("ltr", "Français", "FR", "fr_FR"),
    "ar": ("rtl", "العربية", "AR", "ar_AR"), "ru": ("ltr", "Русский", "RU", "ru_RU"),
    "zh": ("ltr", "中文", "ZH", "zh_CN"),
}
# Six-step brief labels (and the method's author name) that must never appear in a heading or title, in any language.
BANNED = {
    "en": ["hook", "diagnosis", "diagnose", "framework", "vehicle", "loop", "cta", "call to action", "dan koe"],
    "es": ["gancho", "diagnóstico", "marco de trabajo", "vehículo", "bucle", "llamada a la acción"],
    "pt": ["gancho", "diagnóstico", "estrutura de trabalho", "veículo", "loop", "chamada para ação", "chamada à ação"],
    "fr": ["accroche", "hameçon", "diagnostic", "framework", "véhicule", "boucle", "appel à l'action", "appel à l’action"],
    "ar": ["خطاف", "تشخيص", "إطار عمل", "مركبة", "حلقة", "دعوة إلى اتخاذ إجراء", "دعوة لاتخاذ إجراء"],
    "ru": ["крючок", "хук", "диагноз", "диагностика", "фреймворк", "носитель", "петля", "призыв к действию"],
    "zh": ["钩子", "诊断", "框架", "载体", "循环", "行动号召"],
}


def banned_hits(text):
    """Return banned brief words found in text (word-bounded for alphabetic scripts)."""
    hits = []
    low = text.lower()
    for lang, words in BANNED.items():
        for w in words:
            if w in hits:
                continue
            if lang in ("zh", "ar"):
                if w in text:
                    hits.append(w)
            elif re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", low):
                hits.append(w)
    return hits


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


class Page:
    def __init__(self, pdir):
        self.dir = os.path.abspath(pdir)
        self.cfg = load_json(os.path.join(self.dir, "product.json"))
        c = self.cfg
        brand = c.get("brand", "southern-machinery")
        if isinstance(brand, str):
            brand = load_json(os.path.join(TPL, "brand-%s.json" % brand))
        else:
            base = load_json(os.path.join(TPL, "brand-southern-machinery.json"))
            base.update(brand)
            brand = base
        brand.update(c.get("brand_overrides", {}))
        self.b = brand
        self.langs = c.get("languages", ["en", "es", "pt", "fr", "ar", "ru", "zh"])
        idir = os.path.join(self.dir, c.get("i18n_dir", "i18n"))
        self.I = {l: load_json(os.path.join(idir, l + ".json")) for l in self.langs}
        self.EN = self.I["en"]
        bp = os.path.join(self.dir, c.get("blogs", "blogs.json"))
        self.blogs = load_json(bp) if os.path.exists(bp) else {"en": []}
        self.filename = c["filename"]
        self.canon = c.get("canonical_base", "https://www.smthelp.com/") + self.filename
        self.secs = c["sections"]
        self.used = set()

    # ------------------------------------------------------------ helpers
    def t(self, k):
        self.used.add(k)
        if k not in self.EN:
            raise KeyError("i18n/en.json is missing key %r" % k)
        return html.escape(str(self.EN[k]), quote=True)

    def span(self, k, tag="span", cls=None, extra=""):
        c = ' class="%s"' % cls if cls else ""
        return '<%s%s data-i18n="%s"%s>%s</%s>' % (tag, c, k, extra, self.t(k), tag)

    def head2(self, kick, h2, lead=None):
        s = self.span(kick, "span", "kick") + "\n" + self.span(h2, "h2", "sec")
        if lead and lead in self.EN:
            s += "\n" + self.span(lead, "p", "lead")
        return s

    def ev(self, kind):
        c, k = {"v": ("ev-v", "ev_v"), "c": ("ev-c", "ev_c"), "t": ("ev-t", "ev_t")}[kind]
        return '<span class="ev %s" data-i18n="%s">%s</span>' % (c, k, self.t(k))

    def src(self, s):
        """'asset:<file>' -> base64 data URI from <product-dir>/assets; anything else as-is."""
        if not s.startswith("asset:"):
            return s
        p = os.path.join(self.dir, "assets", s[6:])
        mime = mimetypes.guess_type(p)[0] or "image/jpeg"
        return "data:%s;base64,%s" % (mime, base64.b64encode(open(p, "rb").read()).decode())

    def sec_class(self, sid):
        return self.alt.get(sid, "")

    # ------------------------------------------------------------ sections
    def s_hero(self):
        t = self.t
        imgs = "".join('<img src="%s" alt="%s" data-i18n-alt="%s"%s>' % (
            self.src(h["src"]), t(h["alt"]), h["alt"], ' fetchpriority="high"' if i == 0 else ' loading="lazy" decoding="async"')
            for i, h in enumerate(self.cfg["hero"]["images"]))
        cap = self.span("hero_cap", "p", "hcap") if "hero_cap" in self.EN else ""
        return '''<section class="hero" id="top">
  <div class="wrap">
    <div>
      %s
      <h1>%s<br><em data-i18n="hero_h1b">%s</em></h1>
      %s
      <div class="acts"><a class="btn btn-p" href="#contact" data-i18n="hero_cta1">%s</a><a class="btn btn-s" href="%s" data-i18n="hero_cta2">%s</a></div>
      %s
    </div>
    <div class="herofig"><div class="heroimgs playing" id="heroImgs">%s</div>%s</div>
  </div>
</section>''' % (self.span("hero_badge", "span", "badge"), self.span("hero_h1a"), t("hero_h1b"), self.span("hero_sub", "p", "sub"),
                 t("hero_cta1"), self.cfg["hero"].get("cta2_href", "#spec"), t("hero_cta2"), self.span("hero_note", "p", "hnote"), imgs, cap)

    def s_metrics(self):
        m = self.cfg["metrics"]
        ltr = set(m.get("ltr", []))
        ms = "".join('<div class="m"><div class="v"%s data-i18n="m%dv">%s</div><div class="l" data-i18n="m%dl">%s</div></div>'
                     % (' dir="ltr"' if ("m%dv" % i) in ltr else "", i, self.t("m%dv" % i), i, self.t("m%dl" % i))
                     for i in range(1, m["count"] + 1))
        return '<div class="metrics"><div class="wrap">%s</div></div>' % ms

    def s_trust(self):
        return '<div class="trust"><div class="wrap">%s</div></div>' % "".join(
            self.span("trust%d" % i) for i in range(1, self.cfg["trust"]["count"] + 1))

    def s_summary(self):
        t = self.t
        facts = "".join('<div class="sf"><dt data-i18n="sf%dk">%s</dt><dd data-i18n="sf%dv">%s</dd></div>' % (i, t("sf%dk" % i), i, t("sf%dv" % i))
                        for i in range(1, self.cfg["summary"]["facts"] + 1))
        return '''<section id="summary" class="compact"><div class="wrap"><div class="sumbox">
  <div>%s%s%s</div>
  <dl class="sfacts">%s</dl>
</div></div></section>''' % (self.span("sum_kick", "span", "kick"), self.span("sum_h2", "h2", "sec"), self.span("sum_p", "p", "sump"), facts)

    def s_pain(self):
        t = self.t
        cards = "".join('<div class="card"><div class="num">%02d</div><h3 data-i18n="w%dt">%s</h3><p data-i18n="w%dd">%s</p></div>'
                        % (i, i, t("w%dt" % i), i, t("w%dd" % i)) for i in range(1, self.cfg["pain"]["count"] + 1))
        return '<section id="why"%s><div class="wrap">%s<div class="grid g3">%s</div></div></section>' % (
            self.sec_class("pain"), self.head2("why_kick", "why_h2", "why_lead"), cards)

    def s_how(self):
        t, h = self.t, self.cfg["how"]
        steps = "".join('<li><span class="sn">%d</span><div><h3 data-i18n="s%dt">%s</h3><p data-i18n="s%dd">%s</p></div></li>'
                        % (i, i, t("s%dt" % i), i, t("s%dd" % i)) for i in range(1, h["steps"] + 1))
        ill = h.get("illustration")
        if ill and ill.endswith(".svg"):
            art = open(os.path.join(self.dir, ill), encoding="utf-8").read().strip()
        elif ill:
            art = '<img src="%s" alt="%s" data-i18n-alt="how_ev" loading="lazy" decoding="async">' % (self.src(ill), t("how_ev"))
        else:
            art = ""
        legend = ""
        if h.get("legend"):
            legend = '<ul class="legend">%s</ul>' % "".join('<li><b>%s</b><span data-i18n="%s">%s</span></li>' % (html.escape(a), k, t(k)) for a, k in h["legend"])
        safe = '\n<p class="safe" role="note">%s</p>' % self.span("how_safe") if h.get("safety_note") else ""
        return '''<section id="how"%s><div class="wrap">%s
<div class="howgrid">
  <ol class="steps">%s</ol>
  <figure class="ill">
    <div class="evline">%s</div>
    %s
    %s
    <figcaption data-i18n="how_ev">%s</figcaption>
  </figure>
</div>%s
</div></section>''' % (self.sec_class("how"), self.head2("how_kick", "how_h2", "how_lead"), steps, self.ev(h.get("evidence", "c")), art, legend, t("how_ev"), safe)

    # ------------------------------------------------------------ optional: component -> feeder quick-match (since 1.1.0)
    def mx_data(self):
        """Matcher data: product.json "matcher" may hold the data inline or name a JSON file in the product folder."""
        if getattr(self, "_mx", None) is None:
            m = self.cfg.get("matcher", {})
            d = m.get("data", "matcher.json")
            self._mx = load_json(os.path.join(self.dir, d)) if isinstance(d, str) else d
        return self._mx

    def mx_keys(self):
        """Every i18n key the matcher runtime looks up at run time (rows are rendered by runtime.js)."""
        D, keys = self.mx_data(), set()
        for c in D["categories"]:
            keys.add("mx_c_" + c)
        for p_ in D["packaging"]:
            keys.add("mx_p_" + p_)
        for f in D["feeders"]:
            keys.update(("mx_f_%sn" % f["id"], "mx_f_%sd" % f["id"], "mx_fo_%s" % f["id"]))
        for n in D.get("nozzles", []):
            keys.add("mx_n_" + n)
        for s_ in D.get("statuses", []):
            keys.add("mx_s_" + s_)
        for s_ in D.get("sources", []):
            keys.add("mx_src_" + s_)
        for r in D["rows"]:
            keys.add("mx_t_" + r["type"])
            if r.get("note"):
                keys.add("mx_note_" + r["note"])
        keys.update(["mx_col_comp", "mx_col_cat", "mx_col_pack", "mx_col_body", "mx_col_pitch", "mx_col_leads", "mx_col_ld",
                     "mx_col_feeder", "mx_col_nozzle", "mx_col_status", "mx_count", "mx_or", "mx_d_spec", "mx_d_body", "mx_d_oh",
                     "mx_d_feeder", "mx_d_nozzle", "mx_d_status", "mx_d_src", "mx_d_note", "mx_d_env", "mx_ask_wa", "mx_ask_mail",
                     "mx_ask_msg", "mx_ask_subj", "mx_chk_none", "mx_chk_fit", "mx_chk_out", "mx_d_page", "mx_unknown_v"])
        return keys

    def s_matcher(self):
        t, D, m = self.t, self.mx_data(), self.cfg.get("matcher", {})
        bins = D["bins"]

        def sel(sid, key, opts):
            o = '<option value="" data-i18n="mx_any">%s</option>' % t("mx_any")
            for val, lab, i18n in opts:
                o += '<option value="%s"%s>%s</option>' % (html.escape(str(val)), ' data-i18n="%s"' % lab if i18n else ' dir="ltr"',
                                                           t(lab) if i18n else html.escape(lab))
            return '<div class="fld"><label for="%s" data-i18n="%s">%s</label><select id="%s">%s</select></div>' % (sid, key, t(key), sid, o)

        def binopts(name):
            return [(i, b[2], False) for i, b in enumerate(bins[name])]
        filters = "".join([
            sel("mxCat", "mx_cat", [(c, "mx_c_" + c, True) for c in D["categories"]]),
            sel("mxPack", "mx_pack", [(p_, "mx_p_" + p_, True) for p_ in D["packaging"]]),
            sel("mxFeeder", "mx_feeder", [(f["id"], "mx_fo_" + f["id"], True) for f in D["feeders"]]),
            sel("mxPitch", "mx_pitch", binopts("pitch")),
            sel("mxL", "mx_L", binopts("size")), sel("mxW", "mx_W", binopts("size")), sel("mxH", "mx_H", binopts("size")),
            sel("mxLeads", "mx_leads", binopts("leads")), sel("mxLd", "mx_ld", binopts("ld")),
        ])
        cols = "".join('<th scope="col" data-i18n="mx_col_%s">%s</th>' % (c, t("mx_col_" + c))
                       for c in ("comp", "cat", "pack", "body", "pitch", "leads", "ld", "feeder", "nozzle", "status"))
        legend = "".join('<span class="mx-st mx-s-%s" data-i18n="mx_s_%s">%s</span>' % (s_, s_, t("mx_s_" + s_)) for s_ in D.get("statuses", []))
        chk = ""
        if m.get("check_part", True):
            num = lambda i, k: '<div class="fld"><label for="%s" data-i18n="%s">%s</label><input id="%s" type="number" min="0" step="any" inputmode="decimal"></div>' % (i, k, t(k), i)
            chk = '''
<div class="mx-check" id="mxCheck">
  <h3 data-i18n="mx_chk_h">%s</h3><p data-i18n="mx_chk_p">%s</p>
  <div class="mx-cgrid">%s%s%s%s%s%s</div>
  <div class="mx-cout" id="mxChkOut" aria-live="polite"></div>
</div>''' % (t("mx_chk_h"), t("mx_chk_p"),
             sel("mxCPack", "mx_pack", [(p_, "mx_p_" + p_, True) for p_ in D["packaging"]]),
             num("mxCL", "mx_cL"), num("mxCW", "mx_cW"), num("mxCH", "mx_cH"), num("mxCWt", "mx_cWt"), num("mxCLd", "mx_cLd"))
        for k in self.mx_keys():
            self.t(k)  # existence check + mark used
        data = json.dumps(D, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        return '''<section id="matcher"%s><div class="wrap">%s
<div class="mx" id="mx">
  <div class="mx-filters">
    <div class="fld mx-q"><label for="mxQ" data-i18n="mx_search">%s</label><input id="mxQ" type="search" autocomplete="off" placeholder="%s" data-i18n-ph="mx_search_ph"></div>
    %s
    <label class="mx-unk"><input type="checkbox" id="mxUnk" checked> <span data-i18n="mx_unknown">%s</span></label>
    <button type="button" class="btn btn-o mx-reset" id="mxReset" data-i18n="mx_reset">%s</button>
  </div>
  <div class="mx-bar"><b id="mxCount" aria-live="polite"></b><span class="mx-legend">%s</span></div>
  <div class="mx-tw"><table class="mx-table"><thead><tr>%s</tr></thead><tbody id="mxBody"></tbody></table></div>
  <p class="mx-empty" id="mxEmpty" hidden data-i18n="mx_empty">%s</p>
  <p class="qual" data-i18n="mx_note">%s</p>
</div>%s
</div></section>
<div class="modal" id="mxModal" role="dialog" aria-modal="true" aria-label="%s" data-i18n-aria="mx_d_title"><div class="inner mx-detail"><button type="button" class="cl" id="mxClose" aria-label="%s" data-i18n-aria="aria_close">✕</button><div id="mxDetail"></div></div></div>
<script type="application/json" id="matcherData">%s</script>''' % (
            self.sec_class("matcher"), self.head2("mx_kick", "mx_h2", "mx_lead"), t("mx_search"), t("mx_search_ph"), filters,
            t("mx_unknown"), t("mx_reset"), legend, cols, t("mx_empty"), t("mx_note"), chk, t("mx_d_title"), t("aria_close"), data)

    # ------------------------------------------------------------ optional: NPI / selection stepper with checklists (since 1.1.0)
    def s_npi(self):
        t, n = self.t, self.cfg["npi"]
        steps = n["steps"]
        checks = n.get("checks", [3] * steps)
        tabs = "".join('<li><button type="button" role="tab" class="npi-tab%s" id="npiT%d" aria-controls="npiP%d" aria-selected="%s"><span class="npi-n" dir="ltr">%d</span><span data-i18n="n%dt">%s</span></button></li>'
                       % (" on" if i == 1 else "", i, i, "true" if i == 1 else "false", i, i, t("n%dt" % i)) for i in range(1, steps + 1))
        panes = ""
        for i in range(1, steps + 1):
            cl = "".join('<li><label><input type="checkbox" class="npi-cb"> <span data-i18n="n%dc%d">%s</span></label></li>' % (i, j, t("n%dc%d" % (i, j)))
                         for j in range(1, checks[i - 1] + 1))
            nav = '<div class="npi-nav">%s%s</div>' % (
                '<button type="button" class="btn btn-o npi-prev" data-i18n="npi_prev">%s</button>' % t("npi_prev") if i > 1 else "<span></span>",
                '<button type="button" class="btn btn-p npi-next" data-i18n="npi_next">%s</button>' % t("npi_next") if i < steps else
                '<a class="btn btn-p" href="#contact" data-i18n="npi_cta">%s</a>' % t("npi_cta"))
            panes += '<div class="npi-pane%s" role="tabpanel" id="npiP%d" aria-labelledby="npiT%d"%s><span class="npi-k" dir="ltr">%d / %d</span><h3 data-i18n="n%dt">%s</h3><p data-i18n="n%dd">%s</p><ul class="npi-check">%s</ul>%s</div>' % (
                " on" if i == 1 else "", i, i, "" if i == 1 else " hidden", i, steps, i, t("n%dt" % i), i, t("n%dd" % i), cl, nav)
        return '''<section id="npi"%s><div class="wrap">%s
<div class="npi" id="npiBox">
  <ol class="npi-tabs" role="tablist">%s</ol>
  <div class="npi-body">%s
    <div class="npi-prog"><div class="npi-bar"><i id="npiBar"></i></div><span id="npiProg" dir="auto"></span></div>
  </div>
</div>
</div></section>''' % (self.sec_class("npi"), self.head2("npi_kick", "npi_h2", "npi_lead"), tabs, panes)

    def s_fab(self):
        t, n = self.t, self.cfg["fab"]["count"]
        tabs = "".join('<button type="button" role="tab" class="ftab%s" id="ft%d" aria-controls="fp%d" aria-selected="%s" data-i18n="fab%dn">%s</button>'
                       % (" on" if i == 1 else "", i, i, "true" if i == 1 else "false", i, t("fab%dn" % i)) for i in range(1, n + 1))
        panes = ""
        for i in range(1, n + 1):
            rows = "".join('<div class="fr fr-%s"><span class="fl" data-i18n="lab_%s">%s</span><p data-i18n="fab%d%s">%s</p></div>'
                           % (x, x, t("lab_" + x), i, x, t("fab%d%s" % (i, x))) for x in ("f", "a", "b"))
            panes += '<div class="fpane%s" role="tabpanel" id="fp%d" aria-labelledby="ft%d"%s><h3 data-i18n="fab%dn">%s</h3>%s</div>' % (
                " on" if i == 1 else "", i, i, "" if i == 1 else " hidden", i, t("fab%dn" % i), rows)
        return '<section id="fab"%s><div class="wrap">%s<div class="fabshell"><div class="ftabs" role="tablist">%s</div><div class="fpanes">%s</div></div></div></section>' % (
            self.sec_class("fab"), self.head2("fab_kick", "fab_h2", "fab_lead"), tabs, panes)

    def s_models(self):
        t, m = self.t, self.cfg["models"]
        ltr = set(m.get("ltr_titles", []))
        mc = "".join('<div class="mcard2"><span class="mtag" data-i18n="mc%ds">%s</span><h3%s data-i18n="mc%dt">%s</h3><p data-i18n="mc%dd">%s</p></div>' % (
            i, t("mc%ds" % i), ' dir="ltr"' if ("mc%dt" % i) in ltr else "", i, t("mc%dt" % i), i, t("mc%dd" % i)) for i in range(1, m["cards"] + 1))
        fit = ""
        if m.get("fit_rows"):
            rows = "".join('<tr><td data-i18n="fr%da">%s</td><td><b data-i18n="fr%db">%s</b></td><td data-i18n="fr%dc">%s</td></tr>'
                           % (i, t("fr%da" % i), i, t("fr%db" % i), i, t("fr%dc" % i)) for i in range(1, m["fit_rows"] + 1))
            fit = '''
<h3 class="subh" data-i18n="fit_h">%s</h3>
<div class="tw"><table><thead><tr><th data-i18n="fit_c1">%s</th><th data-i18n="fit_c2">%s</th><th data-i18n="fit_c3">%s</th></tr></thead><tbody>%s</tbody></table></div>''' % (
                t("fit_h"), t("fit_c1"), t("fit_c2"), t("fit_c3"), rows)
        return '<section id="models"%s><div class="wrap">%s<div class="mgrid2">%s</div>%s\n</div></section>' % (
            self.sec_class("models"), self.head2("models_kick", "models_h2", "models_lead"), mc, fit)

    def s_spec(self):
        t, sp = self.t, self.cfg["spec"]
        ltr = set(sp.get("ltr", []))
        rows = ""
        for i, evk in enumerate(sp["evidence"], 1):
            rows += '<tr><th scope="row" data-i18n="spr%dn">%s</th><td%s data-i18n="spr%dv">%s</td><td>%s</td></tr>' % (
                i, t("spr%dn" % i), ' dir="ltr"' if ("spr%dv" % i) in ltr else "", i, t("spr%dv" % i), self.ev(evk))
        return '''<section id="spec"%s><div class="wrap">%s
<div class="tw"><table class="spect"><thead><tr><th data-i18n="sp_c1">%s</th><th data-i18n="sp_c2">%s</th><th data-i18n="sp_c3">%s</th></tr></thead><tbody>%s</tbody></table></div>
<p class="qual" data-i18n="spec_note">%s</p>
</div></section>''' % (self.sec_class("spec"), self.head2("spec_kick", "spec_h2", "spec_lead"), t("sp_c1"), t("sp_c2"), t("sp_c3"), rows, t("spec_note"))

    def s_disclosure(self):
        t = self.t
        rows = "".join('<tr><th scope="row" data-i18n="dr%da">%s</th><td data-i18n="dr%db">%s</td><td data-i18n="dr%dc">%s</td><td data-i18n="dr%dd">%s</td></tr>'
                       % (i, t("dr%da" % i), i, t("dr%db" % i), i, t("dr%dc" % i), i, t("dr%dd" % i)) for i in range(1, self.cfg["disclosure"]["rows"] + 1))
        return '''<section id="disclosure"%s><div class="wrap">%s
<div class="tw"><table><thead><tr><th data-i18n="dc_c1">%s</th><th data-i18n="dc_c2">%s</th><th data-i18n="dc_c3">%s</th><th data-i18n="dc_c4">%s</th></tr></thead><tbody>%s</tbody></table></div>
</div></section>''' % (self.sec_class("disclosure"), self.head2("disc_kick", "disc_h2", "disc_lead"), t("dc_c1"), t("dc_c2"), t("dc_c3"), t("dc_c4"), rows)

    def s_calc(self):
        t, c = self.t, self.cfg["calc"]
        fl = "".join('<div class="fld"><label for="%s" data-i18n="%s">%s</label><input id="%s" type="number" min="0" step="any" value="%s" inputmode="decimal"></div>'
                     % (f["id"], f["key"], t(f["key"]), f["id"], f["value"]) for f in c["inputs"])
        res = "".join('<div class="r"><span data-i18n="%s">%s</span><b id="%s" dir="ltr">—</b></div>' % (o["key"], t(o["key"]), o["id"]) for o in c["outputs"])
        return '''<section id="calc"%s><div class="wrap">%s
<div class="calc"><div class="ch"><h3 data-i18n="calc_t">%s</h3><p data-i18n="calc_s">%s</p></div>
<div class="cb"><div>%s</div><div class="cres">%s</div></div>
<div class="cf" data-i18n="calc_note">%s</div></div>
</div></section>''' % (self.sec_class("calc"), self.head2("calc_kick", "calc_h2", "calc_lead"), t("calc_t"), t("calc_s"), fl, res, t("calc_note"))

    def s_gallery(self):
        t = self.t
        figs = "".join('<figure tabindex="0" role="button" data-full="%s"><img src="%s" alt="%s" data-i18n-alt="%s" loading="lazy" decoding="async"><figcaption data-i18n="%s">%s</figcaption></figure>' % (
            html.escape(self.src(g.get("full", g["thumb"])), quote=True), html.escape(self.src(g["thumb"]), quote=True), t(g["key"]), g["key"], g["key"], t(g["key"]))
            for g in self.cfg["gallery"])
        return '<section id="gallery"%s><div class="wrap">%s<div class="galgrid">%s</div></div></section>' % (
            self.sec_class("gallery"), self.head2("gal_kick", "gal_h2", "gal_lead"), figs)

    def s_videos(self):
        t, v = self.t, self.cfg["videos"]
        catkey = dict(v["filters"])
        chips = "".join('<button type="button" class="vchip%s" data-f="%s" data-i18n="%s">%s</button>' % (" on" if f == "all" else "", f, k, t(k))
                        for f, k in [("all", "vf_all")] + [tuple(x) for x in v["filters"]])
        vids = ""
        for it in v["items"]:
            vid, title, cat = it["id"], html.escape(it["title"], quote=True), it["cat"]
            vids += ('<article class="vid" data-cat="%s"><div class="th" data-vid="%s"><img loading="lazy" decoding="async" src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="%s">'
                     '<button type="button" class="pl" aria-label="%s" data-i18n-aria="vid_play"><i></i></button></div>'
                     '<div class="bd"><span class="dur" dir="ltr">%s</span> <span class="vcat" data-i18n="%s">%s</span><h3 lang="en" dir="ltr">%s</h3></div></article>'
                     % (cat, vid, vid, title, t("vid_play"), it["dur"], catkey[cat], t(catkey[cat]), title))
        return '<section id="videos"%s><div class="wrap">%s<div class="vchips" role="group">%s</div><div class="vids" id="vidGrid">%s</div></div></section>' % (
            self.sec_class("videos"), self.head2("vid_kick", "vid_h2", "vid_lead"), chips, vids)

    def s_blog(self):
        t = self.t
        posts = ""
        en_posts = self.blogs.get("en", [])
        for i, post in enumerate(en_posts, 1):
            arts = ""
            for lang in ["en"] + [l for l in self.langs if l != "en" and l in self.blogs]:
                lp = self.blogs[lang][i - 1] if lang != "en" else post
                body = "".join("<h4>%s</h4>" % html.escape(sec["h"]) + "".join("<p>%s</p>" % html.escape(p) for p in sec["p"]) for sec in lp)
                d = LANG_META.get(lang, ("ltr",))[0]
                arts += '<div class="art" lang="%s" dir="%s" data-blang="%s"%s>%s</div>' % (lang, d, lang, "" if lang == "en" else " hidden", body)
            posts += ('<details class="post" id="article-%d"><summary><span class="pt"><small><span dir="ltr">%02d</span> · <span data-i18n="b_min">%s</span></small>'
                      '<span class="ptt" data-i18n="b%dt">%s</span><span class="pts" data-i18n="b%ds">%s</span><span class="rd" data-i18n="b_read">%s</span></span></summary>'
                      '<div class="pbody"><p class="enonly" data-i18n="blog_note">%s</p>%s</div></details>'
                      % (i, i, t("b_min"), i, t("b%dt" % i), i, t("b%ds" % i), t("b_read"), t("blog_note"), arts))
        return '<section id="blog"%s><div class="wrap">%s<div class="postgrid">%s</div></div></section>' % (
            self.sec_class("blog"), self.head2("blog_kick", "blog_h2", "blog_lead"), posts)

    def s_docs(self):
        t, d = self.t, self.cfg["docs"]
        dc = ""
        for it in d["items"]:
            k = it["key"]
            dc += ('<div class="doc"><div class="dico" aria-hidden="true">PDF</div><div class="dtx"><h3 data-i18n="%st">%s</h3><p data-i18n="%sd">%s</p>'
                   '<div class="dact"><a class="dbtn" href="%s" target="_blank" rel="noopener" data-i18n="doc_open">%s</a>'
                   '<button type="button" class="dbtn ghost" data-pdf="%s" data-i18n="doc_prev">%s</button><span class="dsz" dir="ltr">%s</span></div></div></div>'
                   % (k, t(k + "t"), k, t(k + "d"), it["url"], t("doc_open"), it["url"], t("doc_prev"), it.get("size", "")))
        if d.get("boards", True):
            host = re.sub(r"^https?://", "", self.b["catalog_site"]).rstrip("/")
            for k, url in [("dk_vb", self.b["video_board"]), ("dk_cb", self.b["catalog_board"])]:
                dc += ('<div class="doc board"><div class="dico" aria-hidden="true">WEB</div><div class="dtx"><h3 data-i18n="%s">%s</h3><p data-i18n="%sd">%s</p>'
                       '<div class="dact"><a class="dbtn" href="%s" target="_blank" rel="noopener">↗ %s</a></div></div></div>' % (k, t(k), k, t(k + "d"), url, host))
        return '<section id="docs"%s><div class="wrap">%s<div class="docgrid">%s</div></div></section>' % (
            self.sec_class("docs"), self.head2("docs_kick", "docs_h2", "docs_lead"), dc)

    def s_service(self):
        t, n = self.t, self.cfg["service"]["count"]
        sv = "".join('<div class="s"><div class="ic" dir="ltr">%02d</div><h4 data-i18n="sv%dt">%s</h4><p data-i18n="sv%dd">%s</p></div>'
                     % (i, i, t("sv%dt" % i), i, t("sv%dd" % i)) for i in range(1, n + 1))
        return '<section id="service"%s><div class="wrap">%s<div class="svc svc%d">%s</div></div></section>' % (
            self.sec_class("service"), self.head2("svc_kick", "svc_h2"), n, sv)

    def s_faq(self):
        t = self.t
        fq = "".join('<details%s><summary data-i18n="q%dt">%s</summary><div class="ans" data-i18n="q%da">%s</div></details>'
                     % (" open" if i == 1 else "", i, t("q%dt" % i), i, t("q%da" % i)) for i in range(1, self.cfg["faq"]["count"] + 1))
        return '<section id="faq"%s><div class="wrap">%s<div class="fqs">%s</div></div></section>' % (self.sec_class("faq"), self.head2("faq_kick", "faq_h2"), fq)

    def s_family(self):
        fam = "".join('<a class="btn btn-o" href="%s" target="_blank" rel="noopener" data-i18n="%s">%s</a>' % (f["url"], f["key"], self.t(f["key"])) for f in self.cfg["family"])
        return '<section id="family" class="compact"><div class="wrap">%s<div class="acts famacts">%s</div></div></section>' % (self.head2("fam_kick", "fam_h2"), fam)

    def s_contact(self):
        t, c, b = self.t, self.cfg["contact"], self.b
        from urllib.parse import quote
        fields = ""
        for fid, key, kind in c["fields"]:
            if kind == "textarea":
                inp = '<textarea id="%s" rows="3"></textarea>' % fid
            elif kind == "email":
                inp = '<input id="%s" type="email" autocomplete="email">' % fid
            elif kind == "numeric":
                inp = '<input id="%s" inputmode="numeric">' % fid
            elif kind:
                inp = '<input id="%s" autocomplete="%s">' % (fid, kind)
            else:
                inp = '<input id="%s">' % fid
            fields += '\n    <div class="fld"><label for="%s" data-i18n="%s">%s</label>%s</div>' % (fid, key, t(key), inp)
        return '''<section id="contact"><div class="wrap"><div class="cta">
  <div>%s%s%s
    <div class="acts"><a class="btn btn-p" href="%s?text=%s" target="_blank" rel="noopener" data-i18n="wa_btn">%s</a><a class="btn btn-s" href="mailto:%s" data-i18n="mail_btn">%s</a></div>
  </div>
  <form id="qform" novalidate>%s
    <button class="btn btn-p" type="submit" data-i18n="f_send">%s</button>
    <p class="note" data-i18n="f_note">%s</p>
  </form>
</div></div></section>''' % (self.span("ct_kick", "span", "kick"), self.span("ct_h2", "h2"), self.span("ct_lead", "p"), b["whatsapp"],
                             quote(c["wa_text"], safe=""), t("wa_btn"), b["email"], t("mail_btn"), fields, t("f_send"), t("f_note"))

    # ------------------------------------------------------------ chrome
    def header(self):
        t, b = self.t, self.b
        nav = "".join('<a href="#%s" data-i18n="%s"%s>%s</a>' % (h, k, ' class="navcta"' if h == "contact" else "", t(k)) for h, k in self.cfg["nav"])
        return '''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span class="dot"></span>%s</div></div>
<header id="hdr">
  <div class="wrap hd">
    <a class="brand" href="#top"><img src="%s" alt="%s" width="116" height="32"><span class="bs"><b>%s</b>%s</span></a>
    <nav class="mn" id="nav" aria-label="Main">%s</nav>
    <div class="hctl">
      <button class="ibtn" id="themeBtn" type="button" aria-label="%s" data-i18n-aria="aria_theme" title="%s" data-i18n-title="aria_theme"><span id="themeIcon">☀</span></button>
      <div class="lw" id="langWrap">
        <button class="ibtn" id="langBtn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="%s" data-i18n-aria="aria_lang" title="%s" data-i18n-title="aria_lang"><span id="langIcon">EN</span></button>
        <div class="langmenu" id="langMenu" role="menu"></div>
      </div>
      <button class="ibtn burger" id="burger" type="button" aria-label="%s" data-i18n-aria="aria_menu"><span>☰</span></button>
    </div>
  </div>
</header>''' % (self.span("topbar"), b["logo"], b["name"], b["name"], self.span("brand_sub"), nav,
                t("aria_theme"), t("aria_theme"), t("aria_lang"), t("aria_lang"), t("aria_menu"))

    def footer(self):
        t, b, f = self.t, self.b, self.cfg["footer"]
        soc = "".join('<a href="%s" target="_blank" rel="noopener" aria-label="%s" data-i18n-aria="%s" title="%s" data-i18n-title="%s">%s</a>' % (
            s["url"], t(s["key"]), s["key"], t(s["key"]), s["key"], s["glyph"]) for s in b["socials"])
        soclist = "".join('<a href="%s" target="_blank" rel="noopener" data-i18n="%s">%s</a>' % (s["url"], s["key"], t(s["key"])) for s in b["socials"])
        plinks = "".join('<a href="%s" target="_blank" rel="noopener" data-i18n="%s">%s</a>' % (l["url"], l["key"], t(l["key"])) for l in f["product_links"])
        site = b["website"].rstrip("/")
        return '''<footer>
  <div class="wrap">
    <div class="fg">
      <div><img class="fl" src="%s" alt="%s" width="108" height="30">%s<div class="soc">%s</div></div>
      <div>%s%s</div>
      <div>%s<a href="%s" target="_blank" rel="noopener" data-i18n="fl5">%s</a><a href="%s" target="_blank" rel="noopener" data-i18n="fl6">%s</a><a href="%s" target="_blank" rel="noopener" data-i18n="fl7">%s</a><a href="%s" target="_blank" rel="noopener" data-i18n="fl8">%s</a></div>
      <div>%s<a href="mailto:%s" dir="ltr">%s</a><a href="%s" target="_blank" rel="noopener" data-i18n="foot_wa">%s</a><a href="tel:%s" dir="ltr">%s</a><a href="%s" target="_blank" rel="noopener" dir="ltr">%s</a>%s
        <div class="soclist">%s</div></div>
    </div>
    <div class="bot">
      <p class="browse"><span data-i18n="foot_browse">%s</span> · <a class="inl" href="mailto:%s" data-i18n="foot_contact">%s</a></p>
      <p class="disc" data-i18n="foot_rights">%s</p>
    </div>
  </div>
</footer>''' % (b["logo"], b["name"], self.span("foot_about", "p"), soc,
                self.span("foot_h1", "h4"), plinks,
                self.span("foot_h2", "h4"), b["catalog_site"], t("fl5"), b["photo_site"], t("fl6"), b["video_board"], t("fl7"), b["catalog_board"], t("fl8"),
                self.span("foot_h3", "h4"), b["email"], b["email"], b["whatsapp"], t("foot_wa"), b["tel"], b["tel_display"], site,
                re.sub(r"^https?://", "", site), self.span("foot_addr", "p", "addr"), soclist,
                t("foot_browse"), b["email"], t("foot_contact"), t("foot_rights"))

    def overlays(self):
        t = self.t
        wa_svg = ('<svg viewBox="0 0 32 32" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M16 3C9.4 3 4 8.3 4 14.9c0 2.6.8 5 2.3 7L4 29l7.3-2.3c1.4.7 3 1.1 4.7 1.1 6.6 0 12-5.3 12-11.9C28 8.3 22.6 3 16 3zm0 21.8c-1.5 0-3-.4-4.3-1.1l-.3-.2-4.3 1.4 1.4-4.2-.2-.3a9.6 9.6 0 0 1-1.7-5.4c0-5.3 4.3-9.6 9.4-9.6s9.4 4.3 9.4 9.6-4.3 9.6-9.4 9.6zm5.2-7c-.3-.1-1.7-.9-2-1s-.5-.1-.7.1c-.2.3-.8 1-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3 2.4 1 2.9.8 3.4.7.5-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3z"/></svg>')
        return '''<div id="lb" role="dialog" aria-modal="true" aria-label="%s" data-i18n-aria="aria_viewer"><button type="button" aria-label="%s" data-i18n-aria="aria_close">✕</button><img alt="" data-i18n-alt="lb_alt"></div>
<div class="modal" id="pdfModal" role="dialog" aria-modal="true" aria-label="PDF"><div class="inner pdfinner"><button type="button" class="cl" id="pdfClose" aria-label="%s" data-i18n-aria="aria_close">✕</button><iframe id="pdfFrame" title="PDF preview"></iframe></div></div>
<a class="wafab" href="%s" target="_blank" rel="noopener" aria-label="%s" data-i18n-aria="aria_wa">%s</a>
<button type="button" class="totop" id="toTop" aria-label="%s" data-i18n-aria="aria_top">↑</button>''' % (
            t("aria_viewer"), t("aria_close"), t("aria_close"), self.b["whatsapp"], t("aria_wa"), wa_svg, t("aria_top"))

    def body(self):
        # alternate background on content sections, as in the reference page
        self.alt, flip = {}, True
        for s in self.secs:
            if s in ("hero", "metrics", "trust", "summary", "family", "contact"):
                continue
            self.alt[s] = ' class="alt"' if flip else ""
            flip = not flip
        P = [self.header()]
        main = []
        for s in self.secs:
            fn = getattr(self, "s_" + s, None)
            if not fn:
                raise ValueError("unknown section %r (known: %s)" % (s, ", ".join(x[2:] for x in dir(self) if x.startswith("s_"))))
            main.append(fn())
        # hero, metrics and trust sit inside <main> just like the reference
        P.append('<main id="main">\n' + "\n".join(main) + "\n</main>")
        P.append(self.footer())
        P.append(self.overlays())
        return "\n".join(P)

    # ------------------------------------------------------------ SEO / GEO
    def fill(self, o):
        """Substitute {{canonical}}, {{t:key}} and {{steps}} inside JSON-LD templates."""
        if isinstance(o, str):
            if o == "{{npi_steps}}":
                n = self.cfg["npi"]
                return [{"@type": "HowToStep", "position": i, "name": self.EN["n%dt" % i], "text": self.EN["n%dd" % i],
                         "itemListElement": [{"@type": "HowToDirection", "text": self.EN["n%dc%d" % (i, j)]}
                                             for j in range(1, n.get("checks", [3] * n["steps"])[i - 1] + 1)]}
                        for i in range(1, n["steps"] + 1)]
            if o == "{{steps}}":
                return [{"@type": "HowToStep", "position": i, "name": self.EN["s%dt" % i], "text": self.EN["s%dd" % i]} for i in range(1, self.cfg["how"]["steps"] + 1)]
            o = o.replace("{{canonical}}", self.canon).replace("{{org}}", self.b["org_id"])
            return re.sub(r"\{\{t:([a-z0-9_]+)\}\}", lambda m: self.EN[m.group(1)], o)
        if isinstance(o, list):
            return [self.fill(x) for x in o]
        if isinstance(o, dict):
            return {k: self.fill(v) for k, v in o.items()}
        return o

    def jsonld(self):
        b, c, EN, CANON = self.b, self.cfg, self.EN, self.canon
        J = c.get("jsonld", {})
        org = {"@type": "Organization", "@id": b["org_id"], "name": b["legal_name"], "alternateName": b["name"],
               "url": b["website"], "logo": b["logo"], "foundingDate": b["founding_date"], "email": b["email"],
               "telephone": b["tel_ld"], "address": b["address_ld"], "sameAs": [s["url"] for s in b["socials"]]}
        prim = c.get("seo", {}).get("primary_image") or c.get("seo", {}).get("og_image")
        page = {"@type": "WebPage", "@id": CANON, "url": CANON, "name": EN["seo_title"], "description": EN["seo_desc"],
                "inLanguage": self.langs, "datePublished": c["pub_date"], "dateModified": c.get("mod_date", c["pub_date"]),
                "publisher": {"@id": b["org_id"]}, "mainEntity": {"@id": CANON + "#product"},
                "primaryImageOfPage": prim,
                "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".sump", ".fqs .ans"]}}
        crumbs = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": b["name"], "item": b["website"]}] + [
            {"@type": "ListItem", "position": i, "name": n, "item": self.fill(u)} for i, (n, u) in enumerate(J.get("breadcrumb", []), 2)]}
        graph = [org, page, crumbs] + [self.fill(p) for p in J.get("products", [])]
        if J.get("howto"):
            graph.append(self.fill(J["howto"]))
        if "faq" in self.secs:
            graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": EN["q%dt" % i], "acceptedAnswer": {"@type": "Answer", "text": EN["q%da" % i]}}
                                                            for i in range(1, c["faq"]["count"] + 1)]})
        if "blog" in self.secs:
            blog = {"@type": "ItemList", "name": J.get("blog_list_name", "Articles"), "itemListElement": []}
            for i, post in enumerate(self.blogs.get("en", []), 1):
                body = " ".join(" ".join(sec["p"]) for sec in post)
                blog["itemListElement"].append({"@type": "ListItem", "position": i, "item": {
                    "@type": "BlogPosting", "headline": EN["b%dt" % i], "description": EN["b%ds" % i],
                    "url": CANON + "#article-%d" % i, "datePublished": c["pub_date"], "inLanguage": "en",
                    "author": {"@id": b["org_id"]}, "publisher": {"@id": b["org_id"]},
                    "about": {"@id": CANON + "#product"}, "wordCount": len(body.split()), "articleBody": body}})
            graph.append(blog)
        if "videos" in self.secs:
            vids = {"@type": "ItemList", "name": J.get("video_list_name", "Videos"), "itemListElement": []}
            for i, it in enumerate(c["videos"]["items"], 1):
                m, s = it["dur"].split(":")[-2:]
                h = int(it["dur"].split(":")[0]) if it["dur"].count(":") == 2 else 0
                dur = "PT%s%dM%dS" % ("%dH" % h if h else "", int(m), int(s))
                # uploadDate is deliberately absent: the video board does not give it and it must not be invented.
                vids["itemListElement"].append({"@type": "ListItem", "position": i, "item": {
                    "@type": "VideoObject", "name": it["title"], "description": it["title"] + " (%s YouTube channel)" % b["name"],
                    "thumbnailUrl": "https://i.ytimg.com/vi/%s/hqdefault.jpg" % it["id"],
                    "embedUrl": "https://www.youtube-nocookie.com/embed/%s" % it["id"], "url": "https://www.youtube.com/watch?v=%s" % it["id"],
                    "duration": dur, "publisher": {"@id": b["org_id"]}}})
            graph.append(vids)
        if "matcher" in self.secs and self.cfg.get("matcher", {}).get("jsonld_itemlist", True):
            D = self.mx_data()
            graph.append({"@type": "ItemList", "name": J.get("matcher_list_name", "Feeder models in the quick-match table"),
                          "numberOfItems": len(D["feeders"]), "itemListElement": [
                {"@type": "ListItem", "position": i, "item": {
                    "@type": "Product", "@id": CANON + "#feeder-" + f["id"], "name": ("%s %s" % (f["model"], EN["mx_f_%sn" % f["id"]])).strip(),
                    "description": EN["mx_f_%sd" % f["id"]], "model": f.get("model") or None,
                    "brand": {"@type": "Brand", "name": b["name"]} if f.get("own", True) else None,
                    "manufacturer": {"@id": b["org_id"]} if f.get("own", True) else None,
                    "image": f.get("image"), "url": f.get("url")}} for i, f in enumerate(D["feeders"], 1)]})
            for it in graph[-1]["itemListElement"]:
                it["item"] = {k: v for k, v in it["item"].items() if v is not None}
        if J.get("terms"):
            graph.append(J["terms"])
        return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")

    def head(self):
        t, b, seo = self.t, self.b, self.cfg.get("seo", {})
        CANON = self.canon
        alts = "".join('<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, CANON, "" if l == "en" else "?lang=" + l) for l in self.langs)
        alts += '<link rel="alternate" hreflang="x-default" href="%s">\n' % CANON
        og_alt = "".join('<meta property="og:locale:alternate" content="%s">' % LANG_META[l][3] for l in self.langs if l != "en")
        og_img = seo["og_image"]
        return '''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<meta name="keywords" content="%s">
<meta name="author" content="%s">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="theme-color" content="%s">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="%s">
%s<link rel="preconnect" href="https://i.ytimg.com">
<link rel="preconnect" href="%s">
<meta property="og:type" content="product">
<meta property="og:site_name" content="%s">
<meta property="og:locale" content="en_US">
%s
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta property="og:image:alt" content="%s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="%s">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s">
<script type="application/ld+json">
%s
</script>''' % (t("seo_title"), t("seo_desc"), t("seo_keys"), b["legal_name"], b["theme_color_light"], CANON, alts, b["photo_site"], b["name"], og_alt,
                t("og_title"), t("og_desc"), CANON, og_img, html.escape(seo.get("og_image_alt", ""), quote=True),
                b["twitter_handle"], t("og_title"), t("og_desc"), og_img, self.jsonld())

    def chatwoot(self):
        cw = self.b.get("chatwoot")
        if not cw or self.cfg.get("chatwoot") is False:
            return ""
        return '''<script>
window.chatwootSettings = %s;
(function(d,t) {
  /* Always https: an http sdk on an https page is blocked as mixed content (http answers 301 anyway). */
  var BASE_URL="%s";
  var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
  g.src=BASE_URL+"/packs/js/sdk.js";
  g.async = true;
  s.parentNode.insertBefore(g,s);
  g.onload=function(){
    window.chatwootSDK.run({
      websiteToken: '%s',
      baseUrl: BASE_URL
    })
  }
})(document,"script");
</script>''' % (json.dumps(cw["settings"], ensure_ascii=False), cw["base_url"], cw["website_token"])

    # ------------------------------------------------------------ checks
    def check(self):
        """Static checks that need no browser. Returns list of problems."""
        probs = []
        for l in self.langs:
            for k, v in self.I[l].items():
                if k.startswith("__"):
                    continue
                if k not in self.EN:
                    probs.append("%s.json has key %r that en.json lacks" % (l, k))
        heading_keys = [k for k in self.used if re.match(r"^(seo_title|og_title|hero_h1[ab]|.*_h2|w\d+t|s\d+t|n\d+t|fab\d+n|mc\d+t|b\d+t|q\d+t|sv\d+t|calc_t|fit_h|mx_chk_h|dk\d+t)$", k)]
        for l in self.langs:
            for k in heading_keys:
                v = self.I[l].get(k)
                if v and banned_hits(v):
                    probs.append("banned brief word %s in %s:%s = %r" % (banned_hits(v), l, k, v))
        for lang, posts in self.blogs.items():
            for i, post in enumerate(posts, 1):
                for sec in post:
                    if banned_hits(sec["h"]):
                        probs.append("banned brief word %s in blog %s #%d heading %r" % (banned_hits(sec["h"]), lang, i, sec["h"]))
        n_blogs = len(self.blogs.get("en", []))
        want = self.cfg.get("blog_count", 8)
        if "blog" in self.secs and n_blogs != want:
            probs.append("blogs.json has %d English posts, blog_count wants %d" % (n_blogs, want))
        for l in self.blogs:
            if l != "en" and len(self.blogs[l]) != n_blogs:
                probs.append("blogs.json[%s] has %d posts, en has %d" % (l, len(self.blogs[l]), n_blogs))
        price = re.compile(r"(¥|￥|RMB|CNY|USD|US\$|\$\s?\d|€\s?\d|\d\s?元)")
        for k, v in self.EN.items():
            if price.search(str(v)):
                probs.append("possible price in en:%s = %r" % (k, v))
        ex = os.path.join(SKILL, "examples", "radial-splice-tape")
        if os.path.abspath(self.dir) != ex:
            ex_en = load_json(os.path.join(ex, "i18n", "en.json"))
            same = [k for k in ("seo_title", "hero_h1a", "hero_sub", "sum_p", "q1t") if k in self.EN and self.EN[k] == ex_en.get(k)]
            if same:
                probs.append("i18n/en.json still holds the reference example text for %s" % same)
        for sec, path in (("hero", ("hero", "images")), ("gallery", ("gallery",)), ("videos", ("videos", "items")), ("docs", ("docs", "items")), ("family", ("family",))):
            if sec in self.secs:
                v = self.cfg
                for p_ in path:
                    v = v.get(p_, []) if isinstance(v, dict) else v
                if not v:
                    probs.append("section %r is listed but product.json has no %s: fill it or drop the section" % (sec, ".".join(path)))
        if "matcher" in self.secs:
            D = self.mx_data()
            fids = {f["id"] for f in D["feeders"]}
            for r in D["rows"]:
                for fk in ("feeder", "alt"):
                    if r.get(fk) and r[fk] not in fids:
                        probs.append("matcher row %s: unknown %s %r" % (r.get("id"), fk, r[fk]))
                for fk, allowed in (("cat", D["categories"]), ("pack", D["packaging"]), ("nozzle", D.get("nozzles", [])),
                                    ("status", D.get("statuses", [])), ("src", D.get("sources", []))):
                    if r.get(fk) and r[fk] not in allowed:
                        probs.append("matcher row %s: %s %r is not declared" % (r.get("id"), fk, r[fk]))
            for l in self.langs:
                for k in self.mx_keys():
                    v = self.I[l].get(k)
                    if v and re.match(r"^mx_", str(v)):
                        probs.append("matcher key %s in %s looks untranslated (%r)" % (k, l, v))
            for k in self.mx_keys():
                if k not in self.EN:
                    probs.append("matcher needs i18n key %r in en.json" % k)
        if not self.cfg.get("seo", {}).get("og_image"):
            probs.append("seo.og_image is empty")
        for term in self.cfg.get("verify", {}).get("forbidden_terms", []):
            for l in self.langs:
                for k, v in self.I[l].items():
                    if term.lower() in str(v).lower():
                        probs.append("forbidden term %r in %s:%s" % (term, l, k))
        return probs

    # ------------------------------------------------------------ assemble
    def build(self, out_dir):
        css = open(os.path.join(TPL, "base.css"), encoding="utf-8").read() + "\n" + open(os.path.join(TPL, "components.css"), encoding="utf-8").read()
        for extra in self.cfg.get("css", []):
            css += "\n" + open(os.path.join(self.dir, extra), encoding="utf-8").read()
        body = self.body()
        head = self.head()
        I18N = {}
        for l in self.langs:
            d = dict(self.I[l])
            m = LANG_META[l]
            d["__meta"] = {"dir": m[0], "label": m[1], "short": m[2]}
            I18N[l] = d
        calc = self.cfg.get("calc") if "calc" in self.secs else None
        CFG = {"langs": self.langs, "storage": self.cfg.get("storage_prefix", re.sub(r"\W", "_", self.filename[:24])),
               "email": self.b["email"], "whatsapp": self.b["whatsapp"], "themeLight": self.b["theme_color_light"], "themeDark": self.b["theme_color_dark"],
               "calc": {"inputs": [f["id"] for f in calc["inputs"]], "vars": calc.get("vars", []),
                        "outputs": [{"id": o["id"], "expr": o["expr"], "decimals": o.get("decimals", 0)} for o in calc["outputs"]]} if calc else None}
        js = open(os.path.join(TPL, "runtime.js"), encoding="utf-8").read()
        js = js.replace("/*I18N*/", "const I18N = " + json.dumps(I18N, ensure_ascii=False).replace("</", "<\\/") + ";")
        js = js.replace("/*CFG*/", "const CFG = " + json.dumps(CFG, ensure_ascii=False) + ";")
        doc = '<!DOCTYPE html>\n<html lang="en" dir="ltr" data-theme="light">\n<head>\n%s\n<style>\n%s\n</style>\n</head>\n<body>\n%s\n<script>\n%s\n</script>\n%s\n</body>\n</html>\n' % (
            head, css, body, js, self.chatwoot())
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, self.filename)
        with open(out, "w", encoding="utf-8") as f:
            f.write(doc)
        return out, len(doc.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("product_dir")
    ap.add_argument("--out", default=None, help="output folder (default: <product-dir>/dist)")
    ap.add_argument("--check", action="store_true", help="validate only")
    a = ap.parse_args()
    pg = Page(a.product_dir)
    if a.check:
        pg.body(); pg.head()
        probs = pg.check()
        print("\n".join(probs) if probs else "config OK")
        sys.exit(1 if probs else 0)
    out, size = pg.build(a.out or os.path.join(pg.dir, "dist"))
    probs = pg.check()
    for p in probs:
        print("WARN", p)
    print("built", out, "%.0f KB" % (size / 1024))
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
