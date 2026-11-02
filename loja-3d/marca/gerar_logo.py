# Gera os SVGs do logo "Laço 3D": laço em camadas + nome em curvas (não depende de fonte instalada)
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
FONT, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
f = TTFont(FONT)
if 'fvar' in f:
    from fontTools.varLib.instancer import instantiateVariableFont
    f = instantiateVariableFont(f, {"wght": 600})
gs = f.getGlyphSet(); cmap = f.getBestCmap(); capH = f['OS/2'].sCapHeight or 700

def word(text, size, x=0, y=0, tracking=0.0):
    sc = size/capH; d=[]; px=x
    for ch in text:
        g=cmap[ord(ch)]; p=SVGPathPen(gs); gs[g].draw(TransformPen(p,(sc,0,0,-sc,px,y))); d.append(p.getCommands()); px+=gs[g].width*sc+tracking*size
    return " ".join(d), px-x-tracking*size

CACAU="#3E3237"; ROSE="#D98C9A"; ROSE_ESC="#B86F7E"; LILAS="#B9A6D9"; SALVIA="#9DB8A4"; AREIA="#F6F1EA"

def laco(x0, y0, s, mono=None):
    """Laço de fita: duas laçadas em gota, nó, duas caudas com ponta em V, três listras (camadas). Ocupa s x 0.80s."""
    c_loop = mono or ROSE; c_knot = mono or CACAU; c_tail = mono or LILAS; c_line = "#FFFFFF" if not mono else AREIA
    op = ' opacity="0.9"' if mono else ''
    cx, cy = x0+s/2, y0+0.30*s
    def P(dx,dy): return f"{cx+dx*s:.2f} {cy+dy*s:.2f}"
    loop = lambda m: (f'M{P(0,0)} C{P(m*0.08,-0.34)} {P(m*0.56,-0.36)} {P(m*0.50,-0.06)} '
                      f'C{P(m*0.46,0.17)} {P(m*0.14,0.18)} {P(0,0)} Z')
    cid=f"cl{int(x0)}{int(s)}"
    out=[f'<defs><clipPath id="{cid}"><path d="{loop(-1)}"/><path d="{loop(1)}"/></clipPath></defs>']
    for m in (-1,1):   # caudas
        out.append(f'<path d="M{P(m*0.02,0.04)} L{P(m*0.26,0.46)} L{P(m*0.15,0.43)} L{P(m*0.12,0.50)} L{P(m*-0.01,0.10)} Z" fill="{c_tail}" stroke="{c_tail}" stroke-width="{0.03*s:.2f}" stroke-linejoin="round"/>')
    for m in (-1,1):   # laçadas
        out.append(f'<path d="{loop(m)}" fill="{c_loop}"/>')
    for k in (-1,0,1): # camadas
        yy = cy - 0.09*s + k*0.09*s
        out.append(f'<rect x="{x0:.2f}" y="{yy-0.011*s:.2f}" width="{s:.2f}" height="{0.022*s:.2f}" fill="{c_line}" opacity="0.5" clip-path="url(#{cid})"/>')
    out.append(f'<rect x="{cx-0.075*s:.2f}" y="{cy-0.085*s:.2f}" width="{0.15*s:.2f}" height="{0.17*s:.2f}" rx="{0.05*s:.2f}" fill="{c_knot}"{op}/>')
    return "\n".join(out), 1.12*s, 0.88*s

def wordmark(x, baseline, size, ink=CACAU, accent=LILAS):
    d1,w1 = word("Laço", size, x, baseline, tracking=0.01); gap=0.18*size
    d2,w2 = word("3D", size*0.58, x+w1+gap, baseline)
    return f'<path d="{d1}" fill="{ink}"/>\n<path d="{d2}" fill="{accent}"/>', w1+gap+w2

def write(name, w, h, body):
    open(os.path.join(OUT,name),"w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n<title>Laço 3D</title>\n{body}\n</svg>\n')

ic, iw, ih = laco(5,2,84); px=(100-iw)/2; py=(100-ih)/2
write("laco3d-icone.svg",100,100,f'<g transform="translate({px:.2f},{py:.2f})">{ic}</g>')
write("laco3d-icone-mono-escuro.svg",100,100,f'<g transform="translate({px:.2f},{py:.2f})">{laco(5,2,84,mono=CACAU)[0]}</g>')
write("laco3d-icone-mono-branco.svg",100,100,f'<g transform="translate({px:.2f},{py:.2f})">{laco(5,2,84,mono="#FFFFFF")[0]}</g>')

size=58; ic, iw, ih = laco(5,2,78); wm, ww = wordmark(0,0,size); W=iw+22+ww+8; H=100
def horiz(icon, mark): return f'<g transform="translate(4,{(H-ih)/2:.2f})">{icon}</g>\n<g transform="translate({iw+26:.2f},{(H+size)/2+2:.2f})">{mark}</g>'
write("laco3d-logo-horizontal.svg",round(W),H,horiz(ic,wm))
write("laco3d-logo-horizontal-fundo-escuro.svg",round(W),H,horiz(ic,wordmark(0,0,size,ink="#FFFFFF",accent=LILAS)[0]))
write("laco3d-logo-horizontal-mono-escuro.svg",round(W),H,horiz(laco(5,2,78,mono=CACAU)[0],wordmark(0,0,size,ink=CACAU,accent=CACAU)[0]))
write("laco3d-logo-horizontal-mono-branco.svg",round(W),H,horiz(laco(5,2,78,mono="#FFFFFF")[0],wordmark(0,0,size,ink="#FFFFFF",accent="#FFFFFF")[0]))

size=42; ic, iw, ih = laco(8,4,120); wm, ww = wordmark(0,0,size)
tl,tw = word("presentes e brindes impressos em 3D", 9.5, 0, 0, tracking=0.04); W=max(iw,ww,tw)+40; H=ih+24+size+26
body=f'<g transform="translate({(W-iw)/2:.2f},12)">{ic}</g>\n<g transform="translate({(W-ww)/2:.2f},{12+ih+24+size:.2f})">{wm}</g>'
write("laco3d-logo-vertical.svg",round(W),round(H),body)
write("laco3d-logo-vertical-tagline.svg",round(W),round(H+22),body+f'\n<g transform="translate({(W-tw)/2:.2f},{H+12:.2f})"><path d="{tl}" fill="{ROSE_ESC}"/></g>')
print("\n".join(sorted(os.listdir(OUT))))
