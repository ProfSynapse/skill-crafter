#!/usr/bin/env python3
"""Scaffold a new skill directory from skill-crafter templates.

Creates a slim-router SKILL.md plus the folders you ask for, and seeds the
self-refinement scaffolding (protocols/self-refine.md + refinement-log.md) so
every generated skill is self-refining from birth. CLI-first: the agent runs this
once during the Architect phase instead of hand-creating boilerplate.

Templates are read from ../templates relative to this script, so edits to the
templates propagate to every new skill. Placeholders {{NAME}}, {{DESCRIPTION}},
{{TITLE}} are replaced by simple string substitution.

Usage:
  python scaffold.py my-skill --description "Do X when Y." --path ../skills
  python scaffold.py my-skill --folders agents,scripts,references
  python scaffold.py my-skill --no-self-refine
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEFAULT_FOLDERS = ["agents", "scripts", "templates", "references", "protocols"]
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def render(template_name: str, replacements: dict) -> str:
    text = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    for token, value in replacements.items():
        text = text.replace(token, value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("name", help="kebab-case skill name")
    parser.add_argument("--description", default="Describe when this skill should trigger.")
    parser.add_argument("--path", default=".", help="parent directory to create the skill in")
    parser.add_argument("--folders", default=",".join(DEFAULT_FOLDERS))
    parser.add_argument("--no-self-refine", action="store_true")
    parser.add_argument("--force", action="store_true", help="write into a non-empty directory")
    args = parser.parse_args()

    name = args.name.strip()
    skill_dir = Path(args.path) / name
    if skill_dir.exists() and any(skill_dir.iterdir()) and not args.force:
        print(f"error: {skill_dir} exists and is not empty (use --force)", file=sys.stderr)
        return 2

    folders = [f.strip() for f in args.folders.split(",") if f.strip()]
    skill_dir.mkdir(parents=True, exist_ok=True)
    for folder in folders:
        path = skill_dir / folder
        path.mkdir(exist_ok=True)
        if not any(path.iterdir()):
            (path / ".gitkeep").write_text("", encoding="utf-8")

    replacements = {
        "{{NAME}}": name,
        "{{DESCRIPTION}}": args.description,
        "{{TITLE}}": name.replace("-", " ").title(),
    }
    (skill_dir / "SKILL.md").write_text(render("SKILL.template.md", replacements), encoding="utf-8")

    if not args.no_self_refine:
        (skill_dir / "protocols").mkdir(exist_ok=True)
        (skill_dir / "protocols" / "self-refine.md").write_text(
            render("self-refine.template.md", replacements), encoding="utf-8"
        )
        (skill_dir / "refinement-log.md").write_text(
            render("refinement-log.template.md", replacements), encoding="utf-8"
        )

    print(f"scaffolded skill at {skill_dir}")
    print("next: fill in SKILL.md and the folders, then run validate_skill.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
