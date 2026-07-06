# Architecture Context (AI-Oriented Summary)

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Dokumen ini menyediakan gambaran arsitektur tingkat tinggi AetherOS yang dirancang khusus untuk mempermudah pemetaan mental kognitif model AI.

---

## 1. Context Resolution Structure (Struktur Konteks AI-OE)

AI Operating Environment membagi konteks kognitif pengembangan menjadi 6 tipe terpisah untuk diresolusi oleh AI:

1. **Project Context**: Status milestone, tujuan jangka panjang, dan rujukan roadmap aktif ([project_context.md](project_context.md)).
2. **Architecture Context**: Aturan layering, batas dependensi vertikal, invarian, dan status freeze ([architecture_context.md](architecture_context.md)).
3. **Repository Context**: Tanggung jawab direktori konkret dan lokasi penemuan berkas ([repository_map.md](repository_map.md), [discovery.md](discovery.md)).
4. **Implementation Context**: Struktur kode aktual yang saat ini berjalan pada repositori dan test suite koresponden.
5. **Current Development Context**: Instruksi penugasan spesifik (*Task Contract*) yang diberikan oleh Chief Architect.
6. **Runtime Context**: Status kesehatan dan kemampuan yang aktif saat simulasi penugasan dijalankan.

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
