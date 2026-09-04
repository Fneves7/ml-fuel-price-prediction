/agent Kernel SVM

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — classificação

## Objectivo

Construir um classificador SVM com kernels para fronteiras de decisão não lineares.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar distribuição das classes.
- Avaliar separabilidade não linear.
- Verificar escala das variáveis.
- Identificar outliers.
- Avaliar dimensionalidade e custo computacional.
- Verificar valores em falta e duplicados.
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

- Se a EDA indicar linearidade suficiente, compara com SVM linear e justifica se kernel é necessário.
- Se as features tiverem escalas diferentes, normaliza obrigatoriamente.
- Se o dataset for grande, documenta custo computacional e usa amostragem/validação prudente.
- Se houver desequilíbrio de classes, usar class_weight e métricas robustas.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline.
- Separar treino/teste com stratify.
- Criar pipeline com normalização.
- Testar kernels RBF, polynomial e sigmoid quando adequado.
- Ajustar C e gamma.
- Usar validação cruzada.
- Comparar kernels.
- Avaliar no teste e guardar pipeline.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC se aplicável
- Matriz de confusão
- Comparação por kernel
- Tempo de treino

## Entregáveis obrigatórios

- eda_kernel_svm.md
- train_kernel_svm.py
- kernel_comparison.csv
- metrics_kernel_svm.json
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

