# Architecture Decision Records (ADRs)

This directory contains the Architecture Decision Records (ADRs) for the SM Analytics platform.

## What is an ADR?
An Architecture Decision Record (ADR) is a short text file in a specific format that captures an important architectural decision made along with its context and consequences. We use them to keep a historical record of our design choices.

## When to create an ADR?
Create an ADR whenever a significant architectural, technological, or design decision is made that impacts the project's structure, dependencies, or major components.

## ADR Lifecycle
An ADR typically moves through the following states:

1. **Proposed**: The ADR is drafted and under discussion.
2. **Accepted**: The decision has been approved and implemented.
3. **Superseded**: The decision was replaced by a newer ADR.
4. **Deprecated**: The decision is no longer relevant.

**Important**: We never rename or delete old ADRs. If a decision changes, we write a new ADR that supersedes the old one.

## Standard ADR Template
Every ADR should follow this template:

`markdown
# ADR 000X — Title

**Status:** Proposed | Accepted | Superseded by [ADR-XXXX] | Deprecated
**Date:** YYYY-MM-DD

## Context
Why is this decision necessary? What problem are we solving? What constraints exist?

## Decision
Describe the chosen solution. Include rationale.

## Alternatives Considered

### Option A
**Pros:**
**Cons:**

### Option B
**Pros:**
**Cons:**

## Consequences
- Positive consequences
- Negative consequences
- Future considerations

## References
- Links to official documentation
- Relevant discussions
`
"@

 = @"
# ADR 0001 — Project Scope

**Status:** Accepted
**Date:** 2026-07-18

## Context
We need to establish the foundational scope and philosophy for SM Analytics. Without a clear scope, the project risks becoming a monolithic CRUD application rather than a scalable analytics platform.

## Decision
The project will be built as a production-grade Stock Market Analytics Platform. It is an analytics-first platform, not a simple CRUD application. The system will employ a modular, multi-service architecture designed for long-term maintainability and cloud-native deployment.

## Alternatives Considered

### Monolithic Architecture
**Pros:** Easier initial development, simpler local setup.
**Cons:** Harder to scale specific components (e.g., market data ingestion vs. user auth), harder to maintain as complexity grows.

## Consequences
- **Positive:** Scalable, robust, and aligned with modern distributed systems.
- **Negative:** Increased initial complexity and operational overhead.
- **Future:** Services can be independently deployed and scaled on cloud-native infrastructure (e.g., Kubernetes/Nomad).

## References
- System Design references for modern trading platforms
