from __future__ import annotations

import json
import logging
from typing import Any, Dict

import pytest

from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha_solver_entry import _tree_of_thought


def _low_confidence(self, query: str) -> Dict[str, Any]:  # pragma: no cover - used in tests
    return {
        "answer": "low",
        "confidence": 0.55,
        "path": [],
        "explored_nodes": 0,
        "config": {},
        "reason": "ok",
    }


@pytest.mark.parametrize("enable_cot", [True, False])
def test_tree_of_thought_policy(monkeypatch, caplog, enable_cot):
    monkeypatch.setattr(TreeOfThoughtSolver, "solve", _low_confidence)
    with caplog.at_level(logging.INFO):
        result = _tree_of_thought(
            "query",
            low_conf_threshold=0.60,
            enable_cot_fallback=enable_cot,
        )
    assert result["route"] == ("cot_fallback" if enable_cot else "best_effort")
    assert json.dumps(result)
    assert any("safe_out_decision" in r.message for r in caplog.records)
