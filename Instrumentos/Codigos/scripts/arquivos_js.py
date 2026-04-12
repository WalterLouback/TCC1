import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOS_DIR = BASE_DIR / "data" / "repos"
OUT_DIR = BASE_DIR / "data" / "inventory"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VALID_EXTENSIONS = {".js", ".jsx", ".mjs", ".cjs"}
IGNORE_DIRS = {
    "node_modules", ".git", "dist", "build", "coverage",
    ".next", ".nuxt", "vendor", "tmp", "temp"
}
IGNORE_FILE_SUFFIXES = {".min.js"}

def should_ignore(path: Path):
    parts = set(path.parts)
    if parts & IGNORE_DIRS:
        return True
    for suffix in IGNORE_FILE_SUFFIXES:
        if path.name.endswith(suffix):
            return True
    return False

def collect_repo_files(repo_dir: Path):
    items = []
    for file in repo_dir.rglob("*"):
        if not file.is_file():
            continue
        if should_ignore(file):
            continue
        if file.suffix.lower() not in VALID_EXTENSIONS:
            continue

        try:
            rel = file.relative_to(repo_dir).as_posix()
            size = file.stat().st_size
            items.append({
                "repo": repo_dir.name,
                "path": rel,
                "size_bytes": size
            })
        except Exception:
            pass
    return items

def main():
    all_items = []
    for repo_dir in REPOS_DIR.iterdir():
        if repo_dir.is_dir():
            files = collect_repo_files(repo_dir)
            all_items.extend(files)
            out_file = OUT_DIR / f"{repo_dir.name}_files.json"
            out_file.write_text(json.dumps(files, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"[OK] {repo_dir.name}: {len(files)} arquivos")

    summary_file = OUT_DIR / "all_js_files.json"
    summary_file.write_text(json.dumps(all_items, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[TOTAL] {len(all_items)} arquivos inventariados")

if __name__ == "__main__":
    main()