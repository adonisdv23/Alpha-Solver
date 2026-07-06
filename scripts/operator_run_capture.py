#!/usr/bin/env python3
"""Local-only CLI for the operator run capture harness.

Subcommands:
  init      Scaffold a capture file from an operator-authored case packet.
  validate  Check a capture file (add --for-export for export completeness).
  export    Validate and write the normalized evidence packet.

This CLI reads and writes local JSON files only. It performs no provider,
hosted-model, or local-model calls, no tool execution, and no network access,
and it does not score, blind, or unblind outputs.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alpha.eval import operator_run_capture as orc  # noqa: E402

EXIT_OK = 0
EXIT_VALIDATION = 1
EXIT_USAGE = 2


def _read_json(path: Path, label: str):
    try:
        return orc.load_json(path)
    except FileNotFoundError:
        print(f"error: {label} not found: {path}", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)
    except ValueError as exc:
        print(f"error: {label} is not valid JSON: {path}: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)


def _write_bytes(path: Path, payload: bytes, force: bool) -> None:
    if path.exists() and not force:
        print(
            f"error: refusing to overwrite existing file without --force: {path}",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_USAGE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _report_errors(errors: list) -> None:
    for error in errors:
        print(f"FAIL {error}")


def cmd_init(args: argparse.Namespace) -> int:
    case_packet = _read_json(Path(args.case_packet), "case packet")
    errors = orc.validate_case_packet(case_packet)
    if errors:
        _report_errors(errors)
        return EXIT_VALIDATION
    capture = orc.scaffold_capture(case_packet)
    _write_bytes(Path(args.out), orc.render_json_bytes(capture), args.force)
    print(
        f"OK scaffolded capture for packet {capture['packet_id']!r} "
        f"({len(capture['cases'])} cases) -> {args.out}"
    )
    return EXIT_OK


def cmd_validate(args: argparse.Namespace) -> int:
    capture = _read_json(Path(args.capture), "capture file")
    errors = orc.validate_capture(capture, for_export=args.for_export)
    if errors:
        _report_errors(errors)
        return EXIT_VALIDATION
    mode = "export-ready" if args.for_export else "structurally valid"
    print(f"OK capture is {mode}: {args.capture}")
    return EXIT_OK


def cmd_export(args: argparse.Namespace) -> int:
    capture = _read_json(Path(args.capture), "capture file")
    errors = orc.validate_capture(capture, for_export=True)
    if errors:
        _report_errors(errors)
        return EXIT_VALIDATION
    packet = orc.build_evidence_packet(capture)
    _write_bytes(Path(args.out), orc.render_json_bytes(packet), args.force)
    counts = packet["counts"]
    print(
        f"OK exported evidence packet {packet['packet_id']!r} "
        f"(captured={counts['captured']} excluded={counts['excluded']}) -> {args.out}"
    )
    print(f"content_digest: {packet['content_digest']}")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="operator_run_capture",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="scaffold a capture file")
    init_parser.add_argument("--case-packet", required=True)
    init_parser.add_argument("--out", required=True)
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=cmd_init)

    validate_parser = sub.add_parser("validate", help="validate a capture file")
    validate_parser.add_argument("--capture", required=True)
    validate_parser.add_argument("--for-export", action="store_true")
    validate_parser.set_defaults(func=cmd_validate)

    export_parser = sub.add_parser("export", help="export the evidence packet")
    export_parser.add_argument("--capture", required=True)
    export_parser.add_argument("--out", required=True)
    export_parser.add_argument("--force", action="store_true")
    export_parser.set_defaults(func=cmd_export)
    return parser


def main(argv: list | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
