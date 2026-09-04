# -*- coding: utf-8 -*-
"""Módulo partilhado pelas análises do ponto B (B6, B7, B10, B11, B12).
Features enriquecidas + carregador com divisão cronológica."""
from pathlib import Path
import numpy as np, pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"; PASTA_FIG.mkdir(exist_ok=True)
DADOS = RAIZ / "dados"
DATA_CORTE = "2024-01-01"

# Features numéricas (sem os one-hot do combustível)
FEATURES_NUM = [
    "preco_eur_l", "preco_lag_1d", "preco_lag_7d", "preco_lag_30d",
    "media_movel_7d", "media_movel_30d",
    "variacao_1d", "variacao_pct_1d", "variacao_7d", "desvio_media_30d",
    "brent_usd", "eur_usd", "brent_eur", "brent_eur_media_movel_7d",
    "brent_usd_var_pct_1d", "brent_usd_var_pct_7d",
    "eur_usd_var_pct_1d", "eur_usd_var_pct_7d",
    "brent_eur_var_pct_1d", "brent_eur_var_pct_7d",
    "gasolina_spot_eur_l", "gasoleo_spot_eur_l", "crack_gasolina", "crack_gasoleo",
    "gasolina_spot_eur_l_var_pct_7d", "gasoleo_spot_eur_l_var_pct_7d",
    "wti_usd", "wti_usd_var_pct_7d",
    "evento_covid", "evento_guerra", "evento_crise_isp", "epoca_ferias",
    "isp_eur_l", "iva_taxa", "carga_fiscal_pct", "preco_sem_impostos_eur_l",
    "mes", "trimestre", "semana_ano", "dia_semana", "fim_de_semana", "feriado",
]


def carregar(alvo="target_subida", com_dummies=True, extra_cols=None):
    """Devolve treino/teste (divisão cronológica). `extra_cols` fica disponível
    no DataFrame devolvido (para análise de erros)."""
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    feats = list(FEATURES_NUM)
    if com_dummies:
        dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
        df = pd.concat([df, dummies], axis=1)
        feats += list(dummies.columns)
    cols = ["data", "tipoCombustivel"] + feats + [alvo] + list(extra_cols or [])
    cols = list(dict.fromkeys(cols))  # sem duplicados
    df = df[cols].dropna(subset=feats + [alvo]).reset_index(drop=True)
    df[alvo] = df[alvo].astype(int)
    tr = df[df["data"] < DATA_CORTE].copy()
    te = df[df["data"] >= DATA_CORTE].copy()
    return tr, te, feats
