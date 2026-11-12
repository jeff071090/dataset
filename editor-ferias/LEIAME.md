# Editor "Boas Férias" (offline)

Abra **`editor-ferias.html`** com dois cliques (Chrome, Edge ou Firefox). Funciona sem internet:
arte, logo e fontes estão embutidas no arquivo.

1. Digite o **nome**.
2. Escolha o **tratamento**: Feminino (Querida… tê-la) ou Masculino (Querido… tê-lo).
3. Digite a **data de retorno** (dia/mês).
4. **Baixar PNG** ou **Baixar JPG** (1748 × 1240 px).

Em *Editar o texto da mensagem* dá para mudar o texto inteiro; `{nome}` e `{data}` são trocados automaticamente.
O texto quebra as linhas sozinho e diminui a fonte se ficar grande demais para o cartão.
Abaixo de "Atenciosamente," entra a logo da Prisma.

Fonte: DM Sans Light (texto) e DM Sans Bold (assinatura), licença SIL Open Font License.

## Arquivos
- `modelo-original.webp`, `logo-prisma-original.png`: artes originais.
- `gerar_fundo.py`: apaga o texto do cartão → `fundo-modelo.jpg` e deixa a logo transparente → `logo-prisma.png`.
- `editor.src.html` + `build.py`: código do editor; `python3 build.py` gera o `editor-ferias.html`.
