# Loja própria — do site ao carrinho

## Fase 1 (agora): site com dois caminhos + WhatsApp

Pronto em [`../site/index.html`](../site/index.html). Arquivo único, sem
servidor, sem mensalidade. Tem dois caminhos:

- **Quero um presente:** escolhe o produto, digita nomes, cores e data, e o
  site abre o WhatsApp com o pedido formatado.
- **Sou empresa:** informa produto, quantidade, prazo e se tem o logo em
  arquivo, e o site abre o WhatsApp com o pedido de orçamento formatado.
- **Tenho um arquivo / peça sob medida:** descreve a peça, se tem o
  arquivo, material e cor, e o site abre o WhatsApp pedindo o orçamento (o
  arquivo vai na própria conversa).

Por que começar assim e não com carrinho:

- Personalizado precisa de confirmação (nome certo, cor, prazo) e empresa
  precisa de orçamento. A conversa acontece de qualquer jeito; o site só
  organiza o que chega.
- Zero custo fixo e zero dado pessoal guardado.
- Pagamento por **Pix ou link do Mercado Pago** no WhatsApp (até 12×).
  Para empresas, Pix ou boleto com nota fiscal.

### Publicar (15 minutos)

1. Abra `site/index.html` e edite o bloco `DADOS` no fim do arquivo:
   WhatsApp, nome dela, e-mail, @ do Instagram, link do Mercado Livre,
   cidade, CNPJ, prazo.
2. Fotos: crie a pasta `site/img/` e salve uma foto quadrada por produto
   (1200×1200, abaixo de 300 KB). Preencha o campo `img` de cada produto no
   bloco `PRODUTOS`. Sem foto, o site mostra um fundo de cor com o nome.
3. Publique: **GitHub Pages** (grátis: Settings → Pages → pasta do site)
   ou **Netlify** (grátis, aceita domínio próprio: arraste a pasta `site/`).
4. Aponte `laco3d.com.br` para a hospedagem (Registro.br → DNS).
5. Teste os dois formulários no celular.

## Fase 2 (acima de 30 pedidos/mês): plataforma com carrinho

| Plataforma | Custo aproximado | Prós | Contras |
|---|---|---|---|
| **Nuvemshop** | Plano de entrada barato + taxa por venda | Brasileira; integra Mercado Livre, Instagram Shopping, Correios e Melhor Envio; campo de observação no produto | Personalização avançada exige app pago |
| **Loja Integrada** | Plano gratuito com limite de produtos | Começa sem custo | Recursos limitados no grátis |
| **Shopify** | Mensalidade em dólar | Melhores apps de personalização | Caro para o faturamento inicial |

Recomendação: **Nuvemshop**, pela integração com Mercado Livre e Instagram.
Valores mudam; confira antes de assinar.

O que configurar:

- Campo obrigatório **"Nomes e cores"** em cada produto.
- Prazo de produção visível na página do produto e no e-mail.
- Frete: Correios via **Melhor Envio** + "retirar em mãos" se fizer sentido.
- Pagamento: Mercado Pago ou Pagar.me (Pix com 5% de desconto, cartão até 6×).
- Página "Para empresas" com tabela por quantidade e formulário de orçamento.
- Política: personalizado não tem arrependimento após prévia aprovada,
  **exceto defeito**. Escrito antes da compra (Código de Defesa do
  Consumidor, art. 49, vale para compra on-line; a prévia aprovada é a
  proteção).

## Canais para empresas (sem custo)

- **Perfil da Empresa no Google** (antigo Google Meu Negócio): gratuito e
  o canal mais importante para "faz de tudo". Categoria principal
  **"Serviço de impressão 3D"**, secundárias "Loja de brindes" e "Loja de
  presentes". Descrição com "impressão 3D", "brindes personalizados",
  "lembrancinhas", "peças sob encomenda" e a cidade. É onde aparecem
  "impressão 3d perto de mim" e "brindes personalizados perto de mim".
- **LinkedIn** pessoal dela: um post por semana mostrando um lote de
  brindes com logo (com autorização do cliente). Público de RH e marketing
  está lá.
- **Página "Para empresas" em PDF** (exporte a seção do site ou monte no
  Canva com a tabela do `catalogo-inicial.md`) para mandar no WhatsApp.
- **Parcerias:** buffets, cerimonialistas, decoradoras de festa, escolas e
  agências de marketing indicam lembrancinha e brinde o tempo todo. Deixe um
  kit de amostra com cada um.

## WhatsApp Business (semana 1)

- Número separado do pessoal.
- Catálogo com os produtos, etiquetas "orçamento / produzindo / enviado".
- Respostas rápidas: `/prazo`, `/cores`, `/pagamento`, `/empresas` (tabela por quantidade).
- Mensagem de ausência com o horário de atendimento.

## Domínio e e-mail

- `laco3d.com.br` no Registro.br.
- `contato@laco3d.com.br`: Zoho Mail tem plano gratuito para um domínio.
  Use esse e-mail no Mercado Livre, no Instagram e no Google para separar da
  vida pessoal.
