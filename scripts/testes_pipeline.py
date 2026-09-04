# -*- coding: utf-8 -*-
"""
testes_pipeline.py — C2: testes/asserções ao dataset enriquecido.

Verifica a integridade do pipeline (sem *data leakage*, sem NaN indevidos, sem
infinitos, alvos coerentes). Corre: `python scripts/testes_pipeline.py`
Devolve código de saída 0 se tudo passar, 1 se algum teste falhar.
"""
from pathlib import Path
import sys
import numpy as np, pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DF = pd.read_csv(RAIZ / "dados" / "dataset_enriquecido.csv",
                 parse_dates=["data"], encoding="utf-8")
G = DF.sort_values(["tipoCombustivel", "data"]).groupby("tipoCombustivel")

testes = []
def teste(nome):
    def deco(fn): testes.append((nome, fn)); return fn
    return deco


@teste("Colunas essenciais presentes")
def t1():
    for c in ["data", "tipoCombustivel", "preco_eur_l", "brent_eur", "isp_eur_l",
              "target_subida", "target_preco_amanha", "gasoleo_spot_eur_l"]:
        assert c in DF.columns, f"falta a coluna {c}"


@teste("Sem duplicados (data, combustível)")
def t2():
    assert not DF.duplicated(["data", "tipoCombustivel"]).any()


@teste("Limpeza: sem preços 0 nem > 3 €/L")
def t3():
    p = DF["preco_eur_l"].dropna()
    assert (p > 0).all() and (p <= 3).all()


@teste("Outlier de ago/2009 (Gasóleo especial) removido")
def t4():
    m = ((DF.tipoCombustivel == "Gasóleo especial") &
         (DF.data.between("2009-08-04", "2009-08-09")))
    assert DF.loc[m, "preco_eur_l"].isna().all()


@teste("Alvo 'subida' coerente com preço de amanhã")
def t5():
    d = DF.dropna(subset=["preco_amanha", "target_subida"])
    esperado = (d["preco_amanha"] > d["preco_eur_l"]).astype(int)
    assert (d["target_subida"].astype(int) == esperado).all()


@teste("Alvo é NaN exatamente onde não há dia seguinte")
def t6():
    assert (DF["target_subida"].isna() == DF["preco_amanha"].isna()).all()


@teste("Sem leakage: preco_amanha = preço do dia seguinte (por combustível)")
def t7():
    esp = G["preco_eur_l"].shift(-1)
    a, b = DF.sort_values(["tipoCombustivel", "data"])["preco_amanha"], esp
    assert ((a.isna() & b.isna()) | (np.isclose(a, b))).all()


@teste("preco_lag_1d = preço do dia anterior (por combustível)")
def t8():
    esp = G["preco_eur_l"].shift(1)
    a = DF.sort_values(["tipoCombustivel", "data"])["preco_lag_1d"]
    assert ((a.isna() & esp.isna()) | (np.isclose(a, esp))).all()


@teste("IVA só assume 20% / 21% / 23%")
def t9():
    assert set(DF["iva_taxa"].dropna().round(2).unique()) <= {0.20, 0.21, 0.23}


@teste("Sem valores infinitos nas colunas numéricas")
def t10():
    num = DF.select_dtypes("number")
    assert not np.isinf(num.to_numpy(dtype="float64", na_value=np.nan)).any()


@teste("Cobertura temporal 2008–2026 e 8 combustíveis")
def t11():
    assert DF["data"].min().year == 2008 and DF["data"].max().year >= 2026
    assert DF["tipoCombustivel"].nunique() == 8


def main():
    print("=" * 60); print("TESTES AO PIPELINE (C2)"); print("=" * 60)
    falhas = 0
    for nome, fn in testes:
        try:
            fn(); print(f"  [PASS] {nome}")
        except AssertionError as e:
            falhas += 1; print(f"  [FALHA] {nome}: {e}")
        except Exception as e:
            falhas += 1; print(f"  [ERRO] {nome}: {type(e).__name__}: {e}")
    print("-" * 60)
    print(f"{len(testes)-falhas}/{len(testes)} testes passaram.")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
