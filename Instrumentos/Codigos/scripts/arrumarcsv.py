import pandas as pd
from pathlib import Path
# arquivo de entrada
caminho_arquivo = Path(__file__).resolve().parent.parent / "data" / "human_eval" / "avaliacao_humana.csv"
df = pd.read_csv(caminho_arquivo)

# normaliza provider
df["provider_norm"] = (
    df["provider"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({
        "gpt": "chatgpt",
        "chatgpt": "chatgpt",
        "gemni": "gemini",
        "gemini": "gemini"
    })
)

# colunas que identificam o trecho
key_cols = [
    "id_trecho",
    "repo",
    "arquivo",
    "tipo",
    "nome",
    "codigo",
    "documentacao_referencia"
]

# pivota a documentação gerada por provider
pivot = (
    df.pivot_table(
        index=key_cols,
        columns="provider_norm",
        values="documentacao_gerada",
        aggfunc="first"
    )
    .reset_index()
)

# renomeia as colunas finais
pivot = pivot.rename(columns={
    "chatgpt": "documentacao_gerada_chatgpt",
    "gemini": "documentacao_gerada_gemini"
})

# garante que as colunas existam mesmo se um provider faltar
for col in ["documentacao_gerada_chatgpt", "documentacao_gerada_gemini"]:
    if col not in pivot.columns:
        pivot[col] = ""

# organiza a ordem final
pivot = pivot[
    [
        "id_trecho",
        "repo",
        "arquivo",
        "tipo",
        "nome",
        "codigo",
        "documentacao_referencia",
        "documentacao_gerada_gemini",
        "documentacao_gerada_chatgpt",
        "clareza_1_5",
        "completude_1_5",
        "precisao_1_5",
        "utilidade_1_5",
        "comentarios"
    ]
]

pivot.to_csv("avaliacao_humana_consolidada.csv", index=False, encoding="utf-8-sig")
print("Arquivo salvo: avaliacao_humana_consolidada.csv")