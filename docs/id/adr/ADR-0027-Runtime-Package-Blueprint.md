# ADR-0027: Runtime Package Blueprint

## Status
Accepted

## Context
Mulai dari Milestone 3.5 (Organization Runtime) hingga pembangunan lapisan Intelligence (Agent, Provider, Workflow, Constitution), setiap runtime semakin menunjukkan pola internal yang sangat seragam. Ketiadaan *blueprint* universal berpotensi menyebabkan ketidakkonsistenan desain API dan struktur internal saat berpindah antar-domain. Melanjutkan prinsip dari ADR-0021, diperlukan *blueprint* komprehensif yang mengikat.

## Decision
Disahkan **Runtime Package Blueprint** sebagai cetak biru arsitektur bagi setiap *Runtime Package* di AetherOS.

### 1. Struktur Direktori Minimum
Setiap package wajib memiliki struktur ini:
- `core/` (Domain Models: Context, Identity, State)
- `references/` (ResourceURI definitions, ex: `WorkspaceReference`)
- `registry/` (Penyimpanan referensi internal)
- `policies/` (Domain Governance, RBAC Rules)
- `lifecycle/` (State Machine)
- `events/` (Domain Events)
- `diagnostics/` (Health, Metrics, Tracing)
- `protocols/` (Backend/Adapter Interfaces)
- `adapters/` (Concrete Implementations)
- `application/` (CQRS / Orchestrator)
- `exceptions/` (Domain Errors)
- `tests/`

### 2. Aturan Dependensi & Komunikasi
- Dilarang menyimpan *instance* objek runtime lain. Semua komunikasi lintas domain HANYA mengandalkan **Reference (ResourceURI)**.
- Dilarang memanggil *internal function* runtime lain. Seluruh panggilan harus didelegasikan melalui **Runtime SDK** (ADR-0025).

### 3. Pola Public API (Facade)
- Fasad runtime tidak lagi menumpuk method dalam satu class besar.
- API Facade harus menggunakan pendekatan *Domain-Driven Dot Notation*. Contoh:
  `runtime.organization.directory.members()`
  `runtime.organization.catalog.resources()`

### 4. Exit Criteria API Freeze
API Freeze sebuah runtime hanya dapat disahkan jika:
1. Seluruh *Domain Models* dan *Protocols* stabil.
2. Tidak ada *blob/state* asing yang salah tempat (ADR-0024).
3. Terintegrasi mulus ke `AetherRuntime` Facade.

## Consequences
- **Positive:** Skala OS (Operating System) dapat diperluas tanpa henti dengan pola *mental model* yang sama.
- **Negative:** Implementasi *blueprint* sangat kaku dan mewajibkan pembuatan lusinan file dasar walau untuk runtime sederhana.
