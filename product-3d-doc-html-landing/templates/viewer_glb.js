<!-- viewer_glb.js: generic GLB/GLTF viewer for the landing template.
     Build fills %%MODEL_SRC%% (data URI or https URL of a .glb) and %%VIEWS_JSON%% (camera presets, one per mode chip).
     Contract with template: window.__mode3d(i), __reset3d(), __rot, __flow, __mat(), __light(), __fed(n,cycle) (optional). -->
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
const fb=()=>{document.getElementById("fb").style.display="block";document.getElementById("c3d").style.display="none";};
try{
const THREE=await import("three");
const {OrbitControls}=await import("three/addons/controls/OrbitControls.js");
const {GLTFLoader}=await import("three/addons/loaders/GLTFLoader.js");
const {DRACOLoader}=await import("three/addons/loaders/DRACOLoader.js");
const {MeshoptDecoder}=await import("three/addons/libs/meshopt_decoder.module.js");
const {RoomEnvironment}=await import("three/addons/environments/RoomEnvironment.js");
const SRC="%%MODEL_SRC%%";
const VIEWS=%%VIEWS_JSON%%; /* [{"pos":[1.6,0.9,1.6],"target":[0,0,0],"explode":0}] in units of the model's largest dimension */
const cv=document.getElementById("c3d");
const R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true});
R.setPixelRatio(Math.min(devicePixelRatio,2));R.shadowMap.enabled=true;R.outputColorSpace=THREE.SRGBColorSpace;R.toneMapping=THREE.ACESFilmicToneMapping;
const S=new THREE.Scene();const pm=new THREE.PMREMGenerator(R);const ENV=pm.fromScene(new RoomEnvironment(),0.04).texture;S.environment=ENV;
const C=new THREE.PerspectiveCamera(35,1,0.01,500);
const O=new OrbitControls(C,cv);O.enableDamping=true;O.maxPolarAngle=Math.PI*0.495;
const hemi=new THREE.HemisphereLight(0xffffff,0x8899aa,.8);S.add(hemi);
const key=new THREE.DirectionalLight(0xffffff,1.6);key.castShadow=true;key.shadow.mapSize.set(2048,2048);S.add(key);
const fill=new THREE.DirectionalLight(0x9fd8ff,.4);S.add(fill);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.ShadowMaterial({opacity:.18}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;S.add(floor);
let root=null,size=1,center=new THREE.Vector3(),mixer=null,parts=[];
/* material modes: original, metal, clay, x-ray, wireframe */
const MATS=["mat_orig","mat_metal","mat_clay","mat_xray","mat_wire"];let mi=0;
const metal=new THREE.MeshStandardMaterial({color:0xc9d1d9,metalness:.9,roughness:.25,side:THREE.DoubleSide}),clay=new THREE.MeshStandardMaterial({color:0xe9e4dc,roughness:.9,side:THREE.DoubleSide}),
 xray=new THREE.MeshStandardMaterial({color:0x56c8ff,transparent:true,opacity:.22,depthWrite:false}),wire=new THREE.MeshBasicMaterial({color:0x0a9d9d,wireframe:true});
function setMat(i){mi=i;parts.forEach(p=>{p.m.material=i===0?p.orig:[null,metal,clay,xray,wire][i];});}
window.__mat=()=>{setMat((mi+1)%MATS.length);return MATS[mi];};
/* light presets: studio, warm workshop, night line */
const LIGHTS=["light_studio","light_warm","light_night"];let li=0;
function setLight(i){li=i;const P=[[0xffffff,1.6,.8,1],[0xffd8a8,1.4,.6,.8],[0x9fb8ff,.7,.25,.35]][i];key.color.set(P[0]);key.intensity=P[1];hemi.intensity=P[2];R.toneMappingExposure=P[3];S.environment=i===2?null:ENV;}
window.__light=()=>{setLight((li+1)%LIGHTS.length);return LIGHTS[li];};
if(window.__ctl3d)window.__ctl3d();
let tgtPos=null,tgtLook=null,explode=0,exT=0;
function view(i){const v=VIEWS[i]||VIEWS[0];if(!v)return;tgtPos=new THREE.Vector3(...v.pos).multiplyScalar(size).add(center);tgtLook=new THREE.Vector3(...(v.target||[0,0,0])).multiplyScalar(size).add(center);exT=v.explode||0;}
window.__mode3d=i=>view(i);
window.__reset3d=()=>view(0);
const ld=new GLTFLoader();const dr=new DRACOLoader();dr.setDecoderPath("https://www.gstatic.com/draco/versioned/decoders/1.5.6/");ld.setDRACOLoader(dr);ld.setMeshoptDecoder(MeshoptDecoder);
ld.load(SRC,g=>{root=g.scene;S.add(root);
 const b=new THREE.Box3().setFromObject(root);const s=b.getSize(new THREE.Vector3());size=Math.max(s.x,s.y,s.z);root.position.y-=b.min.y;b.setFromObject(root);b.getCenter(center);
 root.traverse(o=>{if(o.isMesh){if(!o.geometry.attributes.normal)o.geometry.computeVertexNormals();o.castShadow=o.receiveShadow=true;const c=new THREE.Box3().setFromObject(o).getCenter(new THREE.Vector3());parts.push({m:o,orig:o.material,home:o.position.clone(),dir:c.sub(center).normalize()});}});
 floor.scale.set(size*6,size*6,1);key.position.set(size*2,size*3,size*2);fill.position.set(-size*2,size,-size);
 Object.assign(key.shadow.camera,{left:-size*2,right:size*2,top:size*2,bottom:-size*2,far:size*10});
 O.minDistance=size*.3;O.maxDistance=size*8;C.near=size/200;C.far=size*50;C.updateProjectionMatrix();
 if(g.animations&&g.animations.length){mixer=new THREE.AnimationMixer(root);g.animations.forEach(a=>mixer.clipAction(a).play());}
 view(0);C.position.copy(tgtPos);O.target.copy(tgtLook);
},undefined,e=>{console.warn("model load failed",e);fb();});
function rs(){const w=cv.clientWidth,h=cv.clientHeight;R.setSize(w,h,false);C.aspect=w/h;C.updateProjectionMatrix();}
new ResizeObserver(rs).observe(cv);rs();
const clk=new THREE.Clock();let vis=true;new IntersectionObserver(e=>{vis=e[0].isIntersecting;}).observe(cv);
(function tick(){requestAnimationFrame(tick);if(!vis)return;const dt=Math.min(clk.getDelta(),.05);
 if(tgtPos){C.position.lerp(tgtPos,.06);O.target.lerp(tgtLook,.06);if(C.position.distanceTo(tgtPos)<size*.005)tgtPos=null;}
 if(Math.abs(explode-exT)>1e-3){explode+=(exT-explode)*.08;parts.forEach(p=>p.m.position.copy(p.home).addScaledVector(p.dir,explode*size*.25));}
 if(mixer&&window.__flow)mixer.update(dt);
 O.autoRotate=!!window.__rot;O.autoRotateSpeed=.6;O.update();R.render(S,C);})();
}catch(err){console.warn("3D unavailable",err);fb();}
</script>
