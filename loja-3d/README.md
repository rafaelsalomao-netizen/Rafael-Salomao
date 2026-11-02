# Camada 3D — kit de abertura da loja

Tudo o que precisa existir para começar a vender produtos impressos em 3D
(Bambu Lab A1) pela internet: nome, logo, Instagram, Mercado Livre, loja
própria, parte legal e preço. Material pensado para a primeira temporada de
vendas — o Natal — e para crescer depois dela.

> **Nome recomendado: Camada 3D.** A justificativa, as alternativas e a
> checagem de disponibilidade estão em [`marca/identidade.md`](marca/identidade.md).
> Nada aqui exige o nome: se preferir outro, troque "Camada 3D" nos textos e
> gere o logo de novo com o script indicado lá.

---

## Comece por aqui (ordem importa)

| Ordem | Arquivo | O que fazer |
|---|---|---|
| 1 | [`marca/identidade.md`](marca/identidade.md) | Confirmar o nome, checar @ e domínio, conhecer cores e fontes |
| 2 | [`marca/logo/`](marca/logo/) | Logo em SVG e PNG (perfil, capas de destaque, banner) prontos para uso |
| 3 | [`juridico-financeiro/mei-nota-e-precos.md`](juridico-financeiro/mei-nota-e-precos.md) | Abrir o CNPJ, entender nota fiscal e definir preço |
| 4 | [`catalogo-inicial.md`](catalogo-inicial.md) | Os 6 produtos de largada, com preço sugerido |
| 5 | [`instagram/perfil-e-lancamento.md`](instagram/perfil-e-lancamento.md) | Montar o perfil e publicar os 9 primeiros posts |
| 6 | [`mercado-livre/guia-de-anuncios.md`](mercado-livre/guia-de-anuncios.md) | Cadastrar a conta e publicar os anúncios |
| 7 | [`loja-propria/guia.md`](loja-propria/guia.md) + [`site/`](site/) | Publicar o site (catálogo + pedido pelo WhatsApp) |
| 8 | [`checklist-lancamento.md`](checklist-lancamento.md) | Plano de 30 dias, dia a dia |

---

## A lógica do negócio

```
INSTAGRAM       → mostra o produto pronto e o processo (confiança + desejo)
MERCADO LIVRE   → captura quem já está procurando "presente personalizado"
SITE + WHATSAPP → fecha o pedido personalizado (nomes, cores, prazo)
```

Produto personalizado não se vende só com botão "comprar": a pessoa quer
confirmar o nome, a cor e a data de entrega. Por isso o WhatsApp é o caixa
da loja nesta fase, e o site existe para organizar o pedido antes da
conversa.

**O que vende em 3D hoje:** personalização (nome, data, frase) e prazo
curto. Ninguém compra um vaso impresso porque é impresso; compra porque tem
o nome do filho e chega antes do Natal.

---

## Cuidados que evitam problema

- **Fonte Impact:** a árvore de nomes usa a Impact, que é fonte da
  Microsoft e não pode ser redistribuída. Para produto vendido, use uma
  fonte com licença livre para uso comercial (Oswald, Anton e Bebas Neue,
  todas no Google Fonts, dão resultado quase igual). O `gerar.py` já aceita
  qualquer `.ttf`.
- **Personagens e marcas** (Disney, times de futebol, Pokémon, logos): não
  venda sem licença. É a causa mais comum de anúncio derrubado e conta
  suspensa no Mercado Livre.
- **Brinquedo para menor de 14 anos** exige certificação do Inmetro. Venda
  como "peça decorativa" e diga isso no anúncio; não anuncie como brinquedo.
- **Modelos de terceiros** (Thingiverse, Printables, MakerWorld): confira a
  licença. "CC BY-NC" proíbe venda. Prefira modelos próprios, como a árvore.
- **Prazo:** personalizado atrasa. Prometa sempre 2 dias a mais do que o
  cálculo e entregue antes.

---

## Estrutura

```
loja-3d/
├── README.md                          # este arquivo
├── catalogo-inicial.md                # 6 produtos de largada, preço, tempo, filamento
├── checklist-lancamento.md            # 30 dias, dia a dia
├── marca/
│   ├── identidade.md                  # nome, tagline, cores, fontes, tom de voz, uso do logo
│   └── logo/                          # SVG (vetor) + png/ (perfil, capas, banner)
├── instagram/
│   └── perfil-e-lancamento.md         # @, bio, destaques, 9 primeiros posts, rotina
├── mercado-livre/
│   └── guia-de-anuncios.md            # conta, anúncio, título, fotos, ficha, personalização, frete
├── loja-propria/
│   └── guia.md                        # fase 1 (site + WhatsApp) e fase 2 (Nuvemshop)
├── juridico-financeiro/
│   ├── mei-nota-e-precos.md           # MEI, CNAE, DAS, nota fiscal, fórmula de preço
│   └── calculadora_preco.py           # calcula preço mínimo a partir de gramas e horas
└── site/
    └── index.html                     # catálogo com pedido pelo WhatsApp (arquivo único)
```
