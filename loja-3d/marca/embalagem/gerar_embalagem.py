#!/usr/bin/env python3
"""Gera o cartão de lembrancinha (60x90 mm) e o adesivo (40 mm) da Laço 3D, com folhas A4.

Uso:  python3 gerar_embalagem.py PASTA_DAS_FONTES [frase linha 1] [frase linha 2] [frase linha 3]
Ex.:  python3 gerar_embalagem.py ../../fontes "Professor(a), você transforma" "o hoje e inspira o amanhã."
Fontes: Fredoka-SemiBold.ttf, Nunito-Regular.ttf, Nunito-Bold.ttf (Google Fonts). Requer fonttools.
Para PNG das folhas A4 em 300 dpi: node ../render.js não serve; use o Inkscape ou abra o SVG no navegador e imprima.
"""
import re, pathlib, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont
AQUI = pathlib.Path(__file__).parent
FONTES = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI
FRASE = sys.argv[2:] or ["Obrigada por fazer parte", "deste momento."]
def loader(path, wght=None):
    f = TTFont(path)
    if 'fvar' in f and wght: f = instantiateVariableFont(f, {"wght": wght})
    return f, f.getGlyphSet(), f.getBestCmap(), (f['OS/2'].sCapHeight or 700)
fred = loader(FONTES/"Fredoka-SemiBold.ttf", 600); nun = loader(FONTES/"Nunito-Regular.ttf", 400); nunb = loader(FONTES/"Nunito-Bold.ttf", 700)
def word(font, text, size, tracking=0.0):
    f, gs, cmap, capH = font; sc = size/capH; d = []; px = 0
    for ch in text:
        g = cmap.get(ord(ch)) or cmap[ord('?')]; p = SVGPathPen(gs); gs[g].draw(TransformPen(p, (sc, 0, 0, -sc, px, 0))); d.append(p.getCommands()); px += gs[g].width*sc + tracking*size
    return " ".join(d), px
def centered(font, text, size, cx, y, fill, tracking=0.0, maxw=None):
    d, w = word(font, text, size, tracking)
    if maxw and w > maxw:  # encolhe até caber
        return centered(font, text, size*0.95, cx, y, fill, tracking, maxw)
    return f'<path transform="translate({cx-w/2:.2f},{y:.2f})" d="{d}" fill="{fill}"/>'
ic = (AQUI.parent/"logo"/"laco3d-icone.svg").read_text()
inner = re.search(r'<g transform="translate\([^"]*\)">(.*)</g>\s*</svg>', ic, re.S).group(1)
def icone(x, y, size, branco=False):
    g = inner
    if branco:
        for c in ("#D98C9A", "#FF9380", "#3E3237"): g = g.replace(c, "#FFFFFF")
        g = g.replace("#B9A6D9", "#FFE9EE")
    return f'<g transform="translate({x:.2f},{y:.2f}) scale({size/100:.4f})"><g transform="translate(5.46,8.56)">{g}</g></g>'
CACAU="#3E3237"; ROSE="#D98C9A"; ROSE_ESC="#B86F7E"; LILAS="#B9A6D9"; AREIA="#F6F1EA"
def cartao(linhas, x=0, y=0):
    g = [f'<g transform="translate({x},{y})">',
         f'<rect width="60" height="90" rx="4" fill="{AREIA}" stroke="{ROSE}" stroke-width="0.4"/>',
         f'<circle cx="30" cy="6" r="2" fill="none" stroke="{CACAU}" stroke-width="0.3" stroke-dasharray="0.8 0.6"/>',
         icone(21, 10, 18),
         centered(fred, "Um mimo", 7, 30, 37, CACAU), centered(fred, "para você", 7, 30, 46, ROSE_ESC),
         f'<line x1="18" y1="52" x2="42" y2="52" stroke="{LILAS}" stroke-width="0.4"/>']
    y0 = 60 if len(linhas) <= 2 else 58
    for i, l in enumerate(linhas): g.append(centered(nun, l, 3.0, 30, y0 + i*5.2, CACAU, maxw=52))
    g += [centered(nunb, "LAÇO 3D", 2.6, 30, 80, ROSE_ESC, 0.18), centered(nun, "feito com carinho, um de cada vez", 2.3, 30, 84.5, "#8A7A80"), '</g>']
    return "\n".join(g)
def adesivo(cx, cy):
    return (f'<g transform="translate({cx-20},{cy-20})"><circle cx="20" cy="20" r="20" fill="{ROSE}"/><circle cx="20" cy="20" r="18.6" fill="none" stroke="#fff" stroke-width="0.35" stroke-dasharray="1 0.8"/>'
            + icone(13, 6.5, 14, branco=True) + centered(fred, "um mimo", 3.6, 20, 25.5, "#FFFFFF") + centered(fred, "para você", 3.6, 20, 30.3, "#FFFFFF")
            + centered(nunb, "LAÇO 3D", 1.9, 20, 35.2, "#FFFFFF", 0.18) + '</g>')
def svg(w, h, body, titulo): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}mm" height="{h}mm">\n<title>{titulo}</title>\n{body}\n</svg>\n'
(AQUI/"cartao-lembrancinha.svg").write_text(svg(60, 90, cartao(FRASE), "Laço 3D — cartão de lembrancinha 60x90 mm"))
(AQUI/"cartao-lembrancinha-A4.svg").write_text(svg(210, 297, '<rect width="210" height="297" fill="#fff"/>' + "".join(cartao(FRASE, 25+i*70, 12+j*98) for j in range(3) for i in range(2)), "Folha A4 — 6 cartões"))
(AQUI/"adesivo-mimo.svg").write_text(svg(40, 40, adesivo(20, 20), "Laço 3D — adesivo 40 mm"))
(AQUI/"adesivo-mimo-A4.svg").write_text(svg(210, 297, '<rect width="210" height="297" fill="#fff"/>' + "".join(adesivo(25+i*42, 20+j*42) for j in range(6) for i in range(4)), "Folha A4 — 24 adesivos"))
print("embalagem gerada em", AQUI)
