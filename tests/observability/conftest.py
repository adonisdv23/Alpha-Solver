from __future__ import annotations

import pytest

from alpha.core.observability import ObservabilityManager


@pytest.fixture
def check_accessibility() -> ObservabilityManager:
    """Provide an ObservabilityManager with accessibility checking enabled."""

    cfg = ObservabilityManager().config
    cfg.enable_accessibility = True
    return ObservabilityManager(cfg)

