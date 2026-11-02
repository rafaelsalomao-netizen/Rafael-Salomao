# Identidade da marca

## 1. Nome

### Recomendado: **Camada 3D**

"Camada" é como a impressora constrói a peça (camada por camada) e também
como os nomes da árvore se empilham. É palavra do dia a dia, fácil de
falar, escrever e lembrar, e não prende a loja a um único produto: serve
para Natal, para porta-chaves, para organizador de mesa.

- Tagline: **Seu nome, camada por camada.**
- Descrição curta (bio, Mercado Livre): *Presentes e decoração impressos em 3D, com o seu nome.*
- Uso por escrito: "Camada 3D" (C maiúsculo, espaço, 3D). Nunca "camada3d" em texto corrido.

### Alternativas, caso o @ ou o domínio estejam ocupados

| Nome | Por que funciona | Risco |
|---|---|---|
| **Letra Forte** | Fala direto do produto (letras grossas, nome em destaque) | Limita a linha a produtos com texto |
| **Vértice 3D** | Geométrico, soa técnico e moderno | Mais frio; menos "presente" |
| **Salomão 3D** | Usa o sobrenome, fácil de confiar | Confunde com a marca de síndico profissional |
| **Fôrma & Nome** | Artesanal, ótimo para presentes | Acento e "&" dificultam @ e domínio |

### Checagem de disponibilidade (faça antes de imprimir qualquer coisa)

Não foi possível verificar automaticamente daqui. Confira, nesta ordem:

1. **Instagram:** abra `instagram.com/camada3d` e `instagram.com/camada.3d`. Se um estiver livre, crie a conta no mesmo dia.
2. **Domínio:** `registro.br` → pesquisar `camada3d.com.br` (cerca de R$ 40/ano).
3. **Marca registrada:** `busca.inpi.gov.br` → pesquisar "camada" nas classes **20** (móveis e decoração), **28** (jogos e enfeites de Natal) e **35** (comércio). Se não houver marca idêntica no mesmo ramo, registre: MEI paga taxa reduzida (confira o valor no site do INPI). O registro leva mais de um ano, mas a proteção conta a partir do pedido.
4. **Mercado Livre:** o nome da loja é escolhido no cadastro; repetido não é bloqueado, mas evite igual a um concorrente.

Se `@camada3d` estiver ocupado, a ordem de preferência é `@camada.3d`,
`@camada3d.br`, `@lojacamada3d`.

---

## 2. Cores

A paleta vem do filamento: cores vivas e opacas sobre fundo neutro, como
peça recém-saída da mesa.

| Papel | Nome | Hex | Uso |
|---|---|---|---|
| Base escura | Tinta | `#171A2B` | Texto, fundo do perfil, fundo de banner |
| Destaque principal | Coral | `#FF5A3C` | "3D" do logo, botões, preço, chamadas |
| Destaque secundário | Verde-água | `#119DA4` | Tagline, ícones, detalhes |
| Destaque de apoio | Limão | `#FFD166` | Fundo claro de destaque, selo, Natal (com coral) |
| Fundo claro | Papel | `#F7F7F4` | Fundo de post, site, embalagem |

Regras simples:

- Em cada post, **uma cor de destaque** só. Coral é a padrão.
- Texto sempre em Tinta sobre Papel, ou em Papel sobre Tinta. Nunca texto
  coral sobre verde-água (não dá contraste).
- Natal: coral + limão sobre Tinta. Não use verde-bandeira e vermelho-sangue
  nos posts, mesmo que a peça seja verde e vermelha: a foto já traz essas
  cores, o layout não precisa repetir.

---

## 3. Tipografia

| Papel | Fonte | Onde baixar | Uso |
|---|---|---|---|
| Títulos e logo | **Outfit** (peso 800 e 700) | Google Fonts | Logo, título de post, capa de destaque, títulos do site |
| Texto | **Manrope** (400 e 600) | Google Fonts | Legendas longas em imagem, texto do site, descrição no Mercado Livre |
| Nas peças | Oswald 700 (ou Anton, Bebas Neue) | Google Fonts | Letras impressas em 3D (licença livre para uso comercial) |

Instale Outfit e Manrope no celular/computador para usar no Canva ou no
CapCut e o material fica igual ao logo.

---

## 4. Logo — arquivos e uso

Pasta [`logo/`](logo/). Os SVG têm o texto convertido em curvas (abrem em
qualquer programa sem precisar da fonte).

| Arquivo | Quando usar |
|---|---|
| `camada3d-logo-horizontal.svg` | Padrão: site, banner, etiqueta, nota, cartão |
| `camada3d-logo-horizontal-fundo-escuro.svg` | Sobre fundo Tinta ou foto escura |
| `camada3d-logo-vertical.svg` / `-tagline.svg` | Embalagem, adesivo quadrado, abertura de Reels |
| `camada3d-icone.svg` | Foto de perfil, favicon, marca d'água, selo na embalagem |
| `*-mono-preto.svg` / `*-mono-branco.svg` | Impressão em uma cor, carimbo, gravação, marca d'água em foto |
| `png/perfil-instagram-escuro.png` | Foto de perfil do Instagram e do Mercado Livre (1080×1080) |
| `png/capa-destaque-*.png` | Capas dos 6 destaques do Instagram (1080×1920) |
| `png/banner-loja-1200x300.png` | Banner da loja no Mercado Livre e cabeçalho de e-mail |
| `png/logo-horizontal-2400px.png` | Quando o sistema não aceita SVG (fundo transparente) |

Regras de uso:

- Margem mínima ao redor do logo: a altura do "3D".
- Não estique, não incline, não troque as cores das camadas, não coloque sombra.
- Em foto, use a versão mono branca com 70% de opacidade no canto inferior direito.
- Tamanho mínimo: horizontal com 120 px de largura; abaixo disso use só o ícone.

Para gerar de novo (outro nome ou outra fonte):

```bash
pip install fonttools
python3 gerar_logo.py caminho/Outfit-ExtraBold.ttf loja-3d/marca/logo
```

O script `gerar_logo.py` está na raiz da pasta `marca/`. Edite a linha com
`"CAMADA"` e `"3D"` para trocar o texto.

---

## 5. Tom de voz

Quem compra é presenteador com pressa: pai, mãe, madrinha, namorado(a),
alguém montando lembrancinha de empresa. Fale com essa pessoa.

- **Direto e caloroso.** "Chega em 5 dias úteis" em vez de "prazo estimado conforme disponibilidade".
- **Mostra o processo.** Vídeo da impressora andando vende mais que foto de catálogo. A pessoa quer ver que é feito, e feito para ela.
- **Sem jargão.** Nada de "PLA", "infill", "0,2 mm" na legenda. Isso vai nos destaques "Bastidores", para quem perguntar.
- **Promessa que cumpre.** Prazo, tamanho e cor sempre explícitos. Em personalizado, o problema nunca é o preço: é a expectativa errada.
- Emojis: no máximo um por linha, e só em stories e legendas; nunca em título de anúncio.

Frases que resumem a marca, para usar em bio, embalagem e anúncios:

- Seu nome, camada por camada.
- Feito aqui, um de cada vez.
- Presente que ninguém mais tem, porque tem o nome de quem recebe.
