/agent Clustering Hierárquico

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem não supervisionada — clustering

## Objectivo

Criar agrupamentos interpretáveis com Clustering Hierárquico e dendrogramas.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar dimensão do dataset.
- Seleccionar features relevantes.
- Verificar valores em falta, duplicados e outliers.
- Analisar escala das variáveis.
- Avaliar correlações e redundância.
- Visualizar dados com PCA 2D quando útil.
- Avaliar se o dataset é pequeno/médio o suficiente para clustering hierárquico.
- Procurar sinais de grupos naturais.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se o dataset for muito grande, avisar custo computacional e propor amostragem ou outro método.
- Se as escalas forem diferentes, normalizar obrigatoriamente.
- Se outliers dominarem distâncias, tratar ou documentar impacto.
- Se diferentes linkages produzirem resultados muito diferentes, documentar instabilidade.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Normalizar dados.
- Testar linkage ward, complete, average e single quando adequado.
- Gerar dendrograma.
- Escolher número de clusters com base no dendrograma e métricas.
- Caracterizar clusters.
- Comparar com K-means se útil.
- Guardar relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Silhouette score
- Calinski-Harabasz index
- Davies-Bouldin index
- Distância de corte
- Tamanho dos clusters

## Entregáveis obrigatórios

- eda_hierarquico.md
- hierarchical_clustering.py
- dendrogram.png
- metrics_hierarchical.json
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

