# SM Analytics

> **Status:** Early Development (Phase 0 — Repository Foundation)

---

# Project Overview

SM Analytics is a production-grade Stock Market Analytics Platform designed to provide real-time market data processing, technical analysis, screening, visualization, and analytics for equities, indices, derivatives, and other financial instruments.

The project is inspired by the architecture and capabilities of modern market platforms such as:

- Zerodha Kite
- Groww
- TradingView
- NSE Trading Terminal
- Bloomberg Terminal (scaled-down)
- Chartink
- Trendlyne

The objective is to build a scalable, maintainable, modular, and production-ready platform using modern distributed system principles.

---

# Objectives

The primary goals of this project are:

- Build a production-grade analytics platform
- Design a scalable microservice architecture
- Process real-time market data efficiently
- Support historical and live analytics
- Provide powerful stock screening capabilities
- Deliver advanced charting and visualization
- Implement event-driven data pipelines
- Maintain clean architecture and engineering best practices
- Serve as a long-term engineering portfolio project

---

# High-Level Architecture

```
                    External Market Data
                            │
                            ▼
                  Data Ingestion Services
                            │
                            ▼
                  Streaming / Message Queue
                            │
           ┌────────────────┼────────────────┐
           ▼                ▼                ▼
   Market Data        Analytics Engine   ML Services
     Processing             │
           │                │
           └────────────┬───┘
                        ▼
                Storage Layer
     PostgreSQL • TimescaleDB • Redis
     ClickHouse • ScyllaDB
                        │
                        ▼
                  Backend APIs
                    (FastAPI)
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
        Web Application      Mobile Application
            React                Flutter
```

---

# Tech Stack

## Backend

- Python
- FastAPI
- Java
- Go

## Frontend

- React
- TradingView Lightweight Charts

## Mobile

- Flutter

## Databases

- PostgreSQL
- TimescaleDB
- MySQL (minimal usage)
- ClickHouse
- ScyllaDB

## Cache

- Redis

## Messaging

- Kafka
- NATS
- Benthos

## API Gateway

- Kong
- NGINX
- HAProxy

## Infrastructure

- Docker
- Nomad

## Monitoring

- Grafana
- VictoriaMetrics

---

# Repository Layout

```
sm-analytics/

├── backend/
├── frontend/
├── mobile/
├── infrastructure/
├── deployment/
├── docs/
├── scripts/
├── tools/
├── tests/
├── .github/
├── pyproject.toml
├── Makefile
├── README.md
└── LICENSE
```

> The repository structure will evolve as development progresses.

---

# Development Setup

## Prerequisites

- Git
- Python 3.12+
- Docker
- Docker Compose
- Make
- Node.js (future)
- Flutter SDK (future)

## Clone Repository

```bash
git clone <repository-url>
cd sm-analytics
```

## Install Development Dependencies

Details will be added as development progresses.

---

# Documentation Index

Project documentation is maintained inside the `docs/` directory.

Planned documentation includes:

- Architecture
- Repository Structure
- Development Guide
- Coding Standards
- API Documentation
- Data Pipeline
- Deployment
- Infrastructure
- Testing
- Design Decisions
- ADRs (Architecture Decision Records)

---

# Roadmap

### Phase 0

- Repository Foundation

### Phase 1

- Core Infrastructure

### Phase 2

- Market Data Pipeline

### Phase 3

- Storage Layer

### Phase 4

- Backend Services

### Phase 5

- Analytics Engine

### Phase 6

- Screening Engine

### Phase 7

- Frontend

### Phase 8

- Authentication & Users

### Phase 9

- Monitoring & Observability

### Phase 10

- Production Deployment

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
