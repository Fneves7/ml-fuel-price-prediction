# -*- coding: utf-8 -*-
"""
02_classificacao.py — Família CLASSIFICAÇÃO (aprendizagem supervisionada).
Algoritmos dos prompts: regressão logística, SVM linear, SVM kernel (RBF),
KNN, Naïve Bayes. Alvo: o preço sobe amanhã? (1/0).
Nota: o SVM kernel (RBF) escala mal (~O(n²)); treinamos numa amostra do treino
para ser tratável no ambiente — fica documentado.
"""
import sys, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from comum import carregar, PASTA_FIG, RAIZ

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score

sns.set_theme(style="whitegrid", context="talk")
ALVO = "target_subida"


def aval(nome, y, p, L):
    acc = accuracy_score(y, p); f1 = f1_score(y, p, zero_division=0)
    print(f"  {nome:26s} accuracy={acc:.3f} | F1={f1:.3f}")
    L.append({"modelo": nome, "accuracy": acc, "f1": f1})


def main():
    print("=" * 66); print("FAMÍLIA: CLASSIFICAÇÃO  (alvo = sobe amanhã?)"); print("=" * 66)
    X_tr, y_tr, X_te, y_te, feats = carregar(ALVO, classif=True)
    print(f"[dados] treino {len(X_tr):,} | teste {len(X_te):,}")
    L = []
    aval("Baseline (maioritária)", y_te,
         DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr).predict(X_te), L)

    m = make_pipeline(StandardScaler(),
        LogisticRegression(max_iter=1000, class_weight="balanced")).fit(X_tr, y_tr)
    aval("Regressão logística", y_te, m.predict(X_te), L)

    m = make_pipeline(StandardScaler(),
        LinearSVC(class_weight="balanced", dual=False, max_iter=5000)).fit(X_tr, y_tr)
    aval("SVM linear", y_te, m.predict(X_te), L)

    # SVM kernel (RBF) — amostra do treino para ser tratável
    rng = np.random.RandomState(42)
    idx = rng.choice(len(X_tr), size=min(8000, len(X_tr)), replace=False)
    m = make_pipeline(StandardScaler(),
        SVC(kernel="rbf", C=2.0, gamma="scale", class_weight="balanced"))
    m.fit(X_tr.iloc[idx], y_tr.iloc[idx])
    aval("SVM kernel RBF (amostra 8k)", y_te, m.predict(X_te), L)

    m = make_pipeline(StandardScaler(),
        KNeighborsClassifier(n_neighbors=25)).fit(X_tr, y_tr)
    aval("KNN (k=25)", y_te, m.predict(X_te), L)

    m = make_pipeline(StandardScaler(), GaussianNB()).fit(X_tr, y_tr)
    aval("Naïve Bayes", y_te, m.predict(X_te), L)

    tab = pd.DataFrame(L).set_index("modelo")
    tab.round(3).to_csv(RAIZ / "dados" / "sup_classificacao.csv", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=tab.index, y=tab["accuracy"], hue=tab.index, palette="flare",
                legend=False, ax=ax)
    ax.axhline(tab.loc["Baseline (maioritária)", "accuracy"], color="gray",
               ls="--", lw=1)
    ax.set_ylabel("Accuracy"); ax.set_xlabel(""); ax.set_ylim(0.5, 0.85)
    ax.set_title("Classificação — accuracy por algoritmo")
    ax.tick_params(axis="x", rotation=25)
    for i, v in enumerate(tab["accuracy"]):
        ax.text(i, v, f"{v:.3f}", ha="center", va="bottom", fontsize=9)
    fig.savefig(PASTA_FIG / "sup_02_classificacao.png", dpi=120, bbox_inches="tight")
    print("[figura] sup_02_classificacao.png")


if __name__ == "__main__":
    main()
