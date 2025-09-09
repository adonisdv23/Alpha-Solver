class UserInputError(Exception):
    """Raised for expected user input/config errors."""


def hint(exc: Exception, suggestion: str) -> Exception:
    exc.args = (f"{exc.args[0]}  (hint: {suggestion})",)
    return exc


# Canonical SAFE-OUT reason taxonomy used across modules.
SAFE_OUT_REASONS = {
    "low_confidence",
    "constraint_violation",
    "missing_requirements",
    "incoherent",
    "timeout",
}


__all__ = ["UserInputError", "hint", "SAFE_OUT_REASONS"]
