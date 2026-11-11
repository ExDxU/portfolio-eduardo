import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Notícias: um arquivo .md por notícia em src/content/noticias/. Para criar: `npm run nova-noticia -- "Título"`.
const noticias = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/noticias' }),
  schema: z.object({
    titulo: z.string().max(90),
    data: z.coerce.date(),
    resumo: z.string().max(180),
    tipo: z.enum(['Conquista', 'Evento', 'Projeto', 'Aviso']),
    destaque: z.boolean().default(false),
    rascunho: z.boolean().default(false),   // true = não aparece no site
    foto: z.string().optional(),            // nome gerado por `npm run foto-noticia`
    fotoW: z.number().optional(),
    fotoH: z.number().optional(),
    fotoAlt: z.string().optional(),
    fotoFoco: z.string().optional(), // ponto de foco do recorte nos cartões, ex.: "50% 80%"
  }),
});

export const collections = { noticias };
