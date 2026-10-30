#!/bin/bash
cd $(dirname $0)
R3D=${R3D:-0.6} AA=0 bash run_render.sh $1 ${BUDGET:-1140} > ../work/r_$1.log 2>&1
tail -1 ../work/r_$1.log
