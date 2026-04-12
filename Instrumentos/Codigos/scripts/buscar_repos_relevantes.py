import requests
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
TOP_N = 5
MIN_STARS = 500
PUSHED_AFTER = "2024-01-01"

SEARCH_GROUPS = [
    "language:JavaScript topic:framework",
    "language:JavaScript topic:frontend",
    "language:JavaScript topic:utility",
    "language:JavaScript topic:cli",
    "language:JavaScript topic:api",
    "language:JavaScript topic:tooling",
]

BASE_URL = "https://api.github.com/search/repositories"
OUT_DIR = Path("../data")
OUT_DIR.mkdir(exist_ok=True)

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "tcc-repo-selector"
}
if GITHUB_TOKEN:
    headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

def months_since(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    return max(0.1, (now - dt).days / 30.0)

def compute_score(repo):
    stars = repo["stargazers_count"]
    forks = repo["forks_count"]
    updated_months = months_since(repo["pushed_at"])

    stars_score = math.log10(stars + 1) * 0.60
    forks_score = math.log10(forks + 1) * 0.15
    activity_score = (1 / updated_months) * 0.25

    return round(stars_score + forks_score + activity_score, 6)

def fetch_repos(query, per_page=30, page=1):
    q = f"{query} stars:>={MIN_STARS} pushed:>={PUSHED_AFTER} archived:false fork:false"
    params = {
        "q": q,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
        "page": page
    }
    r = requests.get(BASE_URL, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("items", [])

repos = {}

for group in SEARCH_GROUPS:
    for page in range(1, 3):  # 2 páginas por grupo
        items = fetch_repos(group, per_page=30, page=page)
        for repo in items:
            if repo["full_name"] not in repos:
                repos[repo["full_name"]] = {
                    "id": repo["id"],
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "html_url": repo["html_url"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "topics": repo.get("topics", []),
                    "stargazers_count": repo["stargazers_count"],
                    "forks_count": repo["forks_count"],
                    "open_issues_count": repo["open_issues_count"],
                    "created_at": repo["created_at"],
                    "updated_at": repo["updated_at"],
                    "pushed_at": repo["pushed_at"],
                    "default_branch": repo["default_branch"],
                    "license": repo["license"]["spdx_id"] if repo.get("license") else None,
                    "owner": repo["owner"]["login"],
                    "score": 0.0
                }

for repo in repos.values():
    repo["score"] = compute_score(repo)

result = sorted(
    repos.values(),
    key=lambda r: (r["score"], r["stargazers_count"], r["forks_count"]),
    reverse=True
)[:TOP_N]

json_path = OUT_DIR / "repos.json"
csv_path = OUT_DIR / "repos.csv"

json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "id", "name", "full_name", "html_url", "description", "language", "owner",
            "license", "stargazers_count", "forks_count", "open_issues_count",
            "created_at", "updated_at", "pushed_at", "default_branch", "score", "topics"
        ]
    )
    writer.writeheader()
    for row in result:
        row = row.copy()
        row["topics"] = ",".join(row["topics"])
        writer.writerow(row)

print(f"{len(result)} repositórios salvos em:")
print(json_path)
print(csv_path)