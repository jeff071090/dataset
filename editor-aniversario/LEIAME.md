# Editor de Aniversariantes (offline)

Abra **`editor-aniversario.html`** com dois cliques (Chrome, Edge ou Firefox). Funciona sem internet:
a imagem de fundo e as fontes estão embutidas no próprio arquivo.

1. **Escolher foto…** (ou arraste/cole a foto). Ajuste com o *Zoom* e arrastando a foto na prévia.
2. Digite o **nome** (o "!" é adicionado automaticamente; nomes longos diminuem sozinhos).
3. Digite a **data** (dia/mês).
4. **Baixar PNG** ou **Baixar JPG** (1080 × 1542 px).

## Fontes
- Data: Montserrat ExtraBold (igual ao modelo).
- "Parabéns!" e nome: Merriweather Black Italic, condensada automaticamente para ocupar a mesma largura do modelo.
  Se você tiver o arquivo da fonte exata usada no Canva, use *Ajustes avançados → Usar outra fonte*.

## Arquivos
- `modelo-original.png`: arte original.
- `gerar_fundo.py`: apaga foto/nome/data da arte → `fundo-modelo.jpg` (requer `pillow`, `numpy`, `opencv-python-headless`).
- `editor.src.html` + `build.py`: código do editor; `python3 build.py` gera o `editor-aniversario.html` final.
- `fontes/`: fontes com licença SIL Open Font License.
