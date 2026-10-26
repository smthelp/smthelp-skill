/* JUKI JM horizontal-slide gripper nozzle (SM-2070) — pick & insert cycle. Southern Machinery
   JawAnim.render(ctx,W,H,{t,theme:'dark'|'light',focus:{x,y,s},noBox,noHud}) world 1600x1000 */
(function(G){
var CYCLE=12,PX=13; // px per mm
var C={teal:'#00A896',tealD:'#028090',sky:'#38BDF8',lime:'#84CC16',yel:'#f5c518',grn:'#2fa84f',red:'#ef4444'};
var STEPS=[
 {a:0,b:1.5,name:'Jaws open over the part',box:[290,250,220,420]},
 {a:1.5,b:3,name:'Descend into the tray pocket',box:[250,330,300,360]},
 {a:3,b:4.5,name:'Parallel horizontal clamp',box:[300,520,200,150]},
 {a:4.5,b:6.5,name:'Lift and move at speed',box:[300,150,620,420]},
 {a:6.5,b:7.5,name:'Vision check from below',box:[700,300,240,640-60]},
 {a:7.5,b:9.3,name:'Insert leads into the PCB',box:[1160,300,280,420]},
 {a:9.3,b:12,name:'Release and retract',box:[1160,120,280,560]}];
function cl(x){return x<0?0:x>1?1:x}
function ez(x){x=cl(x);return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2}
function L(a,b,p){return a+(b-a)*p}
function seg(t,a,b){return ez((t-a)/(b-a))}
function stepAt(t){t=((t%CYCLE)+CYCLE)%CYCLE;for(var i=0;i<STEPS.length;i++)if(t<STEPS[i].b)return i;return STEPS.length-1}
var PICKX=400,MIDX=820,PLX=1300,UPY=440,DNY=630,PARTW=120,PARTMM=PARTW/PX;
function state(t){
  var x=PICKX,y=UPY,o=0,held=false;
  if(t<1.5){o=11*seg(t,0,1.5)}
  else if(t<3){o=11;y=L(UPY,DNY,seg(t,1.5,3))}
  else if(t<4.5){y=DNY;o=L(11,PARTMM,seg(t,3,4.2));held=t>4.2}
  else if(t<9.3){o=PARTMM;held=true;
    if(t<5.3)y=L(DNY,UPY,seg(t,4.5,5.3));
    else if(t<6.5){x=L(PICKX,MIDX,seg(t,5.3,6.5))}
    else if(t<7.5){x=MIDX}
    else if(t<8.3){x=L(MIDX,PLX,seg(t,7.5,8.3))}
    else {x=PLX;y=L(UPY,DNY,seg(t,8.3,9.3))}}
  else if(t<10){x=PLX;y=DNY;o=L(PARTMM,11,seg(t,9.3,9.9))}
  else if(t<10.8){x=PLX;o=11;y=L(DNY,UPY,seg(t,10,10.8))}
  else {x=L(PLX,PICKX,seg(t,10.8,11.9));o=L(11,0,seg(t,10.8,11.9))}
  return {x:x,y:y,o:o,held:held};
}
function rr(c,x,y,w,h,r){c.beginPath();c.moveTo(x+r,y);c.arcTo(x+w,y,x+w,y+h,r);c.arcTo(x+w,y+h,x,y+h,r);c.arcTo(x,y+h,x,y,r);c.arcTo(x,y,x+w,y,r);c.closePath()}
function part(c,cx,by,a){ // bobbin coil: body bottom at by
  c.save();c.globalAlpha=a==null?1:a;
  c.fillStyle='#cbd5e1';c.fillRect(cx-37,by,5,46);c.fillRect(cx+32,by,5,46);
  c.fillStyle='#1f2937';rr(c,cx-60,by-90,120,90,6);c.fill();
  c.fillStyle='#b45309';rr(c,cx-46,by-80,92,58,4);c.fill();
  c.strokeStyle='#f59e0b';c.lineWidth=2;for(var i=0;i<9;i++){c.beginPath();c.moveTo(cx-46,by-76+i*6.2);c.lineTo(cx+46,by-74+i*6.2);c.stroke()}
  c.fillStyle='#111827';c.fillRect(cx-60,by-14,120,14);
  c.restore();
}
function nozzle(c,s,dark){
  var x=s.x,y=s.y,h=o2px(s.o)/2;
  // jaws (tips at y)
  var jg=c.createLinearGradient(0,y-150,0,y);jg.addColorStop(0,'#9aa5b4');jg.addColorStop(1,'#e2e8f0');
  c.fillStyle=jg;
  c.fillRect(x-h-14,y-120,14,120);c.fillRect(x+h,y-120,14,120);
  c.fillStyle='#64748b';c.fillRect(x-h-14,y-8,14,8);c.fillRect(x+h,y-8,14,8);
  // slide block
  c.fillStyle='#475569';rr(c,x-100,y-160,200,42,6);c.fill();
  c.fillStyle='#94a3b8';c.fillRect(x-h-22,y-150,30,26);c.fillRect(x+h-8,y-150,30,26);
  c.fillStyle=C.grn;rr(c,x-78,y-200,156,40,8);c.fill();
  // yellow JUKI body
  c.fillStyle=C.yel;c.beginPath();c.moveTo(x-60,y-200);c.lineTo(x-40,y-290);c.lineTo(x+40,y-290);c.lineTo(x+60,y-200);c.closePath();c.fill();
  c.fillStyle=C.grn;c.fillRect(x-50,y-306,100,18);
  c.fillStyle='#cbd5e1';c.fillRect(x-18,y-420,36,116);c.fillStyle='#94a3b8';c.fillRect(x-24,y-360,48,10);
  // head carriage
  c.fillStyle=dark?'#334155':'#64748b';rr(c,x-70,y-480,140,62,8);c.fill();
  c.fillStyle=dark?'rgba(255,255,255,.12)':'rgba(0,0,0,.12)';c.fillRect(0,y-462,1600,8);
}
function o2px(mm){return mm*PX}
function render(ctx,W,H,o){
  o=o||{};var dark=o.theme!=='light';var t=((o.t||0)%CYCLE+CYCLE)%CYCLE;var st=stepAt(t);var s=state(t);
  var ink=dark?'#e2e8f0':'#0f172a',mut=dark?'rgba(226,232,240,.6)':'#64748b';
  ctx.save();ctx.clearRect(0,0,W,H);
  var sc=Math.min(W/1600,H/1000)*(o.focus?o.focus.s:1),fx=o.focus?o.focus.x:800,fy=o.focus?o.focus.y:500;
  ctx.translate(W/2,H/2);ctx.scale(sc,sc);ctx.translate(-fx,-fy);
  // tray
  ctx.fillStyle=dark?'#3b4a63':'#cbd5e1';ctx.fillRect(110,640,580,110);
  [210,400,590].forEach(function(px){ctx.fillStyle=dark?'#1e293b':'#94a3b8';ctx.fillRect(px-95,640,190,56)});
  ctx.fillStyle=mut;ctx.font='700 22px Arial';ctx.textAlign='center';ctx.fillText('MATRIX TRAY',400,790);
  part(ctx,210,640);part(ctx,590,640);
  // part in pick pocket
  if(!s.held&&t<9.3)part(ctx,PICKX,640);
  if(t>10.6)part(ctx,PICKX,640,cl((t-10.6)/1.2));
  // PCB
  ctx.fillStyle='#166534';ctx.fillRect(1120,640,360,22);ctx.fillStyle='#14532d';ctx.fillRect(1120,662,360,6);
  [PLX-35,PLX+35].forEach(function(hx){ctx.fillStyle='#d4a640';ctx.fillRect(hx-9,640,18,22);ctx.fillStyle='#0b1222';ctx.fillRect(hx-4,640,8,22)});
  ctx.fillStyle=mut;ctx.fillText('PCB',1300,790);
  if(!s.held&&t>=9.3&&t<11.7)part(ctx,PLX,640,1-cl((t-11.2)/0.5));
  // camera
  ctx.fillStyle=dark?'#334155':'#475569';rr(ctx,MIDX-50,820,100,60,8);ctx.fill();ctx.fillStyle='#0ea5e9';ctx.beginPath();ctx.arc(MIDX,820,20,0,6.3);ctx.fill();
  ctx.fillStyle=mut;ctx.fillText('UPWARD CAMERA',MIDX,915);
  if(t>6.5&&t<7.5){var a=Math.sin(Math.PI*(t-6.5));ctx.fillStyle='rgba(56,189,248,'+(0.25*a)+')';ctx.beginPath();ctx.moveTo(MIDX-20,820);ctx.lineTo(MIDX-110,UPY+40);ctx.lineTo(MIDX+110,UPY+40);ctx.lineTo(MIDX+20,820);ctx.fill();
    ctx.strokeStyle='rgba(132,204,22,'+a+')';ctx.lineWidth=3;ctx.strokeRect(MIDX-70,UPY-96,140,150);ctx.fillStyle='rgba(132,204,22,'+a+')';ctx.font='800 22px Arial';ctx.fillText('✓ OK',MIDX+130,UPY-60)}
  // held part
  if(s.held)part(ctx,s.x,s.y+10);
  nozzle(ctx,s,dark);
  // clamp arrows
  if(t>3&&t<4.5){var aa=Math.sin(Math.PI*(t-3)/1.5);ctx.strokeStyle='rgba(0,168,150,'+aa+')';ctx.fillStyle=ctx.strokeStyle;ctx.lineWidth=5;
    [[-1],[1]].forEach(function(d){var sx=s.x+d[0]*150,ex=s.x+d[0]*95;ctx.beginPath();ctx.moveTo(sx,s.y-60);ctx.lineTo(ex,s.y-60);ctx.stroke();ctx.beginPath();ctx.moveTo(ex,s.y-60);ctx.lineTo(ex+d[0]*14,s.y-70);ctx.lineTo(ex+d[0]*14,s.y-50);ctx.fill()})}
  // labels
  if(!o.noLabels){ctx.font='700 22px Arial';ctx.fillStyle=mut;var lr=s.x>700;ctx.textAlign=lr?'right':'left';ctx.fillText('SM-2070 GRIPPER NOZZLE',s.x+(lr?-90:90),s.y-240)}
  // HUD
  if(!o.noHud){ctx.fillStyle=dark?'rgba(15,23,42,.8)':'rgba(255,255,255,.9)';rr(ctx,1120,60,360,150,14);ctx.fill();ctx.strokeStyle=C.teal;ctx.lineWidth=2;ctx.stroke();
    ctx.textAlign='left';ctx.fillStyle=mut;ctx.font='700 18px Arial';ctx.fillText('JAW OPENING',1145,96);
    ctx.fillStyle=C.teal;ctx.font='800 50px Arial';ctx.fillText(s.o.toFixed(1)+' mm',1145,150);
    ctx.fillStyle=mut;ctx.font='600 17px Arial';ctx.fillText(s.held?'CLAMPED · horizontal slide':'range 0 – 11 mm',1145,188)}
  // focus box
  if(!o.noBox){var b=STEPS[st].box,pp=cl((t-STEPS[st].a)/0.4);ctx.save();ctx.strokeStyle='#38BDF8';ctx.lineWidth=4;ctx.setLineDash([14,10]);ctx.lineDashOffset=-t*30;ctx.globalAlpha=pp*0.9;rr(ctx,b[0],b[1],b[2],b[3],16);ctx.stroke();ctx.restore()}
  ctx.restore();return {step:st};
}
G.JawAnim={CYCLE:CYCLE,STEPS:STEPS,stepAt:stepAt,render:render,state:state};
})(window);
