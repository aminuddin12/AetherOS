# ADR-0018: Architecture Runtime Standard

## Status
Accepted

## Context
AetherOS runs on multiple specialized runtimes (Workspace, Storage, Repository, Artifact, etc.). Previously, the internal structure of each runtime varied depending on the implementation milestone, leading to an inconsistent developer experience.

## Decision
All runtimes MUST implement a standardized directory layout ensuring Single Responsibility Principle at the package level:

- `core/`: Pure domain models, aggregates, and entities. No infrastructure code.
- `protocols/`: Abstract definitions (interfaces) for backend dependencies.
- `adapters/`: Concrete implementations of `protocols/` (e.g., Memory, Git, S3).
- `events/`: Event sourcing models and payloads.
- `lifecycle/`: State machine, boot, and shutdown sequences.
- `diagnostics/`: Health checks, metrics, capabilities tracking.
- `policies/`: Governance rules (RBAC, retention, protection).
- `references/`: Reference objects pointing to Resources (`ResourceURI`).
- `application/`: CQRS pattern (Commands & Queries) for orchestration.
- `exceptions/`: Domain-specific error hierarchies.
- `tests/`: Unit and integration test suites.

## Consequences
- **Positive**: Extremely predictable codebase. Developers learning one runtime instantly understand the architecture of all other runtimes.
- **Negative**: High initial boilerplate for simple packages.
