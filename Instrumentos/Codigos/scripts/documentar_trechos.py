import csv
import json
import os
import re
import time
from pathlib import Path

from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent.parent
ENTRADA = BASE_DIR / "data" / "selecionados" / "trechos.json"

SAIDA_DIR = BASE_DIR / "data" / "documentacao" / "gemini"
DOCS_DIR = SAIDA_DIR / "arquivos"

SAIDA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

ARQUIVO_JSON = SAIDA_DIR / "documentacoes.json"
ARQUIVO_CSV = SAIDA_DIR / "documentacoes.csv"

MODELO = "gemini-2.5-flash"
TEMPERATURA = 0.0
MAX_OUTPUT_TOKENS = 1200
TENTATIVAS = 3
PAUSA_ENTRE_TENTATIVAS = 30

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if not API_KEY:
    raise SystemExit("Defina a variável GEMINI_API_KEY antes de rodar o script.")

client = genai.Client(api_key=API_KEY)

INSTRUCAO_SISTEMA = """
Você é um especialista em documentação de código JavaScript.
Sua tarefa é gerar documentação JSDoc fiel ao código fornecido.
Não invente comportamento que não possa ser inferido do código.
Retorne apenas o bloco JSDoc, sem explicações extras fora do comentário.
Use linguagem técnica clara, objetiva e consistente.
""".strip()

PROMPT_FUNCAO = """
Gere documentação JSDoc completa para a seguinte função JavaScript.

Inclua:
- descrição funcional detalhada;
- tipos e descrições de todos os parâmetros, quando inferíveis;
- tipo e descrição do valor de retorno, quando inferível;
- possíveis exceções, erros ou casos especiais, quando aplicável.

Regras:
- Retorne apenas um bloco JSDoc.
- Se algum tipo não puder ser inferido com segurança, use uma descrição neutra sem inventar detalhes.
- Não inclua markdown fora do comentário.
""".strip()

PROMPT_CLASSE = """
Gere documentação JSDoc completa para a seguinte classe JavaScript.

Inclua:
- descrição funcional detalhada da classe;
- documentação do construtor, quando aplicável;
- descrição dos principais parâmetros, quando inferíveis;
- comportamento relevante e casos especiais, quando aplicável.

Regras:
- Retorne apenas um bloco JSDoc principal da classe.
- Se algum tipo não puder ser inferido com segurança, use uma descrição neutra sem inventar detalhes.
- Não inclua markdown fora do comentário.
""".strip()

def carregar_trechos():
    return json.loads(ENTRADA.read_text(encoding="utf-8"))

def montar_prompt(item):
    prompt_base = PROMPT_FUNCAO if item["tipo"] == "function" else PROMPT_CLASSE

    metadados = (
        f"ID do trecho: {item['id_trecho']}\n"
        f"Tipo: {item['tipo']}\n"
        f"Repositório: {item['repo']}\n"
        f"Arquivo: {item['arquivo']}\n"
        f"Nome: {item['nome']}\n"
        f"Linhas: {item['linha_inicio']}-{item['linha_fim']}\n"
    )

    codigo = f"```javascript\n{item['codigo']}\n```"

    return f"{prompt_base}\n\n{metadados}\nCódigo:\n{codigo}"

def limpar_saida(texto):
    if not texto:
        return ""

    texto = texto.strip()

    fence = re.match(r"^```(?:js|javascript)?\s*(.*?)\s*```$", texto, flags=re.S | re.I)
    if fence:
        texto = fence.group(1).strip()

    inicio = texto.find("/**")
    fim = texto.rfind("*/")

    if inicio != -1 and fim != -1 and fim > inicio:
        texto = texto[inicio:fim + 2].strip()

    return texto

def gerar_documentacao(prompt):
    ultimo_erro = None

    for tentativa in range(1, TENTATIVAS + 1):
        inicio = time.perf_counter()

        try:
            response = client.models.generate_content(
                model=MODELO,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCAO_SISTEMA,
                    temperature=TEMPERATURA,
                    max_output_tokens=MAX_OUTPUT_TOKENS,
                    candidate_count=1,
                ),
            )

            fim = time.perf_counter()
            tempo = round(fim - inicio, 4)

            texto = limpar_saida(getattr(response, "text", "") or "")
            if not texto:
                raise ValueError("Resposta vazia ou sem bloco JSDoc identificável.")

            return {
                "ok": True,
                "documentacao_gerada": texto,
                "tempo_geracao_segundos": tempo,
                "tentativa": tentativa,
                "erro": ""
            }

        except Exception as e:
            fim = time.perf_counter()
            tempo = round(fim - inicio, 4)
            ultimo_erro = {
                "ok": False,
                "documentacao_gerada": "",
                "tempo_geracao_segundos": tempo,
                "tentativa": tentativa,
                "erro": str(e)
            }
            if tentativa < TENTATIVAS:
                time.sleep(PAUSA_ENTRE_TENTATIVAS)

    return ultimo_erro

def salvar_arquivo_individual(item, documentacao):
    nome = f"{item['id_trecho']}.jsdoc.txt"
    caminho = DOCS_DIR / nome
    caminho.write_text(documentacao, encoding="utf-8")
    return nome

def main():
    trechos = carregar_trechos()
    resultados = []

    for i, item in enumerate(trechos, start=1):
        prompt = montar_prompt(item)
        geracao = gerar_documentacao(prompt)

        registro = {
            "id_trecho": item["id_trecho"],
            "repo": item["repo"],
            "arquivo": item["arquivo"],
            "tipo": item["tipo"],
            "nome": item["nome"],
            "linha_inicio": item["linha_inicio"],
            "linha_fim": item["linha_fim"],
            "loc": item["loc"],
            "ferramenta": "gemini",
            "modelo": MODELO,
            "temperatura": TEMPERATURA,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "prompt": prompt,
            "ok": geracao["ok"],
            "tentativa": geracao["tentativa"],
            "tempo_geracao_segundos": geracao["tempo_geracao_segundos"],
            "erro": geracao["erro"],
            "documentacao_gerada": geracao["documentacao_gerada"],
            "arquivo_documentacao": ""
        }

        if geracao["ok"]:
            registro["arquivo_documentacao"] = salvar_arquivo_individual(
                item, geracao["documentacao_gerada"]
            )
            print(f"[{i}/{len(trechos)}] {item['id_trecho']} OK em {geracao['tempo_geracao_segundos']}s")
        else:
            print(f"[{i}/{len(trechos)}] {item['id_trecho']} ERRO: {geracao['erro']}")

        resultados.append(registro)

    ARQUIVO_JSON.write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    if resultados:
        campos = [
            "id_trecho",
            "repo",
            "arquivo",
            "tipo",
            "nome",
            "linha_inicio",
            "linha_fim",
            "loc",
            "ferramenta",
            "modelo",
            "temperatura",
            "max_output_tokens",
            "ok",
            "tentativa",
            "tempo_geracao_segundos",
            "erro",
            "arquivo_documentacao",
            "prompt",
            "documentacao_gerada",
        ]
        with ARQUIVO_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(resultados)

    total = len(resultados)
    sucesso = sum(1 for r in resultados if r["ok"])
    falha = total - sucesso

    print("\nResumo:")
    print(f"Total: {total}")
    print(f"Sucesso: {sucesso}")
    print(f"Falha: {falha}")
    print(ARQUIVO_JSON)
    print(ARQUIVO_CSV)

if __name__ == "__main__":
    main()