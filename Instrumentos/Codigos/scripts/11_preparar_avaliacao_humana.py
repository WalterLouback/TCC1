import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
AMOSTRA = BASE / "data" / "dataset" / "amostra_selecionada.json"
GENERATED_DIR = BASE / "data" / "generated"
OUT = BASE / "data" / "human_eval" / "avaliacao_humana.csv"

OUT.parent.mkdir(parents=True, exist_ok=True)


amostra = json.loads(AMOSTRA.read_text(encoding="utf-8"))


docs_por_trecho = {}


for gen_file in GENERATED_DIR.glob("*.json"):
    provider = gen_file.stem.lower().strip()
    gerados = json.loads(gen_file.read_text(encoding="utf-8"))

    for item in gerados:
        if not item.get("ok"):
            continue

        id_trecho = item.get("id_trecho")
        if not id_trecho:
            continue

        if id_trecho not in docs_por_trecho:
            docs_por_trecho[id_trecho] = {}

        docs_por_trecho[id_trecho][provider] = item.get("documentacao_gerada", "")


providers = sorted({
    provider
    for docs in docs_por_trecho.values()
    for provider in docs.keys()
})


rows = []


for trecho in amostra:
    id_trecho = trecho["id_trecho"]

    row = {
        "id_trecho": id_trecho,
        "repo": trecho.get("repo", ""),
        "arquivo": trecho.get("arquivo", ""),
        "tipo": trecho.get("tipo", ""),
        "nome": trecho.get("nome", ""),
        "codigo": trecho.get("codigo", ""),
        "documentacao_referencia": trecho.get("documentacao_referencia", ""),
    }

    for provider in providers:
        row[f"documentacao_{provider}"] = docs_por_trecho.get(id_trecho, {}).get(provider, "")

    row.update({
        "clareza_1_5": "",
        "completude_1_5": "",
        "precisao_1_5": "",
        "utilidade_1_5": "",
        "comentarios": ""
    })

    rows.append(row)


if rows:
    fieldnames = [
        "id_trecho",
        "repo",
        "arquivo",
        "tipo",
        "nome",
        "codigo",
        "documentacao_referencia",
        *[f"documentacao_{provider}" for provider in providers],
        "clareza_1_5",
        "completude_1_5",
        "precisao_1_5",
        "utilidade_1_5",
        "comentarios",
    ]

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


print(f"avaliação humana gerada em {OUT}")
print(f"total de linhas: {len(rows)}")
print(f"providers encontrados: {', '.join(providers)}")