# ADR 0005 — Kafka

**Status:** Accepted
**Date:** 2026-07-18

## Context
The platform requires a robust message broker to handle real-time market data, order events, and drive the analytics pipeline in a decoupled, event-driven manner.

## Decision
We will use Apache Kafka as the central nervous system for event-driven communication and streaming.

## Alternatives Considered

### RabbitMQ
**Pros:** Excellent for traditional task queues and AMQP protocols.
**Cons:** Not designed for high-throughput stream processing or message replay.

### Redis Streams
**Pros:** Very low latency, easy to set up.
**Cons:** Data persistence and consumer group management are less robust than Kafka for massive scale.

### NATS / Pulsar
**Pros:** High performance, modern architectures.
**Cons:** Smaller ecosystem and tooling support compared to Kafka.

## Consequences
- **Positive:** Massive scalability, durability, support for message replay, industry standard for market data pipelines.
- **Negative:** High operational overhead and JVM resource requirements.
- **Future:** We may evaluate Redpanda as a drop-in Kafka replacement to reduce operational complexity if JVM tuning becomes an issue.

## References
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
