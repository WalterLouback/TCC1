# METEOR: An Automatic Metric for MT Evaluation with Improved Correlation with Human Judgments

Banerjee, Satanjeev; Lavie, Alon. "METEOR: An automatic metric for MT evaluation with improved correlation with human judgments," Proceedings of the ACL Workshop on Intrinsic and Extrinsic Evaluation Measures for Machine Translation and/or Summarization, pp. 65-72, 2005.

🔗 ACL Anthology: [W05-0909](https://aclanthology.org/W05-0909/)

## 1. Fichamento de Conteúdo

Este artigo apresenta METEOR (Metric for Evaluation of Translation with Explicit ORdering), uma métrica automática para avaliação de tradução automática desenvolvida para abordar deficiências percebidas no BLEU. A principal motivação é melhorar a correlação com julgamentos humanos, especialmente em nível de segmento (sentença individual). A metodologia do METEOR baseia-se em alinhamento de unigramas entre tradução candidata e referências, considerando correspondências exatas, variantes derivadas (stemming), sinônimos e paráfrases através do WordNet. Diferentemente do BLEU que enfatiza precisão, METEOR equilibra explicitamente precisão e recall através de uma média harmônica (F-measure), e inclui uma penalidade por fragmentação que favorece traduções com palavras consecutivas correspondentes. Os resultados demonstram que METEOR alcança correlação de Pearson significativamente maior (r≈0.33-0.35) com avaliações humanas no conjunto de dados TIDES 2003 comparado a outras métricas. O estudo valida que recall desempenha papel mais importante que precisão isoladamente na obtenção de alta correlação com julgamentos humanos. METEOR tornou-se amplamente utilizado na comunidade de processamento de linguagem natural e foi adaptado para diversas tarefas além de tradução automática.

## 2. Fichamento Bibliográfico

* _Unigram Matching_ (correspondência de unigramas) é o processo de alinhar palavras individuais entre tradução candidata e referências usando correspondências exatas, stemming e sinônimos do WordNet (seção 2).
* _Precision and Recall Balance_ (equilíbrio entre precisão e recall) é alcançado através do F-measure que combina ambas medidas, enfatizando recall através de um parâmetro de ponderação (seção 2.1).
* _Fragmentation Penalty_ (penalidade de fragmentação) reduz a pontuação quando correspondências entre tradução e referência ocorrem em chunks descontínuos, favorecendo ordem de palavras similar (seção 2.2).
* _Segment-Level Correlation_ (correlação em nível de segmento) mede quão bem a métrica correlaciona com julgamentos humanos para traduções individuais, não apenas agregados de corpus (objetivo).
* _WordNet Synonyms_ (sinônimos do WordNet) são utilizados para identificar correspondências semânticas entre palavras que não são idênticas textualmente, melhorando a robustez da métrica (metodologia).

## 3. Fichamento de Citações

* _"We describe METEOR, an automatic metric for machine translation evaluation that is based on a generalized concept of unigram matching between the machine-produced translation and human-produced reference translations."_
* _"Unigrams can be matched based on their surface forms, stemmed forms, and meanings; furthermore, METEOR can be easily extended to include more advanced matching strategies."_
* _"Once all generalized unigram matches between the two strings have been found, METEOR computes a score for this matching using a combination of unigram-precision, unigram-recall, and a measure of fragmentation."_
* _"METEOR gets an R correlation value of 0.347 on the Arabic data and 0.331 on the Chinese data. This is shown to be an improvement on using simply unigram-precision, unigram-recall or the (arithmetic) F1 average of precision and recall."_
* _"The basic BLEU metric... does not adequately compensate for the lack of recall through its fixed brevity penalty."_
* _"Our experimental results strongly support the claim that recall plays a more important role than precision in obtaining high levels of correlation with human judgments."_
