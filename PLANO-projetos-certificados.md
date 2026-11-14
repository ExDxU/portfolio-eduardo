# Plano: Projetos, Certificados e saída de Serviços

Escrito em 2026-11-13. **Executado em 2026-11-13** (fases 1 a 7, sem publicar). Pendências no fim do README. Objetivo: deixar o site mais voltado para currículo e recrutadores.
Ao executar, siga as fases na ordem e **pare nos pontos marcados com ⏸** para pedir o que falta ao Eduardo.

---

## Decisões já tomadas (pelo Eduardo)

1. **Serviços sai do site** por enquanto (fica guardado para outra ocasião, não apagado).
2. **A cabeça da home passa a ter 6 objetos:** Sobre mim, Vídeos, Acadêmico, Notícias (já existentes) + **Projetos** + **Certificados**. O foguete (Serviços) sai.
3. **Projetos é o destaque:** é o que recrutadores mais procuram.
4. **Projetos:** cartões; ao clicar, abre uma **janela menor** (como o player da página Vídeos), com imagem no topo e a descrição do projeto em formato próprio. A imagem do topo é a mesma do cartão.
5. **4 projetos:** Habit Tracker (projeto final do CS50x), mini RAG (projeto final do CS50P), Radar e mapeador de Leads.
6. **3 certificados:** CS50x (Introduction to Computer Science), CS50P (Introduction to Programming with Python) e Hackathon do QuintoAndar.
7. **Certificados ficam numa seção dentro da página Acadêmico** (âncora `/academico#certificados`); o objeto de certificado na cabeça leva direto para ela. Decidido em 2026-11-13.
8. **Menu:** Projetos, Sobre mim, Acadêmico, Vídeos, Notícias. Decidido em 2026-11-13.
9. **`/servicos`:** página guardada em `_guardado/` (fora do build) e redirect para `/projetos` no `vercel.json`. Decidido em 2026-11-13.
10. **Cuidado redobrado no recorte das imagens novas** (são predominantemente brancas) e verificação da medalha do objeto do Acadêmico.

## Decisões em aberto

Nenhuma. Todas as decisões de estrutura foram tomadas.

---

## Fase 1: Imagens (⏸ precisa das imagens do Gemini)

Entradas: `assets-brutos/obj-projetos.*` e `assets-brutos/obj-certificados.*` (prompts na seção 9 do `GEMINI-PROMPTS.md`).

1. **Recorte cuidadoso** (objetos majoritariamente brancos sobre cinza claro, o caso mais difícil):
   - Não confiar só em cor: o branco do objeto (~250) e o cinza do fundo (~229 a 240) ficam próximos, e o fundo pode variar nos vãos.
   - Combinar `rembg` (isnet-general-use) para a silhueta com a separação de cor por região usada no letreiro (`tools/recortar_nome_largo.py`): fundo = regiões claras ligadas à borda ou fechadas com tom de fundo; miolo branco preservado.
   - **Auditoria obrigatória:** compor sobre magenta, verde-escuro e o azul do site, ampliar bordas, vãos e áreas brancas internas (moldura da janela, papel do certificado, estrela do selo), contar pixels opacos com cor de fundo (meta: 0) e conferir que nenhuma área branca interna virou buraco.
2. **Medalha do objeto do Acadêmico:** os arquivos exportados estão íntegros (medalha e estrela aparecem em 380 e 680 px). Hipótese: a medalha some na **exibição**, cortada pela borda rasgada da cabeça (o `clip-path` dos objetos) ou escondida por outro objeto. Conferir na home e na página Acadêmico com print; se for o corte, reposicionar o chapéu ou ajustar o recorte. ⏸ Se não reproduzir, pedir ao Eduardo um print de onde viu.
3. Otimizar (AVIF + WebP, 2 tamanhos, sombra assada como os demais), registrar em `src/data/imagens.ts` e em `tools/otimizar.py`.
4. **Imagens dos projetos** (topo do cartão e da janela): ⏸ pedir ao Eduardo prints de cada projeto. Sem print, usar um cartão com o objeto 3D e as cores da paleta (sem inventar tela).

## Fase 2: Retirar Serviços

- `src/layouts/Base.astro`: tirar Serviços do menu; remover o `ProfessionalService` do JSON-LD (fica WebSite + Person).
- `src/pages/index.astro`: tirar o objeto `obj-servicos` e o cartão; atualizar a meta description (hoje cita "serviços").
- `src/pages/sobre.astro`: tirar Serviços da lista `caminhos`; incluir Projetos.
- `src/pages/sitemap.xml.ts`: tirar `servicos` de `PAGINAS`, incluir `projetos`.
- `src/data/imagens.ts`: tirar a rota `/servicos` do `AQUECER`.
- Mover `src/pages/servicos.astro` para `_guardado/servicos.astro` (fora do build) e adicionar redirect no `vercel.json` (decisão 9).
- O WhatsApp só existia em Serviços: some do site junto (contato fica e-mail, LinkedIn e GitHub).
- Varredura final: `grep -ri "servi" src/` para não sobrar link quebrado nem texto.

## Fase 3: Projetos (⏸ precisa das descrições)

1. **Coleção de conteúdo** `src/content/projetos/` (um `.md` por projeto), schema em `src/content.config.ts`:
   `titulo`, `resumo` (cartão), `ordem`, `destaque`, `tipo` (ex.: "IA", "Web", "Ferramenta"), `stack` (lista), `papel`, `ano`, `links` (GitHub, demo, vídeo; todos opcionais), `imagem`, `imagemAlt`, `rascunho`. O corpo em Markdown é o texto da janela.
2. **Página `/projetos`:** hero com o objeto 3D, grade de cartões (imagem, tipo, título, resumo, stack); o projeto `destaque` ocupa mais espaço.
3. **Janela do projeto:** `<dialog>` no mesmo padrão do player de Vídeos (abre com animação, fecha no X, no Esc e clicando fora, foco preso dentro, rolagem interna). Ordem: imagem, título, tipo e ano, resumo, "O que faz", "Como fiz" (stack e decisões), "O que aprendi", links.
   O texto de todos os projetos já vem no HTML da página (não carregado depois), para buscadores e leitores de tela.
   Bônus barato: `/projetos#mini-rag` abre direto a janela daquele projeto (link compartilhável).
4. **Conteúdo** (⏸ pedir ao Eduardo, um por vez, e não inventar nada):
   - **Mini RAG (CS50P)**: projeto em destaque, ligado à jornada de ML/IA. Perguntar: o que faz, como funciona (embeddings, busca, modelo usado), stack, o que aprendeu, link do GitHub.
   - **Habit Tracker (CS50x)**: aplicação web. Pedir a descrição completa e o link.
   - **Radar**: monitora os sites que ele vende, integra com a API do Google Search Console, qualidade e indexação de páginas. Pedir detalhes, stack, print e se o código pode ser público.
   - **Leads**: mapeamento de leads por área. Base no Orquestrador: dados abertos de CNPJ da Receita, cartões, funil, metas, mapa do Brasil, fila do dia, ~757 mil leads na onda 1; stack proposta Next.js + SQLite. **Repositório privado**: confirmar o que pode ser mostrado (sem dados de empresas, sem nomes de leads, sem números internos que ele não queira expor).
   - Ordem sugerida: Mini RAG, Radar, Leads, Habit Tracker (IA primeiro, depois ferramentas reais, depois o projeto de curso). ⏸ confirmar.
5. **Script de apoio** `npm run novo-projeto -- "Título"` (como o de notícias), para ele adicionar projetos sozinho.

## Fase 4: Certificados (⏸ precisa dos arquivos)

1. **Coleção** `src/content/certificados/` (ou um arquivo de dados): `titulo`, `instituicao`, `data`, `linkVerificacao`, `imagem`, `imagemAlt`, `ordem`.
2. **Exibição** na seção "Certificados" da página Acadêmico (decisão 7): cartões com miniatura do certificado, instituição, data e link "Verificar"; clicar abre a imagem grande na mesma janela usada nos projetos.
3. ⏸ Pedir ao Eduardo: imagem ou PDF de cada certificado, datas e links de verificação (o CS50 tem link oficial de verificação). Converter PDF em imagem otimizada; **ocultar dados pessoais** que ele não queira expor (ex.: e-mail, número de identificação).
4. Na lista do Acadêmico, o item "CS50, de Harvard" passa a apontar para os certificados.

## Fase 5: Home e destaque de Projetos

1. **Cabeça com 6 objetos:** Projetos ocupa o lugar de mais destaque (maior, no centro, na frente) no espaço do foguete; Certificados entra no arranjo. Reposicionar os 6 (`x`, `y`, `width`, `rot`) e testar no desktop e no celular (no celular os objetos são menores, cuidado para não amontoar).
2. **Cartões "Quem sou eu?":** Projetos primeiro, com texto voltado para recrutador.
3. **Menu** conforme a decisão 8.
4. Avaliar com o Eduardo (⏸ não fazer sem pedir): uma faixa curta "Projetos em destaque" logo abaixo do hero, com os 2 principais. Dá destaque, mas aumenta a quantidade de informação, que é o receio dele.

## Fase 6: SEO e textos

- Títulos e descriptions de `/projetos`; revisar a description de `/academico` para citar os certificados, seguindo o padrão: tema primeiro, nome no fim, ~60 e ~155 caracteres.
- JSON-LD: tirar `ProfessionalService`; em `/projetos`, opcionalmente um `ItemList` dos projetos. Sem dados inventados.
- `og-image`: o texto atual ("Desenvolvedor de software e criador de conteúdo sobre IA") continua válido.
- Atualizar `README.md`, `PRODUCT.md`, `CONTEUDO.md` (áreas e como adicionar projeto/certificado).

## Fase 7: Verificação final (antes de publicar)

- Build de produção sem erro; nenhuma referência a Serviços (`grep`).
- **Imagens:** auditoria visual das 2 novas e da medalha, na home, na página e nos cartões, no desktop e no celular.
- Janela de projeto: abre, fecha (X, Esc, clique fora), foco correto, rolagem interna no celular, link com `#` abre a janela certa.
- axe-core em todas as páginas (meta: 0 violações); sem rolagem horizontal; peso e LCP medidos em produção local.
- ⏸ Mostrar ao Eduardo e só então commit + push (deploy automático na Vercel) e conferência no ar com `curl`.

## O que pedir ao Eduardo (resumo)

2. As 2 imagens do Gemini.
3. Descrição, stack, links e print de cada projeto (um por vez).
4. Imagem/PDF, data e link de verificação de cada certificado.
5. Se viu a medalha sumir em algum lugar específico, um print.
