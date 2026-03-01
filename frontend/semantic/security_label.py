from enum import IntEnum


class SecurityLevel(IntEnum):
    TRUSTED = 0
    SANITIZED = 1
    UNTRUSTED = 2
    TAINTED = 3


class SecurityLabel:

    def __init__(self, level=SecurityLevel.TRUSTED, origin=None):
        self.level = level
        self.origin = origin  # source position or variable name

    def join(self, other):
        max_level = max(self.level, other.level)
        return SecurityLabel(max_level, self.origin or other.origin)

    def is_tainted(self):
        return self.level >= SecurityLevel.UNTRUSTED

    def __str__(self):
        return self.level.name