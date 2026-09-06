"""Generate index.json for the Lynx-Skill repository.

Scans skills/ for single-file skills (.py / .js / .sh / .ps1 / .yaml) and
directory skills (<dir>/manifest.yaml), extracts metadata, and produces
index.json. Run by GitHub Actions on every push to main, or locally with:

    python tools/generate_index.py

Output format consumed by the Lynx client skill market (GitHubMarketAdapter):

    {
      "version": "1",
      "updated_at": "<ISO 8601 UTC>",
      "skills": [
        {
          "skill_id": "...",
          "name": "...",
          "author": "...",
          "language": "python",
          "form": "single|dir",
          "trigger": "selection",
          "permission": ["read_file"],
          "category": "...",
          "description": "...",
          "official": false,
          "license": "MIT",
          "download_url": "skills/my_skill.py"
        }
      ]
    }
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OFFICIAL_AUTHORS = ("lynx",)
INDEX_VERSION = "1"
SINGLE_FILE_EXTS = (".py", ".js", ".sh", ".ps1", ".yaml", ".yml")
LANG_BY_EXT = {".py": "python", ".js": "javascript", ".sh": "bash", ".ps1": "powershell",
               ".yaml": "yaml", ".yml": "yaml"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _extract_fields(text: str) -> dict[str, Any]:
    """Extract key="value" fields from a @skill(...) decorator or @lynx-skill header."""
    fields: dict[str, Any] = {}
    for key in ("id", "name", "description", "trigger", "category", "author", "license"):
        m = re.search(rf'\b{key}\s*=\s*"([^"]*)"', text) or re.search(
            rf'\b{key}\s*=\s*\'([^\']*)\'', text)
        if m:
            fields[key] = m.group(1)
    # permission 可能是列表 permission=["a","b"] 或单值 permission="read_file"
    m = re.search(r'permission\s*=\s*\[([^\]]*)\]', text)
    if m:
        fields["permission"] = re.findall(r'"([^"]*)"|\'([^\']*)\'', m.group(1))
        fields["permission"] = [a or b for a, b in fields["permission"]]
    else:
        m = re.search(r'permission\s*=\s*"([^"]*)"', text)
        if m:
            fields["permission"] = [p.strip() for p in m.group(1).split(",") if p.strip()]
    m = re.search(r'dangerous\s*=\s*True', text)
    if m:
        fields["dangerous"] = True
    return fields


def _entry(skill_id: str, meta: dict[str, Any], form: str, language: str,
           download_url: str) -> dict[str, Any] | None:
    if not skill_id:
        print(f"  ! SKIP {download_url}: missing skill id", file=sys.stderr)
        return None
    author = str(meta.get("author", "") or "").strip()
    return {
        "skill_id": skill_id,
        "name": meta.get("name", skill_id),
        "author": author,
        "language": language,
        "form": form,
        "trigger": meta.get("trigger", "selection"),
        "permission": meta.get("permission", ["read_file"]),
        "category": meta.get("category", ""),
        "description": meta.get("description", ""),
        "official": author.lower() in OFFICIAL_AUTHORS if author else False,
        "license": meta.get("license", "MIT"),
        "download_url": download_url,
    }


def extract_single_file(path: Path) -> dict[str, Any] | None:
    """Parse a single-file skill and return its index entry, or None on failure."""
    ext = path.suffix.lower()
    language = LANG_BY_EXT[ext]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"  ! ERROR reading {path}: {e}", file=sys.stderr)
        return None

    if ext == ".yaml" or ext == ".yml":
        try:
            import yaml

            data = yaml.safe_load(text) or {}
        except Exception as e:  # noqa: BLE001
            print(f"  ! SKIP {path.name}: YAML parse error: {e}", file=sys.stderr)
            return None
        if isinstance(data, list):  # v1 模板：文件顶层是技能条目列表
            data = data[0] if data and isinstance(data[0], dict) else {}
        if not isinstance(data, dict):
            return None
        meta = data
        skill_id = str(meta.get("id", "")).strip()
    elif ext == ".py":
        meta = _extract_fields(text)
        skill_id = str(meta.get("id", "")).strip()
    else:
        # js / sh / ps1：文件头注释 # @lynx-skill id="..." ...
        header = "\n".join(text.splitlines()[:30])
        meta = _extract_fields(header)
        skill_id = str(meta.get("id", "")).strip()

    return _entry(skill_id, meta, "single", language, f"skills/{path.name}")


def extract_dir_skill(d: Path) -> dict[str, Any] | None:
    """Parse a directory skill (manifest.yaml) and return its index entry."""
    mf_path = d / "manifest.yaml"
    try:
        import yaml

        meta = yaml.safe_load(mf_path.read_text(encoding="utf-8")) or {}
    except Exception as e:  # noqa: BLE001
        print(f"  ! SKIP {d.name}: manifest parse error: {e}", file=sys.stderr)
        return None
    if not isinstance(meta, dict):
        return None
    entry = _entry(str(meta.get("id", "")).strip(), meta, "dir",
                   str(meta.get("language", "")), f"skills/{d.name}/")
    if entry and (d / "manifest.yaml").exists():
        entry["download_url"] = f"skills/{d.name}/manifest.yaml"  # 目录技能从 manifest 入口拉取
    return entry


def generate_index(repo_root: Path) -> dict[str, Any]:
    """Scan <repo_root>/skills/ and build the index structure."""
    skills_dir = repo_root / "skills"
    entries: list[dict[str, Any]] = []

    if skills_dir.exists():
        for p in sorted(skills_dir.iterdir()):
            if p.name.startswith("_"):
                continue  # 跳过草稿目录（skills/_drafts/ 等）
            if p.is_dir():
                if (p / "manifest.yaml").is_file():
                    print(f"  + {p.name}/manifest.yaml")
                    entry = extract_dir_skill(p)
                    if entry:
                        entries.append(entry)
            elif p.suffix.lower() in SINGLE_FILE_EXTS:
                print(f"  + {p.name}")
                entry = extract_single_file(p)
                if entry:
                    entries.append(entry)
    else:
        print(f"  ! skills/ directory not found at {skills_dir}", file=sys.stderr)

    return {
        "version": INDEX_VERSION,
        "updated_at": _now_iso(),
        "skills": entries,
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    print(f"Scanning {repo_root / 'skills'} ...")
    index = generate_index(repo_root)
    out_path = repo_root / "index.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {out_path}")
    print(f"  skills indexed: {len(index['skills'])}")
    print(f"  updated_at: {index['updated_at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
