# Uso de IA generativa no projeto

O enunciado pede que se use IA generativa (meta-prompting) em várias fases. Este
documento regista **onde e como** a IA ajudou, honestamente — incluindo o que foi
decisão humana e o que a IA propôs.

> Os guiões de referência estão em `meta_prompts_ml/` e `prompts_opencode_ml/`
> (meta-prompts por família e por algoritmo). Ver também `LOG.md` para o registo
> cronológico detalhado.

**Ferramentas de IA generativa usadas:**
- **Fase 1 (escolha do tema):** GPT 5.6
- **Fases 2 a 6 (dataset, análise, modelo, avaliação, apresentação):** Claude Opus 4.8

---

## 1. Escolha do tema — _GPT 5.6_
- **IA:** ajudou a afinar a pergunta de investigação para algo previsível e avaliável
  ("o preço sobe/desce amanhã?") e a delimitar o âmbito (classificação + regressão).
- **Humano:** escolha do tema (combustíveis) e do dataset base (DGEG).

## 2. Seleção e enriquecimento do dataset — _Claude Opus 4.8_
- **IA:** propôs os **drivers que explicam o preço** (Brent, câmbio EUR/USD, Brent em
  euros, impostos ISP/IVA, calendário/feriados) e as features de séries temporais
  (lags, médias móveis, variações) — sempre **por combustível** para evitar *data leakage*.
- **IA:** identificou e corrigiu problemas de qualidade de dados (encoding UTF-8, 133
  preços a 0 €, 5 outliers > 3 €/L) e localizou fontes gratuitas (FRED) e oficiais
  (Portarias do ISP no Diário da República, extraídas dos PDFs).
- **Humano:** decisões sobre âmbito do ISP (escala de referência vs oficial) e validação.

## 3. Análise dos dados — _Claude Opus 4.8_
- **IA:** gerou a análise exploratória (correlações, sazonalidade, decomposição fiscal)
  e os gráficos (matplotlib/seaborn), e **interpretou** os resultados (o preço segue o
  Brent; ~50% do preço são impostos; o corte do ISP de 2022).

## 4. Criação do modelo — _Claude Opus 4.8_
- **IA:** implementou os modelos de aprendizagem supervisionada seguindo a metodologia
  dos meta-prompts (baseline → treino → afinação → validação cruzada → importância de
  variáveis), incluindo **todos os 19 algoritmos** das 4 famílias da `01_supervisionada`.
- **IA:** propôs reformular a regressão para prever a **variação** (não o valor), o que
  tornou a avaliação justa.

## 5. Avaliação dos resultados — _Claude Opus 4.8_
- **IA:** comparou modelos com baselines, produziu matrizes de confusão e métricas, fez
  **validação temporal** (TimeSeriesSplit) e *tuning*, e **interpretou honestamente** —
  ex.: o R²=0,999 da regressão do valor é enganador; o tuning não melhorou o holdout.

## 6. Conclusão e apresentação — _Claude Opus 4.8_
- **IA:** estruturou a conclusão, redigiu o relatório (`Projeto.md`) e construiu a
  **apresentação em HTML** (`apresentacao.html`) com os resultados.

---

## Nota de método
Em todas as fases seguiu-se um princípio dos meta-prompts: **não inventar resultados**.
Sempre que algo não pôde ser executado no ambiente (ex.: `urllib` bloqueado, LibreOffice
indisponível, série semanal completa do ISP), ficou **explícito** no relatório e no `LOG.md`.
