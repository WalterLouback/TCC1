import shutil
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
INPUT_ROOT = BASE / "data" / "lint" / "arquivos"
OUT_ROOT = BASE / "data" / "lint" / "results"
OUT_ROOT.mkdir(parents=True, exist_ok=True)

npx_cmd = shutil.which("npx") or shutil.which("npx.cmd")
if not npx_cmd:
    raise RuntimeError(
        "npx não encontrado no PATH. Abra um novo terminal, rode 'npm install' e teste 'npx --version'."
    )

for provider_dir in INPUT_ROOT.iterdir():
    if not provider_dir.is_dir():
        continue

    out_file = OUT_ROOT / f"{provider_dir.name}.json"

    cmd = [
        "cmd", "/c",
        npx_cmd,
        "eslint",
        str(provider_dir),
        "-f", "json",
        "-o", str(out_file)
    ]

    print(" ".join(cmd))
    result = subprocess.run(cmd, check=False, cwd=BASE)

    if result.returncode not in (0, 1):
        print(f"falha ao rodar eslint para {provider_dir.name}, retorno={result.returncode}")

print("eslint finalizado")