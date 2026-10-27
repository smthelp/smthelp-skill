// node smoke_test.js <page.html>   (needs jsdom: npm i jsdom)
const {JSDOM}=require('jsdom');const fs=require('fs');
const d=new JSDOM(fs.readFileSync(process.argv[2],'utf8'),{runScripts:'dangerously',url:'https://example.com/p.html',pretendToBeVisual:true});
setTimeout(()=>{const doc=d.window.document;let r=[],fail=0;
 const C=JSON.parse(doc.body.innerHTML.match(/var CFG=(\{.*?\});/)[1]);
 for(const l of C.langs.slice(1).concat(['en'])){const b=doc.querySelector(`[data-lang="${l}"]`);if(!b){fail++;continue}b.click();r.push(l+':'+doc.documentElement.dir)}
 const th=doc.getElementById('th');th&&th.click();
 console.log('langs',r.join(' '));console.log('theme',doc.documentElement.getAttribute('data-theme'));
 console.log('sections',doc.querySelectorAll('section').length,'videos',doc.querySelectorAll('.vcard').length,'docs',doc.querySelectorAll('[data-doc]').length,'blogs',doc.querySelectorAll('[data-blog]').length,'bars',doc.querySelectorAll('.bar').length);
 const b1=doc.querySelector('[data-blog]');if(b1){b1.click();console.log('blog modal',!doc.getElementById('modal').hidden)}
 if(!doc.querySelector('[data-lang="ar"]')||!r.includes('ar:rtl'))console.log('WARN rtl not verified');
 process.exit(fail?1:0)},800);
