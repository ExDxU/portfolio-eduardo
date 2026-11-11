import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { statSync } from 'node:fs';
import { join } from 'node:path';

// Só URLs finais (sem redirecionamento) e com `lastmod` real: a data da notícia, ou a da última edição do arquivo da página.
// Sem `site` (domínio) em astro.config.mjs, o sitemap sai vazio de propósito: endereços relativos não valem.
const PAGINAS = ['', 'sobre', 'servicos', 'videos', 'academico', 'noticias'];

const dia = (d: Date) => d.toISOString().slice(0, 10);

export const GET: APIRoute = async ({ site }) => {
  const itens: { loc: string; lastmod: string }[] = [];
  if (site) {
    const raiz = process.cwd();
    for (const p of PAGINAS) {
      const arquivo = p === '' ? 'index.astro' : p === 'noticias' ? join('noticias', 'index.astro') : `${p}.astro`;
      let mod = new Date();
      try { mod = statSync(join(raiz, 'src', 'pages', arquivo)).mtime; } catch { /* mantém a data do build */ }
      itens.push({ loc: new URL(p ? `/${p}` : '/', site).href, lastmod: dia(mod) });
    }
    const noticias = (await getCollection('noticias', ({ data }) => !data.rascunho)).sort((a, b) => +b.data.data - +a.data.data);
    for (const n of noticias) itens.push({ loc: new URL(`/noticias/${n.id}`, site).href, lastmod: dia(n.data.data) });
  }
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${itens
    .map((i) => `  <url><loc>${i.loc}</loc><lastmod>${i.lastmod}</lastmod></url>`)
    .join('\n')}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
