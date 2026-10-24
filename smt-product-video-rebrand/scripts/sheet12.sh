#!/bin/bash
# sheet12.sh video.mp4 out.jpg -> 12 evenly spaced frames, 4x3 grid at 640x360 (look at it!)
v=$1; o=$2; D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $v); T=$(mktemp -d)
for i in $(seq 0 11); do t=$(python3 -c "print(round(1.5+($D-3)*$i/11,2))"); ffmpeg -v error -y -ss $t -i $v -frames:v 1 -vf scale=640:360 -update 1 $T/$i.png; done
python3 -c "
from PIL import Image
c=Image.new('RGB',(2560,1080))
for k in range(12): c.paste(Image.open('$T/%d.png'%k),((k%4)*640,(k//4)*360))
c.save('$o',quality=85)"
rm -rf $T
