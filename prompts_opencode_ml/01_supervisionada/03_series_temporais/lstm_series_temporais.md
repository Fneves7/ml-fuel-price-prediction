/agent LSTM para Séries Temporais

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — deep learning para séries temporais

## Objectivo

Construir um modelo LSTM para previsão de séries temporais através de janelas sequenciais.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar target temporal e frequência.
- Verificar continuidade temporal, datas em falta e duplicados.
- Analisar tendência, sazonalidade, outliers e ruído.
- Avaliar tamanho da série e se é suficiente para LSTM.
- Definir janela temporal candidata.
- Verificar necessidade de normalização.
- Definir treino/validação/teste por ordem temporal.
- Verificar data leakage na criação de janelas.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se a série for curta, avisar que LSTM pode não ser adequado e comparar com ARIMA/Suavização.
- Se houver sazonalidade, escolher janelas que capturem o período sazonal.
- Se houver múltiplas variáveis, preparar formato multivariado.
- Se a validação piorar enquanto treino melhora, aplicar early stopping/dropout e reduzir complexidade.
- Se existirem lacunas temporais, tratar antes de criar janelas.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline naive ou média móvel.
- Normalizar dados com scaler ajustado só no treino.
- Criar janelas temporais.
- Treinar LSTM com validação e early stopping.
- Avaliar no teste.
- Gerar curvas de loss e forecast.
- Guardar modelo, scaler e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- RMSE
- MAPE
- sMAPE
- Loss de treino
- Loss de validação
- Comparação com baseline

## Entregáveis obrigatórios

- eda_lstm_series_temporais.md
- train_lstm_timeseries.py
- lstm_loss.png
- lstm_forecast.png
- metrics_lstm.json
- modelo e scaler guardados

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

