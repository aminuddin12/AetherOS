# Repository Manifest & Architecture Freeze Matrix

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Berkas ini mencatat kondisi terkini repositori, status pembekuan arsitektur (*Freeze Matrix*), serta riwayat keputusan yang aktif dalam proyek AetherOS.

---

## 📋 Detail Manifest Repositori

- **Project Name**: AetherOS (Open Agent Operating System)
- **Current Milestone**: Milestone 3.7 Completed / Milestone 4 (Company Brain) - Active Planning
- **System Version**: 2.0.0
- **AI-OE Governance Version**: 1.0.0 (Governance Freeze v1.0)
- **Active Roadmap**: [ROADMAP.md](../ROADMAP.md)

---

## ❄️ Architecture Freeze Matrix

Matriks ini mendefinisikan status pembekuan untuk masing-masing subsistem. Subsistem yang berstatus **FROZEN** tidak boleh diubah kontrak API atau jalurnya tanpa melewati pengajuan RFC/ADR baru secara formal.

| Subsistem / Komponen | Lokasi Folder | Status Pembekuan | Status API Freeze |
|---|---|---|---|
| **Microkernel Core** | `core/kernel/` | **FROZEN** | **FROZEN** (M1.0) |
| **Execution Engine** | `core/execution/` | **FROZEN** | **FROZEN** (M2.0) |
| **Runtime SDK** | `runtime/` | **FROZEN** | **FROZEN** (M2.7) |
| **Workspace Core** | `workspace/` | **FROZEN** | **FROZEN** (M3.0) |
| **Storage Runtime** | `storage/` | **FROZEN** | **FROZEN** (M3.1) |
| **Repository Runtime** | `repository/` | **FROZEN** | **FROZEN** (M3.2) |
| **Artifact Runtime** | `artifact/` | **FROZEN** | **FROZEN** (M3.3) |
| **Organization Core** | `organization/` | **FROZEN** | **FROZEN** (M3.5) |
| **Runtime Platform** | `core/kernel/sys_platform/` | **FROZEN** | **FROZEN** (M3.7) |
| **Company Brain** | `brain/` *(Direncanakan)* | **NOT STARTED** | **NOT STARTED** (M4.0) |

---

## 📝 Indeks Keputusan Aktif (Active Decisions & RFC)

- **ADR Aktif**: [ADR Index](../docs/id/adr/README.md) (ADR-0001 s/d ADR-0028 aktif).
- **RFC Aktif**: [RFC Index](../docs/id/rfc/README.md) (RFC-0001, RFC-0011, RFC-0012, RFC-0013 disetujui).
