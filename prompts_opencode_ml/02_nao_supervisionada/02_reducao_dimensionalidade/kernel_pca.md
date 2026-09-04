/agent Kernel PCA

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Redução de dimensionalidade — não linear

## Objectivo

Aplicar Kernel PCA para redução de dimensionalidade não linear.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar tipos de variáveis e seleccionar features numéricas.
- Verificar valores em falta, duplicados e outliers.
- Analisar escala das variáveis.
- Procurar relações não lineares.
- Comparar visualmente com PCA linear.
- Avaliar custo computacional.
- Verificar objectivo: visualização, pré-processamento ou separabilidade.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se a EDA indicar relações lineares simples, comparar com PCA e justificar se Kernel PCA é necessário.
- Se as escalas forem diferentes, normalizar obrigatoriamente.
- Se o dataset for grande, documentar custo e usar amostragem se necessário.
- Se visualizações mudarem muito por kernel, documentar sensibilidade.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Normalizar dados.
- Aplicar PCA linear como referência.
- Testar kernels RBF, polynomial e sigmoid quando adequado.
- Comparar visualizações e métricas downstream.
- Seleccionar kernel justificado.
- Guardar transformação e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Erro de reconstrução quando disponível
- Silhouette score se usado com clustering
- Desempenho downstream se houver modelo posterior
- Tempo de execução
- Separabilidade visual

## Entregáveis obrigatórios

- eda_kernel_pca.md
- kernel_pca_analysis.py
- kernel_pca_comparison.png
- metrics_kernel_pca.json
- transformacao_guardada

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

