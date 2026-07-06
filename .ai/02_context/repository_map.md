# Repository Navigation Map

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Peta Navigasi Repositori ini memetakan tanggung jawab setiap direktori di dalam repositori AetherOS agar model AI tidak salah menempatkan kode atau melanggar batas isolasi subsistem.

---

## 🗺️ Peta Direktori Utama (Directory Responsibility Map)

| Direktori | Tanggung Jawab Utama | Batas Dependensi Impor | Konvensi Khas |
|---|---|---|---|
| **`core/kernel/`** | Microkernel sistem: DI, registry, dispatcher, supervisor. | Hanya boleh mengimpor dari `core/contracts/`. | Kode harus murni bebas komentar. |
| **`core/execution/`** | Sandbox execution, pool executor, cancelling, retry, timeout. | Hanya memanggil public API Kernel dan Contracts. | Menggunakan executor SPI. |
| **`core/kernel/sys_platform/`** | Pendaftaran subsistem, graph dependensi, capability resolution. | Mengatur siklus hidup subsistem. | Konsep simetris dengan AI-OE. |
| **`runtime/`** | Gerbang SDK terpadu (`AetherRuntime`). | Fasad tunggal untuk seluruh subsistem eksternal. | `api.md` mendefinisikan stabilitasnya. |
| **`storage/`** | Content-Addressable Storage (CAS) berkas fisik. | Hanya bergantung pada SDK dan Contracts. | Menggunakan skema `storage://`. |
| **`repository/`** | Pelacakan riwayat versi dan Graf Revisi. | Bergantung pada Storage untuk data fisik. | Menggunakan skema `repository://`. |
| **`artifact/`** | Dokumen semantik, klasifikasi, silsilah lineage. | Bergantung pada Repository. | Menggunakan skema `artifact://`. |
| **`workspace/`** | Aggregate Root isolasi operasional proyek. | Bergantung pada SDK dan Contracts. | Menggunakan skema `workspace://`. |
| **`workspace-app/`** | Orkestrasi use-case aplikasi, Command/Query Handlers. | Mengimpor kontrak subsistem di bawahnya (Level 1 & 0). | Mengandung Command/Query Bus. |
| **`organization/`** | Operating Context tertinggi, directory membership, global policies. | Memanggil Workspace App melalui SDK Facade. | Logika audit trail disimpan di sini. |
| **`docs/`** | Buku arsitektur, spesifikasi subsistem, ADR, dan RFC. | Sumber kebenaran dokumentasi tertulis. | Divalidasi oleh test suite. |
| **`.ai/`** | Konstitusi, protokol, dan peta operasi model AI (AI-OE). | Di-mount otomatis saat bootstrap AI. | Penulisan markdown hierarkis. |

---

## 🚦 Aturan Lokasi Penulisan Kode (Where Code Belongs)

- **Jika Anda menulis DTO atau primitives baru**: Letakkan di bawah `core/contracts/` dan pastikan model bersifat `frozen=True`.
- **Jika Anda memodifikasi query/command use-case**: Letakkan di bawah `workspace-app/src/aether_workspace_app/application/`.
- **Jika Anda memperbaiki cara penanganan event platform**: Letakkan di bawah `core/kernel/sys_platform/events.py`.
- **Dilarang keras**: Membuat package baru di root direktori tanpa mendaftarkannya ke dalam `workspace.members` di `pyproject.toml` utama.
