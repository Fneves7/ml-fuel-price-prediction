/agent Gaussian Mixture Models

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem não supervisionada — clustering probabilístico

## Objectivo

Criar agrupamento probabilístico com Gaussian Mixture Models.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar dimensão do dataset e tipos de dados.
- Seleccionar features numéricas relevantes.
- Verificar valores em falta, duplicados e outliers.
- Analisar escala das variáveis.
- Avaliar distribuições das features.
- Procurar grupos sobrepostos.
- Visualizar dados com PCA 2D quando útil.
- Avaliar se a hipótese de componentes gaussianas é plausível.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se as escalas forem diferentes, normalizar obrigatoriamente.
- Se a EDA indicar grupos sobrepostos, priorizar GMM face a K-means.
- Se houver outliers fortes, avaliar impacto nas gaussianas.
- Se AIC/BIC discordarem, documentar trade-off e avaliar interpretabilidade.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Normalizar dados.
- Testar vários números de componentes.
- Comparar AIC e BIC.
- Treinar GMM final.
- Calcular probabilidades de pertença.
- Identificar pontos ambíguos.
- Visualizar clusters.
- Guardar modelo e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- AIC
- BIC
- Silhouette score
- Probabilidade média de pertença
- Percentagem de pontos ambíguos
- Tamanho dos clusters

## Entregáveis obrigatórios

- eda_gmm.md
- train_gmm.py
- gmm_aic_bic_plot.png
- cluster_probabilities.csv
- metrics_gmm.json
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

