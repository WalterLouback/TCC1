import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
AMOSTRA = BASE / "data" / "dataset" / "amostra_selecionada.json"
GENERATED_DIR = BASE / "data" / "generated"
OUT_ROOT = BASE / "data" / "lint" / "arquivos"
MAP_ROOT = BASE / "data" / "lint" / "mapas"

OUT_ROOT.mkdir(parents=True, exist_ok=True)
MAP_ROOT.mkdir(parents=True, exist_ok=True)

amostra = json.loads(AMOSTRA.read_text(encoding="utf-8"))
por_id = {x["id_trecho"]: x for x in amostra}

def short_name(provider: str, id_trecho: str) -> str:
    digest = hashlib.sha1(f"{provider}|{id_trecho}".encode("utf-8")).hexdigest()
    return f"{digest[:20]}.js"

for gen_file in GENERATED_DIR.glob("*.json"):
    provider = gen_file.stem
    itens = json.loads(gen_file.read_text(encoding="utf-8"))
    out_dir = OUT_ROOT / provider
    out_dir.mkdir(parents=True, exist_ok=True)

    mapa = []

    for item in itens:
        if not item.get("ok"):
            continue

        base = por_id.get(item["id_trecho"])
        if not base:
            continue

        file_name = short_name(provider, item["id_trecho"])
        content = f"{item['documentacao_gerada']}\n{base['codigo']}\n"

        file_path = out_dir / file_name
        file_path.write_text(content, encoding="utf-8")

        mapa.append({
            "provider": provider,
            "id_trecho": item["id_trecho"],
            "arquivo_lint": file_name
        })

    (MAP_ROOT / f"{provider}.json").write_text(
        json.dumps(mapa, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

print("arquivos para lint gerados")