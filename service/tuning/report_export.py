from __future__ import annotations

"""Utilities for exporting weight tuning reports as JSON artifacts."""

from pathlib import Path
import argparse
import json
from typing import Any, Dict


REQUIRED_TOP_LEVEL = {"seed", "before", "after", "delta", "per_factor"}


def _round_floats(obj: Any) -> Any:
    """Recursively round floats for stable JSON output."""
    if isinstance(obj, float):
        return round(obj, 6)
    if isinstance(obj, dict):
        return {k: _round_floats(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_round_floats(v) for v in obj]
    return obj


def _validate_report(data: Dict[str, Any]) -> None:
    missing = REQUIRED_TOP_LEVEL - data.keys()
    if missing:
        raise ValueError(f"missing keys: {sorted(missing)}")
    for side in ["before", "after"]:
        section = data[side]
        if not all(k in section for k in ["accuracy", "win_rate", "weights"]):
            raise ValueError(f"{side} section missing fields")
    if not all(k in data["delta"] for k in ["accuracy_pp", "win_rate_pp"]):
        raise ValueError("delta section missing fields")
    if not isinstance(data["per_factor"], list):
        raise ValueError("per_factor must be a list")


def export_tuning_report(in_path: Path, out_path: Path) -> Path:
    """Validate and write *in_path* tuning report to *out_path*.

    Returned path points to the written file.
    """
    raw = json.loads(Path(in_path).read_text())
    _validate_report(raw)
    cleaned = _round_floats(raw)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(cleaned, sort_keys=True, indent=2) + "\n")
    return out_path


def main(argv: list[str] | None = None) -> Path:
    parser = argparse.ArgumentParser(description="Export tuning report JSON")
    parser.add_argument("--in", dest="in_path", required=True)
    parser.add_argument("--out", dest="out_path", required=True)
    args = parser.parse_args(argv)
    return export_tuning_report(Path(args.in_path), Path(args.out_path))


if __name__ == "__main__":  # pragma: no cover - exercised via CLI
    main()
