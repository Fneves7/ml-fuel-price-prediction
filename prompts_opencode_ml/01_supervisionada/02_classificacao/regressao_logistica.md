/agent Regressão Logística

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — classificação

## Objectivo

Construir um classificador com Regressão Logística para problemas binários ou multiclasse.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar target e classes.
- Analisar distribuição das classes e desequilíbrio.
- Analisar valores em falta, duplicados e outliers.
- Identificar variáveis numéricas e categóricas.
- Estudar relações entre features e classes.
- Avaliar correlações e possíveis features redundantes.
- Verificar escala das variáveis.
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

- Se as classes estiverem desequilibradas, usar class_weight, métricas adequadas e PR-AUC quando aplicável.
- Se houver variáveis em escalas diferentes, aplicar StandardScaler no pipeline.
- Se houver categóricas, aplicar OneHotEncoder dentro do pipeline.
- Se a fronteira parecer não linear, documentar limitação e sugerir Kernel SVM ou ensemble.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline com classe maioritária.
- Separar treino/teste com stratify.
- Criar pipeline de pré-processamento.
- Treinar Regressão Logística.
- Ajustar regularização e C.
- Avaliar probabilidades e classes previstas.
- Gerar matriz de confusão e relatório de classificação.
- Guardar pipeline.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC se aplicável
- PR-AUC se desequilibrado
- Log loss
- Matriz de confusão

## Entregáveis obrigatórios

- eda_regressao_logistica.md
- train_regressao_logistica.py
- metrics_regressao_logistica.json
- classification_report.md
- confusion_matrix.png
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

