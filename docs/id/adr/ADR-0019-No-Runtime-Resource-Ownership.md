# ADR-0019: No Runtime Resource Ownership

## Status
Accepted

## Context
As AetherOS evolves into a Knowledge Platform, determining where "Data" lives becomes complicated. If `Repository` stores files, and `Storage` stores files, and `Artifact` stores data, it creates massive duplication and synchronization conflicts.

## Decision
We enforce a strict **No Runtime Resource Ownership** policy, governed by the following Runtime Ownership Matrix:

| Runtime       | Owns                                                | Never Owns        |
| ------------- | --------------------------------------------------- | ----------------- |
| Storage       | Blob, Streams                                       | Metadata, History |
| Repository    | Revision, Branch, Graph                             | Blob              |
| Artifact      | Identity, Metadata, Lineage, Semantic Relationships | Blob, Revision    |
| Workspace     | Context, Lifecycle, Policy                          | Blob              |
| Company Brain | Knowledge Graph, Embeddings, Reasoning Index        | Blob, Revision    |

Integrasi lintas runtime WAJIB menggunakan `ResourceURI` dan `Reference Objects`, tanpa pernah menduplikasi _blob_ atau kepemilikan.

## Consequences
- **Positive**: Zero data duplication. Clear boundaries. Highly scalable.
- **Negative**: Retrieving a single complex entity requires resolving URIs across multiple runtimes.
