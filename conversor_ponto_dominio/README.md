# Conversor de cartão de ponto (PDF) → TXT de importação do Domínio Folha

```bash
python3 converter.py CARTAO1.pdf CARTAO2.pdf -o importacao_10.2026.txt
```

- Lê o bloco **"Totais de horas"** de cada PDF e gera uma linha por rubrica, no mesmo layout do TXT modelo
  (`10` + empregado(10) + AAAAMM + rubrica(4) + `11` + valor(9) + empresa(10)), com quebra de linha CRLF.
- Horas `hh:mm` viram `hhmm` (ex.: `42:12` → `000004212`).
- Antes de usar, ajuste em `config.json`:
  - `rubricas`: evento do ponto → código da rubrica no Domínio (eventos mapeados para a mesma rubrica são somados);
  - `empregados`: matrícula do cartão → código do empregado no Domínio;
  - `codigo_empresa`.
- Eventos sem rubrica configurada aparecem como **AVISO** para conferência.
- Requer `pdftotext` (pacote poppler-utils). Funciona com PDFs com texto (não escaneados).
