# Architecture Context (AI-Oriented Summary)

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Dokumen ini menyediakan ringkasan arsitektur tingkat tinggi AetherOS yang dirancang khusus untuk mempermudah pemetaan mental kognitif model AI.

---

## 1. Hubungan Kesetaraan Konseptual (Symmetric Architectural Mapping)

Untuk menjaga keselarasan filosofis, struktur tata kelola AI pada **AI Operating Environment (AI-OE)** dirancang secara simetris dengan **Runtime Platform** AetherOS:

| Runtime Platform Component | AI Operating Environment Equivalent | Penjelasan Fungsional |
|---|---|---|
| **Bootstrap Engine** | [AI Bootstrap](../00_bootstrap/bootstrap.md) | Langkah booting inisialisasi awal. |
| **Runtime Registry** | [Context Registry](../02_context/project_context.md) | Sumber metadata keadaan proyek. |
| **Runtime Descriptor** | [Knowledge Descriptor](../02_context/architecture_context.md) | Identitas arsitektur platform. |
| **Runtime Graph** | [Discovery / Dependency Resolver](../02_context/discovery.md) | Pengatur dependensi dan relasi penemuan berkas. |
| **Composition Profile** | [Governance Composition](../01_constitution/constitution.md) | Profil aturan yang membatasi lingkungan kerja. |
| **Lifecycle** | [AI Lifecycle](../00_bootstrap/bootstrap.md) | Siklus daur hidup sesi model AI. |
| **Health Evaluation** | [Review & Self-Compliance](../03_protocol/review.md) | Audit kepatuhan arsitektur (Drift Detection). |
| **Capability Resolution** | [Context Resolution](../03_protocol/execution.md) | Resolusi kebutuhan pengerjaan tugas. |

---

## 2. Ringkasan Lapis Arsitektur AetherOS (Layering Overview)

AetherOS beroperasi dengan pembagian 5 lapisan vertikal yang ketat:

1. **Layer 0: Kernel & Platform (`core/kernel/`, `core/execution/`, `core/kernel/sys_platform/`)**
   - *Kernel*: In-memory registry, dispatcher, supervisor, diagnostics.
   - *Execution Engine*: Sandbox, pool executor, cancel token, retry/timeout policies.
   - *Runtime Platform*: Bootstrap, registry subsistem, graph dependensi topologis, dan resolusi kapabilitas.
2. **Layer 1: Subsystems (`storage/`, `repository/`, `artifact/`, `workspace/`)**
   - subsistem fungsional yang beroperasi secara terisolasi tanpa ada hubungan dependensi horizontal.
3. **Layer 2: Workspace Application Layer (`workspace-app/`)**
   - Orkestrator use-case menggunakan pola segregasi Command/Query (CQRS Handlers) dan Middleware Pipeline.
4. **Layer 3: Organization Layer (`organization/`)**
   - Operating Context tertinggi yang membawahi identitas organisasi, directory membership (manusia & AI), RBAC, global policies, dan structured audit log.
5. **Layer 4: Intelligence Layer (`ROADMAP.md` M4+)**
   - Masa depan: *Company Brain* (Knowledge Orchestrator), *Agent Runtime*, *Workflow Runtime*.

---

## 3. Resolusi Berbasis Kapabilitas (Capability Architecture)

Interaksi lintas subsistem tidak boleh memanggil modul konkret secara langsung. Hubungan diselesaikan menggunakan **Capability-Based Resolution**:
- Subsistem bawah mendaftarkan kemampuannya sebagai kapabilitas terstruktur (`CapabilityDescriptor`, contoh: `storage.read`, `storage.write`).
- Subsistem atas menyatakan kebutuhannya di bagian deskriptor manifest (`requires`).
- Platform menyambungkan dependensi tersebut secara otomatis saat booting bootstrap.
