# -*- coding: utf-8 -*-
"""
09_probabilidade.py — Backlog B8: previsão com PROBABILIDADE calibrada.

Em vez de só "sobe/desce", damos a probabilidade ("sobe com 72 % de confiança").
Para a probabilidade ser fiável, CALIBRAMO-LA (isotónica) e medimos:
  - Brier score (erro da probabilidade) antes/depois da calibração;
  - curva de fiabilidade (o que o modelo diz vs o que acontece);
  - "quando o modelo tem >X % de confiança, acerta quanto?".

Divisão temporal: treino < 2023 (ajuste) · 2023 (calibração) · ≥2024 (teste).
Modelo base: LightGBM.
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns

from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.frozen import FrozenEstimator
from sklearn.metrics import brier_score_loss, accuracy_score
from lightgbm import LGBMClassifier

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
sns.set_theme(style="whitegrid", context="talk")
ALVO = "target_subida"

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


def main():
    print("=" * 66); print("B8 — PREVISÃO COM PROBABILIDADE (calibrada)"); print("=" * 66)
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    feats = FEATURES + list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)
    df = df[["data"] + feats + [ALVO]].dropna().reset_index(drop=True)
    df[ALVO] = df[ALVO].astype(int)

    ajuste = df[df["data"] < "2023-01-01"]
    calib = df[(df["data"] >= "2023-01-01") & (df["data"] < "2024-01-01")]
    teste = df[df["data"] >= "2024-01-01"]
    print(f"[dados] ajuste {len(ajuste):,} | calibração {len(calib):,} | teste {len(teste):,}")

    base = LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
        random_state=42, n_jobs=-1, verbose=-1)
    base.fit(ajuste[feats], ajuste[ALVO])
    cal = CalibratedClassifierCV(FrozenEstimator(base), method="isotonic")
    cal.fit(calib[feats], calib[ALVO])

    y = teste[ALVO].values
    p_base = base.predict_proba(teste[feats])[:, 1]
    p_cal = cal.predict_proba(teste[feats])[:, 1]

    print(f"\nBrier score (menor=melhor):  sem calibrar={brier_score_loss(y, p_base):.4f}"
          f"  |  calibrado={brier_score_loss(y, p_cal):.4f}")
    print(f"Accuracy (limiar 0,5): {accuracy_score(y, (p_cal>=0.5).astype(int)):.3f}")

    # "confiança vs acerto": confiança = distância a 0,5
    conf = np.abs(p_cal - 0.5) + 0.5
    pred = (p_cal >= 0.5).astype(int)
    acerto = (pred == y)
    print("\nQuando o modelo tem confiança ≥ …:")
    linhas = []
    for lim in [0.5, 0.6, 0.7, 0.8, 0.9]:
        m = conf >= lim
        if m.sum():
            print(f"  ≥ {lim*100:.0f}%: cobre {m.mean()*100:5.1f}% dos dias | "
                  f"acerta {acerto[m].mean()*100:.1f}%")
            linhas.append({"confianca_min": lim, "cobertura": m.mean(),
                           "acerto": acerto[m].mean()})
    pd.DataFrame(linhas).to_csv(RAIZ / "dados" / "resultados_probabilidade.csv",
                                index=False, encoding="utf-8")

    # Figura: curva de fiabilidade + acerto por nível de confiança
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fx, fy = calibration_curve(y, p_cal, n_bins=10, strategy="quantile")
    ax1.plot([0, 1], [0, 1], "--", color="gray", label="ideal")
    ax1.plot(fy, fx, "o-", color="tab:blue", label="modelo calibrado")
    ax1.set_xlabel("Probabilidade prevista de 'sobe'")
    ax1.set_ylabel("Frequência real de 'sobe'")
    ax1.set_title("Curva de fiabilidade (calibração)"); ax1.legend(fontsize=11)

    L = pd.DataFrame(linhas)
    ax2.bar(range(len(L)), L["acerto"]*100, color="tab:green", alpha=0.85)
    ax2.plot(range(len(L)), L["cobertura"]*100, "o-", color="tab:orange", label="cobertura")
    ax2.set_xticks(range(len(L)))
    ax2.set_xticklabels([f"≥{int(c*100)}%" for c in L["confianca_min"]])
    ax2.set_xlabel("Confiança mínima"); ax2.set_ylabel("%")
    ax2.set_title("Acerto e cobertura por confiança"); ax2.set_ylim(0, 100)
    for i, v in enumerate(L["acerto"]*100):
        ax2.text(i, v+1, f"{v:.0f}%", ha="center", fontsize=10)
    ax2.legend(fontsize=11)
    fig.savefig(PASTA_FIG / "18_probabilidade.png", dpi=120, bbox_inches="tight")
    print("\n[figura] 18_probabilidade.png")


if __name__ == "__main__":
    main()
