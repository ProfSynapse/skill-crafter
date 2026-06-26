#!/usr/bin/env python3
"""Validate a skill directory against the generic skill best practices.

Checks, in order:
  1. SKILL.md exists at the skill root.
  2. Frontmatter has a kebab-case `name` and a non-empty `description` within the
     length budget. Warn if `name` does not match the directory.
  3. The router (SKILL.md body, frontmatter excluded) stays under the line and
     word thresholds. Over threshold is the signal to modularize.
  4. Every relative file reference in any markdown resolves (dependency mapping:
     no dangling links to references/protocols/agents/scripts).

These are the universal checks. Domain-specific checks belong in the skill's own
scripts/ (see references/validation-pattern.md). Stdlib only.

Exit 0 when valid, 1 when an error is found, 2 on usage error. Warnings do not
fail the run.

Usage:
  python validate_skill.py PATH_TO_SKILL_DIR
  python validate_skill.py . --max-lines 150 --max-words 1500 --max-description 1024
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MD_LINK = re.compile(r"\]\(([^)]+)\)")
BACKTICK_PATH = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|sh|json|ya?ml|txt))`")
KNOWN_FOLDERS = {"agents", "scripts", "templates", "references", "protocols"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter dict, body without frontmatter)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    data: dict = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return data, "\n".join(lines[i + 1 :])
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        if m:
            data[m.group(1)] = m.group(2).strip().strip("'\"")
    return data, text


def is_external(ref: str) -> bool:
    return ref.startswith(("http://", "https://", "mailto:", "#", "skill://", "<"))


def collect_refs(md_text: str) -> set[str]:
    """Collect intra-skill file references.

    Markdown links `](path)` are always references. Backticked paths count only
    when they contain a `/`, so casual prose mentions of a bare filename (for
    example `scaffold.py` in a sentence) are not treated as links.
    """
    refs: set[str] = set()
    for m in MD_LINK.finditer(md_text):
        refs.add(m.group(1).split("#", 1)[0].strip())
    for m in BACKTICK_PATH.finditer(md_text):
        token = m.group(1).strip()
        if "/" in token:
            refs.add(token)
    return {r for r in refs if r and not is_external(r)}


def resolves(skill_dir: Path, md: Path, ref: str) -> bool:
    """A reference is valid if it resolves relative to the referring file's
    directory OR relative to the skill root. This keeps the validator agnostic to
    whether a doc uses file-relative (../) or root-relative paths."""
    candidates = [
        (md.parent / ref).resolve(),
        (skill_dir / ref).resolve(),
    ]
    return any(c.exists() for c in candidates)


def validate(skill_dir: Path, args) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"missing SKILL.md at {skill_dir}"], warnings

    fm, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    name = fm.get("name", "")
    desc = fm.get("description", "")

    if not name:
        errors.append("frontmatter: missing `name`")
    elif not KEBAB.match(name):
        errors.append(f"frontmatter: name '{name}' is not kebab-case")
    elif name != skill_dir.resolve().name:
        warnings.append(f"frontmatter: name '{name}' != directory '{skill_dir.resolve().name}'")

    if not desc:
        errors.append("frontmatter: missing `description` (this is the trigger text)")
    elif len(desc) > args.max_description:
        errors.append(f"frontmatter: description is {len(desc)} chars (max {args.max_description})")

    body_lines = [ln for ln in body.splitlines() if ln.strip()]
    n_lines, n_words = len(body_lines), sum(len(ln.split()) for ln in body_lines)
    if n_lines > args.max_lines or n_words > args.max_words:
        errors.append(
            f"router too long: {n_lines} lines / {n_words} words "
            f"(max {args.max_lines}/{args.max_words}) -> modularize (protocols/modularize.md)"
        )

    for md in sorted(skill_dir.rglob("*.md")):
        # templates/ holds inert copy-targets whose paths resolve in the
        # destination skill, not here, so do not resolve their links.
        if "templates" in md.relative_to(skill_dir).parts:
            continue
        for ref in collect_refs(md.read_text(encoding="utf-8")):
            if not resolves(skill_dir, md, ref):
                errors.append(f"{md.relative_to(skill_dir)}: broken reference -> {ref}")

    for child in skill_dir.iterdir():
        if child.is_dir() and child.name not in KNOWN_FOLDERS and not child.name.startswith("."):
            warnings.append(f"non-standard folder: {child.name}/ (known: {', '.join(sorted(KNOWN_FOLDERS))})")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("skill_dir", help="path to the skill directory")
    parser.add_argument("--max-lines", type=int, default=150)
    parser.add_argument("--max-words", type=int, default=1500)
    parser.add_argument("--max-description", type=int, default=1024)
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    if not skill_dir.is_dir():
        print(f"error: not a directory: {skill_dir}", file=sys.stderr)
        return 2

    errors, warnings = validate(skill_dir, args)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\nINVALID: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nVALID: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
