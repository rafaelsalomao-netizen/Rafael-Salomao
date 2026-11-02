# Gera os SVGs do logo "Camada 3D" com o texto convertido em caminhos (sem depender de fonte instalada)
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = sys.argv[1]; OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
f = TTFont(FONT); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
capH = f['OS/2'].sCapHeight or 700

def word(text, size, x=0, y=0, tracking=0.0):
    """Retorna (path d, largura) do texto com baseline em y, altura de caixa alta = size."""
    sc = size / capH
    d = []; pen_x = x
    for ch in text:
        g = cmap[ord(ch)]
        p = SVGPathPen(gs)
        tp = TransformPen(p, (sc, 0, 0, -sc, pen_x, y))
        gs[g].draw(tp)
        d.append(p.getCommands())
        pen_x += gs[g].width * sc + tracking * size
    return " ".join(d), pen_x - x - tracking * size

# ---- cores da marca
INK="#171A2B"; CORAL="#FF5A3C"; TEAL="#119DA4"; LEMON="#FFD166"; PAPER="#F7F7F4"

def shade(hexc, k):
    r,g,b = int(hexc[1:3],16), int(hexc[3:5],16), int(hexc[5:7],16)
    if k>=0: r,g,b = [int(c+(255-c)*k) for c in (r,g,b)]
    else:    r,g,b = [int(c*(1+k)) for c in (r,g,b)]
    return "#%02X%02X%02X" % (r,g,b)

def icon(x0, y0, s, colors=None, mono=None):
    """Três camadas empilhadas em vista isométrica. s = largura da camada de baixo.
    Retorna svg (grupo) ocupando aprox. s x 0.78s."""
    out=[]
    H = 0.19*s            # altura da face frontal de cada camada
    dx, dy = 0.14*s, 0.10*s  # deslocamento da face de cima (profundidade)
    widths = [1.0, 0.70, 0.40]
    cols = colors or [CORAL, TEAL, LEMON]
    base_y = y0 + 3*H + dy    # linha de baixo da camada inferior
    for i,w in enumerate(widths):
        W = w*s; xl = x0 + (s-W)/2 ; yb = base_y - i*H; yt = yb - H
        c = cols[i] if not mono else mono
        front = c if not mono else mono
        top   = shade(c, 0.35) if not mono else mono
        side  = shade(c,-0.30) if not mono else mono
        op_top  = "" if not mono else ' opacity="0.55"'
        op_side = "" if not mono else ' opacity="0.8"'
        # face frontal
        out.append(f'<rect x="{xl:.2f}" y="{yt:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{front}"/>')
        # face de cima (paralelogramo)
        out.append(f'<polygon points="{xl:.2f},{yt:.2f} {xl+dx:.2f},{yt-dy:.2f} {xl+W+dx:.2f},{yt-dy:.2f} {xl+W:.2f},{yt:.2f}" fill="{top}"{op_top}/>')
        # face lateral direita
        out.append(f'<polygon points="{xl+W:.2f},{yt:.2f} {xl+W+dx:.2f},{yt-dy:.2f} {xl+W+dx:.2f},{yb-dy:.2f} {xl+W:.2f},{yb:.2f}" fill="{side}"{op_side}/>')
    return "\n".join(out), s+dx, 3*H+dy

def wordmark(x, baseline, size, ink=INK, accent=CORAL):
    d1,w1 = word("CAMADA", size, x, baseline, tracking=0.02)
    gap = 0.22*size
    d2,w2 = word("3D", size*0.62, x+w1+gap, baseline, tracking=0.0)
    svg = f'<path d="{d1}" fill="{ink}"/>\n<path d="{d2}" fill="{accent}"/>'
    return svg, w1+gap+w2

def write(name, w, h, body, bg=None):
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>\n' if bg else ""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n<title>Camada 3D</title>\n{bgrect}{body}\n</svg>\n'
    open(os.path.join(OUT,name),"w").write(svg)

# 1) Ícone (quadrado 100x100), colorido e mono
ic, iw, ih = icon(0,0,80)
pad_x=(100-iw)/2; pad_y=(100-ih)/2
write("camada3d-icone.svg", 100, 100, f'<g transform="translate({pad_x:.2f},{pad_y:.2f})">{ic}</g>')
icm,_,_ = icon(0,0,80, mono=INK)
write("camada3d-icone-mono-preto.svg", 100, 100, f'<g transform="translate({pad_x:.2f},{pad_y:.2f})">{icm}</g>')
icw,_,_ = icon(0,0,80, mono="#FFFFFF")
write("camada3d-icone-mono-branco.svg", 100, 100, f'<g transform="translate({pad_x:.2f},{pad_y:.2f})">{icw}</g>')

# 2) Horizontal: ícone à esquerda, wordmark à direita
size=60; ic, iw, ih = icon(0,0,78)
wm, ww = wordmark(0, 0, size)
W = iw + 26 + ww + 8; H = 100
body = f'<g transform="translate(4,{(H-ih)/2:.2f})">{ic}</g>\n<g transform="translate({iw+30:.2f},{(H+size)/2:.2f})">{wm}</g>'
write("camada3d-logo-horizontal.svg", round(W), H, body)
# versões mono
icm,_,_ = icon(0,0,78, mono=INK); wmm,_ = wordmark(0,0,size, ink=INK, accent=INK)
write("camada3d-logo-horizontal-mono-preto.svg", round(W), H, f'<g transform="translate(4,{(H-ih)/2:.2f})">{icm}</g>\n<g transform="translate({iw+30:.2f},{(H+size)/2:.2f})">{wmm}</g>')
icw,_,_ = icon(0,0,78, mono="#FFFFFF"); wmw,_ = wordmark(0,0,size, ink="#FFFFFF", accent="#FFFFFF")
write("camada3d-logo-horizontal-mono-branco.svg", round(W), H, f'<g transform="translate(4,{(H-ih)/2:.2f})">{icw}</g>\n<g transform="translate({iw+30:.2f},{(H+size)/2:.2f})">{wmw}</g>')
# versão para fundo escuro (colorida, texto branco)
write("camada3d-logo-horizontal-fundo-escuro.svg", round(W), H, f'<g transform="translate(4,{(H-ih)/2:.2f})">{ic}</g>\n<g transform="translate({iw+30:.2f},{(H+size)/2:.2f})">{wordmark(0,0,size, ink="#FFFFFF", accent=LEMON)[0]}</g>')

# 3) Vertical: ícone em cima, wordmark embaixo, tagline opcional
size=44; ic, iw, ih = icon(0,0,120); wm, ww = wordmark(0,0,size)
W = max(iw, ww)+40; H = ih + 30 + size + 30
body = f'<g transform="translate({(W-iw)/2:.2f},14)">{ic}</g>\n<g transform="translate({(W-ww)/2:.2f},{14+ih+30+size:.2f})">{wm}</g>'
write("camada3d-logo-vertical.svg", round(W), round(H), body)

# 4) Com tagline
tl, tw = word("SEU NOME, CAMADA POR CAMADA", 11, 0, 0, tracking=0.12)
H2 = H + 26
body2 = body + f'\n<g transform="translate({(W-tw)/2:.2f},{H+14:.2f})"><path d="{tl}" fill="{TEAL}"/></g>'
write("camada3d-logo-vertical-tagline.svg", round(W), round(H2), body2)

print("ok", OUT); print("\n".join(sorted(os.listdir(OUT))))
