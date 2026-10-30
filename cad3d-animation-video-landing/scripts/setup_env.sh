#!/bin/bash
PROJ=${PROJ:-$(cd "$(dirname "$0")/.." && pwd)}; export PROJ
# persistent render env under the project (sandbox /tmp and $HOME get wiped)
E=$PROJ/env
export PLAYWRIGHT_BROWSERS_PATH=$E/browsers
if [ ! -x $E/venv/bin/python ]; then python3 -m venv $E/venv && $E/venv/bin/pip install -q playwright==1.47.0 pillow; fi
if [ ! -d $E/browsers/chromium-1134 ]; then $E/venv/bin/python -m playwright install chromium >/dev/null 2>&1; fi
if [ ! -d $E/libs/usr/lib/aarch64-linux-gnu ]; then
  mkdir -p $E/debs && cd $E/debs
  for u in pool/main/a/at-spi2-core/libatk-bridge2.0-0t64_2.56.2-1+deb13u2_arm64.deb pool/main/a/at-spi2-core/libatk1.0-0t64_2.56.2-1+deb13u2_arm64.deb pool/main/a/at-spi2-core/libatspi2.0-0t64_2.56.2-1+deb13u2_arm64.deb pool/main/libx/libxcomposite/libxcomposite1_0.4.6-1_arm64.deb pool/main/libx/libxdamage/libxdamage1_1.1.6-1+b2_arm64.deb; do curl -s -O http://deb.debian.org/debian/$u; done
  for d in *.deb; do dpkg -x $d $E/libs; done
fi
