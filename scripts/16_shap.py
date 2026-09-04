# -*- coding: utf-8 -*-
"""B11 — Explicabilidade com SHAP.
Mostra como cada variável empurra a previsão (para 'sobe' ou 'desce'),
para além da importância global. Gráfico summary (beeswarm)."""
import sys; from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum_modelo import carregar, PASTA_FIG
from lightgbm import LGBMClassifier
import shap


def main():
    print("=" * 66); print("B11 — EXPLICABILIDADE COM SHAP"); print("=" * 66)
    tr, te, feats = carregar(com_dummies=True)
    m = LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
        random_state=42, n_jobs=-1, verbose=-1).fit(tr[feats], tr["target_subida"])

    amostra = te[feats].sample(min(2000, len(te)), random_state=42)
    print(f"[shap] a calcular valores SHAP para {len(amostra)} exemplos…")
    expl = shap.TreeExplainer(m)
    sv = expl.shap_values(amostra)
    if isinstance(sv, list):        # binário -> lista [classe0, classe1]
        sv = sv[1]

    plt.figure()
    shap.summary_plot(sv, amostra, max_display=15, show=False, plot_size=(11, 8))
    plt.title("B11 — SHAP: impacto de cada variável na previsão de 'sobe'", fontsize=13)
    plt.tight_layout()
    plt.savefig(PASTA_FIG / "23_shap_summary.png", dpi=120, bbox_inches="tight")
    plt.close()
    print("[figura] 23_shap_summary.png")

    # top variáveis por |SHAP| médio
    imp = pd.Series(np.abs(sv).mean(0), index=feats).sort_values(ascending=False)
    print("\nTop 10 variáveis por |SHAP| médio:")
    print(imp.head(10).round(4).to_string())


if __name__ == "__main__":
    main()
