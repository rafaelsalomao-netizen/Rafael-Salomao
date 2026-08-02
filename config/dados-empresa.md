# Dados da Empresa — preencha aqui primeiro

> **Este é o único arquivo que você precisa editar.** Todo o kit usa os marcadores
> abaixo (no formato `{{MARCADOR}}`). Preencha a coluna "Seu dado" e depois é só
> substituir nos textos — ou usar o comando de substituição no final desta página.

| Marcador | O que é | Seu dado |
|---|---|---|
| `{{EMPRESA}}` | Nome da empresa de síndico profissional | _(ex.: Salomão Gestão Condominial)_ |
| `{{RESPONSAVEL}}` | Nome do síndico/sócio que aparece nos vídeos | |
| `{{CIDADE}}` | Cidade principal de atuação | |
| `{{REGIAO}}` | Bairros/regiões atendidas | _(ex.: Zona Sul, ABC e Alphaville)_ |
| `{{WHATSAPP}}` | WhatsApp comercial com DDD | |
| `{{LINK_WHATSAPP}}` | Link direto (wa.me/55DDDNUMERO) | |
| `{{EMAIL}}` | E-mail comercial | |
| `{{INSTAGRAM}}` | @ do perfil | |
| `{{SITE}}` | Site ou link da bio (Linktree, etc.) | |
| `{{ANOS}}` | Anos de experiência | |
| `{{QTD_CONDOMINIOS}}` | Quantos condomínios já administrou | |
| `{{FORMACAO}}` | Formação/certificações relevantes | _(ex.: Administração + curso de Síndico Profissional)_ |
| `{{DIFERENCIAL}}` | Sua promessa central em 1 frase | _(ex.: prestação de contas digital todo dia 5)_ |

---

## Aviso importante sobre promessas numéricas

Vários textos deste kit trazem espaços como `{{DIFERENCIAL}}` ou exemplos de
economia percentual. **Só publique números que você consegue comprovar** com
balancete, contrato ou ata. Propaganda com dado inventado gera problema no
Procon e destrói a confiança justamente do público que decide sua contratação
(conselho fiscal e condôminos). Quando não tiver o número, use a versão
qualitativa da frase — todos os modelos deste kit têm as duas opções.

## Substituição automática (opcional)

Se preferir trocar tudo de uma vez, rode na raiz do projeto:

```bash
# Exemplo: trocando o nome da empresa em todos os arquivos .md
grep -rl '{{EMPRESA}}' . --include='*.md' | xargs sed -i 's/{{EMPRESA}}/Sua Empresa Ltda/g'
```

Repita a linha para cada marcador da tabela.
