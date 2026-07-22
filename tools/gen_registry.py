#!/usr/bin/env python3
"""Maintainer-only generator for registry.json, which must never be hand-edited."""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
REGISTRY_PATH = REPO_ROOT / "registry.json"


class RegistryError(Exception):
    """Raised when a skill cannot be represented in the registry."""


def display_path(path: Path) -> str:
    """Return a stable, repository-relative path for messages and JSON."""
    return path.relative_to(REPO_ROOT).as_posix()


def parse_frontmatter(skill_file: Path) -> tuple[str, str]:
    """Read the required single-line name and description fields."""
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    relative_path = display_path(skill_file)

    if not lines or lines[0].strip() != "---":
        raise RegistryError(f"{relative_path}: missing YAML frontmatter")

    try:
        closing_delimiter = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration as exc:
        raise RegistryError(
            f"{relative_path}: unterminated YAML frontmatter"
        ) from exc

    values: dict[str, str] = {}
    for line in lines[1:closing_delimiter]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"name", "description"}:
            values[key] = value.strip()

    missing = [key for key in ("name", "description") if not values.get(key)]
    if missing:
        raise RegistryError(
            f"{relative_path}: missing required frontmatter field(s): "
            + ", ".join(missing)
        )

    return values["name"], values["description"]


def last_updated(path: str, fallback_date: str) -> str:
    """Return the latest commit date for path, or fallback_date if unavailable."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return fallback_date

    updated = result.stdout.strip() if result.returncode == 0 else ""
    return updated or fallback_date


def build_registry() -> dict[str, object]:
    """Build the complete registry object from skill frontmatter."""
    generated_at = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    fallback_date = generated_at[:10]
    skills: list[dict[str, str]] = []

    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        name, description = parse_frontmatter(skill_file)
        skill_path = skill_file.parent.relative_to(REPO_ROOT).as_posix()
        skills.append(
            {
                "name": name,
                "description": description,
                "path": skill_path,
                "updated": last_updated(skill_path, fallback_date),
            }
        )

    skills.sort(key=lambda skill: skill["name"])
    return {"generated_at": generated_at, "skills": skills}


def write_registry(registry: dict[str, object]) -> None:
    """Write registry.json in the repository root."""
    REGISTRY_PATH.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote registry.json ({len(registry['skills'])} skills)")


def check_registry(registry: dict[str, object]) -> int:
    """Compare generated skills with registry.json, ignoring generated_at."""
    if not REGISTRY_PATH.exists():
        print("registry.json does not exist; run with --write", file=sys.stderr)
        return 1

    try:
        committed = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"could not read registry.json: {exc}", file=sys.stderr)
        return 1

    expected_skills = registry["skills"]
    actual_skills = committed.get("skills") if isinstance(committed, dict) else None
    if actual_skills == expected_skills:
        print("registry.json in sync")
        return 0

    expected = json.dumps(expected_skills, indent=2, ensure_ascii=False).splitlines()
    actual = json.dumps(actual_skills, indent=2, ensure_ascii=False).splitlines()
    print("registry.json out of sync", file=sys.stderr)
    print(
        "\n".join(
            difflib.unified_diff(
                actual,
                expected,
                fromfile="registry.json skills",
                tofile="generated skills",
                lineterm="",
            )
        ),
        file=sys.stderr,
    )
    return 1


def make_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Generate or validate the repository's registry.json."
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true", help="write registry.json")
    action.add_argument("--check", action="store_true", help="check registry.json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the requested registry action."""
    parser = make_parser()
    args = parser.parse_args(argv)
    if not args.write and not args.check:
        parser.print_help()
        return 0

    try:
        registry = build_registry()
    except (OSError, RegistryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.write:
        write_registry(registry)
        return 0
    return check_registry(registry)


if __name__ == "__main__":
    raise SystemExit(main())
