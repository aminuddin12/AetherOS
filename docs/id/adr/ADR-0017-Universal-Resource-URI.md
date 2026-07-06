# ADR-0017: Universal Resource URI and Agnostic Storage

## Status
Accepted

## Context
AetherOS will expand to manage multiple forms of resources (Files, Knowledge, Artifacts, Workspaces, Repositories). Addressing them using OS filesystem paths (`/Users/admin/...` or `C:\...`) breaks portability and limits AetherOS to a single execution environment.

## Decision
1. We mandate the use of `ResourceURI` (e.g., `memory://tenant/workspace/data`) as the sole addressing mechanism across all AetherOS layers.
2. The `Storage Runtime` is redefined to process resources, not files. "Filesystem" concepts (VFS) are demoted to merely be one of many Adapters.

## Consequences
- **Positive**: Complete cloud-native flexibility; ready for S3, IPFS, or DB backends without changing domain logic.
- **Negative**: Adds a layer of indirection (URI Parsing and Resolving) compared to simple OS paths.
