import json,numpy as np,gzip,base64,struct
d=json.load(open('../src/mesh.json'))
names={8:'nozzle',14:'pin_inner',20:'setscrew',26:'spring',32:'coil',38:'holder',44:'jawL',50:'pivotL',56:'clipL',62:'plunger',
 68:'pinC',74:'clipC',80:'jawR',86:'pivotR',92:'clipR',98:'padR',104:'padL1',110:'padL2',116:'stop',122:'washL',128:'washR',134:'washC'}
S=40.0/32767
todo=[]
for r in d:
    if r['id'] not in names: continue
    M=np.array(r['mat']).reshape(4,4).T
    p=np.array(r['pos']).reshape(-1,3); n=np.array(r['nor']).reshape(-1,3)
    p=(np.c_[p,np.ones(len(p))]@M.T)[:,:3]*1000
    n=n@M[:3,:3].T; n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-9
    if r['id']==32:
        tri=p.reshape(-1,3,3); c=tri.mean(1)
        lead=(c[:,1]<-31.7)&(np.minimum(np.hypot(c[:,0]-2.5,c[:,2]),np.hypot(c[:,0]+2.5,c[:,2]))<0.5)
        tn=n.reshape(-1,3,3)
        for nm,mask in (('coil_leads',lead),('coil',~lead)):
            todo.append((nm,tri[mask].reshape(-1,3),tn[mask].reshape(-1,3)))
    else:
        todo.append((names[r['id']],p,n))
parts=[];bufs=[];off=0
pad=lambda b:b+b'\0'*((-len(b))%4)
for nm,p,n in todo:
    qp=np.round(p/S).astype(np.int16); qn=np.round(n*127).astype(np.int8)
    key=np.c_[qp.astype(np.int32),qn.astype(np.int32)]
    u,inv=np.unique(key,axis=0,return_inverse=True); inv=inv.reshape(-1)
    idx=inv.astype(np.uint16 if len(u)<65536 else np.uint32)
    entry={'name':nm,'nv':len(u),'ni':len(idx),'i32':bool(idx.dtype==np.uint32)}
    for k,b in (('p',u[:,:3].astype(np.int16).tobytes()),('n',u[:,3:].astype(np.int8).tobytes()),('i',idx.tobytes())):
        b=pad(b); entry[k]=off; bufs.append(b); off+=len(b)
    entry['bmin']=p.min(0).round(3).tolist(); entry['bmax']=p.max(0).round(3).tolist()
    parts.append(entry)
blob=b''.join(bufs)
meta=json.dumps({'scale':S,'parts':parts}).encode()
data=struct.pack('<I',0)+meta; data+=b' '*((-len(data))%4)
data=struct.pack('<I',len(data))+data[4:]
gz=gzip.compress(data+blob,9)
open('model.b64','w').write(base64.b64encode(gz).decode())
print(len(gz))
for e in parts: print(e['name'],e['nv'],e['ni']//3,e['bmin'],e['bmax'])
