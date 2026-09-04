/agent NSGA-II

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Optimização evolutiva multi-objectivo

## Objectivo

Implementar NSGA-II para problemas de optimização multi-objectivo e obter uma frente de Pareto.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Definir objectivos múltiplos.
- Identificar conflitos entre objectivos.
- Definir variáveis de decisão e representação.
- Identificar restrições.
- Definir função de avaliação multi-objectivo.
- Definir baseline aleatória ou heurística.
- Avaliar dimensão do espaço de procura.
- Definir critério de paragem.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se os objectivos não forem realmente conflitantes, documentar e simplificar se adequado.
- Se houver restrições fortes, aplicar penalização ou reparação.
- Se a frente de Pareto tiver pouca diversidade, ajustar crowding distance, mutação ou população.
- Se o hypervolume não melhorar, rever operadores e parâmetros.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Implementar população inicial.
- Implementar avaliação multi-objectivo.
- Implementar non-dominated sorting.
- Implementar crowding distance.
- Implementar selecção, crossover e mutação.
- Executar gerações.
- Extrair frente de Pareto.
- Visualizar soluções.
- Guardar métricas e soluções.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- Hypervolume
- Número de soluções não dominadas
- Spread da frente de Pareto
- Crowding distance médio
- Generational distance se aplicável
- Tempo de execução

## Entregáveis obrigatórios

- analise_problema_nsga2.md
- nsga2.py
- pareto_front.png
- metrics_nsga2.json
- pareto_solutions.csv
- report_nsga2.md

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

