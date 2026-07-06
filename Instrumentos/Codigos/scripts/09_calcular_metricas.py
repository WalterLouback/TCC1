import csv
import json
import re
from pathlib import Path

import nltk
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer

try:
    from codebleu import calc_codebleu
    HAS_CODEBLEU = True
except Exception:
    HAS_CODEBLEU = False

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

BASE = Path(__file__).resolve().parent.parent
AMOSTRA = BASE / "data" / "dataset" / "amostra_selecionada.json"
GENERATED_DIR = BASE / "data" / "generated"
OUT_DIR = BASE / "data" / "metrics"
OUT_DIR.mkdir(parents=True, exist_ok=True)

amostra = json.loads(AMOSTRA.read_text(encoding="utf-8"))
refs = {x["id_trecho"]: x for x in amostra}

smooth = SmoothingFunction().method1
rouge = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

def normalize(text):
    text = text or ""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"^\s*/\*\*", "", text)
    text = re.sub(r"\*/\s*$", "", text)
    lines = []
    for line in text.split("\n"):
        line = re.sub(r"^\s*\*\s?", "", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines).strip()

def compute_codebleu(ref, pred):
    if not HAS_CODEBLEU:
        return None
    try:
        res = calc_codebleu(
            references=[[ref]],
            predictions=[pred],
            lang="javascript"
        )
        return res.get("codebleu")
    except Exception:
        try:
            res = calc_codebleu(
                references=[ref],
                predictions=[pred],
                lang="javascript"
            )
            return res.get("codebleu")
        except Exception:
            return None

for gen_file in GENERATED_DIR.glob("*.json"):
    provider = gen_file.stem
    gerados = json.loads(gen_file.read_text(encoding="utf-8"))
    rows = []

    for item in gerados:
        if not item.get("ok"):
            continue

        ref_item = refs.get(item["id_trecho"])
        if not ref_item:
            continue

        ref = normalize(ref_item["documentacao_referencia"])
        pred = normalize(item["documentacao_gerada"])

        if not ref or not pred:
            continue

        bleu = sentence_bleu([ref.split()], pred.split(), smoothing_function=smooth)
        meteor = meteor_score([ref.split()], pred.split())
        rouge_scores = rouge.score(ref, pred)
        codebleu = compute_codebleu(ref, pred)

        rows.append({
            "provider": provider,
            "id_trecho": item["id_trecho"],
            "bleu": round(float(bleu), 6),
            "meteor": round(float(meteor), 6),
            "rouge1_f": round(float(rouge_scores["rouge1"].fmeasure), 6),
            "rouge2_f": round(float(rouge_scores["rouge2"].fmeasure), 6),
            "rougeL_f": round(float(rouge_scores["rougeL"].fmeasure), 6),
            "codebleu": None if codebleu is None else round(float(codebleu), 6)
        })

    out_json = OUT_DIR / f"{provider}.json"
    out_csv = OUT_DIR / f"{provider}.csv"

    out_json.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    if rows:
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"métricas geradas para {provider}")