/* smt-source-to-landing-page runtime: language, theme, tabs, videos, gallery,
   PDF preview, calculator, enquiry form. No external dependencies.
   The build script replaces the two markers below with JSON. */
/*I18N*/
/*CFG*/
const LANGS = CFG.langs;
const LANG_KEY = CFG.storage+"_lang", THEME_KEY = CFG.storage+"_theme";

/* Wrap left-to-right runs (model codes, dimensions, e-mail) in isolates when the
   string contains right-to-left text, so "12.7 mm" is not reordered in Arabic. */
var RTL_TEXT=/[\u0590-\u05FF\u0600-\u06FF\u0700-\u074F\u0750-\u077F\u08A0-\u08FF\uFB1D-\uFDFF\uFE70-\uFEFF]/;
function isolateRuns(s){
  s=String(s);
  if(!RTL_TEXT.test(s)) return s;
  var wrap=function(seg){
    if(!seg) return "";
    var core=seg.trim();
    if(core.length<3||!/[A-Za-z0-9]/.test(core)) return seg;
    var at=seg.indexOf(core);
    return seg.slice(0,at)+"\u2066"+core+"\u2069"+seg.slice(at+core.length);
  };
  var out="",cur="",i,ch;
  for(i=0;i<s.length;i++){
    ch=s.charAt(i);
    if(RTL_TEXT.test(ch)){ out+=wrap(cur); cur=""; out+=ch; }
    else cur+=ch;
  }
  return out+wrap(cur);
}
function T(lang,key){
  var d=I18N[lang]||I18N.en, v=d[key];
  if(v===undefined) v=I18N.en[key];
  return v===undefined?key:v;
}
function fmt(n,lang){
  try{ return new Intl.NumberFormat(lang==="zh"?"zh-CN":lang,{maximumFractionDigits:1}).format(n); }
  catch(e){ return String(Math.round(n*10)/10); }
}
function curLang(){ return document.documentElement.getAttribute("lang")||"en"; }

function applyLang(lang,persist){
  if(!I18N[lang]) lang="en";
  var meta=I18N[lang].__meta, root=document.documentElement;
  root.setAttribute("lang",lang);
  root.setAttribute("dir",meta.dir||"ltr");
  document.querySelectorAll("[data-i18n]").forEach(function(el){ el.textContent=isolateRuns(T(lang,el.getAttribute("data-i18n"))); });
  document.querySelectorAll("[data-i18n-alt]").forEach(function(el){ el.setAttribute("alt",isolateRuns(T(lang,el.getAttribute("data-i18n-alt")))); });
  document.querySelectorAll("[data-i18n-aria]").forEach(function(el){ el.setAttribute("aria-label",isolateRuns(T(lang,el.getAttribute("data-i18n-aria")))); });
  document.querySelectorAll("[data-i18n-title]").forEach(function(el){ el.setAttribute("title",isolateRuns(T(lang,el.getAttribute("data-i18n-title")))); });
  document.querySelectorAll("[data-i18n-ph]").forEach(function(el){ el.setAttribute("placeholder",T(lang,el.getAttribute("data-i18n-ph"))); });
  document.title=T(lang,"seo_title");
  var set=function(sel,attr,key){ var m=document.querySelector(sel); if(m) m.setAttribute(attr,T(lang,key)); };
  set('meta[name="description"]',"content","seo_desc");
  set('meta[property="og:title"]',"content","og_title");
  set('meta[property="og:description"]',"content","og_desc");
  set('meta[name="twitter:title"]',"content","og_title");
  set('meta[name="twitter:description"]',"content","og_desc");
  var li=document.getElementById("langIcon"); if(li) li.textContent=meta.short;
  /* Articles: show the visitor's language when a translation exists, else English plus a note. */
  document.querySelectorAll(".post").forEach(function(p){
    var arts=p.querySelectorAll(".art[data-blang]"), has=false;
    arts.forEach(function(a){ if(a.getAttribute("data-blang")===lang) has=true; });
    arts.forEach(function(a){ var bl=a.getAttribute("data-blang"); a.hidden = has ? bl!==lang : bl!=="en"; });
    var n=p.querySelector(".enonly"); if(n) n.hidden = has || lang==="en";
  });
  document.querySelectorAll("#langMenu button").forEach(function(b){ b.setAttribute("aria-current", b.getAttribute("data-lang")===lang?"true":"false"); });
  calc();
  if(window.MX) window.MX.render();
  if(window.NPI) window.NPI.progress();
  if(persist!==false){ try{ localStorage.setItem(LANG_KEY,lang); }catch(e){} }
}
function applyTheme(mode,persist){
  if(mode!=="dark") mode="light";
  document.documentElement.setAttribute("data-theme",mode);
  var ic=document.getElementById("themeIcon"); if(ic) ic.textContent= mode==="dark" ? "☾" : "☀";
  var mt=document.querySelector('meta[name="theme-color"]'); if(mt) mt.setAttribute("content", mode==="dark" ? CFG.themeDark : CFG.themeLight);
  if(persist!==false){ try{ localStorage.setItem(THEME_KEY,mode); }catch(e){} }
}

/* Calculator: inputs, intermediate vars and outputs come from product.json (calc).
   Every input is the visitor's; nothing is assumed. */
function num(id){ var el=document.getElementById(id); var v=parseFloat(el&&el.value); return isNaN(v)||v<0?0:v; }
var CALC_FN=null;
function calc(){
  var C=CFG.calc; if(!C||!C.outputs||!C.outputs.length) return;
  var lang=curLang();
  if(!CALC_FN){
    var src=C.vars.map(function(p){ return "var "+p[0]+"=("+p[1]+");"; }).join("")+
      "return ["+C.outputs.map(function(o){ return "("+o.expr+")"; }).join(",")+"];";
    CALC_FN=new Function(C.inputs.join(","),src);
  }
  var vals=CALC_FN.apply(null,C.inputs.map(num));
  C.outputs.forEach(function(o,i){
    var el=document.getElementById(o.id), v=vals[i]; if(!el) return;
    var dec=o.decimals||0, p=Math.pow(10,dec);
    el.textContent = v>0 && isFinite(v) ? (dec ? (Math.round(v*p)/p).toLocaleString(lang==="zh"?"zh-CN":lang) : fmt(Math.round(v),lang)) : "\u2014";
  });
}

(function boot(){
  var params=new URLSearchParams(location.search), lang="en", theme=null;
  try{
    lang = params.get("lang") || localStorage.getItem(LANG_KEY) || "en";
    theme = localStorage.getItem(THEME_KEY);
  }catch(e){ lang=params.get("lang")||"en"; }
  if(!I18N[lang]) lang="en";
  if(!theme) theme=(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)?"dark":"light";
  applyTheme(theme,false);

  var lm=document.getElementById("langMenu");
  lm.innerHTML=LANGS.map(function(c){ var m=I18N[c].__meta; return '<button type="button" role="menuitem" data-lang="'+c+'" lang="'+c+'"><span>'+m.label+'</span><span class="code">'+m.short+'</span></button>'; }).join("");
  document.getElementById("themeBtn").addEventListener("click",function(){
    applyTheme(document.documentElement.getAttribute("data-theme")==="dark"?"light":"dark",true);
  });
  var lw=document.getElementById("langWrap"), lb=document.getElementById("langBtn");
  var closeLang=function(){ lw.classList.remove("open"); lb.setAttribute("aria-expanded","false"); };
  lb.addEventListener("click",function(e){ e.stopPropagation(); var o=lw.classList.toggle("open"); lb.setAttribute("aria-expanded",o?"true":"false"); });
  lm.addEventListener("click",function(e){ var b=e.target.closest("button[data-lang]"); if(!b) return; applyLang(b.getAttribute("data-lang"),true); closeLang(); });
  document.addEventListener("click",closeLang);

  var hdr=document.getElementById("hdr");
  document.getElementById("burger").addEventListener("click",function(){ hdr.classList.toggle("navopen"); });
  document.getElementById("nav").addEventListener("click",function(e){ if(e.target.tagName==="A") hdr.classList.remove("navopen"); });

  /* FAB tabs */
  var tabs=[].slice.call(document.querySelectorAll(".ftab"));
  function selTab(tb){
    tabs.forEach(function(x){ var on=x===tb; x.classList.toggle("on",on); x.setAttribute("aria-selected",on?"true":"false"); x.tabIndex=on?0:-1;
      var p=document.getElementById(x.getAttribute("aria-controls")); p.classList.toggle("on",on); if(on) p.removeAttribute("hidden"); else p.setAttribute("hidden",""); });
  }
  tabs.forEach(function(tb,i){
    tb.tabIndex = i===0?0:-1;
    tb.addEventListener("click",function(){ selTab(tb); });
    tb.addEventListener("keydown",function(e){
      var k=e.key, rtl=document.documentElement.dir==="rtl", n=null;
      if(k==="ArrowRight"||k==="ArrowDown") n=tabs[(i+(rtl&&k==="ArrowRight"?-1:1)+tabs.length)%tabs.length];
      if(k==="ArrowLeft"||k==="ArrowUp") n=tabs[(i+(rtl&&k==="ArrowLeft"?1:-1)+tabs.length)%tabs.length];
      if(n){ e.preventDefault(); selTab(n); n.focus(); }
    });
  });

  /* Videos: click-to-load iframe inside the card; nothing contacts YouTube's player until then. */
  var grid=document.getElementById("vidGrid");
  function playCard(th){
    if(!th || th.querySelector("iframe")) return;
    var id=th.getAttribute("data-vid"), f=document.createElement("iframe");
    f.src="https://www.youtube-nocookie.com/embed/"+id+"?rel=0&autoplay=1";
    f.title=(th.parentNode.querySelector("h3")||{}).textContent||"YouTube video";
    f.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    f.setAttribute("allowfullscreen","");
    f.loading="lazy";
    th.innerHTML=""; th.appendChild(f); th.classList.add("playing");
  }
  if(grid) grid.addEventListener("click",function(e){ var b=e.target.closest(".pl"); if(b) playCard(b.closest(".th")); });
  document.querySelectorAll(".vchip").forEach(function(c){
    c.addEventListener("click",function(){
      var f=c.getAttribute("data-f");
      document.querySelectorAll(".vchip").forEach(function(x){ x.classList.toggle("on",x===c); x.setAttribute("aria-pressed",x===c?"true":"false"); });
      if(grid) grid.querySelectorAll(".vid").forEach(function(v){ v.hidden = !(f==="all"||v.getAttribute("data-cat")===f); });
    });
  });

  /* Lightbox: the image element has no src until opened (an empty src would request the page). */
  var lbx=document.getElementById("lb"), lbimg=lbx.querySelector("img");
  window.closeLb=function(){ lbx.classList.remove("open"); lbimg.removeAttribute("src"); };
  lbx.addEventListener("click",function(e){ if(e.target!==lbimg) closeLb(); });
  document.querySelectorAll(".galgrid figure").forEach(function(f){
    var open=function(){ var full=f.getAttribute("data-full"); if(!full) return; var im=f.querySelector("img");
      lbimg.setAttribute("alt", im.getAttribute("alt")||""); lbimg.src=full; lbx.classList.add("open"); };
    f.addEventListener("click",open);
    f.addEventListener("keydown",function(e){ if(e.key==="Enter"||e.key===" "){ e.preventDefault(); open(); } });
  });

  /* PDF preview: iframe gets its src only on demand and loses it on close. */
  var pm=document.getElementById("pdfModal"), pf=document.getElementById("pdfFrame");
  window.closePdf=function(){ pm.classList.remove("open"); pf.removeAttribute("src"); };
  document.getElementById("pdfClose").addEventListener("click",closePdf);
  pm.addEventListener("click",function(e){ if(e.target===pm) closePdf(); });
  document.querySelectorAll("[data-pdf]").forEach(function(b){
    b.addEventListener("click",function(){ pf.src=b.getAttribute("data-pdf"); pm.classList.add("open"); });
  });
  document.addEventListener("keydown",function(e){ if(e.key==="Escape"){ closeLang(); closeLb(); closePdf(); if(window.MX) window.MX.close(); } });

  ((CFG.calc&&CFG.calc.inputs)||[]).forEach(function(id){ var el=document.getElementById(id); if(el) el.addEventListener("input",calc); });

  /* Enquiry form opens the visitor's own mail client. */
  var qf=document.getElementById("qform");
  if(qf) qf.addEventListener("submit",function(e){
    e.preventDefault();
    var L=curLang();
    var lines=[].map.call(qf.querySelectorAll(".fld"),function(f){
      var lab=f.querySelector("label"), inp=f.querySelector("input,textarea,select");
      return (lab?lab.textContent:"")+": "+((inp&&inp.value)||"").trim();
    }).join("\n");
    location.href="mailto:"+CFG.email+"?subject="+encodeURIComponent(T(L,"f_subject"))+"&body="+encodeURIComponent(lines);
  });

  var tt=document.getElementById("toTop");
  window.addEventListener("scroll",function(){ tt.classList.toggle("show", window.scrollY>900); },{passive:true});
  tt.addEventListener("click",function(){ window.scrollTo({top:0,behavior: matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"}); });

  /* Printing: open every article and answer so the paper copy is complete. */
  window.addEventListener("beforeprint",function(){ document.querySelectorAll("details").forEach(function(d){ d.setAttribute("data-was",d.open?"1":"0"); d.open=true; }); });
  window.addEventListener("afterprint",function(){ document.querySelectorAll("details[data-was]").forEach(function(d){ d.open=d.getAttribute("data-was")==="1"; d.removeAttribute("data-was"); }); });

  var reduced=window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(reduced){ var hi=document.getElementById("heroImgs"); if(hi) hi.classList.remove("playing"); }

  mxInit();
  npiInit();
  applyLang(lang,false);
})();

/* ---------------------------------------------------------------- optional: component -> feeder quick-match
   Data: <script type="application/json" id="matcherData"> written by build.py from product.json "matcher".
   Every label is an i18n key (mx_*), so the table re-renders in the visitor's language. */
function mxInit(){
  var src=document.getElementById("matcherData"); if(!src) return;
  var D=JSON.parse(src.textContent), R=D.rows, FE={};
  D.feeders.forEach(function(f){ FE[f.id]=f; });
  var $=function(id){ return document.getElementById(id); };
  var F={q:$("mxQ"),cat:$("mxCat"),pack:$("mxPack"),feeder:$("mxFeeder"),pitch:$("mxPitch"),L:$("mxL"),W:$("mxW"),H:$("mxH"),leads:$("mxLeads"),ld:$("mxLd"),unk:$("mxUnk")};
  var body=$("mxBody"), modal=$("mxModal"), det=$("mxDetail");
  var esc=function(s){ return String(s==null?"":s).replace(/[&<>"]/g,function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); };
  var n1=function(v){ return v==null||v===""?null:(Math.round(v*100)/100).toString(); };
  var L=function(k){ return T(curLang(),k); };
  var U=function(){ return L("mx_unknown_v"); };
  function bin(name,sel){ var v=sel&&sel.value; if(v===""||v==null) return null; return D.bins[name][+v]; }
  function inBin(v,b){ if(!b) return true; if(v==null) return F.unk.checked; return v>b[0]&&v<=b[1]; }
  function hgt(r){ return r.H!=null?r.H:r.OH; }
  function feederTxt(r,lang){ var f=FE[r.feeder]; var s=f?(f.model?f.model+" · ":"")+T(lang,"mx_f_"+f.id+"n"):""; if(r.alt&&FE[r.alt]) s+=" ("+T(lang,"mx_or")+" "+FE[r.alt].model+")"; return s; }
  function hay(r){ var out=[r.spec||"",(FE[r.feeder]||{}).model||"",(FE[r.alt]||{}).model||""]; ["en",curLang()].forEach(function(lg){ out.push(T(lg,"mx_t_"+r.type),T(lg,"mx_c_"+r.cat),T(lg,"mx_p_"+r.pack),T(lg,"mx_f_"+r.feeder+"n")); }); return out.join(" ").toLowerCase(); }
  function body3(r){ return (r.L==null&&r.W==null&&hgt(r)==null)?U():[n1(r.L)||"?",n1(r.W)||"?",n1(hgt(r))||"?"].join(" × "); }
  function match(r){
    var q=(F.q.value||"").trim().toLowerCase();
    if(q && q.split(/\s+/).some(function(w){ return hay(r).indexOf(w)<0; })) return false;
    if(F.cat.value && r.cat!==F.cat.value) return false;
    if(F.pack.value && r.pack!==F.pack.value) return false;
    if(F.feeder.value && r.feeder!==F.feeder.value && r.alt!==F.feeder.value) return false;
    return inBin(r.pitch,bin("pitch",F.pitch)) && inBin(r.L,bin("size",F.L)) && inBin(r.W,bin("size",F.W)) && inBin(hgt(r),bin("size",F.H)) &&
           inBin(r.leads,bin("leads",F.leads)) && inBin(r.ld,bin("ld",F.ld));
  }
  function render(){
    var lang=curLang(), shown=R.filter(match), th=[].map.call(document.querySelectorAll(".mx-table thead th"),function(h){ return h.textContent; });
    body.innerHTML=shown.map(function(r){
      var cells=[
        '<b>'+esc(T(lang,"mx_t_"+r.type))+'</b>'+(r.spec?'<small dir="ltr">'+esc(r.spec)+'</small>':''),
        esc(T(lang,"mx_c_"+r.cat)), esc(T(lang,"mx_p_"+r.pack)), '<span dir="ltr">'+esc(body3(r))+'</span>',
        '<span dir="ltr">'+esc(n1(r.pitch)||U())+'</span>', '<span dir="ltr">'+esc(r.leads==null?U():r.leads)+'</span>', '<span dir="ltr">'+esc(n1(r.ld)||U())+'</span>',
        (function(){ var f=FE[r.feeder]||{}; return '<span class="mx-fd" dir="ltr">'+esc(f.model||"")+'</span><small>'+esc(T(lang,"mx_f_"+r.feeder+"n"))+(r.alt&&FE[r.alt]?' · '+esc(T(lang,"mx_or"))+' '+esc(FE[r.alt].model):'')+'</small>'; })(), esc(T(lang,"mx_n_"+(r.nozzle||"tbc"))),
        '<span class="mx-st mx-s-'+esc(r.status)+'">'+esc(T(lang,"mx_s_"+r.status))+'</span>'];
      return '<tr tabindex="0" data-id="'+esc(r.id)+'">'+cells.map(function(c,i){ return '<td data-th="'+esc(th[i]||"")+'"><span class="mx-v">'+c+'</span></td>'; }).join("")+'</tr>';
    }).join("");
    $("mxCount").textContent=isolateRuns(T(lang,"mx_count").replace("{n}",shown.length).replace("{total}",R.length));
    $("mxEmpty").hidden=shown.length>0;
    check();
  }
  function msg(r,lang){
    var f=FE[r.feeder]||{};
    return T(lang,"mx_ask_msg")+"\n- "+T("en","mx_t_"+r.type)+(r.spec?" ("+r.spec+")":"")+"\n- "+T("en","mx_col_pack")+": "+T("en","mx_p_"+r.pack)+
      "\n- L x W x H (mm): "+body3(r)+(r.OH!=null?" / overall "+n1(r.OH):"")+"\n- Pitch (mm): "+(n1(r.pitch)||"?")+" / leads: "+(r.leads==null?"?":r.leads)+" / lead dia (mm): "+(n1(r.ld)||"?")+
      "\n- Suggested feeder: "+(f.model||T("en","mx_f_"+r.feeder+"n"))+(r.alt&&FE[r.alt]?" or "+FE[r.alt].model:"")+"\n- Ref: "+r.id;
  }
  function open(r){
    var lang=curLang(), f=FE[r.feeder]||{}, row=function(k,v){ return '<div class="mx-dr"><dt>'+esc(T(lang,k))+'</dt><dd>'+v+'</dd></div>'; };
    var wa=CFG.whatsapp+"?text="+encodeURIComponent(msg(r,lang));
    var ml="mailto:"+CFG.email+"?subject="+encodeURIComponent(T(lang,"mx_ask_subj")+" - "+T("en","mx_t_"+r.type))+"&body="+encodeURIComponent(msg(r,lang));
    det.innerHTML='<span class="kick">'+esc(T(lang,"mx_c_"+r.cat))+' · '+esc(T(lang,"mx_p_"+r.pack))+'</span><h3>'+esc(T(lang,"mx_t_"+r.type))+'</h3>'+
      (r.spec?'<p class="mx-spec" dir="ltr">'+esc(r.spec)+'</p>':'')+'<dl class="mx-dl">'+
      row("mx_d_body",'<span dir="ltr">'+esc(body3(r))+'</span>')+(r.OH!=null?row("mx_d_oh",'<span dir="ltr">'+esc(n1(r.OH))+'</span>'):"")+
      row("mx_col_pitch",'<span dir="ltr">'+esc(n1(r.pitch)||U())+'</span>')+row("mx_col_leads",'<span dir="ltr">'+esc(r.leads==null?U():r.leads)+'</span>')+row("mx_col_ld",'<span dir="ltr">'+esc(n1(r.ld)||U())+'</span>')+
      row("mx_d_feeder",'<b>'+esc(feederTxt(r,lang))+'</b><br>'+esc(T(lang,"mx_f_"+r.feeder+"d"))+(f.page?' <small>('+esc(T(lang,"mx_d_page"))+' '+f.page+')</small>':''))+
      row("mx_d_nozzle",esc(T(lang,"mx_n_"+(r.nozzle||"tbc"))))+row("mx_d_status",'<span class="mx-st mx-s-'+esc(r.status)+'">'+esc(T(lang,"mx_s_"+r.status))+'</span>')+
      (r.note?row("mx_d_note",esc(T(lang,"mx_note_"+r.note))):"")+row("mx_d_src",esc(T(lang,"mx_src_"+r.src)))+'</dl>'+
      '<div class="acts"><a class="btn btn-p" target="_blank" rel="noopener" id="mxWa" href="'+esc(wa)+'">'+esc(T(lang,"mx_ask_wa"))+'</a><a class="btn btn-o" id="mxMail" href="'+esc(ml)+'">'+esc(T(lang,"mx_ask_mail"))+'</a></div>';
    det.querySelectorAll("h3,dd,dt,p,span,b,a").forEach(function(e){ if(e.children.length===0) e.textContent=isolateRuns(e.textContent); });
    modal.classList.add("open"); var c=$("mxClose"); if(c) c.focus();
  }
  function close(){ modal.classList.remove("open"); }
  /* "Check your own part": compare the visitor's numbers with each feeder's published envelope. */
  function check(){
    var out=$("mxChkOut"); if(!out) return;
    var lang=curLang(), v=function(id){ var x=parseFloat(($(id)||{}).value); return isNaN(x)?null:x; };
    var pk=($("mxCPack")||{}).value, P={L:v("mxCL"),W:v("mxCW"),H:v("mxCH"),wt:v("mxCWt"),ld:v("mxCLd")};
    if(!pk && P.L==null && P.W==null && P.H==null && P.wt==null && P.ld==null){ out.innerHTML=""; return; }
    var hits=D.feeders.filter(function(f){
      if(!f.env) return false;
      if(pk && (f.pack||[]).indexOf(pk)<0) return false;
      var dims=[P.L,P.W,P.H].filter(function(x){ return x!=null; }).sort(function(a,b){ return b-a; });
      var env=["L","W","H"].map(function(k){ return f.env[k]; }).filter(Boolean);
      var emax=env.map(function(e){ return e[1]; }).sort(function(a,b){ return b-a; }), emin=env.map(function(e){ return e[0]; }).sort(function(a,b){ return b-a; });
      if(dims.length && !env.length) return false;
      for(var i=0;i<dims.length&&i<emax.length;i++){ if(dims[i]>emax[i]+1e-9) return false; }
      if(dims.length && emin.length && dims[dims.length-1]<Math.min.apply(null,emin)-1e-9) return false;
      if(P.wt!=null && f.env.wt && (P.wt<f.env.wt[0]||P.wt>f.env.wt[1])) return false;
      if(P.ld!=null && f.env.ld && (P.ld<f.env.ld[0]||P.ld>f.env.ld[1])) return false;
      return true;
    });
    out.innerHTML = hits.length ? '<p>'+esc(T(lang,"mx_chk_fit"))+'</p><ul>'+hits.map(function(f){ return '<li><b dir="ltr">'+esc(f.model||"")+'</b> '+esc(T(lang,"mx_f_"+f.id+"n"))+' <small>'+esc(T(lang,"mx_d_env"))+': '+esc(f.envtxt||"")+'</small></li>'; }).join("")+'</ul><p class="mx-cnote">'+esc(T(lang,"mx_chk_out"))+'</p>'
                               : '<p>'+esc(T(lang,"mx_chk_none"))+'</p>';
  }
  Object.keys(F).forEach(function(k){ if(F[k]) F[k].addEventListener(k==="q"?"input":"change",render); });
  ["mxCPack","mxCL","mxCW","mxCH","mxCWt","mxCLd"].forEach(function(id){ var e=$(id); if(e) e.addEventListener("input",check); if(e) e.addEventListener("change",check); });
  $("mxReset").addEventListener("click",function(){ Object.keys(F).forEach(function(k){ if(!F[k]) return; if(k==="unk") F[k].checked=true; else F[k].value=""; }); render(); });
  body.addEventListener("click",function(e){ var tr=e.target.closest("tr[data-id]"); if(!tr) return; var r=R.filter(function(x){ return x.id===tr.getAttribute("data-id"); })[0]; if(r) open(r); });
  body.addEventListener("keydown",function(e){ if(e.key!=="Enter"&&e.key!==" ") return; var tr=e.target.closest("tr[data-id]"); if(!tr) return; e.preventDefault(); tr.click(); });
  $("mxClose").addEventListener("click",close);
  modal.addEventListener("click",function(e){ if(e.target===modal) close(); });
  window.MX={render:render,close:close,rows:R.length};
}

/* ---------------------------------------------------------------- optional: NPI stepper with checklists */
function npiInit(){
  var box=document.getElementById("npiBox"); if(!box) return;
  var tabs=[].slice.call(box.querySelectorAll(".npi-tab")), panes=[].slice.call(box.querySelectorAll(".npi-pane"));
  function go(i){
    i=Math.max(0,Math.min(tabs.length-1,i));
    tabs.forEach(function(t,k){ var on=k===i; t.classList.toggle("on",on); t.setAttribute("aria-selected",on?"true":"false"); t.tabIndex=on?0:-1; panes[k].classList.toggle("on",on); panes[k].hidden=!on; });
  }
  function progress(){
    var cbs=box.querySelectorAll(".npi-cb"), d=[].filter.call(cbs,function(c){ return c.checked; }).length;
    var bar=document.getElementById("npiBar"); if(bar) bar.style.width=(cbs.length?Math.round(100*d/cbs.length):0)+"%";
    var p=document.getElementById("npiProg"); if(p) p.textContent=isolateRuns(T(curLang(),"npi_prog").replace("{d}",d).replace("{n}",cbs.length));
    tabs.forEach(function(t,k){ var c=panes[k].querySelectorAll(".npi-cb"); t.classList.toggle("done", c.length>0 && [].every.call(c,function(x){ return x.checked; })); });
  }
  tabs.forEach(function(t,i){
    t.addEventListener("click",function(){ go(i); });
    t.addEventListener("keydown",function(e){ var rtl=document.documentElement.dir==="rtl", k=e.key, n=null;
      if(k==="ArrowRight"||k==="ArrowDown") n=i+(rtl&&k==="ArrowRight"?-1:1); if(k==="ArrowLeft"||k==="ArrowUp") n=i+(rtl&&k==="ArrowLeft"?1:-1);
      if(n!=null){ e.preventDefault(); go((n+tabs.length)%tabs.length); tabs[(n+tabs.length)%tabs.length].focus(); } });
  });
  box.addEventListener("click",function(e){ var cur=tabs.findIndex(function(t){ return t.classList.contains("on"); });
    if(e.target.closest(".npi-next")) go(cur+1); if(e.target.closest(".npi-prev")) go(cur-1); });
  box.addEventListener("change",function(e){ if(e.target.classList.contains("npi-cb")) progress(); });
  window.NPI={go:go,progress:progress};
}
