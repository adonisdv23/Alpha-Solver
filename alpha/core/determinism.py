from __future__ import annotations
import os
import random
import time

try:
    import numpy  # type: ignore
except Exception:  # pragma: no cover - numpy optional
    numpy = None


def apply_seed(seed: int | None) -> int:
    """Apply global seed to random, numpy, and PYTHONHASHSEED.

    If ``seed`` is ``None``, derive one from current time. The effective seed
    is returned in all cases.
    """
    if seed is None:
        seed = int(time.time() * 1000) % (2**32)
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    if numpy is not None:  # pragma: no cover - only when numpy available
        try:
            numpy.random.seed(seed)
        except Exception:
            pass
    return int(seed)
