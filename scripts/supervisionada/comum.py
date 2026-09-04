# -*- coding: utf-8 -*-
"""Utilitários partilhados pelos scripts de aprendizagem supervisionada.

Estes scripts implementam TODOS os algoritmos dos meta-prompts em
prompts_opencode_ml/01_supervisionada/, organizados pelas mesmas 4 famílias:
    01_regressao · 02_classificacao · 03_series_temporais · 04_metodos_de_conjunto
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
PASTA_FIG.mkdir(exist_ok=True)
DATA_CORTE = "2024-01-01"

FEATURES = [
    "preco_eur_l", "preco_lag_1d", "preco_lag_7d", "preco_lag_30d",
    "media_movel_7d", "media_movel_30d",
    "variacao_1d", "variacao_pct_1d", "variacao_7d", "desvio_media_30d",
    "brent_usd", "eur_usd", "brent_eur", "brent_eur_media_movel_7d",
    "brent_usd_var_pct_1d", "brent_usd_var_pct_7d",
    "eur_usd_var_pct_1d", "eur_usd_var_pct_7d",
    "brent_eur_var_pct_1d", "brent_eur_var_pct_7d",
    "isp_eur_l", "iva_taxa", "carga_fiscal_pct", "preco_sem_impostos_eur_l",
    "mes", "trimestre", "semana_ano", "dia_semana", "fim_de_semana", "feriado",
]


def carregar(alvo, classif=False):
    """Divisão cronológica (treino < 2024, teste >= 2024), com one-hot do
    combustível. Devolve X_tr, y_tr, X_te, y_te, feats."""
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    feats = FEATURES + list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)
    df = df[["data"] + feats + [alvo]].dropna().reset_index(drop=True)
    if classif:
        df[alvo] = df[alvo].astype(int)
    tr = df[df["data"] < DATA_CORTE]
    te = df[df["data"] >= DATA_CORTE]
    return tr[feats], tr[alvo], te[feats], te[alvo], feats


def serie_um_combustivel(combustivel="Gasóleo especial"):
    """Série diária contínua do preço de um combustível, para modelos de
    séries temporais univariadas."""
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    s = (df[df["tipoCombustivel"] == combustivel]
         .set_index("data")["preco_eur_l"].sort_index())
    # calendário diário contínuo + interpolação de pequenos buracos
    s = s.asfreq("D").interpolate(limit=7).dropna()
    return s
