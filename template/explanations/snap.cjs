(async()=>{
const { chromium } = require('playwright');
const fs=require('fs');
const times = process.argv.slice(2).map(Number);
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args:['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport:{width:540,height:960} });
const errs=[]; p.on('pageerror', e=>errs.push(e.message)); p.on('console', m=>{ if(m.type()==='error') errs.push(m.text())});
await p.goto('file://'+process.cwd()+'/index.html');
const ok = await p.evaluate(()=>window.ready);
console.log('fonts', ok, errs);
const OUT=process.env.OUT||'snaps';fs.mkdirSync(OUT,{recursive:true});
for (const t of times){
  const d = await p.evaluate(t=>{renderAt(t);return document.getElementById('c').toDataURL('image/jpeg',0.9)}, t);
  fs.writeFileSync(`${OUT}/t${t.toFixed(2)}.jpg`, Buffer.from(d.split(',')[1],'base64'));
}
console.log(errs);
await b.close();
})();
