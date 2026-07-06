# Testing Standard

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
Required Reading: docs/id/getting-started/coding-standard.md
---

## Aturan Pengujian Kode (Testing Rules)

### 1. In-Memory Execution
- Seluruh pengujian sub-sistem (Kernel, Execution, SDK, Workspace) wajib berjalan secara *in-memory*.
- Dilarang keras membutuhkan koneksi database eksternal (PostgreSQL, Redis, Qdrant) atau panggilan API LLM secara langsung selama proses *Unit Testing*.

### 2. Mocking & Stubs
- Manfaatkan DTO dan antarmuka Protokol dari `core/contracts/` untuk membuat objek mock atau stub saat mensimulasikan interaksi lintas runtime.

### 3. Eksekusi Pytest
- Jalankan pengetesan menggunakan perintah terstandardisasi:
  ```bash
  PYTHONPATH=organization/src:workspace-app/src:artifact/src:repository/src:storage/src:workspace/src:runtime/src uv run pytest
  ```

### 4. Target Kepatuhan Cakupan (Coverage Targets)
- Modul Contracts, Kernel, dan Execution memiliki target cakupan pengujian minimal **100%** menggunakan stub generator untuk mempermudah pengerjaan.
