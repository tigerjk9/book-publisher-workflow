#!/usr/bin/env python3
"""Create a portable book publishing project without external dependencies."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--title", default="Working title")
    parser.add_argument("--language", default="en")
    args = parser.parse_args()

    root = args.project_dir.resolve()
    if root.exists() and not root.is_dir():
        parser.error(f"target exists and is not a directory; no files were changed: {root}")
    if root.exists() and any(root.iterdir()):
        parser.error(f"target directory is not empty; no files were changed: {root}")

    target_files = (
        root / "book-project.json",
        root / "brief.md",
        root / "plan" / "chapter-brief-template.md",
        root / "research" / "sources.md",
        root / "qa" / "open-issues.md",
    )
    conflicts = [path for path in target_files if path.exists()]
    if conflicts:
        joined = ", ".join(str(path) for path in conflicts)
        parser.error(f"target files already exist; no files were changed: {joined}")

    for relative in (
        "manuscript",
        "research",
        "plan/chapters",
        "qa",
        "assets",
        "dist",
    ):
        (root / relative).mkdir(parents=True, exist_ok=True)

    shutil.copyfile(TEMPLATE_DIR / "brief.md", root / "brief.md")
    shutil.copyfile(TEMPLATE_DIR / "chapter-brief.md", root / "plan" / "chapter-brief-template.md")
    (root / "research" / "sources.md").write_text(
        "# Source ledger\n\nRecord source, claim, access date, and license or usage note.\n",
        encoding="utf-8",
    )
    (root / "qa" / "open-issues.md").write_text(
        "# Open issues\n\nRecord the issue, impact, owner, and next action.\n",
        encoding="utf-8",
    )
    state = {
        "schema_version": 1,
        "title": args.title,
        "language": args.language,
        "audience": "Define the primary reader",
        "purpose": "Define the promised reader change",
        "writing_style": "Define voice and conventions",
        "publishing_route": "local-files",
        "outputs": {
            "manuscript": True,
            "presentation": False,
            "website": False,
        },
        "status": "in_progress",
        "stages": {
            "brief": "in_progress",
            "research": "not_started",
            "plan": "not_started",
            "draft": "not_started",
            "qa": "not_started",
            "release": "not_started",
        },
        "evidence": {stage: [] for stage in ("brief", "research", "plan", "draft", "qa", "release")},
    }
    (root / "book-project.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Initialized book project: {root}")
    print("Next: replace placeholder values, then run validate_project.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
