#!/bin/bash
# Regera tudo: peças (STL/3MF), renders para o cliente (frente, ângulo, giro) e comparação com a foto.
# uso: bash ciclo.sh impact [caminho/da/foto_referencia.jpg]
set -e
rm -rf out; python3 gerar.py fonts/$1.ttf out 2>&1 | grep -E "mm  |altura|rror"
python3 - <<'PY'
import base64, glob, json, os, re
pecas=[{"cor":os.path.basename(p).split('_')[1][:-4],"b64":base64.b64encode(open(p,'rb').read()).decode()} for p in sorted(glob.glob('out/montagem/*.stl'))]
s=open('vitrine.tpl.html').read()
s=re.sub(r'const PECAS=\[.*?\];', lambda m:'const PECAS='+json.dumps(pecas)+';', s, flags=re.S)
open('vitrine.html','w').write(s)
PY
mkdir -p cliente
timeout 300 node render2.js fotos 1080 1350
cp vframes/frente.png cliente/arvore_natal_frente.png; cp vframes/angulo.png cliente/arvore_natal_angulo.png
timeout 900 node render2.js 90 810 1012
ffmpeg -loglevel error -y -framerate 30 -i vframes/f%03d.png -c:v libx264 -pix_fmt yuv420p -crf 22 cliente/arvore_natal_giro.mp4
ffmpeg -loglevel error -y -framerate 15 -i vframes/f%03d.png -vf "select='not(mod(n,2))',scale=405:-1,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=3" -loop 0 cliente/arvore_natal_giro.gif
# comparação na mesma escala (câmera fixa) com a foto de referência
if [ -n "$2" ]; then
  BASE=$(python3 -c "import trimesh,glob; print(round(max(trimesh.load(f).extents[0] for f in glob.glob('out/*.stl')),1))")
  VITRINE=vitrine.html QUERY='?dist=620&alvo=105' FRAMES=cmp timeout 300 node render2.js fotos 1080 1350
  python3 comparar.py "$2" comparar.png "cmp:$BASE:MODELO 3D:medidas da foto, fonte Impact"
fi
echo "ok"
