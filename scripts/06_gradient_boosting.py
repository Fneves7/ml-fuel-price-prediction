# -*- coding: utf-8 -*-
"""
06_gradient_boosting.py
=======================
Backlog B3 — Gradient Boosting (XGBoost + LightGBM) vs Random Forest.

Compara três algoritmos nas tarefas principais do projeto, para ver se o
gradient boosting (XGBoost / LightGBM) melhora face à Random Forest:

    Tarefa 1: Classificação sobe/desce a 1 dia   (accuracy, F1)
    Tarefa 2: Regressão da variação (delta)       (MAE, R², acerto direção)
    Tarefa 3: Classificação direção a 7 dias      (accuracy, F1)

Mesma divisão cronológica e mesmas features dos outros scripts (comparação justa).
Ferramentas: pandas, scikit-learn, xgboost, lightgbm, matplotlib, seaborn.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, f1_score, mean_absolute_error,
                             r2_score)
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
sns.set_theme(style="whitegrid", context="talk")
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


def carregar(alvo):
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    feats = FEATURES + list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)
    df = df[["data"] + feats + [alvo]].dropna().reset_index(drop=True)
    tr = df[df["data"] < DATA_CORTE]
    te = df[df["data"] >= DATA_CORTE]
    return tr[feats], tr[alvo], te[feats], te[alvo]


def classificar(nome_tarefa, alvo):
    X_tr, y_tr, X_te, y_te = carregar(alvo)
    y_tr = y_tr.astype(int); y_te = y_te.astype(int)
    # peso para desequilíbrio (nº negativos / nº positivos)
    spw = (y_tr == 0).sum() / max((y_tr == 1).sum(), 1)
    modelos = {
        "Random Forest": RandomForestClassifier(
            n_estimators=300, max_depth=12, min_samples_leaf=5,
            class_weight="balanced", random_state=42, n_jobs=-1),
        "XGBoost": XGBClassifier(
            n_estimators=400, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, scale_pos_weight=spw,
            eval_metric="logloss", random_state=42, n_jobs=-1),
        "LightGBM": LGBMClassifier(
            n_estimators=400, learning_rate=0.05, num_leaves=31,
            subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
            random_state=42, n_jobs=-1, verbose=-1),
    }
    print(f"\n=== {nome_tarefa} ===  (teste: {len(y_te):,} linhas)")
    linhas = []
    for nome, m in modelos.items():
        m.fit(X_tr, y_tr)
        p = m.predict(X_te)
        acc = accuracy_score(y_te, p); f1 = f1_score(y_te, p, zero_division=0)
        print(f"  {nome:14s} accuracy={acc:.3f} | F1={f1:.3f}")
        linhas.append({"tarefa": nome_tarefa, "modelo": nome,
                       "metrica_principal": acc, "f1": f1})
    return linhas


def regressao_delta():
    alvo = "target_delta_amanha"
    X_tr, y_tr, X_te, y_te = carregar(alvo)
    modelos = {
        "Random Forest": RandomForestRegressor(
            n_estimators=300, max_depth=16, min_samples_leaf=3,
            random_state=42, n_jobs=-1),
        "XGBoost": XGBRegressor(
            n_estimators=500, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1),
        "LightGBM": LGBMRegressor(
            n_estimators=500, learning_rate=0.05, num_leaves=31,
            subsample=0.8, colsample_bytree=0.8, random_state=42,
            n_jobs=-1, verbose=-1),
    }
    mae_base = y_te.abs().mean()
    print(f"\n=== Regressão da variação (delta) ===  "
          f"(baseline 'prever 0' MAE={mae_base:.5f})")
    linhas = []
    for nome, m in modelos.items():
        m.fit(X_tr, y_tr)
        p = m.predict(X_te)
        mae = mean_absolute_error(y_te, p); r2 = r2_score(y_te, p)
        mask = y_te != 0
        diracc = (np.sign(p[mask.values]) == np.sign(y_te[mask])).mean()
        ganho = (mae_base - mae) / mae_base * 100
        print(f"  {nome:14s} MAE={mae:.5f} ({ganho:+.0f}% vs baseline) | "
              f"R²={r2:.3f} | direção={diracc*100:.1f}%")
        linhas.append({"tarefa": "Regressão delta", "modelo": nome,
                       "metrica_principal": diracc, "f1": r2})
    return linhas


def main():
    print("=" * 70)
    print("B3 — GRADIENT BOOSTING (XGBoost / LightGBM) vs RANDOM FOREST")
    print("=" * 70)
    res = []
    res += classificar("Classificação 1 dia (sobe/desce)", "target_subida")
    res += regressao_delta()
    res += classificar("Direção a 7 dias", "target_subida_7d")

    tab = pd.DataFrame(res)
    tab.to_csv(RAIZ / "dados" / "resultados_gradient_boosting.csv",
               index=False, encoding="utf-8")

    # Figura: barras agrupadas (métrica principal por tarefa e modelo)
    tarefas = tab["tarefa"].unique()
    modelos = ["Random Forest", "XGBoost", "LightGBM"]
    cores = {"Random Forest": "tab:blue", "XGBoost": "tab:orange",
             "LightGBM": "tab:green"}
    fig, ax = plt.subplots(figsize=(14, 7))
    larg = 0.25
    x = np.arange(len(tarefas))
    for i, mod in enumerate(modelos):
        vals = [tab[(tab.tarefa == t) & (tab.modelo == mod)]
                ["metrica_principal"].values[0] for t in tarefas]
        barras = ax.bar(x + i*larg, vals, larg, label=mod, color=cores[mod])
        for b, v in zip(barras, vals):
            ax.text(b.get_x() + b.get_width()/2, v + 0.005, f"{v:.3f}",
                    ha="center", fontsize=9)
    ax.set_xticks(x + larg)
    ax.set_xticklabels([t.replace(" (", "\n(") for t in tarefas], fontsize=10)
    ax.set_ylabel("Métrica principal\n(accuracy / acerto na direção)")
    ax.set_title("B3 — Gradient Boosting vs Random Forest")
    ax.set_ylim(0, 1)
    ax.legend()
    fig.savefig(PASTA_FIG / "15_comparacao_gradient_boosting.png",
                dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("\n[figura] 15_comparacao_gradient_boosting.png")
    print("[ok] dados/resultados_gradient_boosting.csv")


if __name__ == "__main__":
    main()
