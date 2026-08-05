#!/usr/bin/env python3
"""Package a skill directory into a distributable .skill archive.

A skill ships as a zip of its source tree. Doing that by hand is where skills go
wrong: an ad-hoc `zip -r` sweeps in `.git`, `__pycache__`, a previous `.skill`,
or the `dist/` directory it is writing into, and the packaging step gets skipped
entirely when nothing names the command. This script is that command.

It reads the skill's own frontmatter for the archive name, applies the same
ignore rules `verify_package.py` uses so the two agree by construction, nests
members under a single top-level directory named for the skill, and prints the
exact verification command to run next.

Packaging is not the last step. Run the printed verify_package.py command after
this one -- the archive is not trusted until its bytes are round-tripped against
source. Stdlib only.

Exit 0 when the archive is written, 1 on a packaging error, 2 on usage error.

Usage:
  python package_skill.py PATH_TO_SKILL_DIR
  python package_skill.py ../my-skill --out dist --version 0.2.0
  python package_skill.py . --name my-skill --flat --force
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
import zipfile
from pathlib import Path

# Kept in sync with verify_package.py: the two must agree on what "the source
# tree" means, or every package will report phantom extra members.
DEFAULT_IGNORE = ["dist", ".git", "__pycache__", "*.pyc", "*.skill", ".DS_Store"]


def ignored(rel: str, patterns: list[str]) -> bool:
    parts = Path(rel).parts
    for pat in patterns:
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(Path(rel).name, pat):
            return True
        if any(fnmatch.fnmatch(p, pat) for p in parts):
            return True
    return False


def read_skill_name(skill_dir: Path) -> str | None:
    """Pull `name` out of SKILL.md frontmatter, so the archive is named for the
    skill rather than whatever the directory happens to be called."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^name:\s*(.+)$", line)
        if m:
            return m.group(1).strip().strip("'\"")
    return None


def collect(skill_dir: Path, patterns: list[str]) -> list[tuple[Path, str]]:
    """Return (absolute path, archive-relative posix path) for every shipped file."""
    out: list[tuple[Path, str]] = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(skill_dir).as_posix()
        if ignored(rel, patterns):
            continue
        out.append((path, rel))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("skill_dir", help="path to the skill directory to package")
    parser.add_argument("--out", default="dist", help="directory to write the archive into")
    parser.add_argument("--name", help="archive base name (default: SKILL.md frontmatter name)")
    parser.add_argument("--version", help="version suffix, e.g. 0.2.0 -> my-skill-0.2.0.skill")
    parser.add_argument(
        "--flat",
        action="store_true",
        help="do not nest members under a top-level skill directory",
    )
    parser.add_argument(
        "--ignore",
        default=",".join(DEFAULT_IGNORE),
        help="comma-separated glob patterns to exclude",
    )
    parser.add_argument("--force", action="store_true", help="overwrite an existing archive")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    if not skill_dir.is_dir():
        print(f"error: not a directory: {skill_dir}", file=sys.stderr)
        return 2
    if not (skill_dir / "SKILL.md").is_file():
        print(f"error: no SKILL.md in {skill_dir} -- not a skill directory", file=sys.stderr)
        return 2

    name = args.name or read_skill_name(skill_dir) or skill_dir.resolve().name
    stem = f"{name}-{args.version}" if args.version else name
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"{stem}.skill"

    if archive.exists() and not args.force:
        print(f"error: {archive} exists (use --force to overwrite)", file=sys.stderr)
        return 2

    patterns = [p.strip() for p in args.ignore.split(",") if p.strip()]
    files = collect(skill_dir, patterns)
    if not files:
        print(f"error: no files to package in {skill_dir}", file=sys.stderr)
        return 1

    prefix = "" if args.flat else f"{name}/"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, rel in files:
            zf.write(path, f"{prefix}{rel}")

    size = archive.stat().st_size
    print(f"packaged {len(files)} file(s) -> {archive} ({size:,} bytes)")
    print("\nNEXT: the archive is not trusted until it is round-tripped. Run:")
    print(f"  python verify_package.py --source {skill_dir} --package {archive}")
    print("Then finish delivery per protocols/package.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
