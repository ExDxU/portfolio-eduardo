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

// Projetos: um arquivo .md por projeto em src/content/projetos/. O corpo do arquivo é o texto da janela do projeto.
const projetos = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/projetos' }),
  schema: z.object({
    titulo: z.string().max(60),
    resumo: z.string().max(170),              // aparece no cartão
    ordem: z.number().default(99),            // menor aparece primeiro
    destaque: z.boolean().default(false),     // cartão maior
    tipo: z.string(),                         // etiqueta: "IA", "Aplicação web", "Ferramenta"...
    contexto: z.string().optional(),          // ex.: "Projeto final do CS50P, de Harvard"
    ano: z.string().optional(),
    stack: z.array(z.string()).default([]),
    cor: z.enum(['lime', 'white', 'mist', 'cobalt']).default('lime'),   // cor da capa quando não há imagem
    sigla: z.string().max(12).optional(),     // texto grande da capa sem imagem
    imagem: z.string().optional(),            // nome gerado por `npm run foto-projeto` (sem extensão)
    imagemW: z.number().optional(),
    imagemH: z.number().optional(),
    imagemAlt: z.string().optional(),
    imagemFoco: z.string().optional(),        // parte da imagem que aparece no cartão, ex.: "left top"
    links: z.array(z.object({ rotulo: z.string(), url: z.string().url() })).default([]),
    rascunho: z.boolean().default(false),
  }),
});

// Certificados: um arquivo .md por certificado em src/content/certificados/ (sem corpo). Aparecem em /academico#certificados.
const certificados = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/certificados' }),
  schema: z.object({
    titulo: z.string().max(80),
    instituicao: z.string(),
    quando: z.string().optional(),            // ex.: "2026"
    ordem: z.number().default(99),
    imagem: z.string().optional(),            // nome gerado por `npm run foto-certificado` (sem extensão)
    imagemW: z.number().optional(),
    imagemH: z.number().optional(),
    imagemAlt: z.string().optional(),
    link: z.string().url().optional(),        // link de verificação
    rascunho: z.boolean().default(false),
  }),
});

export const collections = { noticias, projetos, certificados };
