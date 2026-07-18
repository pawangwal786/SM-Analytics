# ADR 0003 — FastAPI

**Status:** Accepted
**Date:** 2026-07-18

## Context
We need a web framework for our backend APIs. The framework must support asynchronous I/O natively, provide high performance, and integrate well with modern Python type hints.

## Decision
We will use FastAPI for building the platform's API services.

## Alternatives Considered

### Django
**Pros:** Batteries included, excellent ORM, massive ecosystem.
**Cons:** Too heavy for modular/microservice architectures, synchronous by default (though async is improving).

### Flask
**Pros:** Lightweight, highly flexible.
**Cons:** Lacks built-in async support (requires extensions), no native OpenAPI integration.

### Litestar / Falcon
**Pros:** Extremely fast and modern.
**Cons:** Smaller ecosystem and community compared to FastAPI.

## Consequences
- **Positive:** Automatic OpenAPI documentation, native async support, excellent developer experience via type hinting.
- **Negative:** Async complexity (requires understanding of async/await paradigms), dependency management (FastAPI relies on Pydantic and Starlette).
- **Future:** Will require strict adherence to async best practices to avoid blocking the event loop.

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
