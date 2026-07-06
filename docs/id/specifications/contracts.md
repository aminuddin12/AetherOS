# Core Contracts Specification

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
Depends On: docs/id/architecture/book.md
Required Reading: docs/id/getting-started/coding-standard.md
Related ADR: ADR-0021
---

## 1. Definisi Kontrak (Contracts)
Kontrak di AetherOS adalah definisi DTO (*Data Transfer Object*) dan *Domain Primitive* yang bersifat murni (*pure*) dan dibagikan secara global ke seluruh sub-sistem. Kontrak dideklarasikan di bawah folder `core/contracts/`.

## 2. Karakteristik Kontrak
1. **Immutable**: Semua objek dideklarasikan menggunakan Pydantic V2 dengan setelan `frozen=True` untuk menjamin data tidak mengalami mutasi selama proses routing.
2. **Strict Validation**: Pydantic melakukan penegakan skema secara agresif sebelum data menyentuh logika bisnis.
3. **No Logic**: Kontrak hanya memuat struktur data, tanpa mengandung logika operasional.

## 3. Sub-Domain Kontrak Utama
- `base`: Abstraksi DDD tingkat dasar (Entity, ValueObject, DomainEvent).
- `common`: Struktur data bersama (Trace, Context, UserCredential).
- `event`: Event dan pesan CQRS (Command, Query, Event).
- `identity`: Model keanggotaan, identitas, dan RBAC.
- `workspace`: Model WorkspaceDescriptor, WorkspaceManifest, dan LockLease.
- `storage`: Model StorageDescriptor dan BlobMetadata.
- `repository`: Model Commit, Branch, dan RevisionGraph.
- `artifact`: Model ArtifactMetadata, LineageNode, dan ProjectionSchema.
