"""
Gol G4 (VW, 2006-2014) 2 portas, rebaixado, com rodas estilo BBS RS aro 17.
Kit multipartes para impressora sem AMS (uma cor por peca).

Uso:  python3 gerar_gol_g4.py            -> gera STLs em ./stl e 3MFs por cor em ./3mf
      python3 gerar_gol_g4.py --escala 24  -> escala 1:24 (padrao 1:18)
      python3 gerar_gol_g4.py --roda cup   -> rodas estilo Porsche Cup (padrao bbs)

Coordenadas do carro (mm reais): x = frente->traseira, y = esquerda(+)/direita(-), z = altura.
Tudo e convertido para a escala do modelo por S. Folgas/espessuras estao em mm do modelo.
"""
import argparse
import os

import manifold3d as m3d
import numpy as np
import trimesh
from shapely.geometry import LineString, Polygon

ap = argparse.ArgumentParser()
ap.add_argument("--escala", type=float, default=18.0)
ap.add_argument("--roda", choices=["bbs", "cup"], default="bbs")
ap.add_argument("--rapido", action="store_true", help="malha mais grossa, para teste")
args = ap.parse_args()

S = 1.0 / args.escala
OUT = os.path.dirname(os.path.abspath(__file__))
m3d.set_circular_segments(24 if args.rapido else 64)

# ---------------------------------------------------------------- parametros (mm do modelo)
PAREDE = 1.8          # espessura da carroceria
ABA = 1.6             # aba interna no fundo da carroceria (apoio/colagem do chassi)
FOLGA = 0.15          # folga de encaixe
PROF_BOLSO = 0.8      # profundidade dos encaixes de farol/lanterna/grade/placa
FRISO_L, FRISO_P = 0.35, 0.45  # largura/profundidade das linhas de porta/capo
VIDRO = 0.8           # espessura dos vidros
EIXO_D = 3.0          # vareta de aco 3 mm (ou eixo impresso)

# ---------------------------------------------------------------- dimensoes reais (mm)
L = 3916.0
EIXO_DIANT, EIXO_TRAS = 740.0, 740.0 + 2468.0
ARCO_Z, ARCO_R = 360.0, 350.0           # centro/raio do recorte do para-lama
PNEU_D = 17 * 25.4 + 2 * 0.45 * 195     # 195/45 R17
PNEU_L = 195.0
RODA_D = 17 * 25.4
FOLGA_PNEU_TOPO = 10.0                   # quase encostando: rebaixado
ROD_Z = ARCO_Z + ARCO_R - FOLGA_PNEU_TOPO - PNEU_D / 2   # centro da roda
CHAO_Z = ROD_Z - PNEU_D / 2
ROD_Y = 828.0 - 5.0 - PNEU_L / 2         # pneu alinhado com a lataria


def P(*xy):
    return np.array(xy, dtype=float) * S


# ---------------------------------------------------------------- utilidades de geometria
def fillet_poly(pts, closed=True, seg=6):
    """pts: lista (x, y, raio). Arredonda cada vertice com o raio dado."""
    pts = [(float(a), float(b), float(r)) for a, b, r in pts]
    n = len(pts)
    out = []
    rng = range(n) if closed else range(n)
    for i in rng:
        x, y, r = pts[i]
        if r <= 0 or (not closed and (i == 0 or i == n - 1)):
            out.append((x, y))
            continue
        A = np.array(pts[i - 1][:2]); B = np.array((x, y)); C = np.array(pts[(i + 1) % n][:2])
        u1 = A - B; l1 = np.linalg.norm(u1); u2 = C - B; l2 = np.linalg.norm(u2)
        if l1 < 1e-9 or l2 < 1e-9:
            out.append((x, y)); continue
        u1 /= l1; u2 /= l2
        cos = np.clip(np.dot(u1, u2), -1, 1)
        th = np.arccos(cos)
        if th > np.pi - 1e-3 or th < 1e-3:
            out.append((x, y)); continue
        t = r / np.tan(th / 2)
        tmax = 0.45 * min(l1, l2)
        if t > tmax:
            t = tmax; r = t * np.tan(th / 2)
        T1 = B + u1 * t; T2 = B + u2 * t
        bis = (u1 + u2); bis /= np.linalg.norm(bis)
        Cc = B + bis * (r / np.sin(th / 2))
        a1 = np.arctan2(*(T1 - Cc)[::-1]); a2 = np.arctan2(*(T2 - Cc)[::-1])
        da = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
        for k in range(seg + 1):
            a = a1 + da * k / seg
            out.append(tuple(Cc + r * np.array([np.cos(a), np.sin(a)])))
    return np.array(out)


def resample(poly, n, peso_curva=0.0):
    """Reamostra a polilinha com n pontos; peso_curva concentra pontos nas curvas."""
    poly = np.asarray(poly)
    seg = np.diff(poly, axis=0)
    ln = np.linalg.norm(seg, axis=1)
    if peso_curva:
        ang = np.arctan2(seg[:, 1], seg[:, 0])
        turn = np.abs((np.diff(ang) + np.pi) % (2 * np.pi) - np.pi)
        ln = ln + peso_curva * np.r_[turn, 0] / 2 + peso_curva * np.r_[0, turn] / 2
    d = np.r_[0, np.cumsum(ln)]
    t = np.linspace(0, d[-1], n)
    return np.c_[np.interp(t, d, poly[:, 0]), np.interp(t, d, poly[:, 1])]


def to_manifold(verts, faces):
    tm = trimesh.Trimesh(verts, faces, process=True)
    tm.merge_vertices()
    trimesh.repair.fix_normals(tm)
    mesh = m3d.Mesh(vert_properties=np.asarray(tm.vertices, np.float32),
                    tri_verts=np.asarray(tm.faces, np.uint32))
    m = m3d.Manifold(mesh)
    assert m.status().name == "NoError", m.status()
    return m


def to_trimesh(m):
    # descarta lascas sem volume que sobram das operacoes booleanas
    pass
    partes = [p for p in m.decompose() if p.volume() > 0.5]
    m = m3d.Manifold.batch_boolean(partes, m3d.OpType.Add) if len(partes) > 1 else partes[0]
    mesh = m.to_mesh()
    return trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts), process=False)


def cs(poly):
    poly = np.asarray(poly, float)
    if Polygon(poly).exterior.is_ccw is False:
        poly = poly[::-1]
    return m3d.CrossSection([poly])


def prism_xz(poly_xz, y0, y1):
    """Extruda um poligono do plano XZ ao longo de Y (de y0 a y1)."""
    m = cs(poly_xz).extrude(y1 - y0)            # x, y(=z do carro), z(=extrusao)
    # (x, y, z) -> (x, z, y)
    M = np.array([[1, 0, 0, 0], [0, 0, 1, y0], [0, 1, 0, 0]], float)
    return m.transform(M)


def prism_xy(poly_xy, z0, z1):
    return cs(poly_xy).extrude(z1 - z0).translate([0, 0, z0])


def prism_yz(poly_yz, x0, x1):
    m = cs(poly_yz).extrude(x1 - x0)
    M = np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], float)
    return m.transform(M)


def box(x0, x1, y0, y1, z0, z1):
    return m3d.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def both_sides(m):
    return m + m.mirror([0, 1, 0])


def rounded_box(c, size, r):
    """Caixa arredondada (hull de esferas). c = centro, size = dimensoes."""
    c = np.asarray(c, float); h = np.asarray(size, float) / 2 - r
    s = m3d.Manifold.sphere(r, 16)
    pts = [s.translate(list(c + h * np.array([i, j, k]))) for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)]
    return m3d.Manifold.batch_hull(pts)


# ---------------------------------------------------------------- perfis do Gol G4
# Perfil lateral (x, z, raio) em mm reais
PERFIL = [
    (25, 240, 60), (0, 330, 60), (0, 520, 40), (40, 600, 60), (150, 715, 140),
    (600, 790, 500), (1085, 860, 30),            # capo ate a base do para-brisa
    (1690, 1392, 160), (2300, 1418, 900), (3200, 1405, 300),   # teto
    (3440, 1378, 25), (3480, 1350, 15),          # aerofolio de teto
    (3765, 1000, 50), (3880, 905, 70), (3916, 760, 60), (3916, 520, 40),
    (3900, 330, 60), (3860, 240, 60), (3600, 200, 120), (300, 200, 120),
]
# Meia-largura na vista de cima (x, y, raio)
PLANTA = [(0, 600, 120), (100, 775, 200), (700, 828, 400), (3400, 828, 400),
          (3800, 812, 150), (3916, 720, 80)]
CINTURA = np.array([(1085, 865), (1700, 925), (3000, 958), (3765, 1000)], float)
TETO_MEIA_LARG = 610.0
Z_TETO_REF = 1410.0
R_BAIXO, R_CINTURA, R_TOPO = 50.0, 45.0, 110.0

perfil_poly = Polygon(fillet_poly([(x * S, z * S, r * S) for x, z, r in PERFIL], seg=8))
pl = [(x * S, y * S, r * S) for x, y, r in PLANTA]
planta_pts = pl + [(x, -y, r) for x, y, r in pl[::-1]]
planta_poly = Polygon(fillet_poly(planta_pts, seg=8))


def vertical_span(poly, x):
    ln = LineString([(x, -1e4), (x, 1e4)])
    g = poly.intersection(ln)
    if g.is_empty:
        return None
    b = g.bounds
    return b[1], b[3]


def cintura(x):
    return np.interp(x, CINTURA[:, 0] * S, CINTURA[:, 1] * S)


def secao(x, d, perf, plan, n_half):
    zs = vertical_span(perf, x)
    ys = vertical_span(plan, x)
    if zs is None or ys is None:
        return None
    zb, zt = zs
    hw = ys[1]
    if zt - zb < 0.2 or hw < 0.2:
        return None
    zc = cintura(x)
    rb = max(R_BAIXO * S - d, 0.3); rc = max(R_CINTURA * S - d, 0.3); rt = max(R_TOPO * S - d, 0.3)
    if zt - zc > 0.3:
        frac = (zt - zc) / max(Z_TETO_REF * S - zc, 1e-6)
        hwt = hw - (hw - (TETO_MEIA_LARG * S - d)) * frac
        pts = [(0, zb, 0), (hw, zb, rb), (hw, zc, rc), (hwt, zt, rt), (0, zt, 0)]
    else:
        pts = [(0, zb, 0), (hw, zb, rb), (hw, zt, rt), (0, zt, 0)]
    half = resample(fillet_poly(pts, closed=False, seg=10), n_half, peso_curva=4.0)
    full = np.r_[half, half[-2:0:-1] * [-1, 1]]
    return full


def loft(d=0.0):
    """Solido da carroceria deslocado para dentro em d (mm do modelo)."""
    perf = perfil_poly.buffer(-d, join_style=1) if d else perfil_poly
    plan = planta_poly.buffer(-d, join_style=1) if d else planta_poly
    x0, _, x1, _ = perf.bounds
    n_st = 70 if args.rapido else 220
    n_half = 30 if args.rapido else 70
    # estacoes mais densas nas pontas
    u = np.linspace(0, 1, n_st)
    xs = x0 + (x1 - x0) * (u - np.sin(2 * np.pi * u) / (2 * np.pi) * 0.75)
    xs[0] += 0.02; xs[-1] -= 0.02
    rings = []
    for x in xs:
        r = secao(x, d, perf, plan, n_half)
        if r is not None:
            rings.append(np.c_[np.full(len(r), x), r[:, 0], r[:, 1]])
    nr, m = len(rings), len(rings[0])
    V = np.vstack(rings)
    F = []
    for i in range(nr - 1):
        a, b = i * m, (i + 1) * m
        for j in range(m):
            k = (j + 1) % m
            F += [[a + j, b + j, b + k], [a + j, b + k, a + k]]
    c0 = len(V); V = np.vstack([V, rings[0].mean(0), rings[-1].mean(0)])
    for j in range(m):
        k = (j + 1) % m
        F.append([c0, k, j])
        F.append([c0 + 1, (nr - 1) * m + j, (nr - 1) * m + k])
    return to_manifold(V, np.array(F))


def plano_vidro(p0, p1, s0, s1, w0, w1, extra=0.0, prof=3.0):
    """Recorte de vidro num plano inclinado contendo o eixo Y, de p0 a p1 (perfil x,z)."""
    p0 = np.asarray(p0) * S; p1 = np.asarray(p1) * S
    a = p1 - p0; ln = np.linalg.norm(a); a /= ln
    s0 *= S; s1 = ln - s1 * S; w0 *= S; w1 *= S
    poly = Polygon([(s0, -w0), (s1, -w1), (s1, w1), (s0, w0)])
    if extra:
        poly = poly.buffer(extra, join_style=2)
    m = cs(np.array(poly.exterior.coords)[:-1]).extrude(2 * prof).translate([0, 0, -prof])
    nrm = np.array([-a[1], a[0]])  # normal no plano xz
    # local (s, y, n) -> mundo
    M = np.array([[a[0], 0, nrm[0], p0[0]], [0, 1, 0, 0], [a[1], 0, nrm[1], p0[1]]], float)
    return m.transform(M)


def linha_xz(pts, w=FRISO_L):
    return np.array(LineString(np.asarray(pts) * S).buffer(w / 2, cap_style=2, join_style=2).exterior.coords)[:-1]


def linha_xy(pts, w=FRISO_L):
    return np.array(LineString(np.asarray(pts) * S).buffer(w / 2, cap_style=2, join_style=2).exterior.coords)[:-1]


def bx(x0, x1, y0, y1, z0, z1):
    return box(x0 * S, x1 * S, y0 * S, y1 * S, z0 * S, z1 * S)


# ---------------------------------------------------------------- carroceria
print("Gerando carroceria...")
externo = loft(0)
interno = loft(PAREDE)
casca_friso = externo - loft(FRISO_P)
casca_bolso = externo - loft(PROF_BOLSO)

ZB = 200 * S
abertura_poly = planta_poly.buffer(-(PAREDE + ABA), join_style=1).intersection(
    Polygon([(300 * S, -1e3), (3600 * S, -1e3), (3600 * S, 1e3), (300 * S, 1e3)]))
abertura_poly = abertura_poly.buffer(-2, join_style=1).buffer(2, join_style=1)
abertura = prism_xy(np.array(abertura_poly.exterior.coords)[:-1], ZB - 5, ZB + PAREDE + 0.05)

arcos = m3d.Manifold()
for xa in (EIXO_DIANT, EIXO_TRAS):
    c = m3d.Manifold.cylinder(1200 * S * 2, ARCO_R * S, ARCO_R * S, 96, True).rotate([90, 0, 0])
    arcos += c.translate([xa * S, 0, ARCO_Z * S])

# janelas laterais (x, z)
JAN_PORTA = [(1330, 909), (1757, 1330), (2380, 1335), (2380, 961)]
JAN_QUEBRA = [(2460, 963), (2460, 1335), (3140, 1322), (3330, 985)]
jan_lat = prism_xz(np.array(JAN_PORTA) * S, -60, 60) + prism_xz(np.array(JAN_QUEBRA) * S, -60, 60)
PB = dict(p0=(1085, 860), p1=(1690, 1392), s0=40, s1=45, w0=690, w1=565)    # para-brisa
VT = dict(p0=(3765, 1000), p1=(3480, 1350), s0=30, s1=30, w0=600, w1=540)   # vigia traseira
para_brisa = plano_vidro(**PB)
vigia = plano_vidro(**VT)

# encaixes (bolsos) de farois, lanternas, grades e placas: caixas que pegam a superficie
FAROL = bx(-50, 290, 245, 860, 548, 712)
LANTERNA = bx(3660, 3990, 560, 860, 625, 975)
GRADE_SUP = bx(-50, 220, -230, 230, 590, 705)
GRADE_INF = bx(-50, 130, -560, 560, 285, 430)
PLACA_D = bx(-50, 60, -200, 200, 445, 575)
PLACA_T = bx(3800, 3990, -200, 200, 700, 830)
bolsos = {
    "farol_esquerdo": FAROL, "farol_direito": FAROL.mirror([0, 1, 0]),
    "lanterna_esquerda": LANTERNA, "lanterna_direita": LANTERNA.mirror([0, 1, 0]),
    "grade_superior": GRADE_SUP, "grade_inferior": GRADE_INF,
    "placa_dianteira": PLACA_D, "placa_traseira": PLACA_T,
}

# frisos (linhas de porta, capo, tampa traseira, para-choques)
frisos = m3d.Manifold()
for pts in ([(1270.6, 271.3), (1285, 905)], [(2421.7, 271.3), (2421.7, 975)], [(1266, 277.3), (2425, 277.3)]):
    frisos += prism_xz(linha_xz(pts), -60, 60)
for pts in ([(260, 735), (1085, 735)],):
    frisos += both_sides(prism_xy(linha_xy(pts), 600 * S, 950 * S))
frisos += prism_xy(linha_xy([(150, -735), (150, 735)]), 690 * S, 900 * S)
frisos += both_sides(prism_xy(linha_xy([(3600, 641.37), (3990, 641.37)]), 650 * S, 985 * S))
frisos += prism_xy(linha_xy([(3410, -646), (3410, 646)]), 1300 * S, 1450 * S)
frisos += box(3790 * S, 4000 * S, -646 * S, 646 * S, 655 * S - FRISO_L / 2, 655 * S + FRISO_L / 2)
frisos += box(-50 * S, 400 * S, -900 * S, 900 * S, 545 * S - FRISO_L / 2, 545 * S + FRISO_L / 2)
frisos += box(3500 * S, 4000 * S, -900 * S, 900 * S, 595 * S - FRISO_L / 2, 595 * S + FRISO_L / 2)
# tampa de combustivel (lado direito)
tampa = bx(3330, 3450, -900, -700, 820, 925) - box(3330 * S + FRISO_L, 3450 * S - FRISO_L, -900 * S, -700 * S,
                                                    820 * S + FRISO_L, 925 * S - FRISO_L)
frisos += tampa
macanetas = both_sides(bx(2200, 2320, 700, 900, 860, 900))

# furo dos retrovisores
RET_X, RET_Z = 1250 * S, 935 * S
furo_ret = both_sides(m3d.Manifold.cylinder(250 * S, 0.55, 0.55, 16).rotate([-90, 0, 0]).translate([RET_X, 700 * S, RET_Z]))

carroceria = externo - interno - abertura - arcos - jan_lat - para_brisa - vigia
carroceria -= (frisos ^ casca_friso)
carroceria -= (macanetas ^ (externo - loft(0.5)))
for b in bolsos.values():
    carroceria -= (b ^ casca_bolso)
carroceria -= furo_ret

# pecas de encaixe (mesma forma do bolso, com folga)
encaixes = {}
casca_ins = externo - loft(PROF_BOLSO)
for nome, b in bolsos.items():
    bb = b.bounding_box()
    shrink = box(bb[0] + FOLGA, bb[3] - FOLGA, bb[1] + FOLGA, bb[4] - FOLGA, bb[2] + FOLGA, bb[5] - FOLGA)
    peca = b ^ casca_ins ^ shrink
    # detalhes em relevo/baixo-relevo nas pecas
    if nome.startswith("grade"):
        z0, z1 = bb[2], bb[5]
        n = 3 if nome == "grade_superior" else 4
        for k in range(1, n + 1):
            zz = z0 + (z1 - z0) * k / (n + 1)
            peca -= box(bb[0] - 1, bb[0] + 1.2, bb[1] + 0.8, bb[4] - 0.8, zz - 0.3, zz + 0.3) ^ (externo - loft(0.4))
    encaixes[nome] = peca

# ---------------------------------------------------------------- vidros (encaixam por dentro)
print("Gerando vidros...")
casca_vidro = loft(PAREDE + FOLGA) - loft(PAREDE + FOLGA + VIDRO)
ext = 1.5
vidros = {
    "vidro_para_brisa": casca_vidro ^ plano_vidro(**PB, extra=ext, prof=5),
    "vidro_traseiro": casca_vidro ^ plano_vidro(**VT, extra=ext, prof=5),
}
for nome, pol in (("porta", JAN_PORTA), ("quebra_vento_traseiro", JAN_QUEBRA)):
    p = np.array(Polygon(np.array(pol) * S).buffer(ext, join_style=2).exterior.coords)[:-1]
    lado = prism_xz(p, 540 * S, 1100 * S) ^ casca_vidro
    vidros[f"vidro_{nome}_esquerdo"] = lado
    vidros[f"vidro_{nome}_direito"] = lado.mirror([0, 1, 0])

# ---------------------------------------------------------------- chassi + interior
print("Gerando chassi e interior...")
plat_poly = abertura_poly.buffer(-FOLGA, join_style=1)
# volumes livres dentro da carroceria (para as pecas internas nao baterem)
pe_plat = prism_xy(np.array(plat_poly.buffer(-0.2).exterior.coords)[:-1], 0, 200)
dentro = (loft(PAREDE + 0.3) + box(-10, L * S + 10, -60, 60, 0, ZB + PAREDE + 0.3)) ^ pe_plat
dentro_vidro = (loft(PAREDE + FOLGA + VIDRO + 0.3) + box(-10, L * S + 10, -60, 60, 0, ZB + PAREDE + 0.3)) ^ pe_plat
chassi = prism_xy(np.array(plat_poly.exterior.coords)[:-1], ZB, ZB + PAREDE)
ZP = ZB + PAREDE  # topo do assoalho
RZ, RY = ROD_Z * S, ROD_Y * S
pneu_r, pneu_l = PNEU_D / 2 * S, PNEU_L * S
y_pneu_int = RY - pneu_l / 2
for xa in (EIXO_DIANT * S, EIXO_TRAS * S):
    chassi -= both_sides(box(xa - pneu_r - 1.6, xa + pneu_r + 1.6, y_pneu_int - 0.5, 60, ZB - 1, ZP + 1))
    # caixa de roda interna (esconde o interior visto pelo para-lama)
    r_in = ARCO_R * S + 0.1
    y_ext_lim = abertura_poly.bounds[3] - FOLGA - 0.2
    liner = (m3d.Manifold.cylinder(y_ext_lim - (y_pneu_int - 0.5), r_in + 1.0, r_in + 1.0, 96) -
             m3d.Manifold.cylinder(30, r_in, r_in, 96, True))
    liner = liner.rotate([-90, 0, 0]).translate([xa, y_pneu_int - 0.5, ARCO_Z * S])
    liner = liner ^ box(xa - 30, xa + 30, -60, 60, ZP - 0.01, 80) ^ dentro
    chassi += both_sides(liner)
    # mancais do eixo
    y_mancal_ext = RY - (RODA_D / 2 * S) * 0 - (9.4 * (18 / args.escala)) / 2 - 0.4
    mancal = box(xa - 3, xa + 3, y_pneu_int - 12, y_mancal_ext, ZP - 0.01, RZ + 2.6)
    chassi += both_sides(mancal)
    chassi -= m3d.Manifold.cylinder(200, EIXO_D / 2 + 0.25, EIXO_D / 2 + 0.25, 32, True).rotate([90, 0, 0]).translate([xa, 0, RZ])

# interior (bancos, painel, console) - cor escura, colado sobre o chassi
IW = 560.0
interior = bx(1150, 3120, -IW, IW, 200, 330)                      # assoalho elevado
interior += bx(1180, 1480, -740, 740, 200, 880)                   # painel
interior += bx(1480, 2050, -110, 110, 330, 520)                   # console
for y in (-300, 300):
    interior += rounded_box(P(2180, y, 430), P(430, 470, 220), 25 * S)        # assento
    encosto = rounded_box(P(0, 0, 0), P(110, 470, 560), 25 * S).rotate([0, 14, 0])
    interior += encosto.translate(list(P(2420, y, 680)))
    interior += rounded_box(P(2470, y, 1040), P(90, 260, 170), 20 * S)       # apoio de cabeca
interior += rounded_box(P(2900, 0, 420), P(380, 1100, 200), 25 * S)          # banco traseiro
interior += rounded_box(P(3080, 0, 680), P(110, 1100, 480), 25 * S).rotate([0, 0, 0])
interior += bx(1150, 1250, -740, 740, 330, 700)                   # parede corta-fogo
interior = interior ^ dentro_vidro
chassi += interior

# ---------------------------------------------------------------- rodas e pneus
print("Gerando rodas e pneus...")
R_ASSENTO = RODA_D / 2 * S
LARG_RODA = 9.4 * (18 / args.escala)
R_BORDA = R_ASSENTO + 0.6 * (18 / args.escala)
F = 18 / args.escala  # fator de detalhes que nao escalam bem


def roda(estilo):
    """Roda com a face para +z. Imprimir com a face interna (z=0) na mesa."""
    w = LARG_RODA
    tambor = m3d.Manifold.cylinder(w, R_ASSENTO, R_ASSENTO, 96) - m3d.Manifold.cylinder(w * 3, R_ASSENTO - 0.9 * F, R_ASSENTO - 0.9 * F, 96, True)
    borda = m3d.Manifold.cylinder(0.8 * F, R_BORDA, R_BORDA, 96) - m3d.Manifold.cylinder(5, R_ASSENTO - 0.9 * F, R_ASSENTO - 0.9 * F, 96, True)
    borda_ext = borda.translate([0, 0, w - 0.8 * F])
    prato = 2.4 * F                       # profundidade da face (aro "prato fundo")
    z_face = w - prato
    esp_face = 1.2 * F
    r_cubo = 3.6 * F
    if estilo == "bbs":
        face2d = m3d.CrossSection.circle(r_cubo + 0.25, 48)
        aro_face = m3d.CrossSection.circle(R_ASSENTO - 0.5 * F, 96) - m3d.CrossSection.circle(R_ASSENTO - 1.6 * F, 96)
        face2d += aro_face
        n = 10
        for i in range(n):
            a = 2 * np.pi * i / n
            for s in (-1, 1):
                b = a + s * np.radians(28)
                p0 = np.array([np.cos(a), np.sin(a)]) * (r_cubo - 0.5)
                p1 = np.array([np.cos(b), np.sin(b)]) * (R_ASSENTO - 1.0 * F)
                bar = LineString([p0, p1]).buffer(0.45 * F, cap_style=2)
                face2d += cs(np.array(bar.exterior.coords)[:-1])
        face = face2d.extrude(esp_face).translate([0, 0, z_face])
    else:  # Porsche Cup 5 raios
        disco = m3d.CrossSection.circle(R_ASSENTO - 0.5 * F, 96)
        for i in range(5):
            a = 2 * np.pi * i / 5 + np.pi / 5
            c = np.array([np.cos(a), np.sin(a)])
            jan = Polygon([tuple(c * (r_cubo + 0.8 * F) + np.array([-c[1], c[0]]) * 1.0 * F),
                           tuple(c * (r_cubo + 0.8 * F) - np.array([-c[1], c[0]]) * 1.0 * F),
                           tuple(c * (R_ASSENTO - 1.4 * F) - np.array([-c[1], c[0]]) * 3.6 * F),
                           tuple(c * (R_ASSENTO - 1.4 * F) + np.array([-c[1], c[0]]) * 3.6 * F)]).buffer(0.6 * F)
            disco -= cs(np.array(jan.exterior.coords)[:-1])
        face = disco.extrude(esp_face).translate([0, 0, z_face])
    # cubo central e tampa
    cubo = m3d.Manifold.cylinder(z_face + esp_face, r_cubo, r_cubo, 48)
    tampa_c = m3d.Manifold.cylinder(0.8 * F, 2.4 * F, 2.0 * F, 48).translate([0, 0, z_face + esp_face])
    furos = m3d.Manifold()
    for i in range(5):
        a = 2 * np.pi * i / 5
        furos += m3d.Manifold.cylinder(1, 0.35 * F, 0.35 * F, 12).translate(
            [np.cos(a) * 2.9 * F, np.sin(a) * 2.9 * F, z_face + esp_face - 0.5])
    r = tambor + borda_ext + face + cubo + tampa_c - furos
    # furo do eixo (cego): vareta de 3 mm entra justa
    r -= m3d.Manifold.cylinder(z_face + esp_face - 0.6, EIXO_D / 2, EIXO_D / 2, 32).translate([0, 0, -0.01])
    return r


def pneu():
    ri = R_ASSENTO + 0.05                 # justo: PLA + cola, ou TPU (entra sob pressao)
    ro = PNEU_D / 2 * S
    w = PNEU_L * S
    sob = (w - LARG_RODA) / 2             # quanto o pneu sobra de cada lado da roda
    z_deg = w - sob - 0.8 * F - 0.1       # degrau que acomoda a borda externa do aro
    prof = fillet_poly([(ri, 0, 0), (ro - 0.4, 0, 0.8), (ro, 0.4 * w / 2, 1.2), (ro, w - 0.4 * w / 2, 1.2),
                        (ro - 0.4, w, 0.8), (R_BORDA + 0.1, w, 0), (R_BORDA + 0.1, z_deg, 0), (ri, z_deg, 0)], seg=6)
    m = cs(prof).revolve(128)
    # sulcos da banda de rodagem
    for f in (0.3, 0.5, 0.7):
        g = m3d.Manifold.cylinder(0.5, ro + 1, ro + 1, 128) - m3d.Manifold.cylinder(0.6, ro - 0.35, ro - 0.35, 128, True).translate([0, 0, 0.25])
        m -= g.translate([0, 0, w * f - 0.25])
    return m


roda_m = roda(args.roda)
pneu_m = pneu()

# eixo impresso (alternativa a vareta de aco): D com face plana para imprimir deitado
y_furo = RY + LARG_RODA / 2 - (LARG_RODA - 2.4 * F + 1.2 * F - 0.6)  # inicio do furo cego (lado interno)
y_fundo = RY - LARG_RODA / 2 + (LARG_RODA - 2.4 * F + 1.2 * F - 0.6)
comp_eixo = 2 * y_fundo - 0.4
eixo = m3d.Manifold.cylinder(comp_eixo, EIXO_D / 2, EIXO_D / 2, 32) ^ box(-5, 5, -5, EIXO_D / 2 - 0.3, -1, comp_eixo + 1)

# ---------------------------------------------------------------- retrovisores e volante
ret = rounded_box([0, 0, 0], [2.4 * F, 5.6 * F, 4.0 * F], 0.8 * F)          # carcaca
ret += rounded_box([0.6 * F, -2.0 * F, -1.0 * F], [2.6 * F, 2.6 * F, 1.8 * F], 0.5 * F)  # braco
ret -= box(-2 * F, -0.9 * F, -2.2 * F, 2.2 * F, -1.4 * F, 1.4 * F)          # espelho (rebaixo)
ret += m3d.Manifold.cylinder(2.0, 0.45, 0.45, 16).rotate([90, 0, 0]).translate([0.6 * F, -3.2 * F + 0.1, -1.0 * F])
ret_esq = ret  # pino aponta para -y (entra na porta esquerda)
ret_dir = ret.mirror([0, 1, 0])

vol = (m3d.Manifold.cylinder(0.9 * F, 3.4 * F, 3.4 * F, 48) - m3d.Manifold.cylinder(3, 2.6 * F, 2.6 * F, 48, True))
for a in (90, 210, 330):
    vol += box(0, 3.0 * F, -0.4 * F, 0.4 * F, 0, 0.7 * F).rotate([0, 0, a])
vol += m3d.Manifold.cylinder(0.9 * F, 1.1 * F, 1.1 * F, 32)
vol += m3d.Manifold.cylinder(4, 0.6, 0.6, 16).translate([0, 0, 0])  # pino da coluna


# ---------------------------------------------------------------- exportacao
def deitar(m, up=None):
    """Coloca a peca na mesa (z min = 0). up: vetor que deve apontar para +z."""
    tm = to_trimesh(m)
    if up is not None:
        up = np.asarray(up, float); up /= np.linalg.norm(up)
        R = trimesh.geometry.align_vectors(up, [0, 0, 1])
        tm.apply_transform(R)
    elif up is None:
        pass
    tm.apply_translation(-tm.bounds[0] * [1, 1, 0] - [0, 0, tm.bounds[0][2]])
    return tm


def deitar_pca(m, sinal_ref):
    """Para pecas finas e curvas (vidros/encaixes): normal media -> +z (face externa para cima)."""
    tm = to_trimesh(m)
    c = tm.vertices - tm.vertices.mean(0)
    w, v = np.linalg.eigh(c.T @ c)
    n = v[:, 0]
    if np.dot(n, sinal_ref) < 0:
        n = -n
    tm.apply_transform(trimesh.geometry.align_vectors(n, [0, 0, 1]))
    xy = tm.vertices[:, :2] - tm.vertices[:, :2].mean(0)
    w2, v2 = np.linalg.eigh(xy.T @ xy)
    ang = np.arctan2(v2[1, 1], v2[0, 1])
    tm.apply_transform(trimesh.transformations.rotation_matrix(-ang, [0, 0, 1]))
    tm.apply_translation(-tm.bounds[0])
    return tm


pecas = {}  # nome -> (trimesh, cor, qtd)
pecas["carroceria"] = (deitar(carroceria), "branco", 1)
pecas["chassi_interior"] = (deitar(chassi), "preto", 1)
pecas["roda"] = (deitar(roda_m), "prata", 4)
pecas["pneu"] = (deitar(pneu_m), "preto", 4)
pecas["eixo_opcional"] = (deitar(eixo.rotate([-90, 0, 0])), "preto", 2)
pecas["retrovisor_esquerdo"] = (deitar(ret_esq, up=[-1, 0, 0]), "preto", 1)
pecas["retrovisor_direito"] = (deitar(ret_dir, up=[-1, 0, 0]), "preto", 1)
pecas["volante"] = (deitar(vol), "preto", 1)
cores_enc = {"farol": "transparente_ou_prata", "lanterna": "vermelho", "grade": "preto", "placa": "branco"}
for nome, peca in encaixes.items():
    cor = cores_enc[nome.split("_")[0]]
    ref = {"farol": [-1, 0, 0.3], "lanterna": [1, 0, 0], "grade": [-1, 0, 0], "placa": [-1, 0, 0]}[nome.split("_")[0]]
    if nome == "placa_traseira":
        ref = [1, 0, 0]
    pecas[nome] = (deitar_pca(peca, ref), cor, 1)
for nome, peca in vidros.items():
    ref = {"para_brisa": [-1, 0, 1], "traseiro": [1, 0, 1]}
    r = [0, 1 if "esquerdo" in nome else -1, 0]
    for k, v in ref.items():
        if k in nome:
            r = v
    pecas[nome] = (deitar_pca(peca, r), "transparente_ou_preto_fume", 1)

os.makedirs(f"{OUT}/stl", exist_ok=True)
for nome, (tm, cor, qtd) in pecas.items():
    os.makedirs(f"{OUT}/stl/{cor}", exist_ok=True)
    fn = f"{OUT}/stl/{cor}/{nome}{'_x' + str(qtd) if qtd > 1 else ''}.stl"
    tm.export(fn)
    print(f"  {cor:28s} {nome:32s} x{qtd}  {tm.extents.round(1)} mm  {'OK' if tm.is_watertight else 'NAO ESTANQUE'}")

# 3MF por cor (pecas ja espalhadas na mesa 256x256 da A1, com as quantidades)
os.makedirs(f"{OUT}/3mf", exist_ok=True)
por_cor = {}
for nome, (tm, cor, qtd) in pecas.items():
    por_cor.setdefault(cor, []).extend([(nome, tm)] * qtd)
for cor, lista in por_cor.items():
    cena = trimesh.Scene()
    x = y = 5.0; linha_h = 0.0
    for i, (nome, tm) in enumerate(sorted(lista, key=lambda t: -t[1].extents[1])):
        e = tm.extents
        if x + e[0] > 251:
            x = 5.0; y += linha_h + 5; linha_h = 0
        t = tm.copy(); t.apply_translation([x, y, 0])
        cena.add_geometry(t, node_name=f"{nome}_{i}")
        x += e[0] + 5; linha_h = max(linha_h, e[1])
    cena.export(f"{OUT}/3mf/mesa_{cor}.3mf")

# montagem (para visualizacao)
os.makedirs(f"{OUT}/preview", exist_ok=True)
mont = trimesh.Scene()
def add(m, cor, nome):
    t = to_trimesh(m); t.visual.face_colors = cor; mont.add_geometry(t, node_name=nome)
add(carroceria, [245, 245, 245, 255], "carroceria")
add(chassi, [30, 30, 30, 255], "chassi")
for nome, peca in encaixes.items():
    c = {"farol": [175, 195, 215, 255], "lanterna": [200, 20, 20, 255], "grade": [20, 20, 20, 255], "placa": [235, 235, 235, 255]}[nome.split("_")[0]]
    add(peca, c, nome)
for nome, peca in vidros.items():
    add(peca, [25, 30, 35, 255], nome)
for xa in (EIXO_DIANT * S, EIXO_TRAS * S):
    for sgn in (1, -1):
        r = roda_m.translate([0, 0, -LARG_RODA / 2]).rotate([-90 * sgn, 0, 0]).translate([xa, sgn * RY, RZ])
        p = pneu_m.translate([0, 0, -PNEU_L * S / 2]).rotate([-90 * sgn, 0, 0]).translate([xa, sgn * RY, RZ])
        add(r, [190, 190, 195, 255], f"roda{xa:.0f}{sgn}"); add(p, [25, 25, 25, 255], f"pneu{xa:.0f}{sgn}")
for sgn, rr in ((1, ret_esq), (-1, ret_dir)):
    yb = vertical_span(planta_poly, RET_X)[1] - 0.6
    add(rr.translate([RET_X - 0.6 * F, sgn * (yb + 3.2 * F), RET_Z + 1.0 * F]), [30, 30, 30, 255], f"ret{sgn}")
mont.export(f"{OUT}/preview/montagem.glb")
print(f"Escala 1:{args.escala:g}  comprimento {L*S:.1f} mm  chao em z={CHAO_Z*S:.1f} (vao livre {(200-CHAO_Z)*S:.1f} mm)")
print(f"Eixo: vareta {EIXO_D} mm x {comp_eixo:.1f} mm (2 unidades)")
