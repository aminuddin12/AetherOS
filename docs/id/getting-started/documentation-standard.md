# Documentation Standard

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
Required Reading: docs/id/getting-started/coding-standard.md
---

## Aturan Dokumentasi Sistem (Documentation Rules)

### 1. Zero Inline Code Documentation
- **SANGAT KETAT**: Dilarang menulis komentar (`#`) maupun docstring (`"""..."""`) di dalam file Python. Kode harus murni mendokumentasikan dirinya sendiri melalui penamaan semantik.
- Seluruh penjelasan fungsionalitas detail wajib ditulis pada file Markdown (`.md`) eksternal di folder `docs/`.

### 2. Berkas README Sub-sistem
- Setiap sub-folder modul utama (seperti `storage`, `repository`, `workspace`) wajib memiliki file `README.md` lokal yang menerangkan tujuan keberadaan subsistem dan daur hidupnya secara singkat.

### 3. Alur Perubahan Arsitektur (ADR & RFC)
- Setiap perubahan pada antarmuka publik atau struktur sistem operasi wajib dideklarasikan melalui pengajuan **RFC (Request for Comments)**, disusul oleh pembekuan keputusan di **ADR (Architecture Decision Records)**.

### 4. Penggunaan Diagram
- Wajib menyertakan diagram **Mermaid** untuk Sequence Diagram, Lifecycle, atau Dependency Graph saat mendokumentasikan arsitektur sub-sistem utama.
