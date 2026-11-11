<!-- SEED: established with the user before implementation; re-run $impeccable document once there's code to capture the actual tokens and components. -->
---
name: Eduardo Rivabem
description: Mundo azul-cobalto de adesivos retrô, com um portal-retrato que leva às áreas da vida profissional.
colors:
  cobalt: "#0131CD"
  white: "#FFFFFF"
  lime: "#B9FC01"
  cobalt-deep: "#011E80"
  cobalt-night: "#00104A"
  ink: "#060814"
  mist: "#E9EEFF"
  cobalt-soft: "#9DB0F0"
typography:
  display:
    fontFamily: "Archivo, 'Arial Narrow', sans-serif"
    fontWeight: 900
    lineHeight: 0.86
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Instrument Sans, system-ui, sans-serif"
    fontWeight: 600
    lineHeight: 1.02
    letterSpacing: "-0.03em"
  body:
    fontFamily: "Instrument Sans, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  md: "16px"
  lg: "24px"
  xl: "32px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "48px"
  2xl: "96px"
  3xl: "128px"
components:
  button-primary:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "10px 18px"
  button-secondary:
    backgroundColor: "{colors.white}"
    textColor: "{colors.cobalt}"
    rounded: "{rounded.pill}"
    padding: "10px 18px"
  card-service:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "22px"
---

# Design System: Eduardo Rivabem

## Overview
Um mundo azul-cobalto chapado onde tudo é **adesivo**: fotos com borda branca grossa, ícones retrô com contorno escuro e sombra sólida, objetos 3D brilhantes e infláveis. A home é um **portal**: o retrato do Eduardo com o topo da cabeça rasgado, de onde saem cinco objetos, um por área. Energia de cartaz retrô (Slush), lógica de navegação do Trevor Noah, acabamento premium. Movimento em **molas curtas e confiantes**; um único momento "uau" (o portal), o resto do site fala o mesmo vocabulário em volume menor. Referência técnica completa em `design-dna.json`.

## Colors
### Primary
Azul cobalto (cobalt) é o chão do site inteiro. Seções podem inverter para branco, com o azul virando a cor do texto.

### Secondary
Branco (white) é a tinta: tipografia sobre azul, borda dos adesivos, fundo das seções invertidas.

### Tertiary
Verde-limão (lime) é a faísca: palavra-chave no título de duas linhas, botão principal, estado ativo, hover.

### Neutral
Tons de azul profundo (cobalt-deep, cobalt-night) para cards sobre azul e para a moldura entre seções; tinta (ink) só em contornos e sombras; mist e cobalt-soft para fundos suaves e brilho do letreiro.

### Named Rules
**The Spark Rule.** O verde ocupa no máximo ~5% da tela e nunca carrega texto longo.
**The No-Lime-on-White Rule.** Verde sobre branco (1,2:1) é proibido; no branco, o destaque vira azul com sublinhado verde contornado.

## Typography
Archivo condensada (largura 62–75, peso 800–900, caixa alta, itálico em momentos de energia) para títulos de seção, cards e faixas. Instrument Sans para corpo, navegação, botões e títulos de duas linhas. O nome no hero é o letreiro 3D inflado (imagem); o `<h1>` real fica no HTML.

### Hierarchy
Escala 1.333 a partir de 17px: 13 / 17 / 22 / 30 / 40 / 53 / 71 / 95 / 128.

### Named Rules
**The Two-Line Title Rule.** Títulos de seção em duas linhas: primeira em branco, segunda em verde (ou azul no fundo branco).

## Layout
Grid de 12 colunas, até 1280px, gutter 24px; mobile com 16px laterais e sem rolagem horizontal. Cada seção é um grande cartão de cantos 32px sobre a moldura azul-noite. O hero é centrado e simétrico; o resto quebra a simetria com fotos-adesivo rotacionadas (−6° a 6°) e sobrepostas. Ritmo alterna seções azuis, invertidas (brancas) e faixas de palavra escuras. Espaço generoso ao redor dos heróis, compacto em listas.

## Elevation & Depth
Profundidade retrô: **sombra sólida deslocada sem desfoque** em tinta (4–6px) para adesivos, cards e botões. Sombra difusa só nos objetos 3D e no letreiro inflado.

## Shapes
Cantos 16px em cards, 24–32px em seções, pílula em botões e etiquetas. Contorno de 2–3px em tinta nos elementos coloridos; contorno branco de 10–14px nas fotos. Bordas rasgadas e cantos descolando são parte da linguagem.

## Components
### Buttons
Primário: pílula verde com texto tinta, contorno e sombra sólida; no hover sobe 2px, no clique afunda. Secundário: pílula branca com texto azul. Transição em mola de 500ms.

### Cards / Containers
Card de serviço: fundo colorido, contorno tinta, título em display itálico, ícone-adesivo saindo pelo canto, botão tinta.

### Navigation
Botão "Menu" em pílula fixo e atalhos das cinco áreas. No hero, os objetos do portal são a navegação, com etiqueta em pílula que segue o cursor.

### Portal (signature)
Retrato recortado como adesivo, topo rasgado, cinco objetos 3D. Hover: sobe ~12px, gira ~5°, escala 1.06 em 300ms `cubic-bezier(0.4, 1.65, 0.3, 1)`. Entrada: objetos de escala 0.2 e −90° em mola de 1,6s, com 100ms entre eles; nome sobe em 1,85s `cubic-bezier(0.65, 0.05, 0, 1)`. No mobile, objetos viram botões tocáveis sem cursor.

## Do's and Don'ts
### Do:
- Usar fotos reais do Eduardo, sempre como adesivo.
- Manter um momento "uau" por página.
- Oferecer versão só com opacidade em `prefers-reduced-motion`.

### Don't:
- Parallax em texto, fade genérico em tudo, loop fora do hero. Sem faixas de texto deslizantes (marquee): o Eduardo não gosta.
- Pin longo que sequestra a rolagem, cursor customizado no site inteiro.
- Gradiente roxo, cards idênticos empilhados, ícones de pacote genérico.
- Depoimentos, notas ou números inventados.
