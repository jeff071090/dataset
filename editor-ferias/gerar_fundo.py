"""Gera fundo-modelo.jpg (arte sem o texto do cartão) e logo-prisma.png (logo com fundo transparente).
Requer: pip install pillow numpy
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

AQUI = Path(__file__).parent
COR_CARTAO = (250, 246, 241)

# 1) apaga o texto do cartão (abaixo do lettering "Boas férias")
arte = Image.open(AQUI / "modelo-original.webp").convert("RGB")
ImageDraw.Draw(arte).rectangle([900, 625, 1530, 1050], fill=COR_CARTAO)
arte.save(AQUI / "fundo-modelo.jpg", quality=93)

# 2) logo: troca o fundo branco por transparência (color-to-alpha) e recorta
a = np.array(Image.open(AQUI / "logo-prisma-original.png").convert("RGB")).astype(float)
alpha = (255 - a).max(axis=2)
rgb = np.zeros_like(a)
m = alpha > 0
for c in range(3):
    rgb[..., c][m] = 255 - (255 - a[..., c][m]) * 255 / alpha[m]
out = np.dstack([np.clip(rgb, 0, 255), alpha]).astype(np.uint8)
logo = Image.fromarray(out, "RGBA")
logo = logo.crop(logo.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
logo.save(AQUI / "logo-prisma.png")
print("OK", arte.size, logo.size)
