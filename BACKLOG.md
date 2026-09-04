# Backlog do projeto — Previsão de preços de combustível

Estado em **2026-09-04**. Lista priorizada do que falta / pode melhorar.
Legenda de esforço: 🟢 baixo · 🟡 médio · 🔴 alto. Valor: ⭐ (1 a 3).

---

## A. Dados / enriquecimento

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| A1 | **Completar a série semanal do ISP** | 🟡 | ⭐ | **Encerrado ao nível de referência:** 13 âncoras oficiais (crise 2022 coberta ~mensal). Série semanal 100% exige URLs `files.dre.pt` por Portaria (grind). CSV editável em `dados/isp_portarias.csv`. |
| ~~A2~~ | ~~**Preços grossistas** (produto refinado)~~ ✅ FEITO | 🔴 | ⭐⭐⭐ | FRED `DGASUSGULF`/`DDFUELUSGULF` (US Gulf Coast, proxy Roterdão) + WTI. `gasoleo_spot_eur_l` correlaciona **0,91** com o preço (> Brent 0,82). |
| A3 | **Taxa de carbono** (adicionamento CO₂) | 🟡 | ⭐ | **Documentado (não implementado):** só há valor de 2026 (~0,16–0,17 €/L); congelada em 2022–23 e interage com o ISP. Sem série anual fiável → evita-se inventar. |
| ~~A4~~ | ~~**Margem de refinação** (crack spread)~~ ✅ FEITO | 🔴 | ⭐⭐ | `crack_gasolina`/`crack_gasoleo` = produto − crude. *(Stocks/inventários da EIA não acessíveis via FRED neste ambiente — documentado.)* |
| ~~A5~~ | ~~Investigar o **outlier de 2009**~~ ✅ FEITO | 🟢 | ⭐ | Pico de 6 dias no Gasóleo especial (ago/2009, ~1,57 vs ~1,12 €/L) → tratado como NaN. |
| A6 | **Comparação ibérica** (Espanha) | 🟡 | ⭐⭐ | **Documentado (não viável aqui):** a API espanhola dá só preços atuais, não série histórica diária. Precisa de um dataset histórico compilado. |
| A7 | **Google Trends** (proxy de procura) | 🟡 | ⭐ | **Documentado (bloqueado):** o endpoint devolve 400; o Google Trends bloqueia acesso automático de datacenter. Precisa de export manual CSV. |
| ~~A8~~ | ~~**Eventos/choques** como flags~~ ✅ FEITO | 🟡 | ⭐⭐ | `evento_covid`, `evento_guerra`, `evento_crise_isp`, `epoca_ferias`. Melhoram a direção a 7 dias (RF 0,689 → 0,717). |

## B. Modelação

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| ~~B1~~ | ~~**Prever a direção a 7 dias**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `scripts/05`. RF **68,9 %** (vs 53 % acaso). Figura `14_confusao_7dias`. |
| ~~B2~~ | ~~**Regressão do *delta***~~ ✅ FEITO | 🟢 | ⭐⭐⭐ | `scripts/05`. RF bate o baseline "prever 0" em **+22 %** MAE; R²=0,38; 76 % direção. Figura `13_regressao_delta`. |
| ~~B3~~ | ~~**Gradient boosting** (XGBoost / LightGBM)~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/06`. Sem vencedor universal: XGB/LGBM ganham a 1 dia (**0,82** vs 0,79); RF ganha no delta e a 7 dias. Figura `15`. |
| ~~B4~~ | ~~**Validação cruzada temporal** + *tuning*~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/07`. Robusto: ~0,78–0,79 ± 0,04 em 5 janelas. Tuning do LightGBM não melhorou o holdout (0,821→0,813). Figura `16`. |
| ~~B5~~ | ~~**Classe "mantém"** (3 classes)~~ ✅ FEITO | 🟢 | ⭐⭐ | `scripts/08`. XGBoost 3 classes: **0,797** acc, F1-macro 0,795 (baseline 0,472). "Mantém" bem prevista (F1 0,79). Figura `17_confusao_3classes`. |
| ~~B6~~ | ~~Modelos **por combustível** vs *pooled*~~ ✅ FEITO | 🟡 | ⭐ | `scripts/13`. Pooled 0,818 ≥ individual 0,806 → o modelo único (one-hot) é tão bom ou melhor. Figura `20`. |
| ~~B7~~ | ~~**Importância por permutação**~~ ✅ FEITO | 🟢 | ⭐ | `scripts/14`. Confirma: dia da semana domina, depois variação recente e produto refinado. Figura `21`. |
| ~~B8~~ | ~~**Previsão com probabilidade**~~ ✅ FEITO | 🟢 | ⭐⭐⭐ | `scripts/09`. LightGBM calibrado (isotónico). Com confiança ≥90% acerta **96%** (cobre 38% dos dias). Figura `18_probabilidade`. |
| ~~B9~~ | ~~**Decisão "atesto hoje ou espero?"**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `scripts/10`. Poupa **0,07 €/depósito** (76% do oráculo); nos dias em que esperou o preço desceu 67% das vezes. Figura `19_decisao`. |
| ~~B10~~ | ~~**Análise de erros**~~ ✅ FEITO | 🟢 | ⭐⭐ | `scripts/15`. Erra mais em dias de variação ≈0 e no GPL/Gasolina 98; sexta é o dia mais previsível. Figura `22`. |
| ~~B11~~ | ~~**Explicabilidade com SHAP**~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/16`. Beeswarm (`shap`): dia da semana + momentum + produto refinado. Figura `23`. |
| ~~B12~~ | ~~**Curva de skill por horizonte**~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/17`. 81 % (1d) → 70 % (7d) → 68 % (14d), sempre acima do acaso. Figura `24`. |

## C. Robustez / qualidade

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| C1 | **Atualizar dados externos** (Brent/EUR-USD do FRED) antes de entregar | 🟢 | ⭐⭐ | 2 comandos `curl` (ver `FONTES.md`). |
| C2 | Adicionar **testes/asserções** simples (sem leakage, sem NaN nos alvos) | 🟡 | ⭐ | Garante que o pipeline não regride. |
| C3 | Fixar **versões** exatas em `requirements.txt` | 🟢 | ⭐ | Reprodutibilidade. |
| C4 | Script **"correr tudo"** (`run_all`) | 🟢 | ⭐ | Um comando que executa o pipeline 01→08 por ordem. |
| ~~C5~~ | ~~**Guardar os modelos treinados** (`joblib`)~~ ✅ FEITO | 🟢 | ⭐ | Feito com o F2: `modelos/modelo_direcao.joblib`, reutilizado nas execuções seguintes. |

## E. Outras famílias de ML — ~~FORA DE ÂMBITO~~
> ❌ Descartado por decisão do utilizador: **só aprendizagem supervisionada**
> (sem não-supervisionada nem reforço). ~~E1 clustering · E2 PCA/LDA · E3 reforço.~~

## F. Produto / aplicação (em HTML)
| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| ~~F1~~ | ~~**Dashboard HTML da previsão do dia**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `scripts/11_dashboard.py` → `dashboard.html` (Artifact). "Vou atestar hoje?": previsão + confiança + recomendação por combustível. |
| ~~F2~~ | ~~**Previsão "ao vivo"**~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/12_previsao_ao_vivo.py`: tabela no terminal com previsão + confiança + recomendação por combustível para o dia seguinte. |

## D. Apresentação / entrega

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| ~~D1~~ | ~~**Slides / relatório final**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `apresentacao.html` — deck HTML navegável (12 slides), publicado como Artifact. Só HTML (o utilizador não quer PowerPoint). |
| ~~D2~~ | ~~**README** de arranque rápido~~ ✅ FEITO | 🟢 | ⭐⭐ | `README.md` na raiz (descrição + como correr + estrutura). |
| ~~D3~~ | ~~Narrativa "IA generativa em cada fase"~~ ✅ FEITO | 🟢 | ⭐ | `IA_GENERATIVA.md` (mapeia as 6 fases). |

---

## Próximo passo recomendado
**Secções A, B, D, F — todas concluídas.** E descartada (fora de âmbito). O projeto
está completo, validado, explicado e documentado.

Só resta a secção **C (qualidade)**, toda opcional:
- **C4** — script "correr tudo" (🟢) · **C1** — atualizar Brent/EUR-USD antes de entregar
  (🟢) · **C2** — testes/asserções (🟡) · **C3** — fixar versões (🟢). *(C5 ✅)*

> Nada aqui é bloqueante: o projeto já está **completo e funcional** (dados → análise →
> 2 modelos → avaliação → conclusão). Este backlog é só para o levar mais longe.
