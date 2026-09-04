# -*- coding: utf-8 -*-
"""B7 — Importância por PERMUTAÇÃO (mais fiável que a impureza).
Mede quanto a accuracy no teste cai quando se baralha cada variável."""
import sys; from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum_modelo import carregar, PASTA_FIG, DADOS
from lightgbm import LGBMClassifier
from sklearn.inspection import permutation_importance

sns.set_theme(style="whitegrid", context="talk")


def main():
    print("=" * 66); print("B7 — IMPORTÂNCIA POR PERMUTAÇÃO"); print("=" * 66)
    tr, te, feats = carregar(com_dummies=True)
    m = LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
        random_state=42, n_jobs=-1, verbose=-1).fit(tr[feats], tr["target_subida"])

    print("[perm] a calcular (5 repetições no conjunto de teste)…")
    r = permutation_importance(m, te[feats], te["target_subida"], n_repeats=5,
                               random_state=42, scoring="accuracy", n_jobs=-1)
    imp = pd.Series(r.importances_mean, index=feats).sort_values(ascending=False)
    imp.round(4).to_csv(DADOS / "resultados_permutacao.csv", encoding="utf-8")
    print("\nTop 12 variáveis (queda de accuracy ao baralhar):")
    print(imp.head(12).round(4).to_string())

    top = imp.head(15).sort_values()
    fig, ax = plt.subplots(figsize=(11, 8))
    sns.barplot(x=top.values, y=top.index, hue=top.index, palette="mako",
                legend=False, ax=ax)
    ax.set_title("B7 — Top 15 variáveis por permutação")
    ax.set_xlabel("Queda média de accuracy quando a variável é baralhada")
    ax.set_ylabel("")
    fig.savefig(PASTA_FIG / "21_permutacao.png", dpi=120, bbox_inches="tight")
    print("[figura] 21_permutacao.png")


if __name__ == "__main__":
    main()
