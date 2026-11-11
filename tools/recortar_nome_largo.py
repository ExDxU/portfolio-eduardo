"""Recorta o letreiro (letras brancas, contorno azul-marinho, sombra lima) sobre fundo cinza claro e monta
"EDUARDO RIVABEM" lado a lado, em uma única linha. Resolução total do arquivo de origem.

O cinza de fundo NÃO é uniforme: é ~229 no fundo aberto, mas fica mais claro (237 a 255) nas frestas e vazados das letras.
Por isso o método classifica por REGIÃO, não por cor fixa:
 1. "Claro neutro" = pixels quase sem cor e claros (miolo branco das letras, fundo aberto, fundo dos vazados).
 2. O contorno azul-marinho separa tudo isso em regiões fechadas (4-conectividade). Cada região é miolo branco (tom
    típico ~254) ou fundo (tom típico < 248) conforme o percentil 60 do seu brilho.
 3. Nos 7 px em volta do fundo, cada pixel é separado em "cor da letra" + "cinza do fundo vizinho" (color-to-alpha,
    com o cinza do fundo mais próximo), o que dá borda suave sem halo. Longe do fundo, nada é alterado.
 4. Auditoria automática no fim.

Uso: python tools/recortar_nome_largo.py <entrada> <saida.png> [espaco_entre_palavras_px] [mapa_de_regioes.png]"""
import sys, numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
GAP = int(sys.argv[3]) if len(sys.argv) > 3 else 90
MAPA = sys.argv[4] if len(sys.argv) > 4 else None

c = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
h, w = c.shape[:2]
mx, mn = c.max(2), c.min(2)
lum = c.mean(2)

claro = ((mx - mn) <= 14) & (mn >= 196)                       # claro e neutro
n, lab, st, _ = cv2.connectedComponentsWithStats(claro.astype(np.uint8), connectivity=4)
bg = np.zeros((h, w), bool)
info = []
for i in range(1, n):
    m = lab == i
    p60 = float(np.percentile(lum[m], 60))
    e_bg = p60 < 248
    toca = st[i, 0] == 0 or st[i, 1] == 0 or st[i, 0] + st[i, 2] == w or st[i, 1] + st[i, 3] == h
    if toca: e_bg = True
    elif st[i, cv2.CC_STAT_AREA] < 150: e_bg = False      # região minúscula e fechada: ponta de estrela/contorno, nunca é fundo
    if e_bg: bg |= m
    info.append((st[i, cv2.CC_STAT_AREA], round(p60, 1), 'FUNDO' if e_bg else 'miolo'))
amb = [x for x in info if 240 <= x[1] <= 250 and x[0] > 40]
print(f'regioes claras: {len(info)} | fundo: {sum(1 for x in info if x[2]=="FUNDO")} | miolo: {sum(1 for x in info if x[2]=="miolo")} | ambiguas (p60 240-250): {len(amb)}')
for a in amb[:10]: print('  ambigua', a)

# cinza de fundo mais próximo de cada pixel (cor local do fundo)
idx = ndi.distance_transform_edt(~bg, return_distances=False, return_indices=True)
Bloc = c[idx[0], idx[1]]                                       # (h, w, 3): cor do fundo mais próximo
dist = ndi.distance_transform_edt(~bg)
zona = (dist > 0) & (dist <= 7)

# color-to-alpha só na zona de borda, contra o cinza local
a_low = np.where(c < Bloc, 1 - c / np.maximum(Bloc, 1), 0)
a_high = np.where(c > Bloc, (c - Bloc) / np.maximum(255 - Bloc, 1), 0)
a = np.clip(np.maximum(a_low, a_high).max(2), 0, 1)
a = np.clip((a - 0.05) / 0.95, 0, 1)
a[a > 0.92] = 1.0

alfa = np.ones((h, w), np.float32)
alfa[bg] = 0.0
alfa[zona] = a[zona]
F = c.copy()
a3 = np.maximum(alfa, 1e-3)[..., None]
Fz = np.clip((c - (1 - alfa)[..., None] * Bloc) / a3, 0, 255)
F[zona] = Fz[zona]
F[bg] = 0

# ---------- auditoria ----------
fundo_ou_borda = (dist <= 7)
vivo = alfa > 0.5
neutro_claro = ((F.max(2) - F.min(2)) <= 14) & (F.mean(2) >= 196)
resto_perto = vivo & neutro_claro & fundo_ou_borda
ghost = (alfa > 0.05) & (alfa <= 0.5) & ((F.max(2) - F.min(2)) <= 14) & (F.mean(2) >= 196)
print('auditoria: opacos neutro-claros a menos de 7px do fundo =', int(resto_perto.sum()),
      '| fantasmas semitransparentes claros =', int(ghost.sum()))

rgba = np.dstack([F, alfa * 255]).clip(0, 255).astype(np.uint8)
im = Image.fromarray(rgba, 'RGBA')

if MAPA:
    vis = np.zeros((h, w, 3), np.uint8)
    vis[bg] = (255, 40, 40); vis[claro & ~bg] = (40, 120, 255); vis[~claro] = (30, 30, 30)
    Image.fromarray(vis).resize((w // 3, h // 3), Image.NEAREST).save(MAPA)

# ---------- separa as duas linhas e monta lado a lado ----------
tinta = (alfa > 0.05).sum(1)
lo, hi = int(h * 0.42), int(h * 0.58)
corte = lo + int(np.argmin(tinta[lo:hi]))
print('corte entre as linhas em y =', corte, '| tinta nessa linha =', int(tinta[corte]))
def linha(y0, y1):
    p = im.crop((0, y0, w, y1))
    return p.crop(p.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox())
L1, L2 = linha(0, corte), linha(corte, h)
print('EDUARDO', L1.size, '| RIVABEM', L2.size)
H = max(L1.height, L2.height)
tela = Image.new('RGBA', (L1.width + GAP + L2.width, H), (0, 0, 0, 0))
tela.alpha_composite(L1, (0, H - L1.height))
tela.alpha_composite(L2, (L1.width + GAP, H - L2.height))
tela.save(dst); print(dst, tela.size)
