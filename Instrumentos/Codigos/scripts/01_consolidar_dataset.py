import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

TRECHOS = BASE / "data" / "selecionados" / "trechos.json"
DOCS = BASE / "data" / "documentacao" / "gemini" / "documentacoes.json"
OUT_JSON = BASE / "data" / "dataset" / "final_documentado.json"
OUT_CSV = BASE / "data" / "dataset" / "final_documentado.csv"

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

trechos = json.loads(TRECHOS.read_text(encoding="utf-8"))
docs = json.loads(DOCS.read_text(encoding="utf-8"))

docs_por_id = {d["id_trecho"]: d for d in docs}

final = []
for t in trechos:
    d = docs_por_id.get(t["id_trecho"], {})
    final.append({
        "id_trecho": t["id_trecho"],
        "repo": t["repo"],
        "arquivo": t["arquivo"],
        "tipo": t["tipo"],
        "nome": t["nome"],
        "linha_inicio": t["linha_inicio"],
        "linha_fim": t["linha_fim"],
        "loc": t["loc"],
        "codigo": t["codigo"],
        "ferramenta": d.get("ferramenta", ""),
        "modelo": d.get("modelo", ""),
        "tempo_geracao_segundos": d.get("tempo_geracao_segundos", ""),
        "ok": d.get("ok", False),
        "erro": d.get("erro", ""),
        "documentacao_gerada": d.get("documentacao_gerada", "")
    })

OUT_JSON.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")

with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=final[0].keys())
    writer.writeheader()
    writer.writerows(final)

print(OUT_JSON)
print(OUT_CSV)