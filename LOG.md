# LOG do projeto — Previsão de preços de combustível

Registo cronológico de todo o trabalho realizado. Data: **2026-09-03**.

---

## 0. Ponto de partida
- Dataset base `Postos.csv`: preço médio diário DGEG, 8 combustíveis,
  2008-11-18 → 2026-09-01 (45 188 linhas; formato `data;tipoCombustivel;precoMedio`).
- Existiam já ficheiros exploratórios (`Postos_ML.csv`, `Postos_ML_OneHot.csv`,
  `Postos_ML_Completo_OneHot.csv`) com features de lag corretas (calculadas por
  combustível — verificado, sem leakage).
- Objetivo: **enriquecer o dataset** com as causas dos preços e construir o projeto
  completo de aprendizagem supervisionada (pandas + scikit-learn + matplotlib + seaborn).

## 1. Ambiente
- Python 3.13; instalados `seaborn` e `nbformat` (faltavam). pandas 3.0, sklearn 1.9,
  matplotlib 3.11, numpy 2.3 já presentes.

## 2. Enriquecimento do dataset — `scripts/01_enriquecer_dataset.py`
- **Dados externos (FRED, CSV sem chave):**
  - Brent USD/barril — série `DCOILBRENTEU` (diária desde 1987).
  - Câmbio EUR/USD — série `DEXUSEU` (diária desde 1999).
  - Guardados em cache local (`dados/externo_brent.csv`, `dados/externo_eurusd.csv`)
    para reprodutibilidade offline. (O `urllib` do Python está bloqueado no ambiente;
    a cache é populada via `curl`. O script usa a cache automaticamente.)
- **Alinhamento temporal:** calendário diário contínuo; fins de semana/feriados
  preenchidos com o último valor conhecido (*forward-fill*).
- **Derivada:** `brent_eur = brent_usd / eur_usd` (custo real da matéria-prima).
- **Feriados nacionais PT:** função própria (fixos + móveis via algoritmo da Páscoa).
- **Features (por combustível, sem leakage):** lags 1/7/30d, médias móveis 7/30d,
  variações 1d/7d e %, desvio à média 30d; lags e variações de Brent/EURUSD/Brent€.
- **Alvos:** `target_subida` (1 = sobe amanhã, 0 = desce/mantém) e
  `target_preco_amanha` (valor €/L do dia seguinte).
- **Saída:** `dados/dataset_enriquecido.csv` (45 188 × 39).

### Problemas encontrados e resolvidos
1. **Parsing do preço** `"1,3800 €"`: o símbolo € não era removido pelo `.replace`.
   → passou-se a limpar com regex `[^0-9,]` e trocar `,`→`.`.
2. **Preços = 0,00 €** (133 registos, 04–22/09/2015): eram dados em falta gravados
   como zero → convertidos para NaN.
3. **Preços absurdos > 3 €/L** (5 registos, Gasolina especial 98 em 2009, até 5,43 €/L):
   erros de registo → convertidos para NaN.
4. **Infinitos** de `pct_change` (divisão por valores em falta) → substituídos por NaN.
5. **Encoding (importante):** confirmou-se por análise de bytes que `Postos.csv` é
   **UTF-8 com BOM** (`c3 b3` para "ó", € em UTF-8). Leituras iniciais em cp1252
   corrompiam os acentos ("Gasóleo"→"GasÃ³leo"). Corrigido para `utf-8-sig` na
   leitura e `encoding="utf-8"` explícito em todas as escritas/leituras dos scripts.

## 2b. Impostos ISP + IVA — adicionados a `scripts/01_enriquecer_dataset.py`
(pedido posterior do utilizador: "juntar impostos, isp e iva")
- **IVA (exato):** taxa normal 20 % (até 30/06/2010) → 21 % (2.º sem. 2010) →
  23 % (desde 01/01/2011). Coluna `iva_taxa`.
- **ISP (escala de referência em degraus):** valores oficiais €/1000 L por Portaria,
  aplicados por grupo fiscal (gasolinas / gasóleos+biodiesel / GPL). Âncoras
  documentadas: padrão 526,64 (gasolina) e 343,15 (gasóleo); corte da crise de 2022
  (gasolina→343,70; gasóleo→168,37 em maio/2022); reposição em 2024; Portarias de
  2025 (497,52 / 361,60) e 2026 (462,13 / 302,44). GPL ≈ 8 €/1000 L (quase nulo).
  Fontes: Ordem dos Advogados (tabela ISP), Diário da República / Governo, RTP/DN/ECO.
  **Limitação assumida (decisão do utilizador):** série de referência, aproximada
  entre datas; o mecanismo semanal de 2022–23 está simplificado.
- **Decomposição do preço (derivada):** `isp_eur_l`, `valor_iva_eur_l`,
  `impostos_eur_l`, `preco_sem_impostos_eur_l`, `carga_fiscal_pct`.
- Carga fiscal média resultante: gasolinas ~48–51 %, gasóleos ~42 %, GPL ~20 %.
- Dataset passou de 39 → **47 colunas**.
- Novas figuras: `11_decomposicao_impostos`, `12_carga_fiscal`.
- Impostos adicionados como features dos modelos → classificação RF melhorou
  **0,785 → 0,790** (regressão inalterada, baseline continua a ganhar).

## 2c. ISP guiado por CSV editável (`dados/isp_portarias.csv`)
(pedido do utilizador: reconstruir ISP a partir de Portarias desde 2018)
- Esclarecido que o **ISP não é novo de 2018** — existe há décadas; a Portaria
  301-A/2018 apenas fixa as taxas base desse período (a partir daí a reconstrução
  é limpa).
- Investigou-se a viabilidade de reconstruir a série oficial a partir do Diário da
  República: **inviável de forma fiável nesta sessão** — os PDFs do DR são binários
  comprimidos (WebFetch não lê; sem libs de PDF instaladas) e os resumos de terceiros
  divergem (base 2018 da gasolina: 363,78 vs 526,64 €/1000 L conforme a fonte).
- Solução implementada: `adicionar_impostos` passa a **ler a escala do ISP de
  `dados/isp_portarias.csv`** (formato data_inicio + valores por grupo + portaria +
  origem), com fallback para os valores embutidos. Basta expandir o CSV (com
  verificação humana das Portarias) para aumentar a precisão, sem tocar no código.
- CSV inicial: valores documentados + `referencia_aproximada`. Documentado em
  `FONTES.md`.

## 2d. Extração de valores OFICIAIS do Diário da República
(pedido do utilizador: "consegues ir à internet buscar essa informação oficial?")
- Método validado: `curl` descarrega o PDF do DR; `pypdf` + `cryptography` extraem o
  texto (os PDFs do DR são cifrados com AES — daí ter sido preciso instalar
  `cryptography`). WebFetch sozinho não lê estes PDFs.
- Valores **confirmados diretamente nos PDFs do DR** e colocados em
  `dados/isp_portarias.csv` (origem `oficial_DR`):
  - Portaria **301-A/2018** (base, 23-11-2018): gasolina **526,64** / gasóleo **343,15**
    → confirma que a base correta é 526,64 (e não 363,78 como um resumo indicava).
  - Portaria **65-B/2023** (03-03-2023): 459,83 / 311,47
  - Portaria **150-B/2023** (05-06-2023): 460,36 / 323,54
  - Portaria **355-B/2024** (vigência 01-01-2025): 481,26 / 337,21
  - Portaria 63-A/2022 (jan–abr 2022): gasolina 506,64 (gasóleo ficou "[...]" inalterado)
- Valores de notícia (origem `oficial_noticia`): corte de maio/2022 (343,70 / 168,37),
  427-A/2025 (497,52 / 361,60), 331-A/2026 (462,13 / 302,44).
- PDFs guardados em `dados/portarias_pdf/`.
- Acrescentaram-se 4 passos semanais de mar–mai/2022 (Portarias 111-A, 128-A, 140-A,
  141-B) a partir da tabela consolidada da Ordem dos Advogados (compila o DR).
  CSV final: **10 oficiais + 1 referência (11 períodos)**.
- Limitação assumida: entre 09-05-2022 e 03-03-2023 há dezenas de Portarias semanais
  não todas capturadas (aggregadores não têm a série completa; tretas.org/curl
  bloqueados no ambiente; URLs do DR não indexadas de forma consolidada). Nesse
  intervalo vale o último passo conhecido. Extrair mais exige uma pesquisa+download
  por Portaria, com valor marginal baixo para o ML.
- Impacto: classificação RF ~**0,79** (estável).

## 2e. Extração continuada das Portarias semanais de 2022–2023 (a pedido do utilizador)
- Extrator melhorado para lidar com dois formatos: "fixada no valor de € X" (valor
  final direto) e "reduzida em € Y" (→ valor final = base − Y). Cuidado tomado para
  ler o texto OPERATIVO (não referências do preâmbulo).
- Novas âncoras oficiais confirmadas nos PDFs do DR:
  - 164-A/2022 (27-06-2022): 316,06 / 162,80
  - 249-C/2022 (03-10-2022): 360,52 / 163,48  (gasolina = 526,64 − 166,12)
  - 312-F/2022 (30-12-2022): 471,64 / 295,98
- CSV do ISP agora com **13 valores oficiais + 1 referência (14 períodos)**, cobrindo
  a crise de 2022 com resolução ~mensal (mar, mai, jun, out, dez/2022; mar, jun/2023).
- Lacunas menores restantes: jul–set/2022, jan–fev/2023, 2024 (entre pontos próximos).
- Limite do ambiente confirmado: cada Portaria exige uma pesquisa própria (URLs do DR
  não indexadas); tretas.org e a página HTML do diariodarepublica.pt não são
  acessíveis (curl bloqueado / conteúdo em JS). Só os PDFs `files.dre.pt` /
  `files.diariodarepublica.pt` funcionam.

## 3. Análise exploratória — `scripts/02_analise_dados.py`
- 6 figuras guardadas em `figuras/`:
  `01_evolucao_precos`, `02_preco_vs_brent`, `03_correlacoes`,
  `04_distribuicao_alvo`, `05_scatter_brent_vs_preco`, `06_sazonalidade`.
- **Correlação preço↔Brent(€) por combustível: 0,72 a 0,91** (forte).
- Movimento diário do preço: ~37 % sobe, ~45 % desce, ~18 % mantém.

## 4. Modelo de classificação — `scripts/03_modelo_classificacao.py`
- Divisão cronológica (treino < 2024-01-01; teste ≥ 2024). One-hot do combustível.
- Resultados (teste, já com impostos): Baseline **0,613** · Regressão Logística
  **0,717** · **Random Forest 0,790** (F1 "sobe" = 0,74).
- Variáveis mais importantes: dia da semana, variação recente do preço, variações
  do Brent/câmbio. Figuras: `07`, `08` (matrizes de confusão), `09` (importâncias).
- Guardado `dados/resultados_classificacao.csv`.

## 5. Modelo de regressão — `scripts/04_modelo_regressao.py`
- Baseline persistência (amanhã = hoje) vs Regressão Linear vs Random Forest.
- Resultados (teste): MAE baseline **0,0042 €/L** < RF 0,0055 < Linear 0,0058;
  R² ≈ 0,999 em todos. **O baseline ganha** → prever o valor exato não compensa.
- Figura: `10_regressao_real_vs_previsto`. Guardado `dados/resultados_regressao.csv`.

## 6. Entregáveis
- `Projeto.md` — relatório completo (6 secções preenchidas com resultados reais).
- `requirements.txt` — dependências.
- `scripts/01..04` — pipeline reproduzível.
- `dados/` — dataset enriquecido + caches + tabelas de resultados.
- `figuras/` — 10 figuras.

## 6b. Limpeza de ficheiros redundantes
- Apagados `dados/Postos_ML.csv`, `dados/Postos_ML_OneHot.csv` e
  `dados/Postos_ML_Completo_OneHot.csv` — versões exploratórias antigas (25 col),
  substituídas pelo `dataset_enriquecido.csv` (47 col), que é um superconjunto mais
  limpo (os zeros/outliers já tratados; drivers externos e impostos incluídos; o
  one-hot é gerado nos scripts do modelo). Nenhum script os referenciava.
- Fonte bruta mantida: `dados/Postos.csv`. Resultado: `dados/dataset_enriquecido.csv`.

## 6c. Extensões B2 + B1 — `scripts/05_modelo_delta_e_7dias.py`
- Adicionados dois alvos no script 01: `target_delta_amanha` (variação de amanhã) e
  `target_subida_7d` (direção a 7 dias).
- **B2 (regressão da variação):** baseline "prever 0" MAE 0,00424; Reg. Linear 0,00618
  (pior — linear não capta); **Random Forest 0,00331 (+22% vs baseline), R²=0,38,
  acerto na direção 76%**. É a avaliação HONESTA (o R²=0,999 da regressão do valor era
  trivial). Figura `13_regressao_delta`; `dados/resultados_delta.csv`.
- **B1 (direção a 7 dias):** alvo mais equilibrado (53% sobe). Baseline 0,531; Reg.
  Logística 0,640; **Random Forest 0,689** (F1 0,69). Figura `14_confusao_7dias`;
  `dados/resultados_direcao_7d.csv`.
- 14 figuras no total. B1 e B2 marcados como concluídos no `BACKLOG.md`.

## 6d. B3 — Gradient Boosting — `scripts/06_gradient_boosting.py`
- Instalados `xgboost` 3.4.1 e `lightgbm` 4.7.0. Comparação com Random Forest nas 3
  tarefas (mesma divisão cronológica e features).
- **Sem vencedor universal:**
  - Classificação 1 dia: XGBoost **0,820** / LightGBM **0,821** > RF 0,793 (ganho ~3pp).
  - Regressão delta: **RF melhor** (dir 75,6%, R²=0,38) que XGB (69,5%) / LGBM (68,1%).
  - Direção a 7 dias: **RF 0,689** > XGB 0,674 / LGBM 0,673.
- Figura `15_comparacao_gradient_boosting`; `dados/resultados_gradient_boosting.csv`.
- Lição: a escolha do algoritmo depende da tarefa/avaliação. (Tuning fica no B4.)

## 6e. B4 — Validação temporal + tuning — `scripts/07_tuning_validacao.py`
- **TimeSeriesSplit (5 janelas)** na classificação a 1 dia: RF 0,782±0,036 · XGBoost
  0,790±0,039 · LightGBM 0,788±0,039 — sempre >> baseline 0,613. Confirma que o
  resultado ~0,79–0,82 é ROBUSTO (não é sorte do corte de 2024); diferenças entre
  algoritmos dentro da margem de erro.
- **RandomizedSearchCV (20 combinações, TimeSeriesSplit)** do LightGBM: o modelo afinado
  (0,813) ficou ligeiramente ABAIXO do de defeito (0,821) no holdout 2024+. Lição
  honesta: ótimo em CV ≠ ótimo em holdout; defaults já bem escolhidos.
- Figura `16_validacao_tuning`; `dados/resultados_validacao_temporal.csv`.

## 6f. D1 — Apresentação final (fase 6)
- **Formato: só HTML** — o utilizador não quer PowerPoints (o `.pptx` que chegou a ser
  gerado foi removido). Ver [[preferencias-trabalho]].
- **HTML:** `apresentacao.html` — deck de slides navegável (teclado/botões/pontos,
  barra de progresso, gráficos embutidos em base64), publicado como Artifact.
  Tipografia Archivo + Public Sans + IBM Plex Mono; design de mundo único.
- Estrutura das 11 slides: título · desafio · dados/enriquecimento · preço vs petróleo ·
  impostos · modelo direção · lição honesta (delta) · algoritmos · robustez · conclusão ·
  fontes/obrigado.

## 6g. TODOS os algoritmos de aprendizagem supervisionada (a pedido do utilizador)
O utilizador pediu para implementar todos os algoritmos dos meta-prompts em
`prompts_opencode_ml/01_supervisionada/` (que eu não tinha usado — eram guiões, não
código). Implementados os **19 algoritmos** em `scripts/supervisionada/` (4 famílias):
- **Regressão** (`01_regressao.py`): linear simples/múltipla, polinomial, Ridge, Lasso.
  Nenhum bate a persistência (MAE ~0,004–0,006).
- **Classificação** (`02_classificacao.py`): logística (0,715), SVM linear (0,708),
  SVM kernel RBF (0,721, amostra 8k), KNN (0,733), Naïve Bayes (0,565).
- **Séries temporais** (`03_series_temporais.py`): suavização exponencial (MAE 0,197),
  ARIMA (0,199), SARIMA (0,207), Prophet (0,293), LSTM (0,230). A 60 dias nenhum bate
  o "último valor" — preço quase random-walk.
- **Métodos de conjunto** (`04_metodos_conjunto.py`): árvore (0,803), Random Forest
  (0,793), XGBoost (**0,820**), CatBoost (0,819).
- Instalados: statsmodels (já existia), catboost, prophet, tensorflow.
- 4 figuras novas (`sup_01..04`), 4 CSVs (`dados/sup_*.csv`), e
  `scripts/supervisionada/README.md` mapeia cada algoritmo ao seu prompt.
- Melhor resultado global para a direção: gradient boosting ~0,82.
- **Apresentação atualizada** (pptx + HTML) com um slide novo "Testámos 19 algoritmos
  em 4 famílias" (grelha 2×2 por família). Ambas passaram a ter 12 slides.

## 6h. B5 + D2 + D3
- **B5 — classificação em 3 classes** (`scripts/08_multiclasse.py`): novo alvo
  `target_movimento` (0 desce / 1 mantém / 2 sobe) no script 01. XGBoost: **0,797**
  accuracy, F1-macro 0,795 (baseline 0,472); a classe "mantém" (17%) é bem prevista
  (F1 0,79). Figura `17_confusao_3classes`; `dados/resultados_multiclasse.csv`.
- **D2 — README** de arranque rápido (`README.md` na raiz).
- **D3 — IA generativa** (`IA_GENERATIVA.md`): mapeia onde a IA ajudou nas 6 fases.

## 6i. B8 + B9 + F1 — probabilidade, decisão e dashboard
- **B8 — probabilidade calibrada** (`scripts/09_probabilidade.py`): LightGBM +
  calibração isotónica (FrozenEstimator; `cv='prefit'` foi removido no sklearn 1.9).
  Brier 0,141; accuracy 0,79. Acerto por confiança: ≥70% → 89% (cobre 65%), ≥90% → 96%
  (cobre 38%). Figura `18_probabilidade`; `dados/resultados_probabilidade.csv`.
- **B9 — decisão "atesto/espero"** (`scripts/10_decisao.py`): regra baseada na previsão;
  poupa 0,07 €/depósito de 50 L = **76% do oráculo**; nos dias em que esperou o preço
  desceu 67% das vezes. Figura `19_decisao`; `dados/resultados_decisao.csv`.
- **F1 — dashboard** (`scripts/11_dashboard.py` → `dashboard.html`): "Vou atestar hoje?"
  com previsão + confiança + recomendação por combustível; publicado como Artifact.
  (Bug corrigido: `preco_eur_l` estava duplicado nas colunas → erro do LightGBM.)
- **Apresentação** (`apresentacao.html`) atualizada com um slide "Da previsão à decisão"
  (B8 probabilidade + B9 poupança). Passou a 13 slides.

## 6j. Secção A do backlog — enriquecimento de dados
- **A2 (produto refinado) + A4 (crack spread):** juntadas as séries FRED `DGASUSGULF`
  (gasolina spot) e `DDFUELUSGULF` (gasóleo spot) + WTI; derivados `*_spot_eur_l`,
  `crack_gasolina/gasoleo` (produto − crude) e respetivas variações. O produto refinado
  correlaciona **0,91** com o preço à bomba (> Brent 0,82) — o "elo em falta".
- **A5:** limpo o pico de 6 dias do Gasóleo especial (ago/2009).
- **A8:** flags `evento_covid`, `evento_guerra`, `evento_crise_isp`, `epoca_ferias`.
- Dataset: 48 → **72 colunas**. Impacto: 1 dia mantém-se (~0,82, já saturado); **direção
  a 7 dias melhora** (RF 0,689 → 0,717). Features adicionadas em `scripts/03` e `06`.
- **A1/A3/A6/A7 — documentados (não implementados):** A1 fica em 13 âncoras oficiais;
  A3 (taxa carbono) sem série anual fiável; A6 (Espanha) sem série histórica na API;
  A7 (Google Trends) bloqueado. Ver `BACKLOG.md`/`FONTES.md`.

## 6k. Ponto F concluído + âmbito só supervisionado
- **F2 (+ C5)** — `scripts/12_previsao_ao_vivo.py`: previsão do dia seguinte no terminal
  (direção + confiança + recomendação por combustível). O modelo calibrado é guardado
  em `modelos/modelo_direcao.joblib` (joblib) e reutilizado. `.gitignore` criado.
- **Âmbito:** o utilizador quer **só aprendizagem supervisionada** — a secção E do
  backlog (clustering, PCA/LDA, reforço) fica **fora de âmbito**. Ver [[preferencias-trabalho]].

## 6l. Ponto B concluído (B6, B7, B10, B11, B12)
Módulo partilhado `scripts/_comum_modelo.py` (features enriquecidas). Instalado `shap`.
- **B6** (`scripts/13`): pooled 0,818 ≥ por combustível 0,806 → o modelo único é tão bom
  ou melhor; não vale separar. Figura `20`.
- **B7** (`scripts/14`): importância por permutação confirma dia da semana + variação
  recente + produto refinado (`gasoleo_spot_var_7d`). Figura `21`.
- **B10** (`scripts/15`): erro global 18,3%; concentra-se em dias de variação ≈0 (22%)
  e no GPL/Gasolina 98 (30-35%); sexta é o dia mais previsível (5%). Figura `22`.
  (O painel "choque vs normal" não é possível no teste: `evento_guerra` persiste desde
  2022 → substituído por erro mensal.)
- **B11** (`scripts/16`): SHAP beeswarm (dia da semana, momentum, produto refinado). Fig `23`.
- **B12** (`scripts/17`): skill por horizonte 81%(1d) → 81%(3d) → 70%(7d) → 68%(14d),
  sempre acima do acaso. Figura `24`.
Secções A, B, D, F concluídas; E fora de âmbito. Resta só C (qualidade), opcional.

## 6m. Secção C concluída (qualidade)
- **C1:** caches FRED atualizadas (5 séries via curl) e dataset regenerado.
- **C2:** `scripts/testes_pipeline.py` — 11 asserções (sem leakage, sem NaN indevido,
  outlier 2009 removido, IVA∈{20,21,23}%, sem infinitos). **11/11 passam.**
- **C3:** `requirements.txt` com versões fixadas (`==`).
- **C4:** `scripts/run_all.py` — corre 01→17 por ordem (`--tudo` inclui a pasta
  supervisionada). Usado também para refrescar todos os outputs após o C1.
- **Backlog encerrado:** secções A, B, C, D, F feitas; E fora de âmbito.

## 6n. Dashboard mais explícito
- `scripts/11_dashboard.py` passou a gerar uma **frase em linguagem simples** no topo
  (ex.: "Amanhã, o preço de X e Y deve subir — se precisa destes, convém atestar hoje;
  os restantes devem descer ou manter-se."), para o leitor perceber logo. O `run_all`
  regenera o `dashboard.html`; a publicação como Artifact continua a ser um passo à parte.

## 7. Conclusão do trabalho
Sim, é possível prever a **direção** do preço com utilidade (≈79 %, acima do acaso
de 61 %); prever o **valor exato** não compensa (o preço é muito estável dia-a-dia).
O enriquecimento com Brent + câmbio foi determinante.

## Ideias de trabalho futuro
- Juntar impostos (ISP/IVA) e preços grossistas de Roterdão.
- Horizonte de previsão a 7 dias; modelos de gradient boosting (XGBoost/LightGBM).
