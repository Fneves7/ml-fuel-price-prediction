# Projeto — Previsão de alteração de preços de combustíveis

## 1. Escolha do tema
**"Previsão de alteração de preços de combustíveis"**
Pergunta de investigação:
> *"Conseguimos prever o aumento/descida do preço de um tipo de combustível num determinado dia?"*

Uso de IA generativa nas fases do projeto: formular perguntas de investigação,
estruturar o problema, explorar ideias de enriquecimento do dataset, interpretar
resultados e melhorar a apresentação.

---

## 2. Seleção e enriquecimento do dataset

**Fonte base:** DGEG — Preço médio diário
<https://precoscombustiveis.dgeg.gov.pt/estatistica/preco-medio-diario/>
Ficheiro `Postos.csv`: preço médio diário de **8 combustíveis** em Portugal,
de **2008-11-18 a 2026-09-01** (45 188 registos).

### Porque é que enriquecemos o dataset?
O dataset original só diz **o que** aconteceu ao preço, não **porquê**. Para o
modelo perceber as causas, juntámos as variáveis que economicamente determinam o
preço do combustível em Portugal:

| Variável adicionada | Fonte | Porque importa |
|---|---|---|
| **Petróleo Brent (USD/barril)** | FRED `DCOILBRENTEU` | principal matéria-prima; principal driver internacional |
| **Câmbio EUR/USD** | FRED `DEXUSEU` | o petróleo é cotado em dólares, mas pagamos em euros |
| **Brent em EUR (derivado)** | cálculo | o custo real da matéria-prima para o consumidor português |
| **Produto refinado spot** (gasolina/gasóleo) | FRED (US Gulf Coast) | o elo entre o crude e a bomba; correlaciona **0,91** com o preço (> Brent) |
| **Crack spread + WTI** | derivado / FRED | margem de refinação (produto − crude) e 2.º crude de referência |
| **Eventos/choques** (COVID, guerra, crise ISP, férias) | flags | explicam desvios face ao Brent; ajudam a direção a 7 dias |
| **ISP** (imposto sobre produtos petrolíferos) | Portarias / DR / OA | é uma das maiores fatias do preço; a sua descida em 2022 baixou o preço |
| **IVA** (taxa normal) | legislação | incide sobre base + ISP; ~½ do preço da gasolina são impostos |
| **Calendário + feriados nacionais** | cálculo | os preços atualizam em dias fixos e congelam ao fim de semana |

> **Nota sobre o ISP:** o **IVA é exato** (20 % até jun/2010 → 21 % → 23 % desde
> jan/2011). O **ISP** é uma escala em degraus cujas âncoras principais foram
> **extraídas dos PDFs oficiais do Diário da República** (Portarias 301-A/2018,
> 65-B/2023, 150-B/2023, 355-B/2024, …) — ver `dados/isp_portarias.csv` e `FONTES.md`.
> Entre Portarias o valor mantém-se constante (como na lei); o mecanismo semanal fino
> de 2022–23 está simplificado aos passos capturados. A partir do preço final
> decompõe-se ainda `valor_iva_eur_l`, `impostos_eur_l`, `preco_sem_impostos_eur_l`
> e `carga_fiscal_pct`.

Além destas, foram criadas **features de séries temporais** (por combustível, para
não haver *data leakage*): *lags* (1, 7, 30 dias), médias móveis (7 e 30 dias),
variações diárias e semanais, e as variações dos drivers externos.

### Limpeza de dados efetuada
- **133 preços a 0,00 €** (ex.: 04–22/09/2015) tratados como dados em falta.
- **5 preços absurdos > 3 €/L** (erros de registo de 2009 na Gasolina especial 98)
  tratados como dados em falta.
- Correção de codificação (UTF-8) e conversão de `"1,3800 €"` → `1.38`.

Resultado: `dados/dataset_enriquecido.csv` — 45 188 linhas × 39 colunas, pronto para ML.

---

## 3. Análise dos dados

Principais conclusões da análise exploratória (ver pasta `figuras/`):

- **O preço segue o petróleo Brent em euros.** A correlação preço↔Brent(€) por
  combustível varia entre **0,72 e 0,91** (ex.: Gasolina simples 95 = 0,91;
  Gasóleo especial = 0,82). Nas figuras vê-se o crash de 2020 (COVID) e o pico de
  2022 (guerra na Ucrânia) refletidos no preço à bomba.
- **Distribuição do movimento diário:** ~37 % dos dias o preço sobe, ~45 % desce e
  ~18 % mantém-se igual (fins de semana/feriados).
- **Sazonalidade semanal forte:** a maior parte das variações concentra-se em dias
  úteis; ao fim de semana o preço quase não muda.
- **Os impostos pesam muito:** em média **~50 % do preço da gasolina** e **~42 % do
  gasóleo** são impostos (ISP + IVA); no GPL Auto apenas ~20 %. A decomposição
  mostra bem a **descida do ISP em 2022** que aliviou o preço à bomba.

Figuras geradas: `01_evolucao_precos`, `02_preco_vs_brent`, `03_correlacoes`,
`04_distribuicao_alvo`, `05_scatter_brent_vs_preco`, `06_sazonalidade`,
`11_decomposicao_impostos`, `12_carga_fiscal`.

---

## 4. Criação do modelo

Duas abordagens de **aprendizagem supervisionada**, ambas com **divisão cronológica**
(treino < 2024-01-01; teste ≥ 2024-01-01) para não "espreitar o futuro":

**A) Classificação — "o preço sobe amanhã?"** (alvo binário)
- Baseline (classe maioritária), Regressão Logística, Random Forest.

**B) Regressão — "qual o valor do preço amanhã?"** (alvo contínuo €/L)
- Baseline persistência (amanhã = hoje), Regressão Linear, Random Forest.

---

## 5. Avaliação dos resultados

### A) Classificação (conjunto de teste 2024–2026)
| Modelo | Accuracy | Precisão | Recall | F1 |
|---|---|---|---|---|
| Baseline (classe maioritária) | 0,613 | — | — | — |
| Regressão Logística | 0,714 | 0,637 | 0,607 | 0,622 |
| **Random Forest** | **0,794** | **0,721** | **0,761** | **0,741** |

✅ A Random Forest **bate claramente o baseline** (79,4 % vs 61,3 %). As variáveis
mais importantes são o **dia da semana** (quando os preços atualizam), a **variação
recente do preço** e as **variações do Brent/câmbio** — coerente com a realidade.

### B) Regressão (conjunto de teste 2024–2026)
| Modelo | MAE (€/L) | RMSE (€/L) | R² |
|---|---|---|---|
| **Baseline (amanhã = hoje)** | **0,0042** | 0,0114 | 0,9990 |
| Regressão Linear | 0,0058 | 0,0117 | 0,9989 |
| Random Forest | 0,0055 | 0,0115 | 0,9989 |

⚠️ **Lição importante:** o R² ≈ 0,999 parece excelente, mas é **enganador** — o preço
de amanhã é quase igual ao de hoje. O simples baseline "amanhã = hoje" **é o melhor**;
os modelos de ML ficam 31–38 % piores no MAE. Prever o *valor exato* não traz valor.

### C) Extensões — prever a VARIAÇÃO e a direção a 7 dias
Para avaliar de forma **justa** a capacidade preditiva, mudámos a pergunta:

**C1) Regressão da variação** (delta = amanhã − hoje). Baseline = "prever 0 (sem alteração)".
| Modelo | MAE (€/L) | R² | Acerto na direção |
|---|---|---|---|
| Baseline (prever 0) | 0,00424 | ~0 | — |
| Regressão Linear | 0,00618 | <0 | 60 % |
| **Random Forest** | **0,00331** | **0,38** | **76 %** |

✅ Agora o Random Forest **bate o baseline em 22 %** (MAE) e explica **38 %** da variância
da variação — este é o valor *honesto* da capacidade preditiva (o R²=0,999 anterior era
trivial). A Regressão Linear é pior que o baseline: é preciso um modelo **não-linear**.

**C2) Direção a 7 dias** ("estará mais caro daqui a 7 dias?"). Alvo mais equilibrado (53 % sobe).
| Modelo | Accuracy | F1 |
|---|---|---|
| Baseline (classe maioritária) | 0,531 | 0,694 |
| Regressão Logística | 0,640 | 0,578 |
| **Random Forest** | **0,689** | **0,690** |

✅ A 7 dias o modelo acerta **69 %** (vs 53 % do acaso), com precisão/recall equilibrados.

**C3) 3 classes — desce / mantém / sobe** (`scripts/08`). Em vez de esconder os dias
"iguais" dentro de "desce", damos-lhes classe própria (~17 %).
| Modelo | Accuracy | F1-macro |
|---|---|---|
| Baseline (maioritária) | 0,472 | 0,214 |
| **XGBoost** | **0,797** | **0,795** |

✅ O modelo distingue bem os três movimentos — a classe "mantém" tem F1 = 0,79 (não é
ignorada). Ver `figuras/17_confusao_3classes.png`.

**C4) Da previsão à decisão — probabilidade e poupança**
- **Probabilidade calibrada** (`scripts/09`): em vez de só "sobe/desce", o modelo dá a
  confiança. As probabilidades são **fiáveis** (curva de calibração cola-se à ideal) e
  quando a confiança é **≥ 90 %** o modelo acerta **96 %** (cobrindo 38 % dos dias).
- **Decisão "atesto hoje ou espero?"** (`scripts/10`): seguir o modelo poupa
  **0,07 €/depósito de 50 L** (76 % da poupança máxima teórica); nos dias em que
  esperou, o preço desceu mesmo em 67 % das vezes. A poupança por depósito é pequena
  (o preço muda pouco ao dia), mas o modelo capta a maior parte do ganho possível.
- **Dashboard** (`scripts/11` → `dashboard.html`): "Vou atestar hoje?" — previsão,
  confiança e recomendação por combustível, publicado como página HTML.

### D) Comparação de algoritmos — Gradient Boosting vs Random Forest
Comparámos **XGBoost** e **LightGBM** com a Random Forest nas três tarefas. Conclusão
importante: **não há um vencedor universal** — depende da tarefa.

| Tarefa (métrica principal) | Random Forest | XGBoost | LightGBM |
|---|---|---|---|
| Classificação 1 dia (accuracy) | 0,793 | **0,820** | **0,821** |
| Regressão delta (acerto direção) | **0,756** | 0,695 | 0,681 |
| Direção a 7 dias (accuracy) | **0,689** | 0,674 | 0,673 |

✅ O **gradient boosting melhora a classificação a 1 dia** (79 % → **82 %**), mas a
**Random Forest é melhor** na regressão da variação e na direção a 7 dias. Bom exemplo
de que a escolha do algoritmo deve ser guiada pela tarefa e pela avaliação, não por moda.

### E) Robustez e afinação — validação temporal (B4)
Um único corte (2024) pode ser sorte. Repetimos a avaliação em **5 janelas temporais**
(`TimeSeriesSplit`) e afinámos o LightGBM com `RandomizedSearchCV` (também temporal).

| Modelo | Accuracy média (5 janelas) |
|---|---|
| Random Forest | 0,782 ± 0,036 |
| XGBoost | 0,790 ± 0,039 |
| LightGBM | 0,788 ± 0,039 |

✅ **Resultados robustos:** ~0,78–0,79 em todas as janelas, sempre bem acima do baseline
(0,613). As diferenças entre os 3 algoritmos ficam **dentro da margem de erro**.
⚠️ **A afinação não melhorou:** o LightGBM afinado (0,813) ficou ligeiramente abaixo do
de defeito (0,821) no teste 2024+ — o ótimo em validação cruzada nem sempre é o melhor
no *holdout*, e os parâmetros de defeito já estavam bem escolhidos. (Honestidade > moda.)

---

## 6. Conclusão

- **Resposta à pergunta:** Sim, conseguimos prever a **direção** (sobe/desce) do preço
  com utilidade real — a 1 dia acerta **≈ 79 %** (Random Forest) ou **82 %** (XGBoost/
  LightGBM), e **69 %** a 7 dias, bem acima do acaso. Já prever o **valor exato** não compensa (o preço é tão
  estável que "amanhã = hoje" é difícil de bater); mas prever a **variação** já compensa
  — o modelo bate em **22 %** o baseline "sem alteração" e acerta **76 %** do sentido.
- **Impostos:** com o ISP e o IVA passámos a poder decompor o preço e mostrar que
  metade do que pagamos são impostos — e que o corte do ISP em 2022 foi visível no
  preço à bomba. As âncoras do ISP foram confirmadas nos PDFs oficiais do Diário da
  República. Como as taxas mudam raramente, ajudam mais a *explicar o nível* do que a
  prever o movimento diário (melhoria marginal no modelo: 78,5 % → 79,4 %).
- **O enriquecimento valeu a pena:** as variáveis de Brent e câmbio, mais as features
  de séries temporais, foram determinantes para o desempenho e para *explicar* as
  subidas/descidas.
- **Conceitos aplicados:** Inteligência Artificial · Machine Learning ·
  Aprendizagem supervisionada (classificação + regressão) · Avaliação de modelos
  (baselines, métricas, matriz de confusão, divisão cronológica).
- **Limitações / trabalho futuro:** incluir impostos (ISP/IVA) e preços grossistas de
  Roterdão; testar horizontes a 7 dias; experimentar modelos de gradient boosting.

---

## Como reproduzir
```bash
pip install -r requirements.txt
python scripts/01_enriquecer_dataset.py     # cria dados/dataset_enriquecido.csv
python scripts/02_analise_dados.py          # gera as figuras em figuras/
python scripts/03_modelo_classificacao.py   # modelo sobe/desce (1 dia)
python scripts/04_modelo_regressao.py       # modelo do valor do preço
python scripts/05_modelo_delta_e_7dias.py   # variação (delta) + direção a 7 dias
python scripts/06_gradient_boosting.py      # XGBoost/LightGBM vs Random Forest
python scripts/07_tuning_validacao.py       # validação temporal + afinação (B4)
python scripts/08_multiclasse.py            # 3 classes: desce/mantém/sobe
python scripts/09_probabilidade.py          # previsão com probabilidade calibrada
python scripts/10_decisao.py                # "atesto hoje ou espero?" (poupança €)
python scripts/11_dashboard.py              # gera dashboard.html (previsão do dia)
python scripts/12_previsao_ao_vivo.py       # previsão do dia no terminal (guarda o modelo)
python scripts/13_por_combustivel.py        # B6: pooled vs por combustível
python scripts/14_permutacao.py             # B7: importância por permutação
python scripts/15_analise_erros.py          # B10: onde falha o modelo
python scripts/16_shap.py                   # B11: explicabilidade (SHAP)
python scripts/17_skill_horizonte.py        # B12: skill por horizonte (1/3/7/14d)
```
Ver `LOG.md` para o registo detalhado de todo o trabalho realizado e
`FONTES.md` para todas as fontes de dados (DGEG, FRED, ISP/IVA).
