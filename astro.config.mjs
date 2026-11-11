import { defineConfig } from 'astro/config';

// `site` entra quando o domínio for registrado (canonical, sitemap e schema dependem dele).
export default defineConfig({
  output: 'static',
  compressHTML: true,
  build: { inlineStylesheets: 'always' },
  prefetch: { prefetchAll: true, defaultStrategy: 'viewport' },
});
