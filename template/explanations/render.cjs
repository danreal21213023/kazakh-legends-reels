const { chromium } = require('playwright'); const fs=require('fs');
const [start,end,dir]=[+process.argv[2],+process.argv[3],process.argv[4]];
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome'});const p=await b.newPage({viewport:{width:540,height:960}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/index.html');await p.evaluate(()=>window.ready);fs.mkdirSync(dir,{recursive:true});
for(let i=start;i<end;i++){const d=await p.evaluate(i=>{renderAt(i/30);return document.getElementById('c').toDataURL('image/jpeg',0.95)},i);
 fs.writeFileSync(`${dir}/f${String(i).padStart(5,'0')}.jpg`,Buffer.from(d.split(',')[1],'base64'));}
if(errs.length)console.log('ERR',errs);
if(process.argv[5]){const d=await p.evaluate(()=>{renderAt(2.4);return document.getElementById('c').toDataURL('image/png')});fs.writeFileSync('cover.png',Buffer.from(d.split(',')[1],'base64'));}
await b.close();console.log('done',start,end)})();
