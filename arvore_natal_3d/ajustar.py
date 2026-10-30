import sys,re
s=open('gerar.py').read()
larg,alt,mold,eng,esp=sys.argv[1:6]
s=re.sub(r'^LARGURAS = .*$',f'LARGURAS = [{larg}]  # largura alvo de cada andar, de baixo para cima (mm)',s,flags=re.M)
s=re.sub(r'^ALT_MAX = .*$',f'ALT_MAX = [{alt}]  # altura máxima de cada andar (mm) – andares de cima mais baixos, como na foto',s,flags=re.M)
s=re.sub(r'^MOLDURA = [0-9.]+',f'MOLDURA = {mold}',s,flags=re.M)
s=re.sub(r'^ENGROSSA = [0-9.]+',f'ENGROSSA = {eng}',s,flags=re.M)
s=re.sub(r'^ESPACO = [0-9.]+',f'ESPACO = {esp}',s,flags=re.M)
s=s.replace('build_piece(txt, alvo, ALT_MAX)','build_piece(txt, alvo, ALT_MAX[i])')
open('gerar.py','w').write(s)
