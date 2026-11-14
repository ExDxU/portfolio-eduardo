---
titulo: Mini RAG das minhas anotações
resumo: Faço perguntas no terminal e recebo respostas tiradas das minhas próprias anotações de aula, com a fonte citada.
ordem: 1
destaque: true
tipo: Inteligência artificial
contexto: Projeto final do CS50P, de Harvard
stack: [Python, scikit-learn, TF-IDF, API do Gemini, pytest]
cor: lime
sigla: RAG
imagem: mini-rag
imagemW: 920
imagemH: 518
imagemAlt: "Trecho do código em Python do mini RAG, com a função que ordena os trechos das anotações por similaridade usando TF-IDF e cosseno"
imagemFoco: left top
links:
  - rotulo: Código no GitHub
    url: https://github.com/ExDxU/Mini-RAG
  - rotulo: Ver demonstração
    url: https://youtube.com/shorts/VCxYGl8mu9w
---

## O que faz

É um programa de linha de comando que responde perguntas usando só as minhas anotações do CS50P, escritas em português. Ele encontra os trechos mais parecidos com a pergunta, envia esses trechos para um modelo de linguagem e devolve a resposta com a indicação de onde cada informação veio.

Essa técnica se chama RAG (geração aumentada por recuperação): em vez de o modelo responder de memória, ele responde com base em documentos que eu forneço.

## Como funciona

1. **Leitura:** carrega as anotações em Markdown e texto.
2. **Divisão em trechos:** separa cada arquivo pelas seções e, quando uma seção é longa, por parágrafos, repetindo um parágrafo entre um trecho e o seguinte para não perder o contexto.
3. **Busca:** transforma a pergunta e os trechos em vetores com TF-IDF e ordena os trechos por similaridade de cosseno. Usei uma lista própria de palavras vazias do português.
4. **Filtro de relevância:** se nenhum trecho passa de uma nota mínima, o programa avisa que a pergunta está fora das anotações e nem chama o modelo.
5. **Resposta:** monta um pedido com os três melhores trechos e instruções para o modelo do Google (Gemini) usar apenas esse material e citar as fontes.

## Decisões que tomei

- **Busca local antes da nuvem.** A busca roda no meu computador e só as perguntas relevantes chegam à API. Pergunta fora do assunto custa zero.
- **Entrada e saída externas isoladas.** Montar o pedido e chamar o modelo são funções separadas. Assim os testes automatizados rodam sem internet e sem gastar cota da API.
- **Avaliação da busca.** Com o comando `--eval`, o programa mede em quantos casos de teste a fonte certa aparece entre os três primeiros resultados.

## Por que este projeto importa para mim

Quero me tornar engenheiro de inteligência artificial, e este foi o projeto em que mais mergulhei até aqui. Ele me fez passar por cada etapa de um sistema de RAG: preparar os dados, recuperar, filtrar, gerar e medir.
