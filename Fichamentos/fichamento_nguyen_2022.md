# An Empirical Evaluation of GitHub Copilot's Code Suggestions

Nguyen, Nhan; Nadi, Sarah. "An empirical evaluation of GitHub Copilot's code suggestions," Proceedings of the 19th International Conference on Mining Software Repositories (MSR), pp. 1-5, 2022.

🔗 DOI: [10.1109/MSR52599.2022.00014](https://doi.org/10.1109/MSR52599.2022.00014)

## 1. Fichamento de Conteúdo

Este artigo apresenta a primeira avaliação empírica sistemática das sugestões de código do GitHub Copilot, um "programador de par de IA" lançado pelo GitHub e OpenAI. O estudo investiga duas questões principais: quão corretas são as sugestões de código do Copilot e quão compreensível é o código fornecido. A metodologia utiliza 33 questões do LeetCode em quatro linguagens de programação (Python, Java, JavaScript e C) para criar contextos de consulta apropriados e coletar 132 sugestões de código. A correção é avaliada executando os casos de teste fornecidos pelo LeetCode, enquanto a compreensibilidade é medida usando as métricas de complexidade ciclomática e complexidade cognitiva do SonarQube. Os resultados mostram que as sugestões Java do Copilot têm a maior pontuação de correção (57%), enquanto JavaScript apresenta a menor (27%). De modo geral, as sugestões do Copilot têm baixa complexidade, sem diferenças notáveis entre as linguagens de programação. O estudo também identifica potenciais deficiências do Copilot, como gerar código que pode ser ainda mais simplificado e código que depende de métodos auxiliares indefinidos. As descobertas fornecem insights importantes sobre as capacidades atuais do Copilot e direções para melhorias futuras.

## 2. Fichamento Bibliográfico

* _GitHub Copilot_ é um assistente de programação baseado em IA que utiliza Processamento de Linguagem Natural, Análise Estática, Síntese de Código e Inteligência Artificial para gerar código a partir de descrições em linguagem natural (introdução).
* _LeetCode Dataset_ é uma plataforma online de problemas de programação usada para avaliar a correção das sugestões de código, fornecendo casos de teste automatizados (metodologia experimental).
* _Cyclomatic Complexity_ (complexidade ciclomática) mede o número de caminhos independentes através do código-fonte, indicando o número de casos de teste necessários para cobertura completa (métricas de avaliação).
* _Cognitive Complexity_ (complexidade cognitiva) avalia o quão difícil é entender o fluxo de controle do código, focando em quebras no fluxo linear e aninhamento de estruturas (métricas de compreensibilidade).
* _Query Context_ (contexto de consulta) refere-se ao conjunto de informações fornecidas ao Copilot para gerar sugestões, incluindo descrições de problemas e declarações de funções (setup experimental).

## 3. Fichamento de Citações

* _"GitHub and OpenAI recently launched Copilot, an 'AI pair programmer' that utilizes the power of Natural Language Processing, Static Analysis, Code Synthesis, and Artificial Intelligence."_
* _"Given a natural language description of the target functionality, Copilot can generate corresponding code in several programming languages."_
* _"We find that Copilot's Java suggestions have the highest correctness score (57%) while JavaScript is lowest (27%)."_
* _"Overall, Copilot's suggestions have low complexity with no notable differences between the programming languages."_
* _"We also find some potential Copilot shortcomings, such as generating code that can be further simplified and code that relies on undefined helper methods."_
* _"GitHub's internal evaluation of Copilot Python suggestions shows that Copilot achieved 43% correctness on the first try, which is similar to our Python results (42%)."_
