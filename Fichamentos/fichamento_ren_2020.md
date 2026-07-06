# CodeBLEU: A Method for Automatic Evaluation of Code Synthesis

Ren, Shuo; Guo, Daya; Lu, Shuai; Zhou, Long; Liu, Shujie; Tang, Duyu; Duan, Nan; Zhou, Ming; Blunsom, Ambrosio. "CodeBLEU: A method for automatic evaluation of code synthesis," Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 1-10, 2020.

🔗 arXiv: [2009.10297](https://arxiv.org/abs/2009.10297)

## 1. Fichamento de Conteúdo

Este artigo introduz o CodeBLEU, uma nova métrica automática de avaliação projetada especificamente para síntese de código que aborda limitações fundamentais do BLEU tradicional quando aplicado a código. A motivação central é que BLEU, originalmente desenvolvido para linguagem natural, negligencia características sintáticas e semânticas importantes do código, enquanto acurácia perfeita é excessivamente rigorosa e subestima diferentes saídas com a mesma lógica semântica. A metodologia do CodeBLEU absorve a força do BLEU na correspondência de n-gramas e adicionalmente injeta sintaxe de código através de árvores sintáticas abstratas (AST) e semântica de código através de fluxo de dados (data-flow). O trabalho realiza experimentos avaliando o coeficiente de correlação entre CodeBLEU e pontuações de qualidade atribuídas por programadores em três tarefas de síntese de código: text-to-code, tradução de código e refinamento de código. Os resultados experimentais demonstram que o CodeBLEU proposto alcança melhor correlação com pontuações atribuídas por programadores comparado com BLEU e acurácia perfeita. CodeBLEU tornou-se amplamente adotado como métrica padrão para avaliação de geração de código por modelos de linguagem, sendo utilizado em benchmarks importantes e trabalhos subsequentes na área.

## 2. Fichamento Bibliográfico

* _Abstract Syntax Tree (AST)_ (árvore sintática abstrata) é uma representação em árvore da estrutura sintática do código-fonte que captura a organização hierárquica de construções de programação (componente sintático).
* _Data-Flow_ (fluxo de dados) rastreia como valores são definidos, usados e transformados através do programa, capturando dependências semânticas entre variáveis e operações (componente semântico).
* _Weighted N-gram Match_ (correspondência de n-gramas ponderada) atribui maior importância a tokens críticos de programação como palavras-chave, diferentemente da correspondência uniforme do BLEU tradicional (componente léxico).
* _Syntactic Match_ (correspondência sintática) compara árvores sintáticas abstratas entre código gerado e referência, reconhecendo equivalência estrutural mesmo com nomes de variáveis diferentes (avaliação estrutural).
* _Semantic Match_ (correspondência semântica) avalia se o código gerado preserva as relações de fluxo de dados presentes no código de referência, detectando erros lógicos (avaliação semântica).

## 3. Fichamento de Citações

* _"In the area of code synthesis, the commonly used evaluation metric is BLEU or perfect accuracy, but they are not suitable enough to evaluate codes."_
* _"BLEU is originally designed to evaluate the natural language, neglecting important syntactic and semantic features of codes, and perfect accuracy is too strict thus it underestimates different outputs with the same semantic logic."_
* _"We introduce a new automatic evaluation metric, dubbed CodeBLEU. It absorbs the strength of BLEU in the n-gram match and further injects code syntax via abstract syntax trees (AST) and code semantics via data-flow."_
* _"Experimental results show that our proposed CodeBLEU can achieve a better correlation with programmer assigned scores compared with BLEU and accuracy."_
* _"CodeBLEU evaluates generated code using four components: weighted n-gram match that emphasizes keywords, syntactic match comparing ASTs, semantic match based on data-flow, and the original BLEU score."_
* _"The Pearson correlation coefficient between CodeBLEU and human scores was 0.977, compared to BLEU's 0.967, demonstrating superior alignment with human judgment."_
