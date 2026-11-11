# Prompts para o Gemini Pro (imagens do site)

**Como usar**
- Uma conversa nova no Gemini para o conjunto inteiro, para manter o estilo consistente. Cole primeiro o **Bloco de estilo** e depois um prompt por vez.
- Peça sempre em **inglês** (o modelo de imagem segue melhor). As notas em português são para você.
- Gere 2 a 4 variações de cada e escolha. Se um objeto sair diferente dos outros, diga: *"match the exact lighting, material and camera angle of the previous image"*.
- **Fundo:** todos os objetos vêm em fundo liso claro para eu recortar depois (não confie em "fundo transparente": o Gemini costuma desenhar um xadrez falso).
- Salve tudo em `portfolio-eduardo/assets-brutos/` com o nome indicado em cada prompt. Eu recorto, otimizo (WebP/AVIF) e monto as camadas.

---

## 0. Bloco de estilo (colar uma vez, no início)

```
I'm creating a set of images for my personal website. All images in this conversation must share ONE consistent visual style:

- Glossy, soft, slightly "inflated" 3D objects, like premium toy-like renders (Blender/Octane look), smooth plastic and soft rubber materials, subtle subsurface glow.
- Soft studio lighting from the top-left, gentle rim light, soft contact shadow only directly under the object.
- Color palette limited to: cobalt blue #0131CD, pure white #FFFFFF, neon lime green #B9FC01, plus a near-black navy #060814 for small details. Small neutral greys allowed for metal/screens.
- Camera: three-quarter view, slightly from above, 50mm lens, object centered with generous empty margin around it.
- Background: perfectly flat, plain light grey #EDEDED, no gradient, no floor, no props, no text unless asked.
- Retro-playful mood (late 90s / early 2000s toys and packaging), but clean and premium, not cartoon-cheap.

Confirm you understood and wait for my first request.
```

---

## 1. Retrato-portal (editar a sua foto) → `portal-cabeca.png`

Anexe **`referencias/Eduardo-capa-terno.jpeg`** e cole:

```
Edit the attached photo of me. Keep my face, smile, hair color, skin tone and expression EXACTLY as they are — do not redraw or beautify my face.

1. Crop to head and the top of the shoulders/collar (keep the knot of the red tie visible at the bottom).
2. Cut me out as a STICKER: a thick, clean, solid white outline (about 3% of the image width) following my silhouette, like a die-cut vinyl sticker.
3. The top of the head is TORN OFF horizontally at forehead level, like ripped paper: the tear line is irregular, with small white paper fibers along the edge. Above the tear there is nothing — the inside of the head is an empty opening (dark navy #060814 inside), ready for objects to come out of it.
4. Place it on a perfectly flat plain light grey #EDEDED background.

Front-facing, centered, high resolution, photographic (not illustrated).
```

> Nota: se o Gemini alterar seu rosto, peça *"redo it, my face must be pixel-identical to the original photo, only the outline and the torn top change"*. Se não ficar bom em 2 tentativas, eu faço o recorte e o rasgo em código (máscara SVG) a partir da foto original: o resultado é até mais controlável.

---

## 2. Objetos do portal (1 por área)

Mesmo estilo do bloco 0. Um objeto por imagem.

### 2.1 Sobre mim → `obj-sobre.png`
```
A single glossy 3D smiley-face ball, lime green #B9FC01, with a big friendly open smile and two simple oval eyes in navy #060814, one eye slightly winking. Soft inflated look. Plain flat light grey #EDEDED background.
```

### 2.2 Serviços → `obj-servicos.png`
```
A single glossy 3D retro toy rocket, white body with cobalt blue #0131CD fins and nose cone, one round porthole window glowing lime green #B9FC01, a short soft cartoon flame in lime green at the bottom. Tilted 30 degrees to the right, as if launching. Plain flat light grey #EDEDED background.
```

### 2.3 Vídeos → `obj-videos.png`
```
A single glossy 3D retro smartphone standing vertically, rounded chunky toy-like body in white, screen in cobalt blue #0131CD showing a big lime green #B9FC01 play button triangle and a short progress bar. Slightly rotated, three-quarter view. Plain flat light grey #EDEDED background.
```

### 2.4 Acadêmico → `obj-academico.png`
```
A single glossy 3D graduation cap (mortarboard) in navy #060814 with a lime green #B9FC01 tassel, and a small round medal in cobalt blue #0131CD with a white star hanging from a white ribbon, resting against the cap. Toy-like, inflated, soft edges. Plain flat light grey #EDEDED background.
```

### 2.5 Notícias → `obj-noticias.png`
```
A single glossy 3D folded newspaper, soft and slightly puffy, white paper with cobalt blue #0131CD headline blocks (abstract bars, no readable text) and one small lime green #B9FC01 sticker dot on the corner. Slightly fanned open, three-quarter view. Plain flat light grey #EDEDED background.
```

> Teste de consistência: depois dos 5, peça *"Now show all five objects together in one image, same style, arranged as if bursting out of the top of a head"*. Serve só para conferir se combinam; no site eu uso as imagens separadas.

---

## 3. Nome em 3D inflado → `nome-3d.png`

```
The text "EDUARDO RIVABEM" written as big puffy, inflated 3D balloon letters (like inflated vinyl / bubble letters), pure glossy white with very subtle cobalt blue #0131CD reflections in the shadows, soft rounded edges, all letters the same height, set in ONE line, perfectly straight, front view (no perspective), letters slightly overlapping. Spelling must be exact: E-D-U-A-R-D-O R-I-V-A-B-E-M. Plain flat cobalt blue #0131CD background. Very high resolution, wide 4:1 format.
```

> Nota: o Gemini às vezes erra letras. Confira a grafia letra por letra. Se errar, peça só *"same image, fix the spelling to EDUARDO RIVABEM"*. Plano B: gerar em duas linhas ("EDUARDO" e "RIVABEM") separadamente.

---

## 4. Ícones-adesivo retrô (2D, estilo Slush) → `icones-adesivo.png`

Este é **ilustração plana**, não 3D. Comece uma conversa nova (ou avise que o estilo muda):

```
Flat retro sticker illustrations, NOT 3D. Thick uniform navy #060814 outlines (same stroke weight on all), flat fills using only cobalt blue #0131CD, white #FFFFFF and lime green #B9FC01, a solid offset navy shadow (no blur) under each, slight isometric tilt. Style of 90s packaging stickers, playful and bold.

Draw these 8 separate stickers on a 4x2 grid, evenly spaced, on a plain white background, no text:
1. a rocket  2. a smiley face  3. a laptop showing a simple web page  4. a play button inside a rounded phone  5. a graduation cap  6. a megaphone  7. a sparkle / AI star  8. a magnifying glass over a bar chart (SEO)
```

> Eu recorto cada um e, se precisar, redesenho em SVG por cima para ficarem nítidos em qualquer tamanho.

---

## 5. Opcional: forma 3D de fundo → `fundo-forma.png`

```
A single long, thick, soft tube shape twisting in an S-curve across the frame, cobalt blue #0131CD slightly lighter than the background, with a fine bumpy foam texture, soft studio lighting. Plain flat cobalt blue #0131CD background, the tube fills most of the frame. Wide 16:9.
```

> Esse fica atrás do hero, bem discreto. Se ficar chamativo demais, a gente descarta.

---

## Checklist de entrega (arquivos)
- [ ] `portal-cabeca.png`
- [ ] `obj-sobre.png`, `obj-servicos.png`, `obj-videos.png`, `obj-academico.png`, `obj-noticias.png`
- [ ] `nome-3d.png`
- [ ] `icones-adesivo.png`
- [ ] `fundo-forma.png` (opcional)

---

## 8. Nome em tipografia com personalidade (3 opções) → `nome-tipo-A.png`, `-B.png`, `-C.png`

**Por que:** o nome em texto simples ficou sem personalidade e pequeno no celular. Aqui o nome vira uma **imagem de letreiro**, em duas linhas empilhadas (EDUARDO / RIVABEM) para ocupar a largura toda do celular.
**Use numa conversa nova do Gemini** (não precisa do Bloco de estilo do item 0; o prompt abaixo já traz tudo). Peça as 3 opções de uma vez; se vierem juntas numa imagem só, peça "now output each option as a separate image".
**Atenção:** o Gemini erra ortografia. Confira se saiu **EDUARDO** e **RIVABEM** (com V, não B). Se errar, diga: *"The text must be exactly: EDUARDO on the first line and RIVABEM on the second. Redo it."*

```
Design 3 DIFFERENT hand-crafted lettering / typography treatments of my name, for the hero of my personal website. I am a young software developer and AI content creator (Google Student Ambassador 2026), so the mood is playful, retro, confident and a little techy.

THE TEXT (spell it EXACTLY, all caps, no other words, no extra letters):
Line 1: EDUARDO
Line 2: RIVABEM
(Careful: it is R-I-V-A-B-E-M, with a V and then a B.)

LAYOUT FOR ALL 3
- Two lines stacked, tight leading, both lines justified to the SAME width so the whole name forms one big solid rectangular block, wider than tall (about 4:3). The letters must be HUGE and fill the canvas edge to edge with only a small margin, because this will be shown on a phone screen.
- Letterforms: ultra-condensed, extra-heavy, tall grotesque (think poster / sports / Slush-style headline type), but each option must have its own distinctive character, custom details and a clever idea, NOT a plain font typed out. Every letter stays perfectly legible.

COLOR PALETTE (use only these): cobalt blue #0131CD, pure white #FFFFFF, neon lime #B9FC01, near-black navy #060814 for outlines and hard shadows.
BACKGROUND: perfectly flat plain light grey #EDEDED, no gradient, no floor, no texture, no props around the lettering (so I can cut it out). Output each option as its own image, 2048 px wide.

OPTION A — "Die-cut sticker": thick lime letters wrapped by one continuous thick white die-cut sticker outline, a hard offset navy shadow (no blur) under it, and a slight playful rotation and bounce of the baseline between letters. One small touch of personality: the dot/counter of one letter replaced by a tiny winking smiley face.

OPTION B — "Code + AI": flat white letters with a bold navy outline and hard lime offset shadow. Letterforms with small technical details cut into them: the counters of the O, D, A and B shaped like code brackets < > and { }, a tiny four-point AI sparkle star as the cut of one letter, and thin pixel/scanline stripes across the lower part of the letters. Retro-computer feel, but clean and premium.

OPTION C — "Torn paper": letters look cut out of thick cobalt-blue paper with a ripped, irregular white paper edge (like a torn sticker edge), a lime paper layer peeking out from behind each letter, and a hard navy offset shadow. A few small flat shapes (star, lightning bolt) tucked behind the letters. Handmade collage mood.

RULES FOR ALL: no photos, no people, no 3D glossy/inflated balloon look (flat or paper-cut graphic style only), no gradients except tiny highlights, no watermark, no extra text, no slogans.
```

**Depois de gerar:** salve em `assets-brutos/` e me avise qual escolheu. Eu recorto o fundo, otimizo (WebP/AVIF) e troco no site (home, imagem de compartilhamento e rodapé, se fizer sentido). Se nenhuma agradar, mande o que gostou ou não de cada uma e eu refaço o prompt.
