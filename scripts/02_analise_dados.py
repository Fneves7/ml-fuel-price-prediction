# -*- coding: utf-8 -*-
"""
02_analise_dados.py
===================
Fase 3 do projeto — Análise Exploratória dos Dados (EDA).

Objetivo:
    Perceber os dados ANTES de modelar: como evoluíram os preços, como se
    relacionam com o petróleo Brent e o câmbio EUR/USD, que sazonalidade existe
    e como está distribuído o alvo (sobe/desce). Cada gráfico é guardado em
    figuras/ para usar na apresentação.

Ferramentas: pandas, matplotlib, seaborn.
Entrada:  dados/dataset_enriquecido.csv  (gerado pelo script 01)
Saída:    figuras/*.png
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_FIG = RAIZ / "figuras"
PASTA_FIG.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")
PALETA = "tab10"

# Combustível de referência para gráficos detalhados (histórico completo desde 2008)
COMB_REF = "Gasóleo especial"


def guardar(fig, nome):
    caminho = PASTA_FIG / nome
    fig.savefig(caminho, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"[figura] {caminho.name}")


def carregar():
    # encoding explícito: neste sistema o pandas usaria cp1252 por omissão e
    # corromperia os acentos (ex.: "Gasóleo").
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    print(f"[dados] {len(df):,} linhas | {df['data'].min().date()} a {df['data'].max().date()}")
    return df


# --------------------------------------------------------------------------- #
# 1. Evolução dos preços de todos os combustíveis                             #
# --------------------------------------------------------------------------- #
def grafico_evolucao_precos(df):
    fig, ax = plt.subplots(figsize=(14, 7))
    for comb, sub in df.groupby("tipoCombustivel"):
        sub = sub.sort_values("data")
        ax.plot(sub["data"], sub["preco_eur_l"], label=comb, linewidth=1.2)
    ax.set_title("Evolução do preço médio diário por combustível (Portugal, 2008–2026)")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Preço (€/litro)")
    ax.legend(fontsize=9, ncol=2, loc="upper left")
    guardar(fig, "01_evolucao_precos.png")


# --------------------------------------------------------------------------- #
# 2. Preço do combustível vs Brent (USD e EUR)                                #
# --------------------------------------------------------------------------- #
def grafico_preco_vs_brent(df):
    sub = df[df["tipoCombustivel"] == COMB_REF].sort_values("data")
    fig, ax1 = plt.subplots(figsize=(14, 7))
    ax1.plot(sub["data"], sub["preco_eur_l"], color="tab:blue",
             label=f"{COMB_REF} (€/L)", linewidth=1.6)
    ax1.set_xlabel("Ano")
    ax1.set_ylabel(f"{COMB_REF} (€/litro)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.plot(sub["data"], sub["brent_eur"], color="tab:red", alpha=0.6,
             label="Brent (€/barril)", linewidth=1.2)
    ax2.set_ylabel("Brent (€/barril)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")
    ax2.grid(False)

    ax1.set_title(f"{COMB_REF} vs Petróleo Brent em euros — andam juntos?")
    guardar(fig, "02_preco_vs_brent.png")


# --------------------------------------------------------------------------- #
# 3. Mapa de calor de correlações                                             #
# --------------------------------------------------------------------------- #
def grafico_correlacoes(df):
    cols = ["preco_eur_l", "brent_usd", "eur_usd", "brent_eur",
            "brent_eur_media_movel_7d", "media_movel_7d", "media_movel_30d",
            "variacao_pct_1d", "brent_eur_var_pct_1d", "brent_eur_var_pct_7d"]
    sub = df[df["tipoCombustivel"] == COMB_REF][cols]
    corr = sub.corr()
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, cbar_kws={"shrink": .8}, ax=ax, annot_kws={"size": 8})
    ax.set_title(f"Correlações entre variáveis ({COMB_REF})")
    guardar(fig, "03_correlacoes.png")


# --------------------------------------------------------------------------- #
# 4. Distribuição do alvo (sobe / desce / mantém)                             #
# --------------------------------------------------------------------------- #
def grafico_distribuicao_alvo(df):
    d = df.dropna(subset=["preco_amanha"]).copy()
    diff = (d["preco_amanha"] - d["preco_eur_l"]).round(4)
    categorias = pd.cut(np.sign(diff), [-2, -0.5, 0.5, 2],
                        labels=["Desce", "Mantém", "Sobe"])
    contagem = categorias.value_counts().reindex(["Desce", "Mantém", "Sobe"])

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.barplot(x=contagem.index, y=contagem.values,
                hue=contagem.index, palette=["tab:red", "tab:gray", "tab:green"],
                legend=False, ax=ax)
    total = contagem.sum()
    for i, v in enumerate(contagem.values):
        ax.text(i, v + total * 0.01, f"{v:,}\n({v/total*100:.1f}%)",
                ha="center", fontsize=12)
    ax.set_title("Movimento do preço no dia seguinte (todos os combustíveis)")
    ax.set_ylabel("Nº de dias")
    guardar(fig, "04_distribuicao_alvo.png")


# --------------------------------------------------------------------------- #
# 5. Relação variação do Brent (7d) vs variação do preço (semana seguinte)    #
# --------------------------------------------------------------------------- #
def grafico_scatter_variacoes(df):
    sub = df[df["tipoCombustivel"] == COMB_REF].dropna(
        subset=["brent_eur_var_pct_7d", "variacao_7d"])
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.regplot(data=sub, x="brent_eur_var_pct_7d", y="variacao_7d",
                scatter_kws={"alpha": 0.15, "s": 12}, line_kws={"color": "red"},
                ax=ax)
    ax.axhline(0, color="gray", lw=0.8)
    ax.axvline(0, color="gray", lw=0.8)
    ax.set_title(f"Variação do Brent (7d) vs variação do preço ({COMB_REF})")
    ax.set_xlabel("Variação % do Brent em EUR nos últimos 7 dias")
    ax.set_ylabel("Variação do preço nos últimos 7 dias (€/L)")
    guardar(fig, "05_scatter_brent_vs_preco.png")


# --------------------------------------------------------------------------- #
# 6. Sazonalidade: preço médio por mês e por dia da semana                    #
# --------------------------------------------------------------------------- #
def grafico_sazonalidade(df):
    sub = df[df["tipoCombustivel"] == COMB_REF]
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sns.boxplot(data=sub, x="mes", y="variacao_pct_1d", ax=axes[0],
                color="tab:blue", fliersize=1)
    axes[0].set_title("Variação diária (%) por mês")
    axes[0].set_xlabel("Mês")
    axes[0].set_ylabel("Variação diária do preço (%)")
    axes[0].set_ylim(-2, 2)

    nomes = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    sns.boxplot(data=sub, x="dia_semana", y="variacao_pct_1d", ax=axes[1],
                color="tab:green", fliersize=1)
    axes[1].set_title("Variação diária (%) por dia da semana")
    axes[1].set_xlabel("Dia da semana")
    axes[1].set_xticks(range(7))
    axes[1].set_xticklabels(nomes)
    axes[1].set_ylabel("")
    axes[1].set_ylim(-2, 2)
    fig.suptitle(f"Sazonalidade das variações de preço ({COMB_REF})", y=1.02)
    guardar(fig, "06_sazonalidade.png")


# --------------------------------------------------------------------------- #
# 7. Decomposição do preço em impostos (ISP + IVA) vs componente comercial     #
# --------------------------------------------------------------------------- #
def grafico_decomposicao_impostos(df):
    sub = df[df["tipoCombustivel"] == COMB_REF].sort_values("data").dropna(
        subset=["preco_eur_l", "isp_eur_l"])
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.stackplot(
        sub["data"],
        sub["preco_sem_impostos_eur_l"].clip(lower=0),
        sub["isp_eur_l"],
        sub["valor_iva_eur_l"],
        labels=["Componente comercial + matéria-prima", "ISP", "IVA"],
        colors=["#4c72b0", "#dd8452", "#c44e52"], alpha=0.9)
    ax.plot(sub["data"], sub["preco_eur_l"], color="black", lw=1,
            label="Preço final")
    ax.set_title(f"Decomposição do preço em impostos ({COMB_REF})\n"
                 f"— repare-se na descida do ISP em 2022")
    ax.set_xlabel("Ano")
    ax.set_ylabel("€/litro")
    ax.legend(loc="upper left", fontsize=10)
    guardar(fig, "11_decomposicao_impostos.png")


def grafico_carga_fiscal(df):
    media = df.groupby("tipoCombustivel")["carga_fiscal_pct"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(x=media.values, y=media.index, hue=media.index,
                palette="rocket", legend=False, ax=ax)
    for i, v in enumerate(media.values):
        ax.text(v + 0.5, i, f"{v:.0f}%", va="center", fontsize=11)
    ax.set_title("Carga fiscal média por combustível (% do preço à bomba)")
    ax.set_xlabel("Impostos (ISP + IVA) em % do preço")
    ax.set_ylabel("")
    guardar(fig, "12_carga_fiscal.png")


def main():
    print("=" * 70)
    print("ANÁLISE EXPLORATÓRIA DOS DADOS")
    print("=" * 70)
    df = carregar()

    # Resumo estatístico rápido no terminal
    print("\nEstatística do preço por combustível (€/L):")
    resumo = df.groupby("tipoCombustivel")["preco_eur_l"].agg(
        ["min", "mean", "max"]).round(3)
    print(resumo.to_string())

    print("\nCorrelação do preço com os drivers (por combustível):")
    for comb, sub in df.groupby("tipoCombustivel"):
        c = sub["preco_eur_l"].corr(sub["brent_eur"])
        print(f"  {comb:24s}  corr(preço, Brent€) = {c:.3f}")

    print()
    grafico_evolucao_precos(df)
    grafico_preco_vs_brent(df)
    grafico_correlacoes(df)
    grafico_distribuicao_alvo(df)
    grafico_scatter_variacoes(df)
    grafico_sazonalidade(df)
    grafico_decomposicao_impostos(df)
    grafico_carga_fiscal(df)
    print("-" * 70)
    print(f"[ok] {len(list(PASTA_FIG.glob('*.png')))} figuras guardadas em {PASTA_FIG}")


if __name__ == "__main__":
    main()
