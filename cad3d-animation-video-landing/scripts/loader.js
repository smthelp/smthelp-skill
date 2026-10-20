import * as THREE from 'three';
export async function loadModel(b64){
  const bin=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));
  const ds=new Blob([bin]).stream().pipeThrough(new DecompressionStream('gzip'));
  const buf=await new Response(ds).arrayBuffer();
  const dv=new DataView(buf); const hl=dv.getUint32(0,true);
  const meta=JSON.parse(new TextDecoder().decode(new Uint8Array(buf,4,hl-4)));
  const base=hl; const geos={};
  for(const p of meta.parts){
    const g=new THREE.BufferGeometry();
    const P=new Int16Array(buf,base+p.p,p.nv*3); const N=new Int8Array(buf.slice(base+p.n,base+p.n+p.nv*3));
    const pos=new Float32Array(p.nv*3); for(let i=0;i<pos.length;i++) pos[i]=P[i]*meta.scale;
    const nor=new Float32Array(p.nv*3); for(let i=0;i<nor.length;i++) nor[i]=N[i]/127;
    g.setAttribute('position',new THREE.BufferAttribute(pos,3));
    g.setAttribute('normal',new THREE.BufferAttribute(nor,3));
    const I=p.i32? new Uint32Array(buf.slice(base+p.i,base+p.i+p.ni*4)) : new Uint16Array(buf.slice(base+p.i,base+p.i+p.ni*2));
    g.setIndex(new THREE.BufferAttribute(I,1));
    geos[p.name]={geo:g,bmin:p.bmin,bmax:p.bmax};
  }
  return geos;
}
