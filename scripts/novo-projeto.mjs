// Cria o arquivo de um novo projeto. Uso: npm run novo-projeto -- "Nome do projeto"
import { writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const titulo = process.argv[2];
if (!titulo) {
  console.error('Uso: npm run novo-projeto -- "Nome do projeto"');
  process.exit(1);
}

const slug = titulo
  .normalize('NFD').replace(/[̀-ͯ]/g, '')
  .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
  .slice(0, 60);
const dir = join(process.cwd(), 'src', 'content', 'projetos');
mkdirSync(dir, { recursive: true });
const arquivo = join(dir, `${slug}.md`);
if (existsSync(arquivo)) {
  console.error(`Já existe: ${arquivo}`);
  process.exit(1);
}

const texto = `---
titulo: "${titulo.replace(/"/g, '\\"')}"
resumo: "Uma frase (até 170 caracteres) que diz o que o projeto faz. Aparece no cartão."
ordem: 99            # menor aparece primeiro
destaque: false      # true = cartão grande (use em um só)
tipo: Aplicação web  # etiqueta: Inteligência artificial, Ferramenta, Aplicação web...
contexto: ""         # ex.: Projeto final do CS50P, de Harvard (pode apagar a linha)
stack: [Python]
cor: lime            # cor da capa sem imagem: lime, white, mist ou cobalt
sigla: "${titulo.slice(0, 10).toUpperCase().replace(/"/g, '')}"   # texto grande da capa sem imagem (até 12 letras)
links:
  - rotulo: Código no GitHub
    url: https://github.com/ExDxU/
rascunho: true
---

## O que faz

Explique em poucas frases, para quem não conhece o projeto.

## Como funciona

1. Passo a passo, ou os recursos principais.

## Decisões que tomei

- **Uma decisão.** Por que você escolheu assim.
`;
writeFileSync(arquivo, texto, 'utf8');
console.log(`Criado: src/content/projetos/${slug}.md
Edite o texto e troque "rascunho: true" por "rascunho: false" para publicar.
Para usar um print como capa: npm run foto-projeto -- caminho/do/print.png ${slug}  (e cole no arquivo as linhas que ele imprimir).`);
