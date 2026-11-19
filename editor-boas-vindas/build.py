"""Gera boas-vindas.html (arquivo único, funciona offline). Uso: python3 build.py"""
import base64
from pathlib import Path

AQUI = Path(__file__).parent


def b64(nome):
    return base64.b64encode((AQUI / nome).read_bytes()).decode()


html = (AQUI / "editor.src.html").read_text(encoding="utf-8")
subs = {"{{LOGO}}": b64("logo-ntw.png")}
for w in (400, 500, 700, 800):
    subs["{{FONT_%d}}" % w] = b64("fontes/montserrat-latin-%d-normal.woff2" % w)
for k, v in subs.items():
    html = html.replace(k, v)
(AQUI / "boas-vindas.html").write_text(html, encoding="utf-8")
print("OK: boas-vindas.html gerado")
