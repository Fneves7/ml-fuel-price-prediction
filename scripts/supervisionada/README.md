# Aprendizagem supervisionada — todos os algoritmos

Implementação de **todos os 19 algoritmos** dos meta-prompts em
`prompts_opencode_ml/01_supervisionada/`, organizados pelas mesmas 4 famílias.
Cada script segue a metodologia dos prompts: divisão cronológica (treino < 2024,
teste ≥ 2024), comparação com **baseline**, tratamento de classes desequilibradas,
sem *data leakage*, e **sem inventar resultados** (o que não corre no ambiente fica
documentado).

Correr: `python scripts/supervisionada/<ficheiro>.py`

---

## 01 — Regressão · `01_regressao.py`
Alvo: **preço (€/L) do dia seguinte**. Baseline: "amanhã = hoje" (MAE 0,0042).

| Algoritmo | Prompt | MAE (€/L) | R² |
|---|---|---|---|
| Regressão linear simples | `regressao_linear_simples.md` | 0,0043 | 0,999 |
| Regressão linear múltipla | `regressao_linear_multipla.md` | 0,0062 | 0,999 |
| Regressão polinomial (grau 2) | `regressao_polinomial.md` | 0,0050 | 0,999 |
| Ridge | `ridge.md` | 0,0061 | 0,999 |
| Lasso | `lasso.md` | 0,0052 | 0,999 |

**Observação:** nenhum bate a persistência — prever o *valor* é dominado pela
auto-correlação (ver a análise do *delta* no `scripts/05`). Figura: `figuras/sup_01_regressao.png`.

## 02 — Classificação · `02_classificacao.py`
Alvo: **o preço sobe amanhã?** Baseline (classe maioritária): 0,613.

| Algoritmo | Prompt | Accuracy | F1 |
|---|---|---|---|
| Regressão logística | `regressao_logistica.md` | 0,715 | 0,623 |
| SVM linear | `svm_linear.md` | 0,708 | 0,612 |
| SVM kernel (RBF)¹ | `kernel_svm.md` | 0,721 | 0,646 |
| KNN (k=25) | `knn.md` | **0,733** | 0,613 |
| Naïve Bayes | `naive_bayes.md` | 0,565 | 0,579 |

¹ O SVM kernel escala mal (~O(n²)); treinado numa amostra de 8 000 linhas (documentado).
**Observação:** todos exceto o Naïve Bayes batem o baseline; o KNN lidera a família.
Figura: `figuras/sup_02_classificacao.png`.

## 03 — Séries temporais · `03_series_temporais.py`
Previsão univariada do preço diário do **Gasóleo especial** (horizonte 60 dias).
Baseline: "último valor" (MAE 0,1993).

| Algoritmo | Prompt | MAE (€/L) | RMSE |
|---|---|---|---|
| Suavização exponencial | `suavizacao_exponencial.md` | **0,1967** | 0,2190 |
| ARIMA(5,1,0) | `arima.md` | 0,1993 | 0,2220 |
| SARIMA (sazonal 7) | `sarima.md` | 0,2073 | 0,2306 |
| Prophet | `prophet.md` | 0,2928 | 0,3082 |
| LSTM | `lstm_series_temporais.md` | 0,2297 | 0,2515 |

**Observação:** a 60 dias, nenhum modelo bate significativamente o "último valor" — o
preço diário é quase um *random walk*. As previsões achatam enquanto o preço real
sobe. Coerente com a conclusão do projeto. Figura: `figuras/sup_03_series_temporais.png`.

## 04 — Métodos de conjunto · `04_metodos_conjunto.py`
Alvo: **o preço sobe amanhã?** Baseline: 0,613.

| Algoritmo | Prompt | Accuracy | F1 |
|---|---|---|---|
| Árvore de decisão (simples) | `arvore_decisao.md` | 0,803 | 0,766 |
| Random Forest | `random_forest.md` | 0,793 | 0,739 |
| XGBoost | `xgboost.md` | **0,820** | 0,774 |
| CatBoost | `catboost.md` | 0,819 | 0,778 |

**Observação:** o gradient boosting (XGBoost/CatBoost) lidera; esta é a **melhor
família** para prever a direção. Figura: `figuras/sup_04_metodos_conjunto.png`.

---

## Conclusão transversal
O **melhor resultado global** para a pergunta do projeto (prever a direção sobe/desce)
é o **gradient boosting a ~0,82**. As famílias mais fracas (regressão do valor,
séries temporais univariadas) confirmam a mesma lição honesta: prever o *nível* do
preço não compensa; prever a *direção/variação* sim.

Bibliotecas usadas: scikit-learn, xgboost, catboost, statsmodels, prophet, tensorflow.
