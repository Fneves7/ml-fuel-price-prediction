/agent PCA

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Redução de dimensionalidade — não supervisionada

## Objectivo

Aplicar PCA para reduzir dimensionalidade, visualizar dados e analisar variância explicada.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar tipos de variáveis e seleccionar variáveis numéricas.
- Verificar valores em falta, duplicados e outliers.
- Analisar escala das variáveis.
- Avaliar correlações e redundância.
- Analisar variância das features.
- Verificar se há features constantes ou quase constantes.
- Avaliar objectivo: compressão, visualização ou pré-processamento.

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
- Se outliers forem fortes, testar PCA com e sem tratamento.
- Se poucas componentes explicarem muita variância, recomendar redução.
- Se a variância explicada estiver muito dispersa, documentar que a redução pode perder muita informação.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Normalizar dados.
- Aplicar PCA.
- Calcular variância explicada.
- Criar scree plot.
- Escolher número de componentes.
- Visualizar dados em 2D/3D quando útil.
- Analisar loadings.
- Guardar transformação.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Variância explicada por componente
- Variância explicada acumulada
- Número de componentes para 90% e 95%
- Erro de reconstrução se aplicável

## Entregáveis obrigatórios

- eda_pca.md
- pca_analysis.py
- scree_plot.png
- pca_2d.png
- loadings.csv
- metrics_pca.json

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

