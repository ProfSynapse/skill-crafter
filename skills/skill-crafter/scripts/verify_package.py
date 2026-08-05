#!/usr/bin/env python3
"""Verify a packaged skill artifact against its source tree.

A structure validator reads the source tree; it cannot see what actually shipped.
Skills are packaged by zipping the filesystem, and if the authoring channel
(editor) and the packaging channel (shell) ever diverge, a file can ship
truncated while every source-side check still passes. This script closes that gap
by inspecting the produced artifact directly:

  1. Round-trip: for each source file, find the matching member in the .skill
     archive and compare a SHA-256 hash. A mismatch means the shipped bytes are
     not the source bytes (truncated, stale, or corrupted on the way into the zip).
  2. Completeness: run cheap content heuristics on the *packaged* members
     (non-empty, closed code fences, not cut mid-sentence). Markdown has no
     compile step, so truncation is otherwise silent.

Run this after packaging and before declaring a skill done. It is the integrity
gate that sits beside validate_skill.py's structure gate. Stdlib only.

Exit 0 when the artifact matches the source and every member is complete, 1 when
a defect is found, 2 on usage error.

Usage:
  python verify_package.py --source PATH_TO_SKILL_DIR --package dist/my-skill.skill
  python verify_package.py --source . --package dist/skill-crafter-0.2.0.skill \
      --ignore dist,.git,__pycache__
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import sys
import zipfile
from pathlib import Path

DEFAULT_IGNORE = ["dist", ".git", "__pycache__", "*.pyc", "*.skill"]
TEXT_SUFFIXES = {".md", ".py", ".sh", ".txt", ".json", ".yaml", ".yml"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ignored(rel: str, patterns: list[str]) -> bool:
    parts = Path(rel).parts
    for pat in patterns:
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(Path(rel).name, pat):
            return True
        if any(fnmatch.fnmatch(p, pat) for p in parts):
            return True
    return False


def source_files(root: Path, patterns: list[str]) -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if ignored(rel, patterns):
            continue
        out[rel] = path.read_bytes()
    return out


def package_members(zip_path: Path) -> dict[str, bytes]:
    """Read every file member, stripping a single common top-level directory if
    the archive nests everything under one (e.g. `skill-crafter/SKILL.md`)."""
    out: dict[str, bytes] = {}
    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        # Strip a single common top-level directory only when every member nests
        # under the same one (e.g. `skill-crafter/...`).
        heads = {n.split("/", 1)[0] for n in names if "/" in n}
        nested = all("/" in n for n in names)
        strip = f"{heads.pop()}/" if nested and len(heads) == 1 else ""
        for n in names:
            rel = n[len(strip):] if strip and n.startswith(strip) else n
            out[rel] = zf.read(n)
    return out


def check_completeness(rel: str, data: bytes) -> tuple[list[str], list[str]]:
    """Cheap heuristics that catch silent truncation in shipped text files."""
    errors: list[str] = []
    warnings: list[str] = []
    if Path(rel).suffix not in TEXT_SUFFIXES:
        return errors, warnings
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        errors.append(f"{rel}: not valid UTF-8 (corrupted)")
        return errors, warnings

    if not text.strip():
        errors.append(f"{rel}: file is empty")
        return errors, warnings
    if text.count("```") % 2 != 0:
        errors.append(f"{rel}: unclosed code fence (``` count is odd)")
    if not text.endswith("\n"):
        warnings.append(f"{rel}: does not end with a newline")

    if Path(rel).suffix == ".md":
        last = next((ln.rstrip() for ln in reversed(text.splitlines()) if ln.strip()), "")
        if _looks_cut_off(last):
            errors.append(f"{rel}: ends mid-sentence -> '{last[-60:]}' (possible truncation)")
    return errors, warnings


def _looks_cut_off(line: str) -> bool:
    """True when a markdown file's last content line reads like cut-off prose.

    Structural lines (headings, list items, table rows, blockquotes, fences) and
    lines ending in sentence punctuation or closing tokens are fine. We flag only
    multi-word prose that ends on a comma or a bare lowercase word, which is the
    signature of a sentence chopped in half.
    """
    if not line or line[0] in "#-*>|" or line.lstrip().startswith(("```", "1.", "- ", "* ")):
        return False
    if line.endswith(("```", "|")):
        return False
    if line[-1] in ".?!:;)]}>\"'`*_":
        return False
    if " " not in line:
        return False
    return line[-1] == "," or line[-1].isalpha() and line[-1].islower()


def verify(source: Path, package: Path, patterns: list[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    src = source_files(source, patterns)
    pkg = package_members(package)

    for rel, data in src.items():
        if rel not in pkg:
            errors.append(f"{rel}: in source but missing from package")
            continue
        if sha256(data) != sha256(pkg[rel]):
            errors.append(
                f"{rel}: hash mismatch source({len(data)}B) != package({len(pkg[rel])}B)"
            )

    for rel in pkg:
        if rel not in src:
            warnings.append(f"{rel}: in package but not in source tree")

    for rel, data in sorted(pkg.items()):
        e, w = check_completeness(rel, data)
        errors.extend(e)
        warnings.extend(w)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--source", required=True, help="path to the skill source directory")
    parser.add_argument("--package", required=True, help="path to the produced .skill archive")
    parser.add_argument(
        "--ignore",
        default=",".join(DEFAULT_IGNORE),
        help="comma-separated glob patterns to skip in the source tree",
    )
    args = parser.parse_args()

    source = Path(args.source)
    package = Path(args.package)
    if not source.is_dir():
        print(f"error: not a directory: {source}", file=sys.stderr)
        return 2
    if not package.is_file():
        print(f"error: not a file: {package}", file=sys.stderr)
        return 2
    if not zipfile.is_zipfile(package):
        print(f"error: not a zip/.skill archive: {package}", file=sys.stderr)
        return 2

    patterns = [p.strip() for p in args.ignore.split(",") if p.strip()]
    errors, warnings = verify(source, package, patterns)

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\nMISMATCH: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nINTACT: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
