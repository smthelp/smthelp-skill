#!/usr/bin/env python3
"""Generate N x 30s html-video segment templates from a spec JSON.

Usage: python3 gen_segment_templates.py spec.json
spec.json:
{
  "templates_root": "/Users/jasonwu/.workbuddy/tools/html-video/templates",
  "clips_dir": "/path/to/clips",
  "segments": [
    {"id": "myvideo-s1", "name": "Segment 1", "desc": "...", "eyebrow": "01 · Intro",
     "scenes": [{"t": "HEADLINE", "tag": "subtitle", "clip": "clip1a"}],
     "caps": [["caption text", 0.8, 6.76]]}
  ]
}
"""
import json, os, shutil, sys

def pct(sec):
    return round(sec / 30.0 * 100, 2)

def build_html(seg):
    scenes, caps = seg["scenes"], seg["caps"]
    sw = [0, 25.0, 50.0, 75.0]
    vis_css = []
    for i in range(4):
        s0 = sw[i]
        c = s0 + 25.0
        vis_css.append(
            f"@keyframes vis{i+1} {{ 0%,{s0}%{{opacity:0;transform:translateY(28px)}} {min(s0+1.3,99.9):.2f}%,{c-1.6:.2f}%{{opacity:1;transform:translateY(0)}} {c:.2f}%,100%{{opacity:0;transform:translateY(-22px)}} }}")
    cap_css = []
    for i, (txt, t0, t1) in enumerate(caps, 1):
        a, b = pct(t0 - 0.2), pct(t1 + 0.25)
        cap_css.append(
            f"@keyframes cap{i} {{0%,{max(a-0.8,0):.2f}%{{opacity:0}}{a:.2f}%,{b:.2f}%{{opacity:1}}{min(b+0.8,100):.2f}%,100%{{opacity:0}}}}")
    scenes_html = "\n".join(
        f'''      <section class="scene sc{n}">
        <div class="media"><video src="assets/{s['clip']}.mp4" autoplay muted loop playsinline preload="auto"></video><div class="shade"></div></div>
        <div class="eyebrow">{seg['eyebrow']}</div>
        <div class="h2">{s['t']}</div>
        <div class="tag">{s['tag']}</div>
      </section>''' for n, s in enumerate(scenes, 1))
    caps_html = "".join(f'        <div class="cap cap{i}">{c[0]}</div>\n' for i, c in enumerate(caps, 1))
    cap_classes = "".join(f".cap{i}{{animation:cap{i} 30s linear forwards}}" for i in range(1, len(caps) + 1))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>{seg['name']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;700;800&display=swap" rel="stylesheet" />
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1920px; height:1080px; overflow:hidden; background:#04090f; color:#f2f7fa; font-family:"Inter",system-ui,sans-serif; }}
.stage {{ position:absolute; inset:0; }}
.bg {{ position:absolute; inset:0; background:radial-gradient(1200px 700px at 76% 14%, rgba(0,179,176,0.18), transparent 60%), radial-gradient(900px 600px at 10% 90%, rgba(130,191,50,0.12), transparent 60%), linear-gradient(160deg,#071117 0%,#04090f 55%,#03070b 100%); }}
.scene {{ position:absolute; inset:0; opacity:0; display:flex; flex-direction:column; justify-content:center; padding:0 150px; z-index:2; }}
.media {{ position:absolute; inset:0; z-index:0; overflow:hidden; }}
.media video {{ width:100%; height:100%; object-fit:cover; }}
.media .shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(3,8,13,0.78) 0%, rgba(3,8,13,0.45) 45%, rgba(3,8,13,0.82) 100%); }}
.eyebrow {{ font-size:28px; letter-spacing:0.34em; text-transform:uppercase; color:#82bf32; font-weight:800; margin-bottom:22px; }}
.h2 {{ font-family:"Archivo Black","Inter",sans-serif; font-size:82px; line-height:1.06; color:#f7fbff; }}
.tag {{ font-size:34px; color:#c3d2de; margin-top:22px; letter-spacing:0.01em; }}
.logo {{ position:absolute; top:62px; right:150px; z-index:5; font-size:23px; font-weight:800; letter-spacing:0.18em; color:rgba(242,247,250,0.6); }}
{chr(10).join(vis_css)}
.sc1{{animation:vis1 30s linear forwards}}.sc2{{animation:vis2 30s linear forwards}}.sc3{{animation:vis3 30s linear forwards}}.sc4{{animation:vis4 30s linear forwards}}
@keyframes rise {{ from{{opacity:0;transform:translateY(24px)}} to{{opacity:1;transform:translateY(0)}} }}
.sc1 .h2{{animation:rise .7s ease both .3s}}.sc2 .h2{{animation:rise .7s ease both 8s}}.sc3 .h2{{animation:rise .7s ease both 15.5s}}.sc4 .h2{{animation:rise .7s ease both 23s}}
.captions {{ position:absolute; left:0; right:0; bottom:56px; text-align:center; pointer-events:none; z-index:60; }}
.cap {{ display:inline-block; opacity:0; max-width:1560px; text-align:center; font-size:37px; font-weight:600; line-height:1.35; color:#f7fbff; padding:15px 32px; background:rgba(3,8,13,0.7); border-radius:14px; border:1px solid rgba(255,255,255,0.12); backdrop-filter:blur(4px); }}
{chr(10).join(cap_css)}
{cap_classes}
.progress {{ position:absolute; left:0; bottom:0; height:8px; width:100%; z-index:70; background:rgba(255,255,255,0.06); }}
.progress > i {{ display:block; height:100%; width:100%; transform-origin:left; transform:scaleX(0); background:linear-gradient(90deg,#00b3b0,#82bf32); animation:grow 30s linear forwards; }}
@keyframes grow {{ to {{ transform:scaleX(1); }} }}
.blackout {{ position:absolute; inset:0; background:#03070b; opacity:0; z-index:80; pointer-events:none; animation:bo 30s linear forwards; }}
@keyframes bo {{ 0%,96%{{opacity:0}} 99%,100%{{opacity:1}} }}
</style>
</head>
<body>
<div class="stage">
  <div class="bg"></div>
  <div class="logo">SOUTHERN MACHINERY · SMThelp</div>
{scenes_html}
  <div class="captions">
{caps_html}  </div>
  <div class="progress"><i></i></div>
  <div class="blackout"></div>
</div>
</body>
</html>'''

def build_yaml(seg):
    return f'''spec_version: 1
id: {seg["id"]}
name: {seg["name"]}
description: >
  {seg.get("desc", seg["name"])}. 30s master, real product footage, burned-in English captions.
  Author-generated for Jason Wu / Southern Machinery.
engine: hyperframes
engine_version: ^0.4.0
source_entry: index.html
category: product-demo
subcategory: multi-scene
tags: [product, promo, southern-machinery]
best_for:
  - "SMT/THT equipment product showcase"
  - "B2B manufacturing promo"
output:
  formats: [mp4, webm]
  default_format: mp4
  resolution:
    default: {{ width: 1920, height: 1080 }}
    supported_aspects: ["16:9"]
  fps:
    default: 30
    supported: [30, 60]
  duration:
    type: variable
    min_sec: 25
    max_sec: 35
    default_sec: 30
  alpha: false
  audio: {{ supported: true, expected_inputs: [] }}
inputs:
  schema:
    type: object
    properties: {{}}
  examples: []
license:
  spdx: MIT
  attribution_required: false
  redistribution_allowed: true
  commercial_use: true
  notes: "Author-generated template for Southern Machinery (smthelp.com)."
author:
  name: "Southern Machinery / 机仔"
  url: "https://www.smthelp.com"
version: "1.0.0"
preview:
  poster: poster.svg
'''

def main():
    spec = json.load(open(sys.argv[1]))
    root, clips = spec["templates_root"], spec["clips_dir"]
    for seg in spec["segments"]:
        d = os.path.join(root, seg["id"])
        a = os.path.join(d, "assets")
        os.makedirs(a, exist_ok=True)
        for s in seg["scenes"]:
            src, dst = os.path.join(clips, s["clip"] + ".mp4"), os.path.join(a, s["clip"] + ".mp4")
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
        with open(os.path.join(d, "index.html"), "w") as f:
            f.write(build_html(seg))
        with open(os.path.join(d, "template.html-video.yaml"), "w") as f:
            f.write(build_yaml(seg))
        print("wrote", seg["id"])

if __name__ == "__main__":
    main()
