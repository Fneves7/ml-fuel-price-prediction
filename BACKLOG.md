# Backlog do projeto — Previsão de preços de combustível

Estado em **2026-09-04**. Lista priorizada do que falta / pode melhorar.
Legenda de esforço: 🟢 baixo · 🟡 médio · 🔴 alto. Valor: ⭐ (1 a 3).

---

## A. Dados / enriquecimento

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| A1 | **Completar a série semanal do ISP** (jul–set/2022, jan–fev/2023, 2024) | 🟡 | ⭐ | **Parado por opção.** Já temos 13 âncoras oficiais; as lacunas estão entre pontos próximos. Destrava-se com os URLs `files.dre.pt` exatos ou um CSV compilado → colar em `dados/isp_portarias.csv`. |
| A2 | **Preços grossistas de Roterdão** (gasolina/gasóleo *spot*) | 🔴 | ⭐⭐⭐ | O elo em falta entre o Brent e o preço à bomba (margem de refinação). Fonte paga/difícil; procurar proxy gratuito (EIA, Neste, ENSE). |
| A3 | **Taxa de carbono** (adicionamento CO₂) | 🟡 | ⭐ | Atualmente incluída na "componente comercial". Separá-la tornaria a decomposição mais exata. |
| A4 | **Stocks/inventários e margem de refinação** (crack spread) | 🔴 | ⭐⭐ | Sinais de oferta/procura; ajudam a explicar desvios do preço face ao Brent. |
| A5 | Investigar o **outlier de 2009** no Gasóleo especial (pico isolado visível nas figuras) | 🟢 | ⭐ | Provável erro de registo; limpar como fizemos aos zeros/>3 €. |
| A6 | **Comparação ibérica** — juntar preços de Espanha | 🟡 | ⭐⭐ | Contexto: PT vs ES; ver o efeito dos impostos na diferença de preço à bomba. |
| A7 | **Google Trends** ("preço combustível", "gasóleo") como proxy de procura | 🟡 | ⭐ | Sinal de procura/atenção do público; testar se antecipa movimentos. |
| A8 | **Eventos/choques** como flags (guerra, decisões OPEP, feriados-ponte, época de férias) | 🟡 | ⭐⭐ | Explica desvios do preço face ao Brent; melhora a interpretabilidade. |

## B. Modelação

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| ~~B1~~ | ~~**Prever a direção a 7 dias**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `scripts/05`. RF **68,9 %** (vs 53 % acaso). Figura `14_confusao_7dias`. |
| ~~B2~~ | ~~**Regressão do *delta***~~ ✅ FEITO | 🟢 | ⭐⭐⭐ | `scripts/05`. RF bate o baseline "prever 0" em **+22 %** MAE; R²=0,38; 76 % direção. Figura `13_regressao_delta`. |
| ~~B3~~ | ~~**Gradient boosting** (XGBoost / LightGBM)~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/06`. Sem vencedor universal: XGB/LGBM ganham a 1 dia (**0,82** vs 0,79); RF ganha no delta e a 7 dias. Figura `15`. |
| ~~B4~~ | ~~**Validação cruzada temporal** + *tuning*~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/07`. Robusto: ~0,78–0,79 ± 0,04 em 5 janelas. Tuning do LightGBM não melhorou o holdout (0,821→0,813). Figura `16`. |
| ~~B5~~ | ~~**Classe "mantém"** (3 classes)~~ ✅ FEITO | 🟢 | ⭐⭐ | `scripts/08`. XGBoost 3 classes: **0,797** acc, F1-macro 0,795 (baseline 0,472). "Mantém" bem prevista (F1 0,79). Figura `17_confusao_3classes`. |
| B6 | Modelos **por combustível** vs modelo único (*pooled*) | 🟡 | ⭐ | Ver se separar melhora face ao one-hot atual. |
| B7 | **Importância por permutação** em vez de impureza | 🟢 | ⭐ | Mais fiável para interpretar variáveis. |
| ~~B8~~ | ~~**Previsão com probabilidade**~~ ✅ FEITO | 🟢 | ⭐⭐⭐ | `scripts/09`. LightGBM calibrado (isotónico). Com confiança ≥90% acerta **96%** (cobre 38% dos dias). Figura `18_probabilidade`. |
| ~~B9~~ | ~~**Decisão "atesto hoje ou espero?"**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `scripts/10`. Poupa **0,07 €/depósito** (76% do oráculo); nos dias em que esperou o preço desceu 67% das vezes. Figura `19_decisao`. |
| B10 | **Análise de erros** — quando é que o modelo falha? | 🟢 | ⭐⭐ | Ver se os erros se concentram em dias de grande variação ou mudanças de ISP. |
| B11 | **Explicabilidade com SHAP** | 🟡 | ⭐⭐ | Explicar previsões individuais, para além da importância global. |
| B12 | **Curva de skill por horizonte** (1, 3, 7, 14 dias) | 🟡 | ⭐⭐ | Mostrar como a previsibilidade cai com o horizonte. |

## C. Robustez / qualidade

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| C1 | **Atualizar dados externos** (Brent/EUR-USD do FRED) antes de entregar | 🟢 | ⭐⭐ | 2 comandos `curl` (ver `FONTES.md`). |
| C2 | Adicionar **testes/asserções** simples (sem leakage, sem NaN nos alvos) | 🟡 | ⭐ | Garante que o pipeline não regride. |
| C3 | Fixar **versões** exatas em `requirements.txt` | 🟢 | ⭐ | Reprodutibilidade. |
| C4 | Script **"correr tudo"** (`run_all`) | 🟢 | ⭐ | Um comando que executa o pipeline 01→08 por ordem. |
| C5 | **Guardar os modelos treinados** (`joblib`) | 🟢 | ⭐ | Reutilizar sem treinar de novo; base para a previsão "ao vivo" (F2). |

## E. Outras famílias de ML — usar as pastas de prompts
> Estende para lá da `01_supervisionada`, cobrindo `02_nao_supervisionada` e `03_reforco`.

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| E1 | **Clustering** (k-means / hierárquico / GMM) | 🟡 | ⭐⭐ | Agrupar dias/regimes de mercado (crise, estável); prompts `02_nao_supervisionada/01_clustering`. |
| E2 | **Redução de dimensionalidade** (PCA / LDA) | 🟢 | ⭐ | Visualizar a estrutura das features; prompts `02_nao_supervisionada/02_reducao_dimensionalidade`. |
| E3 | **Aprendizagem por reforço** — agente "atestar/esperar" | 🔴 | ⭐⭐ | Bandit/Q-learning para a decisão do B9; prompts `03_reforco`. |

## F. Produto / aplicação (em HTML)
| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| ~~F1~~ | ~~**Dashboard HTML da previsão do dia**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `scripts/11_dashboard.py` → `dashboard.html` (Artifact). "Vou atestar hoje?": previsão + confiança + recomendação por combustível. |
| F2 | **Previsão "ao vivo"** | 🟡 | ⭐⭐ | Script que, dado o estado de hoje, devolve a previsão para amanhã (usa C5). |

## D. Apresentação / entrega

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| ~~D1~~ | ~~**Slides / relatório final**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `apresentacao.html` — deck HTML navegável (12 slides), publicado como Artifact. Só HTML (o utilizador não quer PowerPoint). |
| ~~D2~~ | ~~**README** de arranque rápido~~ ✅ FEITO | 🟢 | ⭐⭐ | `README.md` na raiz (descrição + como correr + estrutura). |
| ~~D3~~ | ~~Narrativa "IA generativa em cada fase"~~ ✅ FEITO | 🟢 | ⭐ | `IA_GENERATIVA.md` (mapeia as 6 fases). |

---

## Próximo passo recomendado
Concluídos: ~~B1–B5~~ (modelação) · ~~D1, D2, D3~~ (entrega). O núcleo está **completo**.

Os que dariam mais "salto" a seguir (valor/esforço):
- **B8 — previsão com probabilidade** (🟢 ⭐⭐⭐): "sobe com 72 % de confiança" é muito
  mais útil e é barato (`predict_proba`).
- **F1 — dashboard HTML da previsão do dia** (🟡 ⭐⭐⭐): produto visual em HTML.
- **B9 — decisão "atesto ou espero?"** (🟡 ⭐⭐⭐): traduz a previsão em poupança €.
- **E1 — clustering** (🟡 ⭐⭐): usa a pasta `02_nao_supervisionada`.

Tudo o resto (A*, B6/B7/B10-12, C*, E2/E3, F2) é opcional/incremental.

> Nada aqui é bloqueante: o projeto já está **completo e funcional** (dados → análise →
> 2 modelos → avaliação → conclusão). Este backlog é só para o levar mais longe.
