#!/usr/bin/env python3
"""timing.json -> timeline.json + subtitles_en.srt + build/timeline.js.  usage: timeline.py <job.json>
job.video.phrases: [[spoken, caption], ...] maps TTS-friendly words back to numbers/symbols in captions.
job.video.keywords: {scene_id: [word prefixes]} -> scene.steps (times) used to reveal callouts on cue."""
import json,re,os,sys
sys.path.insert(0, os.path.dirname(__file__))
from common import load_job, W
job=load_job(sys.argv[1]); V=job.get('video',{})
S=json.load(open(W(job,'video','timing.json')))
LEAD=0.8; GAP=0.55; TAIL=3.0
PH=[tuple(x) for x in V.get('phrases',[])]
PH.sort(key=lambda x:-len(x[0].split()))
norm=lambda w: re.sub(r'[^a-z0-9]','',w.lower())
KEY=V.get('keywords',{})
t=LEAD; scenes=[]; cues=[]
for s in S:
    toks=s['text'].split(); times=[None]*len(toks)
    j=0
    for (a,b,w) in s['words']:
        nw=norm(w)
        for k in range(j,min(j+6,len(toks))):
            if nw and (norm(toks[k])==nw or norm(toks[k]).startswith(nw) or nw.startswith(norm(toks[k]) or '#')):
                times[k]=(a,b); j=k+1; break
    # fill gaps
    for k in range(len(toks)):
        if times[k] is None:
            prev=next((times[i] for i in range(k-1,-1,-1) if times[i]),(0,0))
            times[k]=(prev[1],prev[1]+0.2)
    # merge phrases
    D=[]; k=0
    while k<len(toks):
        hit=False
        for p,rep in PH:
            pw=p.split(); n=len(pw)
            if [norm(x) for x in toks[k:k+n]]==[norm(x) for x in pw]:
                tail=re.sub(r'^.*?([.,!?]*)$',r'\1',toks[k+n-1])
                D.append([rep+tail,times[k][0],times[k+n-1][1]]); k+=n; hit=True; break
        if not hit: D.append([toks[k],times[k][0],times[k][1]]); k+=1
    # chunk
    chunk=[]
    def flush():
        if chunk: cues.append({'s':round(t+chunk[0][1],3),'e':round(t+chunk[-1][2]+0.25,3),'text':' '.join(c[0] for c in chunk)})
    rem=[0]*len(D); c=0
    for i in range(len(D)-1,-1,-1):
        if D[i][0][-1] in '.?!': c=0
        rem[i]=c; c+=1
    for i,d in enumerate(D):
        chunk.append(d); txt=' '.join(c[0] for c in chunk)
        if d[0][-1] in '.?!' or (d[0][-1]==',' and len(txt)>22 and rem[i]>2) or (len(txt)>38 and rem[i]>2) or len(txt)>54:
            flush(); chunk=[]
    flush(); chunk=[]
    steps=[]
    for kw in KEY.get(s['id'],[]):
        hit=next((t+d[1] for d in D if norm(d[0]).startswith(kw) and t+d[1]>=(steps[-1] if steps else 0)),None)
        steps.append(round(hit,3) if hit else (steps[-1] if steps else t))
    scenes.append({'id':s['id'],'start':round(t,3),'dur':round(s['dur'],3),'audio':s.get('audio',W(job,'video',f"vo_{s['id']}.mp3")),'steps':steps})
    t+=s['dur']+GAP
total=round(t-GAP+TAIL,2)
# make cue ends not overlap next
for a,b in zip(cues,cues[1:]): a['e']=min(a['e'],b['s']-0.02)
TLD={'total':total,'scenes':scenes,'cues':cues}
json.dump(TLD,open(W(job,'video','timeline.json'),'w'),indent=1)
open(W(job,'build','timeline.js'),'w').write('window.TIMELINE='+json.dumps(TLD)+';')
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:02}:{m:02}:{s:06.3f}".replace('.',',')
with open(W(job,'out','subtitles_en.srt'),'w') as f:
    for i,c in enumerate(cues,1): f.write(f"{i}\n{ts(c['s'])} --> {ts(c['e'])}\n{c['text']}\n\n")
print(total,len(cues)); print([ (x['id'],x['steps']) for x in scenes if x['steps']])

