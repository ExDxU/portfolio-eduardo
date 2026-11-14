// Otimiza a foto de uma notícia (AVIF e WebP em dois tamanhos). Uso: npm run foto-noticia -- caminho/da/foto.jpg nome-da-noticia
// Também serve projetos e certificados: `npm run foto-projeto -- print.png mini-rag` e `npm run foto-certificado -- cert.png cs50x`.
// Depois, no arquivo da notícia, acrescente: foto: nome-da-noticia, fotoW e fotoH (impressos aqui), e fotoAlt.
import sharp from 'sharp';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

const args = process.argv.slice(2);
const pasta = (args.find((a) => a.startsWith('--pasta=')) ?? '--pasta=noticias').split('=')[1];
const [origem, nome] = args.filter((a) => !a.startsWith('--'));
if (!origem || !nome) {
  console.error('Uso: npm run foto-noticia -- caminho/da/foto.jpg nome-da-noticia');
  process.exit(1);
}
const out = join(process.cwd(), 'public', 'img', pasta);
mkdirSync(out, { recursive: true });

const meta = await sharp(origem).rotate().metadata();
// 640 e 1200; se a imagem é menor que 1200, a maior versão é a largura original
const larguras = [640, 1200].filter((w) => w <= (meta.width ?? 1200)).concat(meta.width && meta.width < 1200 && meta.width !== 640 ? [meta.width] : []).sort((a, b) => a - b);
const maior = larguras[larguras.length - 1];
for (const w of larguras) {
  const base = sharp(origem).rotate().resize({ width: w, withoutEnlargement: true });
  await base.clone().avif({ quality: 58, effort: 5 }).toFile(join(out, `${nome}-${w}.avif`));
  await base.clone().webp({ quality: 82 }).toFile(join(out, `${nome}-${w}.webp`));
}
const altura = Math.round(((meta.height ?? 1) * maior) / (meta.width ?? 1));
const campo = pasta === 'noticias' ? 'foto' : 'imagem';
console.log(`Pronto. No arquivo .md, acrescente:
${campo}: ${nome}
${campo}W: ${maior}
${campo}H: ${altura}
${campo}Alt: "Descreva a imagem em uma frase"`);
