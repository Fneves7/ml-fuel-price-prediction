/agent K-means

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem não supervisionada — clustering

## Objectivo

Agrupar dados sem labels em clusters interpretáveis com K-means.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar dimensão do dataset e tipos de dados.
- Seleccionar features numéricas relevantes.
- Verificar valores em falta, duplicados e outliers.
- Analisar escala das variáveis.
- Avaliar correlações e redundância.
- Visualizar dados com PCA 2D quando útil.
- Identificar variáveis que possam dominar distâncias.
- Verificar se os clusters esperados podem ser aproximadamente esféricos.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se as variáveis tiverem escalas diferentes, normalizar obrigatoriamente.
- Se existirem outliers fortes, testar impacto ou tratamento.
- Se a EDA indicar clusters não esféricos, documentar limitação e sugerir GMM ou clustering hierárquico.
- Se muitas features forem irrelevantes, fazer selecção/redução de dimensionalidade antes do K-means.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Normalizar dados.
- Testar vários valores de k.
- Aplicar elbow method.
- Calcular silhouette score e outras métricas.
- Treinar K-means final.
- Caracterizar cada cluster.
- Visualizar clusters.
- Guardar modelo e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Inertia
- Silhouette score
- Calinski-Harabasz index
- Davies-Bouldin index
- Tamanho de cada cluster

## Entregáveis obrigatórios

- eda_kmeans.md
- train_kmeans.py
- elbow_plot.png
- cluster_visualization.png
- metrics_kmeans.json
- cluster_profile.md

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

