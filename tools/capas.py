"""Prepara as capas dos vídeos: remove o ícone de som do Instagram (inpaint), recorta em 9:16 e gera AVIF/WebP.
Uso: python tools/capas.py <raiz> <dia.png> <deep-research.png> <navier-stokes.png>"""
import sys, os
import cv2, numpy as np
from PIL import Image

root = sys.argv[1]
fontes = dict(zip(['dia', 'deep-research', 'navier-stokes'], sys.argv[2:5]))
out_dir = os.path.join(root, 'public', 'img')

for nome, caminho in fontes.items():
    im = cv2.imdecode(np.fromfile(caminho, np.uint8), cv2.IMREAD_COLOR)
    h, w = im.shape[:2]
    # ícone de som: círculo escuro perto do canto inferior direito
    x0, y0 = int(w * 0.88), int(h * 0.93)
    roi = im[y0:, x0:]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    m = (gray < 75).astype(np.uint8)
    n, lb, st, cen = cv2.connectedComponentsWithStats(m)
    best = None
    for i in range(1, n):
        a = st[i, cv2.CC_STAT_AREA]
        if 250 < a < 1200 and (best is None or a > st[best, cv2.CC_STAT_AREA]):
            best = i
    if best is not None:
        cx, cy = cen[best]; r = int(np.sqrt(st[best, cv2.CC_STAT_AREA] / np.pi)) + 7
        mask = np.zeros((h, w), np.uint8)
        cv2.circle(mask, (int(x0 + cx), int(y0 + cy)), r, 255, -1)
        im = cv2.inpaint(im, mask, 5, cv2.INPAINT_TELEA)
        print(nome, 'ícone removido em', int(x0 + cx), int(y0 + cy), 'r', r)
    else:
        # mesma interface do Instagram: o ícone fica sempre na mesma posição relativa
        cx, cy, r = int(w * 0.956), int(h * 0.972), 19
        mask = np.zeros((h, w), np.uint8)
        cv2.circle(mask, (cx, cy), r, 255, -1)
        im = cv2.inpaint(im, mask, 5, cv2.INPAINT_TELEA)
        print(nome, 'ícone removido pela posição relativa em', cx, cy)
    # recorte 9:16 (tira o excesso de altura embaixo)
    th = int(round(w * 16 / 9))
    if th <= h: im = im[:th]
    else: im = im[:, : int(round(h * 9 / 16))]
    pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).convert('RGBA')
    for ww in (320, 480):
        v = pil.resize((ww, round(pil.height * ww / pil.width)), Image.LANCZOS)
        v.save(os.path.join(out_dir, f'capa-{nome}-{ww}.avif'), 'AVIF', quality=60, speed=5)
        v.save(os.path.join(out_dir, f'capa-{nome}-{ww}.webp'), 'WEBP', quality=82, method=6)
        print(f'capa-{nome}-{ww}', v.size, os.path.getsize(os.path.join(out_dir, f'capa-{nome}-{ww}.avif')) // 1024, 'KB avif')
