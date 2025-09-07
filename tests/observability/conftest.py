from __future__ import annotations

import pytest

from alpha.core.accessibility import AccessibilityChecker


@pytest.fixture
def accessibility_checker() -> AccessibilityChecker:
    return AccessibilityChecker.from_config()


@pytest.fixture
def enforce_accessibility(accessibility_checker: AccessibilityChecker):
    def _check(text: str) -> None:
        report = accessibility_checker.check_text(text)
        assert report["ok"], f"readability {report['readability']:.2f} below threshold"

    return _check
