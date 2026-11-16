# Editor "Boas Férias" (offline)

Abra **`editor-ferias.html`** com dois cliques (Chrome, Edge ou Firefox). Funciona sem internet:
arte, logo e fontes estão embutidas no arquivo.

1. Digite o **nome** (marque "Nome em negrito" se quiser destacar).
2. Escolha o **tratamento**: Feminino (Querida… tê-la) ou Masculino (Querido… tê-lo).
3. Digite a **data de retorno** (dia/mês) — opção "Data em negrito".
4. **Baixar PNG** ou **Baixar JPG** (1748 × 1240 px).

Em *Editar o texto da mensagem* dá para mudar o texto inteiro; `{nome}` e `{data}` são trocados automaticamente.
O texto quebra as linhas sozinho e diminui a fonte se ficar grande demais para o cartão.
Abaixo de "Atenciosamente," entra a logo da NTW Contabilidade.

Identidade visual da NTW (ntwcontabilidade.com.br): fonte Montserrat (Light no texto, Bold na assinatura/negrito), azul #09509E, texto #343434. Licença da fonte: SIL Open Font License.

## Arquivos
- `modelo-original.webp`: arte original.
- `logo-ntw.png`: logo da NTW (do site ntwcontabilidade.com.br).
- `gerar_fundo.py`: apaga o texto do cartão → `fundo-modelo.jpg`.
- `editor.src.html` + `build.py`: código do editor; `python3 build.py` gera o `editor-ferias.html`.
