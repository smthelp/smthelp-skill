(function(){
var P=CFG.prefix,LK=P+"lang",TK=P+"theme",root=document.documentElement,cur="en";
function q(s){return document.querySelectorAll(s)}
function iso(t){return t.replace(/([A-Za-z0-9#][A-Za-z0-9#.,\-×~%± \/]*[A-Za-z0-9%])/g,"\u2068$1\u2069")}
function setLang(l,persist){
  if(CFG.langs.indexOf(l)<0)l="en";cur=l;var d=I18N[l]||{},en=I18N.en;
  q("[data-k]").forEach(function(el){var k=el.getAttribute("data-k"),v=d[k]!=null?d[k]:en[k];if(v==null)return;el.textContent=(l==="ar")?iso(v):v;});
  q("[data-kt]").forEach(function(el){var k=el.getAttribute("data-kt");el.title=d[k]||en[k]||el.title});
  root.lang=l==="zh"?"zh-CN":l;root.dir=l==="ar"?"rtl":"ltr";
  document.title=(d.seo_title||en.seo_title);var md=document.querySelector('meta[name=description]');if(md)md.content=d.seo_desc||en.seo_desc;
  document.getElementById("langCur").textContent=l.toUpperCase();
  q("#langMenu button").forEach(function(b){b.setAttribute("aria-current",b.getAttribute("data-lang")===l?"true":"false")});
  if(persist!==false){try{localStorage.setItem(LK,l)}catch(e){}}
}
function setTheme(m,persist){m=m==="dark"?"dark":"light";root.setAttribute("data-theme",m);document.getElementById("themeIcon").textContent=m==="dark"?"☾":"☀";
  var mt=document.querySelector('meta[name="theme-color"]');if(mt)mt.content=m==="dark"?"#00202d":"#003142";
  if(persist!==false){try{localStorage.setItem(TK,m)}catch(e){}}}
var st={};try{st.l=localStorage.getItem(LK);st.t=localStorage.getItem(TK)}catch(e){}
var ql=(location.search.match(/[?&]lang=([a-z]{2})/)||[])[1];
setTheme(st.t||"light",false);setLang(ql||st.l||"en",!!ql);
document.getElementById("th").onclick=function(){setTheme(root.getAttribute("data-theme")==="dark"?"light":"dark")};
var lb=document.getElementById("langBtn"),lm=document.getElementById("langMenu");
lb.onclick=function(e){e.stopPropagation();lm.hidden=!lm.hidden};
q("#langMenu button").forEach(function(b){b.onclick=function(){setLang(b.getAttribute("data-lang"));lm.hidden=true}});
document.addEventListener("click",function(){lm.hidden=true});
var modal=document.getElementById("modal"),mb=document.getElementById("mbody");
function open(h){mb.innerHTML="";if(typeof h==="string")mb.innerHTML=h;else mb.appendChild(h);modal.hidden=false}
function close(){modal.hidden=true;mb.innerHTML=""}
document.getElementById("mclose").onclick=close;modal.onclick=function(e){if(e.target===modal)close()};
document.addEventListener("keydown",function(e){if(e.key==="Escape")close()});
q("[data-yt]").forEach(function(b){b.onclick=function(){open('<div class="vwrap"><iframe src="https://www.youtube-nocookie.com/embed/'+b.getAttribute("data-yt")+'?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="video"></iframe></div>')}});
q("[data-blog]").forEach(function(b){b.onclick=function(){var a=document.getElementById("blog"+b.getAttribute("data-blog")).cloneNode(true);a.hidden=false;a.removeAttribute("id");open(a)}});
var dv=document.getElementById("docview"),df=document.getElementById("docframe");
q("[data-doc]").forEach(function(b){b.onclick=function(){df.src=b.getAttribute("data-doc");dv.hidden=false;dv.scrollIntoView({behavior:"smooth"})}});
document.getElementById("docclose").onclick=function(){dv.hidden=true;df.removeAttribute("src")};
window.SMReport={setLang:setLang,setTheme:setTheme};
})();
