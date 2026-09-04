# -*- coding: utf-8 -*-
"""B12 — Curva de skill por HORIZONTE (1, 3, 7, 14 dias).
Mostra como a previsibilidade da direção cai à medida que o horizonte aumenta."""
import sys; from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum_modelo import FEATURES_NUM, ENTRADA, PASTA_FIG, DADOS, DATA_CORTE
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score

sns.set_theme(style="whitegrid", context="talk")
HORIZONTES = [1, 3, 7, 14]


def main():
    print("=" * 66); print("B12 — SKILL POR HORIZONTE (1, 3, 7, 14 dias)"); print("=" * 66)
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    feats = FEATURES_NUM + list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)
    g = df.groupby("tipoCombustivel")["preco_eur_l"]

    linhas = []
    for h in HORIZONTES:
        fut = g.shift(-h)
        d = df.assign(tgt=(fut > df["preco_eur_l"]).astype("float"))
        d = d.dropna(subset=feats + ["tgt"])
        d["tgt"] = d["tgt"].astype(int)
        tr = d[d["data"] < DATA_CORTE]; te = d[d["data"] >= DATA_CORTE]
        base = max(te["tgt"].mean(), 1 - te["tgt"].mean())   # classe maioritária
        m = LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=31,
            subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
            random_state=42, n_jobs=-1, verbose=-1).fit(tr[feats], tr["tgt"])
        acc = accuracy_score(te["tgt"], m.predict(te[feats]))
        ganho = (acc - base) * 100
        print(f"  {h:>2}d: accuracy={acc:.3f} | baseline={base:.3f} | +{ganho:.1f} pp")
        linhas.append({"horizonte": h, "accuracy": acc, "baseline": base})

    tab = pd.DataFrame(linhas).set_index("horizonte")
    tab.round(3).to_csv(DADOS / "resultados_skill_horizonte.csv", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.plot(tab.index, tab["accuracy"], "o-", color="tab:green", lw=2.5,
            markersize=10, label="Modelo (LightGBM)")
    ax.plot(tab.index, tab["baseline"], "s--", color="gray", lw=1.5, label="Baseline (acaso)")
    ax.fill_between(tab.index, tab["baseline"], tab["accuracy"], alpha=0.15, color="tab:green")
    for h, r in tab.iterrows():
        ax.annotate(f"{r['accuracy']*100:.0f}%", (h, r["accuracy"]),
                    textcoords="offset points", xytext=(0, 12), ha="center", fontsize=12)
    ax.set_xticks(HORIZONTES)
    ax.set_xlabel("Horizonte de previsão (dias)"); ax.set_ylabel("Accuracy")
    ax.set_title("B12 — a previsibilidade da direção cai com o horizonte")
    ax.set_ylim(0.45, 0.85); ax.legend()
    fig.savefig(PASTA_FIG / "24_skill_horizonte.png", dpi=120, bbox_inches="tight")
    print("[figura] 24_skill_horizonte.png")


if __name__ == "__main__":
    main()
