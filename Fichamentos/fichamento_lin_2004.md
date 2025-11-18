# ROUGE: A Package for Automatic Evaluation of Summaries

Lin, Chin-Yew. "ROUGE: A package for automatic evaluation of summaries," Text Summarization Branches Out: Proceedings of the ACL-04 Workshop, pp. 74-81, 2004.

🔗 ACL Anthology: [W04-1013](https://aclanthology.org/W04-1013/)

## 1. Fichamento de Conteúdo

Este artigo apresenta o ROUGE (Recall-Oriented Understudy for Gisting Evaluation), um pacote abrangente de medidas automáticas para avaliar qualidade de resumos comparando-os com resumos ideais criados por humanos. A metodologia conta o número de unidades sobrepostas, como n-gramas, sequências de palavras e pares de palavras entre o resumo gerado automaticamente e os resumos de referência humanos. O trabalho introduz quatro diferentes medidas ROUGE: ROUGE-N (baseada em n-gramas), ROUGE-L (baseada na maior subsequência comum), ROUGE-W (LCS ponderada) e ROUGE-S (estatísticas de skip-bigram). Cada medida captura diferentes aspectos da qualidade do resumo. Os resultados demonstram alta correlação com julgamentos humanos, com ROUGE-1, ROUGE-L e ROUGE-SU4 mostrando desempenho particularmente forte. O estudo valida o pacote ROUGE usando dados das conferências DUC (Document Understanding Conference) 2001, 2002 e 2003, demonstrando que as medidas automáticas podem reproduzir rankings humanos de forma confiável. O ROUGE tornou-se amplamente adotado na comunidade de pesquisa em sumarização e posteriormente foi adaptado para avaliação de geração de código e documentação.

## 2. Fichamento Bibliográfico

* _ROUGE-N_ é uma medida baseada em sobreposição de n-gramas entre resumos candidatos e de referência, sendo ROUGE-1 (unigramas) e ROUGE-2 (bigramas) as mais comumente usadas (seção 2).
* _ROUGE-L_ baseia-se na maior subsequência comum (Longest Common Subsequence - LCS) entre resumos, capturando estrutura de nível de sentença de forma natural (seção 3).
* _ROUGE-W_ é uma versão ponderada do LCS que favorece correspondências consecutivas, diferenciando LCSes de diferentes relações espaciais (seção 4).
* _ROUGE-S_ utiliza estatísticas de skip-bigram, permitindo lacunas arbitrárias entre palavras e capturando padrões de palavras não consecutivas (seção 5).
* _Recall-Oriented Metrics_ (métricas orientadas a recall) priorizam a cobertura de conteúdo importante dos resumos de referência, diferentemente de métricas como BLEU que enfatizam precisão (filosofia de design).

## 3. Fichamento de Citações

* _"ROUGE stands for Recall-Oriented Understudy for Gisting Evaluation. It includes measures to automatically determine the quality of a summary by comparing it to other (ideal) summaries created by humans."_
* _"The measures count the number of overlapping units such as n-gram, word sequences, and word pairs between the computer-generated summary to be evaluated and the ideal summaries created by humans."_
* _"Following the successful application of automatic evaluation methods, such as BLEU, in machine translation evaluation, Lin and Hovy (2003) showed that methods similar to BLEU could be applied to evaluate summaries."_
* _"ROUGE-1, ROUGE-L, ROUGE-SU4 and 9, and ROUGE-W were very good measures, with Pearson's correlation coefficient above 0.95 with human judgments."_
* _"By only awarding credit to in-sequence unigram matches, ROUGE-L also captures sentence level structure in a natural way."_
* _"Using multiple references significantly improves correlation with human judgments for all ROUGE variants."_
