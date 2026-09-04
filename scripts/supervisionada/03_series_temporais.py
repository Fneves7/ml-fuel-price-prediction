# -*- coding: utf-8 -*-
"""
03_series_temporais.py — Família SÉRIES TEMPORAIS (previsão univariada).
Algoritmos dos prompts: suavização exponencial, ARIMA, SARIMA, Prophet, LSTM.
Prevê o preço diário do Gasóleo especial nos últimos ~60 dias (horizonte de teste).
Baseline: 'último valor' (random walk). Prophet e LSTM só correm se instalados.
"""
import sys, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from comum import serie_um_combustivel, PASTA_FIG, RAIZ
from sklearn.metrics import mean_absolute_error, mean_squared_error

sns.set_theme(style="whitegrid", context="talk")
H = 60  # horizonte de teste (dias)


def metr(nome, y, p, L, previsoes):
    p = np.asarray(p, float)
    mae = mean_absolute_error(y, p); rmse = np.sqrt(mean_squared_error(y, p))
    print(f"  {nome:22s} MAE={mae:.4f} | RMSE={rmse:.4f}")
    L.append({"modelo": nome, "MAE": mae, "RMSE": rmse}); previsoes[nome] = p


def main():
    print("=" * 66); print("FAMÍLIA: SÉRIES TEMPORAIS  (preço diário do Gasóleo especial)"); print("=" * 66)
    s = serie_um_combustivel("Gasóleo especial")
    treino, teste = s.iloc[:-H], s.iloc[-H:]
    y = teste.values
    print(f"[dados] série {len(s):,} dias | treino {len(treino):,} | teste {H}")
    L, prev = [], {}

    # Baseline — último valor (random walk)
    metr("Baseline (último valor)", y, np.repeat(treino.iloc[-1], H), L, prev)

    # Suavização exponencial (Holt, tendência aditiva)
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        m = ExponentialSmoothing(treino, trend="add").fit()
        metr("Suavização exponencial", y, m.forecast(H).values, L, prev)
    except Exception as e:
        print(f"  Suavização exponencial: erro ({type(e).__name__})")

    # ARIMA
    try:
        from statsmodels.tsa.arima.model import ARIMA
        m = ARIMA(treino, order=(5, 1, 0)).fit()
        metr("ARIMA(5,1,0)", y, m.forecast(H).values, L, prev)
    except Exception as e:
        print(f"  ARIMA: erro ({type(e).__name__})")

    # SARIMA (sazonalidade semanal)
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        m = SARIMAX(treino, order=(1, 1, 1), seasonal_order=(1, 0, 1, 7),
                    enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
        metr("SARIMA sem.", y, np.asarray(m.forecast(H)), L, prev)
    except Exception as e:
        print(f"  SARIMA: erro ({type(e).__name__})")

    # Prophet
    try:
        from prophet import Prophet
        dfp = pd.DataFrame({"ds": treino.index, "y": treino.values})
        mp = Prophet(daily_seasonality=False, weekly_seasonality=True,
                     yearly_seasonality=True)
        mp.fit(dfp)
        fut = mp.make_future_dataframe(periods=H)
        metr("Prophet", y, mp.predict(fut)["yhat"].values[-H:], L, prev)
    except Exception as e:
        print(f"  Prophet: indisponível/erro ({type(e).__name__}); ignorado.")

    # LSTM (previsão recursiva a partir de janelas)
    try:
        import os; os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Input
        W = 30
        mn, mx = treino.min(), treino.max()
        tn = (treino.values - mn) / (mx - mn)
        Xs = np.array([tn[i:i+W] for i in range(len(tn)-W)])
        ys = tn[W:]
        Xs = Xs.reshape(-1, W, 1)
        net = Sequential([Input((W, 1)), LSTM(32), Dense(1)])
        net.compile(optimizer="adam", loss="mse")
        net.fit(Xs, ys, epochs=8, batch_size=64, verbose=0)
        jan = tn[-W:].tolist(); pr = []
        for _ in range(H):
            nx = float(net.predict(np.array(jan[-W:]).reshape(1, W, 1), verbose=0)[0, 0])
            pr.append(nx); jan.append(nx)
        metr("LSTM", y, np.array(pr)*(mx-mn)+mn, L, prev)
    except Exception as e:
        print(f"  LSTM: indisponível/erro ({type(e).__name__}); ignorado.")

    tab = pd.DataFrame(L).set_index("modelo")
    tab.round(4).to_csv(RAIZ / "dados" / "sup_series_temporais.csv", encoding="utf-8")

    # Figura: histórico recente + previsões no horizonte de teste
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(s.index[-200:], s.values[-200:], color="black", lw=2, label="Real")
    cores = plt.cm.tab10(np.linspace(0, 1, len(prev)))
    for (nome, p), c in zip(prev.items(), cores):
        ax.plot(teste.index, p, lw=1.6, label=nome, color=c)
    ax.axvline(teste.index[0], color="gray", ls="--", lw=1)
    ax.set_title("Séries temporais — previsão do preço (Gasóleo especial, últimos 60 dias)")
    ax.set_xlabel("Data"); ax.set_ylabel("Preço (€/L)")
    ax.legend(fontsize=9, ncol=2)
    fig.savefig(PASTA_FIG / "sup_03_series_temporais.png", dpi=120, bbox_inches="tight")
    print("[figura] sup_03_series_temporais.png")


if __name__ == "__main__":
    main()
