"""Recorta objetos do Gemini (fundo cinza liso, sombra suave) para PNG com alfa.
Método: o fundo e a sombra variam suavemente; o objeto tem bordas nítidas.
Preenche o fundo a partir das bordas da imagem parando onde há gradiente forte.
Uso: python tools/recortar.py entrada saida [lado_max]"""
import sys, cv2, numpy as np
src, dst = sys.argv[1], sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 900
im = cv2.imdecode(np.fromfile(src, np.uint8), cv2.IMREAD_COLOR)
h, w = im.shape[:2]
s = mx / max(h, w)
if s < 1: im = cv2.resize(im, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA); h, w = im.shape[:2]
lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32)
lab = cv2.GaussianBlur(lab, (0,0), 1.0)
gx = cv2.Sobel(lab, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(lab, cv2.CV_32F, 0, 1, ksize=3)
grad = np.sqrt((gx**2 + gy**2).sum(axis=2))
border = np.concatenate([im[:6].reshape(-1,3), im[-6:].reshape(-1,3), im[:,:6].reshape(-1,3), im[:,-6:].reshape(-1,3)])
bgc = cv2.cvtColor(np.uint8([[np.median(border, axis=0)]]), cv2.COLOR_BGR2LAB)[0,0].astype(np.float32)
colordist = np.linalg.norm(lab - bgc, axis=2)
GT = float(sys.argv[4]) if len(sys.argv) > 4 else 7.0
low = (grad < GT).astype(np.uint8)
# fundo = regiões de baixo gradiente conectadas à borda
n, cc = cv2.connectedComponents(low, connectivity=4)
edge_ids = set(np.unique(np.concatenate([cc[0], cc[-1], cc[:,0], cc[:,-1]]))) - {0}
bgmask = np.isin(cc, list(edge_ids))
# o fundo precisa se parecer com o fundo OU ser sombra (mais escuro, pouco saturado), nunca cor viva
sat = np.linalg.norm(lab[...,1:] - 128, axis=2)
import os
bgmask &= (colordist < 40) & ((sat < 14) | (os.environ.get('FUNDO_COLORIDO') == '1'))
# sombra: cinza sem cor, mais escuro que o fundo, de gradiente baixo, nos 30% de baixo
Lc = lab[...,0]; shadowy = (sat < 9) & (grad < 5) & (Lc < bgc[0] - 6) & (Lc > 90)
rows = np.zeros((h, w), bool); ys = np.where((~bgmask).any(axis=1))[0]; y0 = ys.min() + int(0.68*(ys.max()-ys.min()))
rows[y0:] = True
bgmask |= shadowy & rows
fg = (~bgmask).astype(np.uint8) * 255
n2, lb, st, _ = cv2.connectedComponentsWithStats(fg)
if n2 > 1:
    big = st[1:, cv2.CC_STAT_AREA].max(); keep = [i+1 for i,a in enumerate(st[1:, cv2.CC_STAT_AREA]) if a > 0.05*big]; fg = np.where(np.isin(lb, keep), 255, 0).astype(np.uint8)
# preenche buracos internos
ff = fg.copy(); m = np.zeros((h+2, w+2), np.uint8); cv2.floodFill(ff, m, (0,0), 255)
fg = fg | cv2.bitwise_not(ff)
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
fg = cv2.erode(fg, np.ones((3,3), np.uint8))
KEEP = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0   # fração da altura mantida (corta restos de sombra no pé)
if KEEP < 1.0:
    ys = np.where(fg.any(axis=1))[0]; cut = ys.min() + int(KEEP*(ys.max()-ys.min())); fg[cut:] = 0
alpha = cv2.GaussianBlur(fg, (0,0), 1.0)
out = np.dstack([im, alpha])
x, y, bw, bh = cv2.boundingRect((alpha > 8).astype(np.uint8)); p = 6
out = out[max(0,y-p):y+bh+p, max(0,x-p):x+bw+p]
cv2.imencode('.png', out)[1].tofile(dst)
print(dst, out.shape[1], 'x', out.shape[0])
