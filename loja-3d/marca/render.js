const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
const L=process.argv[2], F=process.argv[3], OUT=process.argv[4];
const svg=n=>fs.readFileSync(path.join(L,n),'utf8');
const font=f=>`url(data:font/ttf;base64,${fs.readFileSync(path.join(F,f)).toString('base64')})`;
const css=`@font-face{font-family:Fredoka;font-weight:600;src:${font('Fredoka-SemiBold.ttf')}}@font-face{font-family:Nunito;font-weight:400;src:${font('Nunito-Regular.ttf')}}@font-face{font-family:Nunito;font-weight:700;src:${font('Nunito-Bold.ttf')}}*{box-sizing:border-box;margin:0}body{font-family:Nunito}`;
const CACAU="#3E3237",ROSE="#D98C9A",LILAS="#B9A6D9",SALVIA="#9DB8A4",AREIA="#F6F1EA";
(async()=>{const b=await chromium.launch();const ctx=await b.newContext();
 const shot=async(html,w,h,file)=>{const p=await ctx.newPage();await p.setViewportSize({width:w,height:h});await p.setContent(`<style>${css}</style>${html}`);await p.screenshot({path:path.join(OUT,file),omitBackground:true});await p.close();};
 const W=s=>s.replace(/width="[\d.]+" height="[\d.]+"/,'');
 await shot(`<div style="background:#fff;padding:30px;width:1300px;display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center">
  <div style="padding:40px;background:${AREIA}">${W(svg('laco3d-logo-horizontal.svg')).replace('<svg','<svg width="560"')}</div>
  <div style="padding:40px;background:${CACAU}">${W(svg('laco3d-logo-horizontal-fundo-escuro.svg')).replace('<svg','<svg width="560"')}</div>
  <div style="padding:30px;background:${AREIA};display:flex;justify-content:center">${W(svg('laco3d-logo-vertical-tagline.svg')).replace('<svg','<svg width="340"')}</div>
  <div style="padding:30px;background:${AREIA};display:flex;gap:28px;align-items:center;justify-content:center">${W(svg('laco3d-icone.svg')).replace('<svg','<svg width="180"')}${W(svg('laco3d-icone-mono-escuro.svg')).replace('<svg','<svg width="110"')}<div style="width:64px;height:64px;border-radius:50%;background:${ROSE};display:flex;align-items:center;justify-content:center">${W(svg('laco3d-icone-mono-branco.svg')).replace('<svg','<svg width="46"')}</div><div style="width:32px;height:32px;border-radius:50%;background:${CACAU};display:flex;align-items:center;justify-content:center">${W(svg('laco3d-icone.svg')).replace('<svg','<svg width="24"')}</div></div></div>`,1360,760,'_prova.png');
 const perfil=(bg,ic)=>`<div style="width:1080px;height:1080px;background:${bg};display:flex;align-items:center;justify-content:center">${W(svg(ic)).replace('<svg','<svg width="700" height="700"')}</div>`;
 await shot(perfil(AREIA,'laco3d-icone.svg'),1080,1080,'perfil-instagram-areia.png');
 await shot(perfil(ROSE,'laco3d-icone-mono-branco.svg'),1080,1080,'perfil-instagram-rose.png');
 await shot(perfil(CACAU,'laco3d-icone.svg'),1080,1080,'perfil-instagram-escuro.png');
 await shot(`<div style="display:inline-block">${W(svg('laco3d-logo-horizontal.svg')).replace('<svg','<svg width="2400"')}</div>`,2400,620,'logo-horizontal-2400px.png');
 await shot(`<div style="display:inline-block">${W(svg('laco3d-logo-horizontal-fundo-escuro.svg')).replace('<svg','<svg width="2400"')}</div>`,2400,620,'logo-horizontal-fundo-escuro-2400px.png');
 const capas=[['Presentes',ROSE,'#fff'],['Para empresas',CACAU,'#fff'],['Como pedir',LILAS,CACAU],['Bastidores',SALVIA,CACAU],['Clientes',ROSE,'#fff'],['Datas',AREIA,CACAU]];
 for(const [t,c,fg] of capas){const ic=fg==='#fff'?'laco3d-icone-mono-branco.svg':'laco3d-icone-mono-escuro.svg';
  await shot(`<div style="width:1080px;height:1920px;background:${c};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:36px">${W(svg(ic)).replace('<svg','<svg width="320" height="320"')}<div style="font:600 92px/1 Fredoka;color:${fg};text-align:center;padding:0 60px">${t}</div></div>`,1080,1920,`capa-destaque-${t.toLowerCase().replace(/ /g,'-')}.png`);}
 await shot(`<div style="width:1200px;height:300px;background:${AREIA};display:flex;align-items:center;justify-content:space-between;padding:0 70px"><div>${W(svg('laco3d-logo-horizontal.svg')).replace('<svg','<svg width="520"')}</div><div style="color:${CACAU};font:700 30px/1.35 Nunito;text-align:right">Lembrancinhas e brindes impressos em 3D<br><span style="color:#B86F7E">personalizados para a sua data</span></div></div>`,1200,300,'banner-loja-1200x300.png');
 await b.close();console.log('renders ok');})();
