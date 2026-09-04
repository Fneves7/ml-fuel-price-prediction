/agent Deep Q-Learning

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem por reforço — deep reinforcement learning

## Objectivo

Implementar Deep Q-Learning/DQN para ambientes com estados complexos e acções discretas.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar espaço de observações.
- Confirmar que o espaço de acções é discreto.
- Analisar função de recompensa.
- Identificar condições de fim de episódio.
- Avaliar tamanho do estado e necessidade de rede neuronal.
- Criar baseline com agente aleatório.
- Avaliar recursos computacionais.
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

- Se as acções forem contínuas, não usar DQN; sugerir PPO/SAC/DDPG.
- Se o treino for instável, ajustar replay buffer, target network, learning rate e epsilon decay.
- Se a recompensa for esparsa, rever reward shaping.
- Se DQN não superar agente aleatório, verificar bugs no ambiente, escala de recompensas e exploração.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Implementar agente aleatório.
- Criar rede para Q-values.
- Implementar replay buffer.
- Implementar target network.
- Implementar política epsilon-greedy.
- Treinar por episódios.
- Registar loss e recompensas.
- Avaliar sem exploração.
- Guardar modelo.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Recompensa média
- Recompensa acumulada
- Taxa de sucesso
- Loss da rede
- Passos médios por episódio
- Episódios até threshold
- Comparação com agente aleatório

## Entregáveis obrigatórios

- analise_ambiente_dqn.md
- train_dqn.py
- dqn_rewards.png
- dqn_loss.png
- dqn_model.pt
- metrics_dqn.json

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

