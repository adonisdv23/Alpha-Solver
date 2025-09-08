from __future__ import annotations

import json
import logging

from alpha.reasoning.cot import guidance_score
from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha_solver_entry import _tree_of_thought


def test_integration_modes_and_logs(monkeypatch, caplog):
    monkeypatch.setattr(TreeOfThoughtSolver, "path_scorer", lambda self, node: 0.5)
    cot = guidance_score({"hint": "integration"})
    assert 0.0 <= cot <= 1.0
    single = TreeOfThoughtSolver(seed=42, multi_branch=False).solve("integration")
    multi = TreeOfThoughtSolver(seed=42, multi_branch=True).solve("integration")
    assert single["answer"] and multi["answer"]
    with caplog.at_level(logging.INFO):
        result = _tree_of_thought("integration", enable_progressive_router=True)
    assert "diagnostics" in result
    messages = [r.message for r in caplog.records]
    assert any("tot_layer" in m for m in messages)
    assert any("router_escalate" in m for m in messages)
    json.dumps(result)

