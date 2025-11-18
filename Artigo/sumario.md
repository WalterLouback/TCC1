# Avaliação Empírica da Qualidade da Documentação de Código Gerada por Ferramentas de IA

1. Walter Roberto Rodrigues Loubak

* Danilo Maia
* Leonardo Vilela
* Raphael Ramos 
* Cleiton Tavares 

## Introdução

1. A área da Engenharia de Software tratada neste trabalho é **Qualidade de Software e Documentação de Código**, com ênfase em ferramentas de Inteligência Artificial aplicadas ao nvolvimento de software.

2. O problema que este trabalho busca resolver nessa área é **a falta de avaliação empírica e sistemática sobre a qualidade da documentação de código gerada automaticamente por ferramentas de IA**, como GitHub Copilot, ChatGPT e Amazon CodeWhisperer, considerando aspectos de completude, conformidade e manutenibilidade.

3. Resolver este problema é relevante porque a documentação de código é fundamental para a manutenibilidade e compreensão de sistemas de software. Com o crescente uso de ferramentas de IA para geração automática de documentação, é necessário compreender empiricamente a qualidade do que é gerado, identificar suas limitações e estabelecer diretrizes práticas para seu uso efetivo em projetos reais de Engenharia de Software.

4. O objetivo geral deste trabalho é **investigar empiricamente a qualidade da documentação de código gerada por ferramentas de Inteligência Artificial, utilizando métricas automáticas e ferramentas de análise estática, para identificar padrões de qualidade, limitações e propor diretrizes práticas para uso dessas soluções em projetos de Engenharia de Software**.

5. Os três objetivos específicos deste trabalho são:
   - Avaliar a documentação JSDoc gerada por GitHub Copilot, ChatGPT e Amazon CodeWhisperer utilizando métricas automáticas (BLEU, ROUGE, METEOR, CodeBLEU)
   - Analisar aspectos de conformidade e manutenibilidade da documentação gerada através de ferramentas de análise estática (SonarQube e ESLint)
   - Comparar os resultados obtidos entre as diferentes ferramentas de IA e identificar padrões de qualidade, limitações e propor diretrizes práticas de uso

## Fundamentação Teórica

1. O conceito/teoria principal associado a este trabalho é **Documentação de Código em Engenharia de Software**. A sua definição neste trabalho é conforme definido nos trabalhos sobre manutenibilidade de software e práticas de documentação técnica, incluindo padrões como JSDoc para JavaScript, pelos autores e normas da IEEE e ISO/IEC 25010 sobre qualidade de software.

2. O conceito/teoria secundário associado a este trabalho é **Inteligência Artificial Generativa aplicada ao Desenvolvimento de Software**. A sua definição neste trabalho é conforme definido nos trabalhos sobre modelos de linguagem de grande escala (Large Language Models - LLMs) e suas aplicações em Code Generation e Documentation Generation, conforme apresentado por pesquisadores em conferências como ICSE, FSE e ASE.

3. O conceito/teoria terciário associado a este trabalho é **Métricas de Avaliação de Qualidade de Texto e Código**. A sua definição neste trabalho é conforme definido nos trabalhos sobre métricas automáticas para avaliação de tradução automática (BLEU, ROUGE, METEOR) adaptadas para o contexto de código, e métricas específicas como CodeBLEU, conforme apresentado em trabalhos de avaliação de geração automática de código e documentação.

## Trabalhos Relacionados

1. O trabalho mais relacionado é o estudo sobre avaliação de ferramentas de IA para geração de código e documentação, publicado recentemente em conferências como ICSE e FSE, porque investiga diretamente a qualidade de artefatos gerados por ferramentas de IA generativa no contexto de nvolvimento de software, utilizando métricas quantitativas e análise qualitativa.

2. O segundo trabalho mais relacionado é a pesquisa sobre métricas de qualidade de documentação de software, publicada em journals como IEEE Transactions on Software Engineering, porque estabelece fundamentos teóricos e metodológicos para avaliação sistemática de documentação de código, incluindo aspectos de completude, clareza e conformidade.

3. O terceiro trabalho mais relacionado é o estudo sobre ferramentas de análise estática para verificação de qualidade de código e documentação, publicado em conferências de Engenharia de Software, porque apresenta abordagens práticas e automatizadas para avaliar aspectos técnicos da documentação, como conformidade com padrões e detecção de problemas de manutenibilidade.

## Materiais e Métodos

1. O tipo de pesquisa adotado neste trabalho é **Pesquisa Experimental e Quantitativa**, porque busca mensurar e comparar empiricamente a qualidade da documentação gerada por diferentes ferramentas de IA utilizando métricas objetivas, além de realizar experimentos controlados para avaliar o mpenho das ferramentas em condições padronizadas.

2. Os materiais utilizados neste trabalho são:
   - Base de código JavaScript composta por funções e classes extraídas de repositórios públicos do GitHub
   - Ferramentas de IA: GitHub Copilot, ChatGPT e Amazon CodeWhisperer
   - Ferramentas de análise estática: SonarQube e ESLint
   - Software para cálculo de métricas: implementações de BLEU, ROUGE, METEOR e CodeBLEU
   - Documentação manual de referência (ground truth)
   - Ambiente computacional para execução dos experimentos

3. Os métodos empregados neste trabalho são:
   - Método de amostragem intencional para seleção de trechos de código representativos
   - Método de geração padronizada de prompts para obter documentação das ferramentas de IA
   - Método de análise comparativa entre documentação gerada e documentação de referência
   - Método de análise estatística para comparação de mpenho entre as ferramentas

4. As métricas de avaliação são:
   - **BLEU** (Bilingual Evaluation Understudy): avalia similaridade com base em n-gramas
   - **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation): avalia recall e precisão
   - **METEOR** (Metric for Evaluation of Translation with Explicit ORdering): considera sinônimos e stemming
   - **CodeBLEU**: métrica específica para código que considera sintaxe e semântica
   - Métricas de análise estática do SonarQube: complexidade, duplicação, conformidade
   - Métricas do ESLint: conformidade com padrões de documentação JSDoc

5. As etapas de execução do trabalho são:
   - Etapa 1: Seleção e preparação da base de código JavaScript
   - Etapa 2: Geração de documentação usando GitHub Copilot, ChatGPT e Amazon CodeWhisperer com prompts padronizados
   - Etapa3: Avaliação automática usando métricas BLEU, ROUGE, METEOR e CodeBLEU
   - Etapa 4: Análise estática usando SonarQube e ESLint
   - Etapa 5: Comparação e análise estatística dos resultados
