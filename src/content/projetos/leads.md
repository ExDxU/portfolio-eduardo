---
titulo: Leads
resumo: Aplicação que mapeia empresas por nicho e região a partir de dados públicos e organiza a prospecção em um funil.
ordem: 3
tipo: Ferramenta
contexto: Uso próprio, para prospecção
stack: [Next.js, SQLite, Drizzle ORM, Dados abertos de CNPJ]
cor: mist
sigla: LEADS
imagem: leads
imagemW: 1200
imagemH: 593
imagemAlt: "Tela de Oportunidades do Leads, com o mapa do Brasil colorido por estado e a lista de cidades de São Paulo"
imagemFoco: left top
---

## O que faz

O Leads é uma aplicação web pessoal para encontrar, em todo o Brasil, empresas que podem precisar de um site. Eu escolho um nicho e uma região, ou aceito uma recomendação, e recebo um cartão para cada empresa. A partir daí trabalho os cartões em um funil, com metas.

## Como funciona

1. **Oportunidades:** a tela inicial mostra combinações de nicho e local, ordenadas e com o motivo da sugestão.
2. **Filtros:** dá para refinar por nicho, estado, cidade, idade da empresa e tipo de contato.
3. **Cartões:** cada empresa vira um cartão com pontuação. Abro, confiro os dados e faço a abordagem.
4. **Funil:** movo o cartão pelas etapas e registro o resultado, com anotações e retornos agendados.

## Como fiz

- Os dados vêm da base pública de CNPJ da Receita Federal, com cobertura nacional por atividade e por município.
- Aplicação em Next.js, com banco SQLite e Drizzle ORM.
- A interface tem lista com painel lateral, atalhos de teclado, funil arrastável e um mapa do Brasil.
- Contatos marcados como "não contatar" ficam fora das abordagens.

O código é privado.
