# Site de captação

Página única, sem dependências externas e sem servidor. Abre direto no navegador
e pode ser hospedada de graça.

É o destino do link da bio do Instagram: o conteúdo traz a pessoa, o site
apresenta o serviço, o formulário abre a conversa no seu WhatsApp.

---

## 1. Preencher os seus dados

Abra `index.html` e edite o bloco `DADOS`, perto do fim do arquivo:

```js
const DADOS = {
  EMPRESA:          "Salomão Gestão Condominial",
  RESPONSAVEL:      "Rafael Salomão",
  CIDADE:           "Santos",
  REGIAO:           "Santos, São Vicente e Praia Grande",
  WHATSAPP:         "13991234567",   // só dígitos, com DDD, sem +55
  EMAIL:            "contato@exemplo.com.br",
  INSTAGRAM:        "seuperfil",     // sem @
  ANOS:             "8",
  QTD_CONDOMINIOS:  "14",
  FORMACAO:         "Administração + Síndico Profissional",
  CNPJ:             "00.000.000/0001-00"
};
```

Esses valores substituem automaticamente todos os marcadores `{{...}}` da página.

**Edite também à mão** as 4 primeiras linhas do `<head>` (`<title>`, `description`
e as duas `og:`). Buscadores leem essas tags antes de rodar o JavaScript, então
vale deixá-las escritas direto no arquivo.

## 2. Revisar antes de publicar

- [ ] **Depoimentos** — a seção traz três blocos marcados como espaço reservado.
      Substitua por depoimentos reais e obtenha **autorização por escrito** antes
      de publicar nome, condomínio ou foto.
- [ ] **Números do topo** — anos, condomínios geridos e "dia 5" precisam ser
      verdadeiros. Se você ainda não fecha as contas todo dia 5, mude a data ou
      troque o item.
- [ ] **"0 comissão de fornecedor"** — só mantenha se for verdade. É o
      diferencial mais forte da página e o mais fácil de checar.
- [ ] **CNPJ** no rodapé.
- [ ] **Teste o WhatsApp no celular** — preencha o formulário e confirme que a
      mensagem chega organizada.

## 3. Publicar

**GitHub Pages** (grátis, sem conta nova):

1. No GitHub: **Settings → Pages**
2. Source: `Deploy from a branch`
3. Branch: a sua branch principal · pasta: `/ (root)`
4. O site fica em `https://<usuario>.github.io/<repo>/site/`

**Netlify ou Vercel** (grátis, aceita domínio próprio):
arraste a pasta `site/` na tela de deploy. Leva um minuto.

**Domínio próprio:** registre no Registro.br (`.com.br` custa cerca de R$ 40/ano)
e aponte para a hospedagem. Um domínio como `sindico<cidade>.com.br` ajuda na
busca local.

---

## Como o formulário funciona

Não existe back-end e nada é armazenado. Ao enviar, o navegador monta uma
mensagem com os campos preenchidos e abre o WhatsApp Web ou o aplicativo com o
texto pronto — a pessoa só aperta enviar.

Vantagens: zero custo, zero manutenção, nenhum dado pessoal guardado (o que
simplifica bastante a sua situação frente à LGPD) e o lead chega já organizado.

Se um dia quiser receber por e-mail em vez do WhatsApp, dá para trocar por
Formspree ou Netlify Forms sem mexer no layout.

---

## Estrutura da página

| Seção | Função |
|---|---|
| Topo | Promessa central + dois CTAs + números de credibilidade |
| 6 sinais | Faz o visitante reconhecer o próprio prédio no problema |
| Serviços | Seis frentes do contrato, sem promessa vaga |
| Como funciona | Os 6 passos, do diagnóstico à rotina mensal |
| Diagnóstico | A oferta principal + formulário → WhatsApp |
| Depoimentos | Prova social (preencher) |
| Dúvidas | 7 perguntas, incluindo preço e comissão de fornecedor |
| Fechamento | Última chamada para o WhatsApp |

A oferta de entrada é o **diagnóstico gratuito**, não a contratação. Ninguém
troca de síndico a partir de um site — troca a partir de uma conversa. O site
existe para fazer essa conversa começar.

---

## Detalhes técnicos

- Arquivo único, sem CDN, sem fontes externas, sem rastreador
- Tema claro e escuro conforme a preferência do visitante
- Responsivo, com botão flutuante de WhatsApp no celular
- Acessível: foco visível no teclado e `prefers-reduced-motion` respeitado
