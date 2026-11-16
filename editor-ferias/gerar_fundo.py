"""Gera fundo-modelo.jpg (arte sem o texto do cartão).
Requer: pip install pillow
"""
from pathlib import Path
from PIL import Image, ImageDraw

AQUI = Path(__file__).parent
COR_CARTAO = (250, 246, 241)

# 1) apaga o texto do cartão (abaixo do lettering "Boas férias")
arte = Image.open(AQUI / "modelo-original.webp").convert("RGB")
ImageDraw.Draw(arte).rectangle([900, 625, 1530, 1050], fill=COR_CARTAO)
arte.save(AQUI / "fundo-modelo.jpg", quality=93)

print("OK", arte.size)
