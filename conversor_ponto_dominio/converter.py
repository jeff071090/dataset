#!/usr/bin/env python3
"""Converte cartoes de ponto em PDF para o TXT de importacao de variaveis do Dominio Folha.

Layout de cada linha (43 posicoes):
  01-02  "10"                       fixo
  03-12  codigo do empregado         10 digitos
  13-18  competencia AAAAMM
  19-22  rubrica                     4 digitos
  23-24  tipo de processo            "11" = folha mensal
  25-33  valor                       9 digitos (horas hh:mm -> hhmm; dias/valores com 2 decimais)
  34-43  codigo da empresa           10 digitos

Uso:
  python3 converter.py cartao1.pdf [cartao2.pdf ...] -o saida.txt [-c config.json]
"""
import argparse, json, re, subprocess, sys
from pathlib import Path


def texto_pdf(caminho):
    return subprocess.run(["pdftotext", "-layout", str(caminho), "-"],
                          capture_output=True, text=True, check=True).stdout


def ler_cartao(texto):
    m = re.search(r"Cart[aã]o Ponto - \d{2}/(\d{2})/(\d{4})", texto)
    if not m:
        raise ValueError("periodo do cartao nao encontrado")
    competencia = m.group(2) + m.group(1)
    matricula = re.search(r"Matr[ií]cula:\s*(\d+)", texto).group(1)
    nome = re.search(r"Empregado:\s*(.+?)\s*\|", texto).group(1).strip()

    bloco = texto.split("Totais de horas", 1)[1]
    totais, pendente = {}, None
    for linha in bloco.splitlines():
        # remove textos de assinatura que ficam na mesma linha
        linha = re.sub(r"\s{2,}Assinatura.*$", "", linha).strip()
        if not linha:
            continue
        m = re.match(r"^(.*?)\s{2,}(\d+:\d{2}|\d+)$", linha)
        if m:
            totais[m.group(1).strip()] = m.group(2)
            pendente = None
        elif re.fullmatch(r"\d+:\d{2}|\d+", linha) and pendente:
            # descricao quebrada em varias linhas (ex.: HORA EXTRA 100% NOTURNA / (noturno))
            totais[pendente] = linha
        elif linha.startswith("(") and pendente in totais:
            novo = f"{pendente} {linha}"
            totais[novo] = totais.pop(pendente)
            pendente = None
        else:
            pendente = linha
    return {"competencia": competencia, "matricula": matricula, "nome": nome, "totais": totais}


def valor_campo(valor):
    if ":" in valor:
        h, m = valor.split(":")
        return f"{int(h):07d}{int(m):02d}"
    return f"{int(valor) * 100:09d}"  # dias/quantidades com 2 casas decimais


def somar(a, b):
    if ":" in a:
        ha, ma = map(int, a.split(":")); hb, mb = map(int, b.split(":"))
        t = (ha + hb) * 60 + ma + mb
        return f"{t // 60}:{t % 60:02d}"
    return str(int(a) + int(b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("-o", "--saida", default="importacao_dominio.txt")
    ap.add_argument("-c", "--config", default=str(Path(__file__).with_name("config.json")))
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))

    linhas, avisos = [], []
    for pdf in a.pdfs:
        c = ler_cartao(texto_pdf(pdf))
        cod = cfg["empregados"].get(c["matricula"])
        if not cod:
            cod = c["matricula"]
            avisos.append(f"{c['nome']}: matricula {cod} sem de-para em config.json -> usando a propria matricula")
        por_rubrica = {}
        for evento, valor in c["totais"].items():
            if evento in cfg["ignorar"]:
                continue
            rub = cfg["rubricas"].get(evento)
            if not rub:
                avisos.append(f"{c['nome']}: evento sem rubrica configurada: '{evento}' = {valor}")
                continue
            por_rubrica[rub] = somar(por_rubrica[rub], valor) if rub in por_rubrica else valor
        print(f"{c['nome']} (matr. {c['matricula']}, comp. {c['competencia']})")
        for rub, valor in por_rubrica.items():
            if valor_campo(valor).strip("0") == "":
                continue
            linhas.append("10" + f"{int(cod):010d}" + c["competencia"] + rub +
                          cfg["tipo_processo"] + valor_campo(valor) + cfg["codigo_empresa"])
            print(f"   rubrica {rub}: {valor}")

    Path(a.saida).write_bytes(("\r\n".join(linhas) + "\r\n").encode("ascii"))
    print(f"\n{len(linhas)} linha(s) gravadas em {a.saida}")
    for av in avisos:
        print("AVISO:", av, file=sys.stderr)


if __name__ == "__main__":
    main()
