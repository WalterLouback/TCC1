import json
import os
import time
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "data" / "repos" / "repos_encontrados.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "tcc-jsdoc-pipeline"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

MAX_REPOS = 10
PER_PAGE = 100
MIN_STARS = 1000
PUSHED_AFTER = "2023-01-01"
CREATED_BEFORE = "2022-11-30"
EXCLUDE_TERMS = {"ai", "gpt", "llm", "copilot", "codewhisperer", "chatgpt"}

QUERY = (
    f"language:JavaScript stars:>={MIN_STARS} pushed:>={PUSHED_AFTER} "
    f"fork:false archived:false"
)

def safe_text(v):
    return (v or "").strip()

def looks_unwanted(repo):
    hay = " ".join([
        safe_text(repo.get("name")),
        safe_text(repo.get("description")),
        " ".join(repo.get("topics", []) or [])
    ]).lower()
    return any(term in hay for term in EXCLUDE_TERMS)

def created_old_enough(repo):
    created_at = safe_text(repo.get("created_at"))
    return bool(created_at and created_at[:10] < CREATED_BEFORE)

def search_page(page):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": QUERY,
        "sort": "stars",
        "order": "desc",
        "per_page": PER_PAGE,
        "page": page
    }
    r = requests.get(url, headers=HEADERS, params=params, timeout=60)
    r.raise_for_status()
    return r.json()

repos = []
seen = set()

for page in range(1, 11):
    payload = search_page(page)
    items = payload.get("items", [])
    if not items:
        break

    for item in items:
        full_name = item["full_name"]
        if full_name in seen:
            continue
        if looks_unwanted(item):
            continue
        if not created_old_enough(item):
            continue

        seen.add(full_name)
        repos.append({
            "id": item["id"],
            "full_name": full_name,
            "clone_url": item["clone_url"],
            "html_url": item["html_url"],
            "default_branch": item["default_branch"],
            "stargazers_count": item["stargazers_count"],
            "forks_count": item["forks_count"],
            "open_issues_count": item["open_issues_count"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "pushed_at": item["pushed_at"],
            "description": item.get("description"),
            "topics": item.get("topics", []),
            "language": item.get("language"),
            "license": (item.get("license") or {}).get("spdx_id")
        })

        if len(repos) >= MAX_REPOS:
            break

    if len(repos) >= MAX_REPOS:
        break

    time.sleep(1)

OUT.write_text(json.dumps(repos, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"{len(repos)} repositórios salvos em {OUT}")