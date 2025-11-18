# Correlating Automated and Human Evaluation of Code Documentation Generation Quality

Hu, Xing; Chen, Qiuyuan; Wang, Haoye; Xia, Xin; Lo, David; Zimmermann, Thomas. "Correlating Automated and Human Evaluation of Code Documentation Generation Quality," ACM Transactions on Software Engineering and Methodology, vol. 31, no. 4, pp. 1-28, 2022. doi: [10.1145/3502853](https://doi.org/10.1145/3502853)

## 1. Fichamento de Conteúdo

Este artigo investiga a correlação entre métricas automáticas e avaliações humanas da qualidade de documentação de código gerada por IA. Os autores realizaram um estudo empírico para determinar se métricas automáticas como BLEU, METEOR, ROUGE, CIDEr e SPICE são suficientemente confiáveis para substituir avaliação humana. A metodologia envolveu a replicação de três abordagens estado-da-arte para tarefas de geração de comentários de código e mensagens de commit. A documentação gerada foi avaliada tanto por métricas automáticas quanto por 24 participantes humanos, que consideraram aspectos de linguagem, conteúdo e eficácia. Os resultados revelaram que a classificação da documentação gerada pelas métricas automáticas difere significativamente quando comparada com avaliações especializadas. Embora o METEOR tenha apresentado a correlação mais forte (r≈0.7), essa correlação ainda foi inferior à observada entre diferentes especialistas (r≈0.8). Este estudo ressalta a necessidade de desenvolver abordagens de avaliação mais abrangentes que combinem múltiplas métricas automáticas. O trabalho demonstra que métricas automáticas não são confiáveis o suficiente para substituir completamente avaliação humana, mas podem servir como indicadores complementares quando usadas apropriadamente, destacando a importância de combinar avaliação automática com análise estática.

## 2. Fichamento Bibliográfico

* _Automatic Metrics_ (métricas automáticas) são medidas computacionais que avaliam texto gerado comparando com referências, incluindo BLEU, METEOR, ROUGE-L, CIDEr e SPICE (seção 2).
* _Human Evaluation Metrics_ (métricas de avaliação humana) capturam julgamentos de anotadores sobre linguagem, conteúdo e eficácia da documentação gerada, considerando aspectos que métricas automáticas não capturam adequadamente (seção 3.2).
* _Pearson Correlation_ (correlação de Pearson) mede a força e direção da relação linear entre duas variáveis contínuas, variando de -1 a 1, utilizada para quantificar correlação entre métricas automáticas e avaliação humana (seção 3.3).
* _Kendall's Tau_ (tau de Kendall) é uma medida de correlação baseada em ranks que avalia concordância entre ordenações, especialmente adequada quando a escala ordinal é mais relevante que valores absolutos (seção 3.3).
* _Code Documentation Generation_ (geração de documentação de código) refere-se à criação automática de comentários, descrições de funções e mensagens de commit usando técnicas de aprendizado profundo e modelos de linguagem (introdução).

## 3. Fichamento de Citações

* _"Automatic code documentation generation has been a crucial task in the field of software engineering."_
* _"Unfortunately, there is no evidence demonstrating the correlation between these metrics and human judgment on code documentation generation."_
* _"The results show that the ranking of generated documentation from automatic metrics is different from that evaluated by human annotators."_
* _"METEOR shows the strongest correlation (with moderate Pearson correlation r about 0.7) to human evaluation metrics."_
* _"However, it is still much lower than the correlation observed between different annotators (with a high Pearson correlation r about 0.8)."_
* _"These automatic metrics are not reliable enough to replace human evaluation for code documentation generation tasks."_
* _"Our findings suggest that combining multiple automatic metrics with static code analysis could provide more comprehensive quality assessment."_
