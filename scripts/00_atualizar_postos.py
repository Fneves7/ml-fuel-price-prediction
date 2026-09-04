# -*- coding: utf-8 -*-
"""
00_atualizar_postos.py — vai buscar à DGEG os preços médios diários mais recentes
e acrescenta-os ao Postos.csv, para o dataset ficar atualizado ao correr o run_all.

Fonte: API pública da DGEG (a mesma que a página "Preço médio diário" usa):
    https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PMD
    ?idsTiposComb=&dataIni=YYYY-MM-DD&dataFim=YYYY-MM-DD&qtdPorPagina=9999&pagina=1

Comportamento:
  - Lê a última data já existente em Postos.csv e pede à DGEG só o que é novo.
  - Acrescenta apenas datas MAIS RECENTES (não altera o histórico).
  - Filtra os 8 combustíveis que o projeto acompanha.
  - Se não houver rede, avisa e continua (não quebra o pipeline).

Nota: usa `urllib` (funciona na máquina do utilizador); se falhar, tenta `curl`.
"""
import csv
import json
import subprocess
from datetime import date
from io import StringIO
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
FICHEIRO = RAIZ / "dados" / "Postos.csv"
API = ("https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PMD"
       "?idsTiposComb=&dataIni={ini}&dataFim={fim}&qtdPorPagina=9999&pagina=1&orderDesc=0")

COMBUSTIVEIS = {
    "Biodiesel B15", "GPL Auto", "Gasolina 98", "Gasolina especial 95",
    "Gasolina especial 98", "Gasolina simples 95", "Gasóleo especial",
    "Gasóleo simples",
}


def descarregar(url: str) -> str:
    """Descarrega o JSON. Tenta urllib; se falhar, tenta curl."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except (URLError, TimeoutError, OSError):
        r = subprocess.run(["curl", "-s", "--max-time", "40", url],
                           capture_output=True, text=True, encoding="utf-8")
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
        raise RuntimeError("sem acesso à API da DGEG")


def main():
    print("=" * 64)
    print("ATUALIZAR Postos.csv a partir da DGEG (preço médio diário)")
    print("=" * 64)
    base = pd.read_csv(FICHEIRO, sep=";", encoding="utf-8-sig")
    base.columns = [c.strip() for c in base.columns]
    ultima = pd.to_datetime(base["data"]).max().date()
    hoje = date.today()
    print(f"[base] última data no ficheiro: {ultima} | hoje: {hoje}")
    if ultima >= hoje:
        print("[ok] já está atualizado (nada a fazer)."); return

    url = API.format(ini=ultima.isoformat(), fim=hoje.isoformat())
    try:
        registos = json.loads(descarregar(url)).get("resultado", [])
    except Exception as e:
        print(f"[aviso] não foi possível atualizar ({e}). O pipeline continua "
              f"com os dados existentes."); return

    novos = []
    for x in registos:
        if x.get("TipoCombustivel") in COMBUSTIVEIS:
            novos.append({"data": x["Data"], "tipoCombustivel": x["TipoCombustivel"],
                          "precoMedio": x.get("PrecoMedioC4") or x.get("PrecoMedio")})
    novo = pd.DataFrame(novos)
    if novo.empty:
        print("[ok] a API não devolveu registos novos."); return

    # só datas estritamente mais recentes que a última existente
    novo = novo[pd.to_datetime(novo["data"]).dt.date > ultima]
    if novo.empty:
        print("[ok] sem datas novas para acrescentar."); return

    total = (pd.concat([base, novo], ignore_index=True)
             .drop_duplicates(["data", "tipoCombustivel"], keep="first"))
    total = total.sort_values(["tipoCombustivel", "data"]).reset_index(drop=True)
    total.to_csv(FICHEIRO, sep=";", index=False, encoding="utf-8-sig",
                 quoting=csv.QUOTE_ALL)
    dias = sorted(novo["data"].unique())
    print(f"[ok] acrescentadas {len(novo)} linhas ({len(dias)} dias novos: "
          f"{dias[0]} … {dias[-1]}). Postos.csv atualizado.")


if __name__ == "__main__":
    main()
