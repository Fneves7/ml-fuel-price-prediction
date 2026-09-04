/agent Árvore de Decisão

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — ensemble/árvores

## Objectivo

Construir uma Árvore de Decisão para classificação ou regressão com foco em interpretabilidade.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar se o problema é regressão ou classificação.
- Analisar target e distribuição de classes se aplicável.
- Verificar valores em falta, duplicados e outliers.
- Identificar variáveis categóricas e numéricas.
- Estudar relações entre features e target.
- Verificar data leakage.
- Avaliar se a árvore pode gerar regras interpretáveis úteis.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se houver classes desequilibradas, usar métricas robustas e ponderação se aplicável.
- Se a árvore crescer demasiado, controlar max_depth/min_samples_leaf.
- Se houver muitos outliers, notar que árvores tendem a ser mais robustas mas ainda devem ser analisadas.
- Se o desempenho for instável, comparar com Random Forest.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline adequada ao tipo de problema.
- Preparar dados.
- Treinar árvore inicial.
- Ajustar profundidade e parâmetros de regularização.
- Usar validação cruzada.
- Avaliar no teste.
- Exportar visualização ou regras.
- Guardar modelo.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Classificação: accuracy, precision, recall, F1, ROC-AUC, matriz de confusão
- Regressão: MAE, RMSE, R²
- Profundidade
- Número de folhas
- Diferença treino vs teste

## Entregáveis obrigatórios

- eda_arvore_decisao.md
- train_decision_tree.py
- tree_visualization.png
- feature_importance.csv
- metrics_decision_tree.json
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

