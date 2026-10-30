# SBF1001: classify 439 unnamed bodies into named groups by id + geometry, pack quantized
import json,numpy as np,gzip,base64,struct,collections
d=json.load(open('../src/mesh.json'))
O=np.array([-14.0,-572.0,897.0])   # origin: floor, centre of cart footprint
S=1300.0/32767
R=lambda a,b:set(range(a,b+1,5))
ID=dict(
 bowl={456,401}|R(421,451), drive={471}, rubber=R(461,481), stud=R(496,551)|{131,246}, mount={556},
 top={641}, ebox={761,736,756,716,721,726,746,751,656,671}, handle={1051,1056},
 cam={211}, light={216}, clamp={186,191,196,201,206,221,226,231,236,241},
 hmi={176,136,181,151,161,156,166,146}, screen={171,141},
 lindrive={586,591,596,416}, counter={601}, liniso=R(561,581),
 bracket={626,606,616,621,631,636,486,491,251,256,261,266,271},
 rail={411,406}, station_plate={611}, station={121,16,46,41,71,81,61,66}|R(86,116), stopper={21,26,31,36}|R(1,11)|R(51,56)|{126,76,91},
 caster_plate=R(1271,1286),
)
def classify(r,c,s):
    i=r['id']; p=r['path']
    if 'logo' in p[3]: return 'logo'
    if 2033<=i<=2198: return 'logo'
    for k,v in ID.items():
        if i in v: return k
    if c[1]<-30:
        if c[1]<-430: return 'caster'
        if min(s)<=3 and sorted(s)[1]>=100: return 'panel'
        return 'alu'
    if c[2]>1000 and 300<c[1]<340 and max(s)<20: return 'rail'
    return 'steel'
groups=collections.defaultdict(lambda:([],[]))
for r in d:
    if 'pos' not in r: continue
    M=np.array(r['mat']).reshape(4,4).T
    p=np.array(r['pos']).reshape(-1,3); n=np.array(r['nor']).reshape(-1,3)
    p=(np.c_[p,np.ones(len(p))]@M.T)[:,:3]*1000
    n=n@M[:3,:3].T; n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-9
    lo,hi=p.min(0),p.max(0); g=classify(r,(lo+hi)/2,hi-lo)
    groups[g][0].append(p-O); groups[g][1].append(n)
parts=[];bufs=[];off=0
pad=lambda b:b+b'\0'*((-len(b))%4)
for nm,(P,N) in groups.items():
    p=np.concatenate(P); n=np.concatenate(N)
    qp=np.round(p/S).astype(np.int16); qn=np.round(n*127).astype(np.int8)
    key=np.c_[qp.astype(np.int32),qn.astype(np.int32)]
    u,inv=np.unique(key,axis=0,return_inverse=True); inv=inv.reshape(-1)
    idx=inv.astype(np.uint16 if len(u)<65536 else np.uint32)
    entry={'name':nm,'nv':len(u),'ni':len(idx),'i32':bool(idx.dtype==np.uint32)}
    for k,b in (('p',u[:,:3].astype(np.int16).tobytes()),('n',u[:,3:].astype(np.int8).tobytes()),('i',idx.tobytes())):
        b=pad(b); entry[k]=off; bufs.append(b); off+=len(b)
    entry['bmin']=p.min(0).round(1).tolist(); entry['bmax']=p.max(0).round(1).tolist()
    parts.append(entry)
blob=b''.join(bufs)
meta=json.dumps({'scale':S,'parts':parts}).encode()
data=struct.pack('<I',0)+meta; data+=b' '*((-len(data))%4)
data=struct.pack('<I',len(data))+data[4:]
gz=gzip.compress(data+blob,9)
open('model.b64','w').write(base64.b64encode(gz).decode())
print('gz',len(gz))
for e in parts: print(f"{e['name']:14s} {e['ni']//3:6d} {e['bmin']} {e['bmax']}")
