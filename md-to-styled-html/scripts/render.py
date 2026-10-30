#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown -> 自包含 HTML（深色主题、侧栏导航、代码块一键复制）。

用法:
    python render.py <input.md> <output.html> [--accent amber|teal|violet|blue] [--light] [--lang auto|zh|en]

    --lang  auto（默认）按正文中文占比自动判断；渲染英文交付物时务必确认界面文案是英文，
            否则会给客户看到「复制 / 目录」这类中文按钮。

依赖: markdown  (pip install markdown)
"""
import argparse
import html
import re
import sys
from pathlib import Path

import markdown

ACCENTS = {
    "amber":  ("#f0a02c", "#7a4d0d"),
    "teal":   ("#39d0b8", "#0d5a4e"),
    "violet": ("#a78bfa", "#4c3a8a"),
    "blue":   ("#5aa9f5", "#1b4a7a"),
}

# 界面文案（正文语言与界面语言可以不同：英文交付物 = 英文正文 + 英文界面）
UI = {
    "zh": {"copy": "复制", "copied": "已复制 ✓", "toc": "目录", "html_lang": "zh-CN"},
    "en": {"copy": "Copy", "copied": "Copied ✓", "toc": "Contents", "html_lang": "en"},
}


def detect_lang(md_text: str) -> str:
    """正文中文占比 < 1% 判为英文交付物"""
    cjk = len(re.findall(r"[\u4e00-\u9fff]", md_text))
    return "en" if cjk / max(len(md_text), 1) < 0.01 else "zh"


def build(md_text: str, accent: str = "amber", light: bool = False,
          lang: str = "auto") -> str:
    ac, ac_d = ACCENTS.get(accent, ACCENTS["amber"])
    if lang == "auto":
        lang = detect_lang(md_text)
    ui = UI.get(lang, UI["zh"])

    if light:
        theme = dict(
            bg="#f7f8fa", panel="#ffffff", panel2="#eef1f6", line="#dfe3ea",
            tx="#1a1f2b", tx2="#4c5666", tx3="#8b93a3",
            code_bg="#f2f4f8", code_fg="#8a4b00", pre_bg="#ffffff",
            pre_fg="#1f4d45", h1_from="#1a1f2b",
        )
    else:
        theme = dict(
            bg="#0d1017", panel="#151922", panel2="#1b202b", line="#262d3b",
            tx="#e7ebf2", tx2="#a3adbe", tx3="#6f7a8c",
            code_bg="#232a37", code_fg=ac, pre_bg="#0a0d13",
            pre_fg="#b9e6dd", h1_from="#ffffff",
        )

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "attr_list", "sane_lists"],
    )
    body = md.convert(md_text)

    toc: list[tuple[str, str]] = []
    counter = [0]

    def repl_h2(m):
        counter[0] += 1
        hid = f"s{counter[0]}"
        inner = m.group(1)
        title = re.sub(r"<[^>]+>", "", inner).strip()
        toc.append((hid, title))
        cls = ' class="card"' if re.match(r"^(案例|Case|步骤|Step|模块)\s*\d", title) else ""
        return f'<h2 id="{hid}"{cls}>{inner}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", repl_h2, body, flags=re.S)

    def repl_pre(m):
        return (f'<div class="code-wrap"><button class="copy-btn" type="button">{ui["copy"]}</button>'
                f'<pre>{m.group(1)}</pre></div>')

    body = re.sub(r"<pre>(.*?)</pre>", repl_pre, body, flags=re.S)

    nav_items = []
    for hid, title in toc:
        m = re.match(r"^(案例|Case|步骤|Step|模块)\s*(\d+)\s*[｜|:：]?\s*(.*)$", title)
        if m:
            nav_items.append(
                f'<a class="nav-case" href="#{hid}"><span class="nav-num">{html.escape(m.group(2))}</span>'
                f'<span class="nav-txt">{html.escape(m.group(3) or title)}</span></a>'
            )
        else:
            nav_items.append(f'<a class="nav-plain" href="#{hid}">{html.escape(title)}</a>')
    nav_html = "\n".join(nav_items)

    # 给卡片式 h2 之后的内容包一层
    parts = re.split(r'(<h2 id="s\d+" class="card">.*?</h2>)', body, flags=re.S)
    out = []
    for i, part in enumerate(parts):
        if re.match(r'<h2 id="s\d+" class="card">', part):
            out.append(part)
            if i + 1 < len(parts):
                seg = parts[i + 1]
                nxt = re.search(r"<h2 ", seg)
                if nxt:
                    out.append('<div class="card-body">' + seg[: nxt.start()] + "</div>")
                    parts[i + 1] = seg[nxt.start():]
                else:
                    out.append('<div class="card-body">' + seg + "</div>")
                    parts[i + 1] = ""
        elif part:
            out.append(part)
    body = "".join(out)

    css = f"""
:root{{
  --bg:{theme['bg']}; --panel:{theme['panel']}; --panel2:{theme['panel2']}; --line:{theme['line']};
  --tx:{theme['tx']}; --tx2:{theme['tx2']}; --tx3:{theme['tx3']};
  --accent:{ac}; --accent-d:{ac_d}; --teal:#39d0b8; --green:#4ecb71;
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--tx);
  font-family:-apple-system,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif;
  font-size:15px;line-height:1.78;-webkit-font-smoothing:antialiased}}
.wrap{{display:flex;max-width:1280px;margin:0 auto;gap:36px;padding:0 28px}}
nav{{position:sticky;top:0;align-self:flex-start;height:100vh;overflow-y:auto;
  width:264px;flex:0 0 264px;padding:34px 0 60px;border-right:1px solid var(--line)}}
nav::-webkit-scrollbar{{width:6px}}
nav::-webkit-scrollbar-thumb{{background:#2c3444;border-radius:3px}}
.nav-title{{font-size:11px;letter-spacing:.16em;color:var(--tx3);text-transform:uppercase;
  margin:0 0 14px 12px;font-weight:600}}
.nav-case,.nav-plain{{display:flex;gap:10px;align-items:flex-start;text-decoration:none;
  padding:7px 12px;border-radius:8px;color:var(--tx2);font-size:13.5px;margin-bottom:2px;
  transition:background .15s,color .15s}}
.nav-case:hover,.nav-plain:hover{{background:var(--panel2);color:var(--tx)}}
.nav-num{{flex:0 0 20px;height:20px;border-radius:5px;background:var(--panel2);
  color:var(--accent);font-size:11.5px;font-weight:700;text-align:center;line-height:20px;
  border:1px solid var(--line)}}
.nav-txt{{flex:1;line-height:1.45}}
.nav-plain{{font-size:13px;color:var(--tx3)}}
main{{flex:1;min-width:0;padding:34px 0 100px;max-width:900px}}
h1{{font-size:31px;line-height:1.3;margin:0 0 8px;letter-spacing:-.02em;
  background:linear-gradient(96deg,{theme['h1_from']} 10%,var(--accent) 90%);
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}}
h2{{font-size:21px;margin:52px 0 16px;padding:0 0 12px;letter-spacing:-.01em;
  border-bottom:1px solid var(--line);color:{'#111' if light else '#fff'};scroll-margin-top:20px}}
h2.card{{border-bottom:none;padding:16px 20px;border-radius:12px 12px 0 0;
  background:linear-gradient(180deg,var(--panel2),var(--panel));
  border:1px solid var(--line);border-bottom:none;margin-bottom:0}}
h3{{font-size:16px;margin:30px 0 10px;color:var(--accent)}}
h3::before{{content:"▍";margin-right:7px;opacity:.55}}
h4{{font-size:14.5px;margin:22px 0 8px}}
p{{margin:11px 0;color:{theme['tx']}}}
strong{{color:{'#000' if light else '#fff'};font-weight:600}}
a{{color:var(--teal);text-decoration:none;border-bottom:1px solid rgba(57,208,184,.3)}}
hr{{border:none;border-top:1px solid var(--line);margin:44px 0}}
blockquote{{margin:18px 0;padding:12px 18px;background:rgba(240,160,44,.07);
  border-left:3px solid var(--accent);border-radius:0 8px 8px 0;color:var(--tx2)}}
blockquote p{{margin:5px 0;color:var(--tx2)}}
ul,ol{{padding-left:22px;margin:11px 0}}
li{{margin:5px 0}}
li::marker{{color:var(--tx3)}}
code{{background:{theme['code_bg']};border:1px solid var(--line);padding:1.5px 6px;
  border-radius:5px;font-size:13px;color:{theme['code_fg']};
  font-family:"SF Mono",Menlo,Consolas,monospace}}
table{{width:100%;border-collapse:separate;border-spacing:0;margin:18px 0;font-size:13.5px;
  border:1px solid var(--line);border-radius:10px;overflow:hidden}}
th{{background:var(--panel2);text-align:left;padding:10px 14px;font-weight:600;
  border-bottom:1px solid var(--line);white-space:nowrap}}
td{{padding:9px 14px;border-bottom:1px solid var(--line);vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.code-wrap{{position:relative;margin:16px 0}}
.code-wrap pre{{background:{theme['pre_bg']};border:1px solid var(--line);
  border-left:3px solid var(--teal);border-radius:0 10px 10px 0;
  padding:16px 18px;overflow-x:auto;margin:0}}
.code-wrap pre code{{background:none;border:none;padding:0;color:{theme['pre_fg']};
  font-size:13px;line-height:1.72;font-family:"SF Mono",Menlo,Consolas,monospace;white-space:pre-wrap}}
.copy-btn{{position:absolute;top:9px;right:9px;z-index:2;cursor:pointer;
  background:var(--panel2);color:var(--tx2);border:1px solid var(--line);border-radius:6px;
  padding:4px 11px;font-size:11.5px;font-family:inherit;opacity:0;transition:all .15s}}
.code-wrap:hover .copy-btn{{opacity:1}}
.copy-btn:hover{{background:var(--accent);color:#12151c;border-color:var(--accent)}}
.copy-btn.done{{background:var(--green);color:#0d1017;border-color:var(--green);opacity:1}}
.card-body{{border:1px solid var(--line);border-top:none;border-radius:0 0 12px 12px;
  padding:4px 20px 18px;background:var(--panel);margin-bottom:8px}}
@media (max-width:900px){{nav{{display:none}}.wrap{{padding:0 18px}}h1{{font-size:24px}}h2{{font-size:18px}}}}
@media print{{nav,.copy-btn{{display:none}}}}
"""

    js = """
document.querySelectorAll('.copy-btn').forEach(function(btn){
  btn.addEventListener('click', function(){
    var text = btn.parentElement.querySelector('pre').innerText;
    var done = function(){ btn.textContent='__COPIED__'; btn.classList.add('done');
      setTimeout(function(){ btn.textContent='__COPY__'; btn.classList.remove('done'); },1600); };
    if (navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(done).catch(function(){ fb(text,done); });
    } else { fb(text,done); }
  });
});
function fb(text,cb){
  var ta=document.createElement('textarea'); ta.value=text;
  ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select();
  try{ document.execCommand('copy'); cb(); }catch(e){}
  document.body.removeChild(ta);
}
var heads=[].slice.call(document.querySelectorAll('h2[id]'));
var links=[].slice.call(document.querySelectorAll('nav a'));
function sync(){
  var y=window.scrollY+120, cur=null;
  heads.forEach(function(h){ if(h.offsetTop<=y) cur=h.id; });
  links.forEach(function(a){ var on=a.getAttribute('href')==='#'+cur;
    a.style.background=on?'var(--panel2)':''; a.style.color=on?'#fff':''; });
}
window.addEventListener('scroll',sync,{passive:true}); sync();
"""

    js = (js.replace("__COPIED__", ui["copied"]).replace("__COPY__", ui["copy"]))

    h1m = re.search(r"^#\s+(.+?)\s*$", md_text, flags=re.M)
    doc_title = h1m.group(1).strip() if h1m else (toc[0][1] if toc else "Document")

    return f"""<!DOCTYPE html>
<html lang="{ui['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(doc_title)}</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
<nav><p class="nav-title">{ui['toc']}</p>
{nav_html}
</nav>
<main>
{body}
</main>
</div>
<script>{js}</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--accent", default="amber", choices=list(ACCENTS))
    ap.add_argument("--light", action="store_true")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"],
                    help="界面文案语言；auto = 按正文中文占比自动判断")
    a = ap.parse_args()
    text = Path(a.src).read_text(encoding="utf-8")
    doc = build(text, a.accent, a.light, a.lang)
    Path(a.out).write_text(doc, encoding="utf-8")
    print(f"OK -> {a.out} ({len(doc):,} chars)")


if __name__ == "__main__":
    sys.exit(main())
