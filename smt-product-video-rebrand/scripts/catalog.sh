#!/bin/bash
# catalog.sh <clip.mp4> [step_seconds=1] -> numbered contact sheet (timestamp on each frame) to build the shot library.
# Use it to find clean ranges (a,b) and boxes to blur (logos, model text, title bars, Chinese UI, faces).
v=$1; st=${2:-1}; o=${v%.*}.catalog.jpg; T=$(mktemp -d)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
ffmpeg -v error -i "$v" -vf "fps=1/$st,scale=320:-2,drawtext=fontfile=$(dirname $0)/../assets/fonts/JetBrainsMono-Bold.ttf:text='%{pts\:hms}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6" $T/%04d.png
python3 - "$T" "$o" <<'P'
import sys, glob; from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+'/*.png')); im=Image.open(fs[0]); w,h=im.size; cols=8; rows=(len(fs)+cols-1)//cols
c=Image.new('RGB',(w*cols,h*rows))
for i,f in enumerate(fs): c.paste(Image.open(f),((i%cols)*w,(i//cols)*h))
c.save(sys.argv[2],quality=80); print(sys.argv[2], len(fs),'frames')
P
rm -rf $T
