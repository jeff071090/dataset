# Aniversariantes do Mês (offline) – NTW Contabilidade

Abra **`aniversariantes-do-mes.html`** com dois cliques (Chrome, Edge ou Firefox). Funciona sem internet.

1. Escolha o **mês** (o subtítulo em arco muda para "aniversariantes de <mês>").
2. Digite os **aniversariantes**, um por linha: `11 Daiane`, `11/12 Daiane` ou `11 - Daiane`
   (se digitar só o dia, usa o mês escolhido). Dá para colar de uma planilha. Ordena por data automaticamente.
   As faixas se ajustam à quantidade de pessoas (até ~16 cabem bem).
3. (Opcional) **Cores**: paletas prontas (Azul NTW, Rosa, Verde, Lilás, Dourado, Vermelho, Laranja)
   ou escolha a cor de cada parte: balões, caixa de presente, fundo, textos/enfeites e faixas dos nomes.
4. **Baixar PNG** ou **Baixar JPG** (1024 × 1535 px).

Identidade visual da NTW: logo oficial e azul #09509E como cor padrão dos textos.
Fontes: Patrick Hand (nomes e subtítulo) e Andika Bold (datas), licença SIL Open Font License.

## Arquivos
- `modelo-original.webp`: arte original.
- `gerar_fundo.py`: apaga subtítulo, lista e logo antiga, aplica o azul NTW → `fundo-modelo.jpg`,
  e gera `camadas.png` (máscaras de balões / presente / textos usadas para trocar as cores).
- `editor.src.html` + `build.py`: código do editor; `python3 build.py` gera o `aniversariantes-do-mes.html`.
