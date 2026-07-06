# ADR-0020: Semantic Resource Architecture

## Status
Accepted

## Context
As AetherOS scales its Knowledge Layer, we must prevent tight coupling between core runtimes (Storage, Repository, Artifact, Workspace, Company Brain). Storing complex objects directly inside one another causes synchronization issues and massive technical debt.

## Decision
All interactions between runtimes MUST be conducted through **Resource URIs** combined with **Reference Objects**.
- Runtimes do not "store" objects from other runtimes; they store *URIs* pointing to those objects.
- Runtimes act as autonomous microservices within the AetherOS context.
- E.g., The Artifact Runtime does not hold a blob; it holds `storage://bucket/blob-id` as its payload reference.

## Consequences
- **Positive**: Complete decoupling of domains. Any runtime can be replaced, updated, or re-indexed without corrupting other domains. Company Brain acts purely as an orchestrator, not a database.
- **Negative**: Resolving a full semantic object requires traversing multiple runtimes (e.g., Brain -> Artifact -> Repository -> Storage).
