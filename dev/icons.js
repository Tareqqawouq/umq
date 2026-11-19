// Renders icon.svg into the PNG icons the app needs. Run: node icons.js
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{
const svg=fs.readFileSync(path.join(__dirname,'icon.svg'),'utf8');
const out=path.join(__dirname,'..','icons');fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch();
// maskable: artwork scaled into the safe zone (80%) on full bleed background
const jobs=[['icon-192.png',192,1],['icon-512.png',512,1],['apple-touch-icon.png',180,1],['icon-maskable-512.png',512,0.8]];
for(const [n,s,k] of jobs){
  const p=await b.newPage({viewport:{width:s,height:s},deviceScaleFactor:1});
  const inner=Math.round(s*k),off=Math.round((s-inner)/2);
  await p.setContent('<html><body style="margin:0;background:#0c161c"><div style="position:absolute;left:'+off+'px;top:'+off+'px;width:'+inner+'px;height:'+inner+'px">'+svg.replace('<svg ','<svg width="'+inner+'" height="'+inner+'" ')+'</div></body></html>');
  await p.screenshot({path:path.join(out,n)});await p.close();
}
await b.close();console.log('icons written to',out);})();
