#!/usr/bin/env python3
"""Concat rendered segments + mix.wav -> final MP4 (faststart written in /tmp then copied: the network FS fails on the trailer).
usage: finish_video.py <job.json> <169|916>"""
import sys, os, glob, subprocess, json
sys.path.insert(0, os.path.dirname(__file__))
from common import load_job, W
job = load_job(sys.argv[1]); fmt = sys.argv[2]
segs = sorted(glob.glob(W(job, 'out', f'seg_{fmt}_*.mp4')), key=lambda f: float(f.rsplit('_', 1)[1][:-4]))
segs = [s for s in segs if os.path.exists(s + '.done')]
lst = f'/tmp/concat_{fmt}.txt'; open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
name = f"{job['slug']}-{'16x9' if fmt == '169' else '9x16'}-4k.mp4"; tmp = '/tmp/' + name
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', W(job, 'video', 'mix.wav'), '-map', '0:v', '-map', '1:a',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', tmp], check=True)
subprocess.run(['cp', tmp, W(job, 'out', name)], check=True)
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height:format=duration', '-of', 'json', W(job, 'out', name)]))
TL = json.load(open(W(job, 'video', 'timeline.json')))
v = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]; dur = float(pr['format']['duration'])
ok = (v['width'], v['height']) == ((3840, 2160) if fmt == '169' else (2160, 3840)) and any(s['codec_type'] == 'audio' for s in pr['streams']) and abs(dur - TL['total']) < 1
print(('OK ' if ok else 'CHECK ') + name, v['width'], 'x', v['height'], round(dur, 2), 's', len(segs), 'segments')
