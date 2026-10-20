#!/bin/bash
# usage: enc_all.sh l|p  (resumable: skips finished segments)
cd "$(dirname "$0")"; M=$1; N=${NSEG:-8}
for i in $(seq 0 $((N-1))); do f=../enc/${M}_$(printf %02d $i).mp4; [ -s $f ] && continue; nice -n 8 python3 encode.py $M $i $N || exit 1; done
CODE=${CODE:-PRODUCT} python3 encode.py $M final
