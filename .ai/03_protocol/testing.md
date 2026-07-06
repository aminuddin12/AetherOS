# AI Testing & Documentation Validation Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Berkas ini mendefinisikan standar pengujian unit test dan validasi integritas dokumentasi Markdown yang wajib dijalankan oleh model AI.

---

## 1. Unit Testing & Verification Rules

- **Offline Execution**: Pengujian dilarang memicu panggilan internet atau pemanggilan API LLM eksternal. Gunakan objek Mock atau Stub.
- **In-Memory Backend**: Pengujian dilarang membutuhkan database (Redis, PostgreSQL, Qdrant) aktif secara fisik. Gunakan memory adapter terisolasi.
- **PYTHONPATH Execution**: Eksekusi pytest wajib menggunakan PYTHONPATH yang terstandardisasi:
  ```bash
  PYTHONPATH=core/kernel:organization/src:workspace-app/src:artifact/src:repository/src:storage/src:workspace/src:runtime/src uv run python3 -m pytest <path_to_tests>
  ```

---

## 2. Documentation Validation Protocol (Validasi Dokumen)

Dokumentasi diposisikan sebagai subsistem penting di AetherOS. AI wajib memvalidasi hal berikut pada setiap perubahan berkas Markdown (`.md`):

| Objek Pemeriksaan | Kriteria Kepatuhan Validasi (Compliance Criteria) |
|---|---|
| **Broken Links** | Seluruh tautan relatif wajib divalidasi keberadaannya. Pranala mati dilarang keras. |
| **Cross-References** | Hubungan rujukan antar dokumen arsitektur dan spesifikasi runtime wajib konsisten dengan penamaan folder tergovermentasi. |
| **Mermaid Integrity** | - Node label yang mengandung karakter khusus (seperti tanda kurung) wajib dikutip: `id["Label (Info)"]`.<br/>- Hindari penggunaan tag HTML di dalam label Mermaid untuk mencegah kegagalan render. |
| **Markdown Quality** | Dokumen tidak boleh menjawab "apa" (*what*) saja. Wajib menerangkan batasan tanggung jawab (*Responsibilities vs Non-responsibilities*), dependensi, dan status implementasi. |
| **Navigation Consistency** | Hub navigasi utama ([docs/id/README.md](../../docs/id/README.md)) wajib diperbarui jika berkas spesifikasi baru ditambahkan. |
