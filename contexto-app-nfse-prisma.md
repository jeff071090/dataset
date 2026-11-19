# Contexto — App de Emissão de NFS-e (Prisma Contabilidade)

> Arquivo de continuidade. Importe este arquivo para retomar a conversa deste ponto.
> Data de referência: 19/11/2026

---

## 1. Objetivo

Avaliar e, se viável, construir um **app para o escritório Prisma Contabilidade emitir NFS-e em nome dos seus clientes**, usando o **Sistema Nacional da NFS-e** (Emissor Nacional / Sefin Nacional).

Regra combinada: **ao navegar no portal, apenas ler e mapear — não incluir, não alterar, não enviar nada.**

---

## 2. O que já foi feito

### 2.1 Link analisado
```
https://www.nfse.gov.br/EmissorNacional/Login?ReturnUrl=%2fEmissorNacional%2fNotas%2fVisualizar%2fIndex%2f51026372263900512000124000000000000225120958121216
```
É a tela de login do Emissor Nacional, que redireciona para **Notas › Visualizar** de uma nota específica.

### 2.2 Chave de acesso decodificada (50 dígitos)
`51026372263900512000124000000000000225120958121216`

| Campo | Valor | Significado |
|---|---|---|
| Município emissor (IBGE) | `5102637` | Mato Grosso (prefixo 51); provável Campo Novo do Parecis — confirmar |
| Ambiente gerador | `2` | Sistema Nacional (Sefin Nacional) |
| Tipo de inscrição | `2` | CNPJ |
| CNPJ do emitente | `63.900.512/0001-24` | Prestador |
| Número da NFS-e | `0000000000002` | Nota nº 2 |
| Ano/mês | `2512` | Dezembro/2025 |
| Código numérico | `095812121` | Controle |
| DV | `6` | Dígito verificador |

### 2.3 Acesso ao portal
- O usuário acessa pela opção **"Acesso com Certificado Digital"** usando o **certificado da Prisma**.
- Se o CNPJ 63.900.512/0001-24 for de um **cliente** (e não da própria Prisma), é necessária **procuração eletrônica** do cliente para a Prisma no Emissor Nacional, senão a nota não aparece.

### 2.4 Limitação encontrada
- O ambiente de nuvem do Claude Code **bloqueia o acesso a `nfse.gov.br`** e não tem o certificado da Prisma.
- Por isso **o mapeamento do portal ainda NÃO foi feito**.
- Para mapear de verdade: usar o **app desktop do Claude + extensão Claude in Chrome**, no computador do usuário, já logado (somente leitura). Alternativa: enviar prints das telas.

---

## 3. Conclusão de viabilidade

**Sim, é viável.** O caminho recomendado é a **API oficial do Sistema Nacional da NFS-e**, não a automação do portal web (frágil e sem garantia).

### Fluxo de emissão pela API
1. Montar a **DPS** (Declaração de Prestação de Serviço) em XML no leiaute nacional.
2. **Assinar** a DPS com certificado digital.
3. Enviar à **Sefin Nacional** via API (autenticação mTLS com certificado).
4. Receber a **NFS-e autorizada** (chave de 50 dígitos).
5. Demais operações: consultar por chave, **eventos** (cancelamento, substituição), baixar **DANFSe (PDF)**, consultar **parâmetros municipais** (alíquotas, serviços).

Há ambiente de **Produção Restrita** (homologação, sem valor fiscal) para testes — começar por ele.

### Funcionalidades previstas do app
- Cadastro dos **clientes do escritório** (prestadores) + certificado/autorização de cada um
- Cadastro de **tomadores** e **serviços** (código de tributação nacional, alíquota, retenções)
- Emissão, histórico, cancelamento, substituição
- Download de PDF (DANFSe) e XML
- Controle de usuários e trilha de auditoria (quem emitiu o quê)

---

## 4. Pendências / pontos a confirmar

1. **Certificado na API:** confirmar se a API aceita o certificado da Prisma com procuração, ou se exige o certificado **A1 de cada cliente** (impacta o armazenamento seguro de certificados).
2. **Tipo de certificado dos clientes:** automação em servidor exige **A1** (arquivo). **A3** (token/cartão) não serve para emissão automatizada.
3. **Municípios dos clientes:** verificar quais aderiram ao Emissor Nacional e quais ainda usam sistema próprio da prefeitura.
4. **Reforma tributária:** o leiaute deve contemplar os campos de **IBS/CBS**.
5. **Município 5102637:** confirmar nome pela tabela IBGE.
6. **CNPJ 63.900.512/0001-24:** confirmar se é da Prisma ou de cliente.

---

## 5. Próximos passos sugeridos

1. Usuário responde: clientes têm certificado A1? Em quais municípios estão?
2. (Opcional) Mapear o portal em modo somente leitura via Claude in Chrome no computador do usuário.
3. Montar **documento de projeto**: escopo, telas, arquitetura, fluxo com a API, segurança de certificados.
4. Construir **protótipo** emitindo em **Produção Restrita**.
5. Validar com um cliente piloto e só então ir para produção.
