---
titulo: Radar
resumo: Painel que acompanha os sites que eu entrego, com desempenho no Google, indexação das páginas e saúde técnica.
ordem: 2
tipo: Ferramenta
contexto: Uso próprio, nos sites que desenvolvo
stack: [Next.js, TypeScript, Tailwind CSS, shadcn/ui, Postgres, Drizzle ORM]
cor: cobalt
sigla: RADAR
imagem: radar
imagemW: 1135
imagemH: 793
imagemAlt: "Tela de desempenho do Radar, com impressões, cliques, CTR e posição média de um site e os gráficos por dia"
imagemFoco: center top
---

## O que faz

O Radar é um painel privado em que eu acompanho, num só lugar, os sites que desenvolvo. Para cada site ele reúne:

- **Desempenho no Google**, com dados da API do Google Search Console.
- **Indexação**: quais páginas o Google já indexou e quais ainda não.
- **Check-up técnico** do HTML publicado, para ver a qualidade do que está no ar.
- **Publicações** feitas na Vercel.

## Por que construí

Entregar o site é metade do trabalho. Depois que ele vai ao ar, eu preciso saber se o Google encontrou as páginas e se algo quebrou. Antes eu conferia isso site por site, à mão. O Radar junta tudo.

## Como fiz

- Aplicação em Next.js com TypeScript.
- Interface com Tailwind CSS e shadcn/ui, com tema claro e escuro.
- Login com conta Google, liberado apenas para e-mails autorizados.
- Banco de dados Postgres, acessado com Drizzle ORM.

O código é privado, porque o painel guarda dados dos sites de clientes.
