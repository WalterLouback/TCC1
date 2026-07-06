import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
IN_FILE = BASE / "data" / "dataset" / "trechos_com_referencia.json"
OUT_JSON = BASE / "data" / "dataset" / "amostra_selecionada.json"
OUT_CSV = BASE / "data" / "dataset" / "amostra_selecionada.csv"

TARGET_FUNCTIONS = 10
TARGET_CLASSES = 5
MAX_PER_REPO = 2

dados = json.loads(IN_FILE.read_text(encoding="utf-8"))

def jsdoc_score(doc):
    score = 0
    if "@param" in doc:
        score += 2
    if "@returns" in doc or "@return" in doc:
        score += 2
    if "@throws" in doc:
        score += 1
    score += min(doc.count("\n"), 8)
    return score

for item in dados:
    item["_score"] = (
        item["stars"] * 1000
        + jsdoc_score(item["documentacao_referencia"]) * 100
        - abs(item["loc"] - 20)
    )

functions = sorted(
    [d for d in dados if d["tipo"] == "function"],
    key=lambda x: x["_score"],
    reverse=True
)

classes = sorted(
    [d for d in dados if d["tipo"] == "class"],
    key=lambda x: x["_score"],
    reverse=True
)

selecionados = []
por_repo = defaultdict(int)

def pick(items, target):
    picked = []
    for item in items:
        if por_repo[item["repo"]] >= MAX_PER_REPO:
            continue
        picked.append(item)
        por_repo[item["repo"]] += 1
        if len(picked) >= target:
            break
    return picked

selecionados.extend(pick(functions, TARGET_FUNCTIONS))
selecionados.extend(pick(classes, TARGET_CLASSES))

for item in selecionados:
    item.pop("_score", None)

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(selecionados, indent=2, ensure_ascii=False), encoding="utf-8")

with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=selecionados[0].keys())
    writer.writeheader()
    writer.writerows(selecionados)

print(f"{len(selecionados)} itens salvos em {OUT_JSON}")