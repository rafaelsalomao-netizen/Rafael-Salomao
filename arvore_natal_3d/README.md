# Árvore de Natal de nomes – impressão 3D (Bambu Lab A1)

Nomes empilhados em forma de árvore, alternando verde e vermelho, com "FELIZ NATAL" no pé.
Cada nome é uma peça com letras grossas vazadas, presas por uma barra em cima e outra embaixo.

## Imprimir
- `out/placa_verde.3mf`: THEO, CAMILA, EDU (filamento verde)
- `out/placa_vermelho.3mf`: MAX, NINA, FELIZ NATAL (filamento vermelho)
- Sem suporte: peças deitadas, frente das letras virada para a mesa. PLA, camada 0,2 mm, 15% de preenchimento.
- Montagem, de baixo para cima: FELIZ NATAL, THEO, MAX, CAMILA, NINA, EDU (colar).

## Para o cliente
`cliente/`: vídeo girando (MP4/GIF) e fotos simuladas.

## Regerar
`python3 gerar.py fonts/oswald700.ttf out` (requer trimesh, shapely, fonttools, manifold3d).
Vídeo: `bash ciclo.sh oswald700` e `node render2.js 150` (precisa de three@0.160.0 em `three/package`).
