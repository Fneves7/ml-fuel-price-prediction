/agent Ridge Regression

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — regressão regularizada

## Objectivo

Construir uma solução Ridge para regressão com regularização L2, útil contra overfitting e multicolinearidade.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar target, features, valores em falta, duplicados e outliers.
- Avaliar escala das variáveis.
- Avaliar correlações e multicolinearidade.
- Identificar variáveis redundantes.
- Verificar variáveis categóricas e necessidade de encoding.
- Verificar data leakage.
- Avaliar se há sinais de overfitting em modelos lineares não regularizados.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se houver multicolinearidade, prioriza Ridge como alternativa à regressão linear simples.
- Se as features tiverem escalas diferentes, normaliza dentro do pipeline.
- Se Ridge não melhorar face à regressão linear, documenta que a regularização pode não ser necessária.
- Se alpha demasiado alto reduzir desempenho, selecciona alpha por validação cruzada.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline simples.
- Criar pipeline com pré-processamento e normalização.
- Treinar Ridge com vários valores de alpha.
- Usar validação cruzada.
- Comparar com regressão linear e Lasso se possível.
- Analisar coeficientes.
- Avaliar no teste.
- Guardar pipeline final.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- MSE
- RMSE
- R²
- Erro por alpha
- Estabilidade dos coeficientes
- Comparação com baseline

## Entregáveis obrigatórios

- eda_ridge.md
- train_ridge.py
- ridge_alpha_comparison.csv
- coefficient_report.md
- metrics_ridge.json
- modelo guardado

## Regras de qualidade

- Usar código modular e simples.
- Separar carregamento de dados, pré-processamento, treino, avaliação e relatório.
- Usar seeds quando aplicável.
- Evitar data leakage.
- Guardar artefactos em pastas claras.
- Criar ou actualizar README com instruções de execução.
- Explicar resultados em português de Portugal.
- Não apagar ficheiros sem confirmação.
- Se uma biblioteca não existir no ambiente, indicar comando de instalação e criar alternativa viável quando possível.

