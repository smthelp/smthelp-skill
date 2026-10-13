/* Runtime for the FUJI NXT Feeder Calibration Jig landing page:
   language switch (7 languages, RTL for Arabic), light/dark theme, both
   persisted in localStorage and restored on reload; video modal, lightbox,
   catalogue viewer, payback estimate and mail-client enquiry form. */
const I18N = __I18N__;
const LANGS = [
  {code:"en",label:"English",short:"EN"},
  {code:"es",label:"Español",short:"ES"},
  {code:"pt",label:"Português",short:"PT"},
  {code:"fr",label:"Français",short:"FR"},
  {code:"ar",label:"العربية",short:"AR"},
  {code:"ru",label:"Русский",short:"RU"},
  {code:"zh",label:"中文",short:"ZH"}
];
const VIDEOS = __VIDEOS__;
const LANG_KEY = "__STORE__lang", THEME_KEY = "__STORE__theme";

/* Wrap left-to-right runs (model codes, units, e-mail) in bidi isolates when the
   string contains right-to-left text, so "220 V AC" never renders reversed. */
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
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
function fmt(n,lang){
  try{ return new Intl.NumberFormat(lang==="zh"?"zh-CN":lang,{maximumFractionDigits:1}).format(n); }
  catch(e){ return String(Math.round(n*10)/10); }
}
function renderVideos(lang){
  var g=document.getElementById("vidGrid"); if(!g) return;
  g.innerHTML=VIDEOS.map(function(v){
    return '<article class="vid" data-vid="'+v.id+'" tabindex="0" role="button">'
      +'<div class="th"><img loading="lazy" decoding="async" src="https://i.ytimg.com/vi/'+v.id+'/hqdefault.jpg" alt="'+esc(T(lang,v.t))+'">'
      +'<div class="pl"><i></i></div></div>'
      +'<div class="bd"><span class="dur">'+v.dur+'</span><h3>'+esc(isolateRuns(T(lang,v.t)))+'</h3><p>'+esc(isolateRuns(T(lang,v.d)))+'</p></div></article>';
  }).join("");
}

/* Payback estimate: every money figure comes from the visitor. */
function num(id){ var e=document.getElementById(id); var v=parseFloat(e&&e.value); return isNaN(v)||v<0?0:v; }
function calc(){
  var lang=document.documentElement.lang||"en";
  var feeders=num("cFeeders"), share=Math.min(num("cShare"),100)/100, mins=num("cMin"),
      rate=num("cRate"), tech=num("cTech"), techRate=num("cTechRate"), price=num("cPrice");
  var set=function(id,txt){ var e=document.getElementById(id); if(e) e.textContent=txt; };
  var hours=feeders*share*mins/60;           /* line hours protected per month */
  var value=hours*rate;                      /* value of that line time        */
  var cost=feeders*tech/60*techRate;         /* technician time on the jig     */
  var net=value-cost;
  set("rHours", hours>0 ? fmt(hours,lang) : "—");
  set("rValue", value>0 ? fmt(value,lang) : "—");
  set("rCost",  cost>0 ? fmt(cost,lang) : "—");
  set("rNet",   (value>0||cost>0) ? fmt(net,lang) : "—");
  var pb=document.getElementById("rPayback"), pbu=document.getElementById("rPaybackU");
  if(!pb) return;
  if(price<=0){ pb.textContent="—"; pbu.textContent=T(lang,"calc_needprice"); return; }
  if(net<=0){ pb.textContent="—"; pbu.textContent=T(lang,"calc_needinput"); return; }
  var m=price/net;
  if(m<1){ pb.textContent="<1"; pbu.textContent=T(lang,"unit_month"); }
  else if(m<24){ pb.textContent=m.toFixed(1); pbu.textContent=T(lang,"unit_month"); }
  else { pb.textContent=(m/12).toFixed(1); pbu.textContent=T(lang,"unit_year"); }
}

function applyLang(lang,persist){
  if(!I18N[lang]) lang="en";
  var meta=I18N[lang].__meta||{dir:"ltr",short:"EN"};
  var root=document.documentElement;
  root.setAttribute("lang",lang);
  root.setAttribute("dir",meta.dir||"ltr");
  document.querySelectorAll("[data-i18n]").forEach(function(el){ el.textContent=isolateRuns(T(lang,el.getAttribute("data-i18n"))); });
  document.querySelectorAll("[data-i18n-alt]").forEach(function(el){ el.setAttribute("alt",isolateRuns(T(lang,el.getAttribute("data-i18n-alt")))); });
  document.querySelectorAll("[data-i18n-aria]").forEach(function(el){ el.setAttribute("aria-label",isolateRuns(T(lang,el.getAttribute("data-i18n-aria")))); });
  document.querySelectorAll("[data-i18n-title]").forEach(function(el){ el.setAttribute("title",isolateRuns(T(lang,el.getAttribute("data-i18n-title")))); });
  document.title=T(lang,"seo_title");
  [['meta[name="description"]',"seo_desc"],['meta[name="keywords"]',"seo_keys"],['meta[property="og:title"]',"og_title"],
   ['meta[property="og:description"]',"og_desc"],['meta[name="twitter:title"]',"og_title"],['meta[name="twitter:description"]',"og_desc"]
  ].forEach(function(p){ var m=document.querySelector(p[0]); if(m) m.setAttribute("content",T(lang,p[1])); });
  var li=document.getElementById("langIcon"); if(li) li.textContent=meta.short;
  document.querySelectorAll("#langMenu button").forEach(function(b){ b.setAttribute("aria-current", b.getAttribute("data-lang")===lang?"true":"false"); });
  renderVideos(lang);
  calc();
  if(persist!==false){ try{ localStorage.setItem(LANG_KEY,lang); }catch(e){} }
}
function applyTheme(mode,persist){
  if(mode!=="dark") mode="light";
  document.documentElement.setAttribute("data-theme",mode);
  var ic=document.getElementById("themeIcon"); if(ic) ic.textContent= mode==="dark" ? "☾" : "☀";
  var mt=document.querySelector('meta[name="theme-color"]'); if(mt) mt.setAttribute("content", mode==="dark" ? "#0b1514" : "#0c665c");
  if(persist!==false){ try{ localStorage.setItem(THEME_KEY,mode); }catch(e){} }
}

(function boot(){
  var params=new URLSearchParams(location.search), savedLang="en", savedTheme=null;
  try{
    savedLang=params.get("lang")||localStorage.getItem(LANG_KEY)||"en";
    savedTheme=localStorage.getItem(THEME_KEY);
  }catch(e){}
  if(!I18N[savedLang]) savedLang="en";
  if(!savedTheme) savedTheme=(window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches)?"dark":"light";
  applyTheme(savedTheme,false);

  var lm=document.getElementById("langMenu");
  lm.innerHTML=LANGS.map(function(l){ return '<button type="button" role="menuitem" data-lang="'+l.code+'"><span>'+l.label+'</span><span class="code">'+l.short+'</span></button>'; }).join("");
  document.getElementById("themeBtn").addEventListener("click",function(){
    applyTheme(document.documentElement.getAttribute("data-theme")==="dark"?"light":"dark",true);
  });
  var lw=document.getElementById("langWrap"), lb=document.getElementById("langBtn");
  lb.addEventListener("click",function(e){ e.stopPropagation(); var o=lw.classList.toggle("open"); lb.setAttribute("aria-expanded",o?"true":"false"); });
  lm.addEventListener("click",function(e){
    var b=e.target.closest("button[data-lang]"); if(!b) return;
    applyLang(b.getAttribute("data-lang"),true);
    lw.classList.remove("open"); lb.setAttribute("aria-expanded","false");
  });
  document.addEventListener("click",function(){ lw.classList.remove("open"); lb.setAttribute("aria-expanded","false"); });
  document.addEventListener("keydown",function(e){ if(e.key==="Escape"){ lw.classList.remove("open"); closeVideo(); closeLb(); } });

  var bg=document.getElementById("burger"), hdr=document.getElementById("hdr");
  bg.addEventListener("click",function(){ hdr.classList.toggle("navopen"); });
  document.getElementById("nav").addEventListener("click",function(e){ if(e.target.tagName==="A") hdr.classList.remove("navopen"); });

  /* video modal - never set src="" (it would load this page inside the frame) */
  var modal=document.getElementById("vModal"), frame=document.getElementById("vFrame");
  window.closeVideo=function(){ modal.classList.remove("open"); frame.removeAttribute("src"); };
  document.getElementById("vClose").addEventListener("click",closeVideo);
  modal.addEventListener("click",function(e){ if(e.target===modal) closeVideo(); });
  function openVideo(c){ frame.src="https://www.youtube-nocookie.com/embed/"+c.getAttribute("data-vid")+"?rel=0&autoplay=1"; modal.classList.add("open"); }
  var vg=document.getElementById("vidGrid");
  vg.addEventListener("click",function(e){ var c=e.target.closest(".vid"); if(c) openVideo(c); });
  vg.addEventListener("keydown",function(e){ if(e.key!=="Enter"&&e.key!==" ") return; var c=e.target.closest(".vid"); if(!c) return; e.preventDefault(); openVideo(c); });

  /* lightbox */
  var lbx=document.getElementById("lb"), lbimg=lbx.querySelector("img");
  window.closeLb=function(){ lbx.classList.remove("open"); lbimg.removeAttribute("src"); };
  lbx.addEventListener("click",function(e){ if(e.target!==lbimg) closeLb(); });
  document.querySelectorAll(".galgrid figure").forEach(function(f){
    f.addEventListener("click",function(){
      var full=f.getAttribute("data-full"); if(!full) return;
      var th=f.querySelector("img"); if(th) lbimg.setAttribute("alt",th.getAttribute("alt")||"");
      lbimg.onerror=function(){ lbimg.onerror=null; lbimg.src=th.getAttribute("src"); };
      lbimg.src=full; lbx.classList.add("open");
    });
  });

  /* catalogue viewer: loads the first document only when the section is near */
  var cf=document.getElementById("catFrame");
  function loadCat(src){ cf.src=src; }
  if(typeof window.IntersectionObserver==="function"){
    var io=new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ if(!cf.getAttribute("src")) loadCat(cf.getAttribute("data-src")); io.disconnect(); } }); },{rootMargin:"300px"});
    io.observe(cf);
  } else loadCat(cf.getAttribute("data-src"));
  document.getElementById("catGrid").addEventListener("click",function(e){
    var b=e.target.closest("button.pv"); if(!b) return;
    document.querySelectorAll("#catGrid button.pv").forEach(function(x){ x.classList.remove("on"); });
    b.classList.add("on"); loadCat(b.getAttribute("data-src"));
    cf.scrollIntoView({behavior:"smooth",block:"center"});
  });

  ["cFeeders","cShare","cMin","cRate","cTech","cTechRate","cPrice"].forEach(function(id){ var e=document.getElementById(id); if(e) e.addEventListener("input",calc); });

  document.getElementById("qform").addEventListener("submit",function(e){
    e.preventDefault();
    var lang=document.documentElement.lang||"en";
    var g=function(id){ var el=document.getElementById(id); return el?el.value.trim():""; };
    var body=[T(lang,"form_name")+": "+g("fN"), T(lang,"form_company")+": "+g("fC"), T(lang,"form_email")+": "+g("fE"),
              T(lang,"form_scope")+": "+g("fS"), "", g("fT")].join("\r\n");
    location.href="mailto:info@smthelp.com?subject="+encodeURIComponent(T(lang,"form_subject"))+"&body="+encodeURIComponent(body);
  });

  /* logo fallback: never show a broken brand mark */
  document.querySelectorAll(".brand img, img.fl").forEach(function(im){
    im.addEventListener("error",function(){ if(im.getAttribute("data-fb")!=="1"){ im.setAttribute("data-fb","1"); im.replaceWith(Object.assign(document.createElement("b"),{textContent:"SOUTHERN MACHINERY",style:"color:var(--brand);font-size:15px;letter-spacing:.04em"})); } });
  });

  applyLang(savedLang,false);
})();
