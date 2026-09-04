# Previsão de preços de combustíveis 🇵🇹⛽

Projeto de **aprendizagem supervisionada** (Fundamentos de IA): prever se o preço de um
combustível **sobe ou desce** em Portugal, a partir do preço médio diário da DGEG
(2008–2026, 8 combustíveis) enriquecido com o petróleo Brent, o câmbio EUR/USD e os
impostos (ISP + IVA).

**Resultado principal:** a direção sobe/desce prevê-se com utilidade — **~79 %** a 1 dia
(Random Forest) e **~82 %** com gradient boosting (XGBoost/LightGBM), contra 61 % do
acaso. Prever o *valor exato* não compensa; prever a *variação* sim (+22 % vs baseline).

## Como correr

```bash
pip install -r requirements.txt

# 1) enriquecer o dataset (cria dados/dataset_enriquecido.csv)
python scripts/01_enriquecer_dataset.py
# 2) análise exploratória (gera figuras em figuras/)
python scripts/02_analise_dados.py
# 3) modelos principais
python scripts/03_modelo_classificacao.py    # sobe/desce a 1 dia
python scripts/04_modelo_regressao.py        # valor do preço
python scripts/05_modelo_delta_e_7dias.py    # variação (delta) + direção a 7 dias
python scripts/06_gradient_boosting.py       # XGBoost/LightGBM vs Random Forest
python scripts/07_tuning_validacao.py        # validação temporal + afinação
python scripts/08_multiclasse.py             # 3 classes: desce/mantém/sobe

# todos os 19 algoritmos supervisionados (4 famílias)
python scripts/supervisionada/01_regressao.py
python scripts/supervisionada/02_classificacao.py
python scripts/supervisionada/03_series_temporais.py
python scripts/supervisionada/04_metodos_conjunto.py
```

> Os dados externos (Brent, EUR/USD) estão em cache local; para atualizar, ver `FONTES.md`.

## Estrutura

| Pasta / ficheiro | Conteúdo |
|---|---|
| `dados/Postos.csv` | dataset base bruto (DGEG) |
| `dados/dataset_enriquecido.csv` | dataset final (47 colunas) — **resultado do script 01** |
| `dados/isp_portarias.csv` | escala do ISP (editável) |
| `scripts/01–08` | pipeline: enriquecer → análise → modelos → avaliação |
| `scripts/supervisionada/` | os 19 algoritmos das 4 famílias + `README.md` |
| `figuras/` | todos os gráficos (.png) |
| `apresentacao.html` | apresentação (deck HTML navegável) |

## Documentação
- **`Projeto.md`** — relatório completo (6 fases + resultados).
- **`FONTES.md`** — todas as fontes de dados (DGEG, FRED, Portarias do ISP).
- **`IA_GENERATIVA.md`** — onde a IA generativa ajudou em cada fase.
- **`LOG.md`** — registo cronológico de todo o trabalho.
- **`BACKLOG.md`** — melhorias futuras.

## Ferramentas
pandas · scikit-learn · matplotlib · seaborn · xgboost · lightgbm · statsmodels ·
catboost · prophet · tensorflow
