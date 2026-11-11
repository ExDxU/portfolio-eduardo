/** Imagens do site: gerar com `python tools/otimizar.py`. Cada nome existe em /img/<nome>-<largura>.avif e .webp */
/** Versão das imagens. Os arquivos têm cache de 1 ano (immutable): ao regerar imagens, aumente este número. */
export const V = '1';

export interface Img { w: number; h: number; widths: number[] }

export const IMG: Record<string, Img> = {
  'nome-3d': { w: 1800, h: 279, widths: [640, 1100, 1800] },
  'portal-cabeca': { w: 1456, h: 1696, widths: [640, 960, 1456] },
  'portal-sombra': { w: 928, h: 1082, widths: [558, 928] },
  'obj-sobre': { w: 560, h: 572, widths: [320, 560] },
  'obj-servicos': { w: 560, h: 744, widths: [320, 560] },
  'obj-videos': { w: 420, h: 750, widths: [240, 420] },
  'obj-academico': { w: 680, h: 464, widths: [380, 680] },
  'obj-noticias': { w: 680, h: 580, widths: [380, 680] },
  'ico-foguete': { w: 360, h: 447, widths: [220, 360] },
  'ico-carinha': { w: 360, h: 358, widths: [220, 360] },
  'ico-notebook': { w: 360, h: 367, widths: [220, 360] },
  'ico-celular': { w: 360, h: 493, widths: [220, 360] },
  'ico-capelo': { w: 360, h: 324, widths: [220, 360] },
  'ico-megafone': { w: 360, h: 396, widths: [220, 360] },
  'ico-estrela': { w: 360, h: 408, widths: [220, 360] },
  'ico-lupa': { w: 360, h: 436, widths: [220, 360] },
  'sobre-terno': { w: 760, h: 1227, widths: [380, 760] },
  'foto-hackathon': { w: 720, h: 483, widths: [420, 720] },
  'capa-dia': { w: 480, h: 854, widths: [320, 480] },
  'capa-deep-research': { w: 480, h: 854, widths: [320, 480] },
  'capa-navier-stokes': { w: 480, h: 854, widths: [320, 480] },
};

export const srcset = (name: string, ext: 'avif' | 'webp') =>
  IMG[name].widths.map((w) => `/img/${name}-${w}.${ext}?v=${V} ${w}w`).join(', ');

export const fallback = (name: string) => `/img/${name}-${IMG[name].widths[IMG[name].widths.length - 1]}.webp?v=${V}`;

/** Imagens de cada página, com o mesmo `sizes` da página. Depois que a página atual carrega, as das outras são baixadas em segundo plano. */
const HERO = '(min-width:701px) 310px, 110px';
export const AQUECER: Record<string, [string, string][]> = {
  '/': [
    ['nome-3d', '(min-width:1700px) 1600px, 84vw'],
    ['portal-cabeca', '(min-width:701px) min(1100px,58vw), min(96vw,640px)'],
    ['portal-sombra', '(min-width:701px) min(1275px,67vw), min(111vw,740px)'],
    ['obj-sobre', HERO], ['obj-servicos', HERO], ['obj-videos', HERO], ['obj-academico', HERO], ['obj-noticias', HERO],
  ],
  '/servicos': [
    ['obj-servicos', '(max-width:820px) 55vw, 340px'], ['ico-estrela', '90px'], ['ico-carinha', '90px'],
    ['ico-notebook', '100px'], ['ico-lupa', '100px'], ['ico-foguete', '100px'], ['ico-celular', '100px'], ['ico-megafone', '100px'],
  ],
  '/videos': [
    ['obj-videos', '(max-width:820px) 40vw, 240px'], ['ico-estrela', '80px'], ['ico-carinha', '80px'],
    ['capa-dia', '(max-width:820px) 45vw, 300px'], ['capa-deep-research', '(max-width:820px) 45vw, 300px'], ['capa-navier-stokes', '(max-width:820px) 45vw, 300px'],
  ],
  '/academico': [
    ['obj-academico', '(max-width:820px) 60vw, 360px'], ['ico-estrela', '180px'],
  ],
  '/noticias': [
    ['obj-noticias', '(max-width:820px) 55vw, 340px'], ['ico-estrela', '80px'],
  ],
  '/sobre': [
    ['sobre-terno', '(max-width:820px) 70vw, 380px'], ['ico-estrela', '180px'], ['ico-notebook', '100px'], ['ico-lupa', '100px'],
    ['foto-hackathon', '(max-width:820px) 92vw, 420px'],
  ],
};
