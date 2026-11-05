#!/usr/bin/env python3
"""VO clips placed at scene starts + synthesized pad music, sidechain-ducked, loudnorm -> <work>/video/mix.wav
usage: audio_mix.py <job.json>   (music: job.video.music file, else a generated 4-chord pad)"""
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import load_job, W
job = load_job(sys.argv[1]); cfg = job['_cfg']['video']; P = job['_P']
TL = json.load(open(W(job, 'video', 'timeline.json'))); T = TL['total']; V = lambda f: W(job, 'video', f)
ins, flt = [], []
for i, s in enumerate(TL['scenes']):
    ins += ['-i', s['audio']]; d = int(s['start'] * 1000); flt.append(f'[{i}:a]aresample=48000,adelay={d}|{d}[a{i}]')
n = len(TL['scenes'])
flt.append(''.join(f'[a{i}]' for i in range(n)) + f'amix=inputs={n}:normalize=0,apad,atrim=0:{T}[vo]')
run = lambda *a: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
run(*ins, '-filter_complex', ';'.join(flt), '-map', '[vo]', '-ac', '2', '-ar', '48000', V('vo_full.wav'))
music = P(job.get('video', {}).get('music')) if job.get('video', {}).get('music') else None
if not music:
    ch = [[110, 164.81, 220, 261.63], [87.31, 174.61, 220, 261.63], [130.81, 196, 261.63, 329.63], [98, 196, 246.94, 293.66]]
    e = '(' + '+'.join(f"between(mod(t,16),{4*k},{4*k+4})*(" + '+'.join(f'sin(2*PI*{f}*t)+0.5*sin(2*PI*{f*2.003}*t)' for f in c) + ')' for k, c in enumerate(ch)) + ')*0.06*(0.6+0.4*sin(2*PI*t/4-PI/2))'
    run('-f', 'lavfi', '-i', f"aevalsrc='{e}':s=48000:d={T}", '-af', f'lowpass=f=1400,aecho=0.8:0.7:120|240:0.35|0.25,afade=t=in:d=2,afade=t=out:st={T-3}:d=3,volume=0.55', '-ac', '2', V('music.wav'))
    music = V('music.wav')
L = cfg['loudness_lufs']
run('-i', V('vo_full.wav'), '-i', music, '-filter_complex',
    f'[1:a]volume=1.1[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[0:a][md]amix=inputs=2:normalize=0,loudnorm=I={L}:TP=-1.5:LRA=11[out]',
    '-map', '[out]', '-ar', '48000', '-c:a', 'pcm_s16le', V('mix.wav'))
print('mix.wav', T, 's')
