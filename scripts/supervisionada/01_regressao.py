# -*- coding: utf-8 -*-
"""
01_regressao.py — Família REGRESSÃO (aprendizagem supervisionada).
Algoritmos dos prompts: regressão linear simples, linear múltipla, polinomial,
Ridge, Lasso. Alvo: preço (€/L) do dia seguinte. Baseline: "amanhã = hoje".
"""
import sys, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from comum import carregar, PASTA_FIG, RAIZ

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sns.set_theme(style="whitegrid", context="talk")
ALVO = "target_preco_amanha"
SIMPLES = ["preco_eur_l"]                              # 1 preditor (reg. simples)
POLY = ["preco_eur_l", "brent_eur", "variacao_1d", "media_movel_7d",
        "desvio_media_30d", "brent_eur_var_pct_7d"]    # subconjunto p/ polinomial


def aval(nome, y, p, linhas):
    mae = mean_absolute_error(y, p); rmse = np.sqrt(mean_squared_error(y, p))
    r2 = r2_score(y, p)
    print(f"  {nome:24s} MAE={mae:.4f} | RMSE={rmse:.4f} | R²={r2:.4f}")
    linhas.append({"modelo": nome, "MAE": mae, "RMSE": rmse, "R2": r2})


def main():
    print("=" * 66); print("FAMÍLIA: REGRESSÃO  (alvo = preço €/L amanhã)"); print("=" * 66)
    X_tr, y_tr, X_te, y_te, feats = carregar(ALVO)
    print(f"[dados] treino {len(X_tr):,} | teste {len(X_te):,}")
    L = []
    # Baseline persistência
    aval("Baseline (amanhã=hoje)", y_te, X_te["preco_eur_l"].values, L)
    # Regressão linear simples (1 variável)
    m = LinearRegression().fit(X_tr[SIMPLES], y_tr)
    aval("Reg. linear simples", y_te, m.predict(X_te[SIMPLES]), L)
    # Regressão linear múltipla
    m = LinearRegression().fit(X_tr, y_tr)
    aval("Reg. linear múltipla", y_te, m.predict(X_te), L)
    # Regressão polinomial (grau 2 num subconjunto)
    m = make_pipeline(StandardScaler(), PolynomialFeatures(2, include_bias=False),
                      LinearRegression()).fit(X_tr[POLY], y_tr)
    aval("Reg. polinomial (g2)", y_te, m.predict(X_te[POLY]), L)
    # Ridge e Lasso (com normalização)
    m = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(X_tr, y_tr)
    aval("Ridge", y_te, m.predict(X_te), L)
    m = make_pipeline(StandardScaler(), Lasso(alpha=0.001, max_iter=5000)).fit(X_tr, y_tr)
    aval("Lasso", y_te, m.predict(X_te), L)

    tab = pd.DataFrame(L).set_index("modelo")
    tab.round(4).to_csv(RAIZ / "dados" / "sup_regressao.csv", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=tab.index, y=tab["MAE"]*1000, hue=tab.index, palette="crest",
                legend=False, ax=ax)
    ax.set_ylabel("MAE (milésimos de €/L)"); ax.set_xlabel("")
    ax.set_title("Regressão — erro por algoritmo (menor é melhor)")
    ax.tick_params(axis="x", rotation=25)
    for i, v in enumerate(tab["MAE"]*1000):
        ax.text(i, v, f"{v:.1f}", ha="center", va="bottom", fontsize=9)
    fig.savefig(PASTA_FIG / "sup_01_regressao.png", dpi=120, bbox_inches="tight")
    print("[figura] sup_01_regressao.png")


if __name__ == "__main__":
    main()
