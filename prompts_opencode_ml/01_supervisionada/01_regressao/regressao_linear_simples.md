/agent Regressão Linear Simples

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — regressão

## Objectivo

Construir uma solução de Regressão Linear Simples, usando uma única variável explicativa para prever uma variável numérica contínua.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar a variável alvo e a variável explicativa candidata.
- Verificar dimensão do dataset, tipos de dados, valores em falta e duplicados.
- Analisar distribuição da variável alvo e da variável explicativa.
- Criar gráfico de dispersão entre X e y.
- Medir correlação entre X e y.
- Verificar outliers em X e y.
- Avaliar visualmente se existe relação aproximadamente linear.
- Verificar risco de data leakage entre a variável explicativa e a variável alvo.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se a relação X-y não for aproximadamente linear, documenta essa conclusão e propõe Regressão Polinomial ou outro modelo antes de treinar.
- Se existirem outliers fortes, cria uma experiência com os dados originais e outra com tratamento justificado dos outliers.
- Se a variável explicativa tiver muitos valores em falta, propõe imputação ou troca de variável explicativa.
- Se a correlação for muito fraca, treina o modelo apenas como baseline e avisa que o poder preditivo esperado é baixo.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline com média ou mediana da variável alvo.
- Separar treino e teste.
- Treinar Regressão Linear Simples.
- Avaliar no conjunto de teste.
- Analisar resíduos.
- Criar gráficos real vs previsto, linha ajustada e resíduos.
- Guardar modelo e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- MSE
- RMSE
- R²
- Erro médio dos resíduos
- Comparação com baseline

## Entregáveis obrigatórios

- eda_regressao_linear_simples.md
- train_regressao_linear_simples.py
- metrics_regressao_linear_simples.json
- real_vs_previsto.png
- residuos.png
- modelo guardado em /models

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

