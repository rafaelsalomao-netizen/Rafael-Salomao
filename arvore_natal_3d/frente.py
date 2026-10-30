import json, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from shapely import wkt
P = {k: wkt.loads(v) for k, v in json.load(open("out/_perfis.json")).items()}
ordem = [("FELIZ NATAL","#e0243f"),("CAMILA","#13a34f"),("THEO","#e0243f"),("NINA","#13a34f"),("MAX","#e0243f"),("EDU","#13a34f")]
def desenha(ax, g, dx, dy, c):
    for p in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
        xs, ys = p.exterior.xy; ax.fill([x+dx for x in xs], [y+dy for y in ys], color=c, lw=0)
        for i in p.interiors:
            xs, ys = i.xy; ax.fill([x+dx for x in xs], [y+dy for y in ys], color="white", lw=0)
fig, axs = plt.subplots(1, 2, figsize=(14, 9), dpi=110)
z = 0
for n, c in ordem:
    g = P[n]; w, h = g.bounds[2], g.bounds[3]
    desenha(axs[0], g, -w/2, z, c); z += h
axs[0].set_aspect("equal"); axs[0].axis("off"); axs[0].set_title("Árvore montada (vista de frente)", fontsize=14)
y = 0
for n, c in reversed(ordem):
    g = P[n]; w, h = g.bounds[2], g.bounds[3]
    desenha(axs[1], g, -w/2, y - h, c)
    for yy in (y - 0.6, y - h + 0.6):  # marca início/fim das barras
        axs[1].plot([-w/2, w/2], [yy, yy], color="black", lw=0, marker="|", ms=14, mew=1.5)
    axs[1].annotate("", xy=(-w/2, y-h-5), xytext=(w/2, y-h-5), arrowprops=dict(arrowstyle="<->", lw=1))
    axs[1].text(0, y-h-11, f"barra de cima e de baixo = {w:.0f} mm = largura de {n}", ha="center", fontsize=9)
    y -= h + 22
axs[1].set_aspect("equal"); axs[1].axis("off"); axs[1].set_title("Cada peça separada", fontsize=14)
plt.tight_layout(); plt.savefig("vista_frente.png", facecolor="white")
