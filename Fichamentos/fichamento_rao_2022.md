# Comments on Comments: Where Code Review and Documentation Meet

Rao, Nikitha; Tsay, Jason; Hirzel, Martin; Hellendoorn, Vincent J. "Comments on comments: Where code review and documentation meet," Proceedings of the 44th International Conference on Software Engineering (ICSE), pp. 1-12, 2022.

🔗 arXiv: [2204.00107](https://arxiv.org/abs/2204.00107)  

## 1. Fichamento de Conteúdo

Este artigo investiga a intersecção entre revisão de código e documentação através de uma análise em larga escala de comentários de revisão relacionados à documentação. Uma função central da revisão de código é aumentar compreensão: ajudar revisores a entender mudanças de código auxilia na transferência de conhecimento e na descoberta de bugs. Comentários no código servem propósito similar, ajudando leitores futuros a compreender o programa. O estudo analisa aproximadamente 700 mil comentários de revisão em 2.000 projetos GitHub (Java e Python) para identificar quais comentários são respostas a mudanças na documentação ou solicitam tais mudanças, identificando 65 mil casos relevantes. Os autores desenvolvem uma taxonomia dos intents dos revisores por trás desses "comentários sobre comentários". A metodologia utiliza filtros automatizados combinados com validação manual para identificar comentários relacionados à documentação. Os resultados revelam que alcançar compreensão compartilhada do código é fundamental: comentários de revisores focam mais frequentemente em clarificação, seguido por apontar problemas a corrigir como erros de digitação e comentários desatualizados. Curiosamente, comentários clarificadores foram frequentemente sugeridos verbatim pelo revisor, indicando desejo de persistir seu entendimento adquirido durante a revisão. O trabalho conclui com discussão sobre implicações para melhorar revisão de código, incluindo potenciais benefícios para automatizar o processo de revisão.

## 2. Fichamento Bibliográfico

* _Comments on Comments_ refere-se especificamente a comentários de revisão que discutem, respondem ou solicitam mudanças em comentários e documentação do código (conceito central).
* _Documentation-Related Comments_ são comentários de revisão identificados como tratando especificamente de aspectos de documentação de código, seja responsivos ou prescritivos (foco do estudo).
* _Clarification Intent_ é a categoria mais comum de comentários, onde revisores buscam esclarecer ou melhorar a compreensibilidade da documentação existente (taxonomia).
* _Verbatim Suggestions_ referem-se a comentários onde revisores propõem texto exato de documentação, demonstrando transferência direta de conhecimento (padrão observado).
* _Shared Understanding_ (compreensão compartilhada) é o objetivo primário da interação entre revisores e autores sobre documentação, facilitando manutenção futura (insight principal).

## 3. Fichamento de Citações

* _"A central function of code review is to increase understanding; helping reviewers understand a code change aids in knowledge transfer and finding bugs."_
* _"Comments in code largely serve a similar purpose as code review, helping future readers understand the program."_
* _"We analyze ca. 700K review comments on 2,000 (Java and Python) GitHub projects, identifying 65K documentation-related cases."_
* _"Reviewer comments most often focused on clarification, followed by pointing out issues to fix, such as typos and outdated comments."_
* _"Clarifying comments were frequently suggested verbatim by the reviewer, indicating a desire to persist their understanding acquired during code review."_
* _"Our findings have implications for improving code review and automating the review process, particularly in generating high-quality documentation suggestions."_
