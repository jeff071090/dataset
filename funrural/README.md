# Simulador Funrural × Folha — Prisma Contabilidade

Estudo comparativo da opção do produtor rural pessoa física: contribuição sobre a **folha de pagamento** ou sobre o **faturamento** (Funrural), com a mesma lógica da planilha *MODELO CÁLCULO FUNRURAL*.

- **100% web e offline**: um único `index.html`, sem bibliotecas externas nem internet. Pode ser aberto direto do computador (duplo clique) ou publicado (GitHub Pages / servidor interno); publicado, o `sw.js` guarda tudo em cache e ele abre mesmo sem conexão.
- Gera: imagem para WhatsApp (PNG 1080×1350), imagem para e-mail (PNG 1200 px), PDF A4 e texto pronto para colar. No celular, o botão *Compartilhar* envia a imagem direto ao WhatsApp.
- Nenhum dado sai do navegador. Os últimos valores digitados ficam salvos no próprio navegador.

## Cálculo
| Opção | Base | Alíquotas (editáveis) |
|---|---|---|
| Folha | média anual de salários | INSS patronal 20% + RAT 1/2/3% + outras entidades 0,2% (2,7% com holding) + SENAR 0,2% sobre a receita |
| Faturamento | venda da produção (CFOPs − devoluções) | Funrural + RAT 1,43% + SENAR 0,2% |

Os valores podem ser do período parcial (ex.: jan–out): informe os meses e o simulador projeta para 12 (valor ÷ meses × 12). Média mensal da folha = total ÷ 13. O ponto de equilíbrio (Funrural ÷ alíquotas da folha) mostra a partir de qual folha o faturamento passa a compensar.

O relatório enviado ao cliente traz a memória de cálculo completa: origem dos números, base × alíquota de cada contribuição, comparação e o motivo da escolha.

## Editar
Altere `src/body.html` e rode `./build.sh` para regerar o `index.html`. Exemplos gerados ficam em `exemplos/`.
