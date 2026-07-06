import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

XLSX = "/home/walter/workfolder/TCC1/Respostas - Avaliação cega de documentação de código_10avaliadores (1).xlsx"
OUT_PDF = "/home/walter/workfolder/TCC1/fig_avaliacao_humana_medias.pdf"

wb = openpyxl.load_workbook(XLSX)
ws = wb["Form Responses 1"]

metrics = ["Clareza", "Completude", "Precisão", "Utilidade"]
metric_keys = ["clareza", "completude", "precisao", "utilidade"]
docs = ["A", "B", "C"]

doc_labels = {"A": "Referência", "B": "Gemini", "C": "ChatGPT"}
trecho_names = [
    "mergeExtraSegments",
    "makeSegments",
    "fillEncodeFence",
    "decodeFence",
    "calcStats",
    "generateBlocks",
    "createMetadataExtractor",
    "createAttributes",
    "assertBufferSource",
    "finalizeEsmResolution",
]

data = {t: {d: {m: [] for m in metric_keys} for d in docs} for t in range(1, 11)}

for row_idx in range(3, 13):
    row = [cell.value for cell in ws[row_idx]]
    for t in range(1, 11):
        if t <= 9:
            start = 1 + (t - 1) * 16
        else:
            start = 146
        for d_idx, d in enumerate(docs):
            for m_idx, m in enumerate(metric_keys):
                col = start + d_idx * 5 + m_idx
                val = row[col]
                if val is not None and isinstance(val, (int, float)):
                    data[t][d][m].append(float(val))

fig, axes = plt.subplots(2, 5, figsize=(22, 10))
fig.suptitle("Avaliação Humana — Médias por Trecho (10 avaliadores)", fontsize=16, fontweight="bold")

x = np.arange(len(metrics))
width = 0.25
colors = {"A": "#2ecc71", "B": "#3498db", "C": "#e74c3c"}

for idx, t in enumerate(range(1, 11)):
    ax = axes[idx // 5][idx % 5]
    for d_idx, d in enumerate(docs):
        means = [np.mean(data[t][d][m]) if data[t][d][m] else 0 for m in metric_keys]
        ax.bar(x + d_idx * width, means, width, label=doc_labels[d] if idx == 0 else "", color=colors[d], edgecolor="black", linewidth=0.5)
    ax.set_title(f"T{t}: {trecho_names[t-1]}", fontsize=9)
    ax.set_xticks(x + width)
    ax.set_xticklabels(metrics, fontsize=7, rotation=30, ha="right")
    ax.set_ylim(0, 5.5)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.grid(axis="y", alpha=0.3)

handles = [plt.Rectangle((0, 0), 1, 1, color=colors[d], ec="black", lw=0.5) for d in docs]
fig.legend(handles, [doc_labels[d] for d in docs], loc="lower center", ncol=3, fontsize=12, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.savefig(OUT_PDF, bbox_inches="tight", dpi=150)
print(f"Figura salva em {OUT_PDF}")

overall = {}
for d in docs:
    overall[d] = {}
    for m in metric_keys:
        all_vals = []
        for t in range(1, 11):
            all_vals.extend(data[t][d][m])
        overall[d][m] = np.mean(all_vals) if all_vals else 0
        print(f"{doc_labels[d]}_{m}: {overall[d][m]:.2f}")