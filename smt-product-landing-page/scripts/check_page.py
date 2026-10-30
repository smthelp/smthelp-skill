#!/usr/bin/env python3
"""Quality gate for a built page and its product dir.

usage: check_page.py <product_dir> <built.html>
Checks: identical i18n key sets in all 7 languages; ar is rtl; banned method words
(hook, diagnosis, framework, vehicle, loop, CTA and their zh forms) absent from every
heading/title string in every language; every data-i18n key exists; JSON-LD parses;
inline scripts compile (needs node); Chatwoot token present; required footer links present.
Exit code 1 on any failure.
"""
import json, re, sys, os, subprocess
pd, page = sys.argv[1], sys.argv[2]
L = ["en", "es", "pt", "fr", "ar", "ru", "zh"]
D = {l: json.load(open(os.path.join(pd, "i18n", l + ".json"), encoding="utf-8")) for l in L}
fail = []
for l in L:
    if set(D[l]) != set(D["en"]): fail.append(f"{l}: key set differs ({len(set(D['en'])^set(D[l]))} keys)")
if D["ar"]["__meta"].get("dir") != "rtl": fail.append("ar __meta.dir must be rtl")
BAN = re.compile(r"(?i)\b(hook|diagnosis|framework|vehicle|loop|cta)\b|钩子|诊断|框架|载体|循环|行动号召")
TITLE = re.compile(r"(t|_h2|_h|title|h1a|h1b)$|^q\d+$|^bl\d+t$")
for l in L:
    for k, v in D[l].items():
        if k != "__meta" and TITLE.search(k) and BAN.search(v): fail.append(f"banned word in {l}.{k}: {v}")
h = open(page, encoding="utf-8").read()
for m in re.finditer(r"<(h[1-6]|title|summary)[^>]*>(.*?)</\1>", h, re.S):
    s = re.sub("<[^>]+>", "", m.group(2))
    if BAN.search(s): fail.append("banned word in heading: " + s[:80])
for k in set(re.findall(r'data-i18n(?:-alt|-aria|-title)?="([^"]+)"', h)):
    if k not in D["en"]: fail.append("missing key " + k)
try: json.loads(re.search(r'application/ld\+json">(.*?)</script>', h, re.S).group(1))
except Exception as e: fail.append("JSON-LD: " + str(e))
for need in ["saMcpgSupcmd1VQwytgPLfbK", "Southern-Machinery-logo-300x83.png", "linkedin.com/company/smtmachine",
             "linkedin.com/in/smtsupplier", "twitter.com/smtspecialist", "facebook.com/autoinsertion",
             "youtube.com/c/Smthelping", "file.autoinsertion.com", "ph.smthelp.com", "info@smthelp.com", "wa.me/8613602562576"]:
    if need not in h: fail.append("missing " + need)
js = "const fs=require('fs');const h=fs.readFileSync(process.argv[1],'utf8');[...h.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].forEach((m,i)=>{try{new Function(m[1])}catch(e){console.log('script '+i+': '+e.message);process.exitCode=1}})"
try:
    r = subprocess.run(["node", "-e", js, page], capture_output=True, text=True)
    if r.returncode: fail.append(r.stdout.strip())
except FileNotFoundError: print("node not found - script compile check skipped")
print("\n".join(fail) if fail else "OK: all checks passed")
sys.exit(1 if fail else 0)
