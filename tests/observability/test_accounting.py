from alpha_solver_entry import _tree_of_thought


def test_accounting_summary_present():
    res = _tree_of_thought("impossible question", score_threshold=0.9)
    summary = res.get("run_summary", {}).get("accounting", {})
    assert summary["expansions"] >= 0
    assert summary["sim_tokens"] >= 0
    assert "elapsed_ms" in summary
