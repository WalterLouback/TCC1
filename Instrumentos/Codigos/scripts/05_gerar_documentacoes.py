import json
import os
import re
import time
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "data" / "dataset" / "amostra_selecionada.json"
PROVIDERS = BASE / "config" / "providers.json"
OUT_DIR = BASE / "data" / "generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)

dados = json.loads(INPUT.read_text(encoding="utf-8"))
providers = json.loads(PROVIDERS.read_text(encoding="utf-8"))

SYSTEM_PROMPT = """Você é um gerador de documentação JSDoc para JavaScript.
Responda apenas com um único bloco JSDoc válido.
Não use markdown.
Não use cercas de código.
Não explique nada fora do comentário.
A documentação deve refletir apenas o que é inferível a partir do código."""

def build_prompt(item):
    return f"""Gere um bloco JSDoc completo para o trecho abaixo.

Regras:
- Retorne apenas o comentário JSDoc.
- Inclua descrição funcional objetiva.
- Inclua @param para todos os parâmetros presentes.
- Inclua @returns apenas se houver retorno observável.
- Inclua @throws somente se houver indicação clara no código.
- Não invente comportamentos não observáveis.
- Use inglês técnico simples.

Trecho:
{item["codigo"]}
"""

def sanitize_jsdoc(text):
    text = (text or "").strip()
    text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    m = re.search(r"/\*\*[\s\S]*?\*/", text)
    return m.group(0).strip() if m else text.strip()

def call_openai(provider, prompt):
    api_key = os.getenv(provider["api_key_env"], "").strip()
    if not api_key:
        raise RuntimeError(f"variável ausente: {provider['api_key_env']}")

    url = provider["base_url"].rstrip("/") + "/chat/completions"
    payload = {
        "model": provider["model"],
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]

def call_gemini(provider, prompt):
    api_key = os.getenv(provider["api_key_env"], "").strip()
    if not api_key:
        raise RuntimeError(f"variável ausente: {provider['api_key_env']}")

    model = provider["model"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT + "\n\n" + prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0
        }
    }
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def gerar(provider, item):
    prompt = build_prompt(item)
    if provider["type"] == "openai":
        return call_openai(provider, prompt)
    if provider["type"] == "gemini":
        return call_gemini(provider, prompt)
    raise ValueError(f"provider type inválido: {provider['type']}")

for provider in providers:
    out_file = OUT_DIR / f"{provider['name']}.json"
    existentes = []
    if out_file.exists():
        existentes = json.loads(out_file.read_text(encoding="utf-8"))

    feitos = {x["id_trecho"] for x in existentes}
    resultados = list(existentes)

    for i, item in enumerate(dados, start=1):
        if item["id_trecho"] in feitos:
            print(f"[{provider['name']}] skip {i}/{len(dados)} {item['id_trecho']}")
            continue

        inicio = time.time()
        ok = False
        erro = ""
        doc = ""

        for tentativa in range(1, 4):
            try:
                raw = gerar(provider, item)
                doc = sanitize_jsdoc(raw)
                ok = doc.startswith("/**") and doc.endswith("*/")
                if ok:
                    break
            except Exception as e:
                erro = str(e)
                time.sleep(2 * tentativa)

        resultados.append({
            "id_trecho": item["id_trecho"],
            "provider": provider["name"],
            "model": provider["model"],
            "ok": ok,
            "erro": erro,
            "tempo_geracao_segundos": round(time.time() - inicio, 2),
            "documentacao_gerada": doc
        })

        out_file.write_text(json.dumps(resultados, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[{provider['name']}] {i}/{len(dados)} {item['id_trecho']} ok={ok}")

print("geração finalizada")