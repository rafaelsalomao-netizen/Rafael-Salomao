# Árvore de Natal de nomes – impressão 3D (Bambu Lab A1, sem AMS)

Nomes empilhados em forma de árvore, alternando verde e vermelho, com "FELIZ NATAL" no pé
(igual à foto de referência, sem a estrela). Fonte Impact, a mesma da foto.
Cada nome é uma peça única: letras grossas presas por uma barra em cima e outra embaixo.

Larguras e alturas de cada bloco medidas na foto de referência (de baixo para cima: 150/115/99/75/54 mm
de largura; blocos de 42,3/43,3/20,8/28,2/25,4 mm; FELIZ NATAL 70 x 13 mm). Como na foto, a placa de baixo
de cada bloco é grossa (4–5 mm) e a barra de cima fina (2–2,5 mm); as letras ficam encostadas (vão de 6% da
altura) e alargadas em relação à Impact pura (na foto ~1,2x; aqui 1,2x a 1,4x, porque os nomes são mais curtos).

Duas variantes:
- **EDUARDO** (`out/`, oficial): CAMILA, THEO, EDUARDO, NINA, MAX. EDUARDO (7 letras) faz o andar baixo do
  meio como VALENTINA. Só o 3º e o 4º andares ficam 2 mm mais altos que na foto. Árvore: 150 x 177 mm.
- **EDU** (`out_edu/`): CAMILA, THEO, NINA, MAX, EDU. O 3º andar (NINA, 4 letras) fica com 30,5 mm em vez dos
  20,8 mm da VALENTINA. Árvore: 150 x 183 mm.

`comparar.png` mostra foto e modelo na mesma escala; `comparar_eduardo.png` compara as duas variantes com a foto.
O que não dá para igualar: os nomes da foto têm o número certo de letras para encher cada andar com 1,2x de
alargamento; THEO e NINA são mais curtos e saem com 1,4x.

| Peça        | EDUARDO (cor, L x A mm)     | EDU (cor, L x A mm)      |
|-------------|--------------------------|-----------------------------|
| pé          | FELIZ NATAL verm. 70 x 13   | FELIZ NATAL verm. 70 x 13 |
| 1º andar    | CAMILA verde 149 x 42       | CAMILA verde 149 x 42    |
| 2º andar    | THEO verm. 114 x 43         | THEO verm. 114 x 43      |
| 3º andar    | EDUARDO verde 98 x 23       | NINA verde 96 x 30,5     |
| 4º andar    | NINA verm. 74 x 30          | MAX verm. 74 x 28        |
| 5º andar    | MAX verde 54 x 25,5         | EDU verde 53 x 25,5      |

Profundidade de todas as peças: 25 mm.

## Imprimir
- EDUARDO: `out/placa_verde.3mf` (CAMILA, EDUARDO, MAX) e `out/placa_vermelho.3mf` (THEO, NINA, FELIZ NATAL).
- EDU: `out_edu/placa_verde.3mf` (CAMILA, NINA, EDU) e `out_edu/placa_vermelho.3mf` (THEO, MAX, FELIZ NATAL).
- Duas impressões por árvore: uma placa em verde, troca o filamento, outra em vermelho.
- Ou importe os STL de `out/` um a um (o nome do arquivo já diz a cor).
- Peças deitadas, frente das letras virada para a mesa (já vêm assim) – a textura da mesa fica na frente, como na foto.
- Sem suporte. PLA, camada 0,2 mm, 3 perímetros, 15% de preenchimento. Mesa texturizada PEI.
- Montagem, de baixo para cima: FELIZ NATAL, CAMILA, THEO, EDUARDO, NINA, MAX (variante EDU: FELIZ NATAL, CAMILA, THEO, NINA, MAX, EDU). Colar com cola instantânea (cianoacrilato) centralizando cada andar no de baixo.

## Para o cliente
`cliente/`: foto de frente, foto em ângulo e vídeo girando (MP4/GIF). `comparar.png`: foto de referência lado a lado com o modelo.

## Regerar
`bash ciclo.sh impact caminho/da/foto.jpg` gera peças, renders e comparação na mesma escala (`comparar.py`) (requer Python com trimesh, shapely,
fonttools, manifold3d, Pillow; Node com playwright; ffmpeg; e `three/package` = `npm pack three@0.160.0` extraído).
Só as peças: `python3 gerar.py fonts/impact.ttf out` (EDUARDO) ou `python3 gerar.py fonts/impact.ttf out_edu edu`.
Fonte Impact: não vai no repositório por licença; baixe `impact32.exe` (Microsoft Core Fonts, SourceForge),
extraia com `cabextract` e salve como `fonts/impact.ttf`.
Para trocar os nomes, edite `ANDARES`, `LARGURAS` e `ALT_MAX` em `gerar.py` (de baixo para cima).
