# ADR-0016: Workspace as Pure Aggregate Root

## Status
Accepted

## Context
AetherOS memiliki berbagai Domain Runtime (Storage, Repository, Artifact). Menyuntikkan seluruh logika domain ini secara langsung ke dalam Workspace menyebabkan *tight-coupling*. 

## Decision
Workspace bertindak murni sebagai **Aggregate Root**. Ia tidak memiliki kapabilitas bawaan terkait *VFS* atau *Git*. Workspace hanya memelihara `Context`, `Environment`, `Lifecycle`, dan mengorkestrasi event via `WorkspaceBus`. Fitur-fitur lanjutan akan dikelola oleh *sub-runtimes* yang terdaftar secara dinamis atau disuntikkan via Dependency Injection.

## Consequences
- **Keuntungan**: *Organization Layer* menjadi sangat stabil; kita dapat mengubah *Storage Runtime* dari Local ke S3 tanpa menyentuh *Workspace Core*.
- **Kerugian**: Menuntut desain *Dependency Injection* (DI) yang sangat ketat melalui *Protocols/Interfaces*.
