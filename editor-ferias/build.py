"""Gera editor-ferias.html (arquivo único, funciona offline).

Uso: python3 gerar_fundo.py  (só se mudar a arte ou a logo)
     python3 build.py
"""
import base64
from pathlib import Path

AQUI = Path(__file__).parent


def b64(nome):
    return base64.b64encode((AQUI / nome).read_bytes()).decode()


html = (AQUI / "editor.src.html").read_text(encoding="utf-8")
subs = {
    "{{BG}}": b64("fundo-modelo.jpg"),
    "{{LOGO}}": b64("logo-prisma.png"),
    "{{FONT_LIGHT}}": b64("fontes/dm-sans-latin-300-normal.woff2"),
    "{{FONT_BOLD}}": b64("fontes/dm-sans-latin-700-normal.woff2"),
}
for k, v in subs.items():
    html = html.replace(k, v)
(AQUI / "editor-ferias.html").write_text(html, encoding="utf-8")
print("OK: editor-ferias.html gerado")
