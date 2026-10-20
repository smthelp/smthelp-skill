import json,numpy as np,subprocess,wave
tl=json.load(open('timeline_l.json')); total=tl['total']
sr=48000; n=int((total+0.5)*sr); t=np.arange(n)/sr
def note(f): return 440*2**((f-69)/12)
prog=[[57,60,64,69],[53,57,60,65],[48,52,55,60],[55,59,62,67]]  # Am F C G
bar=4.0; mus=np.zeros(n)
for i in range(int(total/bar)+2):
    ch=prog[i%4]; s=int(i*bar*sr); e=min(n,int((i+1)*bar*sr+sr*1.5))
    if s>=n: break
    tt=t[s:e]-i*bar; env=np.minimum(1,tt/1.2)*np.exp(-np.maximum(0,tt-bar)*2.5)
    for k,m in enumerate(ch):
        f=note(m-12 if k==0 else m)
        mus[s:e]+=env*(0.5*np.sin(2*np.pi*f*tt)+0.18*np.sin(2*np.pi*2*f*tt+0.3)+0.08*np.sin(2*np.pi*3*f*tt))*(0.9 if k else 1.2)
    # soft pluck pulse 8th notes
    for j in range(8):
        ps=s+int(j*bar/8*sr); pe=min(n,ps+int(0.35*sr))
        if ps>=n: break
        pt=t[ps:pe]-t[ps]; f=note(ch[(j*2)%4]+12)
        mus[ps:pe]+=0.22*np.exp(-pt*9)*np.sin(2*np.pi*f*pt)
# low pass-ish smoothing
k=np.ones(6)/6; mus=np.convolve(mus,k,'same')
fade=np.minimum(1,t/2.0)*np.minimum(1,np.maximum(0,(total-t))/2.5)
mus=mus*fade; mus/=np.abs(mus).max()+1e-9; mus*=0.5
st=np.stack([mus,np.roll(mus,int(0.012*sr))],1)
w=wave.open('audio/music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
# voice track
inputs=[]; filt=[]
for i,s in enumerate(tl['scenes']):
    inputs+=['-i',f"audio/{s['id']}.mp3"]; d=int(s['voStart']*1000)
    filt.append(f"[{i}:a]aresample=48000,adelay={d}|{d},apad[v{i}]")
N=len(tl['scenes'])
filt.append(''.join(f'[v{i}]' for i in range(N))+f"amix=inputs={N}:normalize=0,atrim=0:{total:.3f},pan=stereo|c0=c0|c1=c0,loudnorm=I=-16:TP=-1.5:LRA=11[vo]")
subprocess.run(['ffmpeg','-y','-v','error',*inputs,'-filter_complex',';'.join(filt),'-map','[vo]','-ar','48000','audio/vo_full.wav'],check=True)
# duck music under VO and mix
subprocess.run(['ffmpeg','-y','-v','error','-i','audio/vo_full.wav','-i','audio/music.wav','-filter_complex',
 "[1:a]volume=0.22[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[0:a][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[out]",
 '-map','[out]','-ar','48000','-c:a','pcm_s16le','audio/final_mix.wav'],check=True)
print(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','audio/final_mix.wav']).decode())
