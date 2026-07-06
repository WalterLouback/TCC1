import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
IN_ROOT = BASE / "data" / "lint" / "results"
MAP_ROOT = BASE / "data" / "lint" / "mapas"
OUT_JSON = BASE / "data" / "lint" / "eslint_resumo.json"
OUT_CSV = BASE / "data" / "lint" / "eslint_resumo.csv"

resumo = []

for file in IN_ROOT.glob("*.json"):
    provider = file.stem
    dados = json.loads(file.read_text(encoding="utf-8"))

    mapa_file = MAP_ROOT / f"{provider}.json"
    mapa_rows = json.loads(mapa_file.read_text(encoding="utf-8")) if mapa_file.exists() else []
    mapa = {x["arquivo_lint"]: x["id_trecho"] for x in mapa_rows}

    for item in dados:
        lint_name = Path(item["filePath"]).name
        trecho_id = mapa.get(lint_name, "")

        mensagens = item.get("messages", [])
        regras = Counter([m["ruleId"] for m in mensagens if m.get("ruleId")])

        resumo.append({
            "provider": provider,
            "id_trecho": trecho_id,
            "arquivo_lint": lint_name,
            "qtd_erros": sum(1 for m in mensagens if m.get("severity") == 2),
            "qtd_warnings": sum(1 for m in mensagens if m.get("severity") == 1),
            "qtd_total_problemas": len(mensagens),
            "conforme_jsdoc": 1 if len(mensagens) == 0 else 0,
            "regras_violadas": "; ".join(f"{k}:{v}" for k, v in sorted(regras.items()))
        })

OUT_JSON.write_text(json.dumps(resumo, indent=2, ensure_ascii=False), encoding="utf-8")

if resumo:
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=resumo[0].keys())
        writer.writeheader()
        writer.writerows(resumo)

print("resumo eslint gerado")