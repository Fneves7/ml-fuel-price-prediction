# -*- coding: utf-8 -*-
"""
04_metodos_conjunto.py — Família MÉTODOS DE CONJUNTO (ensemble).
Algoritmos dos prompts: árvore de decisão, Random Forest, XGBoost, CatBoost.
Alvo: o preço sobe amanhã? (1/0). Compara com uma árvore simples (baseline do
prompt) para mostrar o ganho do ensemble.
"""
import sys, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from comum import carregar, PASTA_FIG, RAIZ

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from xgboost import XGBClassifier

sns.set_theme(style="whitegrid", context="talk")
ALVO = "target_subida"


def aval(nome, y, p, L):
    acc = accuracy_score(y, p); f1 = f1_score(y, p, zero_division=0)
    print(f"  {nome:16s} accuracy={acc:.3f} | F1={f1:.3f}")
    L.append({"modelo": nome, "accuracy": acc, "f1": f1})


def main():
    print("=" * 66); print("FAMÍLIA: MÉTODOS DE CONJUNTO  (alvo = sobe amanhã?)"); print("=" * 66)
    X_tr, y_tr, X_te, y_te, feats = carregar(ALVO, classif=True)
    print(f"[dados] treino {len(X_tr):,} | teste {len(X_te):,}")
    spw = (y_tr == 0).sum() / max((y_tr == 1).sum(), 1)
    L = []

    m = DecisionTreeClassifier(max_depth=8, min_samples_leaf=20,
        class_weight="balanced", random_state=42).fit(X_tr, y_tr)
    aval("Árvore simples", y_te, m.predict(X_te), L)

    m = RandomForestClassifier(n_estimators=300, max_depth=12, min_samples_leaf=5,
        class_weight="balanced", random_state=42, n_jobs=-1).fit(X_tr, y_tr)
    aval("Random Forest", y_te, m.predict(X_te), L)

    m = XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, scale_pos_weight=spw,
        eval_metric="logloss", random_state=42, n_jobs=-1).fit(X_tr, y_tr)
    aval("XGBoost", y_te, m.predict(X_te), L)

    try:
        from catboost import CatBoostClassifier
        m = CatBoostClassifier(iterations=400, depth=6, learning_rate=0.05,
            auto_class_weights="Balanced", random_state=42, verbose=False)
        m.fit(X_tr, y_tr)
        aval("CatBoost", y_te, m.predict(X_te), L)
    except Exception as e:
        print(f"  CatBoost: indisponível no ambiente ({type(e).__name__}); ignorado.")

    tab = pd.DataFrame(L).set_index("modelo")
    tab.round(3).to_csv(RAIZ / "dados" / "sup_metodos_conjunto.csv", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(x=tab.index, y=tab["accuracy"], hue=tab.index, palette="viridis",
                legend=False, ax=ax)
    ax.set_ylabel("Accuracy"); ax.set_xlabel(""); ax.set_ylim(0.6, 0.85)
    ax.set_title("Métodos de conjunto — accuracy por algoritmo")
    for i, v in enumerate(tab["accuracy"]):
        ax.text(i, v, f"{v:.3f}", ha="center", va="bottom", fontsize=10)
    fig.savefig(PASTA_FIG / "sup_04_metodos_conjunto.png", dpi=120, bbox_inches="tight")
    print("[figura] sup_04_metodos_conjunto.png")


if __name__ == "__main__":
    main()
