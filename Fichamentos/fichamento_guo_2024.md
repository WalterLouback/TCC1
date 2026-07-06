# Exploring the Potential of ChatGPT in Automated Code Refinement: An Empirical Study

Guo, Qi; Cao, Junming; Xie, Xiaofei; Liu, Shangqing; Li, Xiaohong; Chen, Bihuan; Peng, Xin. "Exploring the potential of ChatGPT in automated code refinement: An empirical study," Proceedings of the 46th IEEE/ACM International Conference on Software Engineering (ICSE), pp. 1-13, 2024.

🔗 arXiv: [2309.08221](https://arxiv.org/abs/2309.08221)  
🔗 ACM DL: [10.1145/3597503.3623306](https://doi.org/10.1145/3597503.3623306)

## 1. Fichamento de Conteúdo

Este trabalho conduz o primeiro estudo empírico para entender as capacidades do ChatGPT em tarefas de refinamento automatizado de código, focando especificamente no refinamento baseado em comentários de revisão de código. Revisão de código é uma atividade essencial para garantir qualidade e manutenibilidade de projetos de software, mas é uma tarefa que consome tempo e frequentemente propensa a erros. O estudo utiliza o benchmark CodeReview existente e constrói um novo dataset de revisão de código de alta qualidade (CodeReview-New) para avaliação. A metodologia compara o desempenho do ChatGPT com o CodeReviewer, uma ferramenta de revisão de código estado-da-arte. Os resultados demonstram que o ChatGPT supera significativamente o CodeReviewer em tarefas de refinamento de código, alcançando scores de Exact Match (EM) e BLEU de 22,78 e 76,44 respectivamente, enquanto o método estado-da-arte atinge apenas 15,50 e 62,88 no dataset de alta qualidade. O estudo investiga o impacto de diferentes configurações de prompts e temperatura, revelando que configurações de temperatura mais baixas produzem resultados melhores e mais estáveis. Identificam-se as causas raiz para o desempenho inferior do ChatGPT em certos casos, incluindo falta de conhecimento de domínio, localização pouco clara e mudanças ambíguas nos comentários de revisão. São propostas estratégias preliminares para mitigar esses desafios, incluindo o uso de modelos mais avançados como GPT-4.

## 2. Fichamento Bibliográfico

* _Code Refinement_ (refinamento de código) é o processo de melhorar código existente baseado em feedback de revisão, mantendo funcionalidade enquanto aumenta qualidade e legibilidade (introdução).
* _Exact Match (EM) Score_ mede a proporção de refinamentos de código que correspondem exatamente à referência esperada, sendo uma métrica rigorosa de correção (metodologia de avaliação).
* _Temperature Settings_ (configurações de temperatura) controlam a aleatoriedade das respostas geradas pelo ChatGPT, onde temperaturas mais baixas produzem saídas mais determinísticas e consistentes (análise de RQ1).
* _CodeReview Dataset_ é um benchmark contendo pares de código original, comentários de revisão e código refinado, usado para treinar e avaliar sistemas de refinamento automático (setup experimental).
* _Prompt Engineering_ refere-se ao design cuidadoso de instruções textuais fornecidas a modelos de linguagem para otimizar seu desempenho em tarefas específicas (técnica metodológica).

## 3. Fichamento de Citações

* _"Code review is an essential activity for ensuring the quality and maintainability of software projects. However, it is a time-consuming and often error-prone task."_
* _"ChatGPT outperforms CodeReviewer in code refinement tasks, achieving higher EM and BLEU scores of 22.78 and 76.44 respectively, while the state-of-the-art method achieves only 15.50 and 62.88."_
* _"Different prompts and temperature settings can have a significant impact of up to 5% and 15% on ChatGPT's Exact Match scores in code refinement tasks."_
* _"Lower temperature settings yield better and more stable results, and describing the code review scenario in the prompt helps enhance ChatGPT's performance."_
* _"ChatGPT struggles on tasks involving refining documentation and functionalities, mainly due to a lack of domain knowledge, unclear location, and unclear changes in the review comments."_
* _"Our study highlights the potential of ChatGPT in code refinement tasks and identifies important directions for future research, including improving review quality and using more advanced models like GPT-4."_
