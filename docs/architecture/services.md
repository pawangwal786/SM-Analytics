# Service Architecture

This document describes the high-level service architecture for the SM Analytics platform. It serves as the definitive reference for service responsibilities, ownership boundaries, and deployment patterns as the platform evolves.

## High-Level Architecture

The backend follows a microservice architecture augmented with distinct execution domains for analytics and data processing. The system is split into the following domains:

- **Services** (`backend/services/`): HTTP/gRPC business services exposing APIs.
- **Engines** (`backend/engines/`): Specialized analytical processors (e.g., screening, backtesting, ML).
- **Ingestion** (`backend/ingestion/`): Market data collection, ETL, and feed handlers.
- **Workers** (`backend/workers/`): Background task processors for asynchronous jobs.
- **Libraries** (`backend/libs/`): Shared infrastructure code (e.g., database sessions, caching, telemetry).

## Initial Services

Currently, the platform hosts three core services:

### 1. Gateway (`gateway`)
- **Purpose**: The unified entry point for external API consumers.
- **Responsibilities**:
  - Authentication middleware (validating JWTs).
  - Rate limiting and throttling.
  - Reverse proxy logic to route requests to backend services.
  - API aggregation and request validation.
  - Telemetry (tracing, request IDs).

### 2. Auth Service (`auth`)
- **Purpose**: Centralized authentication and authorization.
- **Responsibilities**:
  - User login, OAuth integration, and JWT issuance.
  - Password hashing and management.
  - Token validation logic.
- **Dependencies**: PostgreSQL, Redis.

### 3. Users Service (`users`)
- **Purpose**: Manages user profiles, preferences, and account states.
- **Responsibilities**:
  - CRUD operations for user profiles.
  - Tracking account settings and subscriptions.
- **Dependencies**: PostgreSQL.

## Architecture Rules & Guidelines

To maintain a healthy, decoupled ecosystem, all services must adhere to the following rules:

### 1. Service Layout
Every business service must maintain a standardized top-level structure to ensure operational predictability. However, **every service should contain only the packages required by its current architectural responsibilities**. Shared conventions (e.g., `api/`, `core/`, `tests/`, `main.py`) are consistent, while optional packages (`db/`, `models/`, `repositories/`, etc.) are present only when the service owns those concerns. Do not create empty directories for the sake of uniformity.

```text
service_name/
├── app/
│   ├── api/            # Required for all API services
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── router.py
│   ├── core/           # Required for all services
│   │   ├── config.py
│   │   └── logging.py
│   ├── db/             # Optional (only if service persists data)
│   │   └── migrations/
│   ├── models/         # Optional
│   ├── repositories/   # Optional
│   ├── schemas/        # Optional
│   └── services/       # Optional (business logic)
├── tests/              # Required
├── main.py             # Required
├── pyproject.toml      # Required
├── Dockerfile          # Required
├── .env.example        # Required
└── README.md           # Required
```

### 2. Database & Migrations
- **Per-Service Ownership**: Each service owns its database schema and handles its own migrations (via `app/db/migrations/`).
- **No Shared Data Access**: Services must not query another service's database directly. All cross-domain data access must go through the owner service's API (HTTP/gRPC) or via asynchronous events.

### 3. Shared Libraries (`libs/`)
- **Infrastructure Only**: The `libs/` directory must only contain generic utilities, framework integrations, and cross-cutting concerns. Create a shared library only when there is a concrete, reusable responsibility shared by multiple services.
- **No Business Logic**: Do not place domain-specific logic in shared libraries. E.g., `libs/security` handles JWT verification algorithms, not user login workflows.
- **Strict Dependency Direction**:
  - `Service -> Shared Library`: Services may import from shared libraries.
  - `Shared Library ✗ Service`: Libraries must **never** import code from a service to prevent circular dependencies.
  - `Service A ✗ Service B`: Services must **never** import from one another. Communication should occur through APIs or events.
- **Packaging**: Avoid creating per-library `pyproject.toml` files to minimize operational overhead. Instead, use a single workspace configuration (`backend/pyproject.toml`) that manages the dependency graph, build system, and tooling configuration for all internal libraries and services. Each library remains isolated as a standard python package (`README.md`, `__init__.py`) within the workspace.

### 4. Communication Model
- **Synchronous**: REST over HTTP (and eventually gRPC) for immediate request-response cycles.
- **Asynchronous**: Event-driven communication via message brokers (e.g., Kafka) will be introduced for background processing and loose inter-service notifications in future phases.

### 5. API Versioning
- All service APIs must be versioned explicitly from inception (e.g., `/api/v1/`). This prevents future breaking changes from impacting existing consumers.

### 6. Observability
- **Canonical Log Schema**: All services must emit structured JSON logs that conform to a strict, versioned contract to ensure compatibility with downstream indexers (e.g., OpenSearch, Datadog, Elasticsearch).
  The canonical schema is:
  ```json
  {
    "timestamp": "2026-07-19T12:00:00Z",
    "level": "INFO",
    "service": "auth",
    "environment": "development",
    "logger": "app.core.logic",
    "module": "logic",
    "function": "process_login",
    "line": 42,
    "message": "User login successful",
    "request_id": "uuid-...",
    "correlation_id": "uuid-...",
    "duration_ms": 12.4,
    "trace_id": null,
    "span_id": null,
    "exception": null
  }
  ```
- **Exception Structure**: The `exception` field must not be flattened into a single string. When an exception occurs, it must be logged as a structured object:
  ```json
  "exception": {
    "type": "ValueError",
    "message": "Invalid credentials",
    "traceback": "..."
  }
  ```
- **Metadata Over Payloads**: Never log entire HTTP request or response bodies by default. Logs should capture metadata (method, path, status, latency) only.
