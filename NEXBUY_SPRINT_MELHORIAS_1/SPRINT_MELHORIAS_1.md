# NEXBUY — Sprint de Melhorias 1

**Objetivo:** deixar o NEXBUY mais seguro, mais confiável e mais fácil de usar
**sem mudar a essência do sistema**: o limite de compra do dia, a aprovação e a
análise do mês continuam funcionando exatamente como antes. Nenhum módulo novo,
nenhuma dependência nova.

---

## O que muda para quem usa

| # | Melhoria | O que a pessoa percebe |
|---|---|---|
| 1 | **Histórico de compras paginado** (50 por página) | A tela abre leve mesmo com anos de compras. O total do rodapé e o CSV continuam com **todas** as compras. |
| 2 | **Custos variáveis paginados** (50 por página) | Mesma coisa na lista de custos variáveis. |
| 3 | **Aprovações em cartões no celular** | No celular, cada compra/provisão aparece como um cartão com valor e botões **Aprovar / Rejeitar / Decidir** sempre visíveis (antes a tabela cortava o valor e o botão). |
| 4 | **"Sábado é dia de compra"** | Nova opção em **Financeiro → Calendário Operacional**. Ligada, todo sábado tem limite de compra próprio, como dia útil — sem precisar marcar sábado por sábado. **Vem desligada**: nenhum número muda para quem já usa. |
| 5 | **Resultado do mês mais honesto no painel** | Com o mês em andamento, o **último mês fechado** aparece primeiro e em destaque; o mês atual vira **"Lucro (prévia)"**. |
| 6 | **Aviso claro quando a receita do mês não foi lançada** | Em vez de vários "Dia crítico à frente (R$ 0,00)", aparece **um** aviso: "Receita do mês não lançada — lance em Financeiro → Receitas". A compra feita nesse período também explica o motivo de ir para aprovação. |
| 7 | **Recomendação sem frase falsa** | Mês sem compras lançadas não mostra mais "as compras já passam da receita". Fica só o aviso de "Análise incompleta". |
| 8 | **Valores dos painéis sem quebra no celular** | "R$ 452.908" não quebra mais em duas linhas. |

## O que muda na segurança (o cliente não vê, mas protege a todos)

| # | Correção | Risco que fecha |
|---|---|---|
| 9 | **Assistente de Implantação só para o suporte** (superusuário) | Qualquer Proprietário conseguia criar empresas novas sem contrato e "reservar" o CNPJ de outra empresa. O atalho some do Centro de Configurações para o cliente. |
| 10 | **Conta do suporte protegida** | O Proprietário não consegue mais editar nem gerar senha para usuário superusuário/equipe (antes isso dava acesso ao /admin de todas as empresas). |
| 11 | **Perfil de acesso global protegido** | Um cliente não consegue mais editar (e "adotar") um perfil global usado por outras empresas. |
| 12 | **Senha inicial forte** | No cadastro de usuário e no Assistente: nada de senha só com números, senha comum ou parecida com o login/nome/e-mail. |
| 13 | **Limite de tentativas de login** | 5 erros no mesmo usuário em 15 minutos pausam o acesso dele por 15 minutos, com mensagem clara. 20 erros do mesmo IP público também pausam aquele IP (atrás do balanceador do PythonAnywhere, onde o IP é igual para todos, essa regra fica desligada sozinha para nunca pausar o site inteiro). Vale também para o /admin. Usa as tentativas que a Central de Auditoria já gravava — **sem tabela nova**. |
| 14 | **CSV sem fórmula do Excel** | Um nome como `=HYPERLINK(...)` não executa mais ao abrir o CSV. Números negativos (`-3.300,00`) continuam números. |
| 15 | **Troca de empresa sem redirecionar para outro site** | O parâmetro "próxima página" só aceita páginas do próprio NEXBUY. |

## Ajuste técnico

- Teste `core/tests_pythonanywhere_uso_real.py` corrigido: no Linux ele "saía"
  do ambiente virtual ao resolver o caminho do Python e falhava sem motivo.

---

## Como instalar a atualização

Há **1 migração nova** (`empresas/0007_sabado_dia_de_compra` — só adiciona a
opção do sábado, desligada).

**PythonAnywhere** (mesmo procedimento do `docs/PYTHONANYWHERE_USO_REAL.md`):
suba o `NEXBUY_PYTHONANYWHERE.zip` desta entrega pela aba **Files** e, no
console Bash:

```bash
cd ~
rm -rf ~/nexbuy_antigo
mv nexbuy nexbuy_antigo
unzip -o NEXBUY_PYTHONANYWHERE.zip
cd ~/nexbuy
cp ../nexbuy_antigo/.env .
chmod 600 .env
bash deploy/pythonanywhere/atualizar.sh
```

O `atualizar.sh` faz backup do banco, aplica a migração e o `collectstatic`.
Depois, **Reload** na aba Web.

**VPS:** suba o código para o GitHub (veja abaixo) e rode o atualizador de
sempre: `bash /opt/nexbuy/app/deploy/atualizar.sh` — ele faz backup, `migrate`,
`collectstatic` e reinicia.

**GitHub:** a pasta `nexbuy/` do zip de código-fonte já está pronta; copie os
arquivos por cima do seu repositório e faça o commit, ou aplique o
`SPRINT_MELHORIAS_1.patch` com `git apply SPRINT_MELHORIAS_1.patch`.

### Configuração opcional (.env)

O limite de login já vem com valores seguros. Só mexa se precisar:

```
LOGIN_JANELA_MINUTOS=15
LOGIN_MAX_FALHAS_USUARIO=5
LOGIN_MAX_FALHAS_IP=20
```

### Depois de atualizar, avise os clientes

1. **Se a loja compra aos sábados:** Financeiro → Calendário Operacional →
   **"Ligar sábado como dia de compra"**.
2. **Senhas novas** precisam ser fortes (as já existentes continuam valendo).
3. **Novo CNPJ / nova empresa:** passa a ser feito pelo suporte do NEXBUY.

---

## Testes

- **25 testes novos** em `core/tests_sprint_melhorias_1.py`, um grupo por melhoria.
- Suíte completa rodada depois das mudanças (ver resultado no relatório da entrega).

Para rodar só os testes desta sprint:

```bash
python manage.py test core.tests_sprint_melhorias_1 --settings=nexbuy.settings_demo
```

## Arquivos alterados

| Área | Arquivos |
|---|---|
| Segurança | `core/limite_login.py` (novo), `core/relatorios.py`, `core/views.py`, `nexbuy/urls.py`, `nexbuy/settings.py`, `empresas/views_wizard.py`, `empresas/forms_wizard.py`, `empresas/views_ncc.py`, `empresas/forms_ncc.py`, `templates/registration/login.html`, `templates/empresas/ncc/estrutura.html` |
| Paginação | `compras/views.py`, `financeiro/views.py` (custos variáveis), `templates/partials/_paginacao.html` (novo), `templates/compras/compra_list.html`, `templates/financeiro/custovariavel_list.html` |
| Celular | `templates/dashboard/aprovacoes.html`, `static/css/nexbuy.css` |
| Sábado | `empresas/models.py`, `empresas/migrations/0007_sabado_dia_de_compra.py` (novo), `finance_engine/calendario_operacional.py`, `finance_engine/services.py`, `financeiro/views.py` (Calendário Operacional), `templates/financeiro/calendario_operacional.html` |
| Avisos e análise | `finance_engine/alertas.py`, `compras/views.py` (mensagem da compra), `financeiro/services_analise.py`, `templates/financeiro/analise/_widget_resultado_mes.html`, `static/css/analise.css` |
| Testes | `core/tests_sprint_melhorias_1.py` (novo), `empresas/tests_wizard.py`, `core/tests_pythonanywhere_uso_real.py` |

## O que ficou para a próxima sprint (de propósito)

Para não complicar esta entrega:

- **Custos fixos com vigência** (mudar o aluguel hoje não alterar os meses passados) — precisa de migração de dados com cuidado.
- **Modo simples** do menu do Proprietário (5 itens + "Mais").
- **Lembretes do dia 1 e do dia 5** (lançar a receita / corrigir a receita real).
- Paginação da Agenda Financeira e de Contas a Pagar (são telas agrupadas por data).
- Comprometimento futuro com base proporcional à janela (30/60/90 dias).
