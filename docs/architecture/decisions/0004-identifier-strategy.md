# ADR 0004: Identifier Strategy

## Status
Accepted

## Context
Decisions around primary keys, data references, and lookup identifiers are difficult and expensive to change after migrations and data are established. We must establish a consistent strategy for how entities identify themselves and how they relate to one another across service boundaries.

## Decision
1. **Primary Key Strategy (UUID v4)**: All primary entities will use UUID v4 as their primary key.
2. **Soft References Between Services**: Foreign Keys will *not* be enforced at the database level across service boundaries (e.g., `profiles.user_id` will not have a DB-level FK constraint pointing to `auth.users.id`). These will be soft UUID references.
3. **One-to-One Relationships**: For true one-to-one extensions of identity (like `Profile` and `Preference` extending a user), the referenced `user_id` will serve as the Primary Key for the table. We will not introduce unnecessary surrogate UUIDs for these records.
4. **Many-to-Many Relationships**: Pure many-to-many associations (e.g., `user_roles`) will be represented as association tables with composite primary keys, not as separate entities with their own UUIDs.
5. **Canonical Login Identifier**: `email` is the canonical login identifier. `username` is strictly a presentation/display attribute.

## Consequences
- **Positive**: UUID v4 allows decentralized ID generation, easier replication, and frictionless future sharding.
- **Positive**: Soft references ensure that migrating the `Users` service to an independent PostgreSQL cluster in the future requires zero database migrations to drop FK constraints.
- **Positive**: Composite keys on association tables prevent bloat and improve query locality.
- **Negative**: Without DB-level FKs across services, referential integrity (e.g., handling orphaned profiles when a user is deleted) becomes an application-level orchestration responsibility.
