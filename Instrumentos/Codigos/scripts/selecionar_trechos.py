
import csv
import json
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRECHOS_DIR = BASE_DIR / "data" / "trechos"
SAIDA_DIR = BASE_DIR / "data" / "selecionados"
CODIGOS_DIR = SAIDA_DIR / "codigos"

ARQUIVO_ENTRADA = TRECHOS_DIR / "todos_os_trechos.json"
ARQUIVO_JSON = SAIDA_DIR / "trechos.json"
ARQUIVO_CSV = SAIDA_DIR / "trechos.csv"
ARQUIVO_RESUMO = SAIDA_DIR / "resumo.json"

SAIDA_DIR.mkdir(parents=True, exist_ok=True)
CODIGOS_DIR.mkdir(parents=True, exist_ok=True)

FUNCOES_POR_REPO = 2
CLASSES_POR_REPO = 1

MODO_ESTRITO = False

LOC_MIN_FUNCAO = 5
LOC_MAX_FUNCAO = 60
LOC_MIN_CLASSE = 8
LOC_MAX_CLASSE = 120

TERMOS_BLOQUEADOS = [
    "/test/", "/tests/", "__tests__",
    "/spec/", ".spec.", ".test.",
    "/example/", "/examples/",
    "/demo/", "/demos/",
    "/fixture/", "/fixtures/",
    "/mock/", "/mocks/"
]

NOMES_RUINS = {
    "Anonymous",
    "DefaultExportFunction",
    "DefaultExportClass"
}

def carregar_trechos():
    return json.loads(ARQUIVO_ENTRADA.read_text(encoding="utf-8"))

def caminho_bloqueado(arquivo):
    arquivo = f"/{(arquivo or '').lower()}/"
    return any(t in arquivo for t in TERMOS_BLOQUEADOS)

def codigo_ok(codigo):
    if not codigo or not codigo.strip():
        return False
    linhas = [l for l in codigo.splitlines() if l.strip()]
    return len(linhas) >= 3

def id_trecho(item):
    base = "|".join([
        item["repo"],
        item["arquivo"],
        item["tipo"],
        item["nome"],
        str(item["linha_inicio"]),
        str(item["linha_fim"])
    ])
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]

def normalizar(item):
    return {
        "repo": item.get("repo"),
        "arquivo": item.get("arquivo"),
        "tipo": item.get("tipo"),
        "nome": item.get("nome") or "Anonymous",
        "linha_inicio": int(item.get("linha_inicio") or 0),
        "linha_fim": int(item.get("linha_fim") or 0),
        "loc": int(item.get("loc") or 0),
        "codigo": (item.get("codigo") or "").strip()
    }

def valido(item):
    if not item["repo"] or not item["arquivo"] or not item["tipo"]:
        return False
    if caminho_bloqueado(item["arquivo"]):
        return False
    if not codigo_ok(item["codigo"]):
        return False

    if item["tipo"] == "function":
        return LOC_MIN_FUNCAO <= item["loc"] <= LOC_MAX_FUNCAO

    if item["tipo"] == "class":
        return LOC_MIN_CLASSE <= item["loc"] <= LOC_MAX_CLASSE

    return False

def pontuar(item):
    if item["tipo"] == "function":
        alvo = 20
    else:
        alvo = 35

    nome_ruim = 1 if item["nome"] in NOMES_RUINS else 0
    distancia = abs(item["loc"] - alvo)

    return (
        nome_ruim,
        distancia,
        item["loc"],
        item["arquivo"].lower(),
        item["linha_inicio"],
        item["nome"].lower()
    )

def agrupar_por_repo(trechos):
    grupos = {}
    for item in trechos:
        grupos.setdefault(item["repo"], []).append(item)
    return grupos

def selecionar_por_tipo(itens_repo, tipo, quantidade):
    candidatos = [i for i in itens_repo if i["tipo"] == tipo and valido(i)]

    # remove duplicatas evidentes
    unicos = {}
    for item in candidatos:
        chave = (
            item["arquivo"],
            item["tipo"],
            item["nome"],
            item["linha_inicio"],
            item["linha_fim"]
        )
        unicos[chave] = item

    candidatos = list(unicos.values())
    candidatos.sort(key=pontuar)

    return candidatos[:quantidade], candidatos

def salvar_codigo(item):
    extensao = ".js"
    caminho = CODIGOS_DIR / f"{item['id_trecho']}{extensao}"
    caminho.write_text(item["codigo"], encoding="utf-8")
    return caminho.name

def main():
    brutos = carregar_trechos()
    trechos = [normalizar(i) for i in brutos]
    grupos = agrupar_por_repo(trechos)

    selecionados = []
    resumo = {
        "config": {
            "funcoes_por_repo": FUNCOES_POR_REPO,
            "classes_por_repo": CLASSES_POR_REPO,
            "modo_estrito": MODO_ESTRITO
        },
        "repositorios": {},
        "erros": []
    }

    for repo in sorted(grupos.keys()):
        itens_repo = grupos[repo]

        escolhidas_funcoes, candidatas_funcoes = selecionar_por_tipo(
            itens_repo, "function", FUNCOES_POR_REPO
        )
        escolhidas_classes, candidatas_classes = selecionar_por_tipo(
            itens_repo, "class", CLASSES_POR_REPO
        )

        resumo["repositorios"][repo] = {
            "funcoes_candidatas": len(candidatas_funcoes),
            "classes_candidatas": len(candidatas_classes),
            "funcoes_selecionadas": len(escolhidas_funcoes),
            "classes_selecionadas": len(escolhidas_classes)
        }

        if len(escolhidas_funcoes) < FUNCOES_POR_REPO:
            resumo["erros"].append(
                f"{repo}: funções insuficientes ({len(escolhidas_funcoes)}/{FUNCOES_POR_REPO})"
            )

        if len(escolhidas_classes) < CLASSES_POR_REPO:
            resumo["erros"].append(
                f"{repo}: classes insuficientes ({len(escolhidas_classes)}/{CLASSES_POR_REPO})"
            )

        for ordem, item in enumerate(escolhidas_funcoes + escolhidas_classes, start=1):
            registro = item.copy()
            registro["id_trecho"] = id_trecho(registro)
            registro["arquivo_codigo"] = salvar_codigo(registro)
            registro["ordem_no_repo"] = ordem
            selecionados.append(registro)

    if MODO_ESTRITO and resumo["erros"]:
        ARQUIVO_RESUMO.write_text(
            json.dumps(resumo, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        raise SystemExit(
            "Seleção interrompida por falta de trechos em modo estrito.\n"
            f"Veja: {ARQUIVO_RESUMO}"
        )

    selecionados.sort(key=lambda x: (x["repo"], x["tipo"], x["arquivo"], x["linha_inicio"]))

    ARQUIVO_JSON.write_text(
        json.dumps(selecionados, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    if selecionados:
        campos = [
            "id_trecho",
            "repo",
            "arquivo",
            "tipo",
            "nome",
            "linha_inicio",
            "linha_fim",
            "loc",
            "arquivo_codigo",
            "ordem_no_repo",
            "codigo"
        ]
        with ARQUIVO_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(selecionados)

    ARQUIVO_RESUMO.write_text(
        json.dumps(resumo, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Trechos selecionados: {len(selecionados)}")
    print(ARQUIVO_JSON)
    print(ARQUIVO_CSV)
    print(ARQUIVO_RESUMO)

if __name__ == "__main__":
    main()