import type { APIRoute } from 'astro';

// Com o domínio definido em `site` (astro.config.mjs), aponta para o sitemap.
export const GET: APIRoute = ({ site }) =>
  new Response(`User-agent: *\nAllow: /\n${site ? `\nSitemap: ${new URL('/sitemap.xml', site).href}\n` : ''}`, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
