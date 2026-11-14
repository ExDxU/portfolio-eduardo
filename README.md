# Site de Eduardo Rivabem

Site-hub pessoal, voltado para currículo (projetos, quem sou, acadêmico com certificados, vídeos e notícias). Feito para ser rápido: páginas estáticas, imagens AVIF/WebP responsivas e pouco JavaScript.

- **Stack:** Astro (estático) + CSS próprio (tokens do `DESIGN.md`), GSAP/ScrollTrigger só na home, Lenis para rolagem suave.
- **Onde está publicado:** https://portfolio-eduardo-six.vercel.app (Vercel, deploy a cada push em `main` de `github.com/ExDxU/portfolio-eduardo`). Domínio próprio pendente.
- **Contexto e design:** `PRODUCT.md`, `DESIGN.md`, `BRIEFING.md`, `CONTEUDO.md`.

## Como rodar
```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # gera a pasta dist/
npm run preview  # serve o build final em http://localhost:4321
```

## Publicar uma notícia (pelo seu computador)
```bash
npm run nova-noticia -- "Título da notícia" Conquista   # tipos: Conquista, Evento, Projeto, Aviso
```
1. Abra o arquivo criado em `src/content/noticias/` e escreva o texto em Markdown.
2. Ajuste `data` e `resumo` (até 180 caracteres).
3. Troque `rascunho: true` por `rascunho: false`. Rascunhos não aparecem no site.
4. Foto (opcional): `npm run foto-noticia -- caminho/da/foto.jpg nome-da-noticia` e cole no arquivo os campos que o comando imprimir.
5. `npm run build` e publique a pasta `dist/`.

## Adicionar um projeto
```bash
npm run novo-projeto -- "Nome do projeto"
```
1. Abra o arquivo criado em `src/content/projetos/` e preencha os campos do topo e o texto (é o que aparece na janela do projeto).
2. `ordem` define a posição; `destaque: true` deixa o cartão grande (use em um só).
3. Capa: sem imagem, o cartão usa uma capa com a `sigla` na `cor` escolhida. Para usar um print: `npm run foto-projeto -- caminho/do/print.png nome-do-projeto` e cole no arquivo as linhas impressas.
4. Troque `rascunho: true` por `rascunho: false`.
Link direto para a janela de um projeto: `/projetos#nome-do-arquivo` (ex.: `/projetos#mini-rag`).

## Adicionar um certificado
Crie um arquivo em `src/content/certificados/` (copie um dos existentes) com `titulo`, `instituicao`, `ordem` e, se quiser, `quando` e `link` (verificação).
Imagem: `npm run foto-certificado -- caminho/do/certificado.png nome` e cole no arquivo as linhas impressas. Em PDF, exporte antes a página como PNG. Eles aparecem em `/academico#certificados`.

## Serviços (guardado)
A página de serviços saiu do site em 2026-11-13 e está em `_guardado/servicos.astro` (fora do build). O endereço `/servicos` redireciona para `/projetos` (`vercel.json`). Para voltar: mover o arquivo para `src/pages/`, recolocar no menu (`src/layouts/Base.astro`) e remover o redirect.

## Imagens
As imagens do site são geradas por scripts a partir dos originais (não versionados): `tools/otimizar.py` (objetos, ícones, retrato), `tools/recortar_objeto_branco.py` (recorte de objeto branco sobre fundo claro) e `tools/capas.py` (capas dos vídeos). Os arquivos têm cache de 1 ano; ao regerar imagens, aumente `V` em `src/data/imagens.ts`.

## Vídeos
Edite o bloco `videos` no topo de `src/pages/videos.astro` (código do Reel e, se quiser, a capa).

## Pendências
- Domínio: ao registrar, definir `site` em `astro.config.mjs` (ativa canonical, sitemap, robots.txt e JSON-LD).
- Currículo em PDF (botão "Baixar currículo").
- Datas das conquistas em `src/pages/academico.astro` (campo `quando`).
