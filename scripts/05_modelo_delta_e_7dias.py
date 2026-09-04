# -*- coding: utf-8 -*-
"""
05_modelo_delta_e_7dias.py
==========================
Extensões do backlog (B2 + B1).

B2 — REGRESSÃO DA VARIAÇÃO (delta):
    Em vez de prever o VALOR do preço amanhã (onde o baseline "amanhã = hoje" é
    imbatível), prevemos a VARIAÇÃO (amanhã - hoje). O baseline passa a ser
    "prever 0" (sem alteração). Assim medimos de forma JUSTA se o modelo tem
    capacidade real de antecipar o movimento.
    Métrica-chave extra: acerto na DIREÇÃO (sinal do delta previsto).

B1 — DIREÇÃO A 7 DIAS:
    "O preço estará mais caro daqui a 7 dias?" — horizonte mais útil que 1 dia,
    porque o preço muda pouco de um dia para o outro.

Ferramentas: pandas, scikit-learn, matplotlib, seaborn.
Entrada: dados/dataset_enriquecido.csv (com os alvos target_delta_amanha e
         target_subida_7d, gerados pelo script 01).
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
                             accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
PASTA_FIG.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", context="talk")

DATA_CORTE = "2024-01-01"

# Mesmas variáveis de entrada dos outros modelos (conhecidas no dia t, sem leakage)
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
    cols_comb = list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)
    feats = FEATURES + cols_comb
    df = df[["data"] + feats + [alvo]].dropna().reset_index(drop=True)
    treino = df[df["data"] < DATA_CORTE]
    teste = df[df["data"] >= DATA_CORTE]
    return treino, teste, feats


# --------------------------------------------------------------------------- #
# B2 — Regressão da variação (delta)                                          #
# --------------------------------------------------------------------------- #
def modelo_delta():
    print("=" * 70)
    print("B2 — REGRESSÃO DA VARIAÇÃO (delta = preço amanhã - preço hoje)")
    print("=" * 70)
    alvo = "target_delta_amanha"
    treino, teste, feats = carregar(alvo)
    X_tr, y_tr = treino[feats], treino[alvo]
    X_te, y_te = teste[feats], teste[alvo]
    print(f"[dados] treino: {len(X_tr):,} | teste: {len(X_te):,}")

    def avaliar(nome, y_pred):
        mae = mean_absolute_error(y_te, y_pred)
        rmse = np.sqrt(mean_squared_error(y_te, y_pred))
        r2 = r2_score(y_te, y_pred)
        # acerto na direção (ignora dias em que o preço não mudou)
        mask = y_te != 0
        dir_acc = (np.sign(y_pred[mask]) == np.sign(y_te[mask])).mean()
        print(f"\n>>> {nome}")
        print(f"    MAE={mae:.5f} €/L | RMSE={rmse:.5f} | R²={r2:.4f} | "
              f"acerto direção={dir_acc*100:.1f}%")
        return {"modelo": nome, "MAE": mae, "RMSE": rmse, "R2": r2,
                "dir_acc": dir_acc}

    resultados = []
    # Baseline: prever 0 (sem alteração)
    resultados.append(avaliar("Baseline (prever 0 / sem alteração)",
                              np.zeros(len(y_te))))
    # Regressão Linear
    lin = LinearRegression().fit(X_tr, y_tr)
    resultados.append(avaliar("Regressão Linear", lin.predict(X_te)))
    # Random Forest
    rf = RandomForestRegressor(n_estimators=300, max_depth=16, min_samples_leaf=3,
                               random_state=42, n_jobs=-1).fit(X_tr, y_tr)
    pred_rf = rf.predict(X_te)
    resultados.append(avaliar("Random Forest", pred_rf))

    tab = pd.DataFrame(resultados).set_index("modelo")
    mae_base = tab.loc["Baseline (prever 0 / sem alteração)", "MAE"]
    print("\n" + "-" * 70)
    for nome in ["Regressão Linear", "Random Forest"]:
        ganho = (mae_base - tab.loc[nome, "MAE"]) / mae_base * 100
        print(f"    {nome}: {ganho:+.1f}% de MAE face a 'prever 0' "
              f"({'melhor' if ganho > 0 else 'pior'})")
    tab.round(5).to_csv(RAIZ / "dados" / "resultados_delta.csv", encoding="utf-8")

    # Figura: MAE por modelo + acerto na direção
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    cores = ["tab:gray", "tab:orange", "tab:green"]
    ax1.bar(range(len(tab)), tab["MAE"]*1000, color=cores)
    ax1.set_xticks(range(len(tab)))
    ax1.set_xticklabels(["Prever 0", "Reg. Linear", "Random\nForest"])
    ax1.set_ylabel("MAE (milésimos de €/L)")
    ax1.set_title("Erro na previsão da variação diária")
    for i, v in enumerate(tab["MAE"]*1000):
        ax1.text(i, v, f"{v:.2f}", ha="center", va="bottom", fontsize=11)

    dir_vals = tab["dir_acc"]*100
    ax2.bar(range(len(tab)), dir_vals, color=cores)
    ax2.axhline(50, color="red", ls="--", lw=1, label="acaso (50%)")
    ax2.set_xticks(range(len(tab)))
    ax2.set_xticklabels(["Prever 0\n(sem direção)", "Reg. Linear", "Random\nForest"])
    ax2.set_ylabel("Acerto na direção (%)")
    ax2.set_title("Acerto no SENTIDO da variação")
    ax2.set_ylim(0, 100)
    ax2.legend()
    for i, v in enumerate(dir_vals):
        if i > 0:
            ax2.text(i, v, f"{v:.0f}%", ha="center", va="bottom", fontsize=11)
    fig.savefig(PASTA_FIG / "13_regressao_delta.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("    [figura] 13_regressao_delta.png")


# --------------------------------------------------------------------------- #
# B1 — Direção a 7 dias                                                        #
# --------------------------------------------------------------------------- #
def modelo_7dias():
    print("\n" + "=" * 70)
    print("B1 — CLASSIFICAÇÃO: o preço estará mais caro daqui a 7 DIAS?")
    print("=" * 70)
    alvo = "target_subida_7d"
    treino, teste, feats = carregar(alvo)
    X_tr = treino[feats]; y_tr = treino[alvo].astype(int)
    X_te = teste[feats]; y_te = teste[alvo].astype(int)
    print(f"[dados] treino: {len(X_tr):,} | teste: {len(X_te):,} | "
          f"% 'sobe' no teste: {y_te.mean()*100:.1f}%")

    def avaliar(nome, y_pred):
        acc = accuracy_score(y_te, y_pred)
        prec = precision_score(y_te, y_pred, zero_division=0)
        rec = recall_score(y_te, y_pred, zero_division=0)
        f1 = f1_score(y_te, y_pred, zero_division=0)
        print(f"\n>>> {nome}")
        print(f"    accuracy={acc:.3f} | precisão={prec:.3f} | "
              f"recall={rec:.3f} | F1={f1:.3f}")
        return {"modelo": nome, "accuracy": acc, "precisao": prec,
                "recall": rec, "f1": f1}

    resultados = []
    base = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
    resultados.append(avaliar("Baseline (classe maioritária)", base.predict(X_te)))
    logit = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=1000, class_weight="balanced"))
    logit.fit(X_tr, y_tr)
    resultados.append(avaliar("Regressão Logística", logit.predict(X_te)))
    rf = RandomForestClassifier(n_estimators=300, max_depth=12, min_samples_leaf=5,
                                class_weight="balanced", random_state=42, n_jobs=-1)
    rf.fit(X_tr, y_tr)
    pred_rf = rf.predict(X_te)
    resultados.append(avaliar("Random Forest", pred_rf))

    print("\n" + classification_report(y_te, pred_rf,
          target_names=["Não sobe", "Sobe (7d)"], zero_division=0))
    tab = pd.DataFrame(resultados).set_index("modelo").round(3)
    tab.to_csv(RAIZ / "dados" / "resultados_direcao_7d.csv", encoding="utf-8")

    cm = confusion_matrix(y_te, pred_rf)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    sns.heatmap(cm, annot=True, fmt=",d", cmap="Greens", cbar=False,
                xticklabels=["Não sobe", "Sobe"],
                yticklabels=["Não sobe", "Sobe"], ax=ax)
    ax.set_title("Matriz de confusão — direção a 7 dias (Random Forest)")
    ax.set_xlabel("Previsto"); ax.set_ylabel("Real")
    fig.savefig(PASTA_FIG / "14_confusao_7dias.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("[figura] 14_confusao_7dias.png")


if __name__ == "__main__":
    modelo_delta()
    modelo_7dias()
