/agent Algoritmos Meméticos

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Optimização evolutiva híbrida

## Objectivo

Implementar um Algoritmo Memético que combina algoritmo genético com pesquisa local.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Definir problema de optimização.
- Definir representação dos indivíduos.
- Definir função de fitness.
- Identificar restrições.
- Escolher método de pesquisa local adequado.
- Avaliar custo computacional da pesquisa local.
- Criar baseline com Algoritmo Genético clássico.
- Definir critérios de paragem.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se a pesquisa local for demasiado cara, aplicá-la apenas aos melhores indivíduos ou em intervalos.
- Se o algoritmo convergir cedo demais, aumentar diversidade ou reduzir intensidade da pesquisa local.
- Se não superar GA clássico, documentar que o custo extra não compensa.
- Se houver restrições, aplicar reparação ou penalização antes/depois da pesquisa local.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Implementar GA base.
- Implementar pesquisa local.
- Definir quando aplicar pesquisa local.
- Executar algoritmo memético.
- Comparar com GA clássico.
- Medir melhoria e custo computacional.
- Guardar melhor solução.
- Gerar relatório.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Melhor fitness
- Fitness médio
- Diversidade populacional
- Melhoria causada pela pesquisa local
- Tempo de execução
- Gerações até convergência
- Comparação com GA clássico

## Entregáveis obrigatórios

- analise_problema_memetico.md
- memetic_algorithm.py
- memetic_vs_ga.png
- fitness_evolution.png
- metrics_memetic.json
- best_solution.json

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

