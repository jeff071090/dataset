"""Gera aniversariantes-do-mes.html (arquivo único, funciona offline).

Uso: python3 gerar_fundo.py  (só se mudar a arte)
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
    "{{CAMADAS}}": b64("camadas.png"),
    "{{LOGO}}": b64("logo-ntw.png"),
    "{{FONT_DATAS}}": b64("fontes/andika-latin-700-normal.woff2"),
    "{{FONT_MAO}}": b64("fontes/patrick-hand-latin-400-normal.woff2"),
}
for k, v in subs.items():
    html = html.replace(k, v)
(AQUI / "aniversariantes-do-mes.html").write_text(html, encoding="utf-8")
print("OK: aniversariantes-do-mes.html gerado")
