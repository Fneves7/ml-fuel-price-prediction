# -*- coding: utf-8 -*-
"""B6 — Modelo ÚNICO (pooled, com one-hot) vs modelos POR COMBUSTÍVEL.
Alvo: sobe amanhã? Vê se separar por combustível melhora face ao one-hot."""
import sys; from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum_modelo import carregar, PASTA_FIG, DADOS
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score

sns.set_theme(style="whitegrid", context="talk")
LGB = dict(n_estimators=400, learning_rate=0.05, num_leaves=31, subsample=0.8,
           colsample_bytree=0.8, class_weight="balanced", random_state=42,
           n_jobs=-1, verbose=-1)


def main():
    print("=" * 66); print("B6 — MODELO ÚNICO (pooled) vs POR COMBUSTÍVEL"); print("=" * 66)
    # Pooled (com one-hot)
    tr, te, feats = carregar(com_dummies=True)
    pool = LGBMClassifier(**LGB).fit(tr[feats], tr["target_subida"])
    te = te.copy(); te["prev_pool"] = pool.predict(te[feats])

    # Por combustível (sem one-hot)
    trn, ten, featsn = carregar(com_dummies=False)
    linhas = []
    for comb in sorted(te["tipoCombustivel"].unique()):
        acc_pool = accuracy_score(te.loc[te.tipoCombustivel == comb, "target_subida"],
                                  te.loc[te.tipoCombustivel == comb, "prev_pool"])
        trf = trn[trn.tipoCombustivel == comb]; tef = ten[ten.tipoCombustivel == comb]
        m = LGBMClassifier(**LGB).fit(trf[featsn], trf["target_subida"])
        acc_ind = accuracy_score(tef["target_subida"], m.predict(tef[featsn]))
        linhas.append({"combustivel": comb, "pooled": acc_pool, "individual": acc_ind})
        print(f"  {comb:22s} pooled={acc_pool:.3f} | individual={acc_ind:.3f}")

    tab = pd.DataFrame(linhas).set_index("combustivel")
    print(f"\nMédia: pooled={tab['pooled'].mean():.3f} | individual={tab['individual'].mean():.3f}")
    tab.round(3).to_csv(DADOS / "resultados_por_combustivel.csv", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(13, 6))
    x = np.arange(len(tab)); w = 0.4
    ax.bar(x - w/2, tab["pooled"], w, label="Modelo único (pooled)", color="tab:blue")
    ax.bar(x + w/2, tab["individual"], w, label="Por combustível", color="tab:orange")
    ax.set_xticks(x); ax.set_xticklabels(tab.index, rotation=30, ha="right", fontsize=10)
    ax.set_ylabel("Accuracy"); ax.set_ylim(0.6, 0.9)
    ax.set_title("B6 — modelo único vs por combustível"); ax.legend()
    fig.savefig(PASTA_FIG / "20_por_combustivel.png", dpi=120, bbox_inches="tight")
    print("[figura] 20_por_combustivel.png")


if __name__ == "__main__":
    main()
