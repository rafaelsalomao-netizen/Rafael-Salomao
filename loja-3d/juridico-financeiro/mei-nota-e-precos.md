# Jurídico e financeiro — CNPJ, nota fiscal e preço

> Valores de impostos, limites e taxas mudam todo ano. Os números abaixo
> são de referência para você saber o que perguntar; confirme no Portal do
> Empreendedor (gov.br) e com o contador antes de decidir.

## 1. Qual CNPJ abrir

### MEI (Microempreendedor Individual): o caminho normal

- Faturamento até **R$ 81 mil/ano** (há proposta para aumentar; confira o
  limite vigente). Dá para uma impressora rodando o ano inteiro.
- Imposto fixo mensal (**DAS**) de cerca de **R$ 80 a 85** para indústria e
  comércio (5% do salário mínimo + R$ 1 de ICMS). Inclui INSS.
- Abertura gratuita, on-line, em 20 minutos: `gov.br/mei` → Formalize-se.
- Pode ter **1 empregado**.
- Não precisa de contador (mas a declaração anual, DASN-SIMEI, é obrigatória até 31/05).

**Ocupação / CNAE para impressão 3D:**

| Papel | Ocupação no MEI | CNAE |
|---|---|---|
| Principal | Fabricante de produtos de material plástico para uso pessoal e doméstico, sob encomenda ou não | 2229-3/01 |
| Secundária | Comerciante de artigos de armarinho / artigos de decoração (conforme a lista vigente) | — |

A lista de ocupações permitidas no MEI muda; confira em "Ocupações
permitidas" no Portal do Empreendedor e escolha a que descreve "fabricante
de artefatos de plástico". É o enquadramento usado pela maioria das lojas
de impressão 3D.

### Atenção: quando o MEI **não** é permitido

Você **não pode ser MEI** se já for **sócio, titular ou administrador de
outra empresa**. Se a atividade de síndico profissional estiver em uma
Ltda ou se você tiver participação em qualquer CNPJ, as alternativas são:

1. **Adicionar o CNAE 2229-3/01 e um CNAE de comércio varejista à empresa
   existente** (mais simples e barato: um contador faz em uma semana).
2. **Abrir uma ME no Simples Nacional** (Anexo II, indústria): imposto a
   partir de ~4,5% do faturamento, exige contador (R$ 150 a 400/mês).

Pergunte ao contador que já cuida da sua empresa de síndico qual das duas
sai mais barata no seu caso. Não abra MEI "para ver se passa": a Receita
cancela e cobra retroativo.

### Endereço

MEI pode usar o endereço residencial. Confira se o condomínio e a
prefeitura permitem atividade industrial leve em casa (impressora 3D não
faz barulho nem lixo relevante; costuma passar como "fabricação artesanal").
Você precisará do alvará ou da dispensa de alvará da prefeitura, que o
próprio Portal do Empreendedor emite em muitas cidades.

## 2. Nota fiscal

| Venda para | Precisa emitir? | Como |
|---|---|---|
| Pessoa física (cliente final) | MEI não é obrigado, mas **emita sempre**: o Mercado Livre pede e o cliente confia mais | NF-e de produto pelo emissor gratuito da Sefaz do seu estado, ou pelo **emissor nacional do MEI** (gov.br) quando o seu estado já aceitar NF-e de produto por lá |
| Pessoa jurídica (lembrancinha corporativa) | **Obrigatório** | Mesmo emissor |
| Mercado Livre | O Mercado Livre exige nota para alguns serviços de envio e para a Loja Oficial; emita para todas as vendas | Dá para integrar com Bling ou Tiny (planos a partir de poucas dezenas de reais) que emitem a nota automaticamente ao vender |

Para emitir NF-e de produto você precisa de **Inscrição Estadual** (o MEI
indústria/comércio recebe no cadastro) e de **certificado digital A1**
(cerca de R$ 150 a 200/ano) ou do emissor gratuito do estado, que em
alguns estados funciona com senha.

Guarde as notas de compra do filamento e das embalagens: comprovam o
custo e servem para a declaração anual.

## 3. Conta bancária e pagamento

- Conta **PJ gratuita** (Inter, Nubank PJ, C6, Mercado Pago). Nunca misture
  com a conta pessoal: é a primeira coisa que a Receita e o contador olham.
- Receba por **Pix** (grátis) e **link de pagamento do Mercado Pago** (taxa
  aproximada de 4% a 5% no cartão à vista; parcelado em até 12×).
- No Mercado Livre o dinheiro cai no Mercado Pago. Deixe lá 10% como
  reserva para devolução e saque o resto para a conta PJ toda semana.

## 4. Preço: a fórmula

```
CUSTO = (filamento + energia + desgaste da máquina) × 1,10 (falhas)
        + sua hora de trabalho + embalagem

PREÇO MÍNIMO = (CUSTO × 1,40 + custo fixo da plataforma + frete que você paga)
               ÷ (1 − comissão da plataforma)
```

A comissão do Mercado Livre incide sobre o **preço final**, por isso se
divide por (1 − comissão) em vez de somar a porcentagem.

Rode a calculadora com os seus números (edite os parâmetros no começo do
arquivo):

```bash
python3 juridico-financeiro/calculadora_preco.py 200 9 40 --canal ml
```

### Exemplo: árvore de nomes

| Item | Valor |
|---|---|
| Filamento (200 g a R$ 110/kg) | R$ 22,00 |
| Energia (9 h × 0,1 kW × R$ 0,95) | R$ 0,86 |
| Máquina (9 h × R$ 1,33) | R$ 12,00 |
| Falhas (10%) | R$ 3,49 |
| Trabalho (40 min a R$ 35/h: preparar, trocar cor, colar, embalar) | R$ 23,33 |
| Embalagem | R$ 4,50 |
| **Custo** | **R$ 66,18** |
| Preço mínimo no site (Pix/link, cliente paga o frete) | R$ 96,51 |
| Preço mínimo no Mercado Livre Premium (17% + frete grátis ~R$ 22) | R$ 138,13 |

Preço de tabela sugerido: **R$ 149** nos dois canais (no site, o cliente
ganha o frete ou um enfeite de brinde). Vender a R$ 89 "porque o
concorrente vende" dá prejuízo no Mercado Livre e paga R$ 2 por hora de
impressora no site.

### Regras de preço

- **Mesmo preço em todos os canais.** Se o site for mais barato, o Mercado
  Livre vira só vitrine e você paga comissão à toa; se for mais caro, o
  cliente que te achou no Instagram se sente enganado. Diferencie com
  brinde ou frete, não com preço.
- Kits diluem taxa fixa: 4 enfeites por R$ 79 em vez de 1 por R$ 24,90.
- Reajuste quando a impressora passar de 70% de ocupação. Fila cheia é
  sinal de preço baixo.
- Guarde **10% de cada venda** para filamento e manutenção e **outros 10%**
  para o imposto e a reserva de devolução. O que sobra é o que a loja deu.

## 5. Obrigações mensais (cabe em 1 hora por mês)

- [ ] Pagar o DAS até o dia 20
- [ ] Emitir as notas das vendas do mês (ou conferir a integração)
- [ ] Separar notas de compra de filamento e embalagem
- [ ] Anotar faturamento numa planilha simples: data, canal, produto, valor, taxa, frete
- [ ] Até 31/05: declaração anual do MEI (DASN-SIMEI)
