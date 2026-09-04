/agent Amostragem de Thompson

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem por reforço — Multi-Armed Bandits

## Objectivo

Implementar Thompson Sampling para selecção de acções com abordagem probabilística bayesiana.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar número de braços/acções.
- Definir tipo de recompensa: binária, contínua ou outra.
- Analisar distribuição esperada das recompensas.
- Definir prior adequada.
- Definir horizonte temporal.
- Criar baseline aleatória.
- Verificar se o problema é bandit ou exige estado.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se a recompensa for binária, usar Beta-Bernoulli.
- Se a recompensa for contínua, escolher distribuição apropriada ou documentar simplificação.
- Se o ambiente não for estacionário, considerar adaptação ou janela temporal.
- Se existir estado complexo, avisar que bandit simples não captura o problema.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Implementar baseline aleatória.
- Implementar Thompson Sampling.
- Simular várias rondas.
- Actualizar posteriores.
- Medir recompensa e regret.
- Comparar com UCB se existir.
- Gerar gráficos e relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Recompensa acumulada
- Recompensa média
- Regret acumulado
- Percentagem de escolha da melhor acção
- Estabilidade da política

## Entregáveis obrigatórios

- analise_ambiente_thompson.md
- train_thompson_sampling.py
- thompson_rewards.png
- thompson_action_selection.png
- metrics_thompson.json

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

