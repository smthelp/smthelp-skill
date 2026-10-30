import * as THREE from 'three';
window.run=(data)=>{
  const r=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true}); r.setSize(1400,1000); document.body.appendChild(r.domElement);
  r.localClippingEnabled=true;
  const sc=new THREE.Scene(); sc.background=new THREE.Color(0xffffff);
  sc.add(new THREE.HemisphereLight(0xffffff,0x555555,1.6)); const dl=new THREE.DirectionalLight(0xffffff,1.8); dl.position.set(300,800,500); sc.add(dl);
  window.M={};
  for(const [id,p] of Object.entries(data)){ const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(p,3)); g.computeVertexNormals();
    const h=(parseInt(id)*0.6180339)%1; const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:new THREE.Color().setHSL(h,0.55,0.55),roughness:0.6,side:THREE.DoubleSide})); m.userData.id=id; sc.add(m); M[id]=m; }
  const cam=new THREE.OrthographicCamera(-1,1,1,-1,-5000,5000);
  window.shot=(dir,center,half,opts={})=>{
    for(const [id,m] of Object.entries(M)){ m.visible=!(opts.hide||[]).includes(+id) && (!opts.only || opts.only.includes(+id));
      m.material.clippingPlanes=opts.clip?[new THREE.Plane(new THREE.Vector3(...opts.clip[0]),opts.clip[1])]:[];
      m.material.emissive=new THREE.Color((opts.hl||[]).includes(+id)?0xff0000:0x000000); m.material.transparent=!!opts.ghost&&!(opts.hl||[]).includes(+id); m.material.opacity=opts.ghost?0.15:1; }
    cam.left=-half*1.4;cam.right=half*1.4;cam.top=half;cam.bottom=-half;cam.updateProjectionMatrix();
    const c=new THREE.Vector3(...center); cam.position.copy(c).add(new THREE.Vector3(...dir).normalize().multiplyScalar(2000)); cam.up.set(0,1,0); if(Math.abs(dir[1])>0.95) cam.up.set(0,0,-1); cam.lookAt(c); r.render(sc,cam);
    // labels
    const lab=[]; if(opts.labels){ for(const id of opts.labels){ const m=M[id]; if(!m) continue; m.geometry.computeBoundingBox(); const v=m.geometry.boundingBox.getCenter(new THREE.Vector3()).project(cam); lab.push([id,(v.x+1)/2*1400,(1-v.y)/2*1000]); } }
    return [r.domElement.toDataURL('image/png'),lab]; };
};
