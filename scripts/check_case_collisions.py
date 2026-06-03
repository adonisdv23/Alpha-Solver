#!/usr/bin/env python3
"""Fail when tracked Git paths collide on case-insensitive filesystems."""

from __future__ import annotations

import subprocess
import sys
from collections import defaultdict


def tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def case_collision_groups(paths: list[str]) -> dict[str, list[str]]:
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for path in paths:
        groups[path.lower()].append(path)
    return {key: sorted(group) for key, group in sorted(groups.items()) if len(group) > 1}


def main() -> int:
    collisions = case_collision_groups(tracked_paths())
    if not collisions:
        print("No Git path case collisions found.")
        return 0

    print("Git path case collisions found:", file=sys.stderr)
    for key, paths in collisions.items():
        print(key, file=sys.stderr)
        for path in paths:
            print(f"  {path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
