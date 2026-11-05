<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
const fb=()=>{document.getElementById("fb").style.display="block";document.getElementById("c3d").style.display="none";};
try{
const THREE=await import("three");
const {OrbitControls}=await import("three/addons/controls/OrbitControls.js");
const cv=document.getElementById("c3d");
const R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true});
R.setPixelRatio(Math.min(devicePixelRatio,2));R.shadowMap.enabled=true;
const S=new THREE.Scene();
const C=new THREE.PerspectiveCamera(36,1,0.05,100);
const HOME=new THREE.Vector3(2.6,2.6,4.2);C.position.copy(HOME);
const O=new OrbitControls(C,cv);O.enableDamping=true;O.target.set(.4,.8,0);O.maxPolarAngle=Math.PI*0.49;O.minDistance=1.2;O.maxDistance=12;
S.add(new THREE.HemisphereLight(0xffffff,0x8899aa,1.15));
const sun=new THREE.DirectionalLight(0xffffff,1.3);sun.position.set(3,6,4);sun.castShadow=true;sun.shadow.mapSize.set(1024,1024);Object.assign(sun.shadow.camera,{left:-5,right:5,top:4,bottom:-4});S.add(sun);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(20,12),new THREE.ShadowMaterial({opacity:.16}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;S.add(floor);
const grid=new THREE.GridHelper(14,28,0x88a0b0,0xc0ccd6);grid.material.opacity=.22;grid.material.transparent=true;S.add(grid);
const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.55,metalness:.15},o));
const white=M(0xeef1f4),grey=M(0x8a94a0),dark=M(0x2c3440),teal=M(0x0a9d9d),steel=M(0xb9c2cc,{metalness:.6,roughness:.3}),belt=M(0x2f6f4f),pcbM=M(0x1f8a4c),flexM=M(0xd99a2b),palM=M(0x3a4250),glass=M(0x9ad7e6,{transparent:true,opacity:.35,roughness:.1}),cup=M(0xd63031);
const box=(w,h,d,m,x,y,z,g)=>{const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);b.position.set(x,y,z);b.castShadow=true;b.receiveShadow=true;g.add(b);return b;};
const cyl=(r,h,m,x,y,z,g)=>{const c=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,18),m);c.position.set(x,y,z);c.castShadow=true;g.add(c);return c;};
function tower(g,x,z,h){cyl(.02,h,steel,x,h/2,z,g);[0xd63031,0xf9ca24,0x27ae60].forEach((c,i)=>cyl(.04,.06,M(c,{emissive:c,emissiveIntensity:.4}),x,h+.04+i*.065,z,g));}
const H=.9;
/* fixed downstream conveyor and next machine */
const fix=new THREE.Group();S.add(fix);
box(1.6,.03,.03,steel,1.5,H-.01,.2,fix);box(1.6,.03,.03,steel,1.5,H-.01,-.2,fix);box(1.6,.012,.38,belt,1.5,H-.03,0,fix);
[[.75,.2],[.75,-.2],[2.25,.2],[2.25,-.2]].forEach(([x,z])=>box(.03,H-.03,.03,grey,x,(H-.03)/2,z,fix));
box(.9,1.4,1.1,white,2.85,.7,0,fix);box(.86,.06,1.12,teal,2.85,1.42,0,fix);box(.5,.35,.02,glass,2.85,1.05,.56,fix);
/* per-mode machine */
let G=null,mode=-1,st={},fed=0,mov=[];
const P={
0:{k:"mag",L:.42,W:.3,T:6,cab:[1.1,.75],n:10},
1:{k:"mag",L:.36,W:.26,T:6,cab:[.55,.6],n:10,mini:1},
2:{k:"lt",L:.36,W:.26,T:6,n:10},
3:{k:"stk",L:.42,W:.32,T:5},
4:{k:"vac",L:.42,W:.3,T:8},
5:{k:"combo",L:.36,W:.26,T:7},
6:{k:"mag",L:1.2,W:.3,T:9,cab:[1.5,.6],n:8,led:1},
7:{k:"semi",L:.3,W:.14,T:6},
8:{k:"rob",L:.24,W:.2,T:9}};
function clear(){if(G){S.remove(G);G.traverse(o=>{if(o.geometry)o.geometry.dispose();});}mov.forEach(b=>S.remove(b.m));mov=[];}
function board(p,mat){const b=new THREE.Mesh(new THREE.BoxGeometry(p.L,.012,p.W),mat||pcbM);b.castShadow=true;return b;}
function magazine(g,p,n,x,z){const mg=new THREE.Group();const d=p.L+.05,w=p.W+.06,h=n*.05+.08;
 box(d,.012,.012,steel,0,0,w/2,mg);box(d,.012,.012,steel,0,0,-w/2,mg);box(d,.012,.012,steel,0,h,w/2,mg);box(d,.012,.012,steel,0,h,-w/2,mg);
 box(d,h,.008,M(0x6b7684,{transparent:true,opacity:.55}),0,h/2,w/2,mg);box(d,h,.008,M(0x6b7684,{transparent:true,opacity:.55}),0,h/2,-w/2,mg);box(d,.01,w,steel,0,0,0,mg);box(d,.01,w,steel,0,h,0,mg);
 const sl=[];for(let i=0;i<n;i++){const b=board(p);b.position.set(0,.05+i*.05,0);mg.add(b);sl.push(b);}
 mg.position.set(x,0,z);g.add(mg);return {g:mg,sl,h};}
function build(m){clear();mode=m;const p=P[m];G=new THREE.Group();S.add(G);st={p,c:0,t:0};
 if(p.k==="mag"){const [cw,cd]=p.cab;box(cw,.5,cd+.2,white,-cw/2+.55,.25,0,G);
  box(.08,1.5,cd+.2,white,-cw+.59,.75,0,G);if(!p.mini){box(cw-.1,.03,.03,steel,-cw/2+.55,.55,.25,G);box(cw-.1,.03,.03,steel,-cw/2+.55,.55,-.25,G);box(cw-.1,.03,.03,steel,-cw/2+.55,1.35,.25,G);box(cw-.1,.03,.03,steel,-cw/2+.55,1.35,-.25,G);}
  else{box(.6,1.6,.7,white,0,.8,-.0,G).material=M(0xf2f4f6,{transparent:true,opacity:.35});box(.25,.18,.02,dark,.15,1.2,.36,G);}
  tower(G,-cw+.59,.3,1.75);box(.22,.15,.02,dark,-cw/2+.4,.9,cd/2+.11,G);
  st.mag=magazine(G,p,p.n,p.led?-.15:0,0);st.push=box(.02,.04,.18,teal,0,H,0,G);
  st.mx=st.mag.g.position.x;}
 else if(p.k==="lt"){box(.75,.5,.75,white,0,.25,-.62,G);box(.75,1.3,.08,white,0,.85,-1.0,G);tower(G,.3,-1.0,1.65);
  st.mag=magazine(G,p,p.n,0,-.62);st.mag.g.rotation.y=Math.PI/2;st.push=box(.18,.04,.02,teal,0,H,-.62,G);
  box(.5,.03,.5,steel,0,H-.02,0,G);box(.06,H-.04,.06,grey,0,(H-.04)/2,0,G);}
 else if(p.k==="stk"){box(.55,H-.05,.65,white,0,(H-.05)/2,0,G);tower(G,-.25,.3,1.5);
  const fr=new THREE.Group();G.add(fr);[[-.24,.19],[-.24,-.19],[.24,.19],[.24,-.19]].forEach(([x,z])=>box(.02,.35,.02,steel,x,H+.17,z,fr));
  st.stack=[];for(let i=0;i<16;i++){const b=board(p);b.position.set(0,H+.015+i*.016,0);G.add(b);st.stack.push(b);}
  box(.55,.03,.03,steel,.3,H-.01,.2,G);box(.55,.03,.03,steel,.3,H-.01,-.2,G);}
 else if(p.k==="vac"||p.k==="combo"){box(.7,H-.05,.9,white,-.15,(H-.05)/2,0,G);box(.7,.85,.9,M(0xeef1f4,{transparent:true,opacity:.28}),-.15,H+.4,0,G);box(.7,.04,.9,white,-.15,H+.85,0,G);tower(G,-.45,.4,1.95);box(.25,.18,.02,dark,.1,1.35,.46,G);
  st.stack=[];const sx=-.2;for(let i=0;i<14;i++){const b=board(p);b.position.set(sx,.62+i*.018,0);G.add(b);st.stack.push(b);}st.sx=sx;
  const hd=new THREE.Group();G.add(hd);box(p.L*.8,.025,.04,dark,0,0,0,hd);[-1,0,1].forEach(a=>[-1,1].forEach(c=>cyl(.018,.04,cup,a*p.L*.3,-.03,c*p.W*.3,hd)));cyl(.012,.4,steel,0,.2,0,hd);hd.position.set(sx,1.3,0);st.hd=hd;
  box(1.1,.02,.02,steel,.1,1.52,0,G);
  if(p.k==="combo"){box(.7,.5,.5,white,-.15,.25,-.75,G);st.mag=magazine(G,p,8,-.15,-.75);st.mag.g.rotation.y=Math.PI/2;st.push=box(.18,.04,.02,teal,-.15,H,-.75,G);}}
 else if(p.k==="semi"){box(.9,.5,.65,white,-.2,.25,0,G);box(.08,1.65,.65,white,-.63,.82,0,G);tower(G,-.63,.25,1.8);
  st.mags=[];for(let j=0;j<3;j++){const mg=magazine(G,p,6,-.2,0);mg.g.position.y=.5+j*.4;st.mags.push(mg);}st.mag=st.mags[0];st.push=box(.02,.03,.1,teal,0,H,0,G);st.mx=-.2;}
 else if(p.k==="rob"){box(.8,H-.05,.87,white,0,(H-.05)/2,0,G);[[-.38,.41],[-.38,-.41],[.38,.41],[.38,-.41]].forEach(([x,z])=>box(.035,.85,.035,grey,x,H+.42,z,G));box(.8,.035,.87,grey,0,H+.85,0,G);tower(G,.35,.4,1.9);
  box(.8,.02,.3,belt,0,H-.02,.25,G);box(.8,.02,.3,belt,0,H-.02,-.22,G);
  const gr=new THREE.Group();G.add(gr);box(.16,.03,.14,dark,0,0,0,gr);cyl(.012,.3,steel,0,.16,0,gr);gr.position.set(-.2,1.3,.25);st.gr=gr;box(.05,.05,.87,dark,0,1.62,0,G);
  st.pal=new THREE.Mesh(new THREE.BoxGeometry(.34,.02,.3),palM);st.pal.position.set(.05,H,-.22);G.add(st.pal);
  st.in=board(p,flexM);st.in.position.set(-.5,H+.005,.25);G.add(st.in);}
 st.mv=board(p,p.k==="rob"?flexM:pcbM);st.mv.visible=false;G.add(st.mv);
}
const ease=x=>x<0?0:x>1?1:x*x*(3-2*x);
function emit(p,x,z,mat){const b=board(p,mat);b.position.set(x,H+.008,z);S.add(b);mov.push({m:b,z});fed++;if(window.__fed)window.__fed(fed,p.T);}
function step(dt){const p=st.p;st.t+=dt;let u=st.t/(p.T/2.2);if(u>=1){u=0;st.t=0;st.c++;}
 const k=p.k;
 if(k==="mag"||k==="semi"){const mg=st.mag,n=mg.sl.length,i=st.c%n;
  if(k==="semi"){const j=Math.floor(st.c/n)%3;st.mag=st.mags[j];st.mags.forEach((m,q)=>{m.g.position.y+=((q===j?H-.05-i*.05:.5+((q-j+3)%3)*.42+.5)-m.g.position.y)*.15;});}
  else{const ty=H-.05-i*.05;mg.g.position.y+=(ty-mg.g.position.y)*.2;}
  if(i===0&&u<.05)mg.sl.forEach(b=>b.visible=true);
  const s=mg.sl[i],a=ease((u-.2)/.45);const x0=st.mag.g.position.x,len=p.L+.05;
  st.push.position.set(x0-len/2-.02+a*(len*.55),H,st.mag.g.position.z);
  if(u>.2&&u<.7){s.visible=false;st.mv.visible=true;st.mv.position.set(x0+a*(.75+p.L*.0)+0,H+.006,st.mag.g.position.z);}
  if(u>=.7&&st.mv.visible){st.mv.visible=false;emit(p,x0+.75,0);}}
 else if(k==="lt"){const mg=st.mag,n=mg.sl.length,i=st.c%n;mg.g.position.y+=(H-.05-i*.05-mg.g.position.y)*.2;if(i===0&&u<.05)mg.sl.forEach(b=>b.visible=true);
  const a=ease((u-.15)/.35),b2=ease((u-.55)/.3);st.push.position.set(0,H,-.62-.25+a*.25);
  if(u>.15&&u<.85){mg.sl[i].visible=false;st.mv.visible=true;st.mv.position.set(b2*.75,H+.006,-.62+a*.62);}
  if(u>=.85&&st.mv.visible){st.mv.visible=false;emit(p,.75,0);}}
 else if(k==="stk"){const sk=st.stack,a=ease((u-.2)/.5);const bot=sk[0];
  if(u>.2&&u<.75){bot.visible=false;st.mv.visible=true;st.mv.position.set(a*.75,H+.006,0);sk.forEach((b,q)=>{if(q>0)b.position.y=H+.015+(q-a)*.016;});}
  if(u>=.75&&st.mv.visible){st.mv.visible=false;emit(p,.75,0);sk.push(sk.shift());sk.forEach((b,q)=>{b.position.y=H+.015+q*.016;b.visible=true;});}}
 else if(k==="vac"||(k==="combo"&&st.c%2===0)){const sk=st.stack,top=sk[sk.length-1],hd=st.hd,sx=st.sx;
  if(k==="combo"&&st.mag)st.push.position.z=-.75-.25;
  const ty=top.position.y+.05;let hx=sx,hy=1.3;
  if(u<.25){hy=1.3+(ty-1.3)*ease(u/.25);}else if(u<.45){hy=ty+(1.15-ty)*ease((u-.25)/.2);top.visible=false;st.mv.visible=true;}else if(u<.75){hy=1.15;hx=sx+(.95-sx)*ease((u-.45)/.3);}else if(u<.9){hx=.95;hy=1.15+(H+.05-1.15)*ease((u-.75)/.15);}else{hx=.95-(.95-sx)*ease((u-.9)/.1);hy=1.3;if(st.mv.visible){st.mv.visible=false;emit(p,.95,0);sk.unshift(sk.pop());sk.forEach((b,q)=>{b.position.y=.62+q*.018;b.visible=true;});}}
  hd.position.set(hx,hy,0);if(st.mv.visible)st.mv.position.set(hx,hy-.05,0);}
 else if(k==="combo"){const mg=st.mag,n=mg.sl.length,i=Math.floor(st.c/2)%n;mg.g.position.y+=(H-.05-i*.05-mg.g.position.y)*.2;if(i===0&&u<.05)mg.sl.forEach(b=>b.visible=true);
  const a=ease((u-.1)/.35),b2=ease((u-.5)/.35);st.push.position.set(-.15,H,-.75-.25+a*.25);st.hd.position.set(st.sx,1.3,0);
  if(u>.1&&u<.88){mg.sl[i].visible=false;st.mv.visible=true;st.mv.position.set(-.15+b2*1.1,H+.006,-.75+a*.75);}
  if(u>=.88&&st.mv.visible){st.mv.visible=false;emit(p,.95,0);}}
 else if(k==="rob"){const gr=st.gr;let gx=-.2,gz=.25,gy=1.3;
  if(u<.2){st.in.visible=true;st.in.position.x=-.5+.3*ease(u/.2);}
  else if(u<.35){gy=1.3-(.38)*ease((u-.2)/.15);}
  else if(u<.65){st.in.visible=false;st.mv.visible=true;gy=.92+.38*ease((u-.35)/.1);gz=.25-.47*ease((u-.4)/.25);gx=-.2+.25*ease((u-.4)/.25);}
  else if(u<.8){gx=.05;gz=-.22;gy=1.3-.36*ease((u-.65)/.15);}
  else{gx=.05;gz=-.22;gy=.94+.36*ease((u-.8)/.2);if(st.mv.visible){st.mv.visible=false;const pb=st.pal.clone();pb.position.set(.05,H,-.22);S.add(pb);const bb=board(p,flexM);bb.position.y=.015;pb.add(bb);mov.push({m:pb,z:-.22,pal:1});fed++;if(window.__fed)window.__fed(fed,p.T);st.in.position.x=-.5;}}
  gr.position.set(gx,gy,gz);if(st.mv.visible)st.mv.position.set(gx,gy-.03,gz);}
 for(let q=mov.length-1;q>=0;q--){const b=mov[q];b.m.position.x+=dt*.45;b.m.position.z+=(0-b.m.position.z)*.05;if(b.m.position.x>2.35){S.remove(b.m);mov.splice(q,1);}}
}
window.__mode3d=i=>{build(i);fed=0;if(window.__fed)window.__fed(0,P[i].T);};
window.__reset3d=()=>{C.position.copy(HOME);O.target.set(.4,.8,0);};
build(0);
function themeBg(){const d=document.documentElement.getAttribute("data-theme")==="dark";grid.material.color.set(d?0x2a3b55:0xc0ccd6);}
addEventListener("themechange",themeBg);themeBg();
function size(){const w=cv.clientWidth,h=cv.clientHeight;R.setSize(w,h,false);C.aspect=w/h;C.updateProjectionMatrix();}
new ResizeObserver(size).observe(cv);size();
const clk=new THREE.Clock();let vis=true;new IntersectionObserver(e=>{vis=e[0].isIntersecting;}).observe(cv);
const ray=new THREE.Raycaster(),mp=new THREE.Vector2();
(function tick(){requestAnimationFrame(tick);if(!vis)return;const dt=Math.min(clk.getDelta(),.05);
 O.autoRotate=!!window.__rot;O.autoRotateSpeed=.6;O.update();if(window.__flow)step(dt);R.render(S,C);})();
}catch(err){console.warn("3D unavailable",err);fb();}
</script>
