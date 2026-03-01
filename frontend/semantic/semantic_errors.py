from enum import Enum


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class SemanticError:

    def __init__(self, message, line, column,
                 error_code=None,
                 severity=Severity.ERROR,
                 security_related=False):

        self.message = message
        self.line = line
        self.column = column
        self.error_code = error_code
        self.severity = severity
        self.security_related = security_related

    def __str__(self):
        return (
            f"[{self.severity.value}] "
            f"Line {self.line}:{self.column} → "
            f"{self.message}"
        )