# Site de Eduardo Rivabem

Site-hub pessoal (quem sou, serviços, vídeos, acadêmico e notícias). Feito para ser rápido: páginas estáticas, imagens AVIF/WebP responsivas e pouco JavaScript.

- **Stack:** Astro (estático) + CSS próprio (tokens do `DESIGN.md`), GSAP/ScrollTrigger só na home, Lenis para rolagem suave.
- **Onde está publicado:** ainda não publicado. Domínio pendente.
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

## Imagens
As imagens do site são geradas por scripts a partir dos originais (não versionados): `tools/otimizar.py` (objetos, ícones, retrato) e `tools/capas.py` (capas dos vídeos). Os arquivos têm cache de 1 ano; ao regerar imagens, aumente `V` em `src/data/imagens.ts`.

## Vídeos
Edite o bloco `videos` no topo de `src/pages/videos.astro` (código do Reel e, se quiser, a capa).

## Pendências
- Domínio: ao registrar, definir `site` em `astro.config.mjs` e então gerar canonical, sitemap, robots.txt e o JSON-LD.
- Currículo em PDF (botão "Baixar currículo").
- Datas das conquistas em `src/pages/academico.astro` (campo `quando`).
