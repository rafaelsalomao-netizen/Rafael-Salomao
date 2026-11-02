# Jurídico e financeiro — CNPJ, nota fiscal e preço

> Valores de impostos, limites e taxas mudam todo ano. Os números abaixo
> são referência para saber o que perguntar; confirme no Portal do
> Empreendedor (gov.br) e com um contador antes de decidir.

## 1. Qual CNPJ abrir (no nome dela)

### MEI (Microempreendedor Individual): o caminho normal

- Faturamento até **R$ 81 mil/ano** (há proposta para aumentar; confira o
  limite vigente). Dá para uma impressora o ano inteiro.
- Imposto fixo mensal (**DAS**) de cerca de **R$ 80 a 85** para indústria e
  comércio (5% do salário mínimo + R$ 1 de ICMS). Inclui INSS dela.
- Abertura gratuita, on-line, em 20 minutos: `gov.br/mei` → Formalize-se,
  com a conta gov.br **dela**.
- Pode ter **1 empregado**.
- Sem contador obrigatório; a declaração anual (DASN-SIMEI) vai até 31/05.

**Ocupação / CNAE para impressão 3D:**

| Papel | Ocupação no MEI | CNAE |
|---|---|---|
| Principal | Fabricante de produtos de material plástico para uso pessoal e doméstico, sob encomenda ou não | 2229-3/01 |
| Secundária | Comerciante de artigos de armarinho / de presentes, conforme a lista vigente | — |

A lista de ocupações permitidas muda; confira em "Ocupações permitidas" no
Portal do Empreendedor e escolha a que descreve "fabricante de artefatos de
plástico". É o enquadramento usado pela maioria das lojas de impressão 3D.

### Quando o MEI **não** é permitido

Ela **não pode ser MEI** se já for **sócia, titular ou administradora de
outra empresa**, ou se for servidora pública federal (estadual e municipal
dependem do estatuto). Se for o caso, alternativas:

1. **Abrir uma ME no Simples Nacional** (Anexo II, indústria): imposto a
   partir de ~4,5% do faturamento, exige contador (R$ 150 a 400/mês).
2. **Incluir o CNAE em uma empresa já existente** da família, se houver
   (um contador faz em uma semana). Nesse caso, a loja fatura pelo CNPJ
   dessa empresa.

Não abra MEI "para ver se passa": a Receita cancela e cobra retroativo.

### Endereço

MEI pode usar o endereço residencial. Confira se o condomínio e a
prefeitura permitem atividade leve em casa (impressora 3D não faz barulho
nem lixo relevante; costuma passar como "fabricação artesanal"). O Portal
do Empreendedor emite a dispensa de alvará em muitas cidades.

## 2. Nota fiscal

| Venda para | Precisa emitir? | Como |
|---|---|---|
| Pessoa física | MEI não é obrigado, mas **emita sempre**: o Mercado Livre pede e o cliente confia mais | NF-e de produto pelo emissor gratuito da Sefaz do estado, ou pelo **emissor nacional do MEI** (gov.br) quando o estado aceitar NF-e de produto por lá |
| Empresa (brindes) | **Obrigatório**, sempre. Empresa não compra sem nota | Mesmo emissor. Peça CNPJ, razão social e endereço no orçamento |
| Mercado Livre | Exige nota para alguns serviços e para a Loja Oficial; emita em todas | Bling ou Tiny (planos a partir de poucas dezenas de reais) integram e emitem automaticamente |

Para NF-e de produto, é preciso **Inscrição Estadual** (o MEI indústria/
comércio recebe no cadastro) e **certificado digital A1** (R$ 150 a
200/ano) ou o emissor gratuito do estado.

Guarde as notas de compra de filamento e embalagem: comprovam o custo e
vão na declaração anual.

## 3. Conta bancária e pagamento

- Conta **PJ gratuita** (Inter, Nubank PJ, C6, Mercado Pago), separada da
  pessoal.
- Varejo: **Pix** (grátis) e **link do Mercado Pago** (~4% a 5% no cartão à
  vista; até 12× para o cliente).
- Empresa: Pix ou **boleto** com nota fiscal. 50% na aprovação da prova e
  50% na entrega, para lotes acima de R$ 1.000.
- No Mercado Livre o dinheiro cai no Mercado Pago. Deixe 10% como reserva
  para devolução e saque o resto para a conta PJ toda semana.

## 4. Preço: a fórmula

```
CUSTO = (filamento + energia + desgaste da máquina) × 1,10 (falhas)
        + hora de trabalho dela + embalagem

PREÇO MÍNIMO = (CUSTO × 1,40 + custo fixo da plataforma + frete que você paga)
               ÷ (1 − comissão da plataforma)
```

A comissão do Mercado Livre incide sobre o **preço final**, por isso divide
por (1 − comissão) em vez de somar a porcentagem.

Rode a calculadora com os números reais (edite os parâmetros no começo do
arquivo):

```bash
python3 juridico-financeiro/calculadora_preco.py 8 0.42 6           # chaveiro, varejo
python3 juridico-financeiro/calculadora_preco.py 7 0.33 4 --qtd 50  # 50 chaveiros com logo
```

### Exemplo 1: chaveiro de nome, varejo

| Item | Valor |
|---|---|
| Filamento (8 g) | R$ 0,88 |
| Energia e máquina (25 min) | R$ 0,60 |
| Falhas (10%) | R$ 0,15 |
| Trabalho (6 min: trocar cor, limpar, colocar argola, embalar) | R$ 3,50 |
| Embalagem (saquinho + fita + envelope) | R$ 6,50 |
| **Custo** | **R$ 11,63** |
| Mínimo no site (cliente paga frete) | R$ 16,96 |
| Mínimo no Mercado Livre Clássico (13% + custo fixo R$ 6,50) | R$ 26,19 |

Conclusão: chaveiro avulso no Mercado Livre não compensa; venda **kit de
3 por R$ 49** (o custo fixo dilui e o frete é um só). No site e no
Instagram, R$ 19,90 avulso funciona.

### Exemplo 2: 50 chaveiros com logo para empresa

| Item | Valor por unidade |
|---|---|
| Filamento (7 g) | R$ 0,77 |
| Energia e máquina (20 min) | R$ 0,48 |
| Falhas | R$ 0,13 |
| Trabalho (4 min × fator de lote 0,45) | R$ 1,05 |
| Embalagem (saquinho individual + caixa dividida por 50) | R$ 2,58 |
| **Custo** | **R$ 5,01** |
| Preço mínimo (Pix/boleto, frete à parte) | R$ 7,01 |
| **Preço de tabela sugerido** | **R$ 12,90/un** (R$ 645 o lote) |

O lote ocupa cerca de 17 horas de impressora: menos de um dia. Brinde para
empresa é o que melhor remunera a hora da máquina; por isso o site tem um
caminho só para isso.

### Regras de preço

- **Mesmo preço de varejo em todos os canais.** Diferencie com brinde ou
  frete, não com desconto no site.
- **Tabela por quantidade** para empresas (20 / 50 / 100) publicada no site:
  evita negociar do zero a cada orçamento.
- Kits diluem a taxa fixa do Mercado Livre e são o formato natural de lembrancinha.
- Reajuste quando a impressora passar de 70% de ocupação. Fila cheia é
  sinal de preço baixo.
- Guarde **10% de cada venda** para filamento e manutenção e **10%** para
  imposto e reserva de devolução.

## 5. Obrigações mensais (1 hora por mês)

- [ ] Pagar o DAS até o dia 20
- [ ] Emitir as notas das vendas do mês (ou conferir a integração)
- [ ] Separar notas de compra de filamento e embalagem
- [ ] Planilha: data, canal, produto, quantidade, valor, taxa, frete
- [ ] Até 31/05: declaração anual do MEI (DASN-SIMEI)
