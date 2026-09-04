/agent Q-Learning

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem por reforço — controlo tabular

## Objectivo

Implementar Q-Learning para ambientes com estados e acções discretos.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar espaço de estados.
- Identificar espaço de acções.
- Descrever função de recompensa.
- Identificar condições de fim de episódio.
- Avaliar se o espaço de estados é pequeno o suficiente para tabela Q.
- Criar baseline com agente aleatório.
- Definir métrica de sucesso.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se o espaço de estados for grande ou contínuo, sugerir DQN ou discretização justificada.
- Se a recompensa for esparsa, propor shaping ou treino mais longo.
- Se o agente não melhorar face à baseline, ajustar alpha, gamma, epsilon e exploração.
- Se a política convergir cedo demais, aumentar exploração ou rever recompensas.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Implementar agente aleatório.
- Implementar tabela Q.
- Definir alpha, gamma e epsilon.
- Treinar por episódios.
- Registar recompensas e passos.
- Avaliar política final sem exploração.
- Testar hiperparâmetros.
- Guardar Q-table.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Recompensa média por episódio
- Recompensa acumulada
- Taxa de sucesso
- Passos médios por episódio
- Episódios até convergência
- Comparação com agente aleatório

## Entregáveis obrigatórios

- analise_ambiente_q_learning.md
- train_q_learning.py
- q_learning_rewards.png
- q_table.npy
- metrics_q_learning.json

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

