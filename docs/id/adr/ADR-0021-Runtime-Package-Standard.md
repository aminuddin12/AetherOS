# ADR-0021: Runtime Package Standard

## Status
Accepted

## Context
Seiring berkembangnya arsitektur AetherOS dari sebuah "AI agent framework" menjadi "Open Agent Operating System", pola struktur kode dari setiap runtime telah bermuara pada satu kesamaan yang konsisten. Ketiadaan standar direktori baku sebelumnya menyebabkan potensi munculnya *technical debt* dan *cognitive load* tinggi bagi kontributor baru.

## Decision
Ditetapkan bahwa **setiap runtime package (Organization Layer dan Knowledge Layer) WAJIB mengikuti standar struktur minimum berikut:**

- `core/`: Agregat dan entitas murni (Domain Model).
- `protocols/`: Abstraksi interface untuk backend dan external dependencies.
- `references/`: Objek referensi (Reference Objects) menuju resource lain.
- `events/`: Definisi payload Event (Event Sourcing).
- `diagnostics/`: Health checks, metrics, dan pemantauan kapabilitas runtime.
- `policies/`: Aturan tata kelola spesifik domain (RBAC, retensi, dll).
- `application/`: CQRS pattern (Commands & Queries), orkestrasi internal.
- `adapters/`: Implementasi konkret dari `protocols/` (misal: S3, Git, Memory).
- `exceptions/`: Hierarki error spesifik domain.
- `tests/`: Unit dan integration test.

Struktur ini memastikan bahwa *AetherOS Subsystems* bertindak layaknya micro-kernel mandiri yang rapi.

## Consequences
- **Positive**: *Cognitive load* mendekati nol saat berpindah antar runtime. Onboarding kontributor baru jauh lebih cepat.
- **Negative**: Sedikit *boilerplate* berlebih pada fase inisialisasi package sederhana.
