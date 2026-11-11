"""Gera as imagens do site em AVIF e WebP, em vários tamanhos (srcset), a partir dos recortes.
Uso: python tools/otimizar.py <raiz do projeto>
Fontes: assets-recortados/ e assets-ml/ (recortes), referencias/ (fotos) e assets-fontes ignorado.
Saída: public/img/<nome>-<largura>.avif|webp"""
import os, sys
from PIL import Image, ImageFilter

root = sys.argv[1]
out_dir = os.path.join(root, 'public', 'img')
AV = dict(quality=58, speed=5)       # AVIF: ~40% menor que WebP com qualidade equivalente
WP = dict(quality=82, method=6)
INK = (6, 8, 20)


def salvar(im: Image.Image, nome: str, larguras):
    for w in larguras:
        v = im if im.width == w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        v.save(os.path.join(out_dir, f'{nome}-{w}.avif'), 'AVIF', **AV)
        v.save(os.path.join(out_dir, f'{nome}-{w}.webp'), 'WEBP', **WP)
        print(f'{nome}-{w}', v.size, os.path.getsize(os.path.join(out_dir, f'{nome}-{w}.avif')) // 1024, 'KB avif /',
              os.path.getsize(os.path.join(out_dir, f'{nome}-{w}.webp')) // 1024, 'KB webp')


def abrir(caminho):
    return Image.open(os.path.join(root, caminho)).convert('RGBA')


def com_sombra(src: Image.Image, largura_max: int):
    """sombra sólida (tinta) deslocada para baixo, assada na imagem"""
    src = src.resize((largura_max, round(src.height * largura_max / src.width)), Image.LANCZOS)
    off = max(4, round(largura_max * 0.022))
    out = Image.new('RGBA', (src.width, src.height + off), (0, 0, 0, 0))
    sh = Image.new('RGBA', src.size, INK + (0,))
    sh.putalpha(src.getchannel('A').point(lambda v: int(v * 0.92)))
    out.alpha_composite(sh, (0, off))
    out.alpha_composite(src, (0, 0))
    return out


# nome em 3D
salvar(abrir('assets-recortados/nome-3d.png'), 'nome-3d', [640, 1100, 1800])

# retrato (alta resolução) e sombra assada (desfocada: pode ser bem menor)
head = abrir('assets-recortados/portal-cabeca-hd.png')
salvar(head, 'portal-cabeca', [640, 960, 1456])
for hw in (480, 800):
    h = head.resize((hw, round(head.height * hw / head.width)), Image.LANCZOS)
    mx, my = round(hw * 0.0803), round(h.height * 0.0803)
    canvas = Image.new('L', (hw + 2 * mx, h.height + 2 * my), 0)
    canvas.paste(h.getchannel('A'), (mx, my + round(h.height * 0.022)))
    canvas = canvas.filter(ImageFilter.GaussianBlur(round(hw * 0.03))).point(lambda v: int(v * 0.5))
    sh = Image.new('RGBA', canvas.size, (0, 16, 74, 0)); sh.putalpha(canvas)
    salvar(sh, 'portal-sombra', [sh.width])

# objetos 3D (com sombra sólida assada)
objs = {'obj-sobre': ([320, 560]), 'obj-servicos': ([320, 560]), 'obj-videos': ([240, 420]),
        'obj-academico': ([380, 680]), 'obj-noticias': ([380, 680])}
for nome, ws in objs.items():
    big = com_sombra(abrir(f'assets-ml/{nome}.png'), ws[-1])
    salvar(big, nome, ws)

# ícones-adesivo
for nome in ['foguete', 'carinha', 'notebook', 'celular', 'capelo', 'megafone', 'estrela', 'lupa']:
    salvar(abrir(f'assets-ml/icones/{nome}.png'), f'ico-{nome}', [220, 360])

# foto-adesivo do terno (já com contorno e sombra) e foto do hackathon
salvar(Image.open(os.path.join(root, 'assets-recortados', 'sobre-terno-fonte.webp')).convert('RGBA'), 'sobre-terno', [380, 760])
hk = Image.open(os.path.join(root, 'referencias', 'Eduardo-Hackaton.jpeg')).convert('RGBA')
hk = hk.resize((720, round(hk.height * 720 / hk.width)), Image.LANCZOS)
salvar(hk, 'foto-hackathon', [420, 720])
