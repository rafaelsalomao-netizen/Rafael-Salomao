"""Gera a árvore de Natal de nomes (estilo empilhado) para impressão 3D.

Cada andar = letras grossas ligadas por uma barra embaixo e outra em cima (vazado).
Imprime deitado (letra de frente para a mesa), sem suporte.
"""
import os, sys, zipfile
import numpy as np
import trimesh
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

FONT = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# (texto, cor) de baixo para cima; "FELIZ NATAL" é o pé
VERDE, VERMELHO = "verde", "vermelho"
ANDARES = [
    ("CAMILA", VERDE),
    ("THEO", VERMELHO),
    ("NINA", VERDE),
    ("MAX", VERMELHO),
    ("EDU", VERDE),
]
# ordem escolhida pela largura natural do nome (mais letras embaixo) para a árvore
# afinar como na foto sem esticar as letras
LARGURAS = [155.0, 107.0, 82.0, 63.0, 44.0]  # largura de cada andar, de baixo para cima (mm)
ALARGA_MAX = 1.2  # letras alargam no máximo 20% (a mais fica em espaço entre letras)
ALT_MAX = [49.0, 43.0, 35.5, 30.5, 26.5]  # altura de cada andar com as barras (mm)
PROF_TOTAL = 25.0                     # profundidade da peça em pé (= altura de impressão)
MOLDURA = 0.055                       # espessura da moldura (barras de cima e de baixo), fração da altura das letras
ENGROSSA = 0.0                      # engrossa o traço da fonte (fração da altura), como na foto
ESPACO = 0.06                        # vão entre letras (fração da altura) – é por onde se vê o outro lado

font = TTFont(FONT)
gs = font.getGlyphSet()
cmap = font.getBestCmap()
cap_h = getattr(font["OS/2"], "sCapHeight", 0) or font["head"].unitsPerEm * 0.7


def flatten(pen_value, steps=12):
    """RecordingPen -> lista de anéis (listas de pontos)."""
    rings, cur = [], []
    for op, pts in pen_value:
        if op == "moveTo":
            cur = [pts[0]]
        elif op == "lineTo":
            cur.append(pts[0])
        elif op == "qCurveTo":
            # TrueType: pontos off-curve implícitos
            start = cur[-1]
            ctrl = list(pts[:-1]); end = pts[-1]
            segs = []
            for i in range(len(ctrl)):
                c = ctrl[i]
                e = end if i == len(ctrl) - 1 else ((ctrl[i][0] + ctrl[i + 1][0]) / 2, (ctrl[i][1] + ctrl[i + 1][1]) / 2)
                segs.append((start, c, e)); start = e
            for p0, c, p1 in segs:
                for t in np.linspace(0, 1, steps)[1:]:
                    cur.append(((1-t)**2*p0[0] + 2*(1-t)*t*c[0] + t*t*p1[0],
                                (1-t)**2*p0[1] + 2*(1-t)*t*c[1] + t*t*p1[1]))
        elif op == "curveTo":
            p0 = cur[-1]; c1, c2, p1 = pts
            for t in np.linspace(0, 1, steps)[1:]:
                cur.append(tuple((1-t)**3*np.array(p0) + 3*(1-t)**2*t*np.array(c1)
                                 + 3*(1-t)*t*t*np.array(c2) + t**3*np.array(p1)))
        elif op in ("closePath", "endPath"):
            if len(cur) > 2:
                rings.append(cur)
            cur = []
    return rings


def glyph_shape(ch):
    g = gs[cmap[ord(ch)]]
    pen = RecordingPen(); g.draw(pen)
    rings = [Polygon(r).buffer(0) for r in flatten(pen.value)]
    shape = Polygon()
    # regra par-ímpar: XOR resolve furos (A, O, etc.)
    for r in sorted(rings, key=lambda p: -p.area):
        shape = shape.symmetric_difference(r)
    return shape, g.width


def engrossa(s, d):
    """Engrossa só o contorno de fora da letra; os furos de dentro (O, A, D, R...)
    continuam do tamanho original para aparecerem bem, como na foto."""
    polys = list(s.geoms) if s.geom_type == "MultiPolygon" else [s]
    fora = unary_union([Polygon(p.exterior) for p in polys]).buffer(d, join_style=2, mitre_limit=4)
    furos = unary_union([Polygon(i) for p in polys for i in p.interiors])
    # furos um pouco maiores que os da fonte (O, A bem visíveis como na foto)
    return fora.difference(furos.buffer(0.35 * d)) if not furos.is_empty else fora


def text_shape(txt, alarga=1.0, gap_extra=0.0):
    """alarga: fator horizontal das letras; gap_extra: espaço a mais entre letras (unid. da fonte)."""
    from shapely import affinity as _af
    parts, x = [], 0.0
    for ch in txt:
        if ch == " ":
            x += gs[cmap[ord(" ")]].width * alarga + gap_extra
            continue
        s, _ = glyph_shape(ch)
        s = engrossa(s, ENGROSSA * cap_h)
        s = _af.scale(s, alarga, 1.0, origin=(0, 0))
        b = s.bounds
        # posiciona pelo contorno real + espaçamento fixo (letras bem juntas, como na foto)
        s = shift(s, x - b[0], 0)
        parts.append(s)
        x += (b[2] - b[0]) + ESPACO * cap_h + gap_extra
    return unary_union(parts)


def shift(geom, dx, dy):
    from shapely import affinity
    return affinity.translate(geom, dx, dy)


def scale(geom, f):
    from shapely import affinity
    return affinity.scale(geom, f, f, origin=(0, 0))


RAIO = 0.9  # raio do arredondamento das quinas (mm)


def extrude(geom, h, z0=0.0, raio=RAIO, passos=6):
    """Extrusão com quinas frontais/traseiras arredondadas (via manifold3d)."""
    import manifold3d as mf
    from shapely.geometry.polygon import orient
    geoms = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    contornos = []
    for g in geoms:
        g = orient(g.buffer(0), 1.0)
        contornos.append(np.array(g.exterior.coords[:-1]))
        contornos += [np.array(i.coords[:-1]) for i in g.interiors]
    cs = mf.CrossSection(contornos, mf.FillRule.EvenOdd)
    solido = None
    for k in range(passos + 1):
        phi = (np.pi / 2) * k / passos
        d, e = raio * (1 - np.cos(phi)), raio * (1 - np.sin(phi))
        sec = cs.offset(-d, mf.JoinType.Round) if d > 1e-6 else cs
        fatia = mf.Manifold.extrude(sec, h - 2 * e).translate((0, 0, e))
        solido = fatia if solido is None else solido + fatia
    mesh = solido.to_mesh()
    m = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts))
    m.apply_translation([0, 0, z0])
    return m


PERFIS = {}


def contorno_pontas(letras, W, H, b, n=200):
    """Silhueta lateral da palavra, como na foto: o lado esquerdo segue o contorno da
    1ª letra e o direito o da última (B reto, O arredondado, A/Y inclinado); nas
    alturas das barras vale a largura da letra onde ela encosta na barra, então a
    barra termina junto com a letra, sem sobrar para fora."""
    from shapely.geometry import LineString, Polygon as P
    partes = list(letras.geoms) if letras.geom_type == "MultiPolygon" else [letras]
    primeira = min(partes, key=lambda g: g.bounds[0])
    ultima = max(partes, key=lambda g: g.bounds[2])

    def perfil(letra, lado):
        _, ly0, _, ly1 = letra.bounds
        lo, hi = max(b, ly0) + 0.05, min(H - b, ly1) - 0.05
        pts = []
        for k in range(n + 1):
            Y = H * k / n
            y = min(max(Y, lo), hi)
            corte = letra.intersection(LineString([(-1, y), (W + 1, y)]))
            if not corte.is_empty:
                pts.append((corte.bounds[0] if lado == "esq" else corte.bounds[2], Y))
        return pts

    return P(perfil(primeira, "esq") + perfil(ultima, "dir")[::-1]).buffer(0)


def build_piece(txt, larg_alvo, alt_max, laterais=False, barra_min=2.2, exato=False):
    """Bloco como na foto: barra em cima e embaixo (sem paredes laterais) com as
    letras grossas indo de uma barra à outra; o vazado fica só entre as letras.
    exato=True: o bloco fica com a largura larg_alvo exata (afinando como na foto)
    e a altura sai da palavra."""
    t = text_shape(txt)
    minx, miny, maxx, maxy = t.bounds
    t = shift(t, -minx, -miny)
    w0, h0 = maxx - minx, maxy - miny
    if exato:
        # largura E altura do andar fixas (proporções da foto). A diferença para a
        # largura natural do nome é dividida entre alargar as letras (até ALARGA_MAX)
        # e abrir um pouco o espaço entre elas.
        hl = alt_max / (1 + 2 * MOLDURA)
        if MOLDURA * hl < barra_min:
            hl = alt_max - 2 * barra_min
        f = hl / h0
        k = larg_alvo / (w0 * f)                 # quanto o nome precisa alargar
        alarga = min(max(k, 1.0), ALARGA_MAX)
        n_gaps = max(len(txt) - 1, 1)
        gap = max(0.0, (larg_alvo / f - w0 * alarga) / n_gaps)
        print(f"   {txt}: letras x{alarga:.2f}, espaço extra {gap * f:.1f} mm")
        t = text_shape(txt, alarga, gap)
        minx, miny, maxx, maxy = t.bounds
        t = shift(t, -minx, -miny)
        w0, h0 = maxx - minx, maxy - miny
        f = hl / h0
    else:
        f = min(larg_alvo / w0, alt_max / h0)
        for _ in range(6):  # ajusta a escala considerando a moldura
            hl = h0 * f
            b = max(barra_min, MOLDURA * hl)
            lat = b if laterais else 0.0
            W, H = w0 * f + 2 * lat, hl + 2 * b
            f *= min(larg_alvo / W, alt_max / H)
    hl, wl = h0 * f, w0 * f
    b = max(barra_min, MOLDURA * hl)
    lat = b if laterais else 0.0
    from shapely import affinity
    # letras entram 0,6 mm nas barras/laterais para fundirem numa peça só
    ov = 0.6
    letras = affinity.scale(scale(t, f).simplify(0.02), (wl + 2 * ov) / wl if laterais else 1.0,
                            (hl + 2 * ov) / hl, origin=(0, 0))
    letras = shift(letras, lat - (ov if laterais else 0.0), b - ov)
    W, H = wl + 2 * lat, hl + 2 * b
    externo = box(0, 0, W, H)
    if laterais:
        moldura = externo.difference(box(b, b, W - b, H - b))
    else:
        moldura = unary_union([box(0, 0, W, b), box(0, H - b, W, H)])
    perfil = unary_union([moldura, letras])
    if not laterais:
        # como na foto: o contorno da 1ª e da última letra fecha o bloco nas pontas
        # (B reto, O arredondado, A/Y inclinado) — as barras não sobram para fora
        perfil = perfil.intersection(contorno_pontas(letras, W, H, b))
    perfil = perfil.buffer(0.12, join_style=2).buffer(-0.12, join_style=2)  # limpa pontos encostados
    perfil = perfil.buffer(-0.4).buffer(0.4).buffer(0.4).buffer(-0.4).simplify(0.02)  # cantos arredondados
    if perfil.geom_type == "MultiPolygon":
        print("   pedaços:", [round(g.area, 2) for g in perfil.geoms])
        perfil = max(perfil.geoms, key=lambda g: g.area)
    print(f"  {txt}: {perfil.geom_type}, furos={len(perfil.interiors) if perfil.geom_type == 'Polygon' else '?'}, barra={b:.1f}mm")
    m = extrude(perfil, PROF_TOTAL)
    PERFIS[txt] = perfil.wkt
    return m, W, H


def write_3mf(path, items):
    """3MF simples: um objeto por peça, já posicionados na placa (256x256)."""
    objs, build = [], []
    for i, (name, m) in enumerate(items, 1):
        v = "".join(f'<vertex x="{a:.4f}" y="{b:.4f}" z="{c:.4f}"/>' for a, b, c in m.vertices)
        f = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in m.faces)
        objs.append(f'<object id="{i}" name="{name}" type="model"><mesh><vertices>{v}</vertices>'
                    f'<triangles>{f}</triangles></mesh></object>')
        build.append(f'<item objectid="{i}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<resources>{"".join(objs)}</resources><build>{"".join(build)}</build></model>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Target="/3D/3DModel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr("3D/3DModel.model", model)


# ---- monta as peças ----
n = len(ANDARES)
pecas = []  # (nome, cor, mesh, w, h)
for i, (txt, cor) in enumerate(ANDARES):
    alvo = LARGURAS[i]
    m, w, h = build_piece(txt, alvo, ALT_MAX[i], exato=True)
    pecas.append((txt, cor, m, w, h))
m, w, h = build_piece("FELIZ NATAL", 75.0, 16.0, laterais=False, barra_min=1.6)
pecas.insert(0, ("FELIZ NATAL", VERMELHO, m, w, h))

for txt, cor, m, w, h in pecas:
    print(f"{txt:12s} {cor:9s} {w:6.1f} x {h:5.1f} mm  estanque={m.is_watertight}")
    m.export(os.path.join(OUT, f"{txt.replace(' ', '_')}_{cor}.stl"))

# ---- placas de impressão por cor (sem AMS: imprime verde, troca o filamento, imprime vermelho) ----
for cor in (VERDE, VERMELHO):
    y, items = 10.0, []
    for txt, c, m, w, h in sorted([p for p in pecas if p[1] == cor], key=lambda p: -p[3]):
        mm = m.copy(); mm.apply_translation([128 - w / 2, y, 0])
        items.append((txt, mm)); y += h + 8
    assert y < 250, f"placa {cor} estourou: {y}"
    write_3mf(os.path.join(OUT, f"placa_{cor}.3mf"), items)

# ---- montagem completa (árvore em pé) para visualizar ----
cores_rgba = {VERDE: [0, 160, 80, 255], VERMELHO: [225, 30, 60, 255]}
z, cena = 0.0, []
for txt, cor, m, w, h in pecas:
    mm = m.copy()
    # em pé: Y da letra vira Z, extrusão vira -Y (letras para frente)
    R = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
    mm.apply_transform(R)
    mm.apply_translation([-w / 2, 0, z])
    mm.visual.face_colors = cores_rgba[cor]
    os.makedirs(os.path.join(OUT, "montagem"), exist_ok=True)
    mm.export(os.path.join(OUT, "montagem", f"{len(cena)}_{cor}.stl"))
    cena.append(mm); z += h
arvore = trimesh.util.concatenate(cena)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(8, 9), dpi=130); ax = fig.add_subplot(projection="3d")
luz = np.array([0.3, -0.8, 0.5]); luz /= np.linalg.norm(luz)
for mm in cena:
    base = mm.visual.face_colors[0, :3] / 255
    sh = np.clip(0.45 + 0.55 * np.abs(mm.face_normals @ luz), 0, 1)[:, None]
    ax.add_collection3d(Poly3DCollection(mm.triangles, facecolors=base * sh, linewidths=0))
b = arvore.bounds; c = b.mean(0); r = (b[1] - b[0]).max() / 2
ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(c[2]-r, c[2]+r)
ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=12, azim=-70); ax.axis("off")
plt.savefig(os.path.join(OUT, "preview_arvore.png"), bbox_inches="tight")
print("altura total:", round(z, 1), "mm")

import json; json.dump(PERFIS, open(os.path.join(OUT, "_perfis.json"), "w"))
