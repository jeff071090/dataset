"""Gera editor-aniversario.html (arquivo único, funciona offline).

Uso: python3 build.py
Embute fundo-modelo.png e as fontes da pasta fontes/ em base64 dentro do HTML.
"""
import base64
from pathlib import Path

AQUI = Path(__file__).parent


def b64(nome):
    return base64.b64encode((AQUI / nome).read_bytes()).decode()


html = (AQUI / "editor.src.html").read_text(encoding="utf-8")
subs = {
    "{{BG}}": b64("fundo-modelo.jpg"),
    "{{FONT_FRAUNCES}}": b64("fontes/fraunces-latin-900-italic.woff2"),
    "{{FONT_SOURCESERIF}}": b64("fontes/source-serif-4-latin-900-italic.woff2"),
    "{{FONT_MERRIWEATHER}}": b64("fontes/merriweather-latin-900-italic.woff2"),
    "{{FONT_MONTSERRAT}}": b64("fontes/montserrat-latin-800-normal.woff2"),
}
for k, v in subs.items():
    html = html.replace(k, v)
(AQUI / "editor-aniversario.html").write_text(html, encoding="utf-8")
print("OK: editor-aniversario.html gerado")
