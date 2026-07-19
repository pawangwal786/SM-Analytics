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
                re.compile(p, re.IGNORECASE) for p in (patterns or self.DEFAULT_PATTERNS)
            )
        except re.error as e:
            raise ValueError(f"Invalid redaction pattern: {e}") from e

    def _redact_key(self, key: str) -> bool:
        key = key.strip().lower()
        return key in self.keys or any(p.search(key) for p in self.patterns)

    def redact(self, obj: Any) -> Any:
        return self._redact(obj, set())

    def _redact(self, obj: Any, seen: set[int]) -> Any:
        if isinstance(obj, Mapping | list | tuple | set | frozenset):
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
