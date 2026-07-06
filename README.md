# AetherOS: The Open Agent Operating System

---
Status: Implemented
Version: 2.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
Implementation Status: Core Foundation Implemented (M1 - M3.5)
---

## 1. What is AetherOS?

AetherOS bukanlah sebuah *AI Agent Framework* biasa untuk membuat *standalone chatbots*. AetherOS adalah sebuah **Sistem Operasi Agen Terbuka (Open Agent Operating System)** berskala penuh yang dirancang dari nol untuk menjalankan, mengoordinasikan, dan mengamankan kolaborasi berskala besar antara agen AI (*Agent Workers*) dan manusia dalam lingkup tata kelola organisasi.

---

## 2. Visi & Filosofi

### "Build Organizations, not Agents"
Membuat agen AI pintar yang bekerja sendiri (seperti asisten personal) tidaklah cukup untuk menyelesaikan tantangan operasional perusahaan modern. Visi AetherOS adalah mempermudah perancangan **Organisasi Berbasis Kecerdasan Buatan (AI-Driven Organizations)**.

AetherOS bertindak sebagai "jantung" komputasi sosial dan kognitif, menyediakan abstraksi sistem operasi tradisional (Kernel, Sandbox, Version Control, I/O Storage, Identitas, Izin Akses) yang disesuaikan secara khusus bagi agen kecerdasan buatan.

---

## 3. Why AetherOS Exists?

- **Pemisahan Kognisi dan Infrastruktur**: Developer agen AI sering kali dipusingkan dengan cara melakukan pembacaan/penulisan file secara aman, integrasi Git, dan penyimpanan memori. AetherOS menangani semua urusan infrastruktur ini di tingkat sistem operasi (*System Level*), membebaskan developer agen AI untuk berfokus pada logika nalar (*cognitive/reasoning logic*).
- **Keamanan Sandboxed by Default**: Seluruh eksekusi kode atau perintah terminal oleh agen diproteksi melalui engine eksekusi terisolasi untuk mencegah eksploitasi lingkungan host.
- **Bahasa Komunikasi Universal**: Komponen internal berkomunikasi menggunakan URI (`workspace://`, `artifact://`, `storage://`) untuk memastikan portabilitas tinggi melintasi sistem terdistribusi.

---

## 4. High-Level Architecture

Sistem AetherOS dibangun murni secara *bottom-up* dengan arah ketergantungan vertikal yang ketat:

```text
               ┌────────────────────────┐
               │      Company Brain     │  <-- Layer 4: Intelligence (M4)
               └───────────┬────────────┘
                           │
               ┌───────────▼────────────┐
               │   Organization Core    │  <-- Layer 3: Organization (M3.5)
               └───────────┬────────────┘
                           │
               ┌───────────▼────────────┐
               │ Workspace Application  │  <-- Layer 2: Orchestration (CQRS) (M3.4)
               └─────┬───┬───┬───┬──────┘
                     │   │   │   │
        ┌────────────┘   │   │   └────────────┐
        ▼                ▼   ▼                ▼
 ┌─────────────┐ ┌───────────┐ ┌────────────┐ ┌────────────┐
 │  Workspace  │ │  Storage  │ │ Repository │ │  Artifact  │ <-- Layer 1: Subsystems (M3.0 - M3.3)
 └─────────────┘ └───────────┘ └────────────┘ └────────────┘
        │                │           │                │
        └────────────┐   │   ┌───────┘                │
                     ▼   ▼   ▼                        ▼
               ┌────────────────────────┐
               │      Runtime SDK       │  <-- Facade (Syscall API) (M2.7)
               └───────────┬────────────┘
                           │
               ┌───────────▼────────────┐
               │   Execution & Kernel   │  <-- Layer 0: System Kernel (M1 - M2)
               └────────────────────────┘
```

---

## 5. Current Implementation & Milestone

AetherOS saat ini berada pada **Milestone 3.7 (Runtime Platform & Bootstrap Architecture)**.

### Status Implementasi Subsistem:
- **Kernel & Execution Engine**: Selesai diimplementasikan secara fungsional.
- **Runtime Platform & Bootstrap**: Pendaftaran runtime, capability resolution, dan dependency graph selesai dibangun (`sys_platform/`).
- **Runtime SDK**: Fasad universal telah diuji dan berjalan stabil.
- **Storage, Repository, Artifact, Workspace**: Seluruh sub-sistem domain organisasi telah selesai di-deploy.
- **Organization Core**: Domain identitas multidimensi, RBAC, dan audit trail telah didefinisikan secara matang.

---

## 6. Repository Structure

```text
AetherOS/
├── .ai/                 # AI Governance System & Operating Protocols
├── core/                # Layer 0: Kernel, Execution & Platform Engine
├── runtime/             # SDK Facade (AetherRuntime)
├── workspace/           # Subsystem: Workspace Domain
├── storage/             # Subsystem: Content-Addressable Storage
├── repository/          # Subsystem: Revision Graph Repository
├── artifact/            # Subsystem: Semantic Artifact Registry
├── workspace-app/       # Layer 2: CQRS & Orchestration Bus
├── organization/        # Layer 3: Organization Context
├── docs/                # Dokumentasi Arsitektur & Panduan
└── tests/               # Unit & Integration Test Suites
```

---

## 7. Roadmap 2.0

- ✅ **M1**: Kernel Runtime
- ✅ **M2**: Execution Engine & CLI
- ✅ **M3.0–3.4**: Workspace & Application Runtime
- ✅ **M3.5**: Organization Runtime
- ✅ **M3.6**: Documentation Governance
- ✅ **M3.7**: Runtime Platform & Bootstrap Architecture
- ⏳ **M4**: Company Brain (Knowledge Orchestrator)
- ⏳ **M5**: Agent Runtime
- ⏳ **M6**: Provider Runtime
- ⏳ **M7**: Workflow Runtime
- ⏳ **M8**: Constitution Runtime
- ⏳ **M9**: Distribution Packs
- ⏳ **M10**: Aether Studio (Web Dashboard)

---

## 8. Documentation Navigation

Seluruh dokumentasi terperinci dikelola menggunakan hierarki tergovermentasi di bawah folder `docs/`:

1. **Konstitusi Utama**: [AetherOS System Architecture Book](docs/id/architecture/book.md)
2. **AI Governance**: [AI Governance System](.ai/GOVERNANCE.md)
3. **Spesifikasi Subsistem**:
   - [Kernel Subsystem](docs/id/runtime/kernel.md)
   - [Execution Subsystem](docs/id/runtime/execution.md)
   - [Runtime SDK Subsystem](docs/id/runtime/runtime-sdk.md)
   - [Workspace Subsystem](docs/id/runtime/workspace.md)
   - [Storage Subsystem](docs/id/runtime/storage.md)
   - [Repository Subsystem](docs/id/runtime/repository.md)
   - [Artifact Subsystem](docs/id/runtime/artifact.md)
   - [Organization Subsystem](docs/id/runtime/organization.md)
4. **Catatan Keputusan Arsitektural**: [Architecture Decision Records (ADR) Log](docs/id/adr/README.md)
5. **Catatan Diskusi Fitur**: [RFC Index](docs/id/rfc/README.md)
6. **Glosarium Istilah**: [Definisi Istilah Baku AetherOS](docs/id/glossary/index.md)

---

## 9. Contribution & Governance

Pengembangan kode AetherOS diatur secara ketat melalui aturan tata tertib kualitas. Silakan merujuk ke **[Developer Onboarding Guide](docs/id/getting-started/quickstart.md)** sebelum mengajukan Pull Request baru. Model AI yang berkontribusi wajib mengikuti aturan **[AI Governance System](.ai/GOVERNANCE.md)**.

