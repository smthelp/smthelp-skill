#!/bin/bash
# Rebuild the SMT stencil wiping paper landing page end to end. usage: bash landing-src/build_all.sh  (from anywhere)
set -e
K=$(cd "$(dirname "$0")/.." && pwd); S=/workspace/smthelp-skills-business/smt-product-landing-page/scripts
cd "$K"
python3 landing-src/en_strings.py landing/i18n/en.json
python3 landing-src/blogs.py landing/blogs.json
python3 landing-src/merge_tr.py es pt fr ar ru zh
python3 landing-src/tr2json.py es pt fr ar ru zh
mkdir -p landing/photos && cp assets/*.jpg landing/photos/
rm -rf landing/videos; python3 landing-src/make_product.py .
rm -rf out/landing; mkdir -p out/landing
python3 landing-src/build_page_ext.py landing --out out/landing
F=$(python3 -c "import json;print(json.load(open('landing/product.json'))['file'])")
[ -d landing/videos ] && mkdir -p out/landing/videos && cp landing/videos/*.mp4 out/landing/videos/
python3 $S/check_page.py landing out/landing/$F
rm -f out/SM-Stencil-Wiping-Paper-Landing-Page.zip
(cd out/landing && zip -qr ../SM-Stencil-Wiping-Paper-Landing-Page.zip "$F" $( [ -d videos ] && echo videos ))
ls -la out/landing out/landing/videos 2>/dev/null; unzip -l out/SM-Stencil-Wiping-Paper-Landing-Page.zip
