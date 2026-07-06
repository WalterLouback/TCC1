import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
AMOSTRA = BASE / "data" / "dataset" / "amostra_selecionada.json"
GENERATED_DIR = BASE / "data" / "generated"
METRICS_DIR = BASE / "data" / "metrics"
ESLINT_FILE = BASE / "data" / "lint" / "eslint_resumo.json"
OUT_JSON = BASE / "data" / "final" / "resultado_final.json"
OUT_CSV = BASE / "data" / "final" / "resultado_final.csv"

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

base = json.loads(AMOSTRA.read_text(encoding="utf-8"))
base_by_id = {x["id_trecho"]: x for x in base}

eslint_rows = []
if ESLINT_FILE.exists():
    eslint_rows = json.loads(ESLINT_FILE.read_text(encoding="utf-8"))

eslint_map = {(x["provider"], x["id_trecho"]): x for x in eslint_rows}

rows = []

for gen_file in GENERATED_DIR.glob("*.json"):
    provider = gen_file.stem
    gen_rows = json.loads(gen_file.read_text(encoding="utf-8"))
    metric_file = METRICS_DIR / f"{provider}.json"
    metric_rows = json.loads(metric_file.read_text(encoding="utf-8")) if metric_file.exists() else []
    metric_map = {x["id_trecho"]: x for x in metric_rows}

    for g in gen_rows:
        trecho = base_by_id.get(g["id_trecho"])
        if not trecho:
            continue

        metric = metric_map.get(g["id_trecho"], {})
        lint = eslint_map.get((provider, g["id_trecho"]), {})

        rows.append({
            "provider": provider,
            "id_trecho": g["id_trecho"],
            "repo": trecho["repo"],
            "arquivo": trecho["arquivo"],
            "tipo": trecho["tipo"],
            "nome": trecho["nome"],
            "stars": trecho["stars"],
            "loc": trecho["loc"],
            "tempo_geracao_segundos": g.get("tempo_geracao_segundos"),
            "ok_geracao": g.get("ok"),
            "bleu": metric.get("bleu"),
            "meteor": metric.get("meteor"),
            "rouge1_f": metric.get("rouge1_f"),
            "rouge2_f": metric.get("rouge2_f"),
            "rougeL_f": metric.get("rougeL_f"),
            "codebleu": metric.get("codebleu"),
            "qtd_erros_lint": lint.get("qtd_erros"),
            "qtd_warnings_lint": lint.get("qtd_warnings"),
            "qtd_total_problemas_lint": lint.get("qtd_total_problemas"),
            "conforme_jsdoc": lint.get("conforme_jsdoc"),
            "regras_violadas": lint.get("regras_violadas", "")
        })

OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

if rows:
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

print("resultado final consolidado")