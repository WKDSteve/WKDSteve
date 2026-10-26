"""Collect the numbers the profile shows into data/family.json.

Needs `gh` (logged in) and the sibling checkouts under REPOS_DIR (default: the parent folder).
Only public repositories are listed; private ones are counted nowhere.

    python scripts/update_data.py
"""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOS = Path(os.environ.get("REPOS_DIR", ROOT.parent))
OWNER = "WKDSteve"

# Where a plugin is shown. The wkd site has its own registry; these are the public ones of it
# plus the few it does not list yet.
CATEGORY = {
    "ai": ["ai.nvim", "buffer-ctx.nvim"],
    "edit": ["cascade.nvim", "replacer.nvim", "emojis.nvim", "language.nvim", "markdown.nvim", "data.nvim", "migrate.nvim"],
    "navigate": ["gopath.nvim", "hover.nvim", "open.nvim", "pickers.nvim", "filetree.nvim", "fileops.nvim", "sessions.nvim", "neotree-fs-refactor.nvim"],
    "inspect": ["dap.nvim", "debugging.nvim", "diff.nvim", "lsp.nvim", "insights.nvim", "runtime-analysis.nvim", "recommender.nvim", "spotlight.nvim", "cmdlog.nvim", "testing.nvim"],
    "project": ["sandbox.nvim", "github_stats.nvim", "reposcope.nvim", "docmap.nvim", "gitsuite.nvim", "terminal.nvim"],
    "view": ["ui.nvim", "color_my_ascii.nvim", "images.nvim", "mdview.nvim", "media.nvim", "pdfport.nvim"],
    "foundation": ["lib.nvim"],
}
NATIVE = ["docmap-desktop", "ai-desktop", "takt"]
LABEL = {"ai": "AI & context", "edit": "Editing", "navigate": "Files & navigation", "inspect": "Debug & inspect",
         "project": "Project & repos", "view": "View & render", "foundation": "Foundation"}


def sh(*args, cwd=None):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd, encoding="utf-8", errors="replace")
    return r.stdout.strip() if r.returncode == 0 else ""


def loc(folder: Path, suffixes):
    n = 0
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix in suffixes and not any(x in p.parts for x in ("node_modules", "target", ".git", "dist")):
            try:
                n += sum(1 for _ in p.open("rb"))
            except OSError:
                pass
    return n


def main():
    listing = json.loads(sh("gh", "repo", "list", OWNER, "--limit", "200", "--visibility", "public",
                            "--json", "name,description,stargazerCount,primaryLanguage,pushedAt"))
    meta = {r["name"]: r for r in listing}
    out = {"owner": OWNER, "categories": [], "native": [], "totals": {}}
    totals = dict(plugins=0, commits=0, lua_lines=0, spec_files=0, stars=0)
    for key, names in CATEGORY.items():
        items = []
        for name in names:
            if name not in meta:
                print("skip (not public):", name, file=sys.stderr)
                continue
            repo = REPOS / name
            commits = int(sh("git", "rev-list", "--count", "HEAD", cwd=repo) or 0) if repo.exists() else 0
            lua = loc(repo / "lua", {".lua"}) if repo.exists() else 0
            specs = sum(1 for _ in (repo / "TESTS").rglob("*_spec.lua")) if (repo / "TESTS").exists() else 0
            m = meta[name]
            items.append({"name": name, "description": (m.get("description") or "").strip(), "stars": m["stargazerCount"],
                          "commits": commits, "lua_lines": lua, "specs": specs})
            totals["plugins"] += 1
            totals["commits"] += commits
            totals["lua_lines"] += lua
            totals["spec_files"] += specs
            totals["stars"] += m["stargazerCount"]
        out["categories"].append({"key": key, "label": LABEL[key], "plugins": items})
    for name in NATIVE:
        m = meta.get(name)
        repo = REPOS / name
        if not m:
            print("skip (not public):", name, file=sys.stderr)
            continue
        commits = int(sh("git", "rev-list", "--count", "HEAD", cwd=repo) or 0) if repo.exists() else 0
        lang = (m.get("primaryLanguage") or {}).get("name", "")
        out["native"].append({"name": name, "description": (m.get("description") or "").strip(), "language": lang,
                              "stars": m["stargazerCount"], "commits": commits})
        totals["commits"] += commits
    out["totals"] = totals
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "family.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(totals))


if __name__ == "__main__":
    main()
