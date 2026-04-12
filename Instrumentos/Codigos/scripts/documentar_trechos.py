import os
import csv
import json
import time
from pathlib import Path

from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
ENTRADA = BASE_DIR / "data" / "selecionados" / "trechos.json"

SAIDA_DIR = BASE_DIR / "data" / "documentacao" / "chatgpt"
SAIDA_DIR.mkdir(parents=True, exist_ok=True)

ARQUIVO_JSON = SAIDA_DIR / "documentacoes.json"
ARQUIVO_CSV = SAIDA_DIR / "documentacoes.csv"

MODELO = "gpt-4o-mini"
TEMPERATURA = 0.0
MAX_TOKENS = 1200

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

PROMPT_FUNCAO = """Gere documentação JSDoc completa para a seguinte função JavaScript.
Inclua:
- descrição funcional detalhada;
- tipos e descrições de todos os parâmetros;
- tipo e descrição do valor de retorno;
- possíveis exceções, erros ou casos especiais, quando aplicável.

Regras:
- Retorne apenas o bloco JSDoc.
- Não explique nada fora do comentário.
- Não invente comportamento que não possa ser inferido do código.
- Use linguagem técnica clara e objetiva.
"""

PROMPT_CLASSE = """Gere documentação JSDoc completa para a seguinte classe JavaScript.
Inclua:
- descrição funcional detalhada da classe;
- documentação do construtor, quando aplicável;
- descrição dos principais parâmetros;
- comportamento relevante, retorno e casos especiais dos métodos principais, quando inferíveis;
- possíveis exceções, erros ou casos especiais, quando aplicável.

Regras:
- Retorne apenas o bloco JSDoc principal da classe.
- Não explique nada fora do comentário.
- Não invente comportamento que não possa ser inferido do código.
- Use linguagem técnica clara e objetiva.
"""

def carregar_trechos():
    return json.loads(ENTRADA.read_text(encoding="utf-8"))

def montar_prompt(item):
    cabecalho = f"""Tipo: {item['tipo']}
Repositório: {item['repo']}
Arquivo: {item['arquivo']}
Nome: {item['nome']}
Linhas: {item['linha_inicio']}-{item['linha_fim']}

Código:
```javascript
{item['codigo']}
```"""

    if item["tipo"] == "function":
        return PROMPT_FUNCAO + "\n\n" + cabecalho

    if item["tipo"] == "class":
        return PROMPT_CLASSE + "\n\n" + cabecalho

    raise ValueError(f"Tipo não suportado: {item['tipo']}")

def gerar_documentacao(prompt):
    inicio = time.perf_counter()

    resposta = client.responses.create(
        model=MODELO,
        temperature=TEMPERATURA,
        max_output_tokens=MAX_TOKENS,
        input=prompt
    )

    fim = time.perf_counter()
    duracao = round(fim - inicio, 4)

    texto = resposta.output_text.strip()

    return texto, duracao

def main():
    trechos = carregar_trechos()
    resultados = []

    for i, item in enumerate(trechos, start=1):
        prompt = montar_prompt(item)
        documentacao, tempo_geracao = gerar_documentacao(prompt)

        registro = {
            "id_trecho": item["id_trecho"],
            "repo": item["repo"],
            "arquivo": item["arquivo"],
            "tipo": item["tipo"],
            "nome": item["nome"],
            "linha_inicio": item["linha_inicio"],
            "linha_fim": item["linha_fim"],
            "loc": item["loc"],
            "ferramenta": "chatgpt",
            "modelo": MODELO,
            "temperatura": TEMPERATURA,
            "prompt": prompt,
            "tempo_geracao_segundos": tempo_geracao,
            "documentacao_gerada": documentacao
        }

        resultados.append(registro)
        print(f"[{i}/{len(trechos)}] {item['id_trecho']} - OK ({tempo_geracao}s)")

    ARQUIVO_JSON.write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    if resultados:
        campos = list(resultados[0].keys())
        with ARQUIVO_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(resultados)

    print("\nArquivos gerados:")
    print(ARQUIVO_JSON)
    print(ARQUIVO_CSV)

if __name__ == "__main__":
    main()