#!/usr/bin/env python3
"""Validate the portable state and required layout of a book project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ALLOWED_STATUS = {"not_started", "in_progress", "blocked", "complete"}
STAGES = ("brief", "research", "plan", "draft", "qa", "release")
REQUIRED_TEXT = (
    "title",
    "language",
    "audience",
    "purpose",
    "writing_style",
    "publishing_route",
)
PLACEHOLDERS = ("working title", "define the ", "replace with", "describe the ")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    state_path = root / "book-project.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ["missing book-project.json"]
    except json.JSONDecodeError as exc:
        return [f"invalid book-project.json: {exc}"]

    if state.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for field in REQUIRED_TEXT:
        value = state.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string")
    outputs = state.get("outputs")
    if not isinstance(outputs, dict):
        errors.append("outputs must be an object")
    else:
        for name in ("manuscript", "presentation", "website"):
            if not isinstance(outputs.get(name), bool):
                errors.append(f"outputs.{name} must be true or false")
    status = state.get("status")
    if status not in ALLOWED_STATUS:
        errors.append(f"status must be one of {sorted(ALLOWED_STATUS)}")
    stages = state.get("stages")
    if not isinstance(stages, dict):
        errors.append("stages must be an object")
    else:
        for name in STAGES:
            if stages.get(name) not in ALLOWED_STATUS:
                errors.append(f"stages.{name} must be one of {sorted(ALLOWED_STATUS)}")
    evidence = state.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence must be an object")
        evidence = {}
    else:
        for stage in STAGES:
            entries = evidence.get(stage)
            if not isinstance(entries, list):
                errors.append(f"evidence.{stage} must be a list of relative file paths")
                continue
            for entry in entries:
                if not isinstance(entry, str) or not entry.strip():
                    errors.append(f"evidence.{stage} contains an invalid path")
                    continue
                relative_path = Path(entry)
                if relative_path.is_absolute() or ".." in relative_path.parts:
                    errors.append(f"evidence.{stage} must use a safe relative path: {entry}")
                    continue
                evidence_path = (root / relative_path).resolve()
                try:
                    evidence_path.relative_to(root)
                except ValueError:
                    errors.append(f"evidence.{stage} escapes the project root: {entry}")
                    continue
                if not evidence_path.is_file():
                    errors.append(f"evidence.{stage} file does not exist: {entry}")
    for relative in ("brief.md", "manuscript", "research", "plan", "qa", "assets", "dist"):
        if not (root / relative).exists():
            errors.append(f"missing {relative}")

    if isinstance(stages, dict):
        for stage in STAGES:
            if stages.get(stage) == "complete" and not evidence.get(stage):
                errors.append(f"complete stage requires evidence.{stage}")

        if stages.get("draft") == "complete":
            manuscript_dir = root / "manuscript"
            if manuscript_dir.is_dir() and not any(manuscript_dir.glob("*.md")):
                errors.append("complete draft requires at least one manuscript Markdown file")
        if stages.get("qa") == "complete":
            qa_dir = root / "qa"
            reports = (
                path for path in qa_dir.glob("*.md")
                if path.name.lower() != "open-issues.md"
            ) if qa_dir.is_dir() else ()
            if not any(reports):
                errors.append("complete qa requires a QA report other than open-issues.md")
        if stages.get("release") == "complete":
            dist_dir = root / "dist"
            if dist_dir.is_dir() and not any(path.is_file() for path in dist_dir.rglob("*")):
                errors.append("complete release requires at least one file in dist")

    if status == "complete" and isinstance(stages, dict):
        incomplete = [name for name in STAGES if stages.get(name) != "complete"]
        if incomplete:
            errors.append(f"complete project has incomplete stages: {', '.join(incomplete)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--strict", action="store_true", help="fail when placeholder values remain")
    args = parser.parse_args()
    root = args.project_dir.resolve()
    errors = validate(root)
    if args.strict and not errors:
        state = json.loads((root / "book-project.json").read_text(encoding="utf-8"))
        for field in REQUIRED_TEXT:
            lowered = state[field].strip().lower()
            if any(marker in lowered for marker in PLACEHOLDERS):
                errors.append(f"{field} still contains a placeholder")
        brief = (root / "brief.md").read_text(encoding="utf-8").lower()
        if any(marker in brief for marker in PLACEHOLDERS):
            errors.append("brief.md still contains a placeholder")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: valid book project at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
