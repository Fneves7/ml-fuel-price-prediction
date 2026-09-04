/agent LDA

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Redução de dimensionalidade — supervisionada

## Objectivo

Aplicar Linear Discriminant Analysis para reduzir dimensionalidade maximizando separação entre classes.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Confirmar que existem labels/classes.
- Analisar distribuição das classes.
- Verificar valores em falta, duplicados e outliers.
- Seleccionar features numéricas ou preparar encoding.
- Avaliar escala das variáveis.
- Avaliar separabilidade inicial entre classes.
- Verificar data leakage.
- Comparar objectivo de LDA com PCA.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se não existirem labels, não usar LDA e sugerir PCA/Kernel PCA.
- Se classes estiverem desequilibradas, avaliar impacto na projecção e nas métricas.
- Se houver mais classes, respeitar limite máximo de componentes n_classes - 1.
- Se LDA não separar bem classes, documentar limitação e comparar com PCA ou modelos não lineares.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Preparar dados e labels.
- Aplicar LDA.
- Visualizar componentes discriminantes.
- Comparar com PCA.
- Treinar classificador simples downstream se adequado.
- Avaliar separação e desempenho.
- Guardar transformação e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Variância discriminante explicada
- Accuracy downstream
- F1-score downstream
- Matriz de confusão se houver classificador
- Separação visual entre classes

## Entregáveis obrigatórios

- eda_lda.md
- lda_analysis.py
- lda_projection.png
- metrics_lda.json
- lda_vs_pca.md

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
## Nota específica

Nota: LDA precisa de labels; não é um método puramente não supervisionado.

