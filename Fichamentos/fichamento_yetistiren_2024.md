# Evaluating the Code Quality of AI-Assisted Code Generation Tools

Yetiştiren, Burak; Özsoy, Işık; Ayerdem, Miray; Tüzün, Eray. "Evaluating the code quality of AI-assisted code generation tools: An empirical study on GitHub Copilot, Amazon CodeWhisperer, and ChatGPT," IEEE Software, vol. 41, no. 3, pp. 86-94, 2024.

🔗 arXiv: [2304.10778](https://arxiv.org/abs/2304.10778)

## 1. Fichamento de Conteúdo

Este estudo realiza uma avaliação empírica comparativa das ferramentas de geração de código assistidas por IA mais proeminentes: GitHub Copilot, Amazon CodeWhisperer e ChatGPT. O objetivo é comparar o desempenho dessas ferramentas em termos de métricas de qualidade de código, incluindo Validade do Código, Correção do Código, Segurança do Código, Confiabilidade do Código e Manutenibilidade do Código. A metodologia utiliza o benchmark HumanEval Dataset contendo 164 problemas de programação para avaliar as capacidades de geração de código. O código gerado é então avaliado com base nas métricas de qualidade propostas usando ferramentas como SonarQube. Os resultados revelam que as versões mais recentes do ChatGPT, GitHub Copilot e Amazon CodeWhisperer geram código correto 65,2%, 46,3% e 31,1% das vezes, respectivamente. As versões mais recentes do GitHub Copilot e Amazon CodeWhisperer mostraram taxas de melhoria de 18% para GitHub Copilot e 7% para Amazon CodeWhisperer. A dívida técnica média, considerando code smells, foi de 8,9 minutos para ChatGPT, 9,1 minutos para GitHub Copilot e 5,6 minutos para Amazon CodeWhisperer. Este estudo destaca os pontos fortes e fracos de algumas das ferramentas de geração de código mais populares, fornecendo insights valiosos para profissionais que buscam selecionar a ferramenta ideal para tarefas específicas.

## 2. Fichamento Bibliográfico

* _Code Validity_ (validade do código) refere-se à capacidade do código gerado de ser compilado e executado sem erros sintáticos, medida pela taxa de sucesso na execução (seção de metodologia).
* _Code Correctness_ (correção do código) avalia se o código gerado resolve corretamente o problema proposto, passando em todos os casos de teste fornecidos pelo HumanEval Dataset (seção de métricas).
* _Technical Debt_ (dívida técnica) representa o tempo estimado necessário para corrigir problemas de qualidade identificados no código, incluindo code smells, bugs e vulnerabilidades (seção de avaliação).
* _HumanEval Dataset_ é um benchmark de 164 problemas de programação em Python usado para avaliar modelos de geração de código, originalmente proposto pela OpenAI (seção de setup experimental).
* _Code Security_ (segurança do código) mede a presença de vulnerabilidades e falhas de segurança no código gerado, avaliada usando análise estática com SonarQube (métricas de qualidade).

## 3. Fichamento de Citações

* _"AI-assisted code generation tools have become increasingly prevalent in software engineering, offering the ability to generate code from natural language prompts or partial code inputs."_
* _"Our analysis reveals that the latest versions of ChatGPT, GitHub Copilot, and Amazon CodeWhisperer generate correct code 65.2%, 46.3%, and 31.1% of the time, respectively."_
* _"The newer versions of GitHub Copilot and Amazon CodeWhisperer showed improvement rates of 18% for GitHub Copilot and 7% for Amazon CodeWhisperer."_
* _"The average technical debt, considering code smells, was found to be 8.9 minutes for ChatGPT, 9.1 minutes for GitHub Copilot, and 5.6 minutes for Amazon CodeWhisperer."_
* _"This study highlights the strengths and weaknesses of some of the most popular code generation tools, providing valuable insights for practitioners."_
* _"By comparing these generators, our results may assist practitioners in selecting the optimal tool for specific tasks, enhancing their decision-making process."_
