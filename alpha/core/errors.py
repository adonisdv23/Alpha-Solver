class UserInputError(Exception):
    """Raised for expected user input/config errors."""


def hint(exc: Exception, suggestion: str) -> Exception:
    exc.args = (f"{exc.args[0]}  (hint: {suggestion})",)
    return exc

