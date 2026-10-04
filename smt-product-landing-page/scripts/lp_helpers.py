#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reusable renderer module for Southern Machinery product landing pages.
Template skeleton: assets/reference-s680a.html (same skill directory).

Usage in a batch build script:
    import os, sys
    os.environ["READY_DIR"] = "<dir with compressed jpgs>"   # before import
    sys.path.insert(0, "<skill scripts dir>")
    from lp_helpers import (data_uri, img, header_nav, hero_block, signals_block,
                            pain_block, fab_block, impact_block, specs_block,
                            gallery_block, videos_block, service_block, faq_block,
                            cta_block, footer_block, chat_block, assemble)
Then build page dicts and call assemble(...). FAB stations and the chat system
prompt are injected as <script type="application/json"> blocks (JSON.parse in JS),
so apostrophes/quotes in copy never break the page.
"""
import base64, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
READY = os.environ.get("READY_DIR", os.path.join(HERE, "assets", "ready"))
SKILL_ROOT = os.path.dirname(HERE)  # this file lives in <skill>/scripts/
REF = os.path.join(SKILL_ROOT, "assets", "reference-s680a.html")

# ---------- image helpers ----------
_cache = {}
def data_uri(name):
    if name not in _cache:
        p = os.path.join(READY, name)
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        _cache[name] = "data:image/jpeg;base64," + b64
    return _cache[name]

def img(name, alt, cls="", lazy=False, w=None, h=None):
    extra = f' class="{cls}"' if cls else ""
    extra += f' width="{w}" height="{h}"' if (w and h) else ""
    extra += ' loading="lazy"' if lazy else ""
    return f'<img src="{data_uri(name)}" alt="{alt}"{extra}>'

# ---------- read reference CSS (keep single <style>) ----------
ref = open(REF, encoding="utf-8").read()
css = re.search(r"<style>.*?</style>", ref, re.S).group(0)

# ---------- shared constants ----------
LOGO = data_uri("logo.jpg")
WA_LINK = "https://wa.me/8613602562576"
WA_TEXT = "Hi%20Jason%2C%20I%20would%20like%20a%20quote%20for%20the%20Southern%20Machinery%20radial%20insertion%20machine.%20Our%20board%20size%20and%20components%3A%20"

def header_nav(active_links):
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in active_links)
    return f"""  <div class="utility-bar">
    <div class="container utility-inner">
      <span>Southern Machinery · Shenzhen, China</span>
      <a href="tel:+8613602562576">+86 136 0256 2576</a>
      <a href="mailto:info@smthelp.com">info@smthelp.com</a>
    </div>
  </div>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="#overview" aria-label="Southern Machinery home">
        <img src="{LOGO}" alt="Southern Machinery" width="300" height="83">
      </a>
      <nav class="site-nav" id="site-nav" aria-label="Primary navigation">
        {links}
      </nav>
      <a class="btn primary header-cta" href="#contact">Get a Quote</a>
      <button class="nav-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="site-nav">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </header>"""

def hero_block(eyebrow, h1, p, note, images, aria_label):
    imgs = "".join(img(n, a, cls="hero-media") for n, a in images)
    return f"""    <section class="hero" id="overview" aria-labelledby="hero-title">
      <div class="hero-carousel" role="img" aria-label="{aria_label}">
        {imgs}
      </div>
      <div class="hero-copy">
        <p class="eyebrow">{eyebrow}</p>
        <h1 id="hero-title">{h1}</h1>
        <p>{p}</p>
        <div class="hero-actions">
          <a class="btn light" href="#contact">Request a Quote</a>
          <a class="btn ghost-light" href="#fab">Explore the FAB Value</a>
        </div>
        <p class="hero-note">{note}</p>
      </div>
    </section>"""

def signals_block(sigs):
    items = "".join(f'<div class="signal"><strong>{s[0]}</strong><span>{s[1]}</span></div>' for s in sigs)
    return f"""    <section class="signal-strip" aria-label="Product highlights">
      <div class="container signals">{items}</div>
    </section>"""

def pain_block(eyebrow, h2, p, items):
    cards = "".join(f'<article class="challenge"><h3>{t}</h3><p>{d}</p></article>' for t, d in items)
    return f"""    <section class="band" id="pain">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div class="challenge-grid">{cards}</div>
      </div>
    </section>"""

def fab_block(eyebrow, h2, p, stations):
    js = json.dumps(stations, ensure_ascii=False)
    return f"""    <section class="band soft" id="fab">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div class="system-shell">
          <div class="system-tabs" role="tablist" aria-label="Feature set"></div>
          <div class="system-detail" role="tabpanel" tabindex="0">
            <div class="system-image">
              <img id="system-image" alt="Product feature view">
              <span class="image-qualifier" id="image-qualifier">Source: Southern Machinery</span>
            </div>
            <div class="system-copy">
              <span class="model-code" id="system-model">Automation</span>
              <h2 id="system-name" style="font-size:30px;">Feature</h2>
              <p class="system-role" id="system-role">Feature description.</p>
              <div class="fab-row"><span class="fab-label">Feature</span><p id="system-feature"></p></div>
              <div class="fab-row"><span class="fab-label">Advantage</span><p id="system-advantage"></p></div>
              <div class="fab-row benefit"><span class="fab-label">Benefit</span><p id="system-benefit"></p></div>
              <div class="system-specs" id="system-specs"></div>
            </div>
          </div>
        </div>
        <noscript><p class="qualification">JavaScript is disabled. The specification table and gallery below remain available.</p></noscript>
      </div>
    </section>
    <script id="fab-data" type="application/json">{js}</script>"""

def impact_block(impacts):
    items = "".join(f'<article class="impact"><strong>{s[0]}</strong><p>{s[1]}</p></article>' for s in impacts)
    return f"""    <section class="band dark compact" aria-label="Operational impact">
      <div class="container impact-grid">{items}</div>
    </section>"""

def specs_block(groups, qualification, chips):
    gs = ""
    for title, span, rows in groups:
        trs = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
        gs += f"""        <section class="spec-group">
          <div class="spec-title"><h3>{title}</h3><span>{span}</span></div>
          <table class="spec-table"><tbody>{trs}</tbody></table>
        </section>"""
    chips_html = "".join(f"<span>{c}</span>" for c in chips)
    return f"""    <section class="band" id="specs">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Source-verified technical data</p>
          <h2>Key specifications for project evaluation</h2>
          <p>Values support initial evaluation and remain subject to final technical confirmation against your board size, component mix and line layout.</p>
        </div>
        {gs}
        <p class="qualification">{qualification}</p>
        <div class="interface-chips" aria-label="Compatibility and interfaces">{chips_html}</div>
      </div>
    </section>"""

def gallery_block(eyebrow, h2, p, items):
    btns = ""
    for name, alt, cap, title in items:
        btns += f'<button class="gallery-item" type="button" data-title="{title}">{img(name, alt, lazy=True)}<span>{cap}</span></button>'
    return f"""    <section class="band soft" id="gallery">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div class="gallery-grid">{btns}</div>
      </div>
    </section>"""

def videos_block(eyebrow, h2, p, videos, note):
    cards = ""
    for vid, poster, alt, h3, p2, load_label in videos:
        cards += f"""          <article class="video-card">
            <div class="video-stage">
              {img(poster, alt, lazy=True)}
              <button class="video-load" type="button" data-video="{vid}" data-title="{h3}">
                <span class="play-icon"><svg class="icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>
                <span>{load_label}</span>
              </button>
            </div>
            <div class="video-copy"><h3>{h3}</h3><p>{p2}</p></div>
          </article>"""
    return f"""    <section class="band" id="videos">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div class="video-grid">{cards}</div>
        <p class="offline-note" role="status">{note}</p>
      </div>
    </section>"""

def service_block(eyebrow, h2, p, steps):
    arts = "".join(f'<article class="service-step"><b>{t}</b><p>{d}</p></article>' for t, d in steps)
    return f"""    <section class="band soft" id="service">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div class="service-flow">{arts}</div>
      </div>
    </section>"""

def faq_block(eyebrow, h2, faqs):
    ds = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    return f"""    <section class="band" id="faq">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
        </div>
        <div class="faq-list">{ds}</div>
      </div>
    </section>"""

def cta_block(eyebrow, h2, p, email_subj, wa_text):
    return f"""    <section class="band cta-band" id="contact">
      <div class="container cta-grid">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div class="cta-actions">
          <a class="btn light" href="mailto:info@smthelp.com?subject={email_subj}">Email for a Quote</a>
          <a class="btn wa" href="https://wa.me/8613602562576?text={wa_text}" target="_blank" rel="noopener">Click to chat on WhatsApp</a>
        </div>
      </div>
    </section>"""

def footer_block(product_links, resource_links):
    pl = "".join(f'<a href="{h}">{t}</a>' for h, t in product_links)
    rl = "".join(f'<a href="{h}" target="_blank" rel="noopener">{t}</a>' for h, t in resource_links)
    return f"""  <footer>
    <div class="container footer-grid">
      <div class="footer-brand">
        <img src="{LOGO}" alt="Southern Machinery" width="300" height="83">
        <p>Automation Partner, Not Supplier. Complete SMT and THT automation solutions for high-mix EMS and electronics factories.</p>
        <div class="social-links" aria-label="Social links">
          <a href="https://www.linkedin.com/company/smtmachine" target="_blank" rel="noopener">LinkedIn Company Page</a>
          <a href="https://cn.linkedin.com/in/smtsupplier" target="_blank" rel="noopener">LinkedIn Profile</a>
          <a href="https://twitter.com/smtspecialist" target="_blank" rel="noopener">Twitter</a>
          <a href="https://www.facebook.com/autoinsertion" target="_blank" rel="noopener">Facebook</a>
          <a href="https://www.youtube.com/c/Smthelping" target="_blank" rel="noopener">YouTube Channel</a>
        </div>
      </div>
      <div class="footer-col">
        <h3>Product</h3>
        {pl}
      </div>
      <div class="footer-col">
        <h3>Resources</h3>
        {rl}
      </div>
      <div class="footer-col">
        <h3>Contact</h3>
        <a href="mailto:info@smthelp.com">info@smthelp.com</a>
        <a href="tel:+8613602562576">+86 136 0256 2576</a>
        <a href="https://wa.me/8613602562576" target="_blank" rel="noopener">WhatsApp chat</a>
        <a href="https://www.smthelp.com" target="_blank" rel="noopener">www.smthelp.com</a>
        <p>Xixiang, Bao'an District<br>Shenzhen, China</p>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container">
        <span>Browse our machine catalog at <a href="https://file.autoinsertion.com" target="_blank" rel="noopener" style="color:inherit;">file.autoinsertion.com</a> and find machine photos at <a href="https://ph.smthelp.com" target="_blank" rel="noopener" style="color:inherit;">ph.smthelp.com</a>.</span>
        <span>© 2026 Southern Machinery Co., Ltd. · Technical content requires human review before external use.</span>
      </div>
    </div>
  </footer>"""

def floating_blocks():
    return f"""  <dialog id="lightbox" aria-labelledby="lightbox-title">
    <div class="dialog-bar">
      <strong id="lightbox-title">Product image</strong>
      <button class="icon-button" type="button" aria-label="Close image">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>
    <img class="dialog-image" alt="">
  </dialog>
  <button class="back-to-top" type="button" aria-label="Back to top">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
  </button>
  <a class="whatsapp-fab" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Click to chat with me on WhatsApp">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20.5 11.5a8.5 8.5 0 0 1-12.6 7.4L3.5 20l1.2-4.2A8.5 8.5 0 1 1 20.5 11.5Z"/><path d="M8.5 8.3c.3 2.9 2.4 5 5.2 5.4M13.8 13.7l1.7-1M8.5 8.3l1.2-1.5"/></svg>
  </a>"""

def chat_block(product, advisor_label, intro_http, intro_file, system_prompt):
    sp = json.dumps(system_prompt)
    return f"""  <button class="chat-fab" id="chat-fab" type="button" aria-expanded="false" aria-controls="chat-panel">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3a7 7 0 0 1 7 7c0 2.4-1.2 4.5-3 5.7V18a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2v-2.3c-1.8-1.2-3-3.3-3-5.7a7 7 0 0 1 7-7Z"/><path d="M9 21h6"/></svg>
    Ask the {advisor_label}
  </button>
  <section class="chat-panel" id="chat-panel" role="dialog" aria-label="{product} product advisor chat" hidden>
    <header class="chat-head">
      <div>
        <strong>{product} Product Advisor</strong>
        <small>AI answers about this machine · powered by Puter.js</small>
      </div>
      <button class="icon-button" id="chat-close" type="button" aria-label="Close chat">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </header>
    <div class="chat-log" id="chat-log" aria-live="polite"></div>
    <form class="chat-form" id="chat-form">
      <input id="chat-input" type="text" autocomplete="off" placeholder="Ask about specs, compatibility, maintenance…" aria-label="Your question about the {product}">
      <button id="chat-send" type="submit">Send</button>
    </form>
  </section>
  <script id="chat-prompt" type="application/json">{sp}</script>"""

JS = """  <script>
    (() => {
      const navToggle = document.querySelector('.nav-toggle');
      const nav = document.getElementById('site-nav');
      navToggle.addEventListener('click', () => {
        const open = nav.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', String(open));
        document.body.classList.toggle('menu-open', open);
      });
      nav.addEventListener('click', (e) => {
        if (e.target.tagName === 'A') {
          nav.classList.remove('open');
          document.body.classList.remove('menu-open');
          navToggle.setAttribute('aria-expanded', 'false');
        }
      });

      const stations = JSON.parse(document.getElementById('fab-data').textContent);
      const tabs = document.querySelector('.system-tabs');
      const fields = {
        image: document.getElementById('system-image'),
        qualifier: document.getElementById('image-qualifier'),
        model: document.getElementById('system-model'),
        name: document.getElementById('system-name'),
        role: document.getElementById('system-role'),
        feature: document.getElementById('system-feature'),
        advantage: document.getElementById('system-advantage'),
        benefit: document.getElementById('system-benefit'),
        specs: document.getElementById('system-specs')
      };
      function activateStation(index, moveFocus = false) {
        const station = stations[index];
        if (!station) return;
        [...tabs.children].forEach((tab, tabIndex) => {
          const selected = tabIndex === index;
          tab.setAttribute('aria-selected', String(selected));
          tab.tabIndex = selected ? 0 : -1;
          if (selected && moveFocus) tab.focus();
        });
        fields.image.src = station.image;
        fields.image.alt = station.alt;
        fields.qualifier.textContent = station.qualifier;
        fields.model.textContent = station.model;
        fields.name.textContent = station.name;
        fields.role.textContent = station.role;
        fields.feature.textContent = station.feature;
        fields.advantage.textContent = station.advantage;
        fields.benefit.textContent = station.benefit;
        fields.specs.innerHTML = station.specs.map((s) => `<span>${s}</span>`).join('');
      }
      stations.forEach((station, index) => {
        const tab = document.createElement('button');
        tab.className = 'system-tab';
        tab.type = 'button';
        tab.role = 'tab';
        tab.textContent = station.tab;
        tab.addEventListener('click', () => activateStation(index));
        tab.addEventListener('keydown', (e) => {
          if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
            e.preventDefault();
            const next = e.key === 'ArrowRight' ? (index + 1) % stations.length : (index - 1 + stations.length) % stations.length;
            activateStation(next, true);
          }
        });
        tabs.appendChild(tab);
      });
      activateStation(0);

      const lightbox = document.getElementById('lightbox');
      const lightboxTitle = document.getElementById('lightbox-title');
      const lightboxImage = lightbox.querySelector('.dialog-image');
      document.querySelectorAll('.gallery-item').forEach((item) => {
        item.addEventListener('click', () => {
          const im = item.querySelector('img');
          lightboxTitle.textContent = item.dataset.title || 'Product image';
          lightboxImage.src = im.src;
          lightboxImage.alt = im.alt;
          lightbox.showModal();
        });
      });
      lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox || e.target.closest('.icon-button')) lightbox.close();
      });

      document.querySelectorAll('.video-load').forEach((btn) => {
        btn.addEventListener('click', () => {
          const stage = btn.closest('.video-stage');
          const iframe = document.createElement('iframe');
          iframe.src = `https://www.youtube.com/embed/${btn.dataset.video}?autoplay=1&title=${encodeURIComponent(btn.dataset.title || '')}`;
          iframe.title = btn.dataset.title || 'Southern Machinery video';
          iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
          iframe.allowFullscreen = true;
          stage.innerHTML = '';
          stage.appendChild(iframe);
        });
      });

      const setOnline = () => document.body.classList.toggle('is-offline', !navigator.onLine);
      window.addEventListener('online', setOnline);
      window.addEventListener('offline', setOnline);
      setOnline();

      const topBtn = document.querySelector('.back-to-top');
      window.addEventListener('scroll', () => {
        topBtn.classList.toggle('visible', window.scrollY > 600);
      }, { passive: true });
      topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

      const servedOverHttp = location.protocol === 'http:' || location.protocol === 'https:';
      let puterReady = null;
      function loadPuter() {
        if (!puterReady) {
          puterReady = new Promise((resolve, reject) => {
            if (window.puter && window.puter.ai) return resolve();
            const s = document.createElement('script');
            s.src = 'https://js.puter.com/v2/';
            s.async = true;
            s.onload = () => (window.puter && window.puter.ai ? resolve() : reject(new Error('puter unavailable')));
            s.onerror = () => reject(new Error('puter load failed'));
            document.head.appendChild(s);
          });
        }
        return puterReady;
      }

      const SYSTEM_PROMPT = JSON.parse(document.getElementById('chat-prompt').textContent);

      const chatFab = document.getElementById('chat-fab');
      const chatPanel = document.getElementById('chat-panel');
      const chatClose = document.getElementById('chat-close');
      const chatLog = document.getElementById('chat-log');
      const chatForm = document.getElementById('chat-form');
      const chatInput = document.getElementById('chat-input');
      const chatSend = document.getElementById('chat-send');
      let history = [];
      function addMsg(role, text) {
        const div = document.createElement('div');
        div.className = 'chat-msg ' + (role === 'user' ? 'user' : role === 'err' ? 'err' : 'bot');
        div.textContent = text;
        chatLog.appendChild(div);
        chatLog.scrollTop = chatLog.scrollHeight;
        return div;
      }
      chatFab.addEventListener('click', () => {
        const open = chatPanel.hidden;
        chatPanel.hidden = !open;
        chatFab.setAttribute('aria-expanded', String(open));
        if (open) {
          if (!chatLog.children.length) {
            if (servedOverHttp) {
              addMsg('bot', INTRO_HTTP_PLACEHOLDER);
            } else {
              addMsg('bot', INTRO_FILE_PLACEHOLDER);
            }
          }
          chatInput.focus();
        }
      });
      chatClose.addEventListener('click', () => {
        chatPanel.hidden = true;
        chatFab.setAttribute('aria-expanded', 'false');
      });
      chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = chatInput.value.trim();
        if (!question) return;
        addMsg('user', question);
        chatInput.value = '';
        chatSend.disabled = true;
        const thinking = addMsg('bot', 'Thinking…');
        const fail = () => {
          thinking.className = 'chat-msg err';
          thinking.textContent = 'The AI advisor is not reachable here. Please email info@smthelp.com or WhatsApp +86 136 0256 2576 — we reply within one working day.';
          chatSend.disabled = false;
          chatInput.focus();
        };
        if (!servedOverHttp) { fail(); return; }
        try {
          await loadPuter();
          history.push({ role: 'user', content: question });
          const chatCall = puter.ai.chat([{ role: 'system', content: SYSTEM_PROMPT }, ...history]);
          const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 90000));
          const response = await Promise.race([chatCall, timeout]);
          const text = (response && (response.message?.content || response.text)) || String(response);
          history.push({ role: 'assistant', content: text });
          thinking.textContent = text;
        } catch (err) {
          fail();
          return;
        }
        chatSend.disabled = false;
        chatLog.scrollTop = chatLog.scrollHeight;
        chatInput.focus();
      });
    })();
  </script>"""

def assemble(meta_desc, meta_kw, title, nav, body_extra, main_html, footer, chat_html, intro_http, intro_file):
    js = JS.replace("INTRO_HTTP_PLACEHOLDER", json.dumps(intro_http)).replace("INTRO_FILE_PLACEHOLDER", json.dumps(intro_file))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{meta_kw}">
  <meta name="theme-color" content="#009fa5">
  <title>{title}</title>
  {css}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  {nav}
  <main id="main">
    {main_html}
    {body_extra}
  </main>
  {footer}
  {floating_blocks()}
  {chat_html}
  {js}
</body>
</html>"""


# ---------- batch-3 bands: equipment options / ROI / installation guide ----------
def options_band(eyebrow, h2, p, items):
    """Equipment-option recommendation cards (3-col grid). items = [(title, sub, desc), ...]"""
    cards = ""
    for sub, title, desc in items:
        cards += f"""          <article class="service-step" style="background:var(--soft);padding:20px;border-top:4px solid var(--teal);">
            <b>{title}</b><p style="color:var(--teal-dark);font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px;">{sub}</p><p>{desc}</p>
          </article>"""
    return f"""    <section class="band" id="options">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div class="service-flow" style="grid-template-columns:repeat(3,1fr);">{cards}</div>
      </div>
    </section>"""

def roi_band(numbers, note):
    """Dark 4-number ROI band + a qualification-style ROI explanation."""
    items = "".join(f'<article class="impact"><strong>{s[0]}</strong><p>{s[1]}</p></article>' for s in numbers)
    return f"""    <section class="band dark compact" aria-label="ROI">
      <div class="container impact-grid">{items}</div>
      <div class="container" style="margin-top:26px;"><p class="qualification" style="background:rgba(255,255,255,.08);border-left-color:var(--lime);color:#d9e0e1;max-width:900px;">{note}</p></div>
    </section>"""

def install_band(eyebrow, h2, p, steps, utilities):
    """Installation guide: 5 service-style steps + utility chips."""
    arts = "".join(f'<article class="service-step"><b>{t}</b><p>{d}</p></article>' for t, d in steps)
    ut = "".join(f"<span>{u}</span>" for u in utilities)
    return f"""    <section class="band soft" id="install">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div class="service-flow">{arts}</div>
        <div class="interface-chips" aria-label="Installation requirements">{ut}</div>
      </div>
    </section>"""


def doc_band(eyebrow, h2, p, docs):
    """Downloadable-catalog cards (3-col). docs = [(title, desc, url), ...]; place before FAQ."""
    cards = ""
    for title, desc, url in docs:
        cards += f"""          <article style="border:1px solid var(--line);border-radius:4px;background:white;padding:22px;display:flex;flex-direction:column;gap:10px;">
            <h3 style="margin-bottom:0;font-size:17px;">{title}</h3>
            <p style="color:var(--muted);font-size:13.5px;margin:0;flex:1;">{desc}</p>
            <a class="btn secondary" href="{url}" target="_blank" rel="noopener" style="align-self:flex-start;text-decoration:none;">Open the PDF</a>
          </article>"""
    return f"""    <section class="band soft" id="documents">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p>{p}</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">
{cards}
        </div>
      </div>
    </section>"""
