# -*- coding: utf-8 -*-
"""
04_modelo_regressao.py
======================
Fases 4 e 5 — Criação e avaliação do modelo de REGRESSÃO.

Pergunta:
    "Conseguimos estimar o VALOR do preço (€/L) de um combustível amanhã?"

Aprendizagem supervisionada (regressão):
    alvo = target_preco_amanha  (preço em €/L no dia seguinte)

Modelos comparados:
    - Baseline "persistência": amanhã = hoje  (referência forte a bater,
      porque o preço diário é muito auto-correlacionado)
    - Regressão Linear
    - Random Forest Regressor

Avaliação:
    - Divisão CRONOLÓGICA treino/teste
    - MAE (erro médio em €/L), RMSE, R²
    - comparação com a persistência: o modelo ganha alguma coisa?

Ferramentas: pandas, scikit-learn, matplotlib, seaborn.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
PASTA_FIG.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", context="talk")

DATA_CORTE = "2024-01-01"
COMB_REF = "Gasóleo especial"

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
ALVO = "target_preco_amanha"


def preparar_dados():
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    cols_comb = list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)

    colunas = ["data", "tipoCombustivel"] + FEATURES + cols_comb + [ALVO]
    df = df[colunas].dropna().reset_index(drop=True)

    treino = df[df["data"] < DATA_CORTE]
    teste = df[df["data"] >= DATA_CORTE]
    feats = FEATURES + cols_comb

    print(f"[dados] treino: {len(treino):,} | teste: {len(teste):,}")
    return treino, teste, feats


def avaliar(nome, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"\n>>> {nome}")
    print(f"    MAE={mae:.4f} €/L | RMSE={rmse:.4f} €/L | R²={r2:.4f}")
    return {"modelo": nome, "MAE_eur_L": mae, "RMSE_eur_L": rmse, "R2": r2}


def grafico_real_vs_previsto(teste, y_pred, nome, ficheiro):
    """Série temporal real vs previsto para o combustível de referência,
    apenas no período de teste."""
    sub = teste.copy()
    sub["previsto"] = y_pred
    sub = sub[sub["tipoCombustivel"] == COMB_REF].sort_values("data")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(sub["data"], sub[ALVO], label="Real", color="tab:blue", linewidth=1.8)
    ax.plot(sub["data"], sub["previsto"], label="Previsto", color="tab:orange",
            linewidth=1.2, alpha=0.8)
    ax.set_title(f"{nome} — preço real vs previsto ({COMB_REF}, teste 2024–2026)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (€/L)")
    ax.legend()
    fig.savefig(PASTA_FIG / ficheiro, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"    [figura] {ficheiro}")


def main():
    print("=" * 70)
    print("MODELO DE REGRESSÃO — qual o preço (€/L) amanhã?")
    print("=" * 70)
    treino, teste, feats = preparar_dados()
    X_tr, y_tr = treino[feats], treino[ALVO]
    X_te, y_te = teste[feats], teste[ALVO]
    resultados = []

    # 1) Baseline persistência: prever que amanhã = hoje
    resultados.append(avaliar("Baseline (amanhã = hoje)",
                              y_te, teste["preco_eur_l"].values))

    # 2) Regressão Linear
    lin = LinearRegression().fit(X_tr, y_tr)
    pred_lin = lin.predict(X_te)
    resultados.append(avaliar("Regressão Linear", y_te, pred_lin))

    # 3) Random Forest Regressor
    rf = RandomForestRegressor(
        n_estimators=300, max_depth=16, min_samples_leaf=3,
        random_state=42, n_jobs=-1)
    rf.fit(X_tr, y_tr)
    pred_rf = rf.predict(X_te)
    resultados.append(avaliar("Random Forest", y_te, pred_rf))
    grafico_real_vs_previsto(teste, pred_rf, "Random Forest",
                             "10_regressao_real_vs_previsto.png")

    tabela = pd.DataFrame(resultados).set_index("modelo").round(4)
    print("\n" + "-" * 70)
    print("RESUMO (conjunto de teste):")
    print(tabela.to_string())

    # Quanto é que os modelos ganham (ou perdem) face à persistência?
    mae_base = tabela.loc["Baseline (amanhã = hoje)", "MAE_eur_L"]
    for nome in ["Regressão Linear", "Random Forest"]:
        ganho = (mae_base - tabela.loc[nome, "MAE_eur_L"]) / mae_base * 100
        print(f"    {nome}: {ganho:+.1f}% de MAE face ao baseline "
              f"({'melhor' if ganho > 0 else 'pior'})")

    tabela.to_csv(RAIZ / "dados" / "resultados_regressao.csv", encoding="utf-8")
    print(f"\n[ok] Resultados guardados em dados/resultados_regressao.csv")


if __name__ == "__main__":
    main()
