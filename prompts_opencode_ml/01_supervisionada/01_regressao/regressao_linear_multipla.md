/agent Regressão Linear Múltipla

## Papel do OpenCode

Actua como um agente autónomo de Machine Learning dentro deste repositório.

Não executes treino imediatamente. Primeiro faz uma análise exploratória de dados ou análise do ambiente/problema. Só depois decides como avançar.

Deves trabalhar de forma incremental, criando código, métricas, gráficos e relatório. Não inventes resultados. Se não conseguires executar algo no ambiente actual, deixa isso explícito no relatório.

## Tipo de problema

Aprendizagem supervisionada — regressão

## Objectivo

Construir uma solução de Regressão Linear Múltipla com várias variáveis explicativas para prever uma variável numérica contínua.

## Fase 1 — Análise exploratória obrigatória

Antes de qualquer treino, implementação principal ou optimização, faz a análise inicial seguinte:

- Identificar target e features candidatas.
- Analisar tipos de dados, valores em falta, duplicados e outliers.
- Estudar distribuição do target.
- Avaliar correlações entre features e target.
- Avaliar correlações entre features para detectar multicolinearidade.
- Identificar variáveis categóricas que exigem encoding.
- Procurar variáveis que possam causar data leakage.
- Verificar escala das variáveis e necessidade de normalização.

Cria um relatório inicial com conclusões objectivas. O relatório deve explicar:
- O que os dados/ambiente mostram.
- Que problemas foram encontrados.
- Que decisões técnicas decorrem dessa análise.
- Que riscos existem.
- Que pré-processamento ou alteração de abordagem é necessário.

## Reagir com base na análise exploratória

Depois da análise exploratória, adapta o plano. Não sigas cegamente o algoritmo se a EDA mostrar que ele é inadequado.

Regras de decisão:

- Se houver multicolinearidade forte, calcula VIF quando possível e considera remover features redundantes ou usar Ridge/Lasso.
- Se existirem categóricas, usa encoding dentro de Pipeline/ColumnTransformer.
- Se existirem outliers relevantes, testa impacto com e sem tratamento.
- Se houver suspeita de data leakage, remove a variável problemática e documenta a decisão.
- Se a relação parecer não linear, compara com regressão polinomial ou modelo não linear.

Antes de implementar o treino/modelo final, escreve um pequeno plano actualizado com base no que foi observado.

## Fluxo de trabalho esperado

- Criar baseline simples.
- Criar pipeline de pré-processamento.
- Separar treino/teste.
- Treinar Regressão Linear Múltipla.
- Avaliar métricas.
- Analisar coeficientes e estabilidade.
- Gerar gráficos de resíduos.
- Guardar pipeline completo.

## Métricas de avaliação obrigatórias

Regista as métricas num ficheiro estruturado, preferencialmente JSON ou CSV.

- MAE
- MSE
- RMSE
- R²
- R² ajustado quando aplicável
- VIF quando aplicável
- Comparação com baseline

## Entregáveis obrigatórios

- eda_regressao_linear_multipla.md
- train_regressao_linear_multipla.py
- metrics_regressao_linear_multipla.json
- coeficientes.md
- residuos.png
- pipeline/modelo guardado

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

