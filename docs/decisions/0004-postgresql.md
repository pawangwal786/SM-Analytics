# ADR 0004 — PostgreSQL

**Status:** Accepted
**Date:** 2026-07-18

## Context
The platform requires a primary relational database to serve as the system of record for users, portfolios, watchlists, metadata, and configuration.

## Decision
We have chosen PostgreSQL as our primary system of record.

## Alternatives Considered

### MySQL / MariaDB
**Pros:** Very popular, easy to set up.
**Cons:** Less advanced JSON support, fewer analytical extensions (like TimescaleDB).

### CockroachDB
**Pros:** Built-in horizontal scalability.
**Cons:** Operational complexity is unnecessary for this phase.

## Consequences
- **Positive:** ACID compliance, mature ecosystem, powerful extensions (e.g., TimescaleDB for time-series data), excellent JSONB support.
- **Negative:** Connection pooling can be challenging at high concurrency (will require PgBouncer or similar).
- **Future:** Time-series data will leverage the TimescaleDB extension built on top of Postgres.

## References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
