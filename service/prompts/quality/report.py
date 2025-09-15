from typing import List, Dict


def batch_compare(pairs: List[Dict], evaluator, *, deck_sha: str, rubrics_sha_str: str) -> Dict:
    """Batch compare prompt pairs using a provided evaluator.

    Args:
        pairs: List of baseline/variant dictionaries.
        evaluator: Object with a ``compare`` method.
        deck_sha: SHA of the prompt deck.
        rubrics_sha_str: SHA of the evaluation rubrics.

    Returns:
        Dict: Summary containing win rate and per-item results.
    """
    items = []
    wins = 0
    total = len(pairs)
    for pair in pairs:
        ctx = pair.get("context", {})
        # ensure deck sha propagated for per-item route_explain
        ctx = {**ctx, "prompt_deck_sha": deck_sha}
        result = evaluator.compare(pair["baseline"], pair["variant"], context=ctx)
        if result["winner"] == "variant":
            wins += 1
        items.append({"id": pair["id"], **result})
    win_rate = wins / total if total else 0.0
    summary = {
        "total": total,
        "wins": wins,
        "win_rate": win_rate,
        "items": items,
        "route_explain": {
            "prompt_deck_sha": deck_sha,
            "rubrics_sha": rubrics_sha_str,
            "win_rate": win_rate,
        },
    }
    return summary
