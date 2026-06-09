"""Local JSON artifact read/write helpers with explicit safe-path rules."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from alpha.self_operator.artifact_schema import SelfOperatorArtifact
from alpha.self_operator.redaction import redact_value


class ArtifactStoreError(ValueError):
    """Raised when an artifact store path or write operation is unsafe."""


def resolve_artifact_path(output_root: Path | str, relative_path: Path | str) -> Path:
    """Resolve an artifact path and reject traversal/outside-root targets."""

    root = Path(output_root).resolve()
    candidate = Path(relative_path)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (root / candidate).resolve()
    if ".." in candidate.parts or not _is_relative_to(resolved, root):
        raise ArtifactStoreError(f"artifact path outside allowed output root: {relative_path}")
    return resolved


def dumps_artifact_json(payload: SelfOperatorArtifact | Mapping[str, Any], *, redact: bool = True) -> str:
    """Return deterministic UTF-8-compatible JSON text for a local artifact."""

    if isinstance(payload, SelfOperatorArtifact):
        data = payload.to_dict(redact=redact)
    else:
        data = redact_value(dict(payload)) if redact else dict(payload)
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_artifact_json(
    payload: SelfOperatorArtifact | Mapping[str, Any],
    *,
    output_root: Path | str,
    relative_path: Path | str,
    overwrite: bool = False,
    redact: bool = True,
) -> Path:
    """Write deterministic local JSON below output_root only.

    The caller must provide a local output root. Source-artifact mutation and
    implicit overwrite are rejected by default.
    """

    target = resolve_artifact_path(output_root, relative_path)
    if target.exists() and not overwrite:
        raise ArtifactStoreError(f"artifact already exists and overwrite is false: {relative_path}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dumps_artifact_json(payload, redact=redact), encoding="utf-8")
    return target


def read_artifact_json(*, output_root: Path | str, relative_path: Path | str) -> dict[str, Any]:
    """Read local JSON from output_root after applying the same path guard."""

    target = resolve_artifact_path(output_root, relative_path)
    return json.loads(target.read_text(encoding="utf-8"))


def _is_relative_to(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True
