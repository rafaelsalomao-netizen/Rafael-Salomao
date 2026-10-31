"""Monta a comparação lado a lado, na mesma escala (mm), da foto de referência com as variantes renderizadas.
uso: python3 comparar.py foto.jpg saida.png pasta_render:base_mm:"Título":"subtítulo" ..."""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
def mask_colored(im):
    a = np.asarray(im.convert('RGB')).astype(int); r,g,b = a[...,0],a[...,1],a[...,2]
    return ((g>r+40)&(g>b+20)) | ((r>g+60)&(r>b+40))
def medidas(im):
    m = mask_colored(im); ys,xs = np.where(m)
    rows = [(np.where(m[y])[0].min(), np.where(m[y])[0].max()) for y in range(m.shape[0]) if m[y].any()]
    return max(x1-x0 for x0,x1 in rows), (xs.min(), ys.min(), xs.max(), ys.max())
foto_path, saida, *vars_ = sys.argv[1:]
foto = Image.open(foto_path).convert('RGB').crop((0,140,739,1360))
wf, bb = medidas(foto)
paineis_src = [(foto, 150/wf, bb, 'FOTO ORIGINAL', 'base 150 mm · nomes de 4 a 9 letras')]
for v in vars_:
    pasta, base, tit, sub = v.split(':')
    im = Image.open(pasta+'/frente.png').convert('RGB'); w, bb = medidas(im)
    paineis_src.append((im, float(base)/w, bb, tit, sub))
PXMM = 3.6; H = int(250*PXMM); pads = 40; paineis = []
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
for im, mmpx, (x0,y0,x1,y1), tit, sub in paineis_src:
    f = mmpx*PXMM
    crop = im.crop((max(0,x0-60), max(0,y0-60), min(im.width,x1+60), min(im.height,y1+60)))
    crop = crop.resize((int(crop.width*f), int(crop.height*f)), Image.LANCZOS)
    pan = Image.new('RGB', (int(185*PXMM), H+140), 'white')
    base_y = H - 20; ty = base_y - (crop.height - int(60*f))
    pan.paste(crop, ((pan.width-crop.width)//2, ty))
    d = ImageDraw.Draw(pan)
    d.text((pan.width//2, H+20), tit, fill='black', font=font, anchor='mt')
    d.text((pan.width//2, H+62), sub, fill='#444', font=fs, anchor='mt')
    d.text((pan.width//2, H+96), f"altura {(y1-y0)*mmpx:.0f} mm · largura {(x1-x0)*mmpx:.0f} mm", fill='#444', font=fs, anchor='mt')
    paineis.append(pan)
W = sum(p.width for p in paineis)+pads*(len(paineis)+1)
out = Image.new('RGB',(W, H+140+pads),'white'); x=pads
for p in paineis: out.paste(p,(x,pads//2)); x+=p.width+pads
d = ImageDraw.Draw(out); d.line([(pads, H-20+pads//2),(W-pads, H-20+pads//2)], fill='#bbb', width=2)
d.text((W//2, 6), "Mesma escala — bases alinhadas", fill='#888', font=fs, anchor='mt')
out.save(saida); print(saida, out.size)
