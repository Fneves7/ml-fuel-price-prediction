# -*- coding: utf-8 -*-
"""
08_multiclasse.py — Backlog B5: classificação em 3 classes (desce / mantém / sobe).

Motivação:
    No modelo binário, os dias em que o preço fica IGUAL (~17%) estavam agregados a
    "desce". Aqui damos-lhes uma classe própria — é mais fiel à realidade e permite
    ver se o modelo distingue os três movimentos.

Alvo: target_movimento (0 = desce, 1 = mantém, 2 = sobe).
Modelos: baseline (classe maioritária), Random Forest, XGBoost.
Avaliação: accuracy, F1-macro, relatório por classe, matriz de confusão 3×3.
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import (accuracy_score, f1_score, confusion_matrix,
                             classification_report)
from xgboost import XGBClassifier

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
sns.set_theme(style="whitegrid", context="talk")
DATA_CORTE = "2024-01-01"
ALVO = "target_movimento"
NOMES = ["Desce", "Mantém", "Sobe"]

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
    df = df[["data"] + feats + [ALVO]].dropna().reset_index(drop=True)
    df[ALVO] = df[ALVO].astype(int)
    tr = df[df["data"] < DATA_CORTE]; te = df[df["data"] >= DATA_CORTE]
    return tr[feats], tr[ALVO], te[feats], te[ALVO], feats


def aval(nome, y, p, L):
    acc = accuracy_score(y, p); f1m = f1_score(y, p, average="macro")
    print(f"  {nome:26s} accuracy={acc:.3f} | F1-macro={f1m:.3f}")
    L.append({"modelo": nome, "accuracy": acc, "f1_macro": f1m})


def main():
    print("=" * 68)
    print("B5 — CLASSIFICAÇÃO EM 3 CLASSES (desce / mantém / sobe)")
    print("=" * 68)
    X_tr, y_tr, X_te, y_te, feats = carregar()
    d = np.bincount(y_tr) / len(y_tr)
    print(f"[dados] treino {len(X_tr):,} | teste {len(X_te):,}")
    print(f"[dados] treino: desce {d[0]*100:.0f}% | mantém {d[1]*100:.0f}% | sobe {d[2]*100:.0f}%")
    L = []

    base = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
    aval("Baseline (maioritária)", y_te, base.predict(X_te), L)

    rf = RandomForestClassifier(n_estimators=300, max_depth=12, min_samples_leaf=5,
        class_weight="balanced", random_state=42, n_jobs=-1).fit(X_tr, y_tr)
    aval("Random Forest", y_te, rf.predict(X_te), L)

    sw = compute_sample_weight("balanced", y_tr)
    xgb = XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, objective="multi:softprob",
        num_class=3, eval_metric="mlogloss", random_state=42, n_jobs=-1)
    xgb.fit(X_tr, y_tr, sample_weight=sw)
    pred = xgb.predict(X_te)
    aval("XGBoost", y_te, pred, L)

    print("\nRelatório por classe (XGBoost):")
    print(classification_report(y_te, pred, target_names=NOMES, zero_division=0))

    tab = pd.DataFrame(L).set_index("modelo").round(3)
    tab.to_csv(RAIZ / "dados" / "resultados_multiclasse.csv", encoding="utf-8")
    print("RESUMO:"); print(tab.to_string())

    cm = confusion_matrix(y_te, pred)
    fig, ax = plt.subplots(figsize=(6.8, 5.8))
    sns.heatmap(cm, annot=True, fmt=",d", cmap="PuBuGn", cbar=False,
                xticklabels=NOMES, yticklabels=NOMES, ax=ax)
    ax.set_title("Matriz de confusão 3 classes (XGBoost)")
    ax.set_xlabel("Previsto"); ax.set_ylabel("Real")
    fig.savefig(PASTA_FIG / "17_confusao_3classes.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("[figura] 17_confusao_3classes.png")


if __name__ == "__main__":
    main()
