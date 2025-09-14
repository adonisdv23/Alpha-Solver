from __future__ import annotations

"""Command line interface for replaying and diffing observability logs."""

import argparse
import json
from typing import List, Optional

from . import diff as diff_mod
from .replay import ReplayHarness

__all__ = ["main"]


# ---------------------------------------------------------------------------
def main(argv: Optional[List[str]] = None) -> int:
    """Entry point for the replay CLI.

    Parameters
    ----------
    argv:
        Optional list of arguments. When ``None`` the arguments are taken from
        ``sys.argv``.
    """

    parser = argparse.ArgumentParser(description="Replay observability JSONL logs")
    parser.add_argument("log", help="path to primary log file")
    parser.add_argument("--diff", dest="diff", help="optional secondary log to diff")
    parser.add_argument("--name", dest="name", help="filter by event name", default=None)
    args = parser.parse_args(argv)

    harness = ReplayHarness(args.log)

    if args.diff:
        output = diff_mod.diff_logs(args.log, args.diff, args.name)
        if output:
            print(output)
    else:
        for event in harness.iter_events(args.name):
            print(json.dumps(event, sort_keys=True))

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
