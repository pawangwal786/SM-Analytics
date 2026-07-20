# ADR 0003: Identity Schema Strategy

## Status
Accepted

## Context
As we build the foundational database schema for the SM Analytics platform across multiple services, we need to decide where identity and user information lives and how it is structured. A monolithic approach would place all user attributes (credentials, preferences, roles, profile details) into a single `users` table. In a microservices architecture, this creates high coupling.

## Decision
We will cleanly separate identity from presentation and preferences:
1. **Auth Service owns `users`**: This table contains only security-critical information: `email` (the canonical login identifier), `password_hash`, `status`, and relationships to roles and permissions.
2. **Users Service owns `profiles` and `preferences`**: These tables contain display attributes (e.g., `username`, `display_name`, `bio`, `avatar_url`) and user configurations (e.g., `timezone`, `language`, `theme`).
3. **No `is_superuser` boolean**: All elevated privileges will be handled purely through Role-Based Access Control (RBAC).

## Consequences
- **Positive**: Clear service boundaries. Security attributes can be strictly audited and protected.
- **Positive**: The `Users` service can evolve presentation data without impacting authentication flows.
- **Negative**: Displaying a user's avatar next to their login email requires querying two different services (or orchestrating the response via an API Gateway/BFF).
