# Backlog do projeto — Previsão de preços de combustível

Estado em **2026-09-03**. Lista priorizada do que falta / pode melhorar.
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

## B. Modelação

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| ~~B1~~ | ~~**Prever a direção a 7 dias**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | `scripts/05`. RF **68,9 %** (vs 53 % acaso). Figura `14_confusao_7dias`. |
| ~~B2~~ | ~~**Regressão do *delta***~~ ✅ FEITO | 🟢 | ⭐⭐⭐ | `scripts/05`. RF bate o baseline "prever 0" em **+22 %** MAE; R²=0,38; 76 % direção. Figura `13_regressao_delta`. |
| ~~B3~~ | ~~**Gradient boosting** (XGBoost / LightGBM)~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/06`. Sem vencedor universal: XGB/LGBM ganham a 1 dia (**0,82** vs 0,79); RF ganha no delta e a 7 dias. Figura `15`. |
| ~~B4~~ | ~~**Validação cruzada temporal** + *tuning*~~ ✅ FEITO | 🟡 | ⭐⭐ | `scripts/07`. Robusto: ~0,78–0,79 ± 0,04 em 5 janelas. Tuning do LightGBM não melhorou o holdout (0,821→0,813). Figura `16`. |
| B5 | **Classe "mantém"** (3 classes) ou remover dias iguais | 🟢 | ⭐⭐ | Hoje "mantém" está agregado a "desce"; 18% dos dias. Multiclasse seria mais fiel. |
| B6 | Modelos **por combustível** vs modelo único (*pooled*) | 🟡 | ⭐ | Ver se separar melhora face ao one-hot atual. |
| B7 | **Importância por permutação** em vez de impureza | 🟢 | ⭐ | Mais fiável para interpretar variáveis. |

## C. Robustez / qualidade

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| C1 | **Atualizar dados externos** (Brent/EUR-USD do FRED) antes de entregar | 🟢 | ⭐⭐ | 2 comandos `curl` (ver `FONTES.md`). |
| C2 | Adicionar **testes/asserções** simples (sem leakage, sem NaN nos alvos) | 🟡 | ⭐ | Garante que o pipeline não regride. |
| C3 | Fixar **versões** exatas em `requirements.txt` | 🟢 | ⭐ | Reprodutibilidade. |

## D. Apresentação / entrega

| # | Tarefa | Esforço | Valor | Notas |
|---|---|---|---|---|
| ~~D1~~ | ~~**Slides / relatório final**~~ ✅ FEITO | 🟡 | ⭐⭐⭐ | 11 slides. `Apresentacao_Combustiveis.pptx` (PowerPoint, validado) + `apresentacao.html` (deck HTML navegável, publicado como Artifact). |
| D2 | **README** de arranque rápido (1 parágrafo + como correr) | 🟢 | ⭐⭐ | Complementa o `Projeto.md`. |
| D3 | Rever a narrativa "IA generativa em cada fase" (exigido pelo enunciado) | 🟢 | ⭐ | Documentar onde a IA ajudou. |

---

## Próximo passo recomendado
~~B1, B2, B3, B4~~ ✅ **concluídos** (`scripts/05–07`; secções 5-C a 5-E do `Projeto.md`).
A modelação está madura e validada. Próximo natural: **D1** (slides/relatório final)
para fechar a fase de apresentação. Modelação extra opcional: B5 (classe "mantém"),
B6 (modelos por combustível), B7 (importância por permutação).

> Nada aqui é bloqueante: o projeto já está **completo e funcional** (dados → análise →
> 2 modelos → avaliação → conclusão). Este backlog é só para o levar mais longe.
