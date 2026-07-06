# ADR-0028: Runtime Platform Architecture

## Status
Accepted

## Context
AetherOS berkembang menjadi platform sistem operasi modular untuk koordinasi agen kognitif. Subsistem seperti Workspace, Storage, Repository, Artifact, dan Organization sebelumnya dikembangkan secara terpisah dan didaftarkan manual ke SDK Facade. Tanpa adanya standardisasi platform yang mengelola siklus hidup, kapabilitas, dan dependensi lintas runtime, penambahan subsistem baru seperti Company Brain (M4) atau Agent Runtime (M5) akan memaksa perubahan di tingkat Kernel. Diperlukan abstraksi penengah yang memisahkan Kernel dari subsistem runtime secara generik.

## Decision
Disahkan pembangunan **Runtime Platform & Bootstrap Architecture** di tingkat Kernel dengan prinsip konstitusi berikut:

1. **Kernel SHALL depend only on Runtime Platform abstractions and SHALL NOT directly depend on application runtimes.**
2. **All runtime-to-runtime interactions SHALL be resolved through declared capabilities rather than concrete implementations.**

### 1. Model Data Platform
- **RuntimeDescriptor**: Metadata statis immutable yang dihasilkan dari **Runtime Manifest** (`manifest.yaml`).
- **RuntimeState**: Mengelola state mutable operasional runtime (lifecycle, health, metrics, last error).
- **CapabilityDescriptor**: Karakteristik kapabilitas terstruktur (ID, nama, versi, provider, kontrak input/output, criticality).

### 2. Daur Hidup & Kesehatan Terpisah
- **Lifecycle States**: `Created -> Discovered -> Registered -> Resolved -> Initialized -> Starting -> Running -> Ready -> Stopping -> Stopped -> Shutdown`.
- **Health States**: `HEALTHY`, `DEGRADED`, `FAILED`.

### 3. Bootstrap Engine
Mengonsolidasikan proses booting dalam satu entrypoint terurut:
`Discovery -> Registry -> Graph -> Resolution -> Initialization -> Ready`.

### 4. Dependency Impact Analysis
Menggunakan analisis dampak dependensi terstruktur untuk derived health. Subsistem atas beralih ke `DEGRADED` (bukan kaskade `FAILED`) jika kehilangan kapabilitas opsional.

## Consequences
- **Positive**: Kernel murni terisolasi. Seluruh subsistem baru dideklarasikan sebagai plug-in runtime berbasis kontrak kapabilitas universal.
- **Negative**: Boilerplate deklarasi manifest.yaml wajib dibuat untuk setiap modul subsistem baru.
