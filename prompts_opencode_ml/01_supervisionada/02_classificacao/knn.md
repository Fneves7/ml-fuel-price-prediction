/agent KNN

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — classificação

## Objectivo

Construir um classificador K-Nearest Neighbors com selecção adequada de k e distância.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar distribuição das classes.
- Verificar valores em falta, duplicados e outliers.
- Avaliar escala das features.
- Identificar features irrelevantes ou ruidosas.
- Analisar separabilidade visual com PCA se útil.
- Avaliar dimensionalidade e tamanho do dataset.
- Verificar data leakage.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se as variáveis tiverem escalas diferentes, normaliza obrigatoriamente.
- Se houver muitos outliers, avalia impacto porque KNN é sensível a distâncias.
- Se a dimensionalidade for muito alta, considera selecção/redução de features.
- Se o dataset for muito grande, documenta custo de inferência e pondera outro modelo.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline com classe maioritária.
- Separar treino/teste com stratify.
- Criar pipeline com normalização.
- Testar vários valores de k.
- Testar métricas de distância quando fizer sentido.
- Usar validação cruzada.
- Escolher melhor k.
- Avaliar no teste e guardar pipeline.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC se aplicável
- Matriz de confusão
- Desempenho por k
- Tempo de inferência

## Entregáveis obrigatórios

- eda_knn.md
- train_knn.py
- knn_k_comparison.csv
- knn_k_plot.png
- metrics_knn.json
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

