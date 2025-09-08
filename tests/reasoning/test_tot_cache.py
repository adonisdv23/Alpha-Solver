from alpha_solver_entry import _tree_of_thought


def test_tot_cache_reduces_exploration(tmp_path):
    cache_file = tmp_path / "cache.json"
    result1 = _tree_of_thought(
        "impossible question",
        score_threshold=0.9,
        cache_path=str(cache_file),
    )
    explored1 = result1["diagnostics"]["tot"]["explored_nodes"]
    result2 = _tree_of_thought(
        "impossible question",
        score_threshold=0.9,
        cache_path=str(cache_file),
    )
    explored2 = result2["diagnostics"]["tot"]["explored_nodes"]
    assert explored1 > explored2
    assert cache_file.exists()
