"""Recorte v2: fundo+sombra = região suave (gradiente baixo após desfoque forte) ligada à borda, sem cor viva.
Uso: python tools/recortar2.py entrada saida [lado_max] [sigma] [limiar]"""
import sys, cv2, numpy as np
src, dst = sys.argv[1], sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
sig = float(sys.argv[4]) if len(sys.argv) > 4 else 2.2
GT = float(sys.argv[5]) if len(sys.argv) > 5 else 3.2
im = cv2.imdecode(np.fromfile(src, np.uint8), cv2.IMREAD_COLOR)
h, w = im.shape[:2]; s = mx/max(h, w)
if s < 1: im = cv2.resize(im, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA); h, w = im.shape[:2]
lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32)
bl = cv2.GaussianBlur(lab, (0,0), sig)
gx = cv2.Sobel(bl, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(bl, cv2.CV_32F, 0, 1, ksize=3)
grad = np.sqrt((gx**2 + gy**2).sum(axis=2))
sat = np.linalg.norm(bl[...,1:] - 128, axis=2)
low = ((grad < GT) & (sat < 11)).astype(np.uint8)
n, cc = cv2.connectedComponents(low, connectivity=4)
border = np.unique(np.concatenate([cc[0], cc[-1], cc[:,0], cc[:,-1]])); border = border[border != 0]
bg = np.isin(cc, border)
fg = (~bg).astype(np.uint8)*255
# componentes grandes, buracos preenchidos
n2, lb, st, _ = cv2.connectedComponentsWithStats(fg)
big = st[1:, cv2.CC_STAT_AREA].max(); keep = [i+1 for i,a in enumerate(st[1:, cv2.CC_STAT_AREA]) if a > 0.05*big]
fg = np.where(np.isin(lb, keep), 255, 0).astype(np.uint8)
ff = fg.copy(); m = np.zeros((h+2, w+2), np.uint8); cv2.floodFill(ff, m, (0,0), 255); fg = fg | cv2.bitwise_not(ff)
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
# a desfoque deslocou a borda para fora: encolhe um pouco
fg = cv2.erode(fg, np.ones((int(sig*1.2)|1,)*2, np.uint8))
alpha = cv2.GaussianBlur(fg, (0,0), 1.0)
out = np.dstack([im, alpha])
x, y, bw, bh = cv2.boundingRect((alpha > 8).astype(np.uint8)); p = 6
out = out[max(0,y-p):y+bh+p, max(0,x-p):x+bw+p]
cv2.imencode('.png', out)[1].tofile(dst); print(dst, out.shape[1], 'x', out.shape[0])
