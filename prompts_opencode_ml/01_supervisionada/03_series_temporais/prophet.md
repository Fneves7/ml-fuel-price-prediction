/agent Prophet

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — séries temporais

## Objectivo

Construir um modelo Prophet para previsão com tendência, sazonalidade, feriados e eventos.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar coluna temporal e target.
- Converter mentalmente o dataset para formato ds/y.
- Verificar frequência, datas em falta, duplicados e outliers.
- Analisar tendência, sazonalidades e eventos conhecidos.
- Verificar se existem feriados, campanhas ou regressors externos.
- Separar treino/teste por ordem temporal.
- Verificar data leakage temporal.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se a série tiver sazonalidade clara, configurar sazonalidades adequadas.
- Se existirem eventos/feriados relevantes, adicioná-los como componentes.
- Se a série for curta, documentar incerteza e comparar com baseline simples.
- Se houver outliers, testar tratamento ou robustez do modelo.
- Se Prophet não estiver instalado, criar instruções de instalação e alternativa com statsmodels.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline naive.
- Preparar dados em formato ds/y.
- Treinar Prophet.
- Gerar forecast e componentes.
- Avaliar no período de teste.
- Guardar gráficos e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- RMSE
- MAPE
- sMAPE
- Cobertura dos intervalos
- Comparação com baseline

## Entregáveis obrigatórios

- eda_prophet.md
- train_prophet.py
- prophet_forecast.png
- prophet_components.png
- metrics_prophet.json
- report_prophet.md

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

