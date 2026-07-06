import json
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
IN_FILE = BASE / "data" / "repos" / "repos_encontrados.json"
OUT_DIR = BASE / "data" / "repos" / "clones"
OUT_DIR.mkdir(parents=True, exist_ok=True)

repos = json.loads(IN_FILE.read_text(encoding="utf-8"))

for repo in repos:
    target = OUT_DIR / repo["full_name"].replace("/", "__")
    if target.exists():
        print(f"[skip] {repo['full_name']}")
        continue

    cmd = ["git", "clone", "--depth", "1", repo["clone_url"], str(target)]
    print(" ".join(cmd))
    subprocess.run(cmd, check=False)

print("clone finalizado")