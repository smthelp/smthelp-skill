import os,asyncio,json,edge_tts,subprocess
for k in list(os.environ):
    if 'proxy' in k.lower(): del os.environ[k]
V="en-US-AndrewMultilingualNeural"
async def one(s):
    c=edge_tts.Communicate(s['text'],V,rate="+2%",boundary="WordBoundary")
    words=[]; f=open(f"audio/{s['id']}.mp3",'wb')
    async for ch in c.stream():
        if ch['type']=='audio': f.write(ch['data'])
        elif ch['type']=='WordBoundary': words.append([ch['offset']/1e7,(ch['offset']+ch['duration'])/1e7,ch['text']])
    f.close()
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f"audio/{s['id']}.mp3"]))
    return {'id':s['id'],'text':s['text'],'dur':dur,'words':words}
async def main():
    S=json.load(open('vo.json')); out=[]
    for s in S: out.append(await one(s)); print(out[-1]['id'],out[-1]['dur'],len(out[-1]['words']))
    json.dump(out,open('audio/vo_timing.json','w'),indent=1)
asyncio.run(main())
