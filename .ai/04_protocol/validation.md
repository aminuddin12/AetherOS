# AI Validation Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan langkah operasional pengujian kode dan validasi dokumen Markdown di AetherOS.

---

## 1. Protokol Uji Coba Kode (Code Validation)

AI wajib menjalankan validasi kode sumber melalui sekuens perintah shell terstandarisasi berikut:

- **Linting & Syntax Validation**:
  `uv run ruff check .`
- **Dependency Linting (ADR-0025)**:
  `uv run import-linter check`
- **Unit Testing (pytest)**:
  `PYTHONPATH=core/kernel:organization/src:workspace-app/src:artifact/src:repository/src:storage/src:workspace/src:runtime/src uv run python3 -m pytest <path_to_tests>`

---

## 2. Protokol Validasi Dokumentasi (Docs Validation)

Pengecekan integritas dokumen Markdown wajib dijalankan secara manual memanfaatkan alat bantu visual atau pemindaian string:

- **Broken Links check**: AI wajib membaca dan menelusuri pranala relatif dokumen yang baru ditambahkan/diubah. Pastikan rujukan file valid.
- **Mermaid Compliance check**: Pindai diagram Mermaid baru untuk memastikan label node bersimbol khusus dikutip kaku dan tidak mengandung tag HTML.
- **Reference check**: Pastikan rujukan ke ADR/RFC di dalam berkas baru selaras dengan log indeks di `docs/id/adr/` dan `docs/id/rfc/`.
