/agent ARIMA

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — séries temporais

## Objectivo

Construir um modelo ARIMA para previsão de série temporal univariada.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar coluna temporal e variável alvo.
- Verificar frequência, ordenação temporal, datas em falta e duplicados.
- Analisar tendência, sazonalidade aparente, ruído e outliers temporais.
- Verificar estacionariedade com testes e análise visual.
- Gerar ACF e PACF.
- Fazer decomposição temporal se aplicável.
- Definir separação treino/validação/teste por ordem temporal.
- Confirmar que não existe shuffle nem data leakage temporal.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se a série não for estacionária, aplicar diferenciação e documentar d.
- Se houver sazonalidade forte, considerar SARIMA em vez de ARIMA simples.
- Se existirem datas em falta, regularizar a frequência e tratar lacunas antes de treinar.
- Se houver outliers temporais, testar impacto com tratamento justificado.
- Se a série for muito curta, avisar sobre baixa fiabilidade da previsão.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline naive forecast.
- Testar combinações de p, d e q.
- Comparar modelos com AIC/BIC e validação temporal.
- Treinar ARIMA final.
- Prever no período de teste.
- Gerar gráfico real vs previsto.
- Guardar métricas e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- RMSE
- MAPE
- sMAPE
- AIC
- BIC
- Comparação com naive forecast

## Entregáveis obrigatórios

- eda_arima.md
- train_arima.py
- forecast_arima.png
- metrics_arima.json
- report_arima.md

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

