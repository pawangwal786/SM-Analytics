# ADR 0002 — Python Version

**Status:** Accepted
**Date:** 2026-07-18

## Context
The backend services require a designated standard Python version to ensure compatibility across development, CI/CD, and production environments.

## Decision
We have selected Python 3.12 (with readiness for 3.13) as the baseline version for all Python-based backend services.

## Alternatives Considered

### Python 3.11
**Pros:** Highly stable and widely supported.
**Cons:** Misses out on recent performance improvements and better typing syntax introduced in 3.12+.

### Python 3.13
**Pros:** Free-threading roadmap, latest performance improvements.
**Cons:** Some third-party packages may lag in compatibility during the initial rollout.

## Consequences
- **Positive:** Access to modern features, typing enhancements, and performance optimizations.
- **Negative:** Forces developers to upgrade their local environments if they are on older versions.
- **Future:** We will actively monitor package compatibility for a smooth transition to 3.13's free-threading features when mature.

## References
- [Python 3.12 Release Notes](https://docs.python.org/3/whatsnew/3.12.html)
