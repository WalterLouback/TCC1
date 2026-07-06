# BLEU: A Method for Automatic Evaluation of Machine Translation

Papineni, Kishore; Roukos, Salim; Ward, Todd; Zhu, Wei-Jing. "BLEU: A method for automatic evaluation of machine translation," Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics, pp. 311-318, 2002.

🔗 DOI: [10.3115/1073083.1073135](https://doi.org/10.3115/1073083.1073135)  
🏆 **NAACL 2018 Test-of-Time Award**

## 1. Fichamento de Conteúdo

Este artigo seminal propõe o BLEU (Bilingual Evaluation Understudy), um método automático revolucionário para avaliação de tradução automática que é rápido, econômico e independente de idioma. A métrica BLEU correlaciona-se altamente com avaliações humanas e tem custo marginal mínimo por execução. A metodologia baseia-se em comparar n-gramas da tradução candidata com n-gramas de traduções de referência humanas, calculando precisão modificada para evitar pontuações inflacionadas. O método inclui uma penalidade de brevidade para evitar que traduções excessivamente curtas recebam pontuações artificialmente altas. Os autores demonstram que a correlação do BLEU com julgamentos humanos em nível de corpus é comparável à correlação entre dois avaliadores humanos independentes. O BLEU tornou-se o padrão de facto para avaliação automática em tradução automática e foi posteriormente adaptado para outras tarefas de geração de linguagem natural, incluindo resumo automático e geração de código. Os resultados validam que métricas automáticas podem servir como substitutos eficientes para juízes humanos quando há necessidade de avaliações rápidas ou frequentes, democratizando o acesso à avaliação de sistemas de tradução automática.

## 2. Fichamento Bibliográfico

* _BLEU Score_ (pontuação BLEU) é calculada como média geométrica ponderada de precisões de n-gramas modificadas, multiplicada por uma penalidade de brevidade exponencial (seção 2).
* _Modified Precision_ (precisão modificada) previne que palavras sejam contadas múltiplas vezes além de suas ocorrências nas traduções de referência, evitando pontuações inflacionadas (seção 2.1).
* _Brevity Penalty_ (penalidade de brevidade) compensa traduções candidatas que são mais curtas que suas traduções de referência efetivas, impedindo que traduções muito breves recebam pontuações altas (seção 3).
* _N-gram Precision_ (precisão de n-gramas) mede a fração de n-gramas na tradução candidata que ocorrem em alguma tradução de referência, com n tipicamente variando de 1 a 4 (metodologia).
* _Corpus-Level Correlation_ (correlação em nível de corpus) avalia o quão bem a métrica automática se alinha com julgamentos humanos agregados em múltiplas traduções (validação experimental).

## 3. Fichamento de Citações

* _"Human evaluations of machine translation are extensive but expensive. Human evaluations can take months to finish and involve human labor that can not be reused."_
* _"We propose a method of automatic machine translation evaluation that is quick, inexpensive, and language-independent, that correlates highly with human evaluation, and that has little marginal cost per run."_
* _"The closer a machine translation is to a professional human translation, the better it is."_
* _"The primary programming task for a BLEU implementor is to compare n-grams of the candidate with the n-grams of the reference translation and count the number of matches."_
* _"BLEU's correlation with human judgment has been demonstrated to be as good as the correlation between two human judges."_
* _"The BLEU metric ranges from 0 to 1. Few translations will attain a score of 1 unless they are identical to a reference translation."_
