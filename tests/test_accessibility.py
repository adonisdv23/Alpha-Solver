from alpha.core.accessibility import AccessibilityChecker


def test_accessibility_readability():
    checker = AccessibilityChecker()
    good = "This is a short and simple sentence."
    bad = "Inconsequentially, the antidisestablishmentarianistic paradigm obfuscates."
    assert checker.check_text(good)["ok"]
    assert not checker.check_text(bad)["ok"]


def test_accessibility_contrast():
    checker = AccessibilityChecker()
    assert checker.check_contrast("#000000", "#FFFFFF")["ok"]
    assert not checker.check_contrast("#777777", "#777777")["ok"]
