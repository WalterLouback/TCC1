import csv
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPOS_DIR = DATA_DIR / "repos"
REPOS_DIR.mkdir(parents=True, exist_ok=True)

JSON_FILE = DATA_DIR / "repos.json"
CSV_FILE = DATA_DIR / "repos.csv"

def load_repos():
    if JSON_FILE.exists():
        data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
        return [
            {
                "name": item.get("name") or item["full_name"].split("/")[-1],
                "clone_url": item.get("clone_url") or f'https://github.com/{item["full_name"]}.git',
                "default_branch": item.get("default_branch", "main"),
                "full_name": item.get("full_name", "")
            }
            for item in data
        ]

    if CSV_FILE.exists():
        repos = []
        with CSV_FILE.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                full_name = row.get("full_name", "")
                clone_url = row.get("clone_url") or row.get("html_url", "").rstrip("/") + ".git"
                repos.append({
                    "name": row.get("name") or full_name.split("/")[-1],
                    "clone_url": clone_url,
                    "default_branch": row.get("default_branch", "main"),
                    "full_name": full_name
                })
        return repos

    raise FileNotFoundError(f"Nenhum repos.json ou repos.csv encontrado em data/ {BASE_DIR}")

def clone_repo(repo):
    target = REPOS_DIR / repo["name"]
    if target.exists():
        print(f"[SKIP] {repo['name']} já existe")
        return

    print(f"[CLONE] {repo['clone_url']}")
    subprocess.run(["git", "clone", "--depth", "1", repo["clone_url"], str(target)], check=True)

def main():
    repos = load_repos()
    for repo in repos:
        try:
            clone_repo(repo)
        except Exception as e:
            print(f"[ERRO] {repo['name']}: {e}")

if __name__ == "__main__":
    main()