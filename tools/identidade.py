"""Gera favicon (192), ícone do iPhone (180, fundo branco) e imagem de compartilhamento (1200x630, <300 KB).
Uso: python tools/identidade.py <raiz do projeto>"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

root = sys.argv[1]
pub = os.path.join(root, 'public')
COBALT = (1, 49, 205)
LIME = (185, 252, 1)
INK = (6, 8, 20)

def abrir(c):
    return Image.open(os.path.join(root, c)).convert('RGBA')

# ---- favicon e ícone do iPhone: a carinha do site ----
carinha = abrir('assets-ml/icones/carinha.png')

def icone(tam, fundo, margem, saida, arredondar=0):
    im = Image.new('RGBA', (tam, tam), fundo)
    alvo = int(tam * (1 - 2 * margem))
    c = carinha.copy(); c.thumbnail((alvo, alvo), Image.LANCZOS)
    im.alpha_composite(c, ((tam - c.width) // 2, (tam - c.height) // 2))
    if arredondar:
        m = Image.new('L', (tam, tam), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, tam, tam), arredondar, fill=255)
        im.putalpha(m)
    im.save(os.path.join(pub, saida)); print(saida, im.size)

icone(192, COBALT + (255,), 0.14, 'favicon-192.png', arredondar=40)
icone(180, (255, 255, 255, 255), 0.12, 'apple-touch-icon.png')
icone(32, COBALT + (255,), 0.1, 'favicon-32.png', arredondar=8)

# ---- imagem de compartilhamento ----
W, H = 1200, 630
og = Image.new('RGB', (W, H), COBALT)
# retrato: a mesma foto da página Sobre mim (rosto completo), recortada em adesivo
retrato = abrir('public/img/sobre-terno-760.webp')
altura = 600
retrato = retrato.resize((int(retrato.width * altura / retrato.height), altura), Image.LANCZOS)
og.paste(retrato, (W - retrato.width - 40, H - altura + 10), retrato)

# nome: o mesmo letreiro da home (opção B), em duas linhas
nome = abrir('public/img/nome-tipo-1100.webp')
nome = nome.resize((780, int(nome.height * 780 / nome.width)), Image.LANCZOS)
og.alpha_composite(nome.convert('RGBA'), (40, 70)) if False else og.paste(nome, (40, 70), nome)

# fonte do corpo: converte o woff2 do site para uso no Pillow
f = TTFont(os.path.join(root, 'assets-fontes', 'instrument-sans-latin-wght-normal.woff2'))
f.flavor = None
ttf = os.path.join(root, 'assets-fontes', 'instrument-sans.ttf'); f.save(ttf)
fonte = ImageFont.truetype(ttf, 40)
try: fonte.set_variation_by_axes([700])
except Exception: pass
d = ImageDraw.Draw(og)
d.text((54, 330), 'Desenvolvedor de software', font=fonte, fill=(255, 255, 255))
d.text((54, 378), 'e criador de conteúdo sobre IA', font=fonte, fill=(255, 255, 255))
pequena = ImageFont.truetype(ttf, 30)
try: pequena.set_variation_by_axes([700])
except Exception: pass
texto = 'Embaixador estudantil do Google 2026'
bbox = d.textbbox((0, 0), texto, font=pequena)
px, py = 54, 480
d.rounded_rectangle((px + 4, py + 5, px + (bbox[2] - bbox[0]) + 44, py + 62), 30, fill=INK)
d.rounded_rectangle((px, py, px + (bbox[2] - bbox[0]) + 40, py + 56), 30, fill=LIME, outline=INK, width=3)
d.text((px + 20, py + 8), texto, font=pequena, fill=INK)

for q in (82, 74, 66):
    og.save(os.path.join(pub, 'og-image.jpg'), 'JPEG', quality=q, optimize=True, progressive=True)
    kb = os.path.getsize(os.path.join(pub, 'og-image.jpg')) // 1024
    if kb < 280: break
print('og-image.jpg', og.size, kb, 'KB')
