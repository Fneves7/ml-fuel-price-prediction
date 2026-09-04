# -*- coding: utf-8 -*-
"""
07_tuning_validacao.py
======================
Backlog B4 — Validação temporal (TimeSeriesSplit) + afinação de hiperparâmetros.

Motivação:
    Até aqui usámos UM único corte (treino < 2024, teste >= 2024). Isso pode ser
    sorte/azar. Aqui avaliamos em VÁRIAS janelas temporais (TimeSeriesSplit) para
    ver se os resultados são ROBUSTOS, e afinamos os hiperparâmetros do melhor
    modelo com uma pesquisa que respeita a ordem do tempo (sem baralhar).

    Tarefa: classificação sobe/desce a 1 dia (a tarefa principal do projeto).

Ferramentas: pandas, scikit-learn, xgboost, lightgbm, matplotlib, seaborn.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
sns.set_theme(style="whitegrid", context="talk")
DATA_CORTE = "2024-01-01"
ALVO = "target_subida"

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


def carregar():
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    feats = FEATURES + list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)
    df = df[["data"] + feats + [ALVO]].dropna()
    # ORDENAR POR DATA é essencial para a validação temporal fazer sentido
    df = df.sort_values("data").reset_index(drop=True)
    df[ALVO] = df[ALVO].astype(int)
    return df, feats


# --------------------------------------------------------------------------- #
# Parte A — Validação cruzada temporal (TimeSeriesSplit)                       #
# --------------------------------------------------------------------------- #
def validacao_temporal(df, feats):
    print("=" * 70)
    print("PARTE A — VALIDAÇÃO TEMPORAL (TimeSeriesSplit, 5 janelas)")
    print("=" * 70)
    X = df[feats]; y = df[ALVO]
    tscv = TimeSeriesSplit(n_splits=5)
    modelos = {
        "Random Forest": RandomForestClassifier(
            n_estimators=200, max_depth=12, min_samples_leaf=5,
            class_weight="balanced", random_state=42, n_jobs=-1),
        "XGBoost": XGBClassifier(
            n_estimators=400, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, eval_metric="logloss",
            random_state=42, n_jobs=-1),
        "LightGBM": LGBMClassifier(
            n_estimators=400, learning_rate=0.05, num_leaves=31,
            subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
            random_state=42, n_jobs=-1, verbose=-1),
    }
    resultados = {}
    for nome, m in modelos.items():
        accs = []
        for tr_idx, te_idx in tscv.split(X):
            m.fit(X.iloc[tr_idx], y.iloc[tr_idx])
            accs.append(accuracy_score(y.iloc[te_idx], m.predict(X.iloc[te_idx])))
        accs = np.array(accs)
        resultados[nome] = accs
        print(f"  {nome:14s} accuracy por janela: "
              f"{', '.join(f'{a:.3f}' for a in accs)}  "
              f"| média={accs.mean():.3f} ± {accs.std():.3f}")
    return resultados


# --------------------------------------------------------------------------- #
# Parte B — Afinação de hiperparâmetros (RandomizedSearchCV + TimeSeriesSplit) #
# --------------------------------------------------------------------------- #
def afinar_lightgbm(df, feats):
    print("\n" + "=" * 70)
    print("PARTE B — AFINAÇÃO DO LIGHTGBM (RandomizedSearchCV temporal)")
    print("=" * 70)
    treino = df[df["data"] < DATA_CORTE]
    teste = df[df["data"] >= DATA_CORTE]
    X_tr, y_tr = treino[feats], treino[ALVO]
    X_te, y_te = teste[feats], teste[ALVO]

    grelha = {
        "n_estimators": [200, 400, 600],
        "learning_rate": [0.02, 0.05, 0.1],
        "num_leaves": [15, 31, 63],
        "max_depth": [-1, 6, 10],
        "subsample": [0.7, 0.9, 1.0],
        "colsample_bytree": [0.7, 0.9, 1.0],
        "min_child_samples": [10, 20, 40],
    }
    base = LGBMClassifier(class_weight="balanced", random_state=42,
                          n_jobs=-1, verbose=-1)
    busca = RandomizedSearchCV(
        base, grelha, n_iter=20, scoring="f1",
        cv=TimeSeriesSplit(n_splits=3), random_state=42, n_jobs=-1, verbose=0)
    busca.fit(X_tr, y_tr)

    # Modelo por defeito (o do script 06) para comparar
    defeito = LGBMClassifier(
        n_estimators=400, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
        random_state=42, n_jobs=-1, verbose=-1).fit(X_tr, y_tr)

    def aval(m):
        p = m.predict(X_te)
        return accuracy_score(y_te, p), f1_score(y_te, p, zero_division=0)

    acc_def, f1_def = aval(defeito)
    acc_afi, f1_afi = aval(busca.best_estimator_)

    print("\nMelhores hiperparâmetros encontrados:")
    for k, v in busca.best_params_.items():
        print(f"    {k} = {v}")
    print(f"\n  LightGBM por defeito : accuracy={acc_def:.3f} | F1={f1_def:.3f}")
    print(f"  LightGBM afinado     : accuracy={acc_afi:.3f} | F1={f1_afi:.3f}")
    ganho = (acc_afi - acc_def) * 100
    print(f"  -> ganho de accuracy no teste 2024+: {ganho:+.1f} pontos percentuais")
    return {"acc_defeito": acc_def, "f1_defeito": f1_def,
            "acc_afinado": acc_afi, "f1_afinado": f1_afi,
            "best_params": busca.best_params_}


def figura(res_cv, tuning):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    # A: accuracy por janela temporal
    cores = {"Random Forest": "tab:blue", "XGBoost": "tab:orange",
             "LightGBM": "tab:green"}
    for nome, accs in res_cv.items():
        ax1.plot(range(1, len(accs)+1), accs, "o-", label=nome,
                 color=cores[nome], linewidth=2)
    ax1.axhline(0.613, color="gray", ls="--", lw=1, label="baseline (0,613)")
    ax1.set_xlabel("Janela temporal (TimeSeriesSplit)")
    ax1.set_ylabel("Accuracy")
    ax1.set_title("Robustez ao longo do tempo")
    ax1.set_xticks(range(1, 6))
    ax1.legend(fontsize=10)

    # B: LightGBM defeito vs afinado
    labels = ["Por defeito", "Afinado"]
    accs = [tuning["acc_defeito"], tuning["acc_afinado"]]
    f1s = [tuning["f1_defeito"], tuning["f1_afinado"]]
    x = np.arange(2)
    ax2.bar(x - 0.2, accs, 0.4, label="Accuracy", color="tab:green")
    ax2.bar(x + 0.2, f1s, 0.4, label="F1", color="tab:olive")
    ax2.set_xticks(x); ax2.set_xticklabels(labels)
    ax2.set_ylim(0, 1)
    ax2.set_title("LightGBM: por defeito vs afinado (teste 2024+)")
    for i, (a, f) in enumerate(zip(accs, f1s)):
        ax2.text(i-0.2, a+0.01, f"{a:.3f}", ha="center", fontsize=10)
        ax2.text(i+0.2, f+0.01, f"{f:.3f}", ha="center", fontsize=10)
    ax2.legend()
    fig.savefig(PASTA_FIG / "16_validacao_tuning.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("\n[figura] 16_validacao_tuning.png")


def main():
    df, feats = carregar()
    res_cv = validacao_temporal(df, feats)
    tuning = afinar_lightgbm(df, feats)
    figura(res_cv, tuning)
    # guardar resumo
    linhas = [{"modelo": n, "acc_media_cv": a.mean(), "acc_std_cv": a.std()}
              for n, a in res_cv.items()]
    pd.DataFrame(linhas).to_csv(
        RAIZ / "dados" / "resultados_validacao_temporal.csv",
        index=False, encoding="utf-8")
    print("[ok] dados/resultados_validacao_temporal.csv")


if __name__ == "__main__":
    main()
