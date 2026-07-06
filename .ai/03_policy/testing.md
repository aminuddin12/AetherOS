# Testing Policy

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Kebijakan ini menetapkan persyaratan, batasan, dan target cakupan pengujian unit test dan integrasi di repositori AetherOS.

---

## 1. Aturan Uji Coba Luring & In-Memory (Offline & Mock Policy)

- **Strict Offline Execution**: Semua berkas pengujian dilarang memicu pemanggilan jaringan internet aktif, pemanggilan soket eksternal, atau pemanggilan berbayar API LLM secara live. Seluruh pemanggilan wajib di-mock secara penuh.
- **In-Memory Backend Default**: Pengujian unit subsistem dilarang bergantung pada database fisik aktif (seperti Redis, PostgreSQL, Qdrant). Gunakan memory adapter (`MockStorageAdapter`, `MemoryRepositoryAdapter`) untuk validasi pengetesan.

---

## 2. Cakupan Uji Coba Kritis (Critical Coverage Targets)

- **Contracts & Microkernel Core**: Modul di bawah `core/contracts/` dan `core/kernel/` wajib memiliki cakupan pengujian minimal **100%**.
- **Execution & SDK Platform**: Modul `core/execution/` dan `runtime/` memiliki cakupan pengujian minimal **80%**.
- Seluruh penambahan logika use-case aplikasi (`workspace-app/`) wajib menyertakan berkas unit test koresponden.

---

## 3. Eksekusi Test Suite Terstandardisasi

Semua kontributor wajib mengeksekusi test suite menggunakan PYTHONPATH lengkap berikut untuk menghindari kesalahan modul tidak ditemukan:
```bash
PYTHONPATH=core/kernel:organization/src:workspace-app/src:artifact/src:repository/src:storage/src:workspace/src:runtime/src uv run python3 -m pytest <path_to_tests>
```
