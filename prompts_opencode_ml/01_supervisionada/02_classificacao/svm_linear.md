/agent SVM Linear

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — classificação

## Objectivo

Construir um classificador SVM linear para problemas aproximadamente separáveis por uma fronteira linear.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Analisar distribuição das classes.
- Avaliar separabilidade linear das features.
- Verificar valores em falta, duplicados e outliers.
- Avaliar escala das variáveis.
- Analisar dimensionalidade.
- Verificar desequilíbrio de classes.
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

- Se as features tiverem escalas diferentes, normaliza obrigatoriamente.
- Se houver classes desequilibradas, usar class_weight e métricas adequadas.
- Se a EDA sugerir fronteira não linear, documenta limitação e compara com Kernel SVM.
- Se houver muitos outliers, analisa impacto no hiperplano.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline.
- Separar treino/teste com stratify.
- Criar pipeline com normalização.
- Treinar SVM linear.
- Ajustar parâmetro C.
- Usar validação cruzada.
- Avaliar no teste.
- Guardar pipeline.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC se aplicável
- Matriz de confusão
- Tempo de treino

## Entregáveis obrigatórios

- eda_svm_linear.md
- train_svm_linear.py
- svm_c_comparison.csv
- metrics_svm_linear.json
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

