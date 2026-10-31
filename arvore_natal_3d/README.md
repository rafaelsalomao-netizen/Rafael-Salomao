# Árvore de Natal de nomes – impressão 3D (Bambu Lab A1, sem AMS)

Nomes empilhados em forma de árvore, alternando verde e vermelho, com "FELIZ NATAL" no pé
(igual à foto de referência, sem a estrela). Fonte Impact, a mesma da foto.
Cada nome é uma peça única: letras grossas presas por uma barra em cima e outra embaixo.

Nomes, de baixo para cima (ordem escolhida pela largura natural de cada nome, para a árvore afinar sem esticar as letras):

| Peça        | Cor      | Largura x altura (mm) |
|-------------|----------|-----------------------|
| FELIZ NATAL | vermelho | 72 x 16               |
| CAMILA      | verde    | 156 x 49              |
| THEO        | vermelho | 106 x 43              |
| NINA        | verde    | 81 x 35,5             |
| MAX         | vermelho | 63 x 30,5             |
| EDU         | verde    | 44 x 26,5             |

Profundidade de todas as peças: 25 mm. Árvore montada: 156 mm de largura x 200 mm de altura.

## Imprimir
- `out/placa_verde.3mf`: CAMILA, NINA, EDU (filamento verde) – uma impressão.
- `out/placa_vermelho.3mf`: THEO, MAX, FELIZ NATAL (filamento vermelho) – outra impressão.
- Ou importe os STL de `out/` um a um (o nome do arquivo já diz a cor).
- Peças deitadas, frente das letras virada para a mesa (já vêm assim) – a textura da mesa fica na frente, como na foto.
- Sem suporte. PLA, camada 0,2 mm, 3 perímetros, 15% de preenchimento. Mesa texturizada PEI.
- Montagem, de baixo para cima: FELIZ NATAL, CAMILA, THEO, NINA, MAX, EDU. Colar com cola instantânea (cianoacrilato) centralizando cada andar no de baixo.

## Para o cliente
`cliente/`: foto de frente, foto em ângulo e vídeo girando (MP4/GIF). `comparar.png`: foto de referência lado a lado com o modelo.

## Regerar
`bash ciclo.sh impact caminho/da/foto.jpg` gera peças, renders e comparação (requer Python com trimesh, shapely,
fonttools, manifold3d, Pillow; Node com playwright; ffmpeg; e `three/package` = `npm pack three@0.160.0` extraído).
Só as peças: `python3 gerar.py fonts/impact.ttf out`.
Fonte Impact: não vai no repositório por licença; baixe `impact32.exe` (Microsoft Core Fonts, SourceForge),
extraia com `cabextract` e salve como `fonts/impact.ttf`.
Para trocar os nomes, edite `ANDARES`, `LARGURAS` e `ALT_MAX` em `gerar.py` (de baixo para cima).
