# -*- coding: utf-8 -*-
"""
01_enriquecer_dataset.py
========================
Fase 2/3 do projeto — Seleção e enriquecimento do dataset.

Objetivo:
    O dataset original (Postos.csv) só tem o preço médio diário de cada
    combustível. Isso diz-nos O QUE aconteceu, mas não PORQUÊ. Para o modelo
    conseguir prever subidas/descidas, juntamos as VARIÁVEIS QUE EXPLICAM o
    preço do combustível em Portugal:

        1. Petróleo Brent (USD/barril)  -> principal driver internacional
        2. Câmbio EUR/USD               -> o petróleo é cotado em dólares
        3. Brent em EUR (derivado)      -> o custo real da matéria-prima para nós
        4. Calendário + feriados        -> sazonalidade e dias sem atualização

    Além disso criamos as FEATURES de séries temporais (lags, médias móveis,
    variações) e os ALVOS (targets) para os dois modelos:
        - Classificação: o preço SOBE amanhã? (1 = sobe, 0 = desce/mantém)
        - Regressão:     qual o preço (€/L) amanhã?

Fonte dos dados externos:
    FRED (Federal Reserve Bank of St. Louis) — descarregável em CSV sem chave:
        Brent : https://fred.stlouisfed.org/series/DCOILBRENTEU
        EURUSD: https://fred.stlouisfed.org/series/DEXUSEU

Saída:
    dados/dataset_enriquecido.csv  -> dataset final pronto para ML

Ferramentas: pandas, numpy (o requisito scikit-learn/matplotlib/seaborn é usado
nos scripts seguintes).
"""

from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Caminhos                                                                     #
# --------------------------------------------------------------------------- #
RAIZ = Path(__file__).resolve().parent.parent
PASTA_DADOS = RAIZ / "dados"
FICHEIRO_BASE = PASTA_DADOS / "Postos.csv"
PASTA_DADOS.mkdir(exist_ok=True)

CACHE_BRENT = PASTA_DADOS / "externo_brent.csv"
CACHE_EURUSD = PASTA_DADOS / "externo_eurusd.csv"
SAIDA = PASTA_DADOS / "dataset_enriquecido.csv"

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"


# --------------------------------------------------------------------------- #
# 1. Ler e limpar o dataset base                                              #
# --------------------------------------------------------------------------- #
def ler_precos_base() -> pd.DataFrame:
    """Lê Postos.csv, corrige o encoding e converte o preço para float (€/L)."""
    # O ficheiro é UTF-8 com BOM. Usamos utf-8-sig para remover o BOM e
    # descodificar corretamente os acentos ("Gasóleo") e o símbolo €.
    df = pd.read_csv(FICHEIRO_BASE, sep=";", encoding="utf-8-sig")

    df["data"] = pd.to_datetime(df["data"])

    # "1,3800 €" -> 1.38
    # Mantém apenas dígitos e a vírgula decimal (remove €, espaços, etc.),
    # depois troca a vírgula por ponto. Robusto a variações do símbolo de moeda.
    df["preco_eur_l"] = (
        df["precoMedio"]
        .str.replace(r"[^0-9,]", "", regex=True)  # fica só "1,3800"
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # LIMPEZA 1: há dias (ex.: 04–22/09/2015) com o preço gravado como 0,00 €.
    # Não é um preço real, é dado em falta -> convertemos para NaN para não
    # contaminar médias móveis, variações e alvos.
    n_zeros = int((df["preco_eur_l"] == 0).sum())
    df.loc[df["preco_eur_l"] == 0, "preco_eur_l"] = np.nan

    # LIMPEZA 2: preços absurdamente altos (> 3 €/L) são erros de registo
    # (ex.: 5,43 €/L na Gasolina especial 98 em 2009, quando rondava 1,3 €/L).
    # Nenhum combustível rodoviário em PT ultrapassou 3 €/L neste período.
    n_altos = int((df["preco_eur_l"] > 3).sum())
    df.loc[df["preco_eur_l"] > 3, "preco_eur_l"] = np.nan

    if n_zeros or n_altos:
        print(f"[base] limpeza: {n_zeros} preços a 0 € + {n_altos} preços > 3 €/L "
              f"tratados como dados em falta")

    df = df[["data", "tipoCombustivel", "preco_eur_l"]]
    df = df.sort_values(["tipoCombustivel", "data"]).reset_index(drop=True)
    print(f"[base] {len(df):,} linhas | "
          f"{df['tipoCombustivel'].nunique()} combustíveis | "
          f"{df['data'].min().date()} a {df['data'].max().date()}")
    return df


# --------------------------------------------------------------------------- #
# 2. Dados externos (Brent + EUR/USD) a partir do FRED, com cache local       #
# --------------------------------------------------------------------------- #
def descarregar_fred(series_id: str, cache: Path, nome_valor: str) -> pd.DataFrame:
    """Descarrega uma série do FRED em CSV. Usa/atualiza uma cache local para
    o projeto continuar reproduzível mesmo sem internet."""
    texto = None
    try:
        req = Request(FRED.format(series_id), headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as resp:
            texto = resp.read().decode("utf-8")
        cache.write_text(texto, encoding="utf-8")
        print(f"[fred] {series_id}: descarregado da internet e guardado em cache")
    except (URLError, TimeoutError, OSError) as erro:
        if cache.exists():
            texto = cache.read_text(encoding="utf-8")
            print(f"[fred] {series_id}: sem internet ({erro}); a usar cache local")
        else:
            raise RuntimeError(
                f"Não consegui descarregar {series_id} nem existe cache em {cache}"
            ) from erro

    from io import StringIO
    df = pd.read_csv(StringIO(texto))
    df.columns = ["data", nome_valor]
    df["data"] = pd.to_datetime(df["data"])
    # O FRED marca dias sem cotação com "." -> vira NaN
    df[nome_valor] = pd.to_numeric(df[nome_valor], errors="coerce")
    return df


def preparar_series_externas(data_min, data_max) -> pd.DataFrame:
    """Junta Brent + EUR/USD num calendário diário contínuo e preenche os
    fins-de-semana/feriados com o último valor conhecido (forward-fill), que é
    o comportamento real dos mercados (vale a última cotação)."""
    brent = descarregar_fred("DCOILBRENTEU", CACHE_BRENT, "brent_usd")
    eurusd = descarregar_fred("DEXUSEU", CACHE_EURUSD, "eur_usd")

    calendario = pd.DataFrame(
        {"data": pd.date_range(data_min, data_max, freq="D")}
    )
    ext = (
        calendario
        .merge(brent, on="data", how="left")
        .merge(eurusd, on="data", how="left")
        .sort_values("data")
    )

    # Preencher gaps: mercado fechado -> mantém-se a última cotação
    ext["brent_usd"] = ext["brent_usd"].ffill()
    ext["eur_usd"] = ext["eur_usd"].ffill()
    # Preencher eventuais NaN iniciais para trás (raro)
    ext[["brent_usd", "eur_usd"]] = ext[["brent_usd", "eur_usd"]].bfill()

    # Derivada económica: preço do barril de Brent em EUROS (o que nos custa)
    ext["brent_eur"] = ext["brent_usd"] / ext["eur_usd"]

    print(f"[externo] Brent + EUR/USD alinhados em "
          f"{len(ext):,} dias contínuos")
    return ext


# --------------------------------------------------------------------------- #
# 3. Feriados nacionais de Portugal (flag simples)                            #
# --------------------------------------------------------------------------- #
def _domingo_pascoa(ano: int) -> pd.Timestamp:
    """Algoritmo de Gauss/Computus para a data da Páscoa (rito ocidental)."""
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return pd.Timestamp(ano, mes, dia)


def feriados_pt(anos) -> set:
    """Conjunto de feriados nacionais fixos + móveis (dependentes da Páscoa)."""
    feriados = set()
    for ano in anos:
        pascoa = _domingo_pascoa(ano)
        moveis = {
            pascoa - pd.Timedelta(days=47),  # Carnaval (não oficial mas tolerado)
            pascoa - pd.Timedelta(days=2),   # Sexta-feira Santa
            pascoa,                          # Páscoa
            pascoa + pd.Timedelta(days=60),  # Corpo de Deus
        }
        fixos = {
            pd.Timestamp(ano, 1, 1),    # Ano Novo
            pd.Timestamp(ano, 4, 25),   # Dia da Liberdade
            pd.Timestamp(ano, 5, 1),    # Dia do Trabalhador
            pd.Timestamp(ano, 6, 10),   # Dia de Portugal
            pd.Timestamp(ano, 8, 15),   # Assunção
            pd.Timestamp(ano, 10, 5),   # Implantação da República
            pd.Timestamp(ano, 11, 1),   # Todos os Santos
            pd.Timestamp(ano, 12, 1),   # Restauração da Independência
            pd.Timestamp(ano, 12, 8),   # Imaculada Conceição
            pd.Timestamp(ano, 12, 25),  # Natal
        }
        feriados |= fixos | moveis
    return feriados


# --------------------------------------------------------------------------- #
# 3b. Impostos: ISP (referência) + IVA (exato) e decomposição do preço        #
# --------------------------------------------------------------------------- #
# NOTA DE HONESTIDADE DOS DADOS:
#   - O IVA é EXATO (taxa normal, bem documentada).
#   - O ISP é uma ESCALA DE REFERÊNCIA em degraus: usa os valores oficiais
#     (€/1000 L) que foi possível documentar em Portarias/fontes públicas
#     (nível padrão + corte da crise de 2022). Entre datas documentadas o valor
#     mantém-se constante; o mecanismo semanal de 2022–2023 está simplificado.
#     Fontes: Ordem dos Advogados (tabela ISP), Diário da República / Governo,
#     notícias RTP/DN/ECO. Ver Projeto.md e LOG.md.

# Grupo fiscal de cada combustível (o ISP difere entre gasolinas e gasóleos)
GRUPO_FISCAL = {
    "Gasolina 98": "gasolina",
    "Gasolina especial 95": "gasolina",
    "Gasolina especial 98": "gasolina",
    "Gasolina simples 95": "gasolina",
    "Gasóleo especial": "gasoleo",
    "Gasóleo simples": "gasoleo",
    "Biodiesel B15": "gasoleo",     # tributado como gasóleo
    "GPL Auto": "gpl",              # ISP muito baixo (regime próprio)
}

# ISP (€ por 1000 litros) — VALORES DE RESERVA (fallback).
# A escala é lida preferencialmente de `dados/isp_portarias.csv` (ver
# _carregar_isp_anchors). Este dicionário só é usado se o CSV não existir.
ISP_ANCHORS = {
    "gasolina": [
        ("2008-01-01", 526.64),   # nível padrão (mantido para trás, aproximação)
        ("2022-03-14", 489.92),   # início do corte da crise energética
        ("2022-05-02", 363.78),
        ("2022-05-09", 343.70),   # corte máximo (mantido durante 2022–2023)
        ("2024-01-01", 526.64),   # reposição gradual do padrão
        ("2025-11-28", 497.52),   # Portaria 427-A/2025
        ("2026-08-07", 462.13),   # Portaria 331-A/2026
    ],
    "gasoleo": [
        ("2008-01-01", 343.15),   # nível padrão (mantido para trás, aproximação)
        ("2022-03-14", 308.83),
        ("2022-03-28", 295.98),
        ("2022-05-02", 180.58),
        ("2022-05-09", 168.37),   # corte máximo (mantido durante 2022–2023)
        ("2024-01-01", 343.15),   # reposição gradual do padrão
        ("2025-11-28", 361.60),   # Portaria 427-A/2025
        ("2026-08-07", 302.44),   # Portaria 331-A/2026
    ],
    "gpl": [
        ("2008-01-01", 8.00),     # ISP do GPL Auto é quase nulo (~8 €/1000 L)
    ],
}


def _iva_taxa(datas: pd.Series) -> pd.Series:
    """Taxa normal de IVA em vigor (exata): 20% até jun/2010, 21% no 2.º semestre
    de 2010, 23% desde 01/01/2011."""
    taxa = pd.Series(0.23, index=datas.index)
    taxa[datas < pd.Timestamp("2011-01-01")] = 0.21
    taxa[datas < pd.Timestamp("2010-07-01")] = 0.20
    return taxa


FICHEIRO_ISP = PASTA_DADOS / "isp_portarias.csv"


def _carregar_isp_anchors() -> dict:
    """Lê a escala do ISP a partir de `dados/isp_portarias.csv` (formato:
    data_inicio, gasolina_eur_1000L, gasoleo_eur_1000L, gpl_eur_1000L, ...).
    Se o ficheiro não existir, usa os valores embutidos em ISP_ANCHORS.
    Assim, basta substituir/expandir o CSV (ex.: por uma série oficial completa
    do Diário da República) para o pipeline usar os novos valores."""
    if not FICHEIRO_ISP.exists():
        print("[isp] a usar escala embutida (CSV isp_portarias.csv não encontrado)")
        return {g: [(d, v) for d, v in a] for g, a in ISP_ANCHORS.items()}

    tab = pd.read_csv(FICHEIRO_ISP, encoding="utf-8")
    tab["data_inicio"] = pd.to_datetime(tab["data_inicio"])
    tab = tab.sort_values("data_inicio")
    anchors = {
        "gasolina": list(zip(tab["data_inicio"], tab["gasolina_eur_1000L"])),
        "gasoleo": list(zip(tab["data_inicio"], tab["gasoleo_eur_1000L"])),
        "gpl": list(zip(tab["data_inicio"], tab["gpl_eur_1000L"])),
    }
    n_of = int(tab["origem"].str.startswith("oficial").sum()) if "origem" in tab else 0
    print(f"[isp] escala lida de {FICHEIRO_ISP.name}: {len(tab)} períodos "
          f"({n_of} oficiais, {len(tab) - n_of} de referência)")
    return anchors


def adicionar_impostos(df: pd.DataFrame) -> pd.DataFrame:
    """Junta ISP (referência), IVA (exato) e decompõe o preço em componentes."""
    df["grupo_fiscal"] = df["tipoCombustivel"].map(GRUPO_FISCAL)
    anchors_por_grupo = _carregar_isp_anchors()

    # ISP por grupo via merge_asof (degrau: vale o último valor em vigor)
    partes = []
    for grupo, anchors in anchors_por_grupo.items():
        tab = pd.DataFrame(anchors, columns=["data", "isp_eur_1000L"])
        tab["data"] = pd.to_datetime(tab["data"])
        tab = tab.sort_values("data")
        sub = df[df["grupo_fiscal"] == grupo].sort_values("data")
        sub = pd.merge_asof(sub, tab, on="data", direction="backward")
        partes.append(sub)
    df = pd.concat(partes, ignore_index=True)

    # ISP em €/litro
    df["isp_eur_l"] = df["isp_eur_1000L"] / 1000.0

    # IVA (exato). O IVA incide sobre (base + ISP), logo o valor de IVA por litro
    # extrai-se do preço final: IVA = PVP * taxa/(1+taxa).
    df["iva_taxa"] = _iva_taxa(df["data"])
    df["valor_iva_eur_l"] = df["preco_eur_l"] * df["iva_taxa"] / (1 + df["iva_taxa"])

    # Decomposição do preço à bomba
    df["impostos_eur_l"] = df["isp_eur_l"] + df["valor_iva_eur_l"]
    df["preco_sem_impostos_eur_l"] = df["preco_eur_l"] - df["impostos_eur_l"]
    df["carga_fiscal_pct"] = df["impostos_eur_l"] / df["preco_eur_l"] * 100

    return df


# --------------------------------------------------------------------------- #
# 4. Features de calendário e de séries temporais + alvos                     #
# --------------------------------------------------------------------------- #
def adicionar_features_e_alvos(df: pd.DataFrame) -> pd.DataFrame:
    """Cria features de calendário, lags/médias móveis (por combustível) e os
    dois alvos de previsão. TUDO calculado por tipo de combustível para não
    haver 'leakage' entre séries diferentes."""

    # --- Calendário ---
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["dia"] = df["data"].dt.day
    df["trimestre"] = df["data"].dt.quarter
    df["semana_ano"] = df["data"].dt.isocalendar().week.astype(int)
    df["dia_semana"] = df["data"].dt.dayofweek          # 0 = segunda
    df["fim_de_semana"] = (df["dia_semana"] >= 5).astype(int)

    feriados = feriados_pt(range(df["ano"].min(), df["ano"].max() + 1))
    df["feriado"] = df["data"].isin(feriados).astype(int)

    # --- Features por combustível (ordenar por data dentro de cada grupo) ---
    df = df.sort_values(["tipoCombustivel", "data"]).reset_index(drop=True)
    g = df.groupby("tipoCombustivel", group_keys=False)

    # Lags e médias móveis do PRÓPRIO preço (só usam o passado -> sem leakage)
    df["preco_lag_1d"] = g["preco_eur_l"].shift(1)
    df["preco_lag_7d"] = g["preco_eur_l"].shift(7)
    df["preco_lag_30d"] = g["preco_eur_l"].shift(30)
    df["media_movel_7d"] = g["preco_eur_l"].transform(
        lambda s: s.rolling(7, min_periods=1).mean())
    df["media_movel_30d"] = g["preco_eur_l"].transform(
        lambda s: s.rolling(30, min_periods=1).mean())

    # Variação recente do próprio preço
    df["variacao_1d"] = df["preco_eur_l"] - df["preco_lag_1d"]
    df["variacao_pct_1d"] = g["preco_eur_l"].pct_change() * 100
    df["variacao_7d"] = df["preco_eur_l"] - df["preco_lag_7d"]

    # Distância do preço à sua média móvel (indicador de "esticado")
    df["desvio_media_30d"] = df["preco_eur_l"] - df["media_movel_30d"]

    # --- Features dos drivers externos (Brent/EUR-USD) ---
    # (Estas colunas são iguais para todos os combustíveis no mesmo dia, mas as
    #  variações/lags fazem sentido calcular na série diária única.)
    for col in ["brent_usd", "eur_usd", "brent_eur"]:
        df[f"{col}_lag_1d"] = g[col].shift(1)
        df[f"{col}_lag_7d"] = g[col].shift(7)
        df[f"{col}_var_pct_1d"] = g[col].pct_change() * 100
        df[f"{col}_var_pct_7d"] = g[col].pct_change(7) * 100
    df["brent_eur_media_movel_7d"] = g["brent_eur"].transform(
        lambda s: s.rolling(7, min_periods=1).mean())

    # --- ALVOS (o que queremos prever) ---
    # 1) Dia seguinte: valor, direção (sobe/desce) e VARIAÇÃO (delta)
    df["preco_amanha"] = g["preco_eur_l"].shift(-1)              # regressão do valor
    df["target_preco_amanha"] = df["preco_amanha"]
    df["target_subida"] = (df["preco_amanha"] > df["preco_eur_l"]).astype("Int64")
    df.loc[df["preco_amanha"].isna(), "target_subida"] = pd.NA
    # B2: alvo = a VARIAÇÃO de amanhã (amanhã - hoje). Prever isto e comparar com
    # "prever 0" (sem alteração) é uma avaliação justa da capacidade preditiva.
    df["target_delta_amanha"] = df["preco_amanha"] - df["preco_eur_l"]

    # 2) B1: Direção a 7 dias — o preço estará mais caro daqui a 7 dias?
    df["preco_daqui_7d"] = g["preco_eur_l"].shift(-7)
    df["target_subida_7d"] = (df["preco_daqui_7d"] > df["preco_eur_l"]).astype("Int64")
    df.loc[df["preco_daqui_7d"].isna(), "target_subida_7d"] = pd.NA

    # 3) B5: movimento em 3 classes — 0 = desce, 1 = mantém, 2 = sobe.
    # Mais fiel que o binário (os dias em que o preço fica igual têm classe própria).
    dif = (df["preco_amanha"] - df["preco_eur_l"]).round(4)
    df["target_movimento"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
    df.loc[dif < 0, "target_movimento"] = 0
    df.loc[dif == 0, "target_movimento"] = 1
    df.loc[dif > 0, "target_movimento"] = 2
    df.loc[df["preco_amanha"].isna(), "target_movimento"] = pd.NA

    return df


# --------------------------------------------------------------------------- #
# 5. Pipeline principal                                                        #
# --------------------------------------------------------------------------- #
def main() -> None:
    print("=" * 70)
    print("ENRIQUECIMENTO DO DATASET DE PREÇOS DE COMBUSTÍVEL (Portugal)")
    print("=" * 70)

    base = ler_precos_base()
    externos = preparar_series_externas(base["data"].min(), base["data"].max())

    # Juntar drivers externos a cada linha (data + combustível)
    df = base.merge(externos, on="data", how="left")

    # Impostos: ISP (referência) + IVA (exato) + decomposição do preço
    df = adicionar_impostos(df)

    df = adicionar_features_e_alvos(df)

    # Segurança: substituir eventuais infinitos (de pct_change com valores
    # em falta) por NaN, para não partir os modelos a jusante.
    df = df.replace([np.inf, -np.inf], np.nan)

    # Ordenar por data para leitura/uso cronológico
    df = df.sort_values(["data", "tipoCombustivel"]).reset_index(drop=True)

    df.to_csv(SAIDA, index=False, encoding="utf-8")
    print("-" * 70)
    print(f"[ok] Dataset enriquecido guardado em: {SAIDA}")
    print(f"     {len(df):,} linhas x {df.shape[1]} colunas")
    print(f"     Colunas: {', '.join(df.columns)}")
    # Pequeno diagnóstico do alvo de classificação
    alvo = df["target_subida"].dropna()
    print(f"     Distribuição do alvo 'subida': "
          f"{(alvo == 1).mean()*100:.1f}% sobe | {(alvo == 0).mean()*100:.1f}% desce/mantém")


if __name__ == "__main__":
    main()
