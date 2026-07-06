# Implementation Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mengatur sinkronisasi dokumen paska penulisan kode. Pengembangan tidak dianggap selesai hanya karena kode Anda berhasil dikompilasi atau ditayangkan. Pekerjaan dinyatakan lengkap jika seluruh ekosistem dokumen pendukung telah diperbarui secara konsisten.

---

## 🔄 Aturan Sinkronisasi Berkas (Artifact Sync Rules)

Setiap kali Anda mengubah kode sumber subsistem, Anda wajib memeriksa matriks dampak di bawah ini dan memperbarui berkas yang bersangkutan secara otomatis:

| Jika Anda Mengubah... | Berkas yang WAJIB Diperbarui secara Sinkron |
|---|---|
| **Antarmuka Publik / Kontrak API** | - `docs/id/adr/` (Tulis ADR baru jika ada perubahan arah desain)<br/>- `docs/id/sdk/api.md` (Update stability status)<br/>- `core/contracts/` (Tambahkan DTO skema baru) |
| **Logic Internal Subsistem** | - `docs/id/runtime/<subsystem>.md` (Update Purpose, API, dan status implementasi)<br/>- `README.md` lokal pada modul (Update tanggung jawab)<br/>- `/tests/` atau sub-folder pengetesan subsistem (Tulis ulang unit test) |
| **Urutan Dependensi Platform** | - `docs/id/architecture/book.md` (Perbarui matriks diagram dependensi)<br/>- `core/kernel/sys_platform/graph.py` (Perbarui node/dependencies) |
| **Rancangan Masa Depan (M4+)** | - `docs/id/architecture/drafts/company-brain-spec.md` (Update spesifikasi kecerdasan)<br/>- `ROADMAP.md` (Geser status pengerjaan milestone) |

---

## 📝 Aturan Penulisan Dokumentasi Tambahan

1. **Gunakan Diagram Mermaid**: Setiap kali ada perubahan daur hidup runtime atau orkestrasi panggilan sistem calls, Anda wajib meregenerasi diagram urutan (*Sequence Diagram*) atau graf transisi pada dokumen spesifikasi runtime terkait.
2. **Kesesuaian Tipe Implementasi**: Jangan pernah menggambarkan *interface* (Protocols) sebagai implementasi konkret, atau stubs tiruan sebagai berkas yang siap digunakan untuk produksi (*production-ready*). Berikan label status yang presisi: `Implemented`, `Partially Implemented`, `Scaffolded`, `Planned`, atau `Deprecated`.
3. **Pembaruan Walkthrough**: Setelah seluruh penulisan kode dan sinkronisasi dokumen selesai, perbarui berkas Walkthrough di direktori artifacts percakapan untuk mencatat riwayat pembaruan yang dapat dipahami oleh Chief Architect.
