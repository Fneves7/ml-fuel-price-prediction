/agent Lasso Regression

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — regressão regularizada

## Objectivo

Construir uma solução Lasso para regressão com regularização L1 e potencial selecção automática de variáveis.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar target, features, valores em falta, duplicados e outliers.
- Avaliar escala das variáveis.
- Avaliar correlações e multicolinearidade.
- Identificar features redundantes ou pouco informativas.
- Verificar variáveis categóricas e necessidade de encoding.
- Verificar data leakage.
- Analisar dimensão do dataset face ao número de features.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se houver muitas features ou multicolinearidade, usa Lasso como candidato forte.
- Se as features não estiverem na mesma escala, normaliza obrigatoriamente dentro de pipeline.
- Se Lasso eliminar features importantes segundo o domínio, documenta e compara com Ridge.
- Se alpha elevado degradar demasiado o desempenho, selecciona alpha por validação cruzada.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline simples.
- Criar pipeline com pré-processamento e normalização.
- Treinar Lasso com vários valores de alpha.
- Usar validação cruzada.
- Comparar com regressão linear e Ridge se possível.
- Analisar coeficientes iguais a zero.
- Avaliar no teste.
- Guardar pipeline final.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- MSE
- RMSE
- R²
- Número de features seleccionadas
- Erro por alpha
- Comparação com baseline

## Entregáveis obrigatórios

- eda_lasso.md
- train_lasso.py
- lasso_alpha_comparison.csv
- selected_features.md
- metrics_lasso.json
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

