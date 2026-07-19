# ADR 0002: Persistence Strategy (PostgreSQL & TimescaleDB)

## Status
Accepted

## Context
The SM Analytics platform requires robust persistence for both standard operational metadata (users, auth, permissions) and high-volume time-series data (market ticks, OHLC data, signals). Using multiple disparate database engines (e.g., PostgreSQL for metadata and InfluxDB/MongoDB for market data) introduces operational overhead, split backup strategies, and fractured ORM ecosystems.

## Decision
We will standardize on a **single persistence technology stack based on PostgreSQL**.
- **PostgreSQL** will handle operational schemas.
- **TimescaleDB** (a PostgreSQL extension) will handle all time-series workloads.

Both will be accessed via **SQLAlchemy 2.x (asyncpg)**.

### Ownership Boundaries
- **PostgreSQL**: Auth, Users, Permissions, Sessions, Configuration, Metadata.
- **TimescaleDB**: OHLC, Trades, Ticks, Indicators, Market Breadth, Signals, Historical Analytics.

## Consequences
### Positive
1. **Unified Infrastructure**: A single connection pooling and transaction strategy across the entire platform.
2. **Simplified ORM**: SQLAlchemy 2.x can natively interact with both standard Postgres tables and TimescaleDB hypertables without bridging multiple client libraries.
3. **Operational Simplicity**: Unified backups, replication, and monitoring tooling (e.g., pg_stat_statements).

### Negative
1. **Compute Coupling**: If deployed on the same physical database instance, heavy analytics queries could theoretically impact metadata latency (mitigated by read replicas later).
2. **Timescale Complexity**: Requires understanding TimescaleDB's hypertable chunking mechanics for optimal performance.
