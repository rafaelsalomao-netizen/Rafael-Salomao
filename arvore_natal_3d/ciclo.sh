set -e
rm -rf out; python3 gerar.py fonts/$1.ttf out 2>&1 | grep -E "mm  |altura|rror"
python3 - <<'PY'
import base64, glob, json, os, re
pecas=[{"cor":os.path.basename(p).split('_')[1][:-4],"b64":base64.b64encode(open(p,'rb').read()).decode()} for p in sorted(glob.glob('out/montagem/*.stl'))]
s=open('vitrine.html').read()
s=re.sub(r'const PECAS=\[.*?\];', lambda m:'const PECAS='+json.dumps(pecas)+';', s, flags=re.S)
open('vitrine.html','w').write(s)
PY
timeout 200 node render2.js 1
python3 -c "
from PIL import Image
a=Image.open('/root/.claude/uploads/daa4785b-4af7-5d47-9ba7-af3f324ba340/36ce56ab-image.jpg').crop((20,260,720,1200)); a=a.resize((int(a.width*900/a.height),900))
b=Image.open('vframes/f000.png').crop((90,60,990,1260)); b=b.resize((int(b.width*900/b.height),900))
c=Image.new('RGB',(a.width+b.width,900),'white'); c.paste(a,(0,0)); c.paste(b,(a.width,0)); c.save('comparar.png')"
