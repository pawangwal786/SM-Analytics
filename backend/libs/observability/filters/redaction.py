# import re
# from typing import Any, List, Set


# class Redactor:
#     """
#     Recursively redacts sensitive keys from dictionaries before logging.
#     Supports both exact matches and pattern-based matches (case-insensitive).
#     """

#     REDACTED_TEXT = "*****"

#     def __init__(self, exact_matches: Set[str] = None, patterns: List[str] = None):

#         # Default exact match denylist
#         self.exact_matches = exact_matches or {
#             "authorization",
#             "proxy-authorization",
#             "cookie",
#             "set-cookie",
#             "password",
#             "passwd",
#             "secret",
#             "client_secret",
#             "api_key",
#             "access_token",
#             "refresh_token",
#             "id_token",
#             "jwt",
#             "session",
#         }
#         self.exact_matches = {k.lower() for k in self.exact_matches}

#         # Default pattern match denylist
#         patterns = patterns or [r".*_password$", r".*_secret$", r".*_token$"]
#         # Compile patterns with IGNORECASE
#         self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

#     def _should_redact(self, key: str) -> bool:
#         key_lower = key.lower()
#         if key_lower in self.exact_matches:
#             return True
#         for pattern in self.patterns:
#             if pattern.match(key):
#                 return True
#         return False

#     def redact(self, data: Any) -> Any:
#         """
#         Recursively redact sensitive data from a dictionary or list.
#         Returns a new copy of the data structure.
#         """
#         if isinstance(data, dict):
#             return {
#                 k: self.REDACTED_TEXT
#                 if isinstance(k, str) and self._should_redact(k)
#                 else self.redact(v)
#                 for k, v in data.items()
#             }
#         elif isinstance(data, list):
#             return [self.redact(item) for item in data]
#         return data

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any


class Redactor:
    """Recursively redact sensitive values from nested data structures."""

    DEFAULT_KEYS = {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "password",
        "passwd",
        "secret",
        "client_secret",
        "client_key",
        "api_key",
        "x-api-key",
        "access_token",
        "refresh_token",
        "id_token",
        "oauth_token",
        "jwt",
        "session",
        "sessionid",
        "csrf_token",
        "xsrf_token",
        "private_key",
        "master_key",
        "signing_key",
        "encryption_key",
        "connection_string",
        "connection_uri",
        "dsn",
        "credentials",
    }

    DEFAULT_PATTERNS = (
        "password",
        "secret",
        "token",
        "credential",
        "api[_-]?key",
        "private[_-]?key",
        "client[_-]?(?:secret|key)",
        "connection[_-]?(?:string|uri)",
        "dsn",
    )

    def __init__(
        self,
        *,
        exact_keys: Iterable[str] | None = None,
        patterns: Iterable[str] | None = None,
        replacement: str = "*****",
    ) -> None:
        self.replacement = replacement
        self.keys = {k.strip().lower() for k in (exact_keys or self.DEFAULT_KEYS)}
        try:
            self.patterns = tuple(
                re.compile(p, re.IGNORECASE)
                for p in (patterns or self.DEFAULT_PATTERNS)
            )
        except re.error as e:
            raise ValueError(f"Invalid redaction pattern: {e}") from e

    def _redact_key(self, key: str) -> bool:
        key = key.strip().lower()
        return key in self.keys or any(p.search(key) for p in self.patterns)

    def redact(self, obj: Any) -> Any:
        return self._redact(obj, set())

    def _redact(self, obj: Any, seen: set[int]) -> Any:
        if isinstance(obj, (Mapping, list, tuple, set, frozenset)):
            oid = id(obj)
            if oid in seen:
                return "<circular-reference>"
            seen.add(oid)

        if isinstance(obj, Mapping):
            result = {
                k: self.replacement
                if isinstance(k, str) and self._redact_key(k)
                else self._redact(v, seen)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            result = [self._redact(v, seen) for v in obj]
        elif isinstance(obj, tuple):
            result = tuple(self._redact(v, seen) for v in obj)
        elif isinstance(obj, set):
            result = {self._redact(v, seen) for v in obj}
        elif isinstance(obj, frozenset):
            result = frozenset(self._redact(v, seen) for v in obj)
        else:
            return obj

        seen.remove(oid)
        return result
