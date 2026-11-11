// Cria o arquivo de uma nova notícia. Uso: npm run nova-noticia -- "Título da notícia" [Conquista|Evento|Projeto|Aviso]
import { writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const titulo = process.argv[2];
const tipo = ['Conquista', 'Evento', 'Projeto', 'Aviso'].includes(process.argv[3]) ? process.argv[3] : 'Conquista';
if (!titulo) {
  console.error('Uso: npm run nova-noticia -- "Título da notícia" [Conquista|Evento|Projeto|Aviso]');
  process.exit(1);
}

const slug = titulo
  .normalize('NFD').replace(/[̀-ͯ]/g, '')
  .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
  .slice(0, 60);
const dir = join(process.cwd(), 'src', 'content', 'noticias');
mkdirSync(dir, { recursive: true });
const arquivo = join(dir, `${slug}.md`);
if (existsSync(arquivo)) {
  console.error(`Já existe: ${arquivo}`);
  process.exit(1);
}

const hoje = new Date().toISOString().slice(0, 10);
const texto = `---
titulo: "${titulo.replace(/"/g, '\\"')}"
data: ${hoje}
tipo: ${tipo}
resumo: "Escreva aqui uma frase curta (até 180 caracteres) que resume a notícia."
destaque: false
rascunho: true
---

Escreva a notícia aqui, em Markdown. Quando terminar, troque \`rascunho: true\` por \`rascunho: false\`.

## Subtítulo (opcional)

Parágrafos, **negrito**, *itálico* e [links](https://exemplo.com) funcionam.
`;
writeFileSync(arquivo, texto, 'utf8');
console.log(`Criada: src/content/noticias/${slug}.md\nEdite o texto, ajuste a data e troque "rascunho: true" por "rascunho: false" para publicar.`);
