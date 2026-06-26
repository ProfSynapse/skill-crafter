#!/usr/bin/env python3
"""One-line summary of what this script checks or does.

Longer description: the rule being enforced or the task being performed, and why
it is a script rather than a prose instruction. Stdlib only so it runs anywhere.

Usage:
  python {{NAME}}.py TARGET [options]

Exit codes:
  0  clean / success
  1  violations found
  2  usage error
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def check(target: Path) -> list[str]:
    """Return a list of violation messages. Empty means clean."""
    violations: list[str] = []
    # TODO: implement the check. Append messages like:
    #   violations.append(f"{target}:{lineno}: what is wrong")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("target", help="file or directory to check")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"error: no such path: {target}", file=sys.stderr)
        return 2

    violations = check(target)
    for v in violations:
        print(v)

    if violations:
        print(f"\n{len(violations)} violation(s)")
        return 1
    print("clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
