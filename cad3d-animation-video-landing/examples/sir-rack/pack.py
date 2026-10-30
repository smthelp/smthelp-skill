# Reel storage rack 5 layer: CAD (X depth, Y up, Z length, mm) -> three (x=Z-595, y=Y+401, z=X+1176; front = +z)
import json,numpy as np,gzip,base64,struct,collections,re
d=json.load(open('../src/mesh.json'))
S=2000.0/32767
def classify(r,lo,hi):
    k=re.sub(r'<\d+>.*','',r['path'][5]) if len(r['path'])>5 else ''
    if r['path'][4].startswith('smt reel _'): return 'reel'
    if k=='____5-1.step': return None            # U-wire dividers -> instanced procedural (exact positions kept)
    if k.startswith('hex lobular'): return None  # M8 screws (hidden in panels) dropped
    if k=='____5.step': return 'rail%d'%int(round((lo[1]-119.8)/380))
    if k=='____5-0.step': return 'foot'
    if k=='________.step': return 'panelL' if (lo[0]+hi[0])<0 else 'panelR'
    return 'misc'
groups=collections.defaultdict(lambda:([],[])); extra={'dividers':[],'rails':[]}
for r in d:
    if 'pos' not in r: continue
    M=np.array(r['mat']).reshape(4,4).T
    p=np.array(r['pos']).reshape(-1,3); n=np.array(r['nor']).reshape(-1,3)
    p=(np.c_[p,np.ones(len(p))]@M.T)[:,:3]*1000; n=n@M[:3,:3].T; n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-9
    p=np.c_[p[:,2]-595,p[:,1]+401,p[:,0]+1176]; n=np.c_[n[:,2],n[:,1],n[:,0]]
    lo,hi=p.min(0),p.max(0)
    g=classify(r,lo,hi)
    k=re.sub(r'<\d+>.*','',r['path'][5]) if len(r['path'])>5 else ''
    if k=='____5-1.step': extra['dividers'].append([lo.round(2).tolist(),hi.round(2).tolist()])
    if g and g.startswith('rail'): extra['rails'].append([lo.round(1).tolist(),hi.round(1).tolist()])
    if g is None: continue
    groups[g][0].append(p); groups[g][1].append(n)
parts=[];bufs=[];off=0
pad=lambda b:b+b'\0'*((-len(b))%4)
for nmg,(P,N) in groups.items():
    p=np.concatenate(P); n=np.concatenate(N)
    assert np.abs(p).max() < S*32767, 'quant overflow: raise S'
    qp=np.round(p/S).astype(np.int16); qn=np.round(n*127).astype(np.int8)
    key=np.c_[qp.astype(np.int32),qn.astype(np.int32)]
    u,inv=np.unique(key,axis=0,return_inverse=True); inv=inv.reshape(-1)
    idx=inv.astype(np.uint16 if len(u)<65536 else np.uint32)
    entry={'name':nmg,'nv':len(u),'ni':len(idx),'i32':bool(idx.dtype==np.uint32)}
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
# compact divider table: per layer y0 and z-range, x positions
D=np.array([[a[0][0],a[0][1],a[0][2],a[1][0],a[1][1],a[1][2]] for a in extra['dividers']])
lay=sorted(set(np.round(D[:,1]).astype(int)))
extra['layers']=[{'y0':float(y),'xs':sorted(np.round(D[np.abs(D[:,1]-y)<3][:,0],2).tolist())} for y in lay]
extra['divz']=[float(D[:,2].min()),float(D[:,5].max())]; extra['divh']=float(np.median(D[:,4]-D[:,1])); extra['divw']=float(np.median(D[:,3]-D[:,0]))
del extra['dividers']
json.dump(extra,open('extra.json','w'))
print('gz',len(gz), 'tris',sum(e['ni'] for e in parts)//3)
for e in sorted(parts,key=lambda e:e['name']): print(f"{e['name']:12s} {e['ni']//3:6d} {e['bmin']} {e['bmax']}")
print(extra['layers'][0]['y0'],extra['layers'][0]['xs'][:4],len(extra['layers'][0]['xs']),extra['divz'],extra['divh'],extra['divw'])
print(sorted(extra['rails']))
