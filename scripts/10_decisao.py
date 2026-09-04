# -*- coding: utf-8 -*-
"""
10_decisao.py — Backlog B9: "atesto hoje ou espero um dia?".

Transforma a previsão numa DECISÃO com valor em euros. Regra:
  - se o modelo prevê que o preço SOBE amanhã  -> atestar HOJE (evita a subida);
  - se prevê que DESCE/mantém                   -> ESPERAR um dia (paga amanhã).

Compara, no período de teste (2024+):
  - "Sempre hoje" (comportamento ingénuo)  -> paga o preço de hoje;
  - "Modelo"                                -> segue a regra acima;
  - "Oráculo" (perfeito, impossível)        -> paga sempre o menor dos dois dias.
Mede a poupança média por litro e por depósito de 50 L.
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
from lightgbm import LGBMClassifier

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
sns.set_theme(style="whitegrid", context="talk")
ALVO = "target_subida"; TANQUE = 50

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
    print("=" * 66); print('B9 — DECISÃO: "atesto hoje ou espero?"'); print("=" * 66)
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    feats = FEATURES + list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)
    # preco_eur_l já está em feats; só juntamos as colunas extra (evita duplicados)
    cols = ["data", "tipoCombustivel", "preco_amanha"] + feats + [ALVO]
    df = df[cols].dropna().reset_index(drop=True)
    df[ALVO] = df[ALVO].astype(int)

    tr = df[df["data"] < "2024-01-01"]
    te = df[df["data"] >= "2024-01-01"].copy()
    m = LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
        random_state=42, n_jobs=-1, verbose=-1).fit(tr[feats], tr[ALVO])
    te["prev_sobe"] = m.predict(te[feats])

    hoje, amanha = te["preco_eur_l"].values, te["preco_amanha"].values
    # custo de cada estratégia (€/L pago)
    custo_hoje = hoje
    custo_modelo = np.where(te["prev_sobe"] == 1, hoje, amanha)   # espera se prevê descida
    custo_oraculo = np.minimum(hoje, amanha)

    def resumo(nome, custo):
        poup = (custo_hoje.mean() - custo.mean())
        return {"estrategia": nome, "preco_medio": custo.mean(),
                "poup_eur_L": poup, "poup_tanque_50L": poup * TANQUE}

    R = [resumo("Sempre hoje (ingénuo)", custo_hoje),
         resumo("Modelo (atesto/espero)", custo_modelo),
         resumo("Oráculo (perfeito)", custo_oraculo)]
    tab = pd.DataFrame(R).set_index("estrategia")
    captura = (tab.loc["Modelo (atesto/espero)", "poup_eur_L"] /
               tab.loc["Oráculo (perfeito)", "poup_eur_L"] * 100)

    print(f"[dados] decisões simuladas: {len(te):,} (2024+)")
    print(tab.round(4).to_string())
    print(f"\n>> O modelo poupa {tab.loc['Modelo (atesto/espero)','poup_eur_L']*100:.2f} "
          f"cêntimos/L ({tab.loc['Modelo (atesto/espero)','poup_tanque_50L']:.2f} €/depósito de 50 L)")
    print(f">> Captura {captura:.0f}% da poupança máxima possível (oráculo).")
    # quando esperou, acertou?
    esperou = te["prev_sobe"] == 0
    desceu = amanha < hoje
    print(f">> Nos dias em que ESPEROU, o preço desceu mesmo em {desceu[esperou].mean()*100:.0f}% das vezes.")
    tab.round(4).to_csv(RAIZ / "dados" / "resultados_decisao.csv", encoding="utf-8")

    # Figura: poupança por depósito
    fig, ax = plt.subplots(figsize=(11, 6))
    cores = ["tab:gray", "tab:green", "tab:blue"]
    vals = tab["poup_tanque_50L"].values
    ax.bar(range(3), vals, color=cores)
    ax.set_xticks(range(3)); ax.set_xticklabels(tab.index, fontsize=12)
    ax.set_ylabel("Poupança por depósito de 50 L (€)")
    ax.set_title("Quanto vale seguir o modelo? (vs atestar sempre hoje)")
    for i, v in enumerate(vals):
        ax.text(i, v, f"{v:.2f} €", ha="center", va="bottom", fontsize=12)
    ax.text(1, vals[1]/2, f"{captura:.0f}% do\noráculo", ha="center",
            color="white", fontsize=12, fontweight="bold")
    fig.savefig(PASTA_FIG / "19_decisao.png", dpi=120, bbox_inches="tight")
    print("[figura] 19_decisao.png")


if __name__ == "__main__":
    main()
