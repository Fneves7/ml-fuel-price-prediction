# -*- coding: utf-8 -*-
"""B10 — Análise de erros: QUANDO é que o modelo falha?
Vê se os erros se concentram em dias de grande variação, certos dias da semana,
períodos de choque, ou combustíveis específicos."""
import sys; from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum_modelo import carregar, PASTA_FIG, DADOS
from lightgbm import LGBMClassifier

sns.set_theme(style="whitegrid", context="talk")
DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


def main():
    print("=" * 66); print("B10 — ANÁLISE DE ERROS (quando falha o modelo?)"); print("=" * 66)
    tr, te, feats = carregar(com_dummies=True, extra_cols=["preco_amanha"])
    m = LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
        random_state=42, n_jobs=-1, verbose=-1).fit(tr[feats], tr["target_subida"])
    te = te.copy()
    te["prev"] = m.predict(te[feats])
    te["erro"] = (te["prev"] != te["target_subida"]).astype(int)
    te["delta_abs"] = (te["preco_amanha"] - te["preco_eur_l"]).abs()
    print(f"[dados] teste {len(te):,} | taxa de erro global: {te['erro'].mean()*100:.1f}%")

    # 1) por magnitude da variação real
    te["mag"] = pd.cut(te["delta_abs"]*1000, [-0.1, 1, 3, 7, 1e9],
                       labels=["≈0 (<1)", "pequena (1-3)", "média (3-7)", "grande (>7)"])
    por_mag = te.groupby("mag", observed=True)["erro"].mean()*100
    # 2) por dia da semana
    por_dia = te.groupby("dia_semana")["erro"].mean()*100
    # 3) ao longo do tempo (erro mensal no período de teste)
    te["mes_ano"] = te["data"].dt.to_period("M").dt.to_timestamp()
    por_mes = te.groupby("mes_ano")["erro"].mean()*100
    # 4) por combustível
    por_comb = te.groupby("tipoCombustivel")["erro"].mean().sort_values()*100

    print("\nTaxa de erro por magnitude da variação (milésimos €/L):")
    print(por_mag.round(1).to_string())
    print(f"\nErro mensal: min {por_mes.min():.0f}% | máx {por_mes.max():.0f}%")
    pd.concat([por_mag.rename("erro_mag"), por_comb.rename("erro_comb")], axis=1
              ).to_csv(DADOS / "resultados_analise_erros.csv", encoding="utf-8")

    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    sns.barplot(x=por_mag.index, y=por_mag.values, hue=por_mag.index,
                palette="Reds", legend=False, ax=axes[0, 0])
    axes[0, 0].set_title("Erro por magnitude da variação real"); axes[0, 0].set_ylabel("Erro (%)")
    axes[0, 0].set_xlabel("")
    sns.barplot(x=[DIAS[i] for i in por_dia.index], y=por_dia.values,
                hue=[DIAS[i] for i in por_dia.index], palette="Blues", legend=False, ax=axes[0, 1])
    axes[0, 1].set_title("Erro por dia da semana"); axes[0, 1].set_ylabel("Erro (%)")
    axes[1, 0].plot(por_mes.index, por_mes.values, "o-", color="tab:purple", lw=1.8)
    axes[1, 0].axhline(te["erro"].mean()*100, color="gray", ls="--", lw=1, label="média")
    axes[1, 0].set_title("Erro ao longo do tempo (mensal)"); axes[1, 0].set_ylabel("Erro (%)")
    axes[1, 0].legend(); axes[1, 0].tick_params(axis="x", rotation=30)
    sns.barplot(x=por_comb.values, y=por_comb.index, hue=por_comb.index,
                palette="rocket", legend=False, ax=axes[1, 1])
    axes[1, 1].set_title("Erro por combustível"); axes[1, 1].set_xlabel("Erro (%)")
    axes[1, 1].set_ylabel("")
    fig.suptitle(f"B10 — Onde falha o modelo (erro global {te['erro'].mean()*100:.1f}%)", y=1.01)
    fig.tight_layout()
    fig.savefig(PASTA_FIG / "22_analise_erros.png", dpi=120, bbox_inches="tight")
    print("[figura] 22_analise_erros.png")


if __name__ == "__main__":
    main()
