def stable_sort(items):
    # Mirror tie-break logic (score desc, prior desc, id asc)
    return sorted(
        items,
        key=lambda x: (-round(x["score"],8), -round(x.get("prior_score",0.0),8), str(x["tool_id"]))
    )

def test_tie_break_deterministic():
    items = [
        {"tool_id":"B","score":0.900000001,"prior_score":0.2},
        {"tool_id":"A","score":0.9,"prior_score":0.3},
        {"tool_id":"C","score":0.9,"prior_score":0.3},
    ]
    out = stable_sort(items)
    # A then C then B because of prior desc, then id asc, then tiny rounding
    assert [x["tool_id"] for x in out] == ["A","C","B"]
