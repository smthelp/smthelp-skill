# SAF1001 axial tape feeder: named bodies -> groups, CAD (X len, Y width, Z up, mm) -> three (x=X-350, y=Z+160, z=46-Y)
import json,numpy as np,gzip,base64,struct,collections,re
d=json.load(open('../src/mesh.json'))
S=800.0/32767
def nm(p): return [re.sub(r'\s*\(默认.*?\)','',x) for x in p]
PAWL_PIVOT={}
def classify(r,lo,hi):
    p=nm(r['path']); s=' > '.join(p); leaf=p[-3] if len(p)>=3 else s; i=r['id']
    if 'logo' in s: return 'logo'
    if '电子元件' in leaf or '元件纸' in leaf: return None          # components drawn procedurally
    if '压紧弹簧' in leaf: return None                              # springs drawn procedurally (24k tris each)
    if 'bslmm5' in leaf: return None                                # silencers drawn procedurally
    if '编带拨针' in leaf:
        k=('L' if '左' in s else 'R')+str(int(round((lo[0]+hi[0])/2)))
        return 'pawl_'+k
    if '拨针安装座' in s or '滚珠滑组' in s or '滑块安装组件' in s or leaf in ('_mu10x20_rod<1>','送料气缸浮动接头<1>'): return 'slider'
    if 'mgw9c滑轨' in leaf: return 'guide'
    if '送料气缸组件' in s: return 'feedcyl'
    if '限位块组件' in s: return 'stop'
    if '调宽轴组件' in s or '调宽套' in leaf: return 'width'
    if '运料组件' in s: return 'transport'
    if '倒料' in leaf: return 'claw'
    if '压料座' in s or '调高偏心轴' in leaf: return 'press'
    if '下料板金' in s: return 'unload'
    if '光纤' in s: return 'fibre'
    if '成型刀组件' in s or '32缸径切脚活塞杆' in s or leaf=='_sda-32x2020_r<1>': return 'knife_move'
    if '切刀总体组件' in s: return 'knife_fixed'
    if '切纸带刀槽组件' in s: return 'cutcyl'
    if '切纸带刀组件' in s or 'md气缸导杆' in s: return 'tapeknife'
    if 'md32x20s' in s: return 'tapecyl'
    if '静纸带切刀' in leaf: return 'knife_fixed'
    if '飞达左侧支撑板' in leaf or '飞达右侧支撑板' in leaf or '飞达左侧盖板' in leaf: return 'side'
    if '飞达底座板' in leaf or '前堵头板' in leaf: return 'frame'
    if '机构安装板' in leaf: return 'plate'
    if '压紧块' in leaf or '压块螺丝' in leaf: return 'clamp'
    if '销钉' in leaf and '安装底座' in s: return 'pins'
    if '安装底座' in s or '定位卡板' in leaf: return 'mount'
    if '控制板' in leaf: return 'pcb'
    if '电器盒子' in s: return 'ebox'
    if '物料导向块' in s: return 'guideblk'
    if '270x80x115' in leaf: return 'carton'
    if '卧式编带盒' in s: return 'tray'
    if '料盒悬挂钉' in leaf: return 'hanger'
    if '12按钮绿' in leaf: return 'btn_g'
    if '12按钮' in leaf: return 'btn_r'
    if '拨动开关' in leaf: return 'switch'
    if '航空插头' in leaf: return 'plug'
    if 'kq2' in leaf or 'm-5h-6' in leaf: return 'fitting'
    if 'syj5123' in leaf: return 'valve'
    if '废纸带槽' in leaf: return 'chute'
    if '不锈钢管' in s: return 'tube'
    return 'misc'
groups=collections.defaultdict(lambda:([],[])); extra={'springs':[],'silencers':[],'pivots':{}}
for r in d:
    if 'pos' not in r: continue
    M=np.array(r['mat']).reshape(4,4).T
    p=np.array(r['pos']).reshape(-1,3); n=np.array(r['nor']).reshape(-1,3)
    p=(np.c_[p,np.ones(len(p))]@M.T)[:,:3]*1000; n=n@M[:3,:3].T; n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-9
    p=np.c_[p[:,0]-350,p[:,2]+160,46-p[:,1]]; n=np.c_[n[:,0],n[:,2],-n[:,1]]
    lo,hi=p.min(0),p.max(0)
    s=' > '.join(nm(r['path']))
    if '压紧弹簧' in s: extra['springs'].append([lo.round(1).tolist(),hi.round(1).tolist()])
    if 'bslmm5' in s: extra['silencers'].append([lo.round(1).tolist(),hi.round(1).tolist()])
    if '拨针转动螺丝' in s: extra['pivots'][('L' if '左' in s else 'R')+str(int(round((lo[0]+hi[0])/2)))]=((lo+hi)/2).round(2).tolist()
    # pawl key uses CAD X centre; recompute on three coords (x shifted by -350)
    g=classify(r,lo+[350,0,0],hi+[350,0,0])
    if g is None: continue
    groups[g][0].append(p); groups[g][1].append(n)
parts=[];bufs=[];off=0
pad=lambda b:b+b'\0'*((-len(b))%4)
for nmg,(P,N) in groups.items():
    p=np.concatenate(P); n=np.concatenate(N)
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
json.dump(extra,open('extra.json','w'))
print('gz',len(gz), 'tris',sum(e['ni'] for e in parts)//3)
for e in sorted(parts,key=lambda e:e['name']): print(f"{e['name']:12s} {e['ni']//3:6d} {e['bmin']} {e['bmax']}")
print(extra['pivots'])
