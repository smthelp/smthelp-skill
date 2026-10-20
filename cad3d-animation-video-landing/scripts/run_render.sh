#!/bin/bash
PROJ=${PROJ:-$(cd "$(dirname "$0")/.." && pwd)}; export PROJ
E=$PROJ/env
bash $PROJ/build/setup_env.sh
export PLAYWRIGHT_BROWSERS_PATH=$E/browsers LD_LIBRARY_PATH=$E/libs/usr/lib/aarch64-linux-gnu
cd $PROJ/build
$E/venv/bin/python render.py $1 24 ${2:-1150}
