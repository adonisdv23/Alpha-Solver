from __future__ import annotations

import math
import re
from collections import Counter
from typing import Callable, Dict, Iterable


def exact_match(pred: str, expected: str, meta: dict | None = None) -> float:
    return float(str(pred).strip() == str(expected).strip())


def f1_token(pred: str, expected: str, meta: dict | None = None) -> float:
    def _tokens(s: str) -> Iterable[str]:
        return s.split()

    pt, gt = Counter(_tokens(str(pred))), Counter(_tokens(str(expected)))
    common = sum((pt & gt).values())
    if not common:
        return 0.0
    precision = common / sum(pt.values())
    recall = common / sum(gt.values())
    return 2 * precision * recall / (precision + recall)


def regex_pass(pred: str, expected: str, meta: dict | None = None) -> float:
    if not meta or not meta.get("regex"):
        return 0.0
    return float(re.search(meta["regex"], str(pred)) is not None)


def numeric_close(pred: str, expected: str, meta: dict | None = None) -> float:
    try:
        p, e = float(pred), float(expected)
    except (TypeError, ValueError):
        return 0.0
    abs_tol = meta.get("abs_tol", 1e-3) if meta else 1e-3
    rel_tol = meta.get("rel_tol", 1e-3) if meta else 1e-3
    return float(math.isclose(p, e, abs_tol=abs_tol, rel_tol=rel_tol))


SCORERS: Dict[str, Callable[[str, str, dict | None], float]] = {
    "em": exact_match,
    "f1": f1_token,
    "regex": regex_pass,
    "num": numeric_close,
}
