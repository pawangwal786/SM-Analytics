import re
from typing import Any, List, Set


class Redactor:
    """
    Recursively redacts sensitive keys from dictionaries before logging.
    Supports both exact matches and pattern-based matches (case-insensitive).
    """

    REDACTED_TEXT = "*****"

    def __init__(self, exact_matches: Set[str] = None, patterns: List[str] = None):
        # Default exact match denylist
        self.exact_matches = exact_matches or {
            "authorization",
            "proxy-authorization",
            "cookie",
            "set-cookie",
            "password",
            "passwd",
            "secret",
            "client_secret",
            "api_key",
            "access_token",
            "refresh_token",
            "id_token",
            "jwt",
            "session",
        }
        self.exact_matches = {k.lower() for k in self.exact_matches}

        # Default pattern match denylist
        patterns = patterns or [r".*_password$", r".*_secret$", r".*_token$"]
        # Compile patterns with IGNORECASE
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

    def _should_redact(self, key: str) -> bool:
        key_lower = key.lower()
        if key_lower in self.exact_matches:
            return True
        for pattern in self.patterns:
            if pattern.match(key):
                return True
        return False

    def redact(self, data: Any) -> Any:
        """
        Recursively redact sensitive data from a dictionary or list.
        Returns a new copy of the data structure.
        """
        if isinstance(data, dict):
            return {
                k: self.REDACTED_TEXT
                if isinstance(k, str) and self._should_redact(k)
                else self.redact(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self.redact(item) for item in data]
        return data
