from __future__ import annotations

from pathlib import Path

import pytest

from alpha.self_operator.artifact_schema import CURRENT_SCHEMA_VERSION, OperatorConfirmation, SelfOperatorArtifact
from alpha.self_operator.artifact_store import ArtifactStoreError, read_artifact_json, write_artifact_json


def artifact() -> SelfOperatorArtifact:
    return SelfOperatorArtifact(
        schema_version=CURRENT_SCHEMA_VERSION,
        lane_id="ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-LOCAL-ARTIFACT-PREFLIGHT-FOUNDATION-001",
        run_id="store-test-run",
        created_at="2026-06-08T00:00:00Z",
        operator_confirmation=OperatorConfirmation(explicit=True),
        input_summary={"kind": "store-test"},
        preflight_result={"allowed": True},
        findings=(),
        stop_state="passed",
        artifact_paths=("nested/artifact.json",),
        evidence_boundary="local-only",
    )


def test_writes_inside_allowed_output_root(tmp_path: Path) -> None:
    target = write_artifact_json(artifact(), output_root=tmp_path, relative_path="nested/artifact.json")
    assert target == tmp_path / "nested" / "artifact.json"
    assert target.read_text(encoding="utf-8").startswith("{\n")


def test_rejects_path_traversal(tmp_path: Path) -> None:
    with pytest.raises(ArtifactStoreError):
        write_artifact_json(artifact(), output_root=tmp_path, relative_path="../artifact.json")


def test_rejects_outside_root_absolute_path(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-artifact.json"
    with pytest.raises(ArtifactStoreError):
        write_artifact_json(artifact(), output_root=tmp_path, relative_path=outside)


def test_refuses_overwrite_by_default(tmp_path: Path) -> None:
    write_artifact_json(artifact(), output_root=tmp_path, relative_path="artifact.json")
    with pytest.raises(ArtifactStoreError):
        write_artifact_json(artifact(), output_root=tmp_path, relative_path="artifact.json")


def test_reads_json_back_deterministically(tmp_path: Path) -> None:
    write_artifact_json(artifact(), output_root=tmp_path, relative_path="artifact.json")
    first = read_artifact_json(output_root=tmp_path, relative_path="artifact.json")
    second = read_artifact_json(output_root=tmp_path, relative_path="artifact.json")
    assert first == second
    assert first["schema_version"] == CURRENT_SCHEMA_VERSION
