"""Recorta a opção B do nome (letras brancas, contorno azul-marinho, sombra lima) do arquivo do Gemini.
O fundo é um cinza liso. Em vez de ligar/desligar pixels, separa cada pixel em "cor da letra" + "cinza do fundo"
(color-to-alpha): a transparência sai suave e o halo cinza das bordas desaparece, inclusive na sombra lima.
Uso: python tools/recortar_nome.py <entrada> <saida.png> x0 y0 x1 y1"""
import sys, numpy as np, cv2
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(int, sys.argv[3:7])
im = Image.open(src).convert('RGB').crop((x0, y0, x1, y1))
c = np.asarray(im).astype(np.float32)
h, w = c.shape[:2]

# cinza do fundo por canal: mediana dos pixels cinza que tocam a borda do recorte
mx, mn = c.max(2), c.min(2)
cand = ((mx - mn) <= 12) & (np.abs(c.mean(2) - np.median(c[:6].reshape(-1, 3))) <= 14)
n0, lab0, st0, _ = cv2.connectedComponentsWithStats(cand.astype(np.uint8), connectivity=4)
toca = [i for i in range(1, n0) if st0[i, 0] == 0 or st0[i, 1] == 0 or st0[i, 0] + st0[i, 2] == w or st0[i, 1] + st0[i, 3] == h]
B = np.median(c[np.isin(lab0, toca)], axis=0)
print('fundo', B)

# transparência mínima que ainda deixa a cor da letra válida (0..255) depois de tirar o cinza
Bf = B.reshape(1, 1, 3)
a_low = np.where(c < Bf, 1 - c / Bf, 0)                                   # mais escuro que o fundo
a_high = np.where(c > Bf, (c - Bf) / (255 - Bf), 0)                       # mais claro que o fundo (branco)
alfa = np.clip(np.maximum(a_low, a_high).max(2), 0, 1)
# ruído do JPEG no fundo: abaixo disso é transparente; o restante é reescalado
alfa = np.clip((alfa - 0.07) / (0.93), 0, 1)
alfa[alfa > 0.88] = 1.0                                                   # miolo das letras 100% opaco (o branco fica a ~0,96)
# cor limpa da letra (sem o cinza misturado)
a3 = np.maximum(alfa, 1e-3)[..., None]
F = np.clip((c - (1 - alfa)[..., None] * Bf) / a3, 0, 255)
F[alfa < 0.02] = 0

# longe do fundo de verdade não há nada a separar: a letra fica 100% opaca com a cor original
# (evita tratar a transição branco -> azul-marinho como se fosse borda do fundo)
fundo_real = np.isin(lab0, toca)
for i in range(1, n0):
    if i not in toca and st0[i, cv2.CC_STAT_AREA] >= 220: fundo_real |= (lab0 == i)
dist = cv2.distanceTransform((~fundo_real).astype(np.uint8), cv2.DIST_L2, 5)
interior = dist > 4.0
alfa[interior] = 1.0
F[interior] = c[interior]
white = (mn >= 240) & ((mx - mn) <= 12) & (dist > 1.5)
alfa[white] = 1.0
F[white] = c[white]

# ilhas minúsculas de ruído somem
bin_ = (alfa > 0.05).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(bin_, connectivity=8)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] < 300: alfa[lab == i] = 0
alfa = cv2.GaussianBlur(alfa, (0, 0), 0.5)

out = np.dstack([F, alfa * 255]).clip(0, 255).astype(np.uint8)
res = Image.fromarray(out, 'RGBA')
res = res.crop(res.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox())
res.save(dst); print(dst, res.size)
