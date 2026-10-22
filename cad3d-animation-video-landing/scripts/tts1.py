import sys,json,asyncio
sys.argv=sys.argv[:1]
import importlib.util
src=open('tts.py').read().replace('asyncio.run(main())','')
exec(src)
async def m(ids):
    S=json.load(open('vo.json')); T=json.load(open('audio/vo_timing.json'))
    for s in S:
        if s['id'] in ids:
            for k in range(5):
                try: r=await one(s); break
                except Exception as e: print('retry',e); await asyncio.sleep(2)
            T=[r if x['id']==s['id'] else x for x in T]; print(r['id'],r['dur'])
    json.dump(T,open('audio/vo_timing.json','w'),indent=1)
import os
asyncio.run(m(os.environ['IDS'].split(',')))
