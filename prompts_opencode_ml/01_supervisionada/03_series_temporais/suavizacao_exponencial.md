/agent Suavização Exponencial

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — séries temporais

## Objectivo

Construir modelos de Suavização Exponencial: simples, Holt ou Holt-Winters, conforme a EDA.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar coluna temporal, target e frequência.
- Verificar continuidade temporal, datas em falta e duplicados.
- Analisar nível, tendência e sazonalidade.
- Detectar outliers temporais.
- Separar treino/teste por ordem temporal.
- Verificar se a série é adequada a modelos de suavização.
- Confirmar ausência de data leakage temporal.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se só houver nível sem tendência/sazonalidade, usar suavização simples.
- Se houver tendência, usar Holt.
- Se houver sazonalidade, usar Holt-Winters.
- Se a frequência for irregular, regularizar antes de treinar.
- Se a sazonalidade não for estável, documentar limitação e comparar com Prophet/SARIMA.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline naive.
- Treinar suavização simples, Holt e Holt-Winters quando aplicável.
- Comparar modelos.
- Avaliar no teste.
- Gerar gráfico real vs previsto.
- Guardar métricas e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- RMSE
- MAPE
- sMAPE
- AIC se disponível
- Comparação com baseline

## Entregáveis obrigatórios

- eda_suavizacao_exponencial.md
- train_exponential_smoothing.py
- smoothing_comparison.csv
- forecast_exponential_smoothing.png
- metrics_exponential_smoothing.json

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

