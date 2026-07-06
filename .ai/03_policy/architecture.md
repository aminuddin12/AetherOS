# Architecture Policy

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Kebijakan ini menetapkan aturan struktural arsitektur sistem operasi AetherOS yang wajib dipatuhi oleh seluruh perubahan kode sumber.

---

## 1. Aturan Dependensi Vertikal (Vertical Isolation Policy)
- **Bottom-Up Stream**: Semua impor modul hanya boleh mengalir dari tingkatan bawah ke atas secara vertikal:
  `Level 0 (Kernel/Execution/SysPlatform) -> Level 1 (Subsystems) -> Level 2 (Workspace App) -> Level 3 (Organization) -> Level 4 (Brain)`.
- **Horizontal Import Ban**: Larangan mutlak melakukan impor konkret melintang horizontal antara sesama subsistem di Level 1.
- **Kernel Purity Protection**: Modul Kernel (`core/kernel/`) dilarang keras mengimpor subsistem tingkat atas (Storage, Repository, Artifact, Workspace, dll) baik secara langsung maupun dinamis.

---

## 2. Capability Resolution Policy
- Semua komunikasi lintas subsistem wajib dideklarasikan secara tertulis di berkas `manifest.yaml` masing-masing subsistem menggunakan format kapabilitas:
  - `Provides`: Kapabilitas yang diekspos secara publik.
  - `Requires`: Kapabilitas eksternal yang dibutuhkan subsistem untuk beroperasi.
- Instans konkret subsistem hanya boleh di-host dan dipanggil melalui `RuntimeManager` setelah divalidasi oleh `CapabilityResolver` pada fase booting Kernel.
