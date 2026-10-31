// Renderiza a vitrine (vitrine.html) com o Chromium do Playwright, sem internet (three.js local).
// uso: node render2.js N [largura] [altura]  -> vframes/fNNN.png (N quadros girando 360°)
//      node render2.js fotos                 -> vframes/frente.png e vframes/angulo.png
const {chromium}=require('playwright'); const path=require('path'), fs=require('fs');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const p=await b.newPage({viewport:{width:+process.argv[3]||1080,height:+process.argv[4]||1350}});
 await p.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**',r=>{const rel=r.request().url().split('three@0.160.0/')[1];r.fulfill({path:path.join(__dirname,'three/package',rel),contentType:'application/javascript'})});
 p.on('pageerror',e=>console.log('err:',e.message));
 await p.goto('file://'+path.join(__dirname,'vitrine.html'));
 await p.waitForFunction('window.__ready',{timeout:120000});
 fs.rmSync('vframes',{recursive:true,force:true}); fs.mkdirSync('vframes');
 if(process.argv[2]==='fotos'){
  await p.evaluate(()=>window.__angulo(0,120)); await p.screenshot({path:'vframes/frente.png'});
  await p.evaluate(()=>window.__angulo(-0.55,190)); await p.screenshot({path:'vframes/angulo.png'});
 }else{
  const N=+process.argv[2]||1;
  for(let i=0;i<N;i++){await p.evaluate(a=>window.__frame(a),2*Math.PI*i/N);await p.screenshot({path:`vframes/f${String(i).padStart(3,'0')}.png`});}
 }
 await b.close();
})();
