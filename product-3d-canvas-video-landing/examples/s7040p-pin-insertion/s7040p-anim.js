/* svg2canvas - draw a live SVG DOM tree onto a 2D canvas, synchronously (p3cv helper, since 1.3.0).
   Lets an existing SVG mechanism module (one that builds <svg> elements and moves them with
   setAttribute) satisfy the canvas animation contract of templates/anim-template.js:

     var svg = document.createElementNS('http://www.w3.org/2000/svg','svg');   // detached is fine
     var anim = new MySvgAnim(svg, {...});
     render(ctx, W, H, o) { anim.render(o.t); SVG2Canvas.draw(ctx, svg, {vars: THEME}); }

   Supported: g (transform translate/rotate/scale/matrix, opacity), rect (rx), circle, ellipse, line,
   path (d via Path2D), polygon/polyline, text + tspan (font-size/-weight/-family, text-anchor,
   letter-spacing), fill / stroke / stroke-width / stroke-dasharray / opacity / fill-opacity,
   var(--name,fallback) colours (resolved from opts.vars, else the fallback), and mask="url(#id)"
   whose mask is white shapes plus black "holes" (drawn via an offscreen canvas). Not supported:
   gradients, filters, clipPath, CSS classes/stylesheets, images - keep SVG modules to inline attributes.
   Draws in the SVG's user units: set up ctx scale/translate before calling. */
(function (G) {
  function num(e, a, d) { var v = e.getAttribute(a); return v === null || v === '' ? (d || 0) : parseFloat(v) }
  function col(v, vars) {
    if (!v) return v; v = v.trim();
    var m = /^var\(\s*(--[\w-]+)\s*(?:,\s*(.+))?\)$/.exec(v);
    if (m) return (vars && vars[m[1]]) || (m[2] ? col(m[2], vars) : '#000');
    return v;
  }
  function inh(e, a, p) { var v = e.getAttribute(a); return v === null ? p[a] : v }
  function transform(ctx, t) {
    if (!t) return;
    var re = /(\w+)\s*\(([^)]*)\)/g, m;
    while ((m = re.exec(t))) {
      var a = m[2].split(/[\s,]+/).filter(Boolean).map(parseFloat);
      if (m[1] === 'translate') ctx.translate(a[0] || 0, a[1] || 0);
      else if (m[1] === 'rotate') { if (a.length > 2) { ctx.translate(a[1], a[2]); ctx.rotate(a[0] * Math.PI / 180); ctx.translate(-a[1], -a[2]) } else ctx.rotate((a[0] || 0) * Math.PI / 180) }
      else if (m[1] === 'scale') ctx.scale(a[0], a.length > 1 ? a[1] : a[0]);
      else if (m[1] === 'matrix') ctx.transform(a[0], a[1], a[2], a[3], a[4], a[5]);
    }
  }
  function rrect(ctx, x, y, w, h, r) {
    r = Math.max(0, Math.min(r, w / 2, h / 2)); ctx.beginPath();
    if (!r) { ctx.rect(x, y, w, h); return }
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function paint(ctx, e, st, path) {
    var f = st.fill, s = st.stroke, sw = parseFloat(st['stroke-width'] || 1);
    if (f && f !== 'none') { ctx.globalAlpha = st._a * parseFloat(st['fill-opacity'] || 1); ctx.fillStyle = f; path ? ctx.fill(path) : ctx.fill() }
    if (s && s !== 'none' && sw > 0) {
      ctx.globalAlpha = st._a * parseFloat(st['stroke-opacity'] || 1); ctx.strokeStyle = s; ctx.lineWidth = sw;
      var d = st['stroke-dasharray']; ctx.setLineDash(d && d !== 'none' ? d.split(/[\s,]+/).map(parseFloat) : []);
      ctx.lineCap = st['stroke-linecap'] || 'butt'; path ? ctx.stroke(path) : ctx.stroke();
    }
  }
  var KEYS = ['fill', 'stroke', 'stroke-width', 'stroke-dasharray', 'stroke-linecap', 'fill-opacity', 'stroke-opacity',
    'font-size', 'font-weight', 'font-family', 'text-anchor', 'letter-spacing'];
  function node(ctx, e, p, o) {
    var tag = (e.localName || e.nodeName || '').toLowerCase();
    if (!tag || tag === 'defs' || tag === 'mask' || tag === 'clippath' || tag === '#text') return;
    var st = { _a: p._a * num(e, 'opacity', 1) };
    if (st._a <= 0.001 || e.getAttribute('display') === 'none' || e.getAttribute('visibility') === 'hidden') return;
    KEYS.forEach(function (k) { st[k] = inh(e, k, p) });
    st.fill = col(st.fill, o.vars); st.stroke = col(st.stroke, o.vars);
    var mk = e.getAttribute('mask');
    if (mk && o.root) { masked(ctx, e, st, mk, o); return }
    ctx.save(); transform(ctx, e.getAttribute('transform'));
    if (tag === 'g' || tag === 'svg') { for (var c = e.firstElementChild; c; c = c.nextElementSibling) node(ctx, c, st, o) }
    else if (tag === 'rect') { rrect(ctx, num(e, 'x'), num(e, 'y'), num(e, 'width'), num(e, 'height'), num(e, 'rx', num(e, 'ry'))); paint(ctx, e, st) }
    else if (tag === 'circle') { ctx.beginPath(); ctx.arc(num(e, 'cx'), num(e, 'cy'), Math.max(0, num(e, 'r')), 0, 2 * Math.PI); paint(ctx, e, st) }
    else if (tag === 'ellipse') { ctx.beginPath(); ctx.ellipse(num(e, 'cx'), num(e, 'cy'), Math.max(0, num(e, 'rx')), Math.max(0, num(e, 'ry')), 0, 0, 2 * Math.PI); paint(ctx, e, st) }
    else if (tag === 'line') { if (!st.stroke) st.stroke = 'none'; st.fill = 'none'; ctx.beginPath(); ctx.moveTo(num(e, 'x1'), num(e, 'y1')); ctx.lineTo(num(e, 'x2'), num(e, 'y2')); paint(ctx, e, st) }
    else if (tag === 'path') { var d = e.getAttribute('d'); if (d) paint(ctx, e, st, new Path2D(d)) }
    else if (tag === 'polygon' || tag === 'polyline') { var pts = (e.getAttribute('points') || '').trim(); if (pts) paint(ctx, e, st, new Path2D('M' + pts + (tag === 'polygon' ? 'Z' : ''))); }
    else if (tag === 'text') text(ctx, e, st);
    ctx.restore();
  }
  function text(ctx, e, st) {
    var fs = parseFloat(st['font-size'] || 16), fam = st['font-family'] || 'Arial, sans-serif';
    ctx.font = (st['font-weight'] || 400) + ' ' + fs + 'px ' + fam;
    var an = st['text-anchor']; ctx.textAlign = an === 'middle' ? 'center' : an === 'end' ? 'right' : 'left'; ctx.textBaseline = 'alphabetic';
    if ('letterSpacing' in ctx) ctx.letterSpacing = (parseFloat(st['letter-spacing'] || 0) || 0) + 'px';
    ctx.globalAlpha = st._a; ctx.fillStyle = st.fill && st.fill !== 'none' ? st.fill : '#000';
    var spans = e.getElementsByTagName ? Array.prototype.slice.call(e.getElementsByTagName('tspan')) : [];
    if (!spans.length) { ctx.fillText(e.textContent, num(e, 'x'), num(e, 'y')); return }
    spans.forEach(function (s) { ctx.fillText(s.textContent, s.hasAttribute('x') ? num(s, 'x') : num(e, 'x'), s.hasAttribute('y') ? num(s, 'y') : num(e, 'y')) });
  }
  function masked(ctx, e, st, mk, o) {
    var id = /url\(#([^)]+)\)/.exec(mk), m = id && o.root.querySelector('#' + CSS.escape(id[1]));
    var cv = document.createElement('canvas'); cv.width = ctx.canvas.width; cv.height = ctx.canvas.height;
    var c2 = cv.getContext('2d'); c2.setTransform(ctx.getTransform());
    var clone = e.cloneNode(true); clone.removeAttribute('mask'); clone.removeAttribute('opacity');
    node(c2, clone, { _a: 1 }, { vars: o.vars });
    if (m) { c2.globalCompositeOperation = 'destination-out';
      for (var c = m.firstElementChild; c; c = c.nextElementSibling) {
        var f = (c.getAttribute('fill') || '').toLowerCase();
        if (f === '#000' || f === '#000000' || f === 'black') { var k = c.cloneNode(true); k.setAttribute('fill', '#000'); node(c2, k, { _a: 1 }, { vars: o.vars }) } } }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = st._a; ctx.drawImage(cv, 0, 0); ctx.restore();
  }
  function draw(ctx, svg, o) {
    o = o || {}; o.root = svg;
    var base = { _a: 1, fill: '#000', stroke: 'none', 'stroke-width': '1', 'font-size': '16', 'font-weight': '400', 'font-family': 'Arial, sans-serif', 'text-anchor': 'start' };
    for (var c = svg.firstElementChild; c; c = c.nextElementSibling) node(ctx, c, base, o);
  }
  G.SVG2Canvas = { draw: draw };
})(window);
/* S7040E/P/T 4-head, 4-feeder pin / eyelet / terminal insertion - deterministic schematic animation.
   new InsertAnim(svg,{model:'T'|'P'|'E'|'cycle',callout:bool}); render(t,focus,amt); setModel(m) */
(function(global){
var NS="http://www.w3.org/2000/svg";
function el(tag,a,p){var e=document.createElementNS(NS,tag);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;}
function cl(x){return Math.max(0,Math.min(1,x));}
function ease(x){x=cl(x);return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;}
function lerp(a,b,x){return a+(b-a)*x;}
var COL=["#e0a63b","#d9733a","#aeb9be","#4fb8a6"];
var MODELS={
 T:{code:"S7040T",fam:"terminal",title:"Terminal insertion",parts:["Straight PCB terminal","Faston tab terminal","Right-angle terminal","Ring-lug terminal"],feed:["reel","reel","bowl","bowl"]},
 P:{code:"S7040P",fam:"pin",title:"Pin insertion",parts:["Square pin","Round pin","Press-fit pin","Test pin"],feed:["reel","bowl","reel","bowl"]},
 E:{code:"S7040E",fam:"eyelet",title:"Eyelet insertion",parts:["Flat-flange eyelet","Funnel eyelet","Rolled-flange eyelet","Tubular rivet"],feed:["bowl","bowl","bowl","bowl"]},
 C:{code:"S7040P",fam:"cust",title:"Press-fit pins + clips",parts:["Medium pin","Large pin","Medium clip","Large clip"],feed:["bowl","bowl","bowl","bowl"],press:true}
};
var ORDER=["T","P","E"];
var HXS=[560,720,880,1040],BH=[40,95,150,205,260,315,370,425],BW=460,BY=455,CAMX=330;
var IN=2.0,MK=1.2,IP=1.0,OUT=1.6,NI=8,BP=IN+MK+NI*IP+OUT,START=CAMX-230;
function steps(m){var M=MODELS[m],fn=function(i){return M.feed[i]==="reel"?"reel feeder":"vibration bowl feeder";};
 if(M.press){var hs=function(i){return {n:"0"+(4+i),t:"Head "+(i+1)+" → "+M.parts[i],d:"Bowl "+(i+1)+" feeds only Head "+(i+1)+": "+M.parts[i].toLowerCase()+(M.dia?", max. Ø"+M.dia[i]+" into a "+M.hole[i]+" mm hole.":", pressed into its own hole size."),f:[HXS[i],235,180]};};
 return [
 {n:"01",t:"Conveyor in",d:"The board with plated through-holes enters on the SMEMA conveyor.",f:[170,470,110]},
 {n:"02",t:"Fiducial vision",d:"The camera reads the board fiducials; MARK correction 0.015 mm.",f:[CAMX,390,95]},
 {n:"03",t:"4 bowl feeders",d:"One vibration bowl per bulk part, tail-down track; clip bowls separate tangled spring fingers.",f:[800,95,300]},
 hs(0),hs(1),hs(2),hs(3),
 {n:"08",t:"Servo press, flush",d:"Pins pressed on the rim only, clips on the collar, until flush. About 0.5 s per part (slowed).",f:[800,430,125]},
 {n:"09",t:"Pedestal + miss check",d:"A pedestal supports the board under each press; a missing part stops the machine.",f:[840,540,320]},
 {n:"10",t:"X-Y table",d:"Point-to-point 0.025 mm, repeatability 0.05 mm, to the next hole.",f:[800,605,140]},
 {n:"11",t:"Conveyor out",d:"All 4 parts in one program, no tooling change. The board leaves the cell.",f:[1440,470,110]}
 ];}
 return [
 {n:"01",t:"Conveyor in",d:"The PCB enters on the left conveyor and moves onto the X-Y table.",f:[170,470,110]},
 {n:"02",t:"Vision programming",d:"The camera reads the board marks; visual correction keeps every hole on target.",f:[CAMX,390,95]},
 {n:"03",t:"4 feeders, your choice",d:"Each of the 4 feeders can be a vibration bowl (bulk) or a reel with tape reel.",f:[800,95,300]},
 {n:"04",t:"Head 1 → "+M.parts[0],d:"Feeder 1 ("+fn(0)+") supplies only Head 1, which inserts only "+M.parts[0].toLowerCase()+"s.",f:[HXS[0],235,180]},
 {n:"05",t:"Head 2 → "+M.parts[1],d:"Feeder 2 ("+fn(1)+") supplies only Head 2, which inserts only "+M.parts[1].toLowerCase()+"s.",f:[HXS[1],235,180]},
 {n:"06",t:"Head 3 → "+M.parts[2],d:"Feeder 3 ("+fn(2)+") supplies only Head 3, which inserts only "+M.parts[2].toLowerCase()+"s.",f:[HXS[2],235,180]},
 {n:"07",t:"Head 4 → "+M.parts[3],d:"Feeder 4 ("+fn(3)+") supplies only Head 4, which inserts only "+M.parts[3].toLowerCase()+"s.",f:[HXS[3],235,180]},
 {n:"08",t:"Insert at any angle",d:"0–360° in 1° steps, vertical error ≤0.8°. Real cycle: 0.5 s per part (slowed here).",f:[800,430,125]},
 {n:"09",t:"Clinch + miss check",d:"A clinch base under each head bends the leads; a missing part stops the machine.",f:[840,540,320]},
 {n:"10",t:"X-Y table",d:"Moves the board under the right head at 0.001 mm per pulse.",f:[800,605,140]},
 {n:"11",t:"Conveyor out",d:"4 part types in one pass. The finished board leaves on the right conveyor.",f:[1440,470,110]}
 ];}
// part shape in local coords: y=0 is 16 px above board top (board 16..32)
function shape(fam,v,p,col,clinched){
 var g=el("g",{},p),dk="#7a5a1a",lead=function(x1,x2){if(clinched)el("path",{d:"M"+x1+" 46 l-8 7 M"+x2+" 46 l8 7",stroke:col,"stroke-width":4,fill:"none"},g);};
 if(fam==="cust"){
  var ring=function(cx,y,w,h){el("rect",{x:cx-w/2,y:y,width:w,height:h,rx:2,fill:col},g);el("rect",{x:cx-w/2+3,y:y,width:w-6,height:Math.min(5,h-2),fill:"rgba(0,0,0,.45)"},g);};
  if(v===0){ring(0,-14,12,8);el("rect",{x:-4,y:-6,width:8,height:16,fill:col},g);el("rect",{x:-6,y:10,width:12,height:6,fill:col},g);el("rect",{x:-2,y:16,width:4,height:24,fill:col},g);}
  else if(v===1){ring(0,-40,20,10);el("rect",{x:-7,y:-30,width:14,height:38,fill:col},g);el("rect",{x:-11,y:8,width:22,height:8,fill:col},g);el("rect",{x:-4,y:16,width:8,height:30,fill:col},g);}
  else if(v===2){el("rect",{x:-5,y:13,width:10,height:4,rx:1,fill:col},g);el("path",{d:"M-5 17 L-3 34 L-1 34 L-1 19 L1 19 L1 34 L3 34 L5 17 Z",fill:col},g);}
  else{el("rect",{x:-10,y:10,width:20,height:6,rx:2,fill:col},g);el("path",{d:"M-10 16 L-6 42 L-3 42 L-3 20 L3 20 L3 42 L6 42 L10 16 Z",fill:col},g);el("rect",{x:-1,y:20,width:2,height:22,fill:col},g);}
 }else if(fam==="pin"){
  if(v===0){el("rect",{x:-3,y:-12,width:6,height:58,fill:col},g);}
  else if(v===1){el("rect",{x:-3,y:-12,width:6,height:58,rx:3,fill:col},g);}
  else if(v===2){el("rect",{x:-3,y:-14,width:6,height:60,fill:col},g);el("ellipse",{cx:0,cy:24,rx:6,ry:10,fill:col},g);el("ellipse",{cx:0,cy:24,rx:2,ry:7,fill:"#0f4d2d"},g);}
  else{el("rect",{x:-3,y:-4,width:6,height:50,fill:col},g);el("rect",{x:-8,y:-16,width:16,height:12,rx:4,fill:col},g);}
  if(clinched)el("path",{d:"M0 46 l9 7",stroke:col,"stroke-width":5,fill:"none"},g);
 }else if(fam==="eyelet"){
  if(v===0){el("rect",{x:-15,y:10,width:30,height:6,rx:2,fill:col},g);el("rect",{x:-6,y:16,width:12,height:22,fill:col},g);}
  else if(v===1){el("path",{d:"M-15 6 L15 6 L6 16 L-6 16 Z",fill:col},g);el("rect",{x:-6,y:16,width:12,height:22,fill:col},g);}
  else if(v===2){el("rect",{x:-13,y:9,width:26,height:7,rx:4,fill:col},g);el("rect",{x:-5,y:16,width:10,height:22,fill:col},g);}
  else{el("rect",{x:-9,y:11,width:18,height:5,rx:2,fill:col},g);el("rect",{x:-4,y:16,width:8,height:26,fill:col},g);}
  el("rect",{x:-2,y:16,width:4,height:22,fill:"rgba(0,0,0,.35)"},g);
  if(clinched)el("path",{d:"M-6 38 l-7 5 M6 38 l7 5",stroke:col,"stroke-width":4,fill:"none"},g);
 }else{
  if(v===0){el("rect",{x:-5,y:-18,width:10,height:34,fill:col},g);el("rect",{x:-2,y:16,width:4,height:30,fill:col},g);lead(-2,2);}
  else if(v===1){el("rect",{x:-10,y:-20,width:20,height:28,rx:2,fill:col},g);el("circle",{cx:0,cy:-8,r:3,fill:"#0f4d2d"},g);el("rect",{x:-6,y:8,width:12,height:8,fill:col},g);el("rect",{x:-6,y:16,width:3,height:30,fill:col},g);el("rect",{x:3,y:16,width:3,height:30,fill:col},g);lead(-5,5);}
  else if(v===2){el("path",{d:"M-3 46 L-3 -4 L22 -4 L22 4 L3 4 L3 46 Z",fill:col},g);lead(-3,3);}
  else{el("circle",{cx:0,cy:-10,r:11,fill:"none",stroke:col,"stroke-width":6},g);el("rect",{x:-4,y:0,width:8,height:16,fill:col},g);el("rect",{x:-2,y:16,width:4,height:30,fill:col},g);lead(-2,2);}
 }
 return g;
}
function InsertAnim(svg,opts){
  opts=opts||{};this.opts=opts;this.svg=svg;svg.setAttribute("viewBox","0 0 1600 720");
  this.fixed=(opts.model&&opts.model!=="cycle")?opts.model:null;
  var defs=el("defs",{},svg),mid="ia"+Math.floor(Math.random()*1e6);
  var m=el("mask",{id:mid},defs);el("rect",{x:0,y:0,width:1600,height:720,fill:"#fff"},m);this.hole=el("circle",{cx:800,cy:360,r:0,fill:"#000"},m);
  this.root=el("g",{},svg);this.mid=mid;
  this.dim=el("rect",{x:0,y:0,width:1600,height:720,rx:24,fill:"var(--ia-dim,rgba(6,28,25,.6))",mask:"url(#"+mid+")",opacity:0},svg);
  this.ring=el("circle",{fill:"none",stroke:"#e0a63b","stroke-width":3,"stroke-dasharray":"6 8",opacity:0},svg);
  var F="Inter,Arial,sans-serif";
  this.cg=el("g",{opacity:0},svg);
  this.cbox=el("rect",{rx:12,fill:"rgba(7,52,45,.95)",stroke:"#e0a63b","stroke-width":2},this.cg);
  this.cnum=el("text",{"font-size":22,"font-weight":800,fill:"#e0a63b","font-family":F},this.cg);
  this.ctit=el("text",{"font-size":26,"font-weight":800,fill:"#fff","font-family":F},this.cg);
  this.cdesc=el("text",{"font-size":17,fill:"#d7e7e3","font-family":F},this.cg);
  this.model=null;this.build(this.fixed||"T");
}
InsertAnim.prototype.build=function(mk){
  if(this.model===mk)return;this.model=mk;var M=MODELS[mk];this.STEPS=steps(mk);
  var root=this.root;while(root.firstChild)root.removeChild(root.firstChild);
  var c={body:"var(--ia-body,#eef4f2)",stroke:"var(--ia-stroke,#0c665c)",ink:"var(--ia-ink,#10201e)",dark:"var(--ia-dark,#33413f)"},F="Inter,Arial,sans-serif";
  var lab=function(x,y,t,o){o=o||{};var e=el("text",{x:x,y:y,"font-size":o.s||15,"font-weight":o.w||700,fill:o.f||c.ink,opacity:o.op||.6,"font-family":F,"letter-spacing":".5","text-anchor":o.a||"middle"},root);e.textContent=t;return e;};
  // X-Y table, conveyors
  el("rect",{x:300,y:590,width:1000,height:22,rx:6,fill:"#9aa6a3"},root);
  this.carr=el("rect",{y:574,width:300,height:16,rx:4,fill:"#5d6b68"},root);
  lab(800,636,M.press?"X-Y TABLE · P2P 0.025 mm · repeat 0.05 mm":"X-Y TABLE · 0.001 mm/pulse");
  [[20,300],[1300,1580]].forEach(function(r){el("rect",{x:r[0],y:471,width:r[1]-r[0],height:10,rx:3,fill:"#7d8a87"},root);for(var x=r[0]+20;x<r[1];x+=40)el("circle",{cx:x,cy:486,r:6,fill:"#5d6b68"},root);});
  lab(160,520,"CONVEYOR IN →");lab(1440,520,"→ CONVEYOR OUT");
  el("rect",{x:300,y:471,width:1000,height:6,fill:"#b9c3c1"},root);
  // clinch bases
  this.cl=[];var self=this;
  HXS.forEach(function(x,i){var g=el("g",{},root);el("rect",{x:-22,y:0,width:44,height:44,rx:5,fill:"#2a3533"},g);el("rect",{x:-13,y:-8,width:26,height:10,rx:2,fill:COL[i]},g);self.cl.push(g);});
  lab(470,548,M.press?"PCB PEDESTALS":"CLINCH BASES",{a:"end",s:13});
  this.chk=el("circle",{cx:1180,cy:545,r:11,fill:"#8d9997"},root);lab(1180,575,"MISS CHECK",{s:13});
  // head → part legend
  HXS.forEach(function(x,i){el("rect",{x:x-74,y:662,width:148,height:44,rx:8,fill:"var(--ia-legend,rgba(255,255,255,.65))",stroke:COL[i],"stroke-width":3},root);
    lab(x,680,"HEAD "+(i+1),{s:13,w:800,f:COL[i]==="#aeb9be"?"#6d7a80":COL[i],op:1});lab(x,699,M.press&&M.hole?(M.parts[i]+" · Ø"+M.hole[i]):M.parts[i],{s:13,op:.85});});
  // board
  this.board=el("g",{},root);
  el("rect",{x:0,y:BY,width:BW,height:16,rx:3,fill:"#1d7a4a"},this.board);
  el("circle",{cx:22,cy:BY+8,r:5,fill:"#e0a63b"},this.board);el("circle",{cx:BW-22,cy:BY+8,r:5,fill:"#e0a63b"},this.board);
  this.slots=[];for(var k=0;k<NI;k++){var g=el("g",{transform:"translate("+BH[k]+" "+(BY-16)+")"},this.board);
    el("rect",{x:-4,y:16,width:8,height:16,fill:"#0f4d2d"},g);this.slots.push(shape(M.fam,k%4,g,COL[k%4],true));}
  // camera
  var cam=el("g",{transform:"translate("+CAMX+" 300)"},root);el("rect",{x:-22,y:-34,width:44,height:50,rx:6,fill:"#1f2a28"},cam);el("circle",{cx:0,cy:16,r:9,fill:"#4aa3c7"},cam);
  this.beam=el("path",{fill:"rgba(74,163,199,.25)",stroke:"#4aa3c7","stroke-width":2,"stroke-dasharray":"5 5"},root);
  lab(CAMX,252,"CAMERA");
  // feeders + tracks
  this.reels=[];this.bowls=[];this.tracks=[];
  HXS.forEach(function(x,i){
    var fd=M.feed[i];
    if(fd==="reel"){var r=el("g",{},root);el("circle",{cx:0,cy:0,r:56,fill:"#dfe7e5",stroke:COL[i],"stroke-width":5},r);el("circle",{cx:0,cy:0,r:15,fill:c.stroke},r);
      for(var q=0;q<12;q++)el("rect",{x:-2,y:-50,width:4,height:14,fill:COL[i],transform:"rotate("+q*30+")"},r);self.reels.push([r,x,i]);}
    else{el("ellipse",{cx:x,cy:66,rx:66,ry:24,fill:"#cfe0f0",stroke:COL[i],"stroke-width":5},root);
      el("path",{d:"M"+(x-66)+" 66 L"+(x-50)+" 128 Q"+x+" 146 "+(x+50)+" 128 L"+(x+66)+" 66",fill:"#9fbfdd",stroke:COL[i],"stroke-width":4},root);
      var bp=el("g",{},root);for(var q2=0;q2<7;q2++)el("rect",{x:-6,y:-3,width:12,height:6,rx:2,fill:COL[i]},bp);self.bowls.push([bp,x,i]);}
    el("rect",{x:x-5,y:fd==="reel"?146:144,width:10,height:48,fill:"#c9d2d0"},root);
    var tr=el("g",{},root);for(var q3=0;q3<3;q3++)el("rect",{x:-4,y:-3,width:8,height:6,rx:2,fill:COL[i]},tr);self.tracks.push([tr,x]);
    var t=lab(x,fd==="reel"?168:166,"F"+(i+1)+" · "+(fd==="reel"?"REEL":"BOWL"),{s:13,w:800,op:.75});t.setAttribute("x",x+(i%2?-0:0));
  });
  // gantry
  el("rect",{x:470,y:196,width:660,height:30,rx:8,fill:c.body,stroke:c.stroke,"stroke-width":3},root);
  var gt=el("text",{"data-title":1,x:40,y:70,"font-size":44,"font-weight":800,fill:c.stroke,"font-family":F},root);gt.textContent=M.code;
  var g2=el("text",{"data-title":1,x:42,y:102,"font-size":18,"font-weight":700,fill:c.ink,opacity:.7,"font-family":F,"letter-spacing":"1"},root);g2.textContent=M.title.toUpperCase();
  var g3=el("text",{"data-title":1,x:42,y:128,"font-size":18,"font-weight":700,fill:c.ink,opacity:.7,"font-family":F,"letter-spacing":"1"},root);g3.textContent="4 HEADS · 4 FEEDERS · 4 PARTS";
  // heads
  this.heads=HXS.map(function(x,i){var g=el("g",{},root);
    el("rect",{x:-27,y:-150,width:54,height:96,rx:8,fill:c.dark},g);
    el("rect",{x:-27,y:-150,width:54,height:12,rx:6,fill:COL[i]},g);
    var tx=el("text",{x:0,y:-108,"font-size":18,"font-weight":800,fill:"#fff","text-anchor":"middle","font-family":F},g);tx.textContent="H"+(i+1);
    var dial=el("g",{transform:"translate(0 -78)"},g);el("circle",{cx:0,cy:0,r:12,fill:"#fff",stroke:COL[i],"stroke-width":3},dial);var nd=el("line",{x1:0,y1:0,x2:0,y2:-10,stroke:"#d23b2b","stroke-width":3},dial);
    el("rect",{x:-10,y:-54,width:20,height:30,rx:3,fill:"#5d6b68"},g);
    el("path",{d:"M-13 -24 L-13 -4 M13 -24 L13 -4",stroke:"#cfd8d6","stroke-width":5},g);
    var part=shape(M.fam,i,g,COL[i],false);
    return {g:g,part:part,nd:nd,x:x};});
};
InsertAnim.MODELS=MODELS;InsertAnim.PERIOD=BP;InsertAnim.COLORS=COL;
InsertAnim.prototype.setModel=function(m){this.fixed=m==="cycle"?null:m;this.build(this.fixed||"T");};
InsertAnim.prototype.render=function(t,focus,amt){
  var nb=Math.floor(t/BP),u=t-nb*BP,i;
  this.build(this.fixed||ORDER[nb%3]);
  var bx,ins=-1,sub=0,phase="in",hb=function(k){return HXS[k%4]-BH[k];};
  if(u<IN){bx=lerp(-BW-40,START,ease(u/IN));}
  else if(u<IN+MK){bx=START;phase="mark";}
  else if(u<IN+MK+NI*IP){var v=u-IN-MK;ins=Math.floor(v/IP);sub=(v-ins*IP)/IP;bx=lerp(ins===0?START:hb(ins-1),hb(ins),ease(sub/0.3));phase="insert";}
  else{bx=lerp(hb(NI-1),1640,ease((u-IN-MK-NI*IP)/OUT));phase="out";}
  this.board.setAttribute("transform","translate("+bx.toFixed(1)+" 0)");
  this.carr.setAttribute("x",Math.max(300,Math.min(1000,bx)).toFixed(1));
  for(i=0;i<NI;i++)this.slots[i].setAttribute("opacity",(phase==="out"||(phase==="insert"&&(i<ins||(i===ins&&sub>=0.5))))?1:0);
  if(phase==="mark"){var mk=(u-IN)/MK,fx=bx+(mk<0.5?22:BW-22);this.beam.setAttribute("d","M"+(CAMX-8)+" 320 L"+(fx-10)+" "+BY+" L"+(fx+10)+" "+BY+" L"+(CAMX+8)+" 320 Z");this.beam.setAttribute("opacity",1);}
  else this.beam.setAttribute("opacity",0);
  var REST=330,YI=BY-16,ANG=MODELS[this.model].press?[0,0,0,0]:[0,90,45,180];
  this.heads.forEach(function(h,hi){
    var act=(phase==="insert"&&ins%4===hi),y=REST,ang=0,has=true,A=ANG[hi];
    if(act){if(sub<0.3){ang=lerp(0,A,ease(sub/0.3));}else if(sub<0.5){ang=A;y=lerp(REST,YI,ease((sub-0.3)/0.2));}else if(sub<0.65){y=YI;has=false;ang=A;}else{y=lerp(YI,REST,ease((sub-0.65)/0.35));has=sub>0.9;ang=lerp(A,0,ease((sub-0.65)/0.35));}}
    h.g.setAttribute("transform","translate("+h.x+" "+y.toFixed(1)+")");
    h.part.setAttribute("opacity",has?1:0);h.nd.setAttribute("transform","rotate("+ang.toFixed(1)+")");
  });
  var self=this;
  this.cl.forEach(function(g,hi){var cu=phase==="insert"&&ins%4===hi&&sub>0.45&&sub<0.72?Math.sin(Math.PI*cl((sub-0.45)/0.27)):0;g.setAttribute("transform","translate("+HXS[hi]+" "+(520-12*cu).toFixed(1)+")");});
  this.chk.setAttribute("fill",phase==="insert"&&sub>0.55&&sub<0.85?"#18e07a":"#8d9997");
  var used=function(hi){var n=nb*2;if(phase==="out")return n+2;if(phase!=="insert")return n;for(var k=0;k<=ins;k++)if(k%4===hi)n+=(k===ins?sub:1);return n;};
  this.reels.forEach(function(r){r[0].setAttribute("transform","translate("+r[1]+" 86) rotate("+(used(r[2])*30).toFixed(1)+")");});
  this.bowls.forEach(function(b){var ch=b[0].children;for(var j=0;j<ch.length;j++){var a=t*1.4+j*0.9+b[2];ch[j].setAttribute("transform","translate("+(b[1]+50*Math.cos(a)).toFixed(1)+" "+(66+17*Math.sin(a)).toFixed(1)+") rotate("+(a*57.3+90).toFixed(0)+")");}});
  this.tracks.forEach(function(tr,ti){var ch=tr[0].children;for(var j=0;j<ch.length;j++){var yy=150+((j*16+t*14+ti*5)%44);ch[j].setAttribute("transform","translate("+tr[1]+" "+yy.toFixed(1)+")");}});
  this.count=nb*NI+(phase==="insert"?ins+(sub>=0.5?1:0):phase==="out"?NI:0);this.phase=phase;this.active=phase==="insert"?ins%4:-1;
  this.setFocus(focus,amt===undefined?1:amt);
};
InsertAnim.prototype.setFocus=function(idx,amt){
  if(idx===undefined||idx===null||idx<0){amt=0;idx=this.focusIdx>=0?this.focusIdx:0;}else this.focusIdx=idx;
  var s=this.STEPS[idx],f=s.f;
  this.hole.setAttribute("cx",f[0]);this.hole.setAttribute("cy",f[1]);this.hole.setAttribute("r",f[2]);
  this.dim.setAttribute("opacity",amt.toFixed(2));
  this.ring.setAttribute("cx",f[0]);this.ring.setAttribute("cy",f[1]);this.ring.setAttribute("r",f[2]+4);this.ring.setAttribute("opacity",amt.toFixed(2));
  this.cg.setAttribute("opacity",(this.opts.callout===false?0:amt).toFixed(2));
  if(this.opts.callout===false)return;
  var W=Math.max(400,Math.min(580,s.d.length*8.2)),H=104,cx=f[0]+f[2]+24,cy=f[1]-H/2;
  if(cx+W>1590)cx=f[0]-f[2]-24-W;
  if(cx<10){cx=Math.max(10,Math.min(1590-W,f[0]-W/2));cy=f[1]+f[2]+16;if(cy+H>712)cy=f[1]-f[2]-20-H;}
  cy=Math.max(8,Math.min(712-H,cy));
  this.cbox.setAttribute("x",cx);this.cbox.setAttribute("y",cy);this.cbox.setAttribute("width",W);this.cbox.setAttribute("height",H);
  this.cnum.setAttribute("x",cx+20);this.cnum.setAttribute("y",cy+38);this.cnum.textContent=s.n;
  this.ctit.setAttribute("x",cx+62);this.ctit.setAttribute("y",cy+38);this.ctit.textContent=s.t;
  var words=s.d.split(" "),lines=[""],maxc=Math.floor((W-40)/8.4);
  words.forEach(function(w){if((lines[lines.length-1]+" "+w).trim().length>maxc)lines.push(w);else lines[lines.length-1]=(lines[lines.length-1]+" "+w).trim();});
  while(this.cdesc.firstChild)this.cdesc.removeChild(this.cdesc.firstChild);
  for(var i=0;i<Math.min(2,lines.length);i++){var ts=el("tspan",{x:cx+20,y:cy+66+i*22},this.cdesc);ts.textContent=lines[i];}
};
global.InsertAnim=InsertAnim;
})(window);
/* S7040P canvas wrapper: InsertAnim (SVG, insert-anim.svg.js) -> p3cv canvas contract via SVG2Canvas.
   World 1600x1000; the 1600x720 SVG sits at y=140. One board = InsertAnim.PERIOD (12.8 s): 8 presses,
   2 per head. Model 'C' = 4 bowls -> 4 heads, pins + multi-finger clips pressed flush (press:true).
   Customer dimensions are NOT in this public example; a project may set them after this file:
     InsertAnim.MODELS.C.dia=[...]; InsertAnim.MODELS.C.hole=[...]   (strings, mm)
   Extra opts: noTitle hides the model title block (video/thumbnail already show the name). */
(function (G) {
  var IA = G.InsertAnim, P = IA.PERIOD, OY = 140, inst = null, svg = null;
  var STEPS = [
    { a: 0, b: 2, name: 'Conveyor in + board stop', f: 0 },
    { a: 2, b: 3.2, name: 'Fiducial vision correction', f: 1 },
    { a: 3.2, b: 4.2, name: 'Bowl 1 → Head 1: medium pin', f: 3 },
    { a: 4.2, b: 5.2, name: 'Bowl 2 → Head 2: large pin', f: 4 },
    { a: 5.2, b: 6.2, name: 'Bowl 3 → Head 3: medium clip', f: 5 },
    { a: 6.2, b: 7.2, name: 'Bowl 4 → Head 4: large clip', f: 6 },
    { a: 7.2, b: 11.2, name: 'Servo press flush + miss check', f: 8 },
    { a: 11.2, b: P, name: 'Conveyor out', f: 10 }];
  function ensure() {
    if (inst) return;
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    inst = new IA(svg, { model: 'C', callout: false });
    STEPS.forEach(function (s) { var f = inst.STEPS[s.f].f; s.box = [f[0] - f[2], f[1] - f[2] + OY, 2 * f[2], 2 * f[2]] });
  }
  function stepAt(t) { t = ((t % P) + P) % P; for (var i = 0; i < STEPS.length; i++) if (t < STEPS[i].b) return i; return STEPS.length - 1 }
  var DARK = { '--ia-body': '#22312f', '--ia-stroke': '#4fb8a6', '--ia-ink': '#e6efed', '--ia-dark': '#3a4a48', '--ia-legend': 'rgba(255,255,255,.08)' };
  function render(ctx, W, H, o) {
    o = o || {}; ensure(); var t = ((o.t || 0) % P + P) % P, st = stepAt(t), dark = o.theme === 'dark';
    var f = o.focus || { x: 800, y: 500, s: 1 }, sc = Math.min(W / 1600, H / 1000) * f.s;
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H);
    ctx.translate(W / 2, H / 2); ctx.scale(sc, sc); ctx.translate(-f.x, -f.y);
    inst.render(t, -1, 0);
    var tt = svg.querySelectorAll('[data-title]'); for (var k = 0; k < tt.length; k++) tt[k].setAttribute('display', o.noTitle ? 'none' : 'inline');
    ctx.save(); ctx.translate(0, OY); SVG2Canvas.draw(ctx, svg, { vars: dark ? DARK : null }); ctx.restore();
    if (!o.noBox) { var b = STEPS[st].box; ctx.strokeStyle = '#e0a63b'; ctx.lineWidth = 4; ctx.setLineDash([14, 10]); ctx.strokeRect(b[0], b[1], b[2], b[3]); ctx.setLineDash([]) }
    if (!o.noHud) { ctx.fillStyle = dark ? '#e6efed' : '#0c665c'; ctx.font = '800 34px Inter, Arial, sans-serif'; ctx.textAlign = 'right';
      ctx.fillText('Parts pressed: ' + (inst.count || 0), 1560, 120) }
    ctx.restore(); return { step: st, count: inst.count };
  }
  G.S7040PAnim = { CYCLE: P, STEPS: STEPS, stepAt: stepAt, render: render };
})(window);
