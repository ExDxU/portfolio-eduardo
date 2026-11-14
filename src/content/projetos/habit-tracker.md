---
titulo: Habit Tracker
resumo: Aplicação web para criar hábitos, marcar o que foi feito e acompanhar a sequência de dias. Feita por mim, da ideia ao código.
ordem: 4
tipo: Aplicação web
contexto: Projeto final do CS50x, de Harvard
stack: [Python, Flask, SQLite, HTML, CSS, Bootstrap 5]
cor: white
sigla: HABIT
imagem: habit-tracker
imagemW: 1200
imagemH: 592
imagemAlt: "Tela Meus Hábitos do Habit Tracker, com a lista de hábitos, a sequência de dias de cada um e os botões Concluir e Excluir"
imagemFoco: center top
links:
  - rotulo: Código no GitHub
    url: https://github.com/ExDxU/Habit-Tracker
  - rotulo: Ver demonstração
    url: https://youtube.com/shorts/3c7CGSrUMyw
---

## O que faz

O Habit Tracker ajuda a criar e manter hábitos diários. A pessoa entra na conta, vê os hábitos do dia, marca como feito com um clique e acompanha a sequência de dias seguidos de cada um.

A ideia foi fugir dos aplicativos cheios de opções: aqui o foco é ser simples e rápido.

Desenvolvi este projeto sozinho, da ideia ao código: as telas em HTML, CSS e Bootstrap, as rotas em Flask e o banco de dados em SQLite.

## Como funciona

- **Contas:** cadastro de novos usuários e login, com a senha guardada de forma criptografada no banco SQLite.
- **Hábitos:** criar, concluir e excluir, cada um ligado à conta de quem criou.
- **Sequência:** o contador de dias seguidos aparece ao lado de cada hábito.

## Decisões que tomei

- **Sequência calculada na hora.** Em vez de guardar um contador no banco, que pode sair de sincronia, a aplicação lê o histórico de conclusões e conta os dias consecutivos a cada consulta. Se o último registro é anterior a ontem, a sequência volta a zero.
- **Sem conclusão em dobro.** Antes de registrar, a aplicação verifica se o hábito já foi concluído no dia. Clicar várias vezes não infla os números.
- **Avisos na própria página.** Erros de preenchimento aparecem como alerta na tela em que a pessoa está, sem levar para uma página de erro separada.
