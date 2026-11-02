# Laço 3D — kit de abertura da loja

Tudo o que precisa existir para o estúdio de impressão 3D da sua esposa
vender pela internet: nome, logo, Instagram, Mercado Livre, site com pedido
pelo WhatsApp, CNPJ e preço. **Ela faz tudo em impressão 3D**, então a marca
é um estúdio, não uma loja de um produto só. Três frentes:

- **Presentes e datas comemorativas:** lembrancinhas de Dia das Mães,
  Páscoa, Natal, aniversário, casamento, chá de bebê, batizado.
- **Empresas e eventos:** brindes em quantidade (chaveiros com logo,
  porta-crachás, lembranças de evento, kits para feiras).
- **Decoração, utilidades e sob encomenda:** vasos, organizadores,
  suportes, peças de reposição e **impressão do arquivo do cliente**
  (quem já tem o modelo 3D e só precisa de quem imprima).

> **Nome recomendado: Laço 3D.** Justificativa, alternativas (inclusive com
> o nome dela) e checagem de disponibilidade em [`marca/identidade.md`](marca/identidade.md).
> Para trocar o nome, basta rodar o script do logo de novo e substituir
> "Laço 3D" nos textos.

Onde aparecer `{{NOME}}` nos textos, coloque o nome dela.

---

## Comece por aqui

| Ordem | Arquivo | O que fazer |
|---|---|---|
| 1 | [`marca/identidade.md`](marca/identidade.md) | Confirmar o nome, checar @ e domínio, conhecer cores e fontes |
| 2 | [`marca/logo/`](marca/logo/) | Logo em SVG e PNG (perfil, capas de destaque, banner), prontos |
| 3 | [`juridico-financeiro/mei-nota-e-precos.md`](juridico-financeiro/mei-nota-e-precos.md) | Abrir o CNPJ dela, nota fiscal e fórmula de preço (varejo e atacado) |
| 4 | [`catalogo-natal-2026.md`](catalogo-natal-2026.md) | **Agora:** os 14 produtos de Natal reais, preço por canal, kits, anúncios e posts |
| 4b | [`catalogo-inicial.md`](catalogo-inicial.md) | Catálogo do ano: presentes, brindes, decoração e utilidades, sob encomenda |
| 5 | [`instagram/perfil-e-lancamento.md`](instagram/perfil-e-lancamento.md) | Montar o perfil e publicar os 9 primeiros posts |
| 6 | [`mercado-livre/guia-de-anuncios.md`](mercado-livre/guia-de-anuncios.md) | Cadastrar e publicar os anúncios de varejo |
| 7 | [`loja-propria/guia.md`](loja-propria/guia.md) + [`site/`](site/) | Publicar o site (presentes + orçamento para empresas) |
| 8 | [`checklist-lancamento.md`](checklist-lancamento.md) | Plano de 30 dias |

---

## A lógica do negócio

```
INSTAGRAM        → mostra o produto pronto e o processo (desejo + confiança)
MERCADO LIVRE    → captura quem já procura "lembrancinha", "vaso 3d", "organizador"
SITE + WHATSAPP  → fecha pedido personalizado, orçamento de empresa e arquivo do cliente
GOOGLE           → "impressão 3d perto de mim": empresa, estudante, quem tem um arquivo
```

Os dois públicos compram a mesma coisa (uma peça com nome ou logo), mas de
jeitos diferentes: pessoa física decide em minutos e quer prazo e preço na
hora; empresa pede orçamento, compara e compra em quantidade com nota
fiscal. O site tem um caminho para cada um e o WhatsApp recebe os dois.

**O que vende em 3D hoje:** personalização (nome, data, logo) e prazo
curto. Ninguém compra um chaveiro porque é impresso em 3D; compra porque
tem o nome da afilhada e chega antes do batizado.

---

## Cuidados que evitam problema

- **Personagens e marcas de terceiros** (Disney, times, Stitch, Pokémon):
  não venda sem licença. É a causa mais comum de anúncio derrubado e conta
  suspensa no Mercado Livre. O **logo do cliente** em brinde corporativo
  pode: ele é dono do logo e está encomendando.
- **Brinquedo para menor de 14 anos** exige certificação do Inmetro. Venda
  como "peça decorativa" ou "lembrancinha" e escreva isso no anúncio.
- **Modelos baixados** (Thingiverse, Printables, MakerWorld): confira a
  licença. "CC BY-NC" proíbe venda. Modelos próprios ou com licença
  comercial.
- **Fontes nas peças:** use fontes com licença livre para uso comercial
  (Google Fonts). Fontes do Windows (Impact, Arial) não podem ser usadas em
  produto vendido.
- **Prazo:** personalizado atrasa. Prometa 2 dias a mais do que o cálculo e
  entregue antes.
- **Alimentos:** PLA comum não é certificado para contato com alimento.
  Topo de bolo vai no palito, fora do bolo; forminha e carimbo de biscoito
  só com filamento certificado.

---

## Estrutura

```
loja-3d/
├── README.md
├── catalogo-natal-2026.md             # Natal: 14 produtos reais, preço por canal, kits, anúncios, posts
├── catalogo-inicial.md                # presentes, brindes, decoração/utilidades e sob encomenda
├── checklist-lancamento.md            # 30 dias, dia a dia
├── marca/
│   ├── identidade.md                  # nome, alternativas, cores, fontes, tom de voz, uso do logo
│   ├── gerar_logo.py                  # regenera o logo com outro nome ou fonte
│   └── logo/                          # SVG + png/ (perfil, 6 capas de destaque, banner)
├── instagram/perfil-e-lancamento.md   # @, bio, destaques, 9 posts, rotina, anúncio pago
├── mercado-livre/guia-de-anuncios.md  # conta, taxas, títulos, fotos, ficha, personalização, envio
├── loja-propria/guia.md               # site + WhatsApp agora, Nuvemshop depois, Google e LinkedIn p/ empresas
├── juridico-financeiro/
│   ├── mei-nota-e-precos.md           # MEI, CNAE, DAS, nota fiscal, preço varejo e tabela por quantidade
│   └── calculadora_preco.py           # preço mínimo a partir de gramas, horas e quantidade
└── site/index.html                    # página: presentes, empresas e sob encomenda, pedido pelo WhatsApp
```
