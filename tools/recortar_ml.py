"""Recorte com rembg (modelo isnet-general-use). Uso: python tools/recortar_ml.py entrada saida [lado_max]"""
import sys, io, numpy as np
from PIL import Image
from rembg import remove, new_session
src, dst = sys.argv[1], sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
im = Image.open(src).convert('RGB')
if max(im.size) > mx: im.thumbnail((mx, mx), Image.LANCZOS)
sess = new_session('isnet-general-use')
out = remove(im, session=sess, post_process_mask=True)
bbox = out.getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox()
out = out.crop(bbox)
out.save(dst); print(dst, out.size)
