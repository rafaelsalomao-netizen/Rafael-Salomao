# Loja própria — do site ao carrinho

## Fase 1 (agora): site de catálogo + pedido pelo WhatsApp

Está pronto em [`../site/index.html`](../site/index.html). Arquivo único,
sem servidor, sem mensalidade. O visitante escolhe o produto, digita os
nomes e as cores, e o site abre o WhatsApp com o pedido já formatado.

Por que começar assim e não com carrinho:

- Produto personalizado precisa de confirmação (nome certo, cor, prazo).
  A conversa acontece de qualquer jeito; o site só organiza o que chega.
- Zero custo fixo e zero dado pessoal guardado (sem obrigação adicional de LGPD).
- O pagamento vai por **link do Mercado Pago ou Pix** enviado no WhatsApp.
  Link do Mercado Pago parcela em até 12× e cobre a venda com a garantia deles.

### Publicar (15 minutos)

1. Abra `site/index.html` e edite o bloco `DADOS` no fim do arquivo:
   WhatsApp, e-mail, @ do Instagram, link da loja no Mercado Livre, preços.
2. Troque as imagens dos produtos: a pasta `site/img/` recebe as fotos
   (fundo claro, quadradas, 1200×1200, abaixo de 300 KB cada).
3. Publique:
   - **GitHub Pages** (grátis): Settings → Pages → branch principal → pasta `/loja-3d/site`.
   - **Netlify** (grátis, aceita domínio próprio): arraste a pasta `site/`.
4. Aponte `camada3d.com.br` para a hospedagem (Registro.br → DNS → CNAME).
5. Teste no celular: escolha um produto, preencha e confira a mensagem que
   abre no WhatsApp.

## Fase 2 (quando passar de 30 pedidos/mês): plataforma com carrinho

| Plataforma | Custo aproximado | Prós | Contras |
|---|---|---|---|
| **Nuvemshop** | Plano de entrada barato + taxa por venda; planos mensais a partir de poucas dezenas de reais | Brasileira, integra Mercado Livre, Instagram Shopping, Correios e Melhor Envio; campo de observação no produto | Personalização avançada exige app pago |
| **Loja Integrada** | Plano gratuito com limite de produtos | Boa para começar sem custo | Recursos limitados no grátis |
| **Shopify** | Mensalidade em dólar | Melhor ecossistema de apps de personalização | Caro para o faturamento inicial; checkout em português precisa de ajuste |

Recomendação: **Nuvemshop**, pela integração com Mercado Livre (estoque e
pedidos em um lugar só) e com o Instagram Shopping. Os valores dos planos
mudam; confira no site antes de assinar.

O que configurar na plataforma:

- Campo obrigatório **"Nomes e cores"** em cada produto (campo de
  observação do pedido).
- Prazo de produção visível na página do produto e no e-mail de confirmação.
- Frete: Correios via **Melhor Envio** (desconto sobre o balcão) + opção
  "retirar em mãos" se fizer sentido na sua cidade.
- Pagamento: Mercado Pago ou Pagar.me (Pix com desconto de 5% e cartão até 6×).
- Página "Como funciona a personalização" com os limites (letras por nome,
  cores disponíveis, prévia em 24 h).
- Política de troca: personalizado não tem arrependimento após aprovada a
  prévia, **exceto defeito**. Isso precisa estar escrito antes da compra
  (Código de Defesa do Consumidor, art. 49, vale para compra on-line; a
  prévia aprovada é a sua proteção).

## Instagram Shopping e WhatsApp Business

- **WhatsApp Business** (grátis): catálogo com os 6 produtos, etiquetas
  "orçamento / produzindo / enviado", respostas rápidas para "prazo",
  "cores" e "como pagar". Configure na semana 1.
- **Instagram Shopping**: exige loja em plataforma (fase 2) ou catálogo do
  Facebook. Vale quando houver 20+ produtos; antes, o link da bio basta.

## Domínio e e-mail

- `camada3d.com.br` no Registro.br.
- E-mail `contato@camada3d.com.br`: o Zoho Mail tem plano gratuito para
  um domínio; o Google Workspace é pago. Use esse e-mail no Mercado Livre e
  no Instagram para separar da vida pessoal.
