#!/bin/bash
# qc.sh <slug>: technical gate (resolution, fps, codecs, duration) + 12-frame sheet for visual check.
HERE=$(cd "$(dirname "$0")" && pwd)
s=$1; f=$(ls $SMV_PROJECT/final/${SMV_BATCH:-*}/*-$s-4k.mp4 2>/dev/null | head -1)
[ -f "$f" ] || { echo "E50 missing output for $s"; exit 1; }
r=$(ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate -show_entries format=duration -of compact=p=0:nk=1 "$f" | tr '\n' ' ')
echo "$s: $r"
python3 - "$r" "$s" <<'P'
import sys; r=sys.argv[1].split(); s=sys.argv[2]
v=r[0].split('|'); a=r[1].split('|'); d=float(r[-1])
bad=[]
if v[:4]!=['h264','3840','2160','30/1']: bad.append('video '+'|'.join(v))
if a[0]!='aac': bad.append('audio '+a[0])
if not 60<=d<=180: bad.append(f'duration {d:.1f}s outside 60-180')
print(('E51 '+s+' '+'; '.join(bad)) if bad else f'{s} PASS {d:.1f}s')
P
bash $HERE/sheet12.sh "$f" $SMV_PROJECT/build/$s.qc.jpg && echo "look at $SMV_PROJECT/build/$s.qc.jpg"
