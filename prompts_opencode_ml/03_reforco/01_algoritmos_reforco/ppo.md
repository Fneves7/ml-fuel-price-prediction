/agent PPO

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem por reforço — policy optimization

## Objectivo

Implementar Proximal Policy Optimization para ambientes com acções discretas ou contínuas.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar espaço de observações.
- Identificar espaço de acções e se é discreto ou contínuo.
- Analisar função de recompensa.
- Identificar condições de fim de episódio.
- Criar baseline com agente aleatório.
- Definir métrica de sucesso.
- Avaliar recursos computacionais e duração do treino.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se a recompensa for mal definida, propor reformulação antes de treinar.
- Se o agente não melhorar, ajustar learning rate, clip range, entropy coefficient e número de steps.
- Se houver colapso de política, aumentar entropia ou reduzir learning rate.
- Se treino for instável, aumentar avaliação separada e seeds.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Configurar ambiente Gymnasium ou equivalente.
- Implementar baseline aleatória.
- Treinar PPO.
- Registar métricas de treino.
- Avaliar em episódios separados.
- Comparar com baseline.
- Guardar modelo.
- Criar script de inferência.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Recompensa média
- Recompensa acumulada
- Taxa de sucesso
- Episode length médio
- Policy loss
- Value loss
- Entropy
- KL divergence se disponível

## Entregáveis obrigatórios

- analise_ambiente_ppo.md
- train_ppo.py
- evaluate_ppo.py
- ppo_rewards.png
- metrics_ppo.json
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

