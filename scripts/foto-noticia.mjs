// Otimiza a foto de uma notícia (AVIF e WebP em dois tamanhos). Uso: npm run foto-noticia -- caminho/da/foto.jpg nome-da-noticia
// Depois, no arquivo da notícia, acrescente: foto: nome-da-noticia, fotoW e fotoH (impressos aqui), e fotoAlt.
import sharp from 'sharp';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

const [origem, nome] = process.argv.slice(2);
if (!origem || !nome) {
  console.error('Uso: npm run foto-noticia -- caminho/da/foto.jpg nome-da-noticia');
  process.exit(1);
}
const out = join(process.cwd(), 'public', 'img', 'noticias');
mkdirSync(out, { recursive: true });

const meta = await sharp(origem).rotate().metadata();
const larguras = [640, 1200].filter((w) => w <= (meta.width ?? 1200)).concat(meta.width && meta.width < 640 ? [meta.width] : []);
const maior = larguras[larguras.length - 1];
for (const w of larguras) {
  const base = sharp(origem).rotate().resize({ width: w, withoutEnlargement: true });
  await base.clone().avif({ quality: 58, effort: 5 }).toFile(join(out, `${nome}-${w}.avif`));
  await base.clone().webp({ quality: 82 }).toFile(join(out, `${nome}-${w}.webp`));
}
const altura = Math.round(((meta.height ?? 1) * maior) / (meta.width ?? 1));
console.log(`Pronto. No arquivo da notícia, acrescente:\nfoto: ${nome}\nfotoW: ${maior}\nfotoH: ${altura}\nfotoAlt: "Descreva a foto em uma frase"`);
