/agent SARIMA

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — séries temporais

## Objectivo

Construir um modelo SARIMA para previsão de série temporal com componente sazonal.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar coluna temporal, target e frequência.
- Verificar datas em falta, duplicados e continuidade temporal.
- Analisar tendência e sazonalidade.
- Detectar período sazonal provável.
- Verificar estacionariedade.
- Gerar ACF e PACF.
- Fazer decomposição da série.
- Definir treino/validação/teste temporal sem shuffle.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se não houver sazonalidade clara, comparar com ARIMA simples e justificar.
- Se houver sazonalidade, definir m e parâmetros sazonais.
- Se a frequência for irregular, regularizar antes de modelar.
- Se houver múltiplas sazonalidades, documentar limitação do SARIMA e sugerir Prophet ou modelos avançados.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline seasonal naive.
- Testar parâmetros não sazonais e sazonais.
- Comparar por AIC/BIC e validação temporal.
- Treinar SARIMA final.
- Gerar forecast com intervalos.
- Avaliar no teste.
- Guardar relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- RMSE
- MAPE
- sMAPE
- AIC
- BIC
- Cobertura de intervalos quando aplicável

## Entregáveis obrigatórios

- eda_sarima.md
- train_sarima.py
- forecast_sarima.png
- metrics_sarima.json
- report_sarima.md

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

