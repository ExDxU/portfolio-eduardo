"""Recorta objeto 3D predominantemente BRANCO sobre fundo cinza claro com sombra no chão (o caso mais difícil).

Nem a IA nem a cor resolvem sozinhas:
 - a IA (rembg/isnet) acerta a silhueta geral, mas perde partes brancas finas (ex.: a folha do certificado);
 - a cor acha tudo que não é o cinza do fundo, mas inclui a sombra do chão.
Regra de união: objeto = IA  OU  (região que a cor diz não ser fundo E que tem "cara de papel": levemente lilás
(B-R >= 3) ou bem clara (>= 236)). A sombra do chão é cinza NEUTRO e mais escura que o fundo, então fica de fora.
Depois: mantém só o componente principal, fecha furinhos, suaviza a borda e remove o cinza misturado nos pixels de
borda (separação de cor contra o cinza do fundo vizinho). No fim imprime uma auditoria.

Opções: --so-ia (não usa a recuperação por cor: para objeto que a IA já pega inteiro, evita trazer sombra do chão);
        --furo N (fecha furos internos de até N px; padrão 1500. Use um valor alto se o objeto não tem vão de verdade).
Uso: python tools/recortar_objeto_branco.py <entrada> <saida.png> [--so-ia] [--furo N] [--debug mapa.png]"""
import sys, numpy as np, cv2
from PIL import Image
from rembg import remove, new_session
from scipy import ndimage as ndi

args = sys.argv[1:]
SO_IA = '--so-ia' in args
FURO = int(args[args.index('--furo') + 1]) if '--furo' in args else 1500
DEBUG = args[args.index('--debug') + 1] if '--debug' in args else None
src, dst = args[0], args[1]

im = Image.open(src).convert('RGB')
c = np.asarray(im).astype(np.float32)
h, w = c.shape[:2]
mx, mn = c.max(2), c.min(2)
lum = c.mean(2)
br = c[..., 2] - c[..., 0]

# 1) IA
ia = np.asarray(remove(im, session=new_session('isnet-general-use'), only_mask=True, post_process_mask=False)).astype(np.float32) / 255

# 2) fundo por cor: cinza neutro ligado à moldura da imagem
cand = ((mx - mn) <= 4) & (np.abs(br) <= 2) & (lum >= 150) & (lum <= 233)
n0, lab, st, _ = cv2.connectedComponentsWithStats(cand.astype(np.uint8), connectivity=4)
toca = [i for i in range(1, n0) if st[i, 0] == 0 or st[i, 1] == 0 or st[i, 0] + st[i, 2] == w or st[i, 1] + st[i, 3] == h]
bg_cor = np.isin(lab, toca)

# 3) união: IA + partes com cara de papel que a IA perdeu
papel = (~bg_cor) & ((br >= 3) | (lum >= 236) | ((mx - mn) >= 25))
obj = (ia > 0.5) if SO_IA else ((ia > 0.5) | papel)
obj = cv2.morphologyEx(obj.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))       # tira pontinhos soltos
n1, lab1, st1, _ = cv2.connectedComponentsWithStats(obj, connectivity=8)
maior = 1 + int(np.argmax(st1[1:, cv2.CC_STAT_AREA]))
obj = (lab1 == maior)
obj = cv2.morphologyEx(obj.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) > 0
# furos internos pequenos (ruído) fecham; furos grandes (ex.: miolo da engrenagem com fundo de verdade) ficam
inv = ~obj
n2, lab2, st2, _ = cv2.connectedComponentsWithStats(inv.astype(np.uint8), connectivity=4)
for i in range(1, n2):
    x, y, ww, hh, area = st2[i]
    borda = x == 0 or y == 0 or x + ww == w or y + hh == h
    if not borda and area < FURO: obj[lab2 == i] = True

# 4) borda suave: 1 px para dentro + desfoque leve
dist_in = ndi.distance_transform_edt(obj)
dist_out = ndi.distance_transform_edt(~obj)
sd = dist_in - dist_out                     # distância com sinal: >0 dentro
alfa = np.clip((sd - 0.4) / 1.6, 0, 1).astype(np.float32)

# 5) descontamina a cor da borda: tira o cinza do fundo vizinho dos pixels semitransparentes
fundo_real = ~cv2.dilate(obj.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
idx = ndi.distance_transform_edt(~fundo_real, return_distances=False, return_indices=True)
Bloc = c[idx[0], idx[1]]
F = c.copy()
semi = (alfa > 0) & (alfa < 1)
a3 = np.maximum(alfa, 0.25)[..., None]
Fd = np.clip((c - (1 - alfa)[..., None] * Bloc) / a3, 0, 255)
F[semi] = Fd[semi]
# faixa interna fina: herda a cor de 3 px mais para dentro, para não sobrar fio cinza
faixa = (sd > 0) & (sd <= 2.0)
dentro = sd > 3.0
idx2 = ndi.distance_transform_edt(~dentro, return_distances=False, return_indices=True)
Fin = c[idx2[0], idx2[1]]
mist = np.clip((2.0 - sd) / 2.0, 0, 1)[..., None]
F[faixa] = (F * (1 - mist * 0.85) + Fin * (mist * 0.85))[faixa]
F[alfa == 0] = 0

# ---------- auditoria ----------
print(f'objeto: {obj.mean()*100:.1f}% da imagem | IA sozinha: {(ia>0.5).mean()*100:.1f}% | recuperado pela cor: {(obj & ~(ia>0.5)).mean()*100:.2f}% | '
      f'removido da IA: {((ia>0.5) & ~obj).mean()*100:.2f}%')
opaco = alfa > 0.9
suspeito = opaco & bg_cor & (dist_in > 6)
print('auditoria: pixels opacos com cor de fundo, longe da borda =', int(suspeito.sum()))
furos = [(int(st2[i, 4])) for i in range(1, n2) if not (st2[i, 0] == 0 or st2[i, 1] == 0 or st2[i, 0] + st2[i, 2] == w or st2[i, 1] + st2[i, 3] == h) and st2[i, 4] >= FURO]
print('furos internos mantidos (px):', furos)

rgba = np.dstack([F, alfa * 255]).clip(0, 255).astype(np.uint8)
res = Image.fromarray(rgba, 'RGBA')
res = res.crop(res.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
res.save(dst); print(dst, res.size)

if DEBUG:
    vis = np.zeros((h, w, 3), np.uint8)
    vis[obj & (ia > 0.5)] = (255, 255, 255); vis[obj & ~(ia > 0.5)] = (0, 200, 255); vis[~obj & (ia > 0.5)] = (255, 0, 0); vis[~obj & ~(ia > 0.5)] = (40, 40, 40)
    v = Image.fromarray(vis); v.thumbnail((700, 700)); v.save(DEBUG)
