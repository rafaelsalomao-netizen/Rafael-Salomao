# Árvore de Natal de nomes – impressão 3D (Bambu Lab A1, sem AMS)

Nomes empilhados em forma de árvore, alternando verde e vermelho, com "FELIZ NATAL" no pé
(igual à foto de referência, sem a estrela). Fonte Impact, a mesma da foto.
Cada nome é uma peça única: letras grossas presas por uma barra em cima e outra embaixo.

Larguras e alturas de cada bloco medidas na foto de referência (de baixo para cima: 150/115/99/75/54 mm
de largura; 42,3/43,3/20,8/28,2/25,4 mm de altura com as barras de 2,5 mm; FELIZ NATAL 70 x 13 mm).
CAMILA embaixo fica quase natural como BRUNNO; os nomes curtos alargam até 50% para preencher o andar.

Duas variantes:
- **EDU** (`out/`): CAMILA, THEO, NINA, MAX, EDU. O 3º andar (NINA, 4 letras) fica com 30,5 mm em vez dos
  20,8 mm da VALENTINA. Árvore: 150 x 183 mm.
- **EDUARDO** (`out_eduardo/`): CAMILA, THEO, EDUARDO, NINA, MAX. EDUARDO (7 letras) faz o andar baixo do
  meio como VALENTINA e todas as alturas ficam iguais às da foto. Árvore: 150 x 173 mm.

`comparar.png` mostra foto e modelo EDU na mesma escala; `comparar_eduardo.png` compara as duas variantes com a foto.

| Peça        | EDU (cor, L x A mm)      | EDUARDO (cor, L x A mm)     |
|-------------|--------------------------|-----------------------------|
| pé          | FELIZ NATAL verm. 68 x 13 | FELIZ NATAL verm. 68 x 13  |
| 1º andar    | CAMILA verde 149 x 42    | CAMILA verde 149 x 42       |
| 2º andar    | THEO verm. 113 x 43      | THEO verm. 113 x 43         |
| 3º andar    | NINA verde 96 x 30,5     | EDUARDO verde 96 x 21       |
| 4º andar    | MAX verm. 73 x 28        | NINA verm. 73 x 28          |
| 5º andar    | EDU verde 52 x 25,5      | MAX verde 53 x 25,5         |

Profundidade de todas as peças: 25 mm.

## Imprimir
- EDU: `out/placa_verde.3mf` (CAMILA, NINA, EDU) e `out/placa_vermelho.3mf` (THEO, MAX, FELIZ NATAL).
- EDUARDO: `out_eduardo/placa_verde.3mf` (CAMILA, EDUARDO, MAX) e `out_eduardo/placa_vermelho.3mf` (THEO, NINA, FELIZ NATAL).
- Duas impressões por árvore: uma placa em verde, troca o filamento, outra em vermelho.
- Ou importe os STL de `out/` um a um (o nome do arquivo já diz a cor).
- Peças deitadas, frente das letras virada para a mesa (já vêm assim) – a textura da mesa fica na frente, como na foto.
- Sem suporte. PLA, camada 0,2 mm, 3 perímetros, 15% de preenchimento. Mesa texturizada PEI.
- Montagem, de baixo para cima: FELIZ NATAL, CAMILA, THEO, NINA, MAX, EDU (ou FELIZ NATAL, CAMILA, THEO, EDUARDO, NINA, MAX). Colar com cola instantânea (cianoacrilato) centralizando cada andar no de baixo.

## Para o cliente
`cliente/`: foto de frente, foto em ângulo e vídeo girando (MP4/GIF). `comparar.png`: foto de referência lado a lado com o modelo.

## Regerar
`bash ciclo.sh impact caminho/da/foto.jpg` gera peças, renders e comparação na mesma escala (`comparar.py`) (requer Python com trimesh, shapely,
fonttools, manifold3d, Pillow; Node com playwright; ffmpeg; e `three/package` = `npm pack three@0.160.0` extraído).
Só as peças: `python3 gerar.py fonts/impact.ttf out` (variante EDU) ou `python3 gerar.py fonts/impact.ttf out_eduardo eduardo`.
Fonte Impact: não vai no repositório por licença; baixe `impact32.exe` (Microsoft Core Fonts, SourceForge),
extraia com `cabextract` e salve como `fonts/impact.ttf`.
Para trocar os nomes, edite `ANDARES`, `LARGURAS` e `ALT_MAX` em `gerar.py` (de baixo para cima).
