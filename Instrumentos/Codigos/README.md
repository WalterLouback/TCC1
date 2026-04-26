# TCC1 – Pipeline de Avaliação de Documentação JSDoc gerada por IA

## Pré-requisitos
- Python 3.10+
- Node.js 18+ com npm
- Token do GitHub com permissão de leitura pública
- Chave da API OpenAI (ChatGPT)

## Instalação

```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('wordnet'); nltk.download('punkt'); nltk.download('punkt_tab')"
npm install
```

Copie `.env.example` para `.env` e preencha os valores.

## Execução (em ordem)

```bash
python scripts/01_buscar_repositorios.py
python scripts/02_extrair_trechos.py
python scripts/03_gerar_documentacao_ia.py
python scripts/04_calcular_metricas.py
node scripts/05_lint_jsdoc.js
python scripts/06_consolidar_resultados.py
```

## Estrutura dos dados gerados

```
data/
  repos/              # lista de repositórios selecionados
  trechos/            # trechos extraídos com JSDoc original
  documentacao_ia/    # documentação gerada por IA por ferramenta
  metricas/           # resultados das métricas textuais
  lint/               # resultados do ESLint/JSDoc
  resultados/         # consolidado final em CSV
```
