# -*- coding: utf-8 -*-
"""
12_previsao_ao_vivo.py — Backlog F2 (+ C5: guardar o modelo).

Dado o ESTADO MAIS RECENTE do dataset, devolve a previsão para o dia seguinte,
por combustível: direção (sobe/desce), confiança e recomendação (atestar/esperar).
É a versão de terminal do dashboard (scripts/11).

C5: o modelo calibrado é guardado em `modelos/modelo_direcao.joblib` e reutilizado
nas execuções seguintes (treina de novo apagando o ficheiro, ou com --retreinar).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd, joblib
from lightgbm import LGBMClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
PASTA_MODELOS = RAIZ / "modelos"; PASTA_MODELOS.mkdir(exist_ok=True)
MODELO = PASTA_MODELOS / "modelo_direcao.joblib"

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
ORDEM = ["Gasolina especial 95", "Gasolina simples 95", "Gasolina 98",
         "Gasolina especial 98", "Gasóleo especial", "Gasóleo simples",
         "Biodiesel B15", "GPL Auto"]


def carregar_dataset():
    df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
    dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
    feats = FEATURES + list(dummies.columns)
    df = pd.concat([df, dummies], axis=1)
    return df, feats


def treinar_e_guardar(df, feats):
    print("[modelo] a treinar (LightGBM + calibração isotónica) e a guardar…")
    d = df.dropna(subset=feats + ["target_subida"]).copy()
    d["target_subida"] = d["target_subida"].astype(int)
    corte = d["data"].max() - pd.Timedelta(days=180)
    ajuste, calib = d[d["data"] < corte], d[d["data"] >= corte]
    base = LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
        random_state=42, n_jobs=-1, verbose=-1).fit(ajuste[feats], ajuste["target_subida"])
    cal = CalibratedClassifierCV(FrozenEstimator(base), method="isotonic").fit(
        calib[feats], calib["target_subida"])
    joblib.dump({"modelo": cal, "feats": feats}, MODELO)
    print(f"[modelo] guardado em {MODELO.relative_to(RAIZ)}")
    return cal


def main():
    retreinar = "--retreinar" in sys.argv
    df, feats = carregar_dataset()
    if MODELO.exists() and not retreinar:
        cal = joblib.load(MODELO)["modelo"]
        print(f"[modelo] carregado de {MODELO.relative_to(RAIZ)} "
              f"(use --retreinar para treinar de novo)")
    else:
        cal = treinar_e_guardar(df, feats)

    # linhas mais recentes com features completas (uma por combustível)
    valid = df.dropna(subset=feats)
    ultima = valid["data"].max()
    proximo = ultima + pd.Timedelta(days=1)
    alvo = valid[valid["data"] == ultima].copy()
    alvo["p_sobe"] = cal.predict_proba(alvo[feats])[:, 1]
    alvo["ord"] = alvo["tipoCombustivel"].map({n: i for i, n in enumerate(ORDEM)})
    alvo = alvo.sort_values("ord")

    print("\n" + "=" * 72)
    print(f"PREVISÃO PARA {proximo.date()}  (a partir dos dados de {ultima.date()})")
    print("=" * 72)
    print(f"{'Combustível':22} {'Hoje':>8}  {'Previsão':>9} {'Conf.':>6}  Recomendação")
    print("-" * 72)
    n_sobe = 0
    for _, r in alvo.iterrows():
        p = float(r["p_sobe"]); sobe = p >= 0.5; n_sobe += sobe
        conf = p if sobe else 1 - p
        direcao = "SOBE ▲" if sobe else "DESCE ▼"
        rec = "atestar hoje" if sobe else "pode esperar"
        print(f"{r['tipoCombustivel']:22} {r['preco_eur_l']:>7.3f}€  "
              f"{direcao:>9} {conf*100:>5.0f}%  {rec}")
    print("-" * 72)
    print(f"Resumo: {n_sobe} devem subir · {len(alvo)-n_sobe} devem descer/manter.")
    print("(Estimativa estatística ~79% de acerto; não é conselho financeiro.)")


if __name__ == "__main__":
    main()
