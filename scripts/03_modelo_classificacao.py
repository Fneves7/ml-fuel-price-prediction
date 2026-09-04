# -*- coding: utf-8 -*-
"""
03_modelo_classificacao.py
==========================
Fases 4 e 5 — Criação e avaliação do modelo de CLASSIFICAÇÃO.

Pergunta do projeto:
    "Conseguimos prever se o preço de um combustível SOBE ou DESCE amanhã?"

Aprendizagem supervisionada (classificação binária):
    alvo = target_subida  (1 = sobe amanhã | 0 = desce ou mantém)

Modelos comparados:
    - Baseline "classe maioritária" (DummyClassifier) -> referência a bater
    - Regressão Logística (linear, com normalização)
    - Random Forest (não-linear, com importância de variáveis)

Avaliação honesta:
    - Divisão CRONOLÓGICA treino/teste (nunca aleatória em séries temporais)
    - accuracy, precisão, recall, F1, matriz de confusão
    - comparação obrigatória com o baseline

Ferramentas: pandas, scikit-learn, matplotlib, seaborn.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
PASTA_FIG.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", context="talk")

DATA_CORTE = "2024-01-01"   # treino: antes desta data | teste: a partir dela

# Variáveis de entrada (features). NÃO incluímos nada do "futuro"
# (preco_amanha/targets) nem o ano (não generaliza no split cronológico).
FEATURES = [
    # preço atual e histórico (conhecidos no dia t)
    "preco_eur_l", "preco_lag_1d", "preco_lag_7d", "preco_lag_30d",
    "media_movel_7d", "media_movel_30d",
    "variacao_1d", "variacao_pct_1d", "variacao_7d", "desvio_media_30d",
    # drivers externos
    "brent_usd", "eur_usd", "brent_eur", "brent_eur_media_movel_7d",
    "brent_usd_var_pct_1d", "brent_usd_var_pct_7d",
    "eur_usd_var_pct_1d", "eur_usd_var_pct_7d",
    "brent_eur_var_pct_1d", "brent_eur_var_pct_7d",
    # impostos (ISP de referência + IVA exato) e decomposição do preço
    "isp_eur_l", "iva_taxa", "carga_fiscal_pct", "preco_sem_impostos_eur_l",
    # calendário
    "mes", "trimestre", "semana_ano", "dia_semana", "fim_de_semana", "feriado",
]
ALVO = "target_subida"


def preparar_dados():
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")

    # one-hot do tipo de combustível (o modelo aprende diferenças entre eles)
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    cols_comb = list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)

    colunas = ["data"] + FEATURES + cols_comb + [ALVO]
    df = df[colunas].dropna().reset_index(drop=True)
    df[ALVO] = df[ALVO].astype(int)

    treino = df[df["data"] < DATA_CORTE]
    teste = df[df["data"] >= DATA_CORTE]

    feats = FEATURES + cols_comb
    X_tr, y_tr = treino[feats], treino[ALVO]
    X_te, y_te = teste[feats], teste[ALVO]

    print(f"[dados] treino: {len(X_tr):,} linhas (até {DATA_CORTE}) | "
          f"teste: {len(X_te):,} linhas (a partir de {DATA_CORTE})")
    print(f"[dados] % 'sobe' no treino: {y_tr.mean()*100:.1f}% | "
          f"no teste: {y_te.mean()*100:.1f}%")
    return X_tr, X_te, y_tr, y_te, feats


def avaliar(nome, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    print(f"\n>>> {nome}")
    print(f"    accuracy={acc:.3f} | precisão={prec:.3f} | "
          f"recall={rec:.3f} | F1={f1:.3f}")
    return {"modelo": nome, "accuracy": acc, "precisao": prec,
            "recall": rec, "f1": f1}


def matriz_confusao(y_true, y_pred, nome, ficheiro):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    sns.heatmap(cm, annot=True, fmt=",d", cmap="Blues", cbar=False,
                xticklabels=["Desce/Mantém", "Sobe"],
                yticklabels=["Desce/Mantém", "Sobe"], ax=ax)
    ax.set_title(f"Matriz de confusão — {nome}")
    ax.set_xlabel("Previsto")
    ax.set_ylabel("Real")
    fig.savefig(PASTA_FIG / ficheiro, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"    [figura] {ficheiro}")


def grafico_importancias(modelo, feats, ficheiro):
    imp = pd.Series(modelo.feature_importances_, index=feats).sort_values()[-15:]
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(x=imp.values, y=imp.index, hue=imp.index,
                palette="viridis", legend=False, ax=ax)
    ax.set_title("Top 15 variáveis mais importantes (Random Forest)")
    ax.set_xlabel("Importância")
    ax.set_ylabel("")
    fig.savefig(PASTA_FIG / ficheiro, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"    [figura] {ficheiro}")


def main():
    print("=" * 70)
    print("MODELO DE CLASSIFICAÇÃO — o preço SOBE amanhã?")
    print("=" * 70)
    X_tr, X_te, y_tr, y_te, feats = preparar_dados()
    resultados = []

    # 1) Baseline: prever sempre a classe maioritária
    base = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
    resultados.append(avaliar("Baseline (classe maioritária)",
                              y_te, base.predict(X_te)))

    # 2) Regressão Logística (com normalização)
    logit = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, class_weight="balanced"))
    logit.fit(X_tr, y_tr)
    pred_logit = logit.predict(X_te)
    resultados.append(avaliar("Regressão Logística", y_te, pred_logit))
    matriz_confusao(y_te, pred_logit, "Regressão Logística",
                    "07_confusao_logistica.png")

    # 3) Random Forest
    rf = RandomForestClassifier(
        n_estimators=300, max_depth=12, min_samples_leaf=5,
        class_weight="balanced", random_state=42, n_jobs=-1)
    rf.fit(X_tr, y_tr)
    pred_rf = rf.predict(X_te)
    resultados.append(avaliar("Random Forest", y_te, pred_rf))
    matriz_confusao(y_te, pred_rf, "Random Forest", "08_confusao_randomforest.png")
    grafico_importancias(rf, feats, "09_importancias_classificacao.png")

    print("\n" + "-" * 70)
    print("Relatório detalhado (Random Forest):")
    print(classification_report(y_te, pred_rf,
          target_names=["Desce/Mantém", "Sobe"], zero_division=0))

    # Tabela-resumo
    tabela = pd.DataFrame(resultados).set_index("modelo").round(3)
    print("RESUMO (conjunto de teste):")
    print(tabela.to_string())
    tabela.to_csv(RAIZ / "dados" / "resultados_classificacao.csv", encoding="utf-8")
    print(f"\n[ok] Resultados guardados em dados/resultados_classificacao.csv")


if __name__ == "__main__":
    main()
