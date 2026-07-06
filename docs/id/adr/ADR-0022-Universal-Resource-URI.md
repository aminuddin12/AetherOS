# ADR-0022: Universal Resource URI

## Status
Accepted

## Context
AetherOS memiliki berbagai entitas dari beragam runtime (Workspace, Storage, Repository, Artifact, dll). Mengidentifikasi sebuah entitas dengan cara yang berbeda-beda (misalnya menggunakan *path file* lokal, ID database, atau URL) akan menyulitkan orkestrasi lintas-domain, terutama oleh Company Brain.

## Decision
Seluruh *resource* di dalam ekosistem AetherOS direpresentasikan dan diakses menggunakan skema **Universal Resource URI**.

Format baku yang diadopsi adalah `scheme://authority/path?query`.

Skema yang dikenali:
- `storage://...` (Physical Blob/Streams)
- `repository://...` (Version Control & Graphs)
- `artifact://...` (Semantic Knowledge & Classification)
- `workspace://...` (Context & Identity)
- `brain://...` (Intelligence & Reasoning)

Company Brain dan sistem *Resolver* akan menggunakan URI ini sebagai bahasa universal komunikasi antar-node semantik.

## Consequences
- **Positive**: Seluruh komponen berbicara dengan protokol penamaan yang sama.
- **Negative**: Parsing URI dan resolver engine menjadi kompleks.
