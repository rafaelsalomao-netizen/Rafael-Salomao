# Árvore de Natal de nomes – impressão 3D (Bambu Lab A1, sem AMS)

Nomes empilhados em forma de árvore, alternando verde e vermelho, com "FELIZ NATAL" no pé
(igual à foto de referência, sem a estrela). Fonte Impact, a mesma da foto.
Cada nome é uma peça única: letras grossas presas por uma barra em cima e outra embaixo.

Larguras dos andares medidas na foto de referência (150/115/99/75/54 mm, de baixo para cima), barras de
3,5 mm. CAMILA embaixo fica natural como BRUNNO (6 letras); os outros nomes, mais curtos, alargam 40% para
preencher o andar. `comparar.png` mostra foto e modelo na mesma escala; `comparar_opcoes.png` e
`comparar_camila.png` mostram as alternativas testadas.

| Peça        | Cor      | Largura x altura (mm) |
|-------------|----------|-----------------------|
| FELIZ NATAL | vermelho | 70 x 16               |
| CAMILA      | verde    | 150 x 48              |
| THEO        | vermelho | 112 x 42              |
| NINA        | verde    | 96 x 37,5             |
| MAX         | vermelho | 73,5 x 31             |
| EDU         | verde    | 52,5 x 29             |

Profundidade de todas as peças: 25 mm. Árvore montada: 150 mm de largura x 203 mm de altura.

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
`bash ciclo.sh impact caminho/da/foto.jpg` gera peças, renders e comparação na mesma escala (`comparar.py`) (requer Python com trimesh, shapely,
fonttools, manifold3d, Pillow; Node com playwright; ffmpeg; e `three/package` = `npm pack three@0.160.0` extraído).
Só as peças: `python3 gerar.py fonts/impact.ttf out`.
Fonte Impact: não vai no repositório por licença; baixe `impact32.exe` (Microsoft Core Fonts, SourceForge),
extraia com `cabextract` e salve como `fonts/impact.ttf`.
Para trocar os nomes, edite `ANDARES`, `LARGURAS` e `ALT_MAX` em `gerar.py` (de baixo para cima).
